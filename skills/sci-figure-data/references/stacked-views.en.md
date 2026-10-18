# Stacked maps, waterfalls and complex comparative views

Choose a view from the reader's task, not from dimensionality as decoration.

## Coordinate contract
Record every axis, its units, sample/condition IDs, actual coordinate values, transformations and missing-value mask. Distinguish:
1. x–y–z spatial data from one calibrated volume;
2. x–y maps indexed by time, temperature, bias or another measurement condition;
3. a curve family with an independent condition coordinate;
4. artificial display offsets with no physical meaning.
A categorical series has labelled categories, not a fabricated numerical metric. Irregular numerical spacing stays irregular unless an explicitly labelled ordinal view is offered.

## Stacked heatmap planes
A plane carries two coordinates; its height carries the third coordinate; color carries a separate scalar. Use one normalization across comparable planes and show its units. Do not use height for the scalar while also calling it time. Save plane locations, ordering, view angle, colormap, limits and interpolation method.

Opaque planes preserve color meaning but can hide lower planes. Choose a view that exposes useful regions and include unobscured 2D slices with the same color scale. Transparency blends colors: it does not preserve directly readable scalar values and must not be the only quantitative representation. Do not turn multiple unrelated maps into a supposed 3D reconstruction. Sparse time planes do not establish a continuous movie; interpolation must be labelled and justified.

## Curve waterfalls
For f(x,c), use x, the actual condition c and amplitude f as three separate coordinates. State whether amplitude is absolute, globally normalized, independently normalized or offset. Keep physical nonuniform condition spacing; use direct labels or a continuous condition legend. A 2D heatmap or aligned profiles is a useful companion because perspective obscures exact amplitude and rear curves.

For 2D offset stacks, retain each baseline and record the exact offsets. The displaced ordinate is not absolute intensity. Do not silently normalize every spectrum or smooth away weak peaks. Ordering must be predefined or disclosed. Preserve sign, negative values, detection limits and outliers; log amplitudes require an explicit policy for nonpositive values.

## Complex heatmaps
Keep common axes/ranges for intensity comparisons. Separate magnitude, signed residuals (meaningful center), phase (cyclic map), categories and missing values. Residual and signal maps can have different scales, explicitly labelled. Show masks, clipping and saturation. Clustering/reordering needs a stated criterion and row/column IDs; an event-time-sorted diagonal does not prove spatial propagation. Mark whether cell boundaries denote actual bins or display interpolation between point samples.

## Genuine volumes and irregular layouts
For volumetric data, retain voxel spacing, axis order, slice index/coordinate, interpolation and transfer function. Locate sections in a 3D view and pair them with unoccluded orthogonal cuts and a profile. Threshold surfaces must report the threshold; smoothed geometry is a processed representation, not raw evidence.

Unequal panels may allocate more space to the decisive comparison. Use a clear reading order, aligned related axes and common object/color identities. Do not distort spatial aspect ratios merely to fill a panel. Distinguish a not-to-scale schematic from a calibrated image.

## Practical acceptance
Check projected overlap, rear-plane visibility, legends, shared ranges, zero/missing semantics, physical aspect ratio, final-size fonts and complete exports. Save raw arrays, coordinate vectors, masks, transforms, camera and generator. A projected SVG remains a 2D editable projection; retain code/data for reorienting the 3D scene. Do not claim native 3D editability from SVG alone.

Gallery examples 05–08 demonstrate these choices with explicitly synthetic data. The gallery is not a mandatory visual template.

## Distribution composites and visual layering
Raincloud views can combine a box, all raw points and a half violin. Define median, quartiles and whisker rule; whiskers are not automatically SD. A violin is a KDE, not a measured outline: report bandwidth and assess whether sample size supports it. Prefer raw points without a density for sparse samples. Never add experimental observations merely to smooth a plot.

Preserve arrow endpoints at their scientific states. Separate background fills, level lines, process arrows and labels by drawing order; do not move endpoints into undefined states to avoid overlap. Label missing-data patches directly or in a legend so they do not resemble export defects.

## Intersecting-plane rendering
Some plotting backends sort entire surface collections rather than individual intersecting geometry. Two orthogonal slices may therefore appear to pass through each other incorrectly. Split at the intersection and sort the relevant subfaces together, or use a depth-buffer renderer. Check both sides of the crossing at the final camera angle; changing opacity does not fix incorrect visibility. Keep the unobscured 2D slices for quantitative reading.
