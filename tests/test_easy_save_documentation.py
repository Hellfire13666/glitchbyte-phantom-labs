"""Guard every indexed tool's beginner saving instructions, offline only."""
import re
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT / "docs" / "TOOL_VAULT.md"
EASY_GUIDE = ROOT / "docs" / "EASY_SAVE_ALL_TOOLS.md"
SAVER = ROOT / "scripts" / "phantom_easy_save.py"


class EasySaveDocumentationTests(unittest.TestCase):
    def test_each_indexed_tool_guide_has_easy_save_recipe(self):
        vault = VAULT.read_text(encoding="utf-8")
        pages = re.findall(r"\[Setup guide\]\(tool-showcases/([^)]+)\)", vault)
        self.assertGreaterEqual(len(set(pages)), 24)
        for page in set(pages):
            with self.subTest(page=page):
                doc = ROOT / "docs" / "tool-showcases" / page
                self.assertTrue(doc.is_file())
                content = doc.read_text(encoding="utf-8")
                self.assertIn("Easy Save", content)
                self.assertIn("EASY_SAVE_ALL_TOOLS.md", content)
                self.assertIn("--o", content)
                self.assertIn("-o", content)

    def test_hubs_link_to_easy_save_guide(self):
        self.assertTrue(EASY_GUIDE.is_file())
        self.assertTrue(SAVER.is_file())
        for page in (
            "README.md", "docs/TOOL_VAULT.md", "docs/CULTIVATION_ROOM.md",
            "docs/TOOL_STARTER_GUIDE.md", "docs/BEGINNER_RUNTIME_RECIPES.md",
            "docs/ECOSYSTEM.md", "docs/ROSIERIOT_OVERDRIVE_LAB.md",
            "docs/COPY_PASTE_OPEN.md", "docs/BUILD_PUBLICATION_STANDARD.md"
        ):
            with self.subTest(page=page):
                self.assertIn("EASY_SAVE_ALL_TOOLS.md",
                              (ROOT / page).read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
