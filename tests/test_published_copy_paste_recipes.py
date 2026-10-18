"""Execute the documented first Bash recipe for each tool under a fresh HOME.

Git maps the public clone URL to the current checkout for deterministic,
offline clones. This checks shell instructions, not an internet clone or
live integrations. Each isolated HOME is removed after its run.
"""
import os
from pathlib import Path
import re
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs" / "tool-showcases"
REMOTE = "https://github.com/Hellfire13666/glitchbyte-phantom-labs.git"
PAGES = (
    "LOG_CONSTELLATION", "DOMAIN_INTEL", "USERNAME_INTEL",
    "ROSE_CRAWLER", "SIGNAL_GARDEN", "DOMAIN_PHANTOM",
    "IP_SPECTER", "IP_SHADOW_SCRAPER", "X_INTEL_PHANTOM",
    "X_SHADOW_NO_API", "GHOST_IN_MY_HEART", "DARK_DESIRE",
    "FIND_ME_IF_YOU_LOVE_ME", "CATCH_ME_IN_THE_CHAOS",
    "HACKGIRL_INTEL", "NEON_ROSE_PHANTOM_3", "VOIDLANTERN",
)
FIRST_BASH = re.compile(r"(?m)^\x60{3}bash[ \t]*\n(.*?)^\x60{3}[ \t]*$", re.S | re.M)


class PublishedRecipeExecution(unittest.TestCase):
    def test_all_17_published_first_blocks(self):
        self.assertEqual(len(PAGES), 17)
        for page in PAGES:
            with self.subTest(page=page):
                path = DOCS / (page + ".md")
                md = path.read_text(encoding="utf-8")
                found = FIRST_BASH.search(md)
                self.assertIsNotNone(found, f"No Bash block: {page}")
                bash = found.group(1)
                self.assertIn("git clone " + REMOTE, bash, page)
                self.assertNotIn("--fetch", bash, "Unsafe live-fetch flag")
                with tempfile.TemporaryDirectory(prefix="phantom-clean-home-") as temp:
                    home = Path(temp)
                    env = os.environ.copy()
                    env["HOME"] = temp
                    env["PYTHONDONTWRITEBYTECODE"] = "1"
                    env["GIT_CONFIG_COUNT"] = "1"
                    env["GIT_CONFIG_KEY_0"] = f"url.file://{ROOT}/.insteadOf"
                    env["GIT_CONFIG_VALUE_0"] = REMOTE
                    # Blank input safely skips live authorized target checks.
                    inputs = "phantomlabdemo\n" if page == "USERNAME_INTEL" else "\n"
                    run = subprocess.run(
                        ["bash", "-c", bash],
                        input=inputs, text=True, capture_output=True,
                        cwd=temp, env=env, timeout=110,
                    )
                    if run.returncode:
                        self.fail(
                            f"{page} returned {run.returncode}.\n"
                            f"Last stdout:\n{run.stdout[-1600:]}\n"
                            f"Last stderr:\n{run.stderr[-1600:]}"
                        )
                    checkouts = list(home.rglob("glitchbyte-phantom-labs/.git"))
                    self.assertTrue(checkouts, "Git clone was not exercised")
                    print(f"PASS: {page} published first Bash recipe")


if __name__ == "__main__":
    unittest.main()
