from fastapi import APIRouter, HTTPException, status
from typing import List

from data.classes import ALL_CLASSES
from data.races import ALL_RACES
from core.character import Character
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
    CharacterCreateRequest,
    CharacterResponse,
    ItemSchema,
)

router = APIRouter(prefix="/api")


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
        inventory=items,
    )
