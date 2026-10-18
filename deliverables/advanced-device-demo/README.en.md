# Interdigitated contacts and a buried interface

[Original Chinese explanation](README_zh.md) · [Repository guide](../../docs/USER_GUIDE.en.md)

![Original teaching illustration](advanced_device_preview.png)

This original 2026-10-17 companion example combines two continuous, separate interdigitated contact networks with a real geometric front-edge cutaway exposing the semiconductor, dielectric and substrate. The overview and close-up use the same native model. Gold identifies both contacts; teal identifies the continuous semiconductor. Geometry is arbitrary and layer thickness is exaggerated. No electric-field solution, measured dimension, contact barrier or material chemistry is asserted.

## Edit or reproduce

- `advanced_device_demo.blend`: native objects, materials, lights and two cameras.
- `advanced_device_demo.py`: parameterized geometry, rendering and projected SVG leaders.
- `advanced_device_parameters.json`: geometric configuration and scope.
- `advanced_device_labels.svg`: independent editable annotations.
- `advanced_device_preview.svg`: composite with embedded render pixels and live text.
- `advanced_device_overview.png` / `advanced_device_interface.png`: source views.

The original execution record uses Blender 4.5.0:

```sh
blender --background --factory-startup --python advanced_device_demo.py -- --out /actual/output --render
```

Use `--params /actual/advanced_device_parameters.json` to reuse configuration. Use a fresh background scene; preserve your own work. Rendering may require denoising support in the selected Blender build. The historical preview and recorded checks are preserved, not claimed as a new full rerender in this repository update.

## Provenance

Imported from the user's verified 151-file Science Figure Atlas archive, whose source SHA-256 is recorded in `docs/ARCHIVE_IMPORT.md`. This is an original companion example from the skill-development project. Available records establish the script, native geometry, rendering and limited QA; they do not contain a separate per-skill invocation log or a verifiable language-model ID for this specific figure. Do not relabel it as a new identified-model benchmark. All geometry is DEMO, not research evidence.
