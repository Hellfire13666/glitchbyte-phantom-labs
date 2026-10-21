"""Offline regression tests for Master Hub v0.3.0: stdlib only."""
import importlib.util, json, pathlib, re, shutil, subprocess, tempfile, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
class HubV030Tests(unittest.TestCase):
    def test_exact_approved_art_bytes(self):
        import hashlib
        p=ROOT/'assets/rosie-phantom-spine-approved.png'
        self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(),'5c903ba9d080a5ac1efc1f7fc49618832346b8e16e8fed0bc31421d6f1559541')
    def test_official_links_present(self):
        text=(ROOT/'recipes/phantom-spine.html').read_text()
        self.assertIn('releases/tag/v0.2.0',text)
        self.assertIn('installers/phantom-spine-live-signal/v0.2.0',text)
        self.assertIn('github.com/Hellfire13666/phantom-spine-live-signal-2026',text)
    def test_real_commands_not_demo(self):
        text=(ROOT/'recipes/phantom-spine.html').read_text()
        self.assertNotIn('START_PHANTOM_SPINE.sh demo',text)
        self.assertNotIn('>Run synthetic demo<',text)
        self.assertEqual(text.count('class="copy"'),8)
        for part in ('--engine native','--engine hexbazaar','--via riftseal','--via local','phantom-spine-live-v020'):
            self.assertIn(part,text)
    def test_sibling_catalog_finds_final_and_legacy(self):
        with tempfile.TemporaryDirectory() as d:
            base=pathlib.Path(d)/'PhantomLabsLaunchers';base.mkdir()
            dest=base/ROOT.name
            shutil.copytree(ROOT,dest,ignore=shutil.ignore_patterns('catalog.js','__pycache__'))
            for tool in ('phantom-spine-live-signal-v0_2_0','phantom-spine-live-signal-v0_2_0_rc2','phantom-spine-intel-workshop-v0_1_0'):
                child=base/tool;child.mkdir();(child/'index.html').write_text('<!doctype html><title>Local tool</title>')
            r=subprocess.run(['python3','-B',str(dest/'scripts/refresh_catalog.py')],capture_output=True,text=True,check=True)
            catalog=(dest/'catalog.js').read_text()
            self.assertIn('phantom-spine-live-signal-v0_2_0/index.html',catalog)
            self.assertIn('phantom-spine-live-signal-v0_2_0_rc2/index.html',catalog)
            self.assertNotIn(str(pathlib.Path(d).resolve()),catalog)
            self.assertIn('3 HTML page(s)',r.stdout)
    def test_no_overwrite_shortcut_script(self):
        script=(ROOT/'OPTIONAL_ADD_DESKTOP_SHORTCUT.sh').read_text()
        self.assertIn('if [ -e "$FILE" ] || [ -L "$FILE" ]',script)
        self.assertIn('Switchboard-v3.desktop',script)
        self.assertNotIn('Switchboard-v2.desktop',script)
    def test_navigation_and_privacy(self):
        hub=(ROOT/'index.html').read_text()
        self.assertIn('spine-feature',hub)
        self.assertIn('rosie-phantom-spine-approved.png',hub)
        self.assertNotIn('Pasted text',hub)
        pub=(ROOT/'public-front-door.html').read_text()
        self.assertNotIn('catalog.js',pub)
        self.assertNotIn('/home/example/',pub)
    def test_script_integrity(self):
        subprocess.run(['python3','-B',str(ROOT/'scripts/verify_hub.py')],capture_output=True,text=True,check=True)
if __name__=='__main__':unittest.main()
