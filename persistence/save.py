import json
import os
from core.character import Character
from core.stats import Stats
from core.exp import ExperienceSystem
from core.inventory import Inventory
from core.mana_pool import ManaPool
from core.skill_cooldowns import SkillCooldowns
from core.items import Item, ItemSlot, Rarity
from data.classes import ALL_CLASSES
from data.races import ALL_RACES

SAVE_DIR = "saves"


def _ensure_save_dir() -> None:
    os.makedirs(SAVE_DIR, exist_ok=True)


def _save_path(name: str) -> str:
    return os.path.join(SAVE_DIR, f"{name.replace(' ', '_').lower()}.json")


def save_character(character: Character) -> None:
    _ensure_save_dir()
    stats = character.base_stats
    data = {
        "name": character.name,
        "class_name": character.character_class.name,
        "race_name": character.race.name,
        "stats": {
            "hp": stats.hp, "max_hp": stats.max_hp,
            "atk": stats.atk, "defense": stats.defense, "speed": stats.speed,
        },
        "mana": character.mana_pool.current,
        "max_mana": character.mana_pool.maximum,
        "exp": character.exp_system.current_exp,
        "level": character.exp_system.level,
        "current_floor": character.current_floor,
        "skill_cooldowns": character.cooldowns.as_dict(),
        "inventory": [
            {
                "name": item.name, "slot": item.slot.value, "rarity": item.rarity.value,
                "hp_bonus": item.hp_bonus, "atk_bonus": item.atk_bonus,
                "defense_bonus": item.defense_bonus, "speed_bonus": item.speed_bonus,
                "description": item.description, "sprite": item.sprite,
            }
            for item in character.inventory.all_items()
        ],
    }
    with open(_save_path(character.name), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_character(name: str) -> Character | None:
    path = _save_path(name)
    if not os.path.exists(path):
        return None

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    char_class = ALL_CLASSES.get(data["class_name"])
    race = ALL_RACES.get(data["race_name"])
    if not char_class or not race:
        return None

    raw = data["stats"]
    stats = Stats(hp=raw["hp"], max_hp=raw["max_hp"], atk=raw["atk"], defense=raw["defense"], speed=raw["speed"])
    exp_system = ExperienceSystem(current_exp=data["exp"], level=data["level"])
    mana_pool = ManaPool(current=data.get("mana", 0), maximum=data.get("max_mana", 0))
    cooldowns = SkillCooldowns.from_dict(data.get("skill_cooldowns", {}))

    inventory = Inventory.empty()
    for item_data in data.get("inventory", []):
        slot = next((sl for sl in ItemSlot if sl.value == item_data["slot"]), None)
        rarity = next((r for r in Rarity if r.value == item_data.get("rarity", "Comum")), Rarity.COMMON)
        if slot is None:
            continue
        inventory = inventory.equip(Item(
            name=item_data["name"], slot=slot, rarity=rarity,
            hp_bonus=item_data["hp_bonus"], atk_bonus=item_data["atk_bonus"],
            defense_bonus=item_data["defense_bonus"], speed_bonus=item_data["speed_bonus"],
            description=item_data["description"], sprite=item_data.get("sprite", ""),
        ))

    return Character(
        name=data["name"],
        character_class=char_class,
        race=race,
        base_stats=stats,
        mana_pool=mana_pool,
        exp_system=exp_system,
        inventory=inventory,
        current_floor=data["current_floor"],
        cooldowns=cooldowns,
    )


def list_saved_characters() -> list[str]:
    _ensure_save_dir()
    return [
        f.replace(".json", "").replace("_", " ").title()
        for f in os.listdir(SAVE_DIR) if f.endswith(".json")
    ]


def delete_character(name: str) -> bool:
    path = _save_path(name)
    if not os.path.exists(path):
        return False
    os.remove(path)
    return True
