"""Offline checks for the Phantom Labs tool vault, recipes and relative links.

This runs through the existing Python unittest CI, without any web requests.
It validates documentation structure, not live tool execution or CLI semantics.
"""
from pathlib import Path
import re
import unittest
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT / "docs" / "TOOL_VAULT.md"
SHOWCASES = ROOT / "docs" / "tool-showcases"

# Markdown link targets. Fenced code blocks are removed before parsing so a
# quoted example inside Bash is not mistaken for a real Markdown link.
LINK = re.compile(r"!?(?:\[[^\]]*\])\(([^\s)]+)(?:\s+[^)]*)?\)")
FENCES = re.compile(r"(?ms)^\s*```[^\n]*\n.*?^\s*```[^\n]*$")
TABLE_MAPPING = re.compile(
    r"\[Source\]\(\.\./tools/([^)]*\.py)\)\s*"
    r"·\s*\[Build recipe\]\(tool-showcases/([^)]*\.md)\)"
)


def markdown_links(document):
    text = FENCES.sub("", document.read_text(encoding="utf-8"))
    return [match.group(1) for match in LINK.finditer(text)]


class ToolRecipeAudit(unittest.TestCase):
    def test_inventory_has_one_recipe_per_python_tool(self):
        source_files = {p.name for p in (ROOT / "tools").glob("*.py")}
        vault = VAULT.read_text(encoding="utf-8")
        mapping = TABLE_MAPPING.findall(vault)
        mapped = [name for name, _ in mapping]
        self.assertGreaterEqual(len(source_files), 19, "Missing original collection or newer tools")
        self.assertEqual(len(mapped), len(set(mapped)), "A Python script is listed twice")
        self.assertEqual(set(mapped), source_files, "Vault lacks a one-to-one recipe for each tool")
        for name, page in mapping:
            with self.subTest(tool=name):
                showcase = SHOWCASES / page
                self.assertTrue(showcase.is_file(), f"Missing recipe page: {page}")
                self.assertIn("../../tools/" + name, showcase.read_text(encoding="utf-8"))

    def test_go_tool_has_its_own_showcase(self):
        self.assertTrue((ROOT / "tools/go/voidlantern-go/main.go").is_file())
        self.assertTrue((ROOT / "tools/go/voidlantern-go/main_test.go").is_file())
        page = SHOWCASES / "VOIDLANTERN.md"
        self.assertTrue(page.is_file())
        self.assertIn("../../tools/go/voidlantern-go/", page.read_text(encoding="utf-8"))

    def test_every_showcase_has_recipe_and_troubleshooting(self):
        pages = [
            p for p in SHOWCASES.glob("*.md")
            if p.name != "SHOWCASE_TEMPLATE.md"
        ]
        self.assertEqual(len(pages), len(list((ROOT / "tools").glob("*.py"))) + 1, "Each Python tool and VOIDLANTERN needs one showcase")
        vault = VAULT.read_text(encoding="utf-8")
        for page in pages:
            with self.subTest(page=page.name):
                text = page.read_text(encoding="utf-8")
                self.assertIn("COPY & PASTE BUILD RECIPE", text)
                self.assertIn("```bash", text)
                self.assertIn("troubleshoot", text.lower())
                self.assertIn("test", text.lower())
                self.assertIn("run", text.lower())
                self.assertTrue("report" in text.lower() or "output" in text.lower())
                self.assertIn("tool-showcases/" + page.name, vault)

    def test_all_local_markdown_links_resolve(self):
        docs = [ROOT / "README.md", *sorted((ROOT / "docs").rglob("*.md"))]
        errors = []
        for page in docs:
            for url in markdown_links(page):
                parsed = urlsplit(url)
                if parsed.scheme or url.startswith("#") or url.startswith("//"):
                    continue  # external destinations and same-page anchors
                target = (page.parent / unquote(parsed.path)).resolve()
                if not target.is_relative_to(ROOT.resolve()):
                    errors.append(f"{page.relative_to(ROOT)}: out-of-repo {url}")
                elif not target.exists():
                    errors.append(f"{page.relative_to(ROOT)}: missing {url}")
        self.assertFalse(errors, "\n".join(errors))


if __name__ == "__main__":
    unittest.main()
