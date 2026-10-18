"""Blender: synthetic LED geometry applying sci-figure-device only.
blender -b -t 2 --python examples/gallery/device3d.py -- --out DIR
Named independent layers, assembled and exploded collections; no measured dimensions.
"""
import bpy,sys,json,math,argparse
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
p=argparse.ArgumentParser();p.add_argument('--out',required=True);a=p.parse_args(sys.argv[sys.argv.index('--')+1:]);out=Path(a.out).resolve();out.mkdir(parents=True,exist_ok=True)
bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
sc=bpy.context.scene;sc.render.engine='CYCLES';sc.cycles.samples=128;sc.cycles.use_denoising=False;sc.render.threads_mode='FIXED';sc.render.threads=2
sc.render.resolution_x=1000;sc.render.resolution_y=800;sc.render.resolution_percentage=100;sc.render.image_settings.file_format='PNG';sc.render.image_settings.color_mode='RGBA';sc.render.film_transparent=True
sc.world.color=(.6,.6,.6)
sc.view_settings.view_transform='Standard'
layers=[('Glass','#d5e4e9',.32),('Transparent_anode','#8fb3c3',.09),('Hole_transport','#b58ca4',.13),('Emitter','#58a897',.17),('Electron_transport','#7d91ba',.13),('Metal_cathode','#56677e',.16)]
def rgb(h):return tuple(((int(h[i:i+2],16)/255+.055)/1.055)**2.4 for i in (1,3,5))
cols={};objects=[]
for name in ['assembled','exploded']:
 col=bpy.data.collections.new(name);sc.collection.children.link(col);cols[name]=col;z=0
 for i,(lab,h,t) in enumerate(layers):
  mat=bpy.data.materials.get(lab) or bpy.data.materials.new(lab);mat.diffuse_color=(*rgb(h),1);mat.use_nodes=True;sh=mat.node_tree.nodes.get('Principled BSDF');sh.inputs['Base Color'].default_value=(*rgb(h),1);sh.inputs['Roughness'].default_value=.35;sh.inputs['Metallic'].default_value=.35 if i==5 else 0
  shift=i*.38 if name=='exploded' else 0
  bpy.ops.mesh.primitive_cube_add(size=1,location=(0,0,z+t/2+shift));ob=bpy.context.object;ob.name=f'{name}_{lab}';ob.dimensions=(4,3,t);bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
  for co in list(ob.users_collection):co.objects.unlink(ob)
  col.objects.link(ob);ob.data.materials.append(mat);bev=ob.modifiers.new('small_edge_bevel','BEVEL');bev.width=.012;bev.segments=3;ob.modifiers.new('weighted_normals','WEIGHTED_NORMAL');objects.append({'name':ob.name,'dimensions':list(ob.dimensions),'location':list(ob.location),'assembled_z':z+t/2,'exploded_shift':shift,'color':h});z+=t
bpy.ops.object.camera_add(location=(7,-9,6));cam=bpy.context.object;sc.camera=cam;cam.data.type='ORTHO';cam.data.ortho_scale=6.8
for loc,power,size in [((1,-4,8),700,5),((-5,-2,4),350,4),((3,5,6),600,4)]:
 bpy.ops.object.light_add(type='AREA',location=loc);l=bpy.context.object;l.data.energy=power;l.data.shape='DISK';l.data.size=size;l.rotation_euler=(Vector((0,0,.8))-l.location).to_track_quat('-Z','Y').to_euler()
for variant in cols:
 for name,col in cols.items():col.hide_render=name!=variant
 target=(0,0,.6 if variant=='assembled' else 1.55);cam.rotation_euler=(Vector(target)-cam.location).to_track_quat('-Z','Y').to_euler();sc.render.filepath=str(out/f'{variant}.png');bpy.context.view_layer.update()
 if variant=='exploded':
  pts=[]
  for lab,_,_ in layers:
   ob=bpy.data.objects['exploded_'+lab];q=world_to_camera_view(sc,cam,Vector((2,1.5,ob.location.z)));pts.append({'name':lab,'pixel':[q.x*1000,(1-q.y)*800]})
  (out/'label_points.json').write_text(json.dumps(pts,indent=2))
 bpy.ops.render.render(write_still=True)
# Save a portable path and assembled initial view, with both collections retained.
cols['assembled'].hide_render=False;cols['exploded'].hide_render=True;cam.rotation_euler=(Vector((0,0,.6))-cam.location).to_track_quat('-Z','Y').to_euler();sc.render.filepath='//assembled.png'
bpy.ops.wm.save_as_mainfile(filepath=str(out/'device.blend'))
(out/'geometry.json').write_text(json.dumps({'kind':'conceptual only','units':'arbitrary display units','thickness':'exaggerated, not measured','objects':objects,'camera':{'location':list(cam.location),'type':'ORTHO','scale':6.8},'samples':128,'render_engine':'CYCLES','denoising':'disabled; local Blender lacks OpenImageDenoise'},indent=2))
