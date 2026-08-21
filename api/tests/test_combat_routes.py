import unittest
from fastapi.testclient import TestClient
from api.app import app

client = TestClient(app)


class TestCombatRoutes(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        # Create test hero
        client.post(
            "/api/characters",
            json={
                "name": "CombatHero",
                "class_name": "Guerreiro",
                "race_name": "Humano",
            },
        )

    @classmethod
    def tearDownClass(cls) -> None:
        client.delete("/api/characters/CombatHero")

    def test_combat_flow_start_and_action(self) -> None:
        # 1. Start combat session
        start_res = client.post(
            "/api/combat/start",
            json={"character_name": "CombatHero", "floor": 1},
        )
        self.assertEqual(start_res.status_code, 200)
        data = start_res.json()
        combat_id = data["combat_id"]
        self.assertTrue(combat_id.startswith("combat_"))
        self.assertEqual(data["character"]["name"], "CombatHero")
        self.assertIn(data["monster"]["name"], ["Goblin", "Rato Gigante", "Slime"])

        # 2. Perform attack action
        action_res = client.post(
            "/api/combat/action",
            json={
                "combat_id": combat_id,
                "action_type": "attack",
            },
        )
        self.assertEqual(action_res.status_code, 200)
        action_data = action_res.json()
        self.assertGreater(action_data["player_damage_dealt"], 0)
        self.assertIn("combat_log", action_data)


if __name__ == "__main__":
    unittest.main()
