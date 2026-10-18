#!/usr/bin/env python3
"""Build an original colour reference sheet from the bundled candidate palettes."""
from pathlib import Path
import html
import json
import base64
import matplotlib
from matplotlib.colors import to_hex

ROOT=Path(__file__).resolve().parents[1]
OUT=Path(__file__).resolve().parent
DB=json.loads((ROOT/'skills/sci-figure-color/assets/palettes.json').read_text())
W,H=1120,1430
parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="210mm" height="{210*H/W:.3f}mm" viewBox="0 0 {W} {H}">',
 '<metadata>'+html.escape(json.dumps({'title':'Scientific colour atlas','provenance':DB['provenance'],'matplotlib_version':matplotlib.__version__,'purpose':'Design reference, not scientific data'},ensure_ascii=False))+'</metadata>',
 '<rect width="1120" height="1430" fill="#F6F7F8"/>',
 '<g font-family="DejaVu Sans, Arial, sans-serif" fill="#253847">']
def text(x,y,t,size=15,fill=None,weight=None):
 attrs=f' fill="{fill}"' if fill else ''
 if weight:attrs+=f' font-weight="{weight}"'
 parts.append(f'<text x="{x}" y="{y}" font-size="{size}"{attrs}>{html.escape(str(t))}</text>')
def rect(x,y,w,h,c,stroke=None):
 parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}"'+(f' stroke="{stroke}"' if stroke else '')+'/>')

text(45,53,'SCIENTIFIC FIGURE ATLAS / 2026',13,'#A05C3C',600)
text(45,102,'Colour follows meaning',39,weight=600)
text(45,134,'12 original categorical combinations + 14 established continuous-map candidates',16)
text(45,160,'Choose for the variable, then inspect the actual figure at its final size.',15,'#586B76')
text(45,202,'01   Categories and material identities',21,weight=600)
text(45,226,'Equal status: hue separates identities. These swatches do not encode a numeric scale.',14,'#586B76')
for k,(name,p) in enumerate(DB['palettes'].items()):
 col,row=k%3,k//3;x=45+col*351;y=248+row*139
 rect(x,y,329,124,'#FFFFFF')
 text(x+13,y+26,f'{k+1:02d}  {name}',16,weight=600)
 for j,c in enumerate(p['colors']):
  sx=x+13+j*61
  rect(sx,y+41,57,37,c)
  text(sx,y+99,c,10.7,'#425460')

text(45,851,'02   Numeric fields and ordered values',21,weight=600)
text(45,875,'Use the colour bar and units. Define zero, endpoints, clipping and missing values.',14,'#586B76')
types=[('sequential','Sequential','Low → high',45),('diverging','Diverging','Negative → zero → positive',396),('cyclic','Cyclic','The endpoints meet',747)]
for key,label,desc,x in types:
 text(x,912,label,19,weight=600);text(x,934,desc,12.5,'#586B76')
 for i,name in enumerate(DB['continuous_candidates'][key]):
  y=958+i*37
  text(x,y,name,12.5)
  cm=matplotlib.colormaps[name]
  n=256
  gid='map-'+name.replace('_','-')
  stops=''.join(f'<stop offset="{100*j/(n-1):.5f}%" stop-color="{to_hex(cm(j/(n-1)))}"/>' for j in range(n))
  parts.append(f'<defs><linearGradient id="{gid}" x1="0%" y1="0%" x2="100%" y2="0%">{stops}</linearGradient></defs>')
  rect(x+115,y-12,208,13,f'url(#{gid})')
 if key=='diverging':
  text(x,1138,'Centre on a meaningful reference.',12.5,'#586B76')
  text(x,1159,'Use balanced limits when comparison',12.5,'#586B76')
  text(x,1180,'requires symmetric magnitude.',12.5,'#586B76')
 if key=='cyclic':
  text(x,1064,'For wrapped angle or phase.',12.5,'#586B76')
  text(x,1085,'State the angular period explicitly.',12.5,'#586B76')
  text(x,1127,'Missing ≠ zero',16,weight=600)
  rect(x,1144,36,23,'#CED3D8')
  text(x+48,1161,'Give missing data its own key.',12.5,'#586B76')
rect(45,1288,1030,1,'#CDD6DD')
text(45,1320,'No universal pass label',18,weight=600)
text(45,1346,'The 12 combinations are original design candidates, not colours extracted from the 89 papers.',13.5,'#586B76')
text(45,1369,'Some merge in grayscale or CVD simulations. Use labels, markers or panels when identity must survive.',13.5,'#586B76')
text(45,1392,'Continuous maps: Matplotlib. CVD diagnostics: Machado 2009 severity 1 in linear RGB; finite scope.',12.5,'#586B76')
parts.append('</g></svg>')
(OUT/'color-atlas.svg').write_text('\n'.join(parts))
(OUT/'color-atlas.json').write_text(json.dumps(DB,ensure_ascii=False,indent=2)+'\n')

cards=[]
for name,p in DB['palettes'].items():
 d=json.loads((OUT/'color-diagnostics'/f'{name}.json').read_text())
 rows=''.join('<tr><td>'+html.escape(k)+'</td><td>'+str(v['nearest_pairs'][0]['pair'])+'</td><td>'+str(v['nearest_pairs'][0]['delta_e76'])+'</td><td>'+str(v['clipped_components'])+'</td></tr>' for k,v in d['cases'].items())
 sv=(OUT/'color-diagnostics'/f'{name}.svg').read_text()
 cards.append(f'<details><summary>{html.escape(p["label"])} · {name}</summary><p>{html.escape(p["use"])}（仅为适配示例，不限定学科）。色卡不是通用色觉通过证书。</p>{sv}<table><thead><tr><th>场景</th><th>最近色对（从1计）</th><th>ΔE76</th><th>截断分量</th></tr></thead><tbody>{rows}</tbody></table></details>')
doc='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>科学绘图配色图谱</title><style>body{font:16px/1.7 system-ui,sans-serif;color:#253847;background:#f6f7f8;margin:auto;max-width:1160px;padding:24px}h1{font-size:34px}details{background:white;margin:18px 0;padding:20px;border:1px solid #d9e0e6;border-radius:8px}summary{font-size:20px;cursor:pointer}svg{width:100%;height:auto}table{border-collapse:collapse;width:100%}td,th{text-align:left;padding:8px;border-bottom:1px solid #d9e0e6}.note{border-left:4px solid #a05c3c;padding:12px 18px;background:white}</style><h1>科学绘图配色图谱</h1><p>12组原创离散配色与14种现有连续色图候选。原创配色不是从89篇论文像素中反推的HEX。</p><div class="note">先确定颜色表达的是类别、数值、偏差还是周期量，再选择色图。以下诊断仅对指定色块与白背景运行；灰度相近的类别应增加形状、文字或分面。ΔE76不是通用可辨阈值，不能据此为整幅图颁发可访问性证书。</div>'''+(OUT/'color-atlas.svg').read_text()+''.join(cards)+'''<h2>诊断方法与边界</h2><p>使用sRGB D65转线性RGB和CIELAB；距离为CIE76，非CIEDE2000。Machado等2009年的严重度1矩阵在线性RGB中作用，超出色域的分量截断，再编码回sRGB；计入截断分量数。灰度使用线性相对亮度。工具也报告背景亮度对比，但不把文本可读标准当作所有科学图元的统一阈值。</p><p>该模型覆盖三种有限模拟情形，不能模拟所有观察者、显示器、打印、细线、拥挤或低视力条件。实际成图仍应检查直接标注、标记与面板身份。</p><p>方法来源：<a href="https://doi.org/10.1109/TVCG.2009.113">Machado et al., 2009</a>；色图来源：<a href="https://matplotlib.org/stable/users/explain/colors/colormaps.html">Matplotlib官方文档</a>。记录日期：2026-10-17。</p></html>'''
font_dir=ROOT/'tools/font-assets'
font_path=font_dir/'color-cjk-subset.woff'
if font_path.exists():
 data=base64.b64encode(font_path.read_bytes()).decode('ascii')
 font_css='@font-face{font-family:"Figure Atlas CJK";src:url(data:font/woff;base64,'+data+') format("woff");font-weight:400;font-style:normal}body{font-family:"Figure Atlas CJK",system-ui,sans-serif}'
 doc=doc.replace('</style>','</style><style>'+font_css+'</style>',1)
 if (font_dir/'OFL.txt').exists():
  doc=doc.replace('</html>','<template id="font-license"><pre>'+html.escape((font_dir/'OFL.txt').read_text())+'</pre></template></html>')
(OUT/'color-atlas.html').write_text(doc)
print(json.dumps({'palettes':len(DB['palettes']),'continuous_maps':sum(map(len,DB['continuous_candidates'].values())),'matplotlib_version':matplotlib.__version__,'outputs':['color-atlas.svg','color-atlas.json','color-atlas.html']}))
