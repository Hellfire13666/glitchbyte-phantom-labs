import ast
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

class RepositoryTests(unittest.TestCase):
    def test_python_syntax(self):
        scripts = sorted((ROOT / "tools").glob("*.py"))
        self.assertGreaterEqual(len(scripts), 16)
        for script in scripts:
            with self.subTest(script=script.name):
                ast.parse(script.read_text(encoding="utf-8"), filename=str(script))

    def test_project_files(self):
        for filename in ("README.md", "LICENSE-NOTICE.md", "SECURITY.md", ".gitignore"):
            self.assertTrue((ROOT / filename).is_file(), filename)

if __name__ == "__main__":
    unittest.main()
