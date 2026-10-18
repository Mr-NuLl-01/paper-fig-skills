---
name: sci-figure-device
description: Create editable device, material and experimental-setup schematics: layer sections, interfaces, optical paths, assemblies, exploded views and multiscale geometry. Choose SVG, CAD or optional Blender to fit the spatial question.
---

# Devices, structures and measurement space

Determine the spatial relationship before adding materials or rendering. Keep geometry, annotations and data independently editable.

List component identities, layers, contacts, dimensions and units, sealed boundaries, stimuli, detection paths and readout positions. State the figure's question. Do not infer missing electrodes, probes or chemistry from familiarity. Use not to scale for unknown or exaggerated dimensions, not a falsely precise ruler.

## Choose by geometry
Use accurate 2D sections for layers and interfacial transport; topology plus a section for access to controlled environments; exploded views with correspondence for hidden assembly; CAD/Blender for curved or 3D geometry that matters; and located ROIs with scale transitions for multiscale structures. Consult [references/routes-and-evidence.md](references/routes-and-evidence.md) and [references/geometry-and-export.md](references/geometry-and-export.md).

## Editable construction
Validate topology before styling. Name SVG groups for materials, contacts, boundaries, inputs, outputs and labels. Record true and displayed thickness separately. An exploded displacement must not change assembly relationships or imply physical gaps. Pair perspective with a section when contacts would otherwise be ambiguous.

Optional Blender models retain named independent objects, original coordinates, dimensions, camera, materials and editable modifiers. Real lattices require supplied coordinates; volume geometry requires data. Conceptual texture is not microscopy. Keep text and scale bars in an independent vector layer. Register material and path colors; transparency must not erase a sealing wall. Highlights and roughness describe appearance, not unmeasured composition.

## Review and deliver
Render at the target size and check order, contact, polarity, paths, sampling volume and legibility of thin layers. State simplifications, unknowns and schematic status. Deliver SVG/PDF and previews; if 3D was used, include native geometry, configuration and render parameters. If optional 3D tools are absent, complete an adequate 2D route. Do not attribute your chosen software to a paper's authors.

The bundled device_demo.py is a DEMO only. It clears scene objects: run it in a separate background process or a new saved-safe file, not in an unsaved working scene.

For 3D layer labels, project defined object anchors through the final camera and save those coordinates. Reproject after camera changes; retain original contact topology despite exploded display gaps.
