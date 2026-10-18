# Gallery revision history

## R2 visual revisions / 第二版

- 01b follows a raincloud grammar: median/IQR/1.5-IQR whiskers, all points and a half KDE. Thirty synthetic samples per batch are used to demonstrate density, rather than fitting a persuasive smooth outline to six points. This changes demo data only, not experimental data.
- 02 uses a revised muted layer palette and centered light-output arrow. 02b adds native six-layer Blender geometry and two camera-matched views.
- 03 separates level lines, process arrows and labels by drawing order; endpoints remain attached to their states.
- 04 uses fixed-seed Voronoi cells, homothetic growth and an exact geometrical area ledger. The parameter is not time and this is not a crystallization law.
- 05 retains an explicit missing-data example, now directly called out.
- 06 uses Blues; 07 uses YlOrBr, with separate meanings for curve-condition color and heatmap intensity; 08 uses PuRd. These are choices for these examples, not universal skill palettes.

### Optional native 3D companion

```sh
blender -b -t 2 --python examples/gallery/device3d.py -- --out examples/gallery/output/device3d
python examples/gallery/compose3d.py
python examples/gallery/check.py
```

Run Blender in a fresh background process: the example clears the scene. The saved device.blend retains named assembled/exploded collections and independent layer meshes/materials; geometry.json records original coordinates and exploded displacements. The output path stored in the blend is relative. Labels are independently editable in the composite SVG; render pixels are embedded. Thicknesses and gaps are display choices, not measured dimensions. Denoising is disabled because the tested Blender build lacks OpenImageDenoise. Rendering uses 128 samples and two CPU threads. The initial failed denoising attempt is a preparation failure, not a successful render.

The user-provided reference was a box/point/density style example. Its pixels are not copied into the gallery or redistributed in the repository.

## R3 revisions

- Example 05 now uses complete synthetic arrays without a missing patch. Missing-data handling remains part of the skills, but is no longer illustrated in this presentation.
- Example 06 now displays the signed difference of two analytic fields with RdBu_r and a fixed −1 to +1 range. White means zero; it is not simply a cosmetic recoloring of a positive intensity field.
- Example 08 uses a light sequential subset of GnBu (0.05–0.72), mapped to the full 0–1 scalar range.
- Device layer leaders use camera-projected 3D anchor points saved in label_points.json.
- Growth is now a three-state native Blender construction with a same-domain 2D plan view. Facets are conceptual prisms, not identified crystal faces or a crystallographic model.

To regenerate the final growth composite, after generate.py:

```sh
blender -b -t 2 --python examples/gallery/growth3d.py -- --out examples/gallery/output/growth3d
python examples/gallery/compose_growth.py
```

Run compose_growth.py after the base generator because it replaces the base 04 preview with the 3D/2D composite. Keep the generated JSON: it contains the fixed seeds and polygon footprints shared by both views. Both .blend files are native editable scenes; SVG overlays retain editable labels and 2D shapes.

## R4 revisions
Device leaders now anchor on each layer's rightmost visible edge. Example 08 uses an original muted teal / neutral / coral diverging map, informed by the user's color reference (reference pixels and numbers are not redistributed). The synthetic field is now a signed analytic Gaussian difference, with a real zero center and shared −1 to +1 scale. This is explicitly a changed synthetic demonstration, not a recoloring or alteration of experimental data.

## R5: intersecting slices
Example 08 now puts both orthogonal planes into one joint tiled polygon collection, with tiles split at their intersection and sorted together. Separate surface collections had sorted whole planes and produced the wrong occlusion relationship. The change fixes this example's camera/view; it is not a claim that painter sorting handles every possible intersecting 3D geometry. For arbitrary intersecting geometry, use a real depth-buffer renderer and validate visibility.
