# Original archive import / 原归档导入

Source: the user's `science-figure-atlas-complete.zip`, 2026-10-17, 12,462,322 bytes.
SHA-256: `51fe54cd16dba5d17d931995e7a42349c5ee723f2a0dbf3fa90c63c9fd222553`.

The ZIP has 151 members. Its manifest covers the other 150 files; all sizes and SHA-256 values were checked before import. The original manifest is retained at `docs/history/archive-manifest-20261017.json`, and the original archive README at `docs/history/archive-readme-20261017.md`. They describe the historical archive, not the current installation path or release state.

## Mapping

- `skills/`: already imported as 71 original files in the prior GitHub commit; current edits and English entrypoints are retained, not overwritten by older copies.
- `deliverables/`, `review/`, `tools/`: restored at the same relative paths to preserve supporting-resource relationships.
- Original root README and manifest: retained under `docs/history/` to avoid conflicting with current navigation and release manifest.
- No paper PDFs, journal figures, private experimental data, machine environments or standalone font binaries are added.

## Historical versus current claims

The literature counts, reading scope and review files remain the original project's records. This update verified archive identity and packaging; it did not reread 89 papers or rerun the original scientific assessments. The archived PDF is the later 26-page version described by the archive manifest; an older `source-inventory.json` entry is a historical snapshot, not its current hash authority.

The homepage hero is the original advanced-device companion example. Its script/native/QA records exist, but no separate skill-invocation or model-ID log for that figure is supplied. The forward-test README records seven skill modules and a from-scratch exercise; that is the original report, not a fresh run by this release. Current gallery skill-use/model metadata is separate.

## Narrow portability changes

- `build_paper_atlas.py`: optional CJK font subset now falls back to system fonts if absent. The existing self-contained HTML stays unchanged. `rebuild_public_atlas.py` successfully rebuilt all 89 records to a separate test output.
- `build_handbook.py`: accepts explicit `--font-regular` and optional `--font-bold` rather than assuming missing machine-specific font files. CLI help was checked; the historical PDF was not rebuilt.

Original imports otherwise preserve their source content. User-supplied reference screenshots used for the new gallery are not redistributed. Font license notices remain alongside the archived tools. See the release manifest for current repository bytes; the old archive manifest is only for the original archive.

中文摘要：此次找回完整151文件归档，按原目录补齐手册、论文/配色图谱、增强DEMO和验证记录。保留新技能改动，不覆盖回旧版本；原文献阅读与旧验证不冒称本轮完成。修正两处字体路径易用性问题，其他原始资料保留来源和日期。
