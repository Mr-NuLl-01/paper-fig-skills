#!/usr/bin/env python3
"""Typeset the authored Chinese handbook; source is scientific-figure-handbook.md."""
from pathlib import Path
import html
import json
import re
import argparse
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle, KeepTogether

OUT=Path(__file__).resolve().parent
ROOT=OUT.parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--font-regular', type=Path, required=True, help='A locally available, appropriately licensed CJK TTF')
parser.add_argument('--font-bold', type=Path, help='Optional matching bold TTF; regular is used otherwise')
args = parser.parse_args()
FONT = args.font_regular.resolve()
BOLD = (args.font_bold or args.font_regular).resolve()
if not FONT.is_file() or not BOLD.is_file():
    parser.error('The supplied font paths must exist.')
pdfmetrics.registerFont(TTFont('NotoSC',str(FONT)))
pdfmetrics.registerFont(TTFont('NotoSC-Semibold',str(BOLD)))
pdfmetrics.registerFontFamily('NotoSC',normal='NotoSC',bold='NotoSC-Semibold',italic='NotoSC',boldItalic='NotoSC-Semibold')
INK=colors.HexColor('#253847');MUTED=colors.HexColor('#566B79');ACCENT=colors.HexColor('#A85F3C')
PAGE_W,PAGE_H=A4
LEFT=43; RIGHT=43; CONTENT_W=PAGE_W-LEFT-RIGHT
styles={
 'body':ParagraphStyle('body',fontName='NotoSC',fontSize=10.3,leading=16.8,spaceAfter=9,textColor=INK,wordWrap='CJK',allowWidows=0,allowOrphans=0),
 'h2':ParagraphStyle('h2',fontName='NotoSC-Semibold',fontSize=18,leading=25,spaceBefore=6,spaceAfter=15,textColor=INK,wordWrap='CJK',keepWithNext=True),
 'h3':ParagraphStyle('h3',fontName='NotoSC-Semibold',fontSize=13.3,leading=19.5,spaceBefore=13,spaceAfter=8,textColor=INK,wordWrap='CJK',keepWithNext=True),
 'small':ParagraphStyle('small',fontName='NotoSC',fontSize=8.5,leading=13,spaceAfter=7,textColor=MUTED,wordWrap='CJK'),
 'cell':ParagraphStyle('cell',fontName='NotoSC',fontSize=8.8,leading=13.3,textColor=INK,wordWrap='CJK'),
 'thead':ParagraphStyle('thead',fontName='NotoSC-Semibold',fontSize=9.1,leading=13.5,textColor=INK,wordWrap='CJK'),
 'ref':ParagraphStyle('ref',fontName='NotoSC',fontSize=8.7,leading=13.5,spaceAfter=4,textColor=INK,wordWrap='CJK'),
 'cover_title':ParagraphStyle('cover_title',fontName='NotoSC-Semibold',fontSize=31,leading=42,spaceAfter=18,textColor=INK,wordWrap='CJK'),
 'cover_sub':ParagraphStyle('cover_sub',fontName='NotoSC',fontSize=13.3,leading=21,spaceAfter=16,textColor=MUTED,wordWrap='CJK'),
 'kicker':ParagraphStyle('kicker',fontName='NotoSC',fontSize=10,leading=15,spaceAfter=16,textColor=ACCENT),
}

def markup(s):
 s=html.escape(s)
 s=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',s)
 s=re.sub(r'`([^`]+)`',r'\1',s)
 s=re.sub(r'https://[^\s<>]+',lambda m:f'<link href="{m.group(0)}" color="#356784">{m.group(0)}</link>',s)
 return s
def p(s,style='body'):return Paragraph(markup(s),styles[style])
def pic(path,width=CONTENT_W):
 from PIL import Image as PILImage
 w,h=PILImage.open(path).size
 return Image(str(path),width=width,height=width*h/w)

outline=[]
class HandbookDoc(SimpleDocTemplate):
 def afterFlowable(self,f):
  if isinstance(f,Paragraph) and f.style.name=='h2':
   label=f.getPlainText();key='section-'+str(len(outline))
   self.canv.bookmarkPage(key);self.canv.addOutlineEntry(label,key,0,False)
   outline.append({'title':label,'page':self.page})

def footer(c,doc):
 c.saveState()
 c.setStrokeColor(colors.HexColor('#D8E0E5'));c.setLineWidth(.5)
 c.line(LEFT,39,PAGE_W-RIGHT,39)
 c.setFont('NotoSC',8);c.setFillColor(MUTED)
 c.drawString(LEFT,25,'科学绘图证据图谱 / 89篇 · 178图 · 9个模块')
 c.drawRightString(PAGE_W-RIGHT,25,str(doc.page))
 if doc.page>1:
  c.setFont('NotoSC',7.8)
  c.drawString(LEFT,PAGE_H-29,'SCIENTIFIC FIGURE ATLAS  ·  2026-10-17')
 c.restoreState()

story=[Spacer(1,10),p('RESEARCH × VISUAL LANGUAGE × EDITABLE SOURCES','kicker'),
 p('科学绘图<br/>证据图谱与新技能','cover_title'),
 p('从89篇论文、178张完整图出发<br/>为数据、机理、器件、生长、实验与影像选择合适的表达','cover_sub')]
# Explicit line breaks are only used in trusted cover strings.
story[2]=Paragraph('科学绘图<br/>证据图谱与新技能',styles['cover_title'])
story[3]=Paragraph('从89篇论文、178张完整图出发<br/>为数据、机理、器件、生长、实验与影像选择合适的表达',styles['cover_sub'])
stat=Table([[p('89篇 / 178图','h3'),p('9个模块','h3'),p('12组原创配色','h3')],[p('66篇主文通读；23篇定向精读','small'),p('按任务路由，保留不同语法','small'),p('附有限模拟，不作通用认证','small')]],colWidths=[CONTENT_W*.39,CONTENT_W*.29,CONTENT_W*.32])
stat.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,-1),colors.HexColor('#F0F3F5')),('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),('TOPPADDING',(0,0),(-1,0),0),('BOTTOMPADDING',(0,-1),(-1,-1),4)]))
story += [stat,Spacer(1,17),pic(OUT/'advanced-device-demo/advanced_device_preview.png'),Spacer(1,10),p('封面图为原创教学DEMO。任意尺寸与厚度夸张已注明；实际几何、材质、相机和标注源分别保留。','small'),p('版本1.0 · 2026-10-17\n内容与有范围验证已完成；技能目录安装及远程同步待授权。','small'),PageBreak()]

def plate_color():
 return [p('配色参考页：颜色先有含义，再有风格','h2'),p('本页为原创分类配色与现有连续色图候选。完整逐组诊断见color-atlas.html。','small'),pic(OUT/'color-atlas.png',width=CONTENT_W*.93),PageBreak()]
def plate_demos():
 return [p('实作示例一：配对关系与批次可见','h2'),p('独立前向试用，从空白制作。所有30个端点均为模拟数值，没有显示真实实验结果。','body'),pic(OUT/'forward-test-demo/demo_performance_bandwidth.png'),Spacer(1,16),p('结构仅占小块面积。三批各五个器件分别成面板，共用坐标；空心圆与实心菱形同时区分前后状态，配对箭头只连接同一器件。未知层厚不画标尺，未测动力学速率没有被转写成“转移更快”的机理。','body'),p('交付包含58个live text、34个命名组的SVG、CSV、参数和独立生成脚本。机械扫描与实际目视检查分别记录。','small'),PageBreak(),
 p('实作示例二：空间图案与埋藏界面','h2'),p('两套互指电极的归属在平面中展开，真实几何切口显示厚度方向上的三层边界。总图与近景使用同一模型。','body'),pic(OUT/'advanced-device-demo/advanced_device_preview.png'),Spacer(1,15),p('三维在这里帮助恢复接触图案和界面关系。图中没有虚构电场或输运路径。两套电极各自连续且相互分离；任意教学尺寸、材料身份和未定义的物理量均在参数中登记。','body'),p('Blender源已实际重新打开并渲染。SVG保留可编辑文字与引线；几何编辑应回到原生三维文件。','small'),PageBreak()]

source=(OUT/'scientific-figure-handbook.md').read_text().splitlines()
i=0;in_refs=False;first_body=True
while i<len(source):
 line=source[i].strip()
 if not line:i+=1;continue
 if line.startswith('# ') or line.startswith('## 从89'):
  i+=1;continue
 if line.startswith('## '):
  title=line[3:]
  if title.startswith('6. '):story+= [PageBreak()]+plate_color()
  elif title.startswith('10. '):story+=[PageBreak()]+plate_demos()
  elif not title.startswith('1. '):story.append(PageBreak())
  else:story.append(Spacer(1,10))
  story.append(p(title,'h2'));in_refs=title.startswith('附录');i+=1;continue
 if line.startswith('### '):story.append(p(line[4:],'h3'));i+=1;continue
 if line.startswith('|'):
  rows=[]
  while i<len(source) and source[i].strip().startswith('|'):
   row=[c.strip() for c in source[i].strip().strip('|').split('|')]
   if not all(re.fullmatch(r':?-+:?',c) for c in row):rows.append(row)
   i+=1
  n=len(rows[0]);ratios={2:[.32,.68],3:[.24,.39,.37]}.get(n,[1/n]*n)
  if rows[0][0]=='科学任务':ratios=[.31,.12,.57]
  if rows[0][0]=='名称':ratios=[.36,.64]
  data=[[p(c,'thead' if ri==0 else 'cell') for c in row] for ri,row in enumerate(rows)]
  tab=Table(data,colWidths=[CONTENT_W*r for r in ratios],repeatRows=1,hAlign='LEFT')
  tab.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#E5EDF1')),('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F6F8F9')]),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),.7,colors.HexColor('#BCCCD5')),('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
  story.extend([tab,Spacer(1,12)]);continue
 block=[line];i+=1
 while i<len(source) and source[i].strip() and not source[i].startswith(('#','|')):
  block.append(source[i].strip());i+=1
 txt=' '.join(block)
 if in_refs and re.match(r'^[ABCD]\d\d ·',txt):
  while i<len(source) and not source[i].strip():i+=1
  meta=[]
  while i<len(source) and source[i].strip():meta.append(source[i].strip());i+=1
  story.append(KeepTogether([p(txt,'ref'),p(' '.join(meta),'small'),Spacer(1,5)]))
 else:story.append(p(txt,'small' if txt.startswith('E0') else 'body'))

pdf=OUT/'scientific-figure-handbook.pdf'
doc=HandbookDoc(str(pdf),pagesize=A4,leftMargin=LEFT,rightMargin=RIGHT,topMargin=53,bottomMargin=54,title='科学绘图证据图谱与新技能手册',author='ChatGPT',subject='89篇论文与178张图的设计分析、九个绘图技能及原创示例')
doc.build(story,onFirstPage=footer,onLaterPages=footer)
(OUT/'handbook-outline.json').write_text(json.dumps(outline,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'file':str(pdf),'bytes':pdf.stat().st_size,'sections':len(outline)},ensure_ascii=False))
