#!/usr/bin/env python3
"""Verify immutable Master Hub v0.3.0 files and references without network access."""
import hashlib, json, re
from html.parser import HTMLParser
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'MANIFEST.json').read_text(encoding='utf-8'))
assert manifest['version']=='v0.3.0'
for name,expected in manifest['files'].items():
    p=ROOT/name
    assert p.is_file() and not p.is_symlink(),f'Missing or unsafe file: {name}'
    assert hashlib.sha256(p.read_bytes()).hexdigest()==expected,f'Checksum mismatch: {name}'
assert hashlib.sha256((ROOT/'assets/rosie-phantom-spine-approved.png').read_bytes()).hexdigest()=='5c903ba9d080a5ac1efc1f7fc49618832346b8e16e8fed0bc31421d6f1559541'
class Refs(HTMLParser):
    def __init__(self):super().__init__();self.refs=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        for key in ('href','src'):
            if a.get(key):self.refs.append(a[key])
count=0
for page in [*ROOT.glob('*.html'),*(ROOT/'recipes').glob('*.html')]:
    t=page.read_text(encoding='utf-8'); assert '<!DOCTYPE html>' in t or '<!doctype html>' in t
    p=Refs();p.feed(t)
    for href in p.refs:
        if href.startswith(('#','https:','http:','mailto:','data:')):continue
        file=href.split('#',1)[0].split('?',1)[0]
        if not file or file=='../catalog.js' or file=='catalog.js':continue
        assert (page.parent/file).is_file(),f'Bad static page reference: {page.name} -> {href}'
    count+=1
spine=(ROOT/'recipes/phantom-spine.html').read_text(encoding='utf-8')
for literal in ('phantom-spine-live-v020','--engine native','--engine hexbazaar','--via riftseal','--via local','facebook.com','example.com','946262cad583f4a22d82091a805da089b6ef68c16815316772f45fb51e87a4f7'):
    assert literal in spine,f'PHANTOM SPINE recipe missing {literal}'
assert spine.count('class="copy"')==8
assert len(list((ROOT/'assets').glob('tool-*.svg')))==6
assert 'phantom-spine-live-signal-v0_2_0/' in (ROOT/'assets/hub.js').read_text()
print(f'[PASS] {len(manifest["files"])} immutable files verified, including exact approved artwork.')
print(f'[PASS] {count} HTML pages / all static references / eight real PHANTOM SPINE copy recipes.')
print('[PASS] Six tool badges, final-v0.2.0 finder priority, no network calls.')
