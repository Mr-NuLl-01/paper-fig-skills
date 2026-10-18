"""Check synthetic-data invariants and exported figure structure; not a visual review."""
from pathlib import Path
import json, xml.etree.ElementTree as ET
import numpy as np
p=Path(__file__).resolve().parent/'output'
svgs=sorted(p.glob('*.svg')); assert len(svgs) in (8,9)
for s in svgs:
 root=ET.parse(s).getroot();texts=root.findall('.//{http://www.w3.org/2000/svg}text')
 assert texts, s
 assert 'SYNTHETIC DEMO' in ''.join(root.itertext()), s
 for suffix in ['.png','.pdf']:assert s.with_suffix(suffix).stat().st_size>1000
j=lambda n:json.loads((p/f'{n}.json').read_text())
d=j('01_paired');assert len(d['before'])==len(d['after'])==90;assert np.bincount(d['batch']).tolist()==[30,30,30]
d=j('05_heatmaps');A=np.array(d['A']);B=np.array(d['B']);m=np.array(d['mask']);assert A.shape==B.shape==m.shape==(81,151);assert m.sum()==0;assert np.isfinite(A).all()
d=j('06_heatmap_stack');assert d['time_s']==[0,2,7];assert np.shape(d['fields'])==(3,31,31)
d=j('07_waterfall');assert d['temperature_K']==[280,295,320,355,400];assert np.shape(d['intensity'])==(5,151);assert len(set(np.diff(d['temperature_K'])))>1
d=j('08_volume_layout');v=np.array(d['volume']);assert v.shape==(31,31,31);assert d['axis_order']=='x,y,z';assert d['axes_um'][d['slice_index']]==0; assert v.min()<0<v.max(); assert np.allclose(v,-v[::-1,:,:])
print(f'PASS: {len(svgs)} editable SVG/PNG/PDF exports and synthetic-data invariants. Visual review is separate.')
