import os
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.character import Character
    from core.stats import Stats

SEP = "━" * 50
SEP_THIN = "─" * 50

FLOOR_FLAVOR: dict[int, str] = {
    1:  "A entrada da torre. Paredes umidas. O ar cheira a musgo e medo.",
    2:  "Tochas cintilam nas paredes. Ecos de passos distantes.",
    3:  "O chao range. Sombras se movem antes mesmo de voce olhar.",
    4:  "Corredor estreito. Algo respirou perto da sua orelha.",
    5:  "Metade da torre. O calor cresce. Um cheiro de pedra queimada.",
    6:  "As paredes pulsam como se estivessem vivas. Nao confie em nada.",
    7:  "Silencio. Perfeito. Assustador. Como se a torre estivesse te observando.",
    8:  "Runas brilham no teto. O poder aqui e quase palpavel.",
    9:  "Voce esta quase la. O ar e gelado. Seus passos ecoam por toda a torre.",
    10: "O topo. Cada passo e pesado. Uma presenca opressora domina tudo.",
}


def _clear() -> None:
    os.system("cls" if os.name == "nt" else "clear")


class ConsoleUI:

    def clear(self) -> None:
        _clear()

    def show_title(self) -> None:
        print("\n" + SEP)
        print("        ★  TOWER OF LUCAS  ★")
        print(SEP)

    def show_message(self, msg: str) -> None:
        print(f"\n  {msg}")

    def get_input(self, prompt: str) -> str:
        return input(f"  {prompt}").strip()

    def show_separator(self) -> None:
        print("\n" + SEP_THIN)

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

    # ── COMBAT ──────────────────────────────────────────────────────────────

    def show_combat_start(self, enemy_name: str, floor: int | None = None) -> None:
        print("\n" + SEP)
        if floor is not None:
            print(f"  ▶  ANDAR {floor}")
        print(f"  ⚠  Encontrou: {enemy_name.upper()}!")
        print(SEP)

    def show_battle_status(self, character: "Character", enemy_name: str, enemy_stats: "Stats") -> None:
        eff = character.effective_stats()
        eff_mana = character.effective_mana_pool()
        mana_info = f"  Mana {eff_mana.current}/{eff_mana.maximum}" if not eff_mana.is_empty() else ""
        level_info = f"Nv.{character.exp_system.level}"
        print(f"\n  {SEP_THIN}")
        print(f"  {character.name} [{level_info}]  HP {eff.hp}/{eff.max_hp}  ATK {eff.atk}  DEF {eff.defense}{mana_info}")
        print(f"  {enemy_name}           HP {enemy_stats.hp}/{enemy_stats.max_hp}  ATK {enemy_stats.atk}  DEF {enemy_stats.defense}")
        active_cds = character.cooldowns.active()
        if active_cds:
            cd_text = " | ".join(f"{k}: {v}t" for k, v in active_cds.items())
            print(f"  Cooldowns: {cd_text}")
        print(f"  {SEP_THIN}")

    def show_combat_options(self, available_skills: list) -> None:
        print("\n  [1] Atacar", end="")
        if available_skills:
            names = ", ".join(s.name for s in available_skills)
            print(f"  |  [2] Skill ({names})", end="")
        print()

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

    def show_combat_victory(
        self,
        enemy_name: str,
        exp_gained: int,
        gold_gained: int,
        old_level: int,
        character: "Character",
    ) -> None:
        new_level = character.exp_system.level
        exp_now = character.exp_system.current_exp
        exp_needed = character.exp_system.exp_needed_for_next_level()
        print("\n" + SEP)
        print(f"  ⚔  VITORIA!  ⚔")
        print(f"\n  {enemy_name} foi derrotado!")
        print(f"\n  ✦  +{exp_gained} EXP    ({exp_now}/{exp_needed} para o proximo nivel)")
        print(f"  ✦  +{gold_gained} Ouro   (total: {character.gold})")
        if new_level > old_level:
            print(f"\n  ★  LEVEL UP!  Nivel {old_level} → {new_level}!")
            stats = character.effective_stats()
            print(f"     HP +5  |  ATK +1  |  DEF +1  |  Mana +5")
        print(SEP)

    # ── FLOOR ───────────────────────────────────────────────────────────────

    def show_floor_intro(self, floor: int) -> None:
        flavor = FLOOR_FLAVOR.get(floor, "Voce avanca pela torre.")
        print("\n" + SEP)
        print(f"  ▶  ANDAR {floor}")
        print(f"\n  {flavor}")
        print(SEP)

    def show_floor_advance(self, to_floor: int) -> None:
        print("\n" + SEP_THIN)
        print(f"  Voce avanca... O andar {to_floor} se aproxima.")
        print(SEP_THIN)

    def show_boss_intro(self, name: str, title: str, intro_text: str) -> None:
        print("\n" + SEP)
        print(f"  !! {name.upper()}, {title.upper()} !!")
        print()
        for line in intro_text.splitlines():
            print(f"  {line}")
        print(SEP)
        input("\n  [Enter para iniciar a batalha...]")

    def show_item_found(self, item) -> str:
        print(f"\n  Item encontrado: {item}")
        return self.get_input("Equipar? [s/n] ")

    def show_death_screen(self, character_name: str) -> None:
        print("\n" + SEP)
        print("  ✝  VOCE FOI DERROTADO")
        print(f"\n  {character_name} sucumbiu às profundezas da torre.")
        print("\n  Sem piedade. Sem segunda chance.")
        print("  Este personagem foi apagado para sempre.")
        print(SEP)
        input("\n  [Enter para voltar ao menu...]")

    def show_victory(self) -> None:
        print("\n" + SEP)
        print("  ★  VOCE DERROTOU LUCAS, O ARQUITETO!  ★")
        print("\n  A torre treme. As paredes racham. A luz retorna.")
        print("  Seu nome sera gravado eternamente nesta torre.")
        print(SEP)
        input("\n  [Enter para continuar...]")

    # ── CAMP ────────────────────────────────────────────────────────────────

    def show_camp_intro(self, floor: int) -> None:
        print("\n" + SEP)
        print(f"  ⛺  ACAMPAMENTO — Apos o Andar {floor}")
        print("\n  Um raro momento de paz na torre.")
        print("  Um ferreiro misterioso surge das sombras.")
        print("  'Tenho tempo... e voce tem ouro?'")
        print(SEP)

    def show_camp_menu(self, character: "Character", can_rest: bool = True) -> str:
        items = character.inventory.all_items()
        print(f"\n  Ouro atual: {character.gold}")
        print("\n  [1] Melhorar um item  (custa ouro)")
        if can_rest:
            print("  [2] Descansar         (+30% HP, gratis)")
        else:
            print("  [2] Descansar         (ja descansou)")
        print("  [3] Continuar a subir")
        return self.get_input("> ")

    def show_camp_upgrade_menu(self, character: "Character") -> int:
        items = character.inventory.all_items()
        if not items:
            print("\n  Voce nao tem itens equipados para melhorar.")
            return -1
        print(f"\n  Ouro atual: {character.gold}")
        print("\n  Qual item deseja melhorar?\n")
        for i, item in enumerate(items, 1):
            if item.can_upgrade():
                cost = item.upgrade_cost()
                next_rarity = item.rarity.next_rarity()
                can = "✓" if character.gold.can_afford(cost) else "✗"
                print(f"    [{i}] {item}  |  {item.rarity.value} → {next_rarity.value}  |  Custo: {cost} ouro  [{can}]")
            else:
                print(f"    [{i}] {item}  |  [MAX]")
        print(f"    [0] Voltar")
        while True:
            raw = self.get_input("Escolha: ")
            if raw == "0":
                return -1
            if raw.isdigit() and 1 <= int(raw) <= len(items):
                return int(raw) - 1
            print("  Opcao invalida.")

    def show_item_upgraded(self, old_item, new_item) -> None:
        print("\n" + SEP_THIN)
        print(f"  O ferreiro martela com precisao...")
        print(f"  {old_item.name}  →  {new_item}")
        print(SEP_THIN)

    def show_camp_rest(self, healed: int) -> None:
        print(f"\n  Voce descansa ao lado da fogueira.")
        print(f"  +{healed} HP recuperado.")
