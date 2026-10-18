# Eight example topics + 3D companion / 八类案例与三维补图

**Visual review approved by the user on 2026-10-18.**

全部为模拟数据或概念结构，不是真实实验。只使用本仓库九模块体系中的相关技能，没有调用 nature-skill、其他科研绘图技能或图像生成模型。这里的“使用技能”指实际读取入口和相关参考规程，据此选择表达、编写并运行代码、检查成图；不是给普通图补贴技能标签。

## Gallery

| # | Example | Skills applied | Purpose |
|---|---|---|---|
| 01 | [Paired devices](output/01_paired.png) | director, data, color, review | 90 synthetic pairs; box + half violin + raw points |
| 02 | [Device section](output/02_device.png) | director, device, color, review | Contact order and conceptual carrier paths |
| 02b | [3D device](output/02b_device3d.png) | device, color, compose, review | Same six-layer topology, assembled and exploded; native Blender source |
| 03 | [Energy routes](output/03_energy.png) | mechanism, color, review | Separate energy coordinates and competing processes |
| 04 | [Growth states](output/04_growth.png) | process, color, review | Voronoi-domain construction with fixed seeds and an area ledger |
| 05 | [Comparative heatmaps](output/05_heatmaps.png) | data, color, compose, review | Shared signal range and signed residuals; complete synthetic data |
| 06 | [Stacked heatmap planes](output/06_heatmap_stack.png) | data, image, compose, review | Signed analytic differences; real time spacing and unobscured companion slices |
| 07 | [3D waterfall](output/07_waterfall.png) | data, color, compose, review | Actual irregular temperatures, no artificial amplitude offsets |
| 08 | [Volume and unequal panels](output/08_volume_layout.png) | image, data, compose, review | Signed volume difference, corrected slice occlusion and a centerline |

Each preview has matching SVG and PDF files in `output/`. Quantitative examples additionally save JSON arrays and coordinates. The conceptual geometry/levels/state rules are in the generator; they do not represent a particular real material. A projected SVG is editable in 2D; use code and arrays to rotate a three-dimensional plot.

## Model disclosure / 模型说明

- Execution surface: OpenAI dot cloud workspace.
- Drawing backend: Python, NumPy, Matplotlib, plus Blender Cycles for the optional 3D companion; no image-generation model.
- The current session does **not expose a verifiable underlying language-model ID or reasoning-effort value** to this run. They are recorded as `not_exposed` in `run.json`, not guessed as Astra or Sol.
- Accordingly this candidate is **not a model-specific benchmark result**. A named-model claim requires a separately verifiable task/runtime configuration before publication.
- All skill files and specific reference paths actually read are recorded with SHA-256 in `run.json`. Merely having a skill installed is not counted as use.

## Reproduce

From the repository root, in an environment of your choice:

```sh
python -m pip install -r examples/gallery/requirements.txt
python examples/gallery/generate.py
python examples/gallery/check.py
```

The script writes only under `examples/gallery/output/`. Re-running replaces its generated example files, not external research data. For a read-only home directory, set MPLCONFIGDIR and XDG_CACHE_HOME to your writable temporary directories before running. Python and library versions used here are recorded in `run.json`; only this Linux execution has been tested.

## Reusable prompt / 可复用提示词

Use only paper-fig-skills. Read sci-figure-director and the relevant specialist entrypoints/references. Generate a small set of clearly synthetic scientific examples spanning paired samples, conceptual device/energy/process diagrams, comparative heatmaps, true-condition stacked heatmap planes, a 3D waterfall and a volume-with-slices composition. Preserve sample identity, real coordinate spacing within the synthetic example, common scale semantics, missingness and editable text. Do not use real experimental or private data. Deliver code, arrays, SVG/PDF/PNG, captions and a record of skills actually used. Inspect final-size outputs and correct errors. State the verifiable model ID and effort; use unknown if not exposed. Do not publish before the user's visual approval.

## What was checked

Executed generator and numeric/export checks, inspected all eight base PNGs and the 3D companion and selected full-size exports; repaired the initial 3D text-call error, heatmap label crowding, missing-mask color, spatial aspect ratio and recombination endpoints. Existing SVG scanner tests passed separately. These checks do not validate an actual material, kinetic theory, device performance or a new scientific finding.

Remaining limits: no native commercial editor test, no Windows/macOS execution, no direct experimental evidence, no complete accessibility certification. Original repository known issues remain documented. Full-size figures are approximately 180 mm wide except the wider comparative heatmap; the code records exact dimensions. Titles and demo footers serve the example gallery and can be adjusted for an actual publication after its requirements are specified.

Heatmap pixels in examples 05 and 07 are deliberately embedded raster fields in the SVG/PDF to avoid vector-cell seam artifacts; their annotations remain editable, and all field arrays/code are retained. This is not a claim that every heatmap cell is a vector object.


## Reproduce the approved 3D companions

```sh
blender -b -t 2 --python examples/gallery/device3d.py -- --out examples/gallery/output/device3d
python examples/gallery/compose3d.py
blender -b -t 2 --python examples/gallery/growth3d.py -- --out examples/gallery/output/growth3d
python examples/gallery/compose_growth.py
python examples/gallery/check.py
```

Run generate.py first, then these composition steps last. Use a fresh background Blender scene: each builder clears its scene. Native .blend files retain named objects, materials, cameras and state collections; the composite SVG embeds render pixels with independently editable annotations. Device layer leaders come from projected right-edge anchors. The growth view is conceptual faceted geometry over fixed Voronoi footprints, not a crystallographic or kinetic model.

Example 06 uses signed differences and a red/white/blue scale centered at zero. Example 08 uses an original muted teal/neutral/coral map, also centered at zero, and one joint tiled collection for both intersecting planes. This corrects this camera's occlusion; arbitrary intersecting geometry may require a depth-buffer renderer. User reference images are not redistributed.

See [revision history](../../docs/history/gallery-revisions.md), [current guide](../../docs/USER_GUIDE.en.md) and [Chinese guide](../../docs/USER_GUIDE.zh.md).
