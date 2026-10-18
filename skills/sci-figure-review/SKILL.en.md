---
name: sci-figure-review
description: Review scientific semantics, visual readability and editable delivery of scientific figures within an explicit scope. Render and inspect actual outputs; automated scans do not prove scientific validity.
---

# Review scientific figures

Identify the version, claim, physical size and evidence supplied. Repair authorized layout and annotation errors directly; preserve concrete unresolved factual questions rather than imposing new approval gates.

## Inspect the real artifact
Open editable sources and exports, inspect the whole figure and its intended physical size. Read captions and directly supporting data/methods. A download, script completion or thumbnail is not full visual inspection. State which panels and assets were inspected and what data cannot be checked.

## Three separate judgments
1. Scientific semantics: object identity, layer order, connectivity, direction, axes, transformations and evidence levels; units, scales, sampling, uncertainty and repeats. A beautiful surface or significance star does not establish a mechanism.
2. Visual readability: reading order, comparison, text, lines, arrows, legends, clipping and identity across views at final size. Judge backgrounds and colors by the task, not a fixed palette.
3. Editable delivery: live text, independent objects, available image links and reproducible data plots; verify that SVG/PDF/PNG exports retain content and placement.

See [references/review-cases.md](references/review-cases.md). A pass in one category does not imply a pass in the others.

## Mechanical assistance
Use scripts/check_svg.py FIGURE.svg, optionally with a task-derived --min-label-pt. It reports some canvas, text, approximate font size, image placement, metadata and local-reference properties. It does not fetch remote assets or implement full CSS/filter/layout semantics. Read [references/svg-scan.md](references/svg-scan.md) and repository known issues, especially definitions/use instances. Render nested views and inspect font substitution rather than claiming all visible text has been certified.

## Repair, recheck, report
Prioritize misleading or hidden evidence, then spacing. Changing a scale, count, connection or experimental annotation requires a basis. Identify the missing datum if uncertain. Recheck changed areas and affected exports rather than expanding into unrelated tests.

Report substantive findings as finding, evidence, impact and repair/unresolved item. Give separate scoped conclusions for science, visuals and editability. Deliver actual revisions and previews, with physical size. State unverified statistics, mechanisms or cross-editor behavior. Do not promise journal acceptance or treat hashes, model self-assessment or scans as scientific proof. Use [references/review-report.md](references/review-report.md) as a concise guide.
