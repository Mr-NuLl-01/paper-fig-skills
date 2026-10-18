---
name: sci-figure-color
description: Design and diagnose categorical, sequential, diverging and cyclic color encodings for scientific figures, including missing data, contrast and cross-panel identity. Avoid universal palettes or unsupported accessibility claims.
---

# Color is an interpretable encoding

Decide whether color identifies an object, magnitude, sign, direction, state or decoration. Different scopes may coexist, but legends must define them. Check established element/channel conventions before replacing them.

Use categorical colors with shapes or labels for unordered groups; sequential maps for ordered magnitude; diverging maps only around a meaningful center; cyclic maps for phase or angle with period/direction; and explicit two-dimensional legends or facets for bivariate encoding. Missing and inapplicable values are not zero. Preserve microscopy channel identity and record LUT changes.

Read [references/color-semantics.md](references/color-semantics.md). The twelve palettes in [assets/palettes.json](assets/palettes.json) are original starting points, not exact paper colors or certified universally accessible palettes. Inspect the actual figure, not only swatches.

## Implementation
Register entities, conditions, states and fields separately. Keep identity across views, or explain scope changes. Too many categories may call for grouping/faceting rather than more hues. Thin lines and small points need stronger contrast than large fills. Light fills can use dark edges; dark image panels and white statistical panels can coexist.

Never alter specimen intensity, independently autoscale comparisons or add false signal halos for appearance. Use established scientific continuous maps where available rather than interpolating category swatches. Check sequential lightness, diverging sides and cyclic closure according to their meanings; cyclic lightness cannot be globally monotonic.

The bundled palette_audit.py reports swatches, grayscale, three color-vision approximations, L*, approximate ΔE76 and contrast. Run with --palette indigo-copper --out OUTPUT, or --colors and --background. These are limited diagnostics, not guarantees about all sizes, occlusion, vision or semantics. Simulation transforms linear RGB and records gamut clipping. Read [references/diagnostics-and-sources.md](references/diagnostics-and-sources.md), and the repository's known issues before trusting nonwhite-background SVG previews.

## Delivery
Save the color registry, range/center/missing-value definitions, real figure and diagnostic preview. Retain color bars and units. Check key comparisons at final size and add line style, shape or direct labels when necessary. Report only the scenarios actually checked.
