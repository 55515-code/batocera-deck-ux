import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = json.loads(
    (ROOT / "profiles/library-vault-v1.json").read_text(encoding="utf-8")
)


class LibraryVaultPolicyTests(unittest.TestCase):
    def test_paths_follow_batocera_system_definitions(self):
        self.assertEqual(
            POLICY["system_definition_source"],
            "batocera-es-system/es_systems.yml",
        )
        self.assertEqual(POLICY["library"]["source_template"], "/userdata/roms/{system}")
        self.assertTrue(POLICY["selection"]["derive_extensions_from_system_definitions"])

    def test_import_is_staged_and_recoverable(self):
        importing = POLICY["import"]
        self.assertTrue(importing["quarantine_before_library"])
        self.assertTrue(importing["verify_manifest_hashes"])
        self.assertTrue(importing["free_space_reservation"])
        self.assertTrue(importing["rollback_journal"])
        self.assertFalse(importing["auto_execute_received_files"])

    def test_sensitive_payloads_and_raw_configs_are_separate(self):
        restricted = POLICY["restricted"]
        self.assertIn("/userdata/bios", restricted["deny_paths"])
        self.assertIn("/userdata/system", restricted["deny_paths"])
        self.assertIn("prod.keys", restricted["deny_names"])
        self.assertFalse(restricted["raw_emulator_config_transfer"])
        self.assertFalse(restricted["firmware_and_bios_transfer"])
        self.assertFalse(POLICY["selection"]["include_raw_configs"])

    def test_shared_presets_are_declarative(self):
        presets = POLICY["presets"]
        self.assertEqual(presets["format"], "versioned-declarative-allowlist")
        self.assertFalse(presets["allow_commands"])
        self.assertFalse(presets["allow_absolute_paths"])
        self.assertFalse(presets["allow_credentials"])
        self.assertTrue(presets["require_preview"])


if __name__ == "__main__":
    unittest.main()
