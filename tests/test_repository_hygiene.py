import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKIP_PARTS = {".git", "__pycache__"}
VENDORED = {Path("third_party/bua/bua_installerx86.py")}
PRIVATE_NAMES = {
    "prod.keys",
    "title.keys",
    "keys.txt",
    "id_rsa",
    "id_ed25519",
}


class RepositoryHygieneTests(unittest.TestCase):
    def files(self):
        for path in ROOT.rglob("*"):
            if path.is_file() and not (set(path.relative_to(ROOT).parts) & SKIP_PARTS):
                yield path

    def test_no_private_payload_names(self):
        offenders = [str(path.relative_to(ROOT)) for path in self.files() if path.name in PRIVATE_NAMES]
        self.assertEqual(offenders, [])

    def test_no_accidental_large_files(self):
        limit = 5 * 1024 * 1024
        offenders = [str(path.relative_to(ROOT)) for path in self.files() if path.stat().st_size > limit]
        self.assertEqual(offenders, [])

    def test_no_moving_remote_code_execution_in_project_code(self):
        pipe_pattern = re.compile(r"(?:curl|wget).{0,200}\|\s*(?:ba)?sh", re.DOTALL)
        offenders = []
        for path in self.files():
            relative = path.relative_to(ROOT)
            if relative in VENDORED or b"\0" in path.read_bytes()[:4096]:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if pipe_pattern.search(text):
                offenders.append(str(relative))
        self.assertEqual(offenders, [])


if __name__ == "__main__":
    unittest.main()
