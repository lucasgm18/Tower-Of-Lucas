import random
import uuid
from fastapi import APIRouter, HTTPException, status
from typing import List, Dict

from data.classes import ALL_CLASSES, Skill
from data.races import ALL_RACES
from data.monsters import MONSTERS_BY_FLOOR, Monster
from data.bosses import BOSSES_BY_FLOOR, Boss
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
    res = []
    for c in ALL_CLASSES.values():
        skills = [
            SkillSchema(
                name=s.name,
                description=s.description,
                cooldown=s.cooldown,
                mana_cost=s.mana_cost,
                skill_type=s.skill_type.name,
                sprite=s.sprite,
            )
            for s in c.skills
        ]
        res.append(
            CharacterClassSchema(
                name=c.name,
                description=c.description,
                base_hp=c.base_hp,
                base_atk=c.base_atk,
                base_defense=c.base_defense,
                base_speed=c.base_speed,
                base_mana=c.base_mana,
                skills=skills,
                sprite=c.sprite,
            )
        )
    return res


@router.get("/races", response_model=List[RaceSchema])
def get_races() -> List[RaceSchema]:
    return [
        RaceSchema(
            name=r.name,
            description=r.description,
            hp_bonus=r.hp_bonus,
            atk_bonus=r.atk_bonus,
            defense_bonus=r.defense_bonus,
            speed_bonus=r.speed_bonus,
            mana_bonus=r.mana_bonus,
        )
        for r in ALL_RACES.values()
    ]


@router.get("/characters", response_model=List[str])
def get_characters() -> List[str]:
    return list_saved_characters()


@router.post("/characters", response_model=CharacterResponse, status_code=status.HTTP_201_CREATED)
def create_new_character(req: CharacterCreateRequest) -> CharacterResponse:
    existing = load_character(req.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Personagem com o nome '{req.name}' ja existe.",
        )

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

    character = Character.create(req.name, char_class, race)
    save_character(character)
    return _build_character_response(character)


@router.get("/characters/{name}", response_model=CharacterResponse)
def get_character_details(name: str) -> CharacterResponse:
    character = load_character(name)
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Personagem '{name}' nao encontrado.",
        )
    return _build_character_response(character)


@router.delete("/characters/{name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_existing_character(name: str) -> None:
    deleted = delete_character(name)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Personagem '{name}' nao encontrado.",
        )


@router.post("/characters/{name}/advance", response_model=CharacterResponse)
@router.post("/characters/{name}/advance_floor", response_model=CharacterResponse)
def advance_character_floor(name: str) -> CharacterResponse:
    character = load_character(name)
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Personagem '{name}' nao encontrado.",
        )
    if character.tower_completed or character.current_floor >= 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A Torre de Lucas ja foi conquistada por este heroi!",
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
        floor_progress=character.floor_progress,
        tower_completed=character.tower_completed,
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


def _get_encounter_monster(target_floor: int, is_boss: bool) -> Monster:
    if is_boss:
        boss = BOSSES_BY_FLOOR[target_floor]
        return Monster(
            name=boss.name,
            stats=boss.stats,
            exp_reward=boss.exp_reward,
            min_floor=target_floor,
            description=boss.title,
            sprite=boss.sprite,
            gold_reward=boss.gold_reward,
        )

    floor_monsters = MONSTERS_BY_FLOOR.get(target_floor)
    if not floor_monsters:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Nenhum monstro cadastrado para o andar {target_floor}.",
        )
    return random.choice(floor_monsters)


def _handle_floor_progression(character: Character, combat_log: List[str]) -> tuple[Character, bool, bool]:
    total_encounters = 4 if character.current_floor in BOSSES_BY_FLOOR else 3
    floor_completed = character.floor_progress >= total_encounters
    if not floor_completed:
        return character, False, False

    if character.current_floor == 10:
        combat_log.append("PARABENS! Voce derrotou Lucas, o Arquiteto, e conquistou a Torre de Lucas!")
        return character.complete_tower(), True, True

    advanced = character.advance_floor()
    combat_log.append(f"Andar {advanced.current_floor - 1} concluido! Voce avancou para o Andar {advanced.current_floor}.")
    return advanced, True, False


def _resolve_monster_turn(
    monster: Monster,
    character: Character,
    defensive_stance: bool,
    arcane_shield: bool,
    combat_log: List[str],
) -> tuple[Character, int, bool]:
    if arcane_shield:
        combat_log.append(f"{monster.name} atacou, mas o dano foi absorvido pelo Escudo!")
        return character, 0, False

    eff_def = character.effective_stats().defense * (2 if defensive_stance else 1)
    raw_damage = _resolve_attack(monster.stats.atk, eff_def)
    damaged = character.take_damage(raw_damage)
    combat_log.append(f"{monster.name} atacou {damaged.name} por {raw_damage} de dano!")
    return damaged, raw_damage, False


def _execute_skill_turn(
    character: Character,
    monster: Monster,
    skill_name: str,
    arcane_shield: bool,
    combat_log: List[str],
) -> tuple[Character, Monster, int, str, bool, bool]:
    matched_skill = next(
        (s for s in character.character_class.skills if s.name == skill_name),
        None,
    )
    if not matched_skill:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Habilidade '{skill_name}' nao encontrada para esta classe.",
        )

    if not character.skill_is_ready(matched_skill.name):
        cd_rem = character.cooldowns.as_dict().get(matched_skill.name, 0)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Habilidade '{skill_name}' em recarga. Faltam {cd_rem} turno(s).",
        )

    if not character.has_mana(matched_skill.mana_cost):
        current_mana = character.effective_mana_pool().current
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Mana insuficiente para '{skill_name}'. Requer {matched_skill.mana_cost}, voce possui {current_mana}.",
        )

    new_char, new_monster_stats, action_msg = _use_skill(
        character, monster.stats, monster.stats.defense, matched_skill
    )
    damage_dealt = monster.stats.hp - new_monster_stats.hp
    updated_monster = Monster(
        name=monster.name,
        stats=new_monster_stats,
        exp_reward=monster.exp_reward,
        min_floor=monster.min_floor,
        description=monster.description,
        sprite=monster.sprite,
        gold_reward=monster.gold_reward,
    )
    defensive_stance = "Postura Defensiva" in action_msg
    new_shield = arcane_shield or ("Escudo Arcano" in action_msg or "Passo das Sombras" in action_msg)
    combat_log.append(action_msg)
    return new_char, updated_monster, damage_dealt, matched_skill.name, defensive_stance, new_shield


def _execute_attack_turn(
    character: Character,
    monster: Monster,
    arcane_shield: bool,
    combat_log: List[str],
) -> tuple[Character, Monster, int, str, bool, bool]:
    player_damage = _resolve_attack(character.effective_stats().atk, monster.stats.defense)
    new_stats = _damage_enemy(monster.stats, player_damage)
    updated_monster = Monster(
        name=monster.name,
        stats=new_stats,
        exp_reward=monster.exp_reward,
        min_floor=monster.min_floor,
        description=monster.description,
        sprite=monster.sprite,
        gold_reward=monster.gold_reward,
    )
    ticked_char = character.tick_cooldowns()
    if not ticked_char.mana_pool.is_empty():
        ticked_char = ticked_char.restore_mana(2)
    combat_log.append(f"{ticked_char.name} atacou {monster.name} por {player_damage} de dano!")
    return ticked_char, updated_monster, player_damage, "Ataque Basico", False, arcane_shield


@router.post("/combat/start", response_model=CombatStartResponse)
def start_combat(req: CombatStartRequest) -> CombatStartResponse:
    character = load_character(req.character_name)
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Personagem '{req.character_name}' nao encontrado.",
        )

    if character.tower_completed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A Torre de Lucas ja foi conquistada por este heroi!",
        )

    if character.current_floor > 10:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Andar invalido. A torre possui 10 andares.",
        )

    target_floor = character.current_floor
    if req.floor is not None and req.floor != target_floor:
        if req.floor > 10 or req.floor < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Andar invalido. A torre possui 10 andares.",
            )
        target_floor = req.floor

    total_encounters = 4 if target_floor in BOSSES_BY_FLOOR else 3
    encounter_index = character.floor_progress + 1
    is_boss = (encounter_index == total_encounters and target_floor in BOSSES_BY_FLOOR)
    monster = _get_encounter_monster(target_floor, is_boss)

    # Regra de Gameplay: Cada nova batalha começa com as habilidades resetadas (prontas)
    fresh_cooldowns = SkillCooldowns.from_skills(character.character_class.skills)
    fresh_char = character._with(cooldowns=fresh_cooldowns)

    combat_id = f"combat_{uuid.uuid4().hex[:8]}"
    ACTIVE_COMBATS[combat_id] = {
        "combat_id": combat_id,
        "character": fresh_char,
        "monster": monster,
        "floor": target_floor,
        "encounter_index": encounter_index,
        "total_encounters": total_encounters,
        "is_boss": is_boss,
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
        encounter_index=encounter_index,
        total_encounters=total_encounters,
        is_boss=is_boss,
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

    # Turno do Jogador
    if req.action_type == "skill" and req.skill_name:
        character, monster, player_damage_dealt, player_skill_used, defensive_stance, arcane_shield = _execute_skill_turn(
            character, monster, req.skill_name, arcane_shield, combat_log
        )
    if not (req.action_type == "skill" and req.skill_name):
        character, monster, player_damage_dealt, player_skill_used, defensive_stance, arcane_shield = _execute_attack_turn(
            character, monster, arcane_shield, combat_log
        )

    # Verificar se Monstro Morreu
    if not monster.is_alive():
        combat_log.append(f"Voce derrotou {monster.name}! Ganhou {monster.exp_reward} XP e {monster.gold_reward} Ouro.")
        updated_char, _ = character.gain_exp(monster.exp_reward)
        updated_char = updated_char.earn_gold(monster.gold_reward)
        updated_char = updated_char.increment_floor_progress()

        updated_char, floor_completed, tower_completed = _handle_floor_progression(updated_char, combat_log)

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
            floor_completed=floor_completed,
            tower_completed=tower_completed,
            character_defeated=False,
            combat_log=combat_log,
            character=_build_character_response(updated_char),
        )

    # Turno do Monstro
    character, enemy_damage_dealt, arcane_shield = _resolve_monster_turn(
        monster, character, defensive_stance, arcane_shield, combat_log
    )

    char_defeated = not character.is_alive()
    if char_defeated:
        combat_log.append(f"{character.name} foi derrotado em combate...")
        del ACTIVE_COMBATS[req.combat_id]
        return CombatActionResponse(
            player_damage_dealt=player_damage_dealt,
            player_skill_used=player_skill_used,
            enemy_damage_dealt=enemy_damage_dealt,
            player_hp_after=character.effective_stats().hp,
            enemy_hp_after=monster.stats.hp,
            player_mana_after=character.effective_mana_pool().current,
            victory=False,
            floor_completed=False,
            tower_completed=False,
            character_defeated=True,
            combat_log=combat_log,
            character=_build_character_response(character),
        )

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
        floor_completed=False,
        tower_completed=False,
        character_defeated=False,
        combat_log=combat_log,
        character=_build_character_response(character),
    )
