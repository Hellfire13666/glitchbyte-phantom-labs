#!/usr/bin/env python3
"""Read-only local HTML page discovery for GlitchByte Phantom Labs Master Hub.

Writes ONLY hub/catalog.js, never touches sibling tool directories or reports.
"""
import json
import os
from pathlib import Path

HUB = Path(__file__).resolve().parent.parent
ROOT = HUB.parent
IGNORED = {'.git', '.venv', 'venv', 'node_modules', '__pycache__', 'site-packages', 'tests'}
KNOWN = (
    ('hexbazaar', 'HEXBAZAAR'),
    ('phantom-spine', 'PHANTOM SPINE'),
    ('riftseal', 'RIFTSEAL'),
    ('rootsignal', 'ROOTSIGNAL'),
    ('velvetecho', 'VELVETECHO'),
    ('subdominatrix', 'SUBDOMINATRIX'),
)

def human_name(s):
    low=s.lower()
    for k,v in KNOWN:
        if k in low:return v
    return s.replace('_',' ').replace('-',' ').strip().title()[:70]

def scan():
    output = []
    if not ROOT.is_dir(): return output
    for project in sorted(ROOT.iterdir(), key=lambda a:a.name.lower()):
        if project == HUB or not project.is_dir() or project.is_symlink() or project.name.startswith('.'):
            continue
        found=[]
        for page in sorted(project.glob('*.html')):
            if page.is_symlink() or not page.is_file(): continue
            if page.name.lower() in ('index.html','facebook-recipes.html'):
                found.insert(0,page)
            else: found.append(page)
        # One optional docs level; no recursive private-home search.
        doc=project/'docs'
        if doc.is_dir() and not doc.is_symlink():
            found.extend(p for p in sorted(doc.glob('*.html')) if p.is_file() and not p.is_symlink())
        for page in found[:18]:
            output.append({
                'project': human_name(project.name),
                'title': ('Main shop page' if page.name=='index.html' else 'Facebook recipes' if page.name=='facebook-recipes.html' else page.stem.replace('-',' ').replace('_',' ').title()),
                'type': 'Installed HTML',
                'href': Path(os.path.relpath(page, HUB)).as_posix(),
            })
    return sorted(output, key=lambda x:(x['project'].lower(),x['title'].lower()))[:300]

def main():
    rows=scan()
    dest=HUB/'catalog.js'
    dest.write_text('window.GB_CATALOG = '+json.dumps(rows,ensure_ascii=False,indent=2)+';\n',encoding='utf-8')
    print('[PASS] Hub catalog updated:',len(rows),'HTML page(s) discovered. No tool folders changed.')
    for r in rows:print(' •',r['project'],'/',r['title'])
if __name__=='__main__':main()
