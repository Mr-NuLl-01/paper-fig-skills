"""Synthetic examples applying this repository's sci-figure skills only.
Run from any directory: python examples/gallery/generate.py
All values and structures are demonstrations, not experimental evidence.
"""
from pathlib import Path
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, TwoSlopeNorm, LinearSegmentedColormap
from matplotlib.patches import Rectangle, Circle, FancyArrowPatch, Polygon
from matplotlib.cm import ScalarMappable
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
O=Path(__file__).resolve().parent/'output'; O.mkdir(exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.titlesize':11,'axes.labelsize':9,'axes.spines.top':False,'axes.spines.right':False,'svg.fonttype':'none','pdf.fonttype':42,'savefig.facecolor':'white','axes.labelcolor':'#273643','text.color':'#273643','axes.edgecolor':'#80909a'})
FRESH=LinearSegmentedColormap.from_list('muted_teal_coral',['#3e8093','#e6e2df','#c75d40'])
C=['#2D7192','#853E59','#85884A','#BD7658','#626698']; rng=np.random.default_rng(20261018)
def save(fig,name,caption,data=None):
 fig.text(.02,.015,'SYNTHETIC DEMO  |  '+caption,fontsize=7,color='#52616b')
 for ext in ['png','svg','pdf']: fig.savefig(O/f'{name}.{ext}',dpi=180)
 plt.close(fig)
 if data is not None: (O/f'{name}.json').write_text(json.dumps(data,indent=2))
def tag(ax,s):
 (ax.text2D if hasattr(ax,'text2D') else ax.text)(-.12,1.05,s,transform=ax.transAxes,weight='bold',fontsize=12)
def arr(ax,a,b,c='#52616b',style='-|>',**kw): ax.add_patch(FancyArrowPatch(a,b,arrowstyle=style,mutation_scale=12,color=c,lw=1.4,zorder=5,**kw))
# 01. Raincloud: enough explicitly synthetic samples to illustrate a KDE.
f,axs=plt.subplots(1,2,figsize=(7.6,4.2)); f.subplots_adjust(left=.1,right=.98,bottom=.23,top=.82,wspace=.4)
f.suptitle('01  Paired samples and batch distributions',x=.05,ha='left',weight='bold')
nper=30; before=rng.normal(12,1.6,3*nper); batch=np.repeat(np.arange(3),nper); after=before+np.repeat([.6,1.5,2.2],nper)+rng.normal(0,.8,3*nper)
for i in range(3*nper): axs[0].plot([0,1],[before[i],after[i]],color=C[batch[i]],alpha=.32,lw=.6,marker='o',ms=2)
axs[0].set(xticks=[0,1],xticklabels=['Before','After'],ylabel='Hypothetical efficiency (%)'); tag(axs[0],'a')
for b in range(3):
 v=(after-before)[batch==b]
 parts=axs[1].violinplot([v],positions=[b+.18],widths=.54,showextrema=False,bw_method=.5)
 for body in parts['bodies']:
  vertices=body.get_paths()[0].vertices;vertices[:,0]=np.maximum(vertices[:,0],b+.18);body.set_facecolor(C[b]);body.set_edgecolor(C[b]);body.set_alpha(.2)
 bp=axs[1].boxplot([v],positions=[b-.10],widths=.24,patch_artist=True,showfliers=False,whis=1.5,manage_ticks=False)
 for patch in bp['boxes']:patch.set(facecolor=C[b],alpha=.35,edgecolor=C[b])
 for key in ['whiskers','caps','medians']:
  for line in bp[key]:line.set(color=C[b],linewidth=1.1)
 axs[1].scatter(b+.22+rng.uniform(.02,.18,nper),v,c=C[b],s=8,alpha=.65,zorder=3)
axs[1].axhline(0,color='#87939b',ls='--',lw=.8); axs[1].set(xlim=(-.5,2.85),xticks=range(3),xticklabels=['Batch A','Batch B','Batch C'],ylabel='Paired change (percentage points)');tag(axs[1],'b')
save(f,'01_paired','90 synthetic pairs; box = median / IQR; whiskers = 1.5 IQR; dots = all values; KDE bw = 0.5.',{'before':before.tolist(),'after':after.tolist(),'batch':batch.tolist(),'kde_bandwidth':.5,'whisker_rule':'1.5 IQR; all individual values retained'})
# 02. Editable structure with contact topology; display thickness is deliberately exaggerated.
f,ax=plt.subplots(figsize=(7.1,4.1));f.subplots_adjust(left=.03,right=.98,bottom=.14,top=.86);ax.set(xlim=(0,10),ylim=(0,7));ax.axis('off');f.suptitle('02  A device is a stack of contacts',x=.05,ha='left',weight='bold')
layers=[('Glass','#d5e4e9'),('Transparent anode','#8fb3c3'),('Hole transport layer','#b58ca4'),('Emissive layer','#58a897'),('Electron transport layer','#7d91ba'),('Metal cathode','#56677e')]
for i,(label,col) in enumerate(layers):
 y=.8+i*.72
 ax.add_patch(Rectangle((1,y),4,.65,facecolor=col,edgecolor='white',lw=1.5)); ax.plot([5,6],[y+.32]*2,color='#75838e',lw=.8);ax.text(6.12,y+.32,label,va='center')
arr(ax,(2.3,4.9),(2.3,3.5),'#102b3d');ax.text(2.5,4.55,'e−')
arr(ax,(3.7,2.2),(3.7,3.1),'#63351b');ax.text(3.88,2.45,'h+')
ax.text(2.55,3.28,'recombination',color='white',ha='center',fontsize=8)
arr(ax,(3,.8),(3,.05),C[2]);ax.text(3.25,.15,'light output',va='bottom',color=C[2]);ax.text(1,5.6,'Conceptual bottom-emitting LED',fontsize=10)
save(f,'02_device','Conceptual layers; not to scale; no material identities or measured thicknesses implied.')
# 03. Separate electron-energy diagram from spatial construction.
f,ax=plt.subplots(figsize=(7.1,4.1));f.subplots_adjust(left=.14,right=.96,bottom=.23,top=.83);f.suptitle('03  Energy alignment and competing routes',x=.05,ha='left',weight='bold')
levels=[(-2.3,-5.2),(-3.2,-5.7),(-3.1,-6.3)]
for i,(hi,lo) in enumerate(levels):
 col=['#b58ca4','#58a897','#7d91ba'][i]; ax.fill_between([i-.32,i+.32],lo,hi,color=col,alpha=.07)
 for y in [hi,lo]: ax.plot([i-.32,i+.32],[y,y],color=col,lw=3);ax.text(i+.36,y+.07,f'{y:.1f}',va='bottom',fontsize=8,zorder=8)
arr(ax,(2,-3.1),(1.1,-3.2),C[0]);arr(ax,(.05,-5.2),(.9,-5.7),C[1]);arr(ax,(1,-3.2),(1,-5.7),C[2]);ax.text(.95,-4.4,'radiative',fontsize=8,ha='right',bbox=dict(facecolor='white',edgecolor='none',alpha=.85,pad=2))
arr(ax,(1.2,-3.25),(1.2,-5.65),'#87939b',connectionstyle='arc3,rad=-.55');ax.text(1.56,-4.5,'non-radiative',fontsize=8,bbox=dict(facecolor='white',edgecolor='none',alpha=.85,pad=2))
ax.text(1.65,-2.75,'e− injection',fontsize=8,color=C[0]);ax.text(.1,-6.1,'h+ injection',fontsize=8,color=C[1]); ax.set(xlim=(-.55,2.7),ylim=(-6.7,-1.8),xticks=[0,1,2],xticklabels=['HTL','Emitter','ETL'],ylabel='Electron energy relative to vacuum (eV)');ax.grid(axis='y',alpha=.13)
save(f,'03_energy','Invented energy levels; arrows denote conceptual processes, not measured rates.',{'levels_eV':levels,'reference':'vacuum'})
# 04. Explicit conceptual Voronoi domains, material reservoir and growth bookkeeping.
f=plt.figure(figsize=(8.2,5.6));f.suptitle('04  From nuclei toward a connected film',x=.05,ha='left',weight='bold')
gs=f.add_gridspec(2,3,left=.06,right=.96,bottom=.17,top=.82,height_ratios=[1.25,.65],wspace=.25,hspace=.6)
seeds=np.array([[.13,.18],[.35,.15],[.67,.13],[.87,.29],[.17,.52],[.45,.43],[.68,.55],[.88,.78],[.42,.8],[.15,.85],[.64,.88]])
def clip(poly,n,c):
 ans=[]
 for a,b in zip(poly,np.roll(poly,-1,axis=0)):
  va=np.dot(a,n)-c;vb=np.dot(b,n)-c
  if va<=0:ans.append(a)
  if (va<=0)!=(vb<=0):ans.append(a+(b-a)*va/(va-vb))
 return np.array(ans)
cells=[]
for i,q in enumerate(seeds):
 poly=np.array([[0.,0.],[1.,0.],[1.,1.],[0.,1.]])
 for j,r in enumerate(seeds):
  if i!=j:poly=clip(poly,r-q,(np.dot(r,r)-np.dot(q,q))/2)
 cells.append(poly)
for k,g in enumerate([.12,.60,.97]):
 ax=f.add_subplot(gs[0,k]);ax.set(aspect='equal',xlim=(0,1),ylim=(0,1));ax.set_xticks([]);ax.set_yticks([]);ax.set_facecolor('#edf3f1')
 for i,(q,poly) in enumerate(zip(seeds,cells)):
  grown=q+(poly-q)*g;ax.add_patch(Polygon(grown,closed=True,fc=C[i%5],ec='white',lw=.7,alpha=.85))
  if i in [4,5,6] and k>0:ax.text(*q,str(i+1),ha='center',va='center',color='white',fontsize=7)
 ax.set_title(['Nucleation','Lateral growth','Near coalescence'][k],fontsize=10)
 ax.text(.5,-.16,['Small solid domains','Solute feeds domain edges','Grain boundaries remain'][k],transform=ax.transAxes,ha='center',fontsize=8)
ax=f.add_subplot(gs[1,:2]);u=np.linspace(0,1,101);solid=u**2;ax.plot(u,solid,color='#2D7192',label='Solid');ax.plot(u,1-solid,color='#853E59',ls='--',label='Reservoir');ax.set(xlabel='Construction parameter (not time)',ylabel='Area fraction');ax.legend(frameon=False,fontsize=8,ncol=2);ax.set(ylim=(0,1.05))
ax=f.add_subplot(gs[1,2]);ax.axis('off');ax.text(0,.95,'A geometrical illustration\nFixed seeds and field of view\nCells grow without overlap\nSolid + reservoir = 1\nNot a kinetic growth law',va='top',fontsize=8,linespacing=1.65)
save(f,'04_growth','Conceptual Voronoi construction; not microscopy or a measured growth pathway.',{'seeds':seeds.tolist(),'cells':[c.tolist() for c in cells],'construction_factors':[.12,.6,.97],'fraction_rule':'g squared for homothetic cells; reservoir is one minus solid; no physical time model'})
# Spectrum field reused, physical third coordinate has irregular actual spacing.
w=np.linspace(450,700,151); T=np.array([280,295,320,355,400]); W,TT=np.meshgrid(w,T)
S=(1-.001*(TT-280))*np.exp(-.5*((W-(520+.16*(TT-280)))/(12+.025*(TT-280)))**2)+.12*np.exp(-.5*((W-605)/18)**2)
# 05. Multi-heatmap comparison with meaningful zero residual and explicit missing data.
t=np.linspace(0,60,81); WW,tg=np.meshgrid(w,t); A=np.exp(-.5*((WW-(520+.5*tg))/15)**2)*np.exp(-tg/100); B=np.exp(-.5*((WW-(520+.25*tg))/15)**2)*np.exp(-tg/150);mask=np.zeros_like(A,dtype=bool);# R3: no missing patch in this presentation example
f=plt.figure(figsize=(8.6,5.5)); gs=f.add_gridspec(2,3,left=.1,right=.95,bottom=.16,top=.86,hspace=.55,wspace=.85); f.suptitle('05  Spectral maps and difference signals',x=.05,ha='left',weight='bold')
cm=plt.colormaps['Blues'].copy();cm.set_bad('#d8dce0'); dm=plt.colormaps['RdBu_r'].copy();dm.set_bad('#d8dce0')
for i,Z in enumerate([A,B,B-A]):
 ax=f.add_subplot(gs[0,i]);tag(ax,chr(97+i));im=ax.pcolormesh(w,t,np.ma.array(Z,mask=mask),shading='auto',rasterized=True,cmap=cm if i<2 else dm,norm=Normalize(0,1) if i<2 else TwoSlopeNorm(0,vmin=-.5,vmax=.5));ax.set(xlabel='Wavelength (nm)',ylabel='Time (s)',title=['Condition A','Condition B','B − A'][i]);f.colorbar(im,ax=ax,fraction=.06,pad=.04,label='a.u.')
ax=f.add_subplot(gs[1,:2]);tag(ax,'d')
for i,(Z,c) in enumerate([(A,C[0]),(B,C[1])]):ax.plot(t,Z[:,np.argmin(abs(w-540))],color=c,label=f'Condition {"AB"[i]}')
ax.legend(frameon=False,fontsize=8);ax.set(xlabel='Time (s)',ylabel='Signal at 540 nm (a.u.)');ax=f.add_subplot(gs[1,2]);ax.axis('off');ax.text(0,.8,'Shared intensity range\nA and B: 0–1\n\nResidual centered at zero',fontsize=8,va='top')
save(f,'05_heatmaps','Analytic synthetic fields; all values shown; residual scale differs from signal scale.',{'wavelength_nm':w.tolist(),'time_s':t.tolist(),'A':A.tolist(),'B':B.tolist(),'mask':mask.tolist()})
# 06. Stacked heatmap planes: vertical axis = measurement time, color = field.
x=np.linspace(-2,2,31);y=np.linspace(-2,2,31);X,Y=np.meshgrid(x,y);times=[0,2,7];F=[np.exp(-((X-.1*z)**2+(Y+.04*z)**2)/(.5+.1*z))-np.exp(-((X+.65)**2+(Y-.6)**2)/.7) for z in times]
f=plt.figure(figsize=(7.1,5.2));f.suptitle('06  Time-indexed planes with a shared signal scale',x=.05,ha='left',weight='bold');ax=f.add_axes([.01,.21,.62,.64],projection='3d');norm=TwoSlopeNorm(0,vmin=-1,vmax=1)
for z,Z in zip(times,F):ax.plot_surface(X,Y,np.full_like(X,z),facecolors=plt.colormaps['RdBu_r'](norm(Z)),shade=False,rstride=1,cstride=1,alpha=1,linewidth=0,antialiased=False)
ax.set(xlabel='x (mm)',ylabel='y (mm)',zlabel='Time (s)',zticks=times);ax.view_init(24,-59);ax.set_box_aspect((1,1,1.2))
for i,Z in enumerate(F):
 a=f.add_axes([.71,.65-i*.22,.2,.15]);a.imshow(Z,origin='lower',extent=[-2,2,-2,2],cmap='RdBu_r',vmin=-1,vmax=1);a.set_title(f't = {times[i]} s',fontsize=8,pad=2);a.set_xticks([-2,0,2] if i==2 else []);a.set_yticks([-2,0,2]);a.tick_params(labelsize=7)
cax=f.add_axes([.18,.115,.4,.025]);f.colorbar(ScalarMappable(norm=norm,cmap='RdBu_r'),cax=cax,orientation='horizontal',label='Synthetic signed change (a.u.)')
save(f,'06_heatmap_stack','Synthetic signed differences; white = zero; time is not spatial depth.',{'x_mm':x.tolist(),'y_mm':y.tolist(),'time_s':times,'fields':[a.tolist() for a in F]})
# 07. Waterfall with actual T positions; no vertical offset or independent normalization.
f=plt.figure(figsize=(7.1,4.7));f.suptitle('07  Spectral evolution in three coordinates',x=.05,ha='left',weight='bold');ax=f.add_axes([.01,.2,.59,.65],projection='3d');norm=Normalize(T.min(),T.max())
for temp,s in zip(T,S):ax.plot(w,np.full_like(w,temp),s,c=plt.colormaps['YlOrBr'](.4+.55*norm(temp)),lw=1.6)
ax.set(xlabel='Wavelength (nm)',ylabel='Temperature (K)',zlabel='Intensity (a.u.)',yticks=T);ax.view_init(27,-65);ax.set_box_aspect((1.6,1,.8))
a=f.add_axes([.71,.28,.24,.48]);im=a.pcolormesh(w,T,S,shading='nearest',rasterized=True,cmap='YlOrBr',vmin=0,vmax=1);a.set(xlabel='Wavelength (nm)',ylabel='Temperature (K)',title='Same data, 2D',ylim=(280,400));f.colorbar(im,ax=a,fraction=.09,pad=.06)
save(f,'07_waterfall','Uneven temperature spacing retained; absolute synthetic intensity; no display offset.',{'wavelength_nm':w.tolist(),'temperature_K':T.tolist(),'intensity':S.tolist()})
# 08. Non-uniform evidence layout + genuine 3D volume orthogonal slices.
a=np.linspace(-1,1,31);XX,YY,ZZ=np.meshgrid(a,a,a,indexing='ij');vol=np.exp(-((XX-.35)**2/.18+(YY+.2)**2/.5+ZZ**2/.3))-np.exp(-((XX+.35)**2/.18+(YY+.2)**2/.5+ZZ**2/.3));mid=15
f=plt.figure(figsize=(7.1,5.5));f.suptitle('08  Three spatial axes, several ways to read them',x=.05,ha='left',weight='bold');gs=f.add_gridspec(3,4,left=.12,right=.95,bottom=.16,top=.85,wspace=.7,hspace=.75)
ax=f.add_subplot(gs[:2,:2],projection='3d');tag(ax,'a');norm=TwoSlopeNorm(0,vmin=-1,vmax=1)
# x-z plane at y=0; then x-y plane at z=0, both with explicit shared coordinates.
# One shared polygon collection: split both orthogonal planes into tiles at the intersection.
# Separate plot_surface collections sort whole planes, which causes incorrect interpenetration.
faces=[]; facecolors=[]
for plane,values in [('xz',vol[:,mid,:]),('xy',vol[:,:,mid])]:
 for i in range(len(a)-1):
  for j in range(len(a)-1):
   coords=[(a[i],a[j]),(a[i+1],a[j]),(a[i+1],a[j+1]),(a[i],a[j+1])]
   faces.append([(x,0,z) for x,z in coords] if plane=='xz' else [(x,y,0) for x,y in coords])
   facecolors.append(FRESH(norm(values[i:i+2,j:j+2].mean())))
mesh=Poly3DCollection(faces,facecolors=facecolors,edgecolors='none',linewidths=0,zsort='average',antialiased=False)
ax.add_collection3d(mesh);ax.set(xlim=(-1,1),ylim=(-1,1),zlim=(-1,1));ax.view_init(24,-52);ax.set(xlabel='x (µm)',ylabel='y (µm)',zlabel='z (µm)',title='Orthogonal slice locations')
for spec,dat,title in [(gs[0,2:],vol[:,:,mid].T,'x–y at z = 0 µm'),(gs[1,2:],vol[:,mid,:].T,'x–z at y = 0 µm')]:
 ax=f.add_subplot(spec);im=ax.imshow(dat,origin='lower',extent=[-1,1,-1,1],cmap=FRESH,vmin=-1,vmax=1,aspect='equal');ax.set_title(title,fontsize=9);ax.set_xlabel('x (µm)');ax.set_ylabel('y (µm)' if 'x–y' in title else 'z (µm)');f.colorbar(im,ax=ax,fraction=.04,pad=.02)
ax=f.add_subplot(gs[2,:3]);ax.plot(a,vol[:,mid,mid],color=C[0]);ax.set(xlabel='x (µm)',ylabel='Δ field (a.u.)',title='Centerline at y = z = 0');ax=f.add_subplot(gs[2,3]);ax.axis('off');ax.text(0,.9,'Analytic difference\n31³ voxels\nNo segmentation\nNo microscopy',fontsize=8,va='top')
save(f,'08_volume_layout','Synthetic difference field; teal < 0, neutral = 0, coral > 0; common −1 to +1 scale.',{'axes_um':a.tolist(),'volume':vol.tolist(),'axis_order':'x,y,z','slice_index':mid,'quantity':'signed difference of two analytic Gaussians','colormap':['#3e8093','#e6e2df','#c75d40'],'range':[-1,1],'center':0})
print(O)
