# User guide · paper-fig-skills 1.1.0

[中文](USER_GUIDE.zh.md) · [Home](../README.en.md)

## 1. What to open first

- **See the visual result:** [interdigitated contacts and buried interface](../deliverables/advanced-device-demo/README.en.md), the homepage hero, includes original Blender geometry and editable SVG annotation.
- **Browse examples:** [new gallery](../examples/gallery/README.md) covers paired distributions, structures, mechanisms, processes, heatmaps, 3D stacks, waterfalls and intersecting volume slices. All values and conceptual structures are synthetic.
- **Choose colors:** download/open [color-atlas.html](../deliverables/color-atlas.html), or view [color-atlas.svg](../deliverables/color-atlas.svg). JSON contains reusable values. Categories and continuous quantities need different encodings.
- **Study visual reasoning:** [26-page historical handbook](../deliverables/scientific-figure-handbook.pdf) and [paper atlas](../deliverables/paper-atlas.html). These retain their original Chinese research content and 2026-10-17 reading scope. This English guide and the nine English entrypoints explain operation; they are not a full translation of all historical literature notes.

GitHub previews Markdown, images and PDFs. For interactive HTML, download the repository and open the HTML locally in a browser; GitHub's normal file page displays source code. The delivered HTML contains its own analysis and fonts; source-paper links still need the internet. No GitHub Pages deployment is required.

## 2. Repository map

| Folder | Role |
|---|---|
| `skills/` | Nine stable skill IDs, Chinese and English entrypoints, references and existing helpers |
| `examples/gallery/` | New reproducible synthetic examples and their model/tool/use record |
| `deliverables/advanced-device-demo/` | Original complex device example used on the homepage |
| `deliverables/forward-test-demo/` | Original recorded forward-test example, distinct from a model benchmark |
| `deliverables/` | Historical handbook, literature/color atlases, source data and build helpers |
| `review/` | Original scoped checks, dated 2026-10-17; not new certification |
| `docs/` | Current usage guides, release notes and historical archive manifest |
| `tools/font-assets/` | Retained font-license notice; standalone fonts were not in the original archive |

## 3. Export and install one edition

From the repository root:

```sh
python scripts/export_skills.py --language en --output ../paper-fig-en
```

Use `zh` for Chinese. The destination must be new; existing files are not overwritten. Export copies complete skill directories, including references, assets and scripts. English replaces only the exported `SKILL.md`; the source Chinese entrypoint remains available as `SKILL.zh.md`. The script does not install, call a model, or change global settings.

Copy the exported nine folders into the skills root recognized by your client. The repository's existing instructions use `$HOME/.agents/skills` or Windows `$HOME\.agents\skills`; custom/older clients may differ. Compare and back up a same-name skill before updating it. Do not install both language editions under duplicate names. Preserve every supporting directory, not just the entrypoint. Refresh/restart skill discovery as needed.

A downloaded repository is not automatically an installed skill set. For a smoke test, use an invented data table rather than unpublished research.

## 4. Give the figure a useful brief

Provide the question to answer, relevant files and columns, units, sample/batch definitions, measured/modelled/proposed status, target size and required editable formats. Specify only tool constraints you actually need. The director should select a route without forcing every task into one template.

```text
Use $sci-figure-director and the relevant modules from paper-fig-skills only.
Question: Does the change occur across batches or only in a few outliers?
Inputs: my CSV, with device_id, batch_id, before, after and units.
Keep pairs, individual points and batch hierarchy. Do not fabricate values.
Final figure: 180 mm wide. Deliver SVG, PDF, PNG and reproducible code.
Read the skills before working, inspect the rendered result, and record the
actual model/effort if exposed by the runtime. State unknown otherwise.
```

If you have no data and want an example, explicitly request synthetic/demo data. Do not allow a concept sketch to acquire fabricated measurement labels or error bars.

## 5. Pick the appropriate route

- **Paired distributions:** data + color + review. Box/point/half-violin views retain raw samples and define quartiles, whiskers and KDE bandwidth. Sparse samples may not warrant a smoothed density.
- **Device:** device + compose. Supply layer/contact topology. Use a section for adjacency; add native 3D where geometry/occlusion matters. Exploded gaps and exaggerated thickness must be stated.
- **Mechanism:** mechanism. Define whether an axis is position, energy or reaction coordinate. Arrow endpoints, charge/current signs and competing routes matter more than embellishment.
- **Growth:** process + device/image as needed. Keep specimen identities and observed versus hypothetical events separate. A conceptual faceted grain is not a known crystal face.
- **Heatmaps:** data + color. Preserve common ranges, zero, masks and calibration. A diverging palette needs a meaningful center; do not silently turn missing data into zero.
- **Stacks/waterfalls:** data + image + compose. The third axis may be time/temperature, not spatial depth. Preserve real irregular condition spacing. Include unobscured 2D views for reading.
- **Volumes:** image. Retain voxel spacing, axis order and slice position. Intersecting planes need correct visibility, not just transparent overlays.
- **Mixed/unequal panels:** compose. Allocate area by the scientific comparison and keep related axes and identities aligned.

Specialized guidance is in [stacked-views.en.md](../skills/sci-figure-data/references/stacked-views.en.md). Do not load every reference for a simple task.

## 6. Reproduce the new gallery

Use a dedicated Python environment if convenient, then:

```sh
python -m pip install -r examples/gallery/requirements.txt
python examples/gallery/generate.py
python examples/gallery/check.py
```

This regenerates the eight base plots. It overwrites files only in the gallery output folder. To reproduce the approved native-3D companions and final growth composite:

```sh
blender -b -t 2 --python examples/gallery/device3d.py -- --out examples/gallery/output/device3d
python examples/gallery/compose3d.py
blender -b -t 2 --python examples/gallery/growth3d.py -- --out examples/gallery/output/growth3d
python examples/gallery/compose_growth.py
python examples/gallery/check.py
```

Run the base generator before the growth builder: it saves the shared polygon coordinates. Run the composition steps last. Blender scripts clear their fresh background scene; do not execute them in an unsaved interactive scene. Current gallery rendering was checked with Blender 4.3.2; the legacy device example records Blender 4.5.0. Native mesh objects, materials and state collections remain editable. A composite SVG contains render pixels plus independently editable labels, not a full 3D editor.

The gallery uses NumPy/Matplotlib and optionally Blender, not image-generation APIs. `run.json` records skill paths/hashes and runtime information. The language-model ID/effort was not exposed in this run and is explicitly unknown; do not market these results as an identified-model benchmark.

## 7. Use the historical resources

The original archive contained 151 files. The original 71 skill files were already imported; this update restores the complementary material rather than replacing current skills with old copies. Import mapping and version differences are recorded in [ARCHIVE_IMPORT.md](ARCHIVE_IMPORT.md).

- **Paper atlas:** use existing HTML, JSON or CSV. For a portable HTML rebuild from the shipped JSON:
  `python deliverables/rebuild_public_atlas.py --out /your/new/path/atlas.html`
  Optional font subsets are no longer required; without them the rebuild uses system fonts. The original self-contained HTML is preserved unchanged.
- **Color atlas:** values live in the color skill and delivered JSON. `make_color_atlas.py` rebuilds the delivered color files and therefore should be run in a working copy if you want to preserve the historical originals.
- **Chinese handbook:** the PDF is ready to read. The build helper requires ReportLab and appropriately licensed local CJK TTF files: `python deliverables/build_handbook.py --font-regular /actual/font.ttf --font-bold /actual/bold.ttf`. It rebuilds the PDF beside the source. Fonts are not downloaded automatically; the helper's CLI was checked, but this update did not re-typeset the historical book.
- **Legacy demos:** retain their own README and original checks. Do not relabel an accompanying example as a newly executed independent skill test. Historical model IDs are unknown unless documented.

## 8. Review and adapt

Inspect the intended physical size, not only a large screen preview. Check units, labels, sign conventions, legend meaning, object connections, sample definitions, crop, opacity and exported text. Open native sources and ensure you can regenerate quantitative layers from arrays or tables.

Automated checks support these tasks but cannot prove a material mechanism or publication readiness. Keep known limitations visible without letting a generic checklist replace the specific scientific question. Preserve raw research data when adapting a demo. Only the synthetic examples may have their invented values changed for demonstration.
