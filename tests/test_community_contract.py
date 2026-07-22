import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
COMMUNITY = ROOT / "community"


class CommunityContractTests(unittest.TestCase):
    def test_canonical_reddit_configuration_is_complete(self):
        config = json.loads((COMMUNITY / "reddit/community.json").read_text())

        self.assertEqual(config["name"], "LuigiOS")
        self.assertFalse(config["over_18"])
        self.assertGreaterEqual(len(config["rules"]), 5)
        self.assertGreaterEqual(len(config["post_flair"]), 5)
        for post in config["seed_posts"]:
            source = ROOT / post["source"]
            self.assertTrue(source.is_file())
            self.assertGreater(len(source.read_text().strip()), 100)

    def test_channel_registry_never_publishes_placeholder_links(self):
        registry = json.loads((COMMUNITY / "channels.json").read_text())

        self.assertEqual(registry["schema_version"], 1)
        for platform in ("discord", "reddit"):
            details = registry[platform]
            published_link = details.get("invite") or details.get("url")
            if not details["status"].startswith("live"):
                self.assertIsNone(published_link)

    def test_live_discord_has_reviewable_identity(self):
        registry = json.loads((COMMUNITY / "channels.json").read_text())
        discord = registry["discord"]

        self.assertEqual(discord["status"], "live-soft-launch")
        self.assertRegex(discord["invite"], r"^https://discord\.gg/[A-Za-z0-9-]+$")
        self.assertRegex(discord["guild_id"], r"^[0-9]+$")
        self.assertTrue(discord["community_mode"])
        self.assertTrue(discord["onboarding"])

    def test_discord_onboarding_has_reviewed_default_channel_floor(self):
        blueprint = (COMMUNITY / "discord/server-blueprint.yml").read_text()
        default_match = re.search(
            r"^  default_channels: \[([^]]+)\]$", blueprint, re.MULTILINE
        )
        self.assertIsNotNone(default_match)

        default_channels = {
            value.strip() for value in default_match.group(1).split(",")
        }
        writable_channels = {
            match.group(1)
            for match in re.finditer(
                r"\{name: ([a-z0-9-]+),[^}]*writable: true,[^}]*default: true[^}]*\}",
                blueprint,
            )
        }

        self.assertGreaterEqual(len(default_channels), 7)
        self.assertGreaterEqual(len(default_channels & writable_channels), 5)
        self.assertIn("rules", default_channels)
        self.assertIn("help", default_channels)
        self.assertIn("forum_guidelines:", blueprint)
        self.assertIn("welcome_message:", blueprint)

    def test_automoderator_has_no_automatic_ban_action(self):
        automod = (COMMUNITY / "reddit/automoderator.yml").read_text().lower()

        self.assertNotRegex(automod, r"^action:\s*ban\s*$")
        self.assertIn("action: filter", automod)

    def test_downstream_policy_requires_no_promotional_credit(self):
        policy = (ROOT / "DOWNSTREAM.md").read_text()
        normalized = " ".join(policy.split())

        self.assertIn("does not require promotional credit", normalized)
        self.assertIn("component license controls", normalized)
        self.assertIn("compatibility entry", normalized)


if __name__ == "__main__":
    unittest.main()
