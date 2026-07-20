import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
POLICY = json.loads((ROOT / "profiles/secure-implementation-v1.json").read_text())


class SecureImplementationPolicyTests(unittest.TestCase):
    def test_new_sensitive_code_defaults_to_memory_safe_rust(self):
        language = POLICY["language_policy"]
        self.assertEqual("rust", language["new_privileged_network_parser_and_daemon_code"])
        self.assertTrue(language["rust_unsafe_forbidden_by_default"])
        self.assertTrue(language["unsafe_requires_documented_invariant_and_review"])
        self.assertTrue(language["new_c_or_cpp_requires_abi_hardware_or_upstream_justification"])

    def test_policy_prefers_hardened_integration_over_reinvention(self):
        integration = POLICY["integration_policy"]
        self.assertTrue(integration["prefer_mature_maintained_upstream"])
        self.assertFalse(integration["rewrite_upstream_by_default"])
        self.assertTrue(integration["pin_source_and_dependencies"])
        self.assertTrue(integration["isolate_imported_components"])

    def test_native_memory_hardening_is_required(self):
        hardening = POLICY["native_hardening"]
        for key, enabled in hardening.items():
            self.assertTrue(enabled, key)
        makefile = (
            ROOT
            / "product/package/batocera-deck-desktop-host/batocera-deck-desktop-host.mk"
        ).read_text()
        for flag in (
            "-fstack-protector-strong",
            "-fPIE",
            "-Wl,-z,relro",
            "-Wl,-z,now",
            "-Wl,-z,noexecstack",
            "-pie",
        ):
            self.assertIn(flag, makefile)

    def test_runtime_never_exposes_arbitrary_privileged_execution(self):
        runtime = POLICY["runtime"]
        self.assertTrue(runtime["unprivileged_by_default"])
        self.assertTrue(runtime["typed_privilege_broker"])
        self.assertFalse(runtime["arbitrary_privileged_commands"])
        self.assertFalse(runtime["custom_cryptography"])

    def test_human_policy_covers_secrets_fuzzing_and_faults(self):
        text = (ROOT / "docs/SECURE_IMPLEMENTATION.md").read_text()
        for phrase in (
            "default to stable Rust",
            "Core dumps are disabled",
            "coverage-guided fuzzing",
            "Low-memory and allocation-failure",
            "Do not design custom",
            "cryptography, password storage, or update-signature formats",
        ):
            self.assertIn(phrase, text)
        self.assertNotRegex(text, re.compile(r"guarantee[sd]? complete security", re.I))


if __name__ == "__main__":
    unittest.main()
