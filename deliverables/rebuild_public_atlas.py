#!/usr/bin/env python3
"""Rebuild the standalone atlas HTML from delivered JSON and font assets."""
import argparse
import json
from pathlib import Path
import build_paper_atlas as builder

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--atlas',type=Path,default=Path(__file__).with_name('paper-atlas.json'))
p.add_argument('--out',type=Path,default=Path(__file__).with_name('paper-atlas.rebuilt.html'))
a=p.parse_args()
atlas=json.loads(a.atlas.read_text())
content=builder.make_html(atlas['records'],atlas['statistics'])
a.out.write_text(content,encoding='utf-8')
print(json.dumps({'out':str(a.out),'records':len(atlas['records']),'bytes':a.out.stat().st_size}))
