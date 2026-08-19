from core.character import Character
from data.classes import ALL_CLASSES
from data.races import ALL_RACES
from floors.floor_manager import run_floor
from persistence.save import save_character, load_character, list_saved_characters, delete_character
from ui.console_ui import ConsoleUI


def _create_character(ui: ConsoleUI) -> None:
    ui.clear()
    ui.show_separator()
    print("\n  Criar novo personagem\n")

    name = ui.get_input("Nome do personagem: ")

    print("\n  Escolha a classe:")
    class_names = list(ALL_CLASSES.keys())
    for cls in ALL_CLASSES.values():
        print(f"    -> {cls}")
    class_index = ui.pick_from_list("classe", class_names)

    print("\n  Escolha a raca:")
    race_names = list(ALL_RACES.keys())
    for race in ALL_RACES.values():
        print(f"    -> {race}")
    race_index = ui.pick_from_list("raca", race_names)

    char_class = ALL_CLASSES[class_names[class_index]]
    race = ALL_RACES[race_names[race_index]]

    character = Character.create(name=name, character_class=char_class, race=race)
    save_character(character)
    ui.show_message(f"Personagem '{name}' criado!")
    ui.show_character_summary(character)


def _select_character(ui: ConsoleUI) -> Character | None:
    saved = list_saved_characters()
    if not saved:
        ui.show_message("Nenhum personagem encontrado. Crie um primeiro!")
        return None

    ui.show_character_list(saved)
    index = ui.pick_from_list("personagem", saved)
    character = load_character(saved[index])

    if not character:
        ui.show_message("Erro ao carregar personagem.")
        return None

    ui.show_character_summary(character)
    return character


def _delete_character(ui: ConsoleUI) -> None:
    saved = list_saved_characters()
    if not saved:
        ui.show_message("Nenhum personagem para excluir.")
        return

    ui.show_character_list(saved)
    index = ui.pick_from_list("personagem para excluir", saved)
    name = saved[index]
    confirm = ui.get_input(f"Confirmar exclusao de '{name}'? [s/n] ")
    if confirm.lower() == "s":
        delete_character(name)
        ui.show_message(f"Personagem '{name}' excluido.")


def _play(ui: ConsoleUI) -> None:
    character = _select_character(ui)
    if not character:
        return

    current = character
    while current and current.current_floor <= 10:
        result = run_floor(current, current.current_floor)
        if result is None:
            delete_character(current.name)
            return
        current = result
        save_character(current)

    if current and current.current_floor > 10:
        ui.show_message("Voce conquistou a Tower of Lucas. Lenda eterna!")


def main() -> None:
    ui = ConsoleUI()
    actions = {
        "1": lambda: _play(ui),
        "2": lambda: _create_character(ui),
        "3": lambda: _delete_character(ui),
    }

    while True:
        ui.clear()
        choice = ui.show_main_menu()

        if choice == "0":
            print("\n  Ate a proxima aventura.\n")
            break

        action = actions.get(choice)
        if action:
            action()
            input("\n  [Enter para voltar ao menu...]")


if __name__ == "__main__":
    main()
