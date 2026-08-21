from pydantic import BaseModel, Field
from typing import List, Optional


class SkillSchema(BaseModel):
    name: str
    description: str
    cooldown: int
    mana_cost: int
    skill_type: str
    sprite: str = ""


class SkillStatusSchema(SkillSchema):
    cooldown_remaining: int
    is_ready: bool


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
    skills: List[SkillStatusSchema] = []
    inventory: List[ItemSchema]


class MonsterSchema(BaseModel):
    name: str
    hp: int
    max_hp: int
    atk: int
    defense: int
    speed: int
    exp_reward: int
    gold_reward: int
    sprite: str = ""


class CombatStartRequest(BaseModel):
    character_name: str
    floor: Optional[int] = None



class CombatStartResponse(BaseModel):
    combat_id: str
    character: CharacterResponse
    monster: MonsterSchema


class CombatActionRequest(BaseModel):
    combat_id: str
    action_type: str  # "attack" ou "skill"
    skill_name: str = ""


class CombatActionResponse(BaseModel):
    player_damage_dealt: int
    player_skill_used: str
    enemy_damage_dealt: int
    player_hp_after: int
    enemy_hp_after: int
    player_mana_after: int
    victory: bool
    character_defeated: bool
    combat_log: List[str]

