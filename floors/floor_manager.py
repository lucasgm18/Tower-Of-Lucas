import random
from core.character import Character
from core.combat import run_combat, CombatResult
from data.monsters import MONSTERS_BY_FLOOR
from data.bosses import BOSSES_BY_FLOOR
from data.items_db import FLOOR_DROPS
from ui.console_ui import ConsoleUI

MONSTERS_PER_FLOOR = 3


def _run_monster_gauntlet(character: Character, floor: int, ui: ConsoleUI) -> Character | None:
    pool = MONSTERS_BY_FLOOR.get(floor, list(MONSTERS_BY_FLOOR[1]))
    encounters = random.choices(pool, k=MONSTERS_PER_FLOOR)

    current = character
    for monster in encounters:
        result: CombatResult = run_combat(
            character=current,
            enemy_name=monster.name,
            enemy_stats=monster.stats,
            exp_reward=monster.exp_reward,
        )
        if not result.victory:
            return None
        current = result.character
        current = _maybe_drop_item(current, floor, ui)

    return current


def _maybe_drop_item(character: Character, floor: int, ui: ConsoleUI) -> Character:
    drops = FLOOR_DROPS.get(floor, [])
    if not drops:
        return character
    if random.random() > 0.4:
        return character

    item = random.choice(drops)
    choice = ui.show_item_found(item)
    if choice.lower() == "s":
        return character.equip(item)
    return character


def _run_boss(character: Character, floor: int, ui: ConsoleUI) -> Character | None:
    boss = BOSSES_BY_FLOOR[floor]
    ui.show_boss_intro(boss.name, boss.title, boss.intro_text)

    result = run_combat(
        character=character,
        enemy_name=boss.name,
        enemy_stats=boss.stats,
        exp_reward=boss.exp_reward,
    )
    if not result.victory:
        return None

    if floor == 10:
        ui.show_victory()

    return result.character


def run_floor(character: Character, floor: int) -> Character | None:
    ui = ConsoleUI()
    ui.show_floor_intro(floor)

    after_gauntlet = _run_monster_gauntlet(character, floor, ui)
    if after_gauntlet is None:
        ui.show_death_screen()
        return None

    if floor in BOSSES_BY_FLOOR:
        after_boss = _run_boss(after_gauntlet, floor, ui)
        if after_boss is None:
            ui.show_death_screen()
            return None
        return after_boss.advance_floor()

    return after_gauntlet.advance_floor()
