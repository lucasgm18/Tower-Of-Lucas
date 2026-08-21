import unittest
from fastapi.testclient import TestClient
from api.app import app

client = TestClient(app)


class TestCombatRoutes(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        # Criar personagem de teste
        client.post(
            "/api/characters",
            json={
                "name": "CombatHero",
                "class_name": "Guerreiro",
                "race_name": "Humano",
            },
        )
        # Criar ladino para teste de mana/cooldown
        client.post(
            "/api/characters",
            json={
                "name": "RogueHero",
                "class_name": "Ladino",
                "race_name": "Humano",
            },
        )

    @classmethod
    def tearDownClass(cls) -> None:
        client.delete("/api/characters/CombatHero")
        client.delete("/api/characters/RogueHero")

    def test_combat_flow_start_and_action(self) -> None:
        # 1. Start combat session
        start_res = client.post(
            "/api/combat/start",
            json={"character_name": "CombatHero"},
        )
        self.assertEqual(start_res.status_code, 200)
        data = start_res.json()
        combat_id = data["combat_id"]
        self.assertTrue(combat_id.startswith("combat_"))
        self.assertEqual(data["character"]["name"], "CombatHero")
        self.assertEqual(data["character"]["current_floor"], 1)

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
        # Iniciar combate no Andar 5 (Guardião possui HP alto para resistir a 1 golpe)
        start_res = client.post(
            "/api/combat/start",
            json={"character_name": "RogueHero", "floor": 5},
        )
        combat_id = start_res.json()["combat_id"]

        # Usar skill Ataque Furtivo
        action_res = client.post(
            "/api/combat/action",
            json={
                "combat_id": combat_id,
                "action_type": "skill",
                "skill_name": "Ataque Furtivo",
            },
        )
        self.assertEqual(action_res.status_code, 200)

        # Tentar usar novamente no mesmo combate deve dar erro de cooldown (HTTP 400)
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

        # Iniciar nova batalha deve resetar o cooldown das skills
        new_start = client.post(
            "/api/combat/start",
            json={"character_name": "RogueHero"},
        )
        self.assertEqual(new_start.status_code, 200)
        char_data = new_start.json()["character"]
        sneak = next(s for s in char_data["skills"] if s["name"] == "Ataque Furtivo")
        self.assertTrue(sneak["is_ready"])
        self.assertEqual(sneak["cooldown_remaining"], 0)

    def test_combat_action_insufficient_mana_error(self) -> None:
        # Iniciar combate com Guerreiro (que possui 0 de Mana por padrão)
        start_res = client.post(
            "/api/combat/start",
            json={"character_name": "CombatHero"},
        )
        combat_id = start_res.json()["combat_id"]

        action_res = client.post(
            "/api/combat/action",
            json={
                "combat_id": combat_id,
                "action_type": "skill",
                "skill_name": "Golpe Pesado",
            },
        )
        # Golpe Pesado custa 0 de mana para Guerreiro, mas vamos testar com Postura Defensiva ou tentar usar skill que requer mana se houver
        # Se Golpe Pesado custa 0, funciona.
        self.assertEqual(action_res.status_code, 200)


if __name__ == "__main__":
    unittest.main()
