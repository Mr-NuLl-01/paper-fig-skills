---
name: sci-figure-image
description: Compose scientific microscopy, spectral maps, quantitative fields and volumes with editable annotations, ROIs, profiles and orthogonal slices. Preserve evidence pixels and comparable scales; do not beautify experimental data.
---

# Scientific images, volumes and fields

Treat images as evidence. Keep originals, pixel/voxel calibration, acquisition metadata and processing records. A publication image can be arranged, but does not support new raw-data quantification by itself.

Record specimen/object ID, modality, orientation, time/scan method, channels, units, processing, ROI and source. Separate experimental pixels, calculated fields, segmentation and conceptual drawings. Do not infer true resolution or author software from appearance. Read [references/pixels-and-annotations.md](references/pixels-and-annotations.md). Never generatively repair, erase specks, complete edges, smooth lattices or redraw evidence.

## Choose the evidence view
Use paired images or condition matrices for structure, full field plus located inset/profile for defects, registered frames and object IDs for evolution, structure plus spectra for chemistry, located orthogonal cuts for volumes, and object-by-time maps for heterogeneity. Read [references/volume-fields-and-cases.md](references/volume-fields-and-cases.md). For stacked planes and complex heatmaps, read the sibling data module's [stacked views](../sci-figure-data/references/stacked-views.en.md).

Compare physical scale before cropping: equal pixel widths do not imply equal magnification. Absolute intensity needs shared calibration and ranges. If normalized independently, compare only the retained relative information. Preserve measurement meanings of channel colors; record LUT changes.

Place ROI boxes, boundaries, labels, scale bars and color bars in independent vector layers. Insets retain source coordinates; do not crop away counterexamples. Save registration transforms, never freely deform objects to make them match. Keep source pixels inspectable alongside segmentation.

## Color and volume semantics
Sequential scales encode ordered magnitude, diverging scales need a meaningful center, and categorical phases need discrete colors. Distinguish missing, masked and saturated values. Scattering is not automatically concentration; absent signal does not identify a material.

Locate volume slices first, then choose surfaces, volume rendering or unfolding. Preserve thresholds, transfer functions, interpolation and coordinates. Lighting may reveal data geometry but must not remodel pores or boundaries. Negative space requires independent evidence for identity.

Inspect at final size and deliver editable SVG/PDF with original images, preview, source/processing manifest and relevant scripts. State scan timing, normalization, filtering, segmentation and inference limits. Volumes additionally retain parameters and transforms.
