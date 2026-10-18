"""Native 3D conceptual growth views + one editable 2D diagram and area ledger."""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
p=Path(__file__).resolve().parent/'output';d=json.loads((p/'04_growth.json').read_text());plt.rcParams.update({'font.family':'DejaVu Sans','svg.fonttype':'none','pdf.fonttype':42,'font.size':9,'axes.spines.top':False,'axes.spines.right':False})
f=plt.figure(figsize=(8.6,5.8));f.text(.035,.95,'04  A faceted growth construction, in 3D and plan view',fontsize=13,weight='bold',color='#273643')
for i,name in enumerate(['Nuclei','Growing domains','Near coalescence']):
 ax=f.add_axes([.02+i*.326,.48,.32,.39]);ax.imshow(plt.imread(p/'growth3d'/f'state{i+1}.png'));ax.axis('off');ax.set_title(name,fontsize=10)
colors=['#8cbcb5','#9caccb','#cfb28e','#93b2c1','#b9a5bd'];ax=f.add_axes([.075,.12,.25,.30]);ax.set(aspect='equal',xlim=(0,1),ylim=(0,1));ax.set_xticks([]);ax.set_yticks([])
for i,(q,cell) in enumerate(zip(d['seeds'],d['cells'])):
 q=np.array(q);poly=q+.97*(np.array(cell)-q);ax.add_patch(Polygon(poly,closed=True,fc=colors[i%5],ec='white',lw=.6))
 if i in [4,5,6]:ax.text(*q,str(i+1),ha='center',va='center',fontsize=8,color='#273643')
ax.set_title('Same final domains, top view',fontsize=9)
ax=f.add_axes([.49,.17,.44,.22]);g=np.linspace(0,1,101);ax.plot(g,g*g,color='#3b7f8a',label='Solid area');ax.plot(g,1-g*g,color='#9c708f',ls='--',label='Remaining area');ax.set(xlim=(0,1),ylim=(0,1.05),xlabel='Construction parameter (not time)',ylabel='Area fraction');ax.legend(frameon=False,fontsize=8)
f.text(.49,.43,'Fixed seed IDs and Voronoi footprints\nFaceted roofs are conceptual, not crystallographic data.',fontsize=8,color='#52616b')
f.text(.035,.035,'SYNTHETIC DEMO  |  Geometry construction, not a growth law; native Blender + editable 2D source supplied.',fontsize=7.5,color='#52616b')
for ext in ['png','svg','pdf']:f.savefig(p/f'04_growth.{ext}',dpi=180,facecolor='white')
