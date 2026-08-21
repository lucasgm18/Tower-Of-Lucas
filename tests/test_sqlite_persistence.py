import unittest
import os
from core.character import Character
from data.classes import ALL_CLASSES
from data.races import ALL_RACES
from persistence.database import init_db, get_connection
from persistence.save import (
    save_character,
    load_character,
    list_saved_characters,
    delete_character,
)

TEST_DB_PATH = "saves/test_tower.db"


class TestSQLitePersistence(unittest.TestCase):

    def setUp(self) -> None:
        init_db(TEST_DB_PATH)

    def tearDown(self) -> None:
        if os.path.exists(TEST_DB_PATH):
            os.remove(TEST_DB_PATH)

    def test_save_and_load_character_sqlite(self) -> None:
        hero_name = "Arthas"
        warrior = Character.create(
            hero_name, ALL_CLASSES["Guerreiro"], ALL_RACES["Humano"]
        )
        save_character(warrior, db_path=TEST_DB_PATH)

        loaded = load_character(hero_name, db_path=TEST_DB_PATH)
        self.assertIsNotNone(loaded)
        if loaded:
            self.assertEqual(loaded.name, hero_name)
            self.assertEqual(loaded.character_class.name, "Guerreiro")
            self.assertEqual(loaded.race.name, "Humano")
            self.assertEqual(loaded.effective_stats().hp, 60)

    def test_list_saved_characters_sqlite(self) -> None:
        c1 = Character.create("RogueOne", ALL_CLASSES["Ladino"], ALL_RACES["Humano"])
        c2 = Character.create("MageOne", ALL_CLASSES["Mago"], ALL_RACES["Orc"])

        save_character(c1, db_path=TEST_DB_PATH)
        save_character(c2, db_path=TEST_DB_PATH)

        saved = list_saved_characters(db_path=TEST_DB_PATH)
        self.assertIn("RogueOne", saved)
        self.assertIn("MageOne", saved)

    def test_delete_character_sqlite(self) -> None:
        hero_name = "ToDelete"
        hero = Character.create(
            hero_name, ALL_CLASSES["Ladino"], ALL_RACES["Humano"]
        )
        save_character(hero, db_path=TEST_DB_PATH)

        self.assertTrue(delete_character(hero_name, db_path=TEST_DB_PATH))
        self.assertIsNone(load_character(hero_name, db_path=TEST_DB_PATH))
        self.assertFalse(delete_character(hero_name, db_path=TEST_DB_PATH))


if __name__ == "__main__":
    unittest.main()
