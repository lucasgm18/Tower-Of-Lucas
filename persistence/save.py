import json
from core.character import Character
from core.stats import Stats
from core.exp import ExperienceSystem
from core.inventory import Inventory
from core.mana_pool import ManaPool
from core.skill_cooldowns import SkillCooldowns
from core.gold import Gold
from core.items import Item, ItemSlot, Rarity
from data.classes import ALL_CLASSES
from data.races import ALL_RACES
from persistence.database import get_connection, init_db, DEFAULT_DB_PATH


def save_character(character: Character, db_path: str = DEFAULT_DB_PATH) -> None:
    init_db(db_path)
    stats = character.base_stats
    conn = get_connection(db_path)
    with conn:
        conn.execute(
            """
            INSERT INTO characters (
                name, class_name, race_name, hp, max_hp, atk, defense, speed,
                mana, max_mana, gold, exp, level, current_floor, skill_cooldowns
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(name) DO UPDATE SET
                class_name = excluded.class_name,
                race_name = excluded.race_name,
                hp = excluded.hp,
                max_hp = excluded.max_hp,
                atk = excluded.atk,
                defense = excluded.defense,
                speed = excluded.speed,
                mana = excluded.mana,
                max_mana = excluded.max_mana,
                gold = excluded.gold,
                exp = excluded.exp,
                level = excluded.level,
                current_floor = excluded.current_floor,
                skill_cooldowns = excluded.skill_cooldowns
            """,
            (
                character.name,
                character.character_class.name,
                character.race.name,
                stats.hp,
                stats.max_hp,
                stats.atk,
                stats.defense,
                stats.speed,
                character.mana_pool.current,
                character.mana_pool.maximum,
                character.gold.amount,
                character.exp_system.current_exp,
                character.exp_system.level,
                character.current_floor,
                json.dumps(character.cooldowns.as_dict()),
            ),
        )

        conn.execute("DELETE FROM inventory_items WHERE character_name = ?", (character.name,))
        for item in character.inventory.all_items():
            conn.execute(
                """
                INSERT INTO inventory_items (
                    character_name, name, slot, rarity, hp_bonus, atk_bonus,
                    defense_bonus, speed_bonus, mana_bonus, upgrade_level, description, sprite
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    character.name,
                    item.name,
                    item.slot.value,
                    item.rarity.value,
                    item.hp_bonus,
                    item.atk_bonus,
                    item.defense_bonus,
                    item.speed_bonus,
                    item.mana_bonus,
                    item.upgrade_level,
                    item.description,
                    item.sprite,
                ),
            )
    conn.close()


def load_character(name: str, db_path: str = DEFAULT_DB_PATH) -> Character | None:
    init_db(db_path)
    conn = get_connection(db_path)
    cursor = conn.execute("SELECT * FROM characters WHERE name = ?", (name,))
    row = cursor.fetchone()
    if row is None:
        conn.close()
        return None

    char_class = ALL_CLASSES.get(row["class_name"])
    race = ALL_RACES.get(row["race_name"])
    if not char_class or not race:
        conn.close()
        return None

    stats = Stats(
        hp=row["hp"],
        max_hp=row["max_hp"],
        atk=row["atk"],
        defense=row["defense"],
        speed=row["speed"],
    )
    exp_system = ExperienceSystem(current_exp=row["exp"], level=row["level"])
    mana_pool = ManaPool(current=row["mana"], maximum=row["max_mana"])
    cooldowns = SkillCooldowns.from_dict(json.loads(row["skill_cooldowns"]))
    gold = Gold(amount=row["gold"])

    item_cursor = conn.execute(
        "SELECT * FROM inventory_items WHERE character_name = ?", (name,)
    )
    inventory = Inventory.empty()
    for item_row in item_cursor.fetchall():
        slot = next((sl for sl in ItemSlot if sl.value == item_row["slot"]), None)
        rarity = next(
            (r for r in Rarity if r.value == item_row["rarity"]), Rarity.COMMON
        )
        if slot is None:
            continue
        inventory = inventory.equip(
            Item(
                name=item_row["name"],
                slot=slot,
                rarity=rarity,
                hp_bonus=item_row["hp_bonus"],
                atk_bonus=item_row["atk_bonus"],
                defense_bonus=item_row["defense_bonus"],
                speed_bonus=item_row["speed_bonus"],
                mana_bonus=item_row["mana_bonus"],
                upgrade_level=item_row["upgrade_level"],
                description=item_row["description"],
                sprite=item_row["sprite"],
            )
        )

    conn.close()
    return Character(
        name=row["name"],
        character_class=char_class,
        race=race,
        base_stats=stats,
        mana_pool=mana_pool,
        exp_system=exp_system,
        inventory=inventory,
        current_floor=row["current_floor"],
        cooldowns=cooldowns,
        gold=gold,
    )


def list_saved_characters(db_path: str = DEFAULT_DB_PATH) -> list[str]:
    init_db(db_path)
    conn = get_connection(db_path)
    cursor = conn.execute("SELECT name FROM characters ORDER BY created_at DESC")
    names = [row["name"] for row in cursor.fetchall()]
    conn.close()
    return names


def delete_character(name: str, db_path: str = DEFAULT_DB_PATH) -> bool:
    init_db(db_path)
    conn = get_connection(db_path)
    with conn:
        cursor = conn.execute("DELETE FROM characters WHERE name = ?", (name,))
        deleted = cursor.rowcount > 0
    conn.close()
    return deleted
