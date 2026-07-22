import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_PATH = ROOT / "profiles" / "settings-registry-v1.json"


class SettingsRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))

    def test_ui_is_unprivileged_and_operations_are_typed(self):
        broker = self.registry["broker"]
        self.assertFalse(broker["run_ui_as_root"])
        self.assertFalse(broker["allow_arbitrary_commands"])
        self.assertFalse(broker["allow_arbitrary_paths"])
        self.assertTrue(broker["require_typed_operations"])

    def test_surface_ids_and_providers_are_explicit(self):
        surfaces = self.registry["surfaces"]
        ids = [surface["id"] for surface in surfaces]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertIn("updates", ids)
        self.assertIn("backup-restore", ids)
        for surface in surfaces:
            self.assertRegex(surface["provider"], r"^[a-z][a-z0-9.-]+$")
            self.assertNotIn("command", surface)
            self.assertIn(surface["restart"], {"none", "game", "session", "reboot"})

    def test_required_input_modes_are_first_class(self):
        inputs = self.registry["input"]
        self.assertTrue(inputs["controller"])
        self.assertTrue(inputs["touch"])
        self.assertTrue(inputs["keyboard_mouse"])
        self.assertTrue(inputs["external_controller_reconnect"])

    def test_developer_mode_is_not_visible_by_default(self):
        developer = next(
            surface for surface in self.registry["surfaces"] if surface["id"] == "developer"
        )
        self.assertTrue(developer["hidden_by_default"])
        self.assertIn("gamer", developer["visible_in_modes"])
        self.assertEqual("experience-modes-v1.json", self.registry["experience_policy"])


if __name__ == "__main__":
    unittest.main()
