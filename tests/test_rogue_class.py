import unittest
from core.character import Character
from core.stats import Stats
from core.combat import _use_skill
from data.classes import ALL_CLASSES, ROGUE
from data.races import ALL_RACES
from persistence.save import save_character, load_character, delete_character


class TestRogueClass(unittest.TestCase):

    def test_rogue_class_registered(self) -> None:
        self.assertIn("Ladino", ALL_CLASSES)
        self.assertEqual(ALL_CLASSES["Ladino"], ROGUE)

    def test_rogue_creation_with_human_race(self) -> None:
        rogue = Character.create("Shadow", ALL_CLASSES["Ladino"], ALL_RACES["Humano"])
        stats = rogue.effective_stats()

        # Base Rogue HP 45, Humano HP bonus 0 -> max_hp 45
        self.assertEqual(stats.hp, 45)
        # Base ATK 7 + 0 = 7
        self.assertEqual(stats.atk, 7)
        # Base DEF 3 + Humano DEF bonus 1 = 4
        self.assertEqual(stats.defense, 4)
        # Base VEL 9 + Humano VEL bonus 2 = 11
        self.assertEqual(stats.speed, 11)
        # Base Mana 15 + Humano Mana bonus 5 = 20
        self.assertEqual(rogue.mana_pool.maximum, 20)
        self.assertEqual(rogue.mana_pool.current, 20)

    def test_sneak_attack_skill_execution(self) -> None:
        rogue = Character.create("Shadow", ALL_CLASSES["Ladino"], ALL_RACES["Humano"])
        enemy_stats = Stats(hp=50, max_hp=50, atk=5, defense=4, speed=5)
        sneak_attack = ROGUE.skills[0]  # Ataque Furtivo

        updated_char, updated_enemy, msg = _use_skill(rogue, enemy_stats, 4, sneak_attack)

        # Sneak attack cost 5 mana (20 -> 15)
        self.assertEqual(updated_char.mana_pool.current, 15)
        # Sneak attack sets cooldown 3
        self.assertFalse(updated_char.skill_is_ready("Ataque Furtivo"))
        # Enemy took damage: ATK(7+0)+VEL(9+2) = 18. Enemy DEF 4 // 2 = 2. Damage = 18 - 2 = 16. HP 50 -> 34.
        self.assertEqual(updated_enemy.hp, 34)
        self.assertIn("Ataque Furtivo!", msg)

    def test_shadow_step_skill_execution(self) -> None:
        rogue = Character.create("Shadow", ALL_CLASSES["Ladino"], ALL_RACES["Humano"])
        # Spend some mana first (20 -> 10)
        rogue = rogue.spend_mana(10)
        enemy_stats = Stats(hp=50, max_hp=50, atk=5, defense=4, speed=5)
        shadow_step = ROGUE.skills[1]  # Passo das Sombras

        updated_char, updated_enemy, msg = _use_skill(rogue, enemy_stats, 4, shadow_step)

        # Spent 5 mana and restored 5 mana (10 - 5 + 5 = 10)
        self.assertEqual(updated_char.mana_pool.current, 10)
        # Cooldown 4 set
        self.assertFalse(updated_char.skill_is_ready("Passo das Sombras"))
        self.assertIn("Passo das Sombras ativado!", msg)

    def test_save_and_load_rogue(self) -> None:
        char_name = "TestRogueSave"
        try:
            rogue = Character.create(char_name, ALL_CLASSES["Ladino"], ALL_RACES["Humano"])
            save_character(rogue)

            loaded = load_character(char_name)
            self.assertIsNotNone(loaded)
            if loaded:
                self.assertEqual(loaded.name, char_name)
                self.assertEqual(loaded.character_class.name, "Ladino")
                self.assertEqual(loaded.effective_stats().hp, 45)
        finally:
            delete_character(char_name)


if __name__ == "__main__":
    unittest.main()
