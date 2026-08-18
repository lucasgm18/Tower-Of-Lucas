import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.character import Character
    from core.stats import Stats


def _clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")


RARITY_LABEL = {
    "Comum":   "[CINZA]",
    "Incomum": "[VERDE]",
    "Raro":    "[AZUL] ",
    "Epico":   "[ROXO] ",
}


class ConsoleUI:

    def clear(self) -> None:
        _clear()

    def show_title(self) -> None:
        print("\n" + "=" * 48)
        print("           TOWER OF LUCAS")
        print("=" * 48)

    def show_message(self, msg: str) -> None:
        print(f"\n  {msg}")

    def get_input(self, prompt: str) -> str:
        return input(f"  {prompt}").strip()

    def show_separator(self) -> None:
        print("\n" + "-" * 48)

    def show_main_menu(self) -> str:
        self.show_title()
        print("\n  [1] Jogar")
        print("  [2] Criar Personagem")
        print("  [3] Excluir Personagem")
        print("  [0] Sair")
        return self.get_input("> ")

    def show_character_list(self, names: list[str]) -> None:
        self.show_separator()
        print("\n  Personagens salvos:\n")
        for i, name in enumerate(names, 1):
            print(f"    [{i}] {name}")
        print()

    def pick_from_list(self, label: str, options: list[str]) -> int:
        for i, opt in enumerate(options, 1):
            print(f"  [{i}] {opt}")
        while True:
            raw = self.get_input(f"Escolha {label} (numero): ")
            if raw.isdigit() and 1 <= int(raw) <= len(options):
                return int(raw) - 1
            print("  Opcao invalida.")

    def show_character_summary(self, character: "Character") -> None:
        self.show_separator()
        print(character.summary())
        self.show_separator()

    def show_combat_start(self, enemy_name: str) -> None:
        self.show_separator()
        print(f"\n  >> Encontrou: {enemy_name}!")
        self.show_separator()

    def show_battle_status(self, character: "Character", enemy_name: str, enemy_stats: "Stats") -> None:
        self.show_separator()
        eff = character.effective_stats()
        mana_info = f" | {character.mana_pool}" if not character.mana_pool.is_empty() else ""
        print(f"  {character.name}  HP: {eff.hp}/{eff.max_hp}  ATK: {eff.atk}  DEF: {eff.defense}{mana_info}")
        print(f"  {enemy_name}      HP: {enemy_stats.hp}/{enemy_stats.max_hp}  ATK: {enemy_stats.atk}  DEF: {enemy_stats.defense}")
        active_cds = character.cooldowns.active()
        if active_cds:
            print("  Cooldowns: " + " | ".join(f"{k}: {v}t" for k, v in active_cds.items()))
        self.show_separator()

    def show_combat_options(self, available_skills: list) -> None:
        print("\n  [1] Atacar", end="")
        if available_skills:
            names = ", ".join(s.name for s in available_skills)
            print(f"  [2] Skill ({names})", end="")
        print("  [3] Ver status")

    def pick_skill(self, skills: list) -> int:
        print("\n  Skills disponiveis:")
        for i, skill in enumerate(skills, 1):
            mana_info = f" | Mana: {skill.mana_cost}" if skill.mana_cost > 0 else ""
            print(f"    [{i}] {skill.name} — {skill.description}{mana_info}")
        while True:
            raw = self.get_input("Escolha a skill: ")
            if raw.isdigit() and 1 <= int(raw) <= len(skills):
                return int(raw) - 1
            print("  Opcao invalida.")

    def show_floor_intro(self, floor: int) -> None:
        self.show_separator()
        print(f"\n  [Andar {floor}]")
        self.show_separator()

    def show_boss_intro(self, name: str, title: str, intro_text: str) -> None:
        self.show_separator()
        print(f"\n  !! {name.upper()}, {title} !!\n")
        for line in intro_text.splitlines():
            print(f"  {line}")
        self.show_separator()
        input("\n  [Enter para iniciar a batalha...]")

    def show_item_found(self, item) -> str:
        rarity_tag = RARITY_LABEL.get(item.rarity.value, "")
        print(f"\n  Item encontrado: {rarity_tag} {item.name} ({item.bonus_summary()}) {item.rarity.stars()}")
        return self.get_input("Equipar? [s/n] ")

    def show_death_screen(self) -> None:
        print("\n" + "=" * 48)
        print("            VOCE FOI DERROTADO")
        print("  Voltando ao inicio... Nivel 1. Sem itens.")
        print("  A torre aguarda sua proxima tentativa.")
        print("=" * 48)
        input("\n  [Enter para continuar...]")

    def show_victory(self) -> None:
        print("\n" + "=" * 48)
        print("       VOCE DERROTOU LUCAS!")
        print("  A torre foi conquistada. Lenda eterna.")
        print("=" * 48)
        input("\n  [Enter para continuar...]")
