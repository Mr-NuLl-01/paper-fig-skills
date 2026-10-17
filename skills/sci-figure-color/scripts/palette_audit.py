#!/usr/bin/env python3
"""Finite palette diagnostics. Standard library only. No image/data modification.
Machado 2009 severity-1 matrices, applied to linear RGB; see bundled sources.
Outputs editable SVG and JSON. Delta E is CIE76, not CIEDE2000.
"""
import argparse
import html
import itertools
import json
import math
import re
from pathlib import Path

CVD = {
    'protanopia': [[.152286, 1.052583, -.204868], [.114503, .786281, .099216], [-.003882, -.048116, 1.051998]],
    'deuteranopia': [[.367322, .860646, -.227968], [.280085, .672501, .047413], [-.011820, .042940, .968881]],
    'tritanopia': [[1.255528, -.076749, -.178779], [-.078411, .930809, .147602], [.004733, .691367, .303900]]
}

def rgb(h):
    if not re.fullmatch(r'#[0-9a-fA-F]{6}', h):
        raise ValueError('Expected #RRGGBB, got '+repr(h))
    return [int(h[i:i+2], 16)/255 for i in (1,3,5)]

def decode(v):
    return v/12.92 if v <= .04045 else ((v+.055)/1.055)**2.4

def encode(v):
    return 12.92*v if v <= .0031308 else 1.055*v**(1/2.4)-.055

def lin(h):
    return [decode(v) for v in rgb(h)]

def ashex(v):
    return '#'+''.join(f'{round(255*min(1,max(0,x))):02X}' for x in v)

def dot(a,b):
    return sum(x*y for x,y in zip(a,b))

def luminance(h):
    return dot([.2126,.7152,.0722], lin(h))

def lab(h):
    v=lin(h)
    xyz=[dot(r,v)/w for r,w in zip([[.4124564,.3575761,.1804375],[.2126729,.7151522,.0721750],[.0193339,.1191920,.9503041]],[.95047,1,1.08883])]
    d=6/29
    f=[t**(1/3) if t>d**3 else t/(3*d*d)+4/29 for t in xyz]
    return [116*f[1]-16,500*(f[0]-f[1]),200*(f[1]-f[2])]

def simulate(h,matrix):
    values=[dot(row,lin(h)) for row in matrix]
    clipped=sum(x<0 or x>1 for x in values)
    return ashex([encode(min(1,max(0,x))) for x in values]),clipped

def metrics(colors,background):
    labs=[lab(h) for h in colors]
    pairs=[]
    for i,j in itertools.combinations(range(len(colors)),2):
        pairs.append({'pair':[i+1,j+1],'delta_e76':round(math.dist(labs[i],labs[j]),3)})
    pairs.sort(key=lambda v:v['delta_e76'])
    b=luminance(background)
    return {'L_star':[round(x[0],3) for x in labs],
            'contrast_to_background':[round((max(luminance(h),b)+.05)/(min(luminance(h),b)+.05),3) for h in colors],
            'nearest_pairs':pairs[:min(4,len(pairs))]}

def audit(colors,background):
    cases={'original':{'colors':colors,'background':background,'clipped_components':0}}
    for name,m in CVD.items():
        vals=[simulate(h,m) for h in colors]
        bg,n=simulate(background,m)
        cases[name]={'colors':[v[0] for v in vals],'background':bg,'clipped_components':sum(v[1] for v in vals)+n}
    cases['grayscale']={'colors':[ashex([encode(luminance(h))]*3) for h in colors],'background':ashex([encode(luminance(background))]*3),'clipped_components':0}
    for v in cases.values():v.update(metrics(v['colors'],v['background']))
    return {'method':'sRGB D65, CIELAB delta-E76; Machado2009 severity=1, linear RGB; gamut clipped',
            'scope':'Finite diagnostic only. Not a universal accessibility pass; inspect actual figures at final size. Grayscale alone need not distinguish all categories.',
            'source':'https://doi.org/10.1109/TVCG.2009.113', 'cases':cases}

def svg_report(result,title):
    n=len(result['cases']['original']['colors']);w=max(880,230+n*114);h=580
    s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{210*w/880:.3f}mm" height="{210*h/880:.3f}mm" viewBox="0 0 {w} {h}">',
       '<metadata>'+html.escape(json.dumps({'title':title,'purpose':'Palette diagnostic, not scientific data'},ensure_ascii=False))+'</metadata>',
       '<rect width="100%" height="100%" fill="white"/>',
       '<g font-family="Arial, DejaVu Sans, sans-serif" fill="#26313D">',
       f'<text x="24" y="38" font-size="23" font-weight="bold">{html.escape(title)}</text>',
       '<text x="24" y="65" font-size="13">Original combinations • finite simulations • verify in the actual figure</text>']
    for i,(name,v) in enumerate(result['cases'].items()):
        y=96+i*82
        s.append(f'<text x="24" y="{y+25}" font-size="15">{name}</text>')
        near=v['nearest_pairs'][0]
        s.append(f'<text x="24" y="{y+47}" font-size="10.5">min ΔE76 {near["delta_e76"]:.1f} · pair {near["pair"][0]}/{near["pair"][1]}</text>')
        for j,c in enumerate(v['colors']):
            x=215+j*114
            s.append(f'<rect x="{x}" y="{y}" width="104" height="35" fill="{c}"/>')
            s.append(f'<text x="{x}" y="{y+51}" font-size="12">{j+1}  {c}</text>')
            s.append(f'<text x="{x}" y="{y+68}" font-size="10.5">L* {v["L_star"][j]:.1f} · CR {v["contrast_to_background"][j]:.2f}</text>')
    s.extend(['<text x="24" y="530" font-size="12">CR: luminance contrast to the specified background. Use dark labels outside pale fills.</text>',
              '<text x="24" y="551" font-size="12">Colour alone may merge categories. Add labels, shapes or panels when the task requires it.</text>',
              '</g></svg>'])
    return '\n'.join(s)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    g=p.add_mutually_exclusive_group(required=True)
    g.add_argument('--palette');g.add_argument('--colors',nargs='+')
    p.add_argument('--background',default='#FFFFFF');p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();db=json.loads((Path(__file__).resolve().parents[1]/'assets/palettes.json').read_text())
    if a.palette:
        if a.palette not in db['palettes']:p.error('Unknown palette; choose: '+', '.join(db['palettes']))
        colors=db['palettes'][a.palette]['colors'];title=a.palette
    else:colors=a.colors;title='custom palette'
    if len(colors)<2:p.error('At least two colours are needed for pairwise diagnostics.')
    try:
        for c in colors+[a.background]:rgb(c)
    except ValueError as e:p.error(str(e))
    result=audit(colors,a.background);result['name']=title
    a.out.mkdir(parents=True,exist_ok=True)
    (a.out/'palette_diagnostic.json').write_text(json.dumps(result,ensure_ascii=False,indent=2))
    (a.out/'palette_diagnostic.svg').write_text(svg_report(result,title))
    print(json.dumps({'palette':title,'outputs':[str(a.out/'palette_diagnostic.svg'),str(a.out/'palette_diagnostic.json')],'nearest_original':result['cases']['original']['nearest_pairs'][0]}))

if __name__=='__main__':main()
