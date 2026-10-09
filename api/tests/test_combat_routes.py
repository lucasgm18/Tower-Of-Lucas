import unittest
import os
import tempfile
import sqlite3
from fastapi.testclient import TestClient
from api.app import app
from persistence.database import init_db
from persistence.save import save_character, load_character

client = TestClient(app)


class TestCombatRoutes(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        client.post(
            "/api/characters",
            json={
                "name": "CombatHero",
                "class_name": "Guerreiro",
                "race_name": "Humano",
            },
        )
        client.post(
            "/api/characters",
            json={
                "name": "RogueHero",
                "class_name": "Ladino",
                "race_name": "Humano",
            },
        )
        client.post(
            "/api/characters",
            json={
                "name": "ProgressionHero",
                "class_name": "Guerreiro",
                "race_name": "Humano",
            },
        )

    @classmethod
    def tearDownClass(cls) -> None:
        client.delete("/api/characters/CombatHero")
        client.delete("/api/characters/RogueHero")
        client.delete("/api/characters/ProgressionHero")

    def setUp(self) -> None:
        # Resetar ProgressionHero antes de cada teste para evitar interferência entre testes
        hero = load_character("ProgressionHero")
        if hero:
            hero = hero._with(current_floor=1, floor_progress=0, tower_completed=False)
            save_character(hero)

    def test_sqlite_migration_preserves_existing_characters(self) -> None:
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as tmp:
            tmp_db_path = tmp.name

        try:
            conn = sqlite3.connect(tmp_db_path)
            conn.execute("""
                CREATE TABLE characters (
                    name TEXT PRIMARY KEY,
                    class_name TEXT NOT NULL,
                    race_name TEXT NOT NULL,
                    hp INTEGER NOT NULL,
                    max_hp INTEGER NOT NULL,
                    atk INTEGER NOT NULL,
                    defense INTEGER NOT NULL,
                    speed INTEGER NOT NULL,
                    mana INTEGER NOT NULL,
                    max_mana INTEGER NOT NULL,
                    gold INTEGER NOT NULL DEFAULT 0,
                    exp INTEGER NOT NULL DEFAULT 0,
                    level INTEGER NOT NULL DEFAULT 1,
                    current_floor INTEGER NOT NULL DEFAULT 1,
                    skill_cooldowns TEXT NOT NULL DEFAULT '{}'
                );
            """)
            conn.execute("""
                INSERT INTO characters (
                    name, class_name, race_name, hp, max_hp, atk, defense, speed,
                    mana, max_mana, gold, exp, level, current_floor, skill_cooldowns
                ) VALUES (
                    'OldHero', 'Guerreiro', 'Humano', 100, 100, 15, 10, 5, 0, 0, 50, 0, 1, 3, '{}'
                )
            """)
            conn.commit()
            conn.close()

            init_db(tmp_db_path)

            loaded = load_character("OldHero", db_path=tmp_db_path)
            self.assertIsNotNone(loaded)
            self.assertEqual(loaded.name, "OldHero")
            self.assertEqual(loaded.current_floor, 3)
            self.assertEqual(loaded.floor_progress, 0)
            self.assertFalse(loaded.tower_completed)

        finally:
            if os.path.exists(tmp_db_path):
                os.remove(tmp_db_path)

    def test_monster_1_and_2_victory_do_not_advance_floor(self) -> None:
        # Iniciar 1ª batalha
        start_res = client.post("/api/combat/start", json={"character_name": "ProgressionHero"})
        self.assertEqual(start_res.status_code, 200)
        data = start_res.json()
        self.assertEqual(data["encounter_index"], 1)
        self.assertEqual(data["total_encounters"], 3)
        self.assertFalse(data["is_boss"])

        combat_id = data["combat_id"]
        for _ in range(20):
            res = client.post("/api/combat/action", json={"combat_id": combat_id, "action_type": "attack"})
            if res.status_code != 200 or res.json().get("victory"):
                break

        action_data = res.json()
        self.assertTrue(action_data["victory"])
        self.assertFalse(action_data["floor_completed"])

        updated_hero = load_character("ProgressionHero")
        self.assertEqual(updated_hero.current_floor, 1)
        self.assertEqual(updated_hero.floor_progress, 1)

    def test_monster_3_victory_advances_floor_on_normal_floor(self) -> None:
        hero = load_character("ProgressionHero")
        hero = hero._with(current_floor=1, floor_progress=2)
        save_character(hero)

        start_res = client.post("/api/combat/start", json={"character_name": "ProgressionHero"})
        self.assertEqual(start_res.status_code, 200)
        data = start_res.json()
        self.assertEqual(data["encounter_index"], 3)
        self.assertFalse(data["is_boss"])

        combat_id = data["combat_id"]
        for _ in range(20):
            res = client.post("/api/combat/action", json={"combat_id": combat_id, "action_type": "attack"})
            if res.status_code != 200 or res.json().get("victory"):
                break

        action_data = res.json()
        self.assertTrue(action_data["victory"])
        self.assertTrue(action_data["floor_completed"])

        updated_hero = load_character("ProgressionHero")
        self.assertEqual(updated_hero.current_floor, 2)
        self.assertEqual(updated_hero.floor_progress, 0)

    def test_floor_5_monster_3_victory_spawns_boss_guardian_next(self) -> None:
        hero = load_character("ProgressionHero")
        hero = hero._with(current_floor=5, floor_progress=3)
        save_character(hero)

        start_res = client.post("/api/combat/start", json={"character_name": "ProgressionHero"})
        self.assertEqual(start_res.status_code, 200)
        data = start_res.json()
        self.assertEqual(data["encounter_index"], 4)
        self.assertEqual(data["total_encounters"], 4)
        self.assertTrue(data["is_boss"])
        self.assertIn("Guardiao", data["monster"]["name"])

    def test_floor_10_boss_lucas_victory_completes_tower(self) -> None:
        hero = load_character("ProgressionHero")
        god_stats = hero.base_stats.apply_bonus(hp=1000, atk=500, defense=100, speed=50)
        hero = hero._with(base_stats=god_stats, current_floor=10, floor_progress=3)
        save_character(hero)

        start_res = client.post("/api/combat/start", json={"character_name": "ProgressionHero"})
        self.assertEqual(start_res.status_code, 200)
        data = start_res.json()
        self.assertEqual(data["encounter_index"], 4)
        self.assertTrue(data["is_boss"])
        self.assertEqual(data["monster"]["name"], "Lucas")

        combat_id = data["combat_id"]
        res = client.post("/api/combat/action", json={"combat_id": combat_id, "action_type": "attack"})
        action_data = res.json()
        self.assertTrue(action_data["victory"])
        self.assertTrue(action_data["floor_completed"])
        self.assertTrue(action_data["tower_completed"])

        updated_hero = load_character("ProgressionHero")
        self.assertEqual(updated_hero.current_floor, 10)
        self.assertTrue(updated_hero.tower_completed)

    def test_completed_tower_blocks_new_combat(self) -> None:
        hero = load_character("ProgressionHero")
        hero = hero.complete_tower()
        save_character(hero)

        start_res = client.post("/api/combat/start", json={"character_name": "ProgressionHero"})
        self.assertEqual(start_res.status_code, 400)
        self.assertIn("ja foi conquistada", start_res.json()["detail"])

    def test_server_restart_preserves_floor_progress(self) -> None:
        hero = load_character("ProgressionHero")
        hero = hero._with(current_floor=4, floor_progress=2, tower_completed=False)
        save_character(hero)

        reloaded = load_character("ProgressionHero")
        self.assertEqual(reloaded.current_floor, 4)
        self.assertEqual(reloaded.floor_progress, 2)
        self.assertFalse(reloaded.tower_completed)

    def test_character_response_reports_skill_cooldown(self) -> None:
        res = client.get("/api/characters/RogueHero")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertIn("skills", data)
        self.assertGreater(len(data["skills"]), 0)
        sneak_skill = next((s for s in data["skills"] if s["name"] == "Ataque Furtivo"), None)
        self.assertIsNotNone(sneak_skill)
        self.assertIn("cooldown_remaining", sneak_skill)
        self.assertIn("is_ready", sneak_skill)
        self.assertTrue(sneak_skill["is_ready"])
        self.assertEqual(sneak_skill["cooldown_remaining"], 0)

    def test_start_combat_resets_skill_cooldowns(self) -> None:
        # Configurar RogueHero no andar 5, encontro do Boss Guardião (100 HP)
        rogue = load_character("RogueHero")
        rogue = rogue._with(current_floor=5, floor_progress=3)
        save_character(rogue)

        start_res = client.post(
            "/api/combat/start",
            json={"character_name": "RogueHero"},
        )
        self.assertEqual(start_res.status_code, 200)
        self.assertTrue(start_res.json()["is_boss"])
        combat_id = start_res.json()["combat_id"]

        action_res = client.post(
            "/api/combat/action",
            json={
                "combat_id": combat_id,
                "action_type": "skill",
                "skill_name": "Ataque Furtivo",
            },
        )
        self.assertEqual(action_res.status_code, 200)
        self.assertFalse(action_res.json()["victory"])

        action_repeat = client.post(
            "/api/combat/action",
            json={
                "combat_id": combat_id,
                "action_type": "skill",
                "skill_name": "Ataque Furtivo",
            },
        )
        self.assertEqual(action_repeat.status_code, 400)
        self.assertIn("em recarga", action_repeat.json()["detail"])

        new_start = client.post(
            "/api/combat/start",
            json={"character_name": "RogueHero"},
        )
        self.assertEqual(new_start.status_code, 200)
        char_data = new_start.json()["character"]
        sneak = next(s for s in char_data["skills"] if s["name"] == "Ataque Furtivo")
        self.assertTrue(sneak["is_ready"])


if __name__ == "__main__":
    unittest.main()
