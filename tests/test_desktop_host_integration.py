import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class DesktopHostIntegrationTests(unittest.TestCase):
    def test_audio_endpoint_is_local_and_dedicated(self):
        config = (ROOT / "prototype/desktop/90-desktop-pulse.conf").read_text()

        self.assertIn("unix:/run/arch-plasma-audio/native", config)
        self.assertNotIn("tcp:", config)

    def test_desktop_uses_host_audio_without_starting_a_second_stack(self):
        session = (ROOT / "prototype/desktop/arch-plasma-session.sh").read_text()
        service = (ROOT / "prototype/services/desktop_host_integration").read_text()

        self.assertIn("PULSE_SERVER=unix:/run/arch-plasma-audio/native", session)
        for daemon in ("pipewire &", "wireplumber &", "pulseaudio"):
            self.assertNotIn(daemon, session)
            self.assertNotIn(daemon, service)

    def test_emulationstation_audio_is_scoped_and_restorable(self):
        session = (ROOT / "prototype/desktop/arch-plasma-session.sh").read_text()

        self.assertIn('contains("emulationstation")', session)
        self.assertIn("es_audio_instance_for_index", session)
        self.assertIn("$logical", session)
        self.assertIn("set-sink-input-mute", session)
        self.assertNotIn("set-sink-mute", session)
        self.assertLess(session.index("trap cleanup"), session.index("mute_es_audio\n"))

    def test_connman_policy_does_not_introduce_network_manager(self):
        policy = (ROOT / "prototype/desktop/desktop-connman.conf").read_text()
        autostart = (ROOT / "prototype/desktop/cmst-autostart.desktop").read_text()

        self.assertIn('send_destination="net.connman"', policy)
        self.assertIn("Exec=/usr/bin/cmst --minimized", autostart)
        self.assertNotIn("NetworkManager", policy + autostart)


if __name__ == "__main__":
    unittest.main()
