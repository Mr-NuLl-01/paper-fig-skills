"""Original editable spatial teaching illustration, Blender 4.5.

No experimental data, measured dimensions, material identification, calculated
electric field or paper-derived geometry is represented here. All lengths are
arbitrary illustration units. Use --render to create the two source renders,
the native .blend, parameter file, and editable SVG annotation/composite files.

blender --background --factory-startup --python advanced_device_demo.py -- \
  --out /absolute/output/directory --render
"""

import argparse
import base64
import json
import math
import sys
from pathlib import Path
from xml.sax.saxutils import escape

import bpy
from bpy_extras.object_utils import world_to_camera_view
from mathutils import Vector


EVIDENCE = 'DEMO — original teaching geometry; no measured dimensions; not to scale'
PARAMETERS = {
    'evidence': EVIDENCE,
    'scientific_object': 'generic top-contact interdigitated photoconductor',
    'units': 'arbitrary illustration units; no physical scale',
    'layer_order_bottom_to_top': [
        {'id': 'substrate', 'z_bottom': 0.0, 'thickness': 0.55,
         'meaning': 'mechanical support; material unspecified'},
        {'id': 'dielectric', 'z_bottom': 0.55, 'thickness': 0.18,
         'meaning': 'electrical isolation from support; material unspecified'},
        {'id': 'semiconductor', 'z_bottom': 0.73, 'thickness': 0.32,
         'meaning': 'continuous illustrative photoactive semiconductor'},
    ],
    'footprint': {'x_min': -5.0, 'x_max': 5.0, 'y_min': -3.0, 'y_max': 3.0},
    'cutaway': {'x_min': 1.6, 'y_max': -2.12,
                'meaning': 'front-right notch removed through all layers; conceptual cut only'},
    'contacts': {
        'z_bottom': 1.05, 'thickness': 0.11,
        'finger_width': 0.22,
        'A': {'bus_x': [-4.25, -3.65], 'bus_y': [-1.85, 2.45],
              'finger_x': [-3.95, 2.95], 'finger_y': [-1.55, -0.55, 0.45, 1.45],
              'terminal_center': [-3.95, 2.48], 'terminal_radius': 0.46},
        'B': {'bus_x': [3.65, 4.25], 'bus_y': [-1.85, 2.45],
              'finger_x': [-2.95, 3.95], 'finger_y': [-1.05, -0.05, 0.95, 1.95],
              'terminal_center': [3.95, 2.48], 'terminal_radius': 0.46},
        'meaning': 'two connected metal networks, separated from one another; same illustrative metal',
        'physical_caveat': 'no work functions, contact resistances, depletion regions or field solutions specified',
    },
    'views': {
        'overview': {'location': [10, -13, 13], 'target': [0, 0.0, 0.64],
                     'ortho_scale': 13.25, 'resolution': [1600, 1100]},
        'interface': {'location': [8.5, -11.0, 5.7], 'target': [3.25, -2.15, 0.57],
                      'ortho_scale': 4.5, 'resolution': [900, 900]},
    },
    'presentation': {
        'surface_colors': 'part identity only; not chemistry, field magnitude or measured optical color',
        'roughness': 'illustration material setting, not a measurement',
        'edge_rounding': 'illustration readability only, not fabricated edge radius',
        'denoising': 'synthetic Cycles image only; never experimental pixels',
    },
}


def arguments():
    tail = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
    p = argparse.ArgumentParser()
    p.add_argument('--out', required=True)
    p.add_argument('--render', action='store_true')
    p.add_argument('--params', help='Optional previously exported parameter JSON; geometry/view keys are reused')
    return p.parse_args(tail)


def material(name, color, metallic=0.0, roughness=0.5):
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    mat.diffuse_color = (*color, 1)
    shader = mat.node_tree.nodes.get('Principled BSDF')
    shader.inputs['Base Color'].default_value = (*color, 1)
    shader.inputs['Metallic'].default_value = metallic
    shader.inputs['Roughness'].default_value = roughness
    return mat


def move_to(obj, collection):
    for col in list(obj.users_collection):
        col.objects.unlink(obj)
    collection.objects.link(obj)


def prism(name, polygon, z0, height, mat, collection, bevel=0.0):
    """Native mesh with exact polygon footprint, genuine cut edges and caps."""
    n = len(polygon)
    vertices = [(x, y, z) for z in (z0, z0 + height) for x, y in polygon]
    faces = [tuple(range(n - 1, -1, -1)), tuple(range(n, 2*n))]
    faces += [(i, (i+1) % n, (i+1) % n + n, i+n) for i in range(n)]
    mesh = bpy.data.meshes.new(name + '__editable_mesh')
    mesh.from_pydata(vertices, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    collection.objects.link(obj)
    obj.data.materials.append(mat)
    obj['evidence'] = EVIDENCE
    if bevel:
        mod = obj.modifiers.new('Illustration edge radius — not measured', 'BEVEL')
        mod.width = bevel
        mod.segments = 3
        mod.affect = 'EDGES'
        mod = obj.modifiers.new('Weighted normals for synthetic render', 'WEIGHTED_NORMAL')
        mod.keep_sharp = True
    return obj


def rectangle(x0, x1, y0, y1):
    return [(x0,y0), (x1,y0), (x1,y1), (x0,y1)]


def contact_network(key, spec, mat, collection):
    """One editable comb mesh; exact union keeps pads and fingers connected."""
    z = PARAMETERS['contacts']['z_bottom']
    h = PARAMETERS['contacts']['thickness']
    w = PARAMETERS['contacts']['finger_width']
    network = prism('Contact_'+key+'__continuous_network',
                    rectangle(*spec['bus_x'], *spec['bus_y']), z, h, mat, collection)
    parts = []
    for i, y in enumerate(spec['finger_y']):
        parts.append(prism('temporary_'+key+'_finger_'+str(i),
                           rectangle(*spec['finger_x'], y-w/2, y+w/2),
                           z, h, mat, collection))
    cx, cy = spec['terminal_center']
    radius = spec['terminal_radius']
    circle = [(cx+radius*math.cos(i*math.tau/80),
               cy+radius*math.sin(i*math.tau/80)) for i in range(80)]
    parts.append(prism('temporary_'+key+'_terminal', circle, z, h, mat, collection))
    bpy.context.view_layer.objects.active = network
    for obj in parts:
        mod = network.modifiers.new('Connected finger / terminal union', 'BOOLEAN')
        mod.operation = 'UNION'
        mod.solver = 'EXACT'
        mod.object = obj
        bpy.ops.object.modifier_apply(modifier=mod.name)
        bpy.data.objects.remove(obj, do_unlink=True)
    bevel = network.modifiers.new('Illustration edge radius — not measured', 'BEVEL')
    bevel.width = 0.025
    bevel.segments = 3
    bevel.affect = 'EDGES'
    network.modifiers.new('Weighted normals', 'WEIGHTED_NORMAL')
    network['network_id'] = key
    network['finger_count'] = len(spec['finger_y'])
    network['terminal'] = 'same connected conductor as this network'
    network['contact_to_other_network'] = 'none; geometric separation verified by generator'
    return network


def verify_pattern():
    contacts = PARAMETERS['contacts']
    a, b = contacts['A'], contacts['B']
    # Both combs terminate short of the opposite bus; finger rows never overlap.
    assert a['finger_x'][1] < b['bus_x'][0]
    assert b['finger_x'][0] > a['bus_x'][1]
    dy = min(abs(ay-by) for ay in a['finger_y'] for by in b['finger_y'])
    assert dy > contacts['finger_width']
    # Teaching cutaway lies wholly in the electrode-free front margin.
    low = min(a['finger_y'] + b['finger_y']) - contacts['finger_width']/2
    assert PARAMETERS['cutaway']['y_max'] < min(low, a['bus_y'][0], b['bus_y'][0])
    assert math.isclose(contacts['z_bottom'], sum(x['thickness'] for x in PARAMETERS['layer_order_bottom_to_top']))
    for spec in (a,b):
        assert spec['bus_y'][0] <= min(spec['finger_y']) - contacts['finger_width']/2
        assert spec['bus_y'][1] >= max(spec['finger_y']) + contacts['finger_width']/2
        assert spec['terminal_center'][1] - spec['terminal_radius'] < spec['bus_y'][1]
        assert spec['bus_x'][0] < spec['terminal_center'][0] < spec['bus_x'][1]
    return {'A_fingers': len(a['finger_y']), 'B_fingers': len(b['finger_y']),
            'minimum_between_row_gap_illustration_units': round(dy-contacts['finger_width'], 6),
            'opposite_bus_tip_gaps_illustration_units': [round(b['bus_x'][0]-a['finger_x'][1],6), round(b['finger_x'][0]-a['bus_x'][1],6)],
            'cutaway_intersects_contacts': False,
            'physical_electrical_or_optical_model': 'not evaluated'}


def aim(obj, point):
    obj.rotation_euler = (Vector(point)-obj.location).to_track_quat('-Z', 'Y').to_euler()


def set_view(scene, camera, name):
    spec = PARAMETERS['views'][name]
    camera.location = spec['location']
    camera.data.ortho_scale = spec['ortho_scale']
    aim(camera, spec['target'])
    scene.render.resolution_x, scene.render.resolution_y = spec['resolution']
    bpy.context.view_layer.update()


def project(scene, camera, point, rect):
    q = world_to_camera_view(scene, camera, Vector(point))
    x, y, width, height = rect
    return [round(x+q.x*width, 2), round(y+(1-q.y)*height, 2)]


def write_svgs(out, anchors, images):
    width, height = 1600, 1040
    labels = [
        '<g id="header" font-family="Arial, sans-serif" fill="#203740">',
        '<text x="48" y="57" font-size="32" font-weight="600">Interdigitated contacts + a buried interface</text>',
        '<text x="48" y="94" font-size="20" fill="#526b75">DEMO · original teaching geometry · not to scale · no measured dimensions</text></g>',
        '<g id="panel-labels" font-family="Arial, sans-serif" fill="#203740">',
        '<text x="48" y="148" font-size="22" font-weight="600">A  Spatial overview</text>',
        '<text x="1130" y="260" font-size="22" font-weight="600">B  Cutaway detail</text>',
        '<text x="1130" y="288" font-size="16" fill="#526b75">Same geometry, closer camera</text></g>',
    ]
    def label(identifier, lines, x, y, anchor, bend=None, text_anchor='start', accent='#455f68', leader_end=None):
        ax, ay = anchors[anchor]
        lx, ly = leader_end if leader_end is not None else (x-12 if text_anchor == 'start' else x+12, y-6)
        if bend is None:
            path = f'M {ax},{ay} L {lx},{ly}'
        else:
            bx,by = bend
            path = f'M {ax},{ay} L {bx},{by} L {lx},{ly}'
        labels.append(f'<g id="annotation_{identifier}"><path d="{path}" stroke="{accent}" stroke-width="1.6" fill="none"/><circle cx="{ax}" cy="{ay}" r="3.6" fill="{accent}"/>')
        labels.append(f'<text x="{x}" y="{y}" text-anchor="{text_anchor}" font-family="Arial, sans-serif" font-size="19" fill="#203740">')
        for i,line in enumerate(lines):
            labels.append(f'<tspan x="{x}" dy="{0 if i == 0 else 25}">{escape(line)}</tspan>')
        labels.append('</text></g>')
    label('contact_A', ['Contact A', 'one continuous comb'], 48, 223, 'overview_A',
          bend=(330,235), leader_end=(275,235))
    label('contact_B', ['Contact B', 'separate continuous comb'], 1128, 194, 'overview_B',
          bend=(1060,260))
    label('semiconductor', ['Continuous semiconductor', 'lateral gaps remain exposed'], 48, 849,
          'overview_film', bend=(40,780), leader_end=(48,827))
    label('cut', ['Front-edge cutaway', 'outside both contact networks'], 715, 910,
          'overview_interface', bend=(826,856), leader_end=(715,888))
    # Detail labels use the left margin of the inset, avoiding its rendered face.
    label('detail_active', ['Semiconductor'], 1128, 756, 'interface_film',
          bend=(1245,720), leader_end=(1245,734))
    label('detail_dielectric', ['Dielectric layer'], 1128, 810, 'interface_dielectric',
          bend=(1302,775), leader_end=(1302,788))
    label('detail_substrate', ['Supporting substrate'], 1128, 864, 'interface_substrate',
          bend=(1390,825), leader_end=(1390,842))
    labels += [
        '<g id="footer" font-family="Arial, sans-serif" fill="#526b75" font-size="17">',
        '<text x="48" y="978">Gold identifies both metal networks; teal identifies the semiconductor. Color does not encode a measured field.</text>',
        '<text x="48" y="1007">No contact chemistry, field solution, photocurrent or fabricated dimensions are asserted. Layer thicknesses are exaggerated.</text></g>',
    ]
    svg_start = f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{width}" height="{height}" viewBox="0 0 {width} {height}">'
    meta = '<title>DEMO — interdigitated top contacts and a true geometric cutaway</title><desc>Original illustrative 3D model with two connected but mutually separated comb electrodes. No physical scale, data or paper reproduction.</desc>'
    (out/'advanced_device_labels.svg').write_text('\n'.join([svg_start,meta]+labels+['</svg>']))
    composite = [svg_start, meta, '<rect width="1600" height="1040" fill="#f7f9fa"/>']
    composite += ['<rect x="1110" y="312" width="445" height="424" rx="8" fill="#edf2f4"/>']
    for name, rect in images.items():
        data = base64.b64encode((out/f'advanced_device_{name}.png').read_bytes()).decode()
        x,y,w,h = rect
        composite.append(f'<g id="render_{name}"><image x="{x}" y="{y}" width="{w}" height="{h}" xlink:href="data:image/png;base64,{data}"/></g>')
    composite += labels + ['</svg>']
    (out/'advanced_device_preview.svg').write_text('\n'.join(composite))


def main():
    args = arguments()
    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    if args.params:
        incoming = json.loads(Path(args.params).read_text())
        for key in ('layer_order_bottom_to_top', 'footprint', 'cutaway', 'contacts', 'views'):
            if key in incoming:
                PARAMETERS[key] = incoming[key]
    checks = verify_pattern()
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    scene = bpy.context.scene
    scene['evidence'] = EVIDENCE
    scene['geometry_purpose'] = 'Explain planar electrode interdigitation and vertical interface in one spatial object'
    scene['physical_model'] = 'none — no measured evidence generated'
    scene.unit_settings.system = 'NONE'
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = 64
    scene.cycles.use_denoising = True
    scene.render.resolution_percentage = 100
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.film_transparent = True
    scene.world.color = (0.75,0.75,0.75)
    scene.view_settings.view_transform = 'AgX'
    layers = bpy.data.collections.new('01__native_cutaway_layers')
    contacts = bpy.data.collections.new('02__electrically_separate_contact_networks')
    studio = bpy.data.collections.new('03__illustration_cameras_and_lights')
    for col in (layers,contacts,studio):
        scene.collection.children.link(col)
    mats = {
        'substrate': material('DEMO matte blue-grey support', (0.43,0.51,0.58), roughness=0.65),
        'dielectric': material('DEMO pale dielectric', (0.83,0.86,0.82), roughness=0.7),
        'semiconductor': material('DEMO teal semiconductor — identity color only', (0.045,0.38,0.43), roughness=0.5),
        'metal': material('DEMO same metal for A and B — chemistry unspecified', (0.69,0.48,0.19), metallic=0.38, roughness=0.43),
    }
    # A concave footprint makes a real open notch through all three layers.
    # The newly exposed y=-2.12 face shows the buried interfaces; no overlay
    # pretends that an intact top surface is transparent.
    fp, cut = PARAMETERS['footprint'], PARAMETERS['cutaway']
    footprint = [(fp['x_min'],fp['y_min']), (cut['x_min'],fp['y_min']),
                 (cut['x_min'],cut['y_max']), (fp['x_max'],cut['y_max']),
                 (fp['x_max'],fp['y_max']), (fp['x_min'],fp['y_max'])]
    for order, spec in enumerate(PARAMETERS['layer_order_bottom_to_top']):
        obj = prism('Layer_'+spec['id']+'__real_front_notch', footprint,
                    spec['z_bottom'], spec['thickness'], mats[spec['id']], layers)
        obj['layer_order_bottom_to_top'] = order
        obj['cutaway'] = 'native concave prism; removed x>1.6 AND y<-2.12'
        obj['material_identity'] = 'unspecified; illustration color only'
    for key in ('A','B'):
        contact_network(key, PARAMETERS['contacts'][key], mats['metal'], contacts)
    bpy.ops.object.camera_add(location=(10,-13,13))
    camera = bpy.context.object
    camera.name = 'Camera__overview__orthographic'
    move_to(camera, studio)
    camera.data.type = 'ORTHO'
    scene.camera = camera
    for name, loc, power, size in [
        ('key',(-3,-5,12),1900,8),
        ('fill',(6,-2,8),1150,7),
        ('back',(-2,7,10),1300,7),
    ]:
        bpy.ops.object.light_add(type='AREA', location=loc)
        light = bpy.context.object
        light.name = 'Studio_'+name
        move_to(light, studio)
        light.data.energy = power
        light.data.shape = 'DISK'
        light.data.size = size
        aim(light,(0,0,0.5))
    images = {'overview': (0,170,1080,742.5), 'interface': (1115,312,435,435)}
    world_anchors = {
        'overview': {'overview_A': (-3.95,2.48,1.16), 'overview_B': (3.95,2.48,1.16),
                     'overview_film': (-4.65,-1.65,1.05), 'overview_interface': (3.7,-2.12,0.73)},
        'interface': {'interface_film': (2.25,-2.12,0.91),
                      'interface_dielectric': (2.9,-2.12,0.64),
                      'interface_substrate': (3.9,-2.12,0.28)},
    }
    anchors = {}
    for name in PARAMETERS['views']:
        set_view(scene, camera, name)
        for key,point in world_anchors[name].items():
            anchors[key] = project(scene, camera, point, images[name])
        if args.render:
            scene.render.filepath = str(out/f'advanced_device_{name}.png')
            bpy.ops.render.render(write_still=True)
    PARAMETERS['geometry_checks'] = checks
    PARAMETERS['annotation_canvas'] = [1600,1040]
    PARAMETERS['render_placement'] = images
    PARAMETERS['annotation_anchors_canvas_pixels'] = anchors
    PARAMETERS['annotation_anchors_world_illustration_units'] = world_anchors
    (out/'advanced_device_parameters.json').write_text(json.dumps(PARAMETERS, indent=2, ensure_ascii=False))
    if args.render:
        write_svgs(out, anchors, images)
    set_view(scene,camera,'overview')
    # Retain the second orthographic camera as an independently editable asset.
    camera_detail = bpy.data.objects.new('Camera__interface_detail__orthographic', camera.data.copy())
    studio.objects.link(camera_detail)
    spec = PARAMETERS['views']['interface']
    camera_detail.location = spec['location']
    camera_detail.data.ortho_scale = spec['ortho_scale']
    aim(camera_detail, spec['target'])
    scene.camera = camera
    bpy.ops.wm.save_as_mainfile(filepath=str(out/'advanced_device_demo.blend'))
    print(json.dumps({'saved': str(out/'advanced_device_demo.blend'),
                      'geometry_checks': checks, 'evidence': EVIDENCE}))


if __name__ == '__main__':
    main()
