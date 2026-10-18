---
name: sci-figure-data
description: Choose and produce editable quantitative scientific figures for performance curves, repeated samples, spectra, time/frequency responses, heatmaps, parameter sweeps and trade-offs. Preserve units, conditions, uncertainty and measured/modelled boundaries.
---

# Quantitative figures: start with the comparison

## Data contract
State what the reader must decide. Inspect units, independent samples, batches, conditions, missing values and provenance. Only ask for missing quantities that prevent the comparison. Without measurements, make explicitly labelled DEMO figures, never invented research results.

Preserve raw values and transformations, including sample_id, batch_id, condition and measurement_type, plus relevant time, bandwidth, initial brightness or temperature. Separate measurement, calibration, fitting, simulation and extrapolation. An author's software is unknown unless documented.

## Select the representation
- Driving conditions or performance: unit-bearing curves and working windows, not only champion bars.
- Reproducibility: individual points, paired connections, batch facets and defined distribution bands.
- Time and frequency: synchronized input/output, separate magnitude, phase and noise with bandwidth.
- Spectra and maps: original spectra or heatmaps, then extracted quantities and fits; share scales when comparison needs them.
- Associations: scatter, paired differences and intervals that preserve hierarchy; correlation does not establish causation.
- Trade-offs: conditional scatter, feasible regions or parameter surfaces; do not compare mixed-unit radar areas.

Consult [references/task-cases.md](references/task-cases.md) selectively and [references/scientific-checks.md](references/scientific-checks.md) for lifetime, log axes, normalization and statistics. For stacked maps and waterfall plots, read [references/stacked-views.en.md](references/stacked-views.en.md).

## Preserve comparisons
Decide which quantities require shared axes, scales and operating conditions. Unequal panel layouts and paired rows are allowed. Perspective is not a replacement for accurate quantitative reading. Register object colors, state markers and continuous color maps; preserve zero, ranges, saturation and missingness. Emission color and thermal pseudocolor are not treatment identity.

Keep weak tails, outliers and unfavorable groups. Do not silently remove nonpositive log values or add arbitrary offsets. Define breaks and normalization. Keep pairs and batch hierarchy; technical repeats are not independent devices. Define SD, SE, CI or quantiles rather than using unspecified error bars. Lifetime extrapolation must name its model and fitting interval. Shared intensity claims require comparable calibration.

## Execute and deliver
Choose an appropriate existing Python, R or vector workflow; see [references/reconstruction.md](references/reconstruction.md). Generate exact charts from numbers, not image generation. Export editable SVG/PDF and a preview; inspect units, glyphs, legends, clipping, scales and small-size readability. Deliver source data, code, transformations and a self-contained caption stating sample units, uncertainty definitions, conditions and evidence type. The bundled make_demo.py is an illustration, not a compulsory layout.
