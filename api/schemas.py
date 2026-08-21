from pydantic import BaseModel, Field
from typing import List


class SkillSchema(BaseModel):
    name: str
    description: str
    cooldown: int
    mana_cost: int
    skill_type: str
    sprite: str = ""


class CharacterClassSchema(BaseModel):
    name: str
    description: str
    base_hp: int
    base_atk: int
    base_defense: int
    base_speed: int
    base_mana: int
    skills: List[SkillSchema]
    sprite: str = ""


class RaceSchema(BaseModel):
    name: str
    description: str
    hp_bonus: int
    atk_bonus: int
    defense_bonus: int
    speed_bonus: int
    mana_bonus: int


class ItemSchema(BaseModel):
    name: str
    slot: str
    rarity: str
    hp_bonus: int
    atk_bonus: int
    defense_bonus: int
    speed_bonus: int
    mana_bonus: int
    upgrade_level: int
    description: str
    sprite: str = ""


class StatsSchema(BaseModel):
    hp: int
    max_hp: int
    atk: int
    defense: int
    speed: int


class CharacterCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    class_name: str
    race_name: str


class CharacterResponse(BaseModel):
    name: str
    class_name: str
    race_name: str
    level: int
    exp: int
    current_floor: int
    gold: int
    hp: int
    max_hp: int
    atk: int
    defense: int
    speed: int
    mana: int
    max_mana: int
    inventory: List[ItemSchema]
