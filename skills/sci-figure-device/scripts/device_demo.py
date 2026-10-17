"""Blender 4.x: editable illustrative stack, exploded assembly, and section.

Run: blender -b --python device_demo.py -- --out /absolute/out --render
DEMO geometry only. No measured or paper-derived device dimensions are used.
"""
import argparse
import base64
import json
import math
import sys
from pathlib import Path

import bpy
from mathutils import Vector


def arguments():
    tail = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument('--out', required=True)
    p.add_argument('--render', action='store_true')
    p.add_argument('--resolution', type=int, default=1100)
    return p.parse_args(tail)


def material(name, color, metallic=0.0, roughness=0.35, transmission=0.0):
    m = bpy.data.materials.new(name)
    m.diffuse_color = (*color, 1.0)
    m.use_nodes = True
    shader = m.node_tree.nodes.get('Principled BSDF')
    shader.inputs['Base Color'].default_value = (*color, 1)
    shader.inputs['Metallic'].default_value = metallic
    shader.inputs['Roughness'].default_value = roughness
    shader.inputs['Transmission Weight'].default_value = transmission
    shader.inputs['IOR'].default_value = 1.46
    return m


def box(name, dimensions, location, mat, collection):
    bpy.ops.mesh.primitive_cube_add(size=1, location=location)
    obj = bpy.context.object
    obj.name = name
    obj.dimensions = dimensions
    bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
    for parent in list(obj.users_collection):
        parent.objects.unlink(obj)
    collection.objects.link(obj)
    obj.data.materials.append(mat)
    bevel = obj.modifiers.new('Editable edge rounding - illustration only', 'BEVEL')
    bevel.width = min(dimensions) * 0.06
    bevel.segments = 3
    obj.modifiers.new('Weighted surface normals', 'WEIGHTED_NORMAL')
    return obj


def aim(obj, point):
    direction = Vector(point) - obj.location
    obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()


def svg_side(path, layers):
    # All polygons, leader lines, and labels remain independently editable.
    widths = {x['name']: x['dimensions'][0] for x in layers}
    fills = {'substrate': '#c2ccd5', 'bottom_electrode': '#b56b43',
             'active_DEMO': '#34a6b1', 'top_electrode': '#c7a255',
             'cover_DEMO': '#dfe9f4'}
    y = 430
    parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="600" viewBox="0 0 1100 600">',
             '<title>DEMO illustrative layered structure — not measured</title>',
             '<g id="labels" fill="#22313c" font-family="Arial, sans-serif">',
             '<text x="55" y="48" font-size="28">DEMO · editable side section</text>',
             '<text x="55" y="80" font-size="17">Illustrative geometry; thickness exaggerated; no physical scale</text></g>']
    # Display scale chosen for clarity, explicitly not a physical scale bar.
    for i, layer in enumerate(layers):
        h = layer['dimensions'][2] * 165
        w = widths[layer['name']] * 75
        x = 55 + (450 - w)/2
        y -= h
        label_y = 180 + (len(layers)-1-i)*47
        parts += [f'<g id="layer_{layer["name"]}"><rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" fill="{fills[layer["name"]]}" stroke="#33424c" stroke-width="1"/></g>',
                  f'<g id="annotation_{layer["name"]}" fill="none" stroke="#546674"><path d="M{x+w:.2f},{y+h/2:.2f} H560 L610,{label_y-6}"/></g>',
                  f'<g id="text_{layer["name"]}" font-family="Arial, sans-serif" font-size="20" fill="#22313c"><text x="625" y="{label_y}">{layer["name"].replace("_", " ")}</text></g>']
    parts += ['<g id="note" font-family="Arial, sans-serif" fill="#546674" font-size="16"><text x="55" y="535">Source assets: device_demo.blend · separate assembled / exploded / section collections</text><text x="55" y="565">Material colors identify parts; they do not encode composition, thickness or performance.</text></g></svg>']
    path.write_text('\n'.join(parts))


def svg_overlay(path):
    path.write_text('''<svg xmlns="http://www.w3.org/2000/svg" width="1100" height="750" viewBox="0 0 1100 750">
<title>Editable overlay for DEMO renders</title>
<g id="demo-label" font-family="Arial, sans-serif" fill="#20353f">
<text x="38" y="45" font-size="28">DEMO · illustrative geometry</text>
<text x="38" y="74" font-size="17">Not measured · not a reconstruction of a published figure</text>
<text x="38" y="713" font-size="17">Material labels and section references remain editable in the side-section SVG.</text>
</g></svg>''')


def svg_preview(out):
    parts=['<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="1500" height="560" viewBox="0 0 1500 560">',
           '<title>DEMO editable structure: assembled, exploded and section</title>',
           '<rect width="1500" height="560" fill="#f6f8fa"/>',
           '<g id="preview-title" font-family="Arial, sans-serif" fill="#20353f"><text x="40" y="48" font-size="28">DEMO · three editable spatial views</text><text x="40" y="80" font-size="18">Illustrative geometry, not measured · all materials, parts and cameras retained in device_demo.blend</text></g>']
    for i,(variant,label) in enumerate([('assembled','A · assembled'),('exploded','B · exploded assembly'),('section','C · planar half-section')]):
        x=40+i*490
        data=base64.b64encode((out/f'device_demo_{variant}.png').read_bytes()).decode()
        parts += [f'<g id="view_{variant}"><text x="{x}" y="128" font-family="Arial, sans-serif" font-size="21" fill="#20353f">{label}</text><image x="{x-20}" y="145" width="480" height="327" xlink:href="data:image/png;base64,{data}"/></g>']
    parts += ['<g id="preview-note" font-family="Arial, sans-serif" font-size="17" fill="#51636e"><text x="40" y="512">Layer identities and editable leader lines: device_demo_side_section.svg</text><text x="40" y="539">No physical scale; thicknesses exaggerated for explanation. This example does not reproduce a published figure.</text></g></svg>']
    (out/'device_demo_preview.svg').write_text('\n'.join(parts))


def main():
    args = arguments()
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    for collection in list(bpy.data.collections):
        if collection.name != 'Collection' and not collection.objects:
            bpy.data.collections.remove(collection)
    scene = bpy.context.scene
    scene['figure_evidence'] = 'DEMO / illustrative / no real device measurements'
    scene.unit_settings.system = 'NONE'
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 40
    scene.cycles.use_denoising = True  # Only the synthetic illustrative render.
    scene.render.resolution_x = args.resolution
    scene.render.resolution_y = round(args.resolution * 750/1100)
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.film_transparent = True
    scene.world.color = (0.7, 0.7, 0.7)
    scene.view_settings.view_transform = 'AgX'
    mats = {
        'substrate': material('DEMO ceramic substrate', (0.48, 0.55, 0.62), roughness=0.5),
        'bottom_electrode': material('DEMO copper tone bottom electrode', (0.55, 0.23, 0.10), metallic=0.65),
        'active_DEMO': material('DEMO teal active layer', (0.025, 0.36, 0.40), roughness=0.3),
        'top_electrode': material('DEMO pale gold top electrode', (0.65, 0.44, 0.16), metallic=0.7),
        'cover_DEMO': material('DEMO translucent cover', (0.65, 0.77, 0.86), roughness=0.12, transmission=0.7),
    }
    layers = [
        {'name':'substrate', 'dimensions':(6.0, 4.0, 0.34)},
        {'name':'bottom_electrode', 'dimensions':(5.6, 3.6, 0.11)},
        {'name':'active_DEMO', 'dimensions':(5.2, 3.2, 0.38)},
        {'name':'top_electrode', 'dimensions':(4.8, 2.8, 0.13)},
        {'name':'cover_DEMO', 'dimensions':(6.0, 4.0, 0.23)},
    ]
    collections = {}
    for variant in ['assembled', 'exploded', 'section']:
        col = bpy.data.collections.new('DEMO_' + variant)
        scene.collection.children.link(col)
        collections[variant] = col
        z = 0.0
        for i, layer in enumerate(layers):
            dx, dy, dz = layer['dimensions']
            shift = i*0.52 if variant == 'exploded' else 0
            if variant == 'section':
                # A true planar half-section, retaining each original rear boundary.
                dy = dy/2
                center_y = dy/2
            else:
                center_y = 0
            obj = box(variant+'__'+layer['name'], (dx,dy,dz), (0,center_y,z+dz/2+shift), mats[layer['name']], col)
            obj['source'] = 'illustrative DEMO'
            obj['layer_order_bottom_to_top'] = i
            obj['assembled_z_bottom'] = z
            obj['cut_plane'] = 'y=0; rear half retained' if variant == 'section' else 'none'
            z += dz
    bpy.ops.object.camera_add(location=(9,-11,8))
    camera = bpy.context.object
    camera.name = 'DEMO editable orthographic camera'
    camera.data.type = 'ORTHO'
    scene.camera = camera
    for name, loc, power, size in [('key',(1,-5,9),1400,7),('fill',(-5,-1,5),850,6),('rim',(2,5,7),1000,5)]:
        bpy.ops.object.light_add(type='AREA', location=loc)
        light=bpy.context.object
        light.name='DEMO '+name
        light.data.energy=power
        light.data.shape='DISK'
        light.data.size=size
        aim(light,(0,0,0.8))
    views = {
        'assembled': {'camera':(9,-11,8),'target':(0,0,0.7),'scale':8.3},
        'exploded': {'camera':(9,-11,9),'target':(0,0,1.65),'scale':9.2},
        'section': {'camera':(7,-12,5.6),'target':(0,0.6,0.65),'scale':7.8},
    }
    svg_side(out/'device_demo_side_section.svg',layers)
    svg_overlay(out/'device_demo_overlay.svg')
    params = {'evidence':'DEMO / illustrative / not to physical scale','layers':layers,'views':views,
              'collections':list(collections),'render_note':'Denoising applies only to generated illustration; never apply to experimental pixels.'}
    (out/'device_demo_parameters.json').write_text(json.dumps(params,indent=2))
    def set_view(name):
        for key,col in collections.items():
            col.hide_render = key != name
            col.hide_viewport = key != name
        view=views[name]
        camera.location=view['camera']
        camera.data.ortho_scale=view['scale']
        aim(camera,view['target'])
    if args.render:
        for variant in views:
            set_view(variant)
            scene.render.filepath=str(out/f'device_demo_{variant}.png')
            bpy.ops.render.render(write_still=True)
        svg_preview(out)
    set_view('assembled')
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'device_demo.blend'))
    print(json.dumps({'saved':str(out/'device_demo.blend'),'rendered':args.render,'evidence':'DEMO'}))


if __name__ == '__main__':
    main()
