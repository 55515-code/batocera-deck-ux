import pathlib
import re
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]


class PlasmaRecoveryTests(unittest.TestCase):
    def test_status_is_observational(self):
        service = (ROOT / "prototype/services/plasma_recovery").read_text()
        status = re.search(r"\n    status\)\n(.*?)\n        ;;", service, re.DOTALL)

        self.assertIsNotNone(status)
        self.assertNotIn("recover_if_stale", status.group(1))
        self.assertNotIn("rm ", status.group(1))
        self.assertNotRegex(status.group(1), r"kill\s+(?!-0)")

    def test_transaction_state_contains_process_start_time(self):
        launcher = (ROOT / "prototype/desktop/desktop").read_text()
        recovery = (ROOT / "prototype/services/plasma_recovery").read_text()

        self.assertIn('awk \'{print $22}\' "/proc/$$/stat"', launcher)
        self.assertIn("recorded_start", recovery)
        self.assertIn("current_start", recovery)


if __name__ == "__main__":
    unittest.main()
