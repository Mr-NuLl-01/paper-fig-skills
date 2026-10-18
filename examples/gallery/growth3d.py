"""Synthetic faceted grain construction, not atomistic crystallography or measured morphology.
blender -b -t 2 --python examples/gallery/growth3d.py -- --out DIR
Run generate.py first. Clears only this fresh background scene.
"""
import bpy,json,sys,argparse
from pathlib import Path
from mathutils import Vector
p=argparse.ArgumentParser();p.add_argument('--out',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);o=Path(a.out).resolve();o.mkdir(parents=True,exist_ok=True)
d=json.loads((Path(__file__).resolve().parent/'output/04_growth.json').read_text());cells=d['cells'];seeds=d['seeds']
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
s=bpy.context.scene;s.render.engine='CYCLES';s.cycles.samples=64;s.cycles.use_denoising=False;s.render.threads_mode='FIXED';s.render.threads=2;s.render.resolution_x=850;s.render.resolution_y=650;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.render.image_settings.color_mode='RGBA';s.render.film_transparent=True;s.world.color=(.7,.7,.7);s.view_settings.view_transform='Standard'
colors=['#8cbcb5','#9caccb','#cfb28e','#93b2c1','#b9a5bd']
def mat(name,h):
 m=bpy.data.materials.new(name);m.use_nodes=True;c=tuple(((int(h[i:i+2],16)/255+.055)/1.055)**2.4 for i in (1,3,5));m.diffuse_color=(*c,1);bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(*c,1);bs.inputs['Roughness'].default_value=.38;return m
mats=[mat(f'grain_identity_{i}',h) for i,h in enumerate(colors)];base=mat('substrate','#dfe8eb');cols={}
for k,g in enumerate(d['construction_factors']):
 c=bpy.data.collections.new(f'state_{k+1}');s.collection.children.link(c);cols[k]=c
 bpy.ops.mesh.primitive_cube_add(size=1,location=(0,0,-.04));ob=bpy.context.object;ob.name=f'substrate_{k+1}';ob.dimensions=(1.08,1.08,.07);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 for old in list(ob.users_collection):old.objects.unlink(ob)
 c.objects.link(ob);ob.data.materials.append(base)
 for i,(q,poly) in enumerate(zip(seeds,cells)):
  xy=[(q[0]+g*(x-q[0])-.5,q[1]+g*(y-q[1])-.5) for x,y in poly];n=len(xy);h=.015+.1*g;v=[(x,y,0) for x,y in xy]+[(x,y,h) for x,y in xy]+[(q[0]-.5,q[1]-.5,h+.035*g)]
  faces=[tuple(reversed(range(n)))]+[(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)]+[(j+n,(j+1)%n+n,2*n) for j in range(n)]
  me=bpy.data.meshes.new(f'grain_{i+1}');me.from_pydata(v,[],faces);me.update();ob=bpy.data.objects.new(f'state{k+1}_grain{i+1}',me);c.objects.link(ob);ob.data.materials.append(mats[i%5])
bpy.ops.object.camera_add(location=(1.6,-2.2,2.1));cam=bpy.context.object;s.camera=cam;cam.rotation_euler=(Vector((0,0,.06))-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=1.65
for loc,pow,size in [((1,-2,4),160,3),((-2,-1,3),100,2),((1,3,3),130,2)]:
 bpy.ops.object.light_add(type='AREA',location=loc);l=bpy.context.object;l.data.energy=pow;l.data.shape='DISK';l.data.size=size;l.rotation_euler=(Vector((0,0,0))-l.location).to_track_quat('-Z','Y').to_euler()
for k,c in cols.items():
 for j,co in cols.items():co.hide_render=j!=k
 s.render.filepath=str(o/f'state{k+1}.png');bpy.ops.render.render(write_still=True)
s.render.filepath='//state3.png';bpy.ops.wm.save_as_mainfile(filepath=str(o/'growth.blend'))
(o/'parameters.json').write_text(json.dumps({'kind':'conceptual faceted prisms over fixed Voronoi cells','no_crystallographic_claim':True,'growth_factor':d['construction_factors'],'height_rule':'0.015 + 0.1*g; roof +0.035*g; arbitrary units','seed_count':len(seeds),'camera':list(cam.location),'samples':64},indent=2))
