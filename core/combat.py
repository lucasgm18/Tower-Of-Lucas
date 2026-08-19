import random
from dataclasses import dataclass
from typing import Callable
from core.character import Character
from core.stats import Stats
from data.classes import Skill, SkillType
from ui.console_ui import ConsoleUI


@dataclass
class CombatResult:
    victory: bool
    character: Character
    exp_gained: int
    gold_gained: int
    message: str


def _resolve_attack(attacker_atk: int, defender_defense: int) -> int:
    base = max(1, attacker_atk - defender_defense)
    variance = random.randint(-1, 2)
    return max(1, base + variance)


def _damage_enemy(enemy_stats: Stats, damage: int) -> Stats:
    return Stats(
        hp=max(0, enemy_stats.hp - damage),
        max_hp=enemy_stats.max_hp,
        atk=enemy_stats.atk,
        defense=enemy_stats.defense,
        speed=enemy_stats.speed,
    )


# ── Efeitos de skill ─────────────────────────────────────────────────────────

SkillEffect = Callable[[Character, Stats, int], tuple[Character, Stats, str]]


def _apply_heavy_strike(character: Character, enemy_stats: Stats, _: int) -> tuple[Character, Stats, str]:
    damage = character.effective_stats().atk * 2
    return character, _damage_enemy(enemy_stats, damage), f"Golpe Pesado! {damage} de dano devastador!"


def _apply_defensive_stance(character: Character, enemy_stats: Stats, _: int) -> tuple[Character, Stats, str]:
    return character, enemy_stats, "Postura Defensiva ativada! DEF dobrada neste turno."


def _apply_fireball(character: Character, enemy_stats: Stats, _: int) -> tuple[Character, Stats, str]:
    damage = character.effective_stats().atk + random.randint(3, 8)
    return character, _damage_enemy(enemy_stats, damage), f"Bola de Fogo! {damage} de dano magico (ignora DEF)!"


def _apply_arcane_shield(character: Character, enemy_stats: Stats, _: int) -> tuple[Character, Stats, str]:
    return character, enemy_stats, "Escudo Arcano ativado! Proximo ataque sera absorvido."


def _apply_generic(character: Character, enemy_stats: Stats, enemy_defense: int) -> tuple[Character, Stats, str]:
    damage = _resolve_attack(character.effective_stats().atk, enemy_defense)
    return character, _damage_enemy(enemy_stats, damage), f"{damage} de dano."


_SKILL_DISPATCH: dict[SkillType, SkillEffect] = {
    SkillType.HEAVY_STRIKE:     _apply_heavy_strike,
    SkillType.DEFENSIVE_STANCE: _apply_defensive_stance,
    SkillType.FIREBALL:         _apply_fireball,
    SkillType.ARCANE_SHIELD:    _apply_arcane_shield,
    SkillType.GENERIC:          _apply_generic,
}


def _use_skill(
    character: Character,
    enemy_stats: Stats,
    enemy_defense: int,
    skill: Skill,
) -> tuple[Character, Stats, str]:
    activated = character.use_skill(skill.name).spend_mana(skill.mana_cost).tick_cooldowns()
    effect = _SKILL_DISPATCH.get(skill.skill_type, _apply_generic)
    return effect(activated, enemy_stats, enemy_defense)


def _player_turn(
    character: Character,
    enemy_name: str,
    enemy_stats: Stats,
    enemy_defense: int,
    arcane_shield: bool,
) -> tuple[Character, Stats, str, bool]:
    ui = ConsoleUI()
    available_skills = [
        skill for skill in character.character_class.skills
        if character.skill_is_ready(skill.name) and character.has_mana(skill.mana_cost)
    ]

    ui.show_battle_status(character, enemy_name, enemy_stats)
    ui.show_combat_options(available_skills)
    choice = ui.get_input("> ")

    if choice == "2" and available_skills:
        skill_index = ui.pick_skill(available_skills)
        char, enemy, msg = _use_skill(character, enemy_stats, enemy_defense, available_skills[skill_index])
        new_shield = arcane_shield or "Escudo Arcano" in msg
        return char, enemy, msg, new_shield

    damage = _resolve_attack(character.effective_stats().atk, enemy_defense)
    updated = character.tick_cooldowns()
    if not updated.mana_pool.is_empty():
        updated = updated.restore_mana(2)
    return updated, _damage_enemy(enemy_stats, damage), f"Voce atacou por {damage} de dano!", arcane_shield


def run_combat(
    character: Character,
    enemy_name: str,
    enemy_stats: Stats,
    exp_reward: int,
    gold_reward: int = 0,
) -> CombatResult:
    ui = ConsoleUI()
    current_char = character
    current_enemy = enemy_stats
    arcane_shield = False
    defensive_stance = False

    ui.show_combat_start(enemy_name)

    while current_enemy.is_alive() and current_char.is_alive():
        current_char, current_enemy, action_msg, arcane_shield = _player_turn(
            current_char, enemy_name, current_enemy, enemy_stats.defense, arcane_shield
        )
        defensive_stance = "Postura Defensiva" in action_msg
        ui.show_message(action_msg)

        if not current_enemy.is_alive():
            break

        effective_defense = current_char.effective_stats().defense * (2 if defensive_stance else 1)
        enemy_damage = _resolve_attack(current_enemy.atk, effective_defense)

        if arcane_shield:
            ui.show_message(f"{enemy_name} atacou, mas o Escudo Arcano absorveu o golpe!")
            arcane_shield = False
        else:
            current_char = current_char.take_damage(enemy_damage)
            ui.show_message(f"{enemy_name} causou {enemy_damage} de dano!")

    if current_char.is_alive():
        old_level = current_char.exp_system.level
        updated, _ = current_char.gain_exp(exp_reward)
        updated = updated.earn_gold(gold_reward)
        ui.show_combat_victory(enemy_name, exp_reward, gold_reward, old_level, updated)
        return CombatResult(
            victory=True,
            character=updated,
            exp_gained=exp_reward,
            gold_gained=gold_reward,
            message=f"Voce derrotou {enemy_name}!",
        )

    return CombatResult(
        victory=False,
        character=current_char,
        exp_gained=0,
        gold_gained=0,
        message="Voce foi derrotado...",
    )
