"""Guard the prominent Phantom Labs tool-door index against missing future tools.

No network calls. Run via:
    python3 -m unittest discover -s tests -p 'test_tool_vault_doors.py' -v
"""
from collections import Counter
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT / "docs" / "TOOL_VAULT.md"
START = "<!-- PHANTOM-DOOR-INDEX:START -->"
END = "<!-- PHANTOM-DOOR-INDEX:END -->"
DOOR_ROW = re.compile(
    r"^\|\s*(?P<name>[^|]+?)\s*\|\s*(?P<purpose>[^|]+?)\s*\|\s*"
    r"\[Open (?:source|project)\]\((?P<source>\.\./tools/[^)]+)\)\s*\|\s*"
    r"\[Setup guide\]\((?P<guide>tool-showcases/[^)]+\.md)\)\s*\|\s*$",
    re.MULTILINE,
)


def indexed_doors():
    vault = VAULT.read_text(encoding="utf-8")
    if vault.count(START) != 1 or vault.count(END) != 1:
        raise AssertionError("The Tool Vault needs exactly one marked door index")
    before, rest = vault.split(START, 1)
    indexed, _ = rest.split(END, 1)
    return before, [match.groupdict() for match in DOOR_ROW.finditer(indexed)]


def discovered_sources():
    """All standalone Python entry points and Go projects are required."""
    tools = ROOT / "tools"
    python_files = [
        *tools.glob("*.py"),
        *tools.glob("*/*.py"),
    ]
    python_files = [p for p in python_files if p.name != "__init__.py"]
    go_projects = [p.parent for p in tools.glob("go/*/go.mod")]
    return {
        "../" + p.relative_to(ROOT).as_posix() for p in python_files
    } | {
        "../" + p.relative_to(ROOT).as_posix() + "/" for p in go_projects
    }


class ToolVaultDoorChecks(unittest.TestCase):
    def test_complete_and_unique_source_inventory(self):
        before, doors = indexed_doors()
        self.assertIn("PHANTOM TOOL VAULT", before)
        self.assertTrue(doors, "No tool doors found")
        sources = [door["source"] for door in doors]
        counts = Counter(sources)
        self.assertEqual(len(counts), len(sources), f"Duplicate doors: {counts}")
        expected = discovered_sources()
        actual = set(sources)
        self.assertEqual(
            expected, actual,
            "New/removed tools must be reconciled with the main Tool Vault "
            "index. Missing doors: {}. Obsolete doors: {}".format(
                sorted(expected - actual), sorted(actual - expected)
            ),
        )

    def test_every_door_has_real_source_and_unique_setup_guide(self):
        _, doors = indexed_doors()
        guides = [door["guide"] for door in doors]
        self.assertEqual(len(guides), len(set(guides)), "Give every tool its own guide")
        for door in doors:
            with self.subTest(tool=door["name"]):
                self.assertTrue(door["name"].strip())
                self.assertTrue(door["purpose"].strip())
                source = (VAULT.parent / door["source"]).resolve()
                guide = (VAULT.parent / door["guide"]).resolve()
                self.assertTrue(source.is_relative_to(ROOT), "Source must stay in repo")
                self.assertTrue(guide.is_relative_to(ROOT), "Guide must stay in repo")
                self.assertTrue(source.exists(), f"Missing source: {source}")
                self.assertTrue(guide.is_file(), f"Missing guide: {guide}")

    def test_door_index_appears_before_long_documentation(self):
        vault = VAULT.read_text(encoding="utf-8")
        self.assertLess(vault.index(START), vault.index("## 📋 The Phantom Build Recipe standard"))
        self.assertIn("All tool doors", vault)


if __name__ == "__main__":
    unittest.main()
