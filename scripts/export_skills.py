"""Export nine skills in one language to a NEW directory, without installing."""
from pathlib import Path
import argparse, shutil
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--language',choices=['zh','en'],required=True)
p.add_argument('--output',type=Path,required=True)
a=p.parse_args();src=Path(__file__).resolve().parents[1]/'skills';out=a.output.resolve()
if out.exists():p.error('Output already exists; choose a new directory. Nothing was overwritten.')
if out==src or src in out.parents:p.error('Export outside the source skills directory.')
folders=sorted(src.glob('sci-figure-*'))
if len(folders)!=9:p.error('Expected exactly nine skills.')
if a.language=='en' and any(not (s/'SKILL.en.md').is_file() for s in folders):p.error('Missing English entrypoint.')
out.mkdir(parents=True)
for s in folders:
 d=out/s.name;shutil.copytree(s,d)
 if a.language=='en':
  shutil.copy2(d/'SKILL.md',d/'SKILL.zh.md');shutil.copy2(d/'SKILL.en.md',d/'SKILL.md')
print(f'Exported {len(folders)} skills ({a.language}) to {out}; not installed.')
