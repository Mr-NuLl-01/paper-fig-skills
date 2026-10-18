"""Reopen the saved native scene, inspect native mesh connectivity, render again.

blender -b advanced_device_demo.blend --python verify_native.py
The script intentionally does not save over the source scene.
"""
import json
from pathlib import Path

import bmesh
import bpy


def mesh_report(obj):
    mesh = obj.data
    adjacency = {v.index: set() for v in mesh.vertices}
    for edge in mesh.edges:
        a,b = edge.vertices
        adjacency[a].add(b)
        adjacency[b].add(a)
    unseen = set(adjacency)
    components = 0
    while unseen:
        components += 1
        stack = [unseen.pop()]
        while stack:
            for other in adjacency[stack.pop()]:
                if other in unseen:
                    unseen.remove(other)
                    stack.append(other)
    bm = bmesh.new()
    bm.from_mesh(mesh)
    nonmanifold = sum(not edge.is_manifold for edge in bm.edges)
    volume = bm.calc_volume(signed=False)
    bm.free()
    return {'vertices': len(mesh.vertices), 'edges': len(mesh.edges),
            'polygons': len(mesh.polygons), 'connected_components': components,
            'nonmanifold_edges': nonmanifold,
            'volume_arbitrary_illustration_units': volume}


out = Path(bpy.data.filepath).resolve().parent
scene = bpy.context.scene
objects = {obj.name: mesh_report(obj) for obj in scene.objects if obj.type == 'MESH'}
for key in ('A','B'):
    obj = objects['Contact_'+key+'__continuous_network']
    assert obj['connected_components'] == 1
    assert obj['nonmanifold_edges'] == 0
assert len(objects) == 5
assert all(obj['connected_components'] == 1 and obj['nonmanifold_edges'] == 0 for obj in objects.values())
assert len([obj for obj in scene.objects if obj.type == 'CAMERA']) == 2
assert 'DEMO' in scene['evidence']
scene.camera = bpy.data.objects['Camera__overview__orthographic']
scene.render.resolution_x = 1600
scene.render.resolution_y = 1100
scene.render.resolution_percentage = 100
scene.render.filepath = str(out/'advanced_device_reopened_check.png')
bpy.ops.render.render(write_still=True)
report = {'native_file_reopened': str(bpy.data.filepath),
          'blender_version': bpy.app.version_string,
          'reopened_render': 'advanced_device_reopened_check.png',
          'mesh_objects': objects,
          'camera_count': 2,
          'evidence': scene['evidence'],
          'scope': 'geometry connectivity/manifold/native reopen checks only; no physical simulation'}
(out/'native_verification.json').write_text(json.dumps(report, indent=2, ensure_ascii=False))
print(json.dumps(report, ensure_ascii=False))
