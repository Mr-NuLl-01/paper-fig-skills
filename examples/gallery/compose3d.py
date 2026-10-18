"""Compose two synthetic Blender views with editable vector labels."""
from pathlib import Path
import json
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
p=Path(__file__).resolve().parent/'output';plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none','pdf.fonttype':42,'font.size':9})
f=plt.figure(figsize=(8.4,5.1));f.text(.035,.94,'02b  The same six layers, two spatial views',weight='bold',fontsize=14,color='#273643')
for i,v in enumerate(['assembled','exploded']):
 ax=f.add_axes([.02+i*.48,.23,.47,.65]);ax.imshow(plt.imread(p/'device3d'/f'{v}.png'));ax.axis('off');ax.set_title('Assembled contacts' if i==0 else 'Exploded for inspection',fontsize=11)
 if i==1:
  ax.set_xlim(0,1520)
  for j,entry in enumerate(json.loads((p/'device3d/label_points.json').read_text())):
   x,y=entry['pixel']; target=650-j*68
   ax.plot([x,1000,1050],[y,target,target],color='#52616b',lw=.65)
   ax.text(1070,target,entry['name'].replace('_',' '),va='center',fontsize=7.5,color='#273643')
names=['Glass','Anode','Hole transport','Emitter','Electron transport','Cathode'];colors=['#d5e4e9','#8fb3c3','#b58ca4','#58a897','#7d91ba','#56677e']
for i,(n,c) in enumerate(zip(names,colors)):
 x=.06+(i%3)*.31;y=.16-(i//3)*.055;f.patches.append(Rectangle((x,y),.018,.025,transform=f.transFigure,facecolor=c,edgecolor='#8a96a0',lw=.5));f.text(x+.025,y+.003,n,fontsize=9,color='#273643')
f.text(.035,.03,'SYNTHETIC DEMO  |  Display thicknesses exaggerated; exploded gaps are not physical voids.',fontsize=8,color='#52616b')
for ext in ['png','svg','pdf']:f.savefig(p/f'02b_device3d.{ext}',dpi=180,facecolor='white')
