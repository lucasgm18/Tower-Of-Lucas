import unittest
import os
from fastapi.testclient import TestClient
from api.app import app
from persistence.database import DEFAULT_DB_PATH

client = TestClient(app)


class TestAPIRoutes(unittest.TestCase):

    def tearDown(self) -> None:
        # Clean up test characters if created
        client.delete("/api/characters/APITester")

    def test_root_endpoint(self) -> None:
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "online")

    def test_get_classes_endpoint(self) -> None:
        response = client.get("/api/classes")
        self.assertEqual(response.status_code, 200)
        classes_data = response.json()
        class_names = [c["name"] for c in classes_data]
        self.assertIn("Guerreiro", class_names)
        self.assertIn("Mago", class_names)
        self.assertIn("Ladino", class_names)

    def test_get_races_endpoint(self) -> None:
        response = client.get("/api/races")
        self.assertEqual(response.status_code, 200)
        races_data = response.json()
        race_names = [r["name"] for r in races_data]
        self.assertIn("Humano", race_names)
        self.assertIn("Orc", race_names)

    def test_character_crud_api(self) -> None:
        # 1. Create character via POST
        create_res = client.post(
            "/api/characters",
            json={
                "name": "APITester",
                "class_name": "Ladino",
                "race_name": "Humano",
            },
        )
        self.assertEqual(create_res.status_code, 201)
        data = create_res.json()
        self.assertEqual(data["name"], "APITester")
        self.assertEqual(data["class_name"], "Ladino")
        self.assertEqual(data["race_name"], "Humano")
        self.assertEqual(data["current_floor"], 1)

        # 2. Get character list via GET
        list_res = client.get("/api/characters")
        self.assertEqual(list_res.status_code, 200)
        self.assertIn("APITester", list_res.json())

        # 3. Get character details via GET
        get_res = client.get("/api/characters/APITester")
        self.assertEqual(get_res.status_code, 200)
        self.assertEqual(get_res.json()["name"], "APITester")

        # 4. Advance floor via POST
        advance_res = client.post("/api/characters/APITester/advance")
        self.assertEqual(advance_res.status_code, 200)
        self.assertEqual(advance_res.json()["current_floor"], 2)

        # 5. Delete character via DELETE
        del_res = client.delete("/api/characters/APITester")
        self.assertEqual(del_res.status_code, 204)

        # 6. Verify non-existent
        get_after_del = client.get("/api/characters/APITester")
        self.assertEqual(get_after_del.status_code, 404)


if __name__ == "__main__":
    unittest.main()
