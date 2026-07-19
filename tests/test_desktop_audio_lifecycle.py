import json
import os
import pathlib
import shutil
import subprocess
import tempfile
import textwrap
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
SESSION = ROOT / "prototype/desktop/arch-plasma-session.sh"


class DesktopAudioLifecycleTests(unittest.TestCase):
    def setUp(self):
        if shutil.which("jq") is None:
            self.skipTest("jq is required for the audio lifecycle helper")
        self.tempdir = tempfile.TemporaryDirectory()
        self.work = pathlib.Path(self.tempdir.name)
        self.pulse_state = self.work / "pulse.json"
        self.saved_state = self.work / "saved.tsv"
        self.log = self.work / "pactl.log"
        self.bin = self.work / "bin"
        self.bin.mkdir()
        pactl = self.bin / "pactl"
        pactl.write_text(
            textwrap.dedent(
                """\
                #!/usr/bin/env python3
                import json
                import os
                import pathlib
                import sys

                state_path = pathlib.Path(os.environ["FAKE_PULSE_STATE"])
                log_path = pathlib.Path(os.environ["FAKE_PACTL_LOG"])
                state = json.loads(state_path.read_text())
                args = sys.argv[1:]

                if args == ["-f", "json", "list", "sink-inputs"]:
                    streams = state["streams"]
                    print(json.dumps(streams))
                    state["list_calls"] = state.get("list_calls", 0) + 1
                    if state.get("swap_after_list") == state["list_calls"]:
                        state["streams"] = state["replacement_streams"]
                    state_path.write_text(json.dumps(state))
                    raise SystemExit(0)

                if len(args) == 3 and args[0] == "set-sink-input-mute":
                    index = int(args[1])
                    value = args[2] in ("1", "yes", "true")
                    log_path.open("a").write(f"{index} {int(value)}\\n")
                    for stream in state["streams"]:
                        if stream["index"] == index:
                            stream["mute"] = value
                            state_path.write_text(json.dumps(state))
                            raise SystemExit(0)
                    raise SystemExit(1)

                raise SystemExit(2)
                """
            )
        )
        pactl.chmod(0o755)

        source = SESSION.read_text()
        functions = source[source.index("restore_es_audio() {") : source.index("is_container_process() {")]
        self.harness = self.work / "audio-harness.sh"
        self.harness.write_text(
            "#!/bin/bash\nset -u\n"
            + functions
            + '\nes_audio_state="$FAKE_SAVED_STATE"\n"$@"\n'
        )
        self.harness.chmod(0o755)

    def tearDown(self):
        self.tempdir.cleanup()

    @staticmethod
    def es_stream(index, serial, muted, name="ES-DE", node=None, process_id="4242"):
        return {
            "index": index,
            "mute": muted,
            "properties": {
                "object.serial": str(serial),
                "application.process.id": process_id,
                "application.process.binary": "emulationstation",
                "application.name": name,
                "media.name": "Music",
                "media.role": "music",
                "node.name": node or f"emulationstation-{serial}",
            },
        }

    @staticmethod
    def other_stream(index, muted=False):
        return {
            "index": index,
            "mute": muted,
            "properties": {
                "object.serial": "9000",
                "application.process.id": "5151",
                "application.process.binary": "firefox",
                "application.name": "Firefox",
                "node.name": "firefox",
            },
        }

    def write_pulse_state(self, streams, **extra):
        self.pulse_state.write_text(json.dumps({"streams": streams, **extra}))

    def run_helper(self, function):
        env = os.environ.copy()
        env.update(
            {
                "PATH": f"{self.bin}:{env['PATH']}",
                "FAKE_PULSE_STATE": str(self.pulse_state),
                "FAKE_PACTL_LOG": str(self.log),
                "FAKE_SAVED_STATE": str(self.saved_state),
            }
        )
        subprocess.run([self.harness, function], check=True, env=env)

    def streams(self):
        return json.loads(self.pulse_state.read_text())["streams"]

    def test_late_streams_restore_independent_state_and_ignore_reused_index(self):
        self.write_pulse_state(
            [self.es_stream(7, 100, False), self.es_stream(8, 101, True), self.other_stream(9)]
        )
        self.run_helper("mute_es_audio")
        self.assertEqual([stream["mute"] for stream in self.streams()], [True, True, False])

        # Pulse reused 7 for an unrelated app. A recreated ES stream gets a
        # new serial and index and must receive its own baseline on the poll.
        self.write_pulse_state(
            [self.other_stream(7), self.es_stream(8, 101, True), self.es_stream(12, 102, False)]
        )
        self.run_helper("mute_es_audio")
        self.assertEqual([stream["mute"] for stream in self.streams()], [False, True, True])

        self.log.write_text("")
        self.run_helper("restore_es_audio")
        self.assertEqual([stream["mute"] for stream in self.streams()], [False, True, False])
        self.assertFalse(any(line.startswith("7 ") for line in self.log.read_text().splitlines()))
        self.assertFalse(self.saved_state.exists())

    def test_index_is_reverified_immediately_before_muting(self):
        original = [self.es_stream(4, 200, False)]
        replacement = [self.other_stream(4)]
        self.write_pulse_state(
            original,
            swap_after_list=1,
            replacement_streams=replacement,
        )

        self.run_helper("mute_es_audio")

        self.assertFalse(self.streams()[0]["mute"])
        self.assertFalse(self.log.exists())

    def test_recreated_logical_stream_inherits_original_unmuted_baseline(self):
        self.write_pulse_state([self.es_stream(7, 100, False, node="emulationstation-X")])
        self.run_helper("mute_es_audio")
        self.assertTrue(self.streams()[0]["mute"])

        # PipeWire stream-restore may initialize the replacement from our
        # temporary mute. Its new serial/index identify a new instance, while
        # the stable application/node/media properties identify the same
        # logical stream whose original baseline was unmuted.
        self.write_pulse_state(
            [
                self.es_stream(
                    12,
                    102,
                    True,
                    node="emulationstation-X",
                    process_id="4343",
                )
            ]
        )
        self.run_helper("mute_es_audio")
        self.assertTrue(self.streams()[0]["mute"])

        self.run_helper("restore_es_audio")
        self.assertFalse(self.streams()[0]["mute"])


if __name__ == "__main__":
    unittest.main()
