import random
import uuid
from fastapi import APIRouter, HTTPException, status
from typing import List, Dict

from data.classes import ALL_CLASSES, Skill
from data.races import ALL_RACES
from data.monsters import MONSTERS_BY_FLOOR, Monster
from core.character import Character
from core.stats import Stats
from core.skill_cooldowns import SkillCooldowns
from core.combat import _resolve_attack, _damage_enemy, _use_skill
from persistence.save import (
    save_character,
    load_character,
    list_saved_characters,
    delete_character,
)
from api.schemas import (
    CharacterClassSchema,
    RaceSchema,
    SkillSchema,
    SkillStatusSchema,
    CharacterCreateRequest,
    CharacterResponse,
    ItemSchema,
    MonsterSchema,
    CombatStartRequest,
    CombatStartResponse,
    CombatActionRequest,
    CombatActionResponse,
)

router = APIRouter(prefix="/api")
ACTIVE_COMBATS: Dict[str, Dict] = {}


@router.get("/classes", response_model=List[CharacterClassSchema])
def get_classes() -> List[CharacterClassSchema]:
    result = []
    for cls in ALL_CLASSES.values():
        skills = [
            SkillSchema(
                name=s.name,
                description=s.description,
                cooldown=s.cooldown,
                mana_cost=s.mana_cost,
                skill_type=s.skill_type.name,
                sprite=s.sprite,
            )
            for s in cls.skills
        ]
        result.append(
            CharacterClassSchema(
                name=cls.name,
                description=cls.description,
                base_hp=cls.base_hp,
                base_atk=cls.base_atk,
                base_defense=cls.base_defense,
                base_speed=cls.base_speed,
                base_mana=cls.base_mana,
                skills=skills,
                sprite=cls.sprite,
            )
        )
    return result


@router.get("/races", response_model=List[RaceSchema])
def get_races() -> List[RaceSchema]:
    result = []
    for race in ALL_RACES.values():
        result.append(
            RaceSchema(
                name=race.name,
                description=race.description,
                hp_bonus=race.hp_bonus,
                atk_bonus=race.atk_bonus,
                defense_bonus=race.defense_bonus,
                speed_bonus=race.speed_bonus,
                mana_bonus=race.mana_bonus,
            )
        )
    return result


@router.get("/characters", response_model=List[str])
def get_characters() -> List[str]:
    return list_saved_characters()


@router.post("/characters", response_model=CharacterResponse, status_code=status.HTTP_201_CREATED)
def create_character(req: CharacterCreateRequest) -> CharacterResponse:
    char_class = ALL_CLASSES.get(req.class_name)
    if not char_class:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Classe '{req.class_name}' invalida.",
        )

    race = ALL_RACES.get(req.race_name)
    if not race:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Raca '{req.race_name}' invalida.",
        )

    character = Character.create(name=req.name, character_class=char_class, race=race)
    save_character(character)
    return _build_character_response(character)


@router.get("/characters/{name}", response_model=CharacterResponse)
def get_character(name: str) -> CharacterResponse:
    character = load_character(name)
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Personagem '{name}' nao encontrado.",
        )
    return _build_character_response(character)


@router.delete("/characters/{name}", status_code=status.HTTP_204_NO_CONTENT)
def remove_character(name: str) -> None:
    deleted = delete_character(name)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Personagem '{name}' nao encontrado.",
        )


@router.post("/characters/{name}/advance", response_model=CharacterResponse)
def advance_floor(name: str) -> CharacterResponse:
    character = load_character(name)
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Personagem '{name}' nao encontrado.",
        )
    updated = character.advance_floor()
    save_character(updated)
    return _build_character_response(updated)


def _build_character_response(character: Character) -> CharacterResponse:
    eff = character.effective_stats()
    mana = character.effective_mana_pool()
    items = [
        ItemSchema(
            name=item.name,
            slot=item.slot.value,
            rarity=item.rarity.value,
            hp_bonus=item.hp_bonus,
            atk_bonus=item.atk_bonus,
            defense_bonus=item.defense_bonus,
            speed_bonus=item.speed_bonus,
            mana_bonus=item.mana_bonus,
            upgrade_level=item.upgrade_level,
            description=item.description,
            sprite=item.sprite,
        )
        for item in character.inventory.all_items()
    ]
    skill_statuses = [
        SkillStatusSchema(
            name=s.name,
            description=s.description,
            cooldown=s.cooldown,
            mana_cost=s.mana_cost,
            skill_type=s.skill_type.name,
            sprite=s.sprite,
            cooldown_remaining=character.cooldowns.as_dict().get(s.name, 0),
            is_ready=character.skill_is_ready(s.name),
        )
        for s in character.character_class.skills
    ]
    return CharacterResponse(
        name=character.name,
        class_name=character.character_class.name,
        race_name=character.race.name,
        level=character.exp_system.level,
        exp=character.exp_system.current_exp,
        current_floor=character.current_floor,
        gold=character.gold.amount,
        hp=eff.hp,
        max_hp=eff.max_hp,
        atk=eff.atk,
        defense=eff.defense,
        speed=eff.speed,
        mana=mana.current,
        max_mana=mana.maximum,
        skills=skill_statuses,
        inventory=items,
    )


@router.post("/combat/start", response_model=CombatStartResponse)
def start_combat(req: CombatStartRequest) -> CombatStartResponse:
    character = load_character(req.character_name)
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Personagem '{req.character_name}' nao encontrado.",
        )

    target_floor = req.floor if req.floor is not None else character.current_floor
    floor_monsters = MONSTERS_BY_FLOOR.get(target_floor, list(MONSTERS_BY_FLOOR[1]))
    monster = random.choice(floor_monsters)

    # Regra de Gameplay: Cada nova batalha começa com as habilidades resetadas (prontas)
    fresh_cooldowns = SkillCooldowns.from_skills(character.character_class.skills)
    fresh_char = character._with(cooldowns=fresh_cooldowns)

    combat_id = f"combat_{uuid.uuid4().hex[:8]}"
    ACTIVE_COMBATS[combat_id] = {
        "combat_id": combat_id,
        "character": fresh_char,
        "monster": monster,
        "floor": target_floor,
        "arcane_shield": False,
    }

    monster_schema = MonsterSchema(
        name=monster.name,
        hp=monster.stats.hp,
        max_hp=monster.stats.max_hp,
        atk=monster.stats.atk,
        defense=monster.stats.defense,
        speed=monster.stats.speed,
        exp_reward=monster.exp_reward,
        gold_reward=monster.gold_reward,
        sprite=monster.sprite,
    )

    return CombatStartResponse(
        combat_id=combat_id,
        character=_build_character_response(fresh_char),
        monster=monster_schema,
    )


@router.post("/combat/action", response_model=CombatActionResponse)
def combat_action(req: CombatActionRequest) -> CombatActionResponse:
    session = ACTIVE_COMBATS.get(req.combat_id)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sessao de combate nao encontrada ou expirada.",
        )

    character: Character = session["character"]
    monster: Monster = session["monster"]
    arcane_shield: bool = session["arcane_shield"]

    combat_log: List[str] = []
    player_damage_dealt = 0
    player_skill_used = "Ataque Basico"
    defensive_stance = False

    # Turno do Jogador
    if req.action_type == "skill" and req.skill_name:
        matched_skill = next(
            (s for s in character.character_class.skills if s.name == req.skill_name),
            None,
        )
        if not matched_skill:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Habilidade '{req.skill_name}' nao encontrada para esta classe.",
            )

        if not character.skill_is_ready(matched_skill.name):
            cd_rem = character.cooldowns.as_dict().get(matched_skill.name, 0)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Habilidade '{req.skill_name}' em recarga. Faltam {cd_rem} turno(s).",
            )

        if not character.has_mana(matched_skill.mana_cost):
            current_mana = character.effective_mana_pool().current
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Mana insuficiente para '{req.skill_name}'. Requer {matched_skill.mana_cost}, voce possui {current_mana}.",
            )

        player_skill_used = matched_skill.name
        new_char, new_monster_stats, action_msg = _use_skill(
            character, monster.stats, monster.stats.defense, matched_skill
        )
        player_damage_dealt = monster.stats.hp - new_monster_stats.hp
        monster = Monster(
            name=monster.name,
            stats=new_monster_stats,
            exp_reward=monster.exp_reward,
            min_floor=monster.min_floor,
            description=monster.description,
            sprite=monster.sprite,
            gold_reward=monster.gold_reward,
        )
        character = new_char
        defensive_stance = "Postura Defensiva" in action_msg
        arcane_shield = arcane_shield or ("Escudo Arcano" in action_msg or "Passo das Sombras" in action_msg)
        combat_log.append(action_msg)
    else:
        player_damage_dealt = _resolve_attack(character.effective_stats().atk, monster.stats.defense)
        new_monster_stats = _damage_enemy(monster.stats, player_damage_dealt)
        monster = Monster(
            name=monster.name,
            stats=new_monster_stats,
            exp_reward=monster.exp_reward,
            min_floor=monster.min_floor,
            description=monster.description,
            sprite=monster.sprite,
            gold_reward=monster.gold_reward,
        )
        character = character.tick_cooldowns()
        if not character.mana_pool.is_empty():
            character = character.restore_mana(2)
        combat_log.append(f"{character.name} atacou {monster.name} por {player_damage_dealt} de dano!")

    # Verificar se Monstro Morreu
    victory = not monster.is_alive()
    enemy_damage_dealt = 0

    if victory:
        combat_log.append(f"Voce derrotou {monster.name}! Ganhou {monster.exp_reward} XP e {monster.gold_reward} Ouro.")
        updated_char, _ = character.gain_exp(monster.exp_reward)
        updated_char = updated_char.earn_gold(monster.gold_reward)
        # Progressão de andar na vitória
        updated_char = updated_char.advance_floor()
        save_character(updated_char)
        del ACTIVE_COMBATS[req.combat_id]
        return CombatActionResponse(
            player_damage_dealt=player_damage_dealt,
            player_skill_used=player_skill_used,
            enemy_damage_dealt=0,
            player_hp_after=updated_char.effective_stats().hp,
            enemy_hp_after=0,
            player_mana_after=updated_char.effective_mana_pool().current,
            victory=True,
            character_defeated=False,
            combat_log=combat_log,
        )

    # Turno do Monstro
    eff_def = character.effective_stats().defense * (2 if defensive_stance else 1)
    raw_enemy_damage = _resolve_attack(monster.stats.atk, eff_def)

    if arcane_shield:
        combat_log.append(f"{monster.name} atacou, mas o dano foi absorvido pelo Escudo!")
        arcane_shield = False
        enemy_damage_dealt = 0
    else:
        enemy_damage_dealt = raw_enemy_damage
        character = character.take_damage(enemy_damage_dealt)
        combat_log.append(f"{monster.name} atacou {character.name} por {enemy_damage_dealt} de dano!")

    char_defeated = not character.is_alive()
    if char_defeated:
        combat_log.append(f"{character.name} foi derrotado em combate...")
        del ACTIVE_COMBATS[req.combat_id]
    else:
        session["character"] = character
        session["monster"] = monster
        session["arcane_shield"] = arcane_shield

    return CombatActionResponse(
        player_damage_dealt=player_damage_dealt,
        player_skill_used=player_skill_used,
        enemy_damage_dealt=enemy_damage_dealt,
        player_hp_after=character.effective_stats().hp,
        enemy_hp_after=monster.stats.hp,
        player_mana_after=character.effective_mana_pool().current,
        victory=False,
        character_defeated=char_defeated,
        combat_log=combat_log,
    )

