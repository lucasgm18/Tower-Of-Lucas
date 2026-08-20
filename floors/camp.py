from core.character import Character
from ui.console_ui import ConsoleUI

CAMP_FLOORS = {3, 6, 9}


def _upgrade_item(character: Character, ui: ConsoleUI) -> Character:
    index = ui.show_camp_upgrade_menu(character)
    if index == -1:
        return character

    items = character.inventory.all_items()
    item = items[index]

    if not item.can_upgrade():
        ui.show_message("Este item ja esta na qualidade maxima (Epico)!")
        return character

    cost = item.upgrade_cost()

    if not character.gold.can_afford(cost):
        ui.show_message(f"Ouro insuficiente! Precisa de {cost} ouro.")
        return character

    upgraded = item.upgraded()
    new_char = character.spend_gold(cost).equip(upgraded)
    ui.show_item_upgraded(item, upgraded)
    return new_char


def _rest(character: Character, ui: ConsoleUI) -> Character:
    eff = character.effective_stats()
    heal_amount = max(1, eff.max_hp * 30 // 100)
    healed = character.heal(heal_amount)
    ui.show_camp_rest(heal_amount)
    return healed


def run_camp(character: Character, floor: int) -> Character:
    ui = ConsoleUI()
    ui.show_camp_intro(floor)

    current = character
    already_rested = False

    while True:
        choice = ui.show_camp_menu(current, can_rest=not already_rested)
        if choice == "1":
            current = _upgrade_item(current, ui)
        elif choice == "2" and not already_rested:
            current = _rest(current, ui)
            already_rested = True
        elif choice == "3":
            break
        else:
            ui.show_message("Opcao invalida.")

    return current
