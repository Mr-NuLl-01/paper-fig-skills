#!/usr/bin/env python3
"""Original forward test. All numeric values are simulated DEMO values.

No package demo asset is imported. Python stdlib writes editable SVG + CSV;
Inkscape renders the SVG into PNG (see README for the two commands).
"""
import csv
import json
import math
import random
from pathlib import Path
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parent
NS = "http://www.w3.org/2000/svg"
ET.register_namespace("", NS)

COLORS = {
    "ink": "#25343B", "muted": "#5B6970", "rule": "#D8DFE1",
    "before": "#697680", "after": "#176B7B", "pair": "#9BA9AD",
    "glass": "#E7EDF0", "ITO": "#B8CED3", "active_film": "#E5C58D",
    "Au": "#BA9461", "demo": "#8B541F", "paper": "#FFFFFF",
}

def el(tag, parent, text=None, **attrs):
    obj = ET.SubElement(parent, f"{{{NS}}}{tag}", {k.replace('_', '-'): str(v) for k, v in attrs.items()})
    if text is not None:
        obj.text = str(text)
    return obj

def txt(parent, x, y, text, size=29, weight=400, color=None, anchor="start", **attrs):
    if "id" not in attrs:
        attrs["id"] = f"label-{txt.counter:03d}"
        txt.counter += 1
    return el("text", parent, text, x=x, y=y, font_size=size,
              font_weight=weight, fill=color or COLORS["ink"], text_anchor=anchor, **attrs)

txt.counter = 1

def line(parent, x1, y1, x2, y2, color=None, width=2, **attrs):
    return el("line", parent, x1=x1, y1=y1, x2=x2, y2=y2,
              stroke=color or COLORS["rule"], stroke_width=width, **attrs)

def marker(parent, x, y, condition, radius=7, **attrs):
    if condition == "before":
        return el("circle", parent, cx=x, cy=y, r=radius, fill="white",
                  stroke=COLORS["before"], stroke_width=2.7, **attrs)
    return el("path", parent,
              d=f"M {x} {y-radius-1} L {x+radius+1} {y} L {x} {y+radius+1} L {x-radius-1} {y} Z",
              fill=COLORS["after"], stroke=COLORS["after"], stroke_width=1.8, **attrs)

def root_svg(width=180, height=104, viewbox="0 0 1800 1040"):
    root = ET.Element(f"{{{NS}}}svg", {
        "width": f"{width}mm", "height": f"{height}mm", "viewBox": viewbox,
        "font-family": "DejaVu Sans, sans-serif", "font-size": "29",
        "version": "1.1",
    })
    return root

def write_svg(root, path):
    ET.indent(root, space="  ")
    ET.ElementTree(root).write(path, encoding="utf-8", xml_declaration=True)

def generate_data():
    rng = random.Random(2601017)
    rows = []
    p0 = [0.86, 0.99, 1.12, 1.25, 1.38]
    bw0 = [20.0, 16.8, 13.3, 9.3, 6.9]
    dp = [0.19, 0.13, 0.08, -0.09, 0.15]
    dbw = [-1.8, -1.5, -1.2, 0.9, 0.8]
    for batch, (poffset, boffset) in enumerate([(-0.03, 0), (0.02, 0.4), (0.07, -0.6)], 1):
        for device in range(1, 6):
            p = round(p0[device-1] + poffset + rng.uniform(-0.012, 0.012), 3)
            b = round(bw0[device-1] + boffset + rng.uniform(-0.15, 0.15), 3)
            pa = round(p + dp[device-1] + rng.uniform(-0.012, 0.012), 3)
            ba = round(b + dbw[device-1] + rng.uniform(-0.15, 0.15), 3)
            for condition, perf, bandwidth in [("before", p, b), ("after", pa, ba)]:
                rows.append({
                    "sample_id": f"B{batch}-D{device:02d}", "batch_id": f"B{batch}",
                    "condition": condition, "measurement_type": "DEMO simulated endpoint",
                    "performance_index_au": perf, "bandwidth_MHz": bandwidth,
                    "provenance": "DEMO; not measured", "independent_unit": "device",
                    "pairing": "same device, assumed for DEMO", "test_conditions": "unknown",
                    "bandwidth_definition": "unknown; numeric range only for DEMO",
                })
    with (ROOT / "demo_data.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return rows

def make_sketches():
    root = root_svg(180, 90, "0 0 1800 900")
    txt(root, 40, 55, "DEMO | two layout routes considered", 37, 600)
    txt(root, 40, 110, "A — compact context + batch facets (selected)", 31, 600)
    x, y = 40, 150
    for i, (w, h, label) in enumerate([(350, 260, "layer context"), (420, 260, "batch 1"), (420, 260, "batch 2"), (420, 260, "batch 3")]):
        el("rect", root, x=x, y=y, width=w, height=h, fill="#F4F7F7", stroke="#9BA9AD")
        txt(root, x+20, y+50, label, 28)
        x += w + 25
    txt(root, 40, 475, "B — context strip + one pooled tradeoff scatter", 31, 600)
    el("rect", root, x=40, y=510, width=1720, height=90, fill="#F4F7F7", stroke="#9BA9AD")
    txt(root, 60, 565, "layers + qualitative evidence boundary", 28)
    el("rect", root, x=40, y=625, width=1720, height=220, fill="#F4F7F7", stroke="#9BA9AD")
    txt(root, 60, 680, "15 paired vectors; batch needs a second visual code", 28)
    txt(root, 60, 730, "Rejected: pooled paths cross and dilute batch identity.", 28)
    write_svg(root, ROOT / "layout_routes.svg")

def make_figure(rows, config):
    root = root_svg()
    el("title", root, "DEMO paired performance–bandwidth tradeoff across three batches")
    el("desc", root, "All plotted numbers are simulated, not measured. Three batches, five independent devices each, with before and after endpoints. Layer schematic is not to scale. Carrier transfer rate is unmeasured.")
    el("metadata", root, json.dumps(config, ensure_ascii=False))
    el("rect", root, x=0, y=0, width=1800, height=1040, fill="white", id="paper")
    defs = el("defs", root)
    am = el("marker", defs, id="paired-arrowhead", viewBox="0 0 10 10", refX=8, refY=5,
            markerWidth=4.4, markerHeight=4.4, orient="auto-start-reverse", markerUnits="strokeWidth")
    el("path", am, d="M 0 1 L 9 5 L 0 9 Z", fill=COLORS["pair"])

    header = el("g", root, id="title-and-study-design")
    txt(header, 40, 58, "DEMO", 36, 700, COLORS["demo"])
    txt(header, 190, 58, "Paired performance–bandwidth tradeoff", 36, 600)
    txt(header, 40, 108, "3 batches × 5 independent devices  |  Before/after pairing assumed for this DEMO", 29, color=COLORS["muted"])
    line(header, 40, 139, 1760, 139)

    context = el("g", root, id="panel-a-layer-context")
    txt(context, 40, 192, "a", 35, 700)
    txt(context, 84, 192, "Layer context", 31, 600)
    txt(context, 40, 242, "Layer order only", 28, color=COLORS["muted"])
    # Bottom-up layer list; physical thickness unknown, display thickness arbitrary.
    layers = [("glass", 385, 98), ("ITO", 358, 27), ("active_film", 304, 54), ("Au", 280, 24)]
    labels = {"glass": "glass", "ITO": "ITO", "active_film": "active film", "Au": "Au"}
    for name, y, h in layers:
        group = el("g", context, id=f"layer-{name}")
        el("rect", group, x=43, y=y, width=174, height=h, fill=COLORS[name], stroke="#53616A", stroke_width=1.5)
        ym = y+h/2
        line(group, 220, ym, 245, ym, COLORS["muted"], 1.8)
        # Label baselines spaced independently of exaggerated display thickness.
        label_y = {"Au": 290, "active_film": 335, "ITO": 382, "glass": 440}[name]
        if abs(label_y-9-ym) > 8:
            line(group, 245, ym, 255, label_y-9, COLORS["muted"], 1.8)
        txt(group, 263, label_y, labels[name], 28)
    txt(context, 40, 535, "Not to scale", 28, color=COLORS["muted"])
    txt(context, 40, 574, "All thicknesses unknown", 28, color=COLORS["muted"])

    evidence = el("g", context, id="qualitative-evidence-boundary")
    line(evidence, 40, 625, 405, 625)
    txt(evidence, 40, 668, "Qualitative evidence", 27, 600)
    txt(evidence, 40, 710, "Steady-state spectrum", 26)
    txt(evidence, 40, 744, "changes; stability improves", 26)
    txt(evidence, 40, 798, "Transfer rate:", 27, 600, COLORS["demo"])
    txt(evidence, 40, 835, "unmeasured", 27, 600, COLORS["demo"])

    legend = el("g", root, id="condition-and-pair-legend")
    marker(legend, 530, 249, "before", 8)
    txt(legend, 552, 258, "Before", 28)
    marker(legend, 720, 249, "after", 8)
    txt(legend, 742, 258, "After", 28)
    line(legend, 910, 249, 967, 249, COLORS["pair"], 2.7, marker_end="url(#paired-arrowhead)")
    txt(legend, 985, 258, "Same device", 28)

    px = [520, 950, 1380]
    py, pw, ph = 315, 345, 405
    xmin, xmax, ymin, ymax = .7, 1.7, 6., 22.
    def project(i, p, b):
        return px[i] + (p-xmin)/(xmax-xmin)*pw, py + ph - (b-ymin)/(ymax-ymin)*ph
    for i in range(3):
        batch = f"B{i+1}"
        facet = el("g", root, id=f"panel-{chr(98+i)}-batch-{i+1}")
        txt(facet, px[i]-24, 192, chr(98+i), 35, 700)
        txt(facet, px[i]+20, 192, f"Batch {i+1}", 31, 600)
        txt(facet, px[i]+pw, 192, "n = 5", 27, color=COLORS["muted"], anchor="end")
        axes = el("g", facet, id=f"axes-{batch}")
        for b in [6, 10, 14, 18, 22]:
            _, yp = project(i, xmin, b)
            if b != 6:
                line(axes, px[i], yp, px[i]+pw, yp, "#E8EDEE", 1.5)
            line(axes, px[i]-8, yp, px[i], yp, COLORS["muted"], 1.8)
            txt(axes, px[i]-17, yp+10, b, 27, anchor="end", color=COLORS["muted"])
        for p in [.8, 1.2, 1.6]:
            xp, _ = project(i, p, ymin)
            line(axes, xp, py+ph, xp, py+ph+8, COLORS["muted"], 1.8)
            txt(axes, xp, py+ph+42, f"{p:.1f}", 27, anchor="middle", color=COLORS["muted"])
        line(axes, px[i], py, px[i], py+ph, COLORS["muted"], 1.8)
        line(axes, px[i], py+ph, px[i]+pw, py+ph, COLORS["muted"], 1.8)
        pairs = el("g", facet, id=f"paired-device-trajectories-{batch}")
        for j in range(1, 6):
            sid = f"{batch}-D{j:02d}"
            d = [row for row in rows if row["sample_id"] == sid]
            before, after = d
            x0, y0 = project(i, before["performance_index_au"], before["bandwidth_MHz"])
            x1, y1 = project(i, after["performance_index_au"], after["bandwidth_MHz"])
            pair = el("g", pairs, id=f"device-{sid}", data_sample_id=sid)
            el("title", pair, f"{sid}: before {before['performance_index_au']} a.u., {before['bandwidth_MHz']} MHz; after {after['performance_index_au']} a.u., {after['bandwidth_MHz']} MHz. DEMO.")
            # Trim the line at each endpoint so its arrowhead does not cover the after marker.
            dx, dy = x1-x0, y1-y0
            dist = math.hypot(dx, dy)
            ux, uy = dx/dist, dy/dist
            line(pair, x0+ux*10, y0+uy*10, x1-ux*11, y1-uy*11, COLORS["pair"], 2.5,
                 marker_end="url(#paired-arrowhead)", id=f"pair-{sid}")
            marker(pair, x0, y0, "before", 7.2, id=f"before-{sid}")
            marker(pair, x1, y1, "after", 7.2, id=f"after-{sid}")

    ann = el("g", root, id="shared-data-axis-labels")
    txt(ann, 445, 518, "Bandwidth (MHz; DEMO)", 29, anchor="middle", transform="rotate(-90 445 518)")
    txt(ann, 1120, 811, "Performance index (a.u.; DEMO)", 30, anchor="middle")
    txt(ann, 1120, 857, "Higher values preferred on both axes by DEMO definition", 26, color=COLORS["muted"], anchor="middle")

    footer = el("g", root, id="caption-and-simulation-warning")
    line(footer, 40, 893, 1760, 893)
    txt(footer, 40, 943, "DEMO ONLY — every plotted number is simulated; no experimental result is shown.", 29, 600, COLORS["demo"])
    txt(footer, 40, 987, "Each arrow joins the same device before → after; panels share axis limits. No kinetic mechanism is inferred.", 27, color=COLORS["muted"])
    write_svg(root, ROOT / "demo_performance_bandwidth.svg")

def main():
    rows = generate_data()
    config = {
        "status": "DEMO — NOT RESEARCH RESULTS",
        "claim": "Demonstrate how batch-resolved paired data expose performance–bandwidth tradeoffs.",
        "canvas_mm": [180, 104],
        "layout": "compact layer context plus three equal-scale batch facets",
        "independent_devices": 15, "batches": 3, "devices_per_batch": 5,
        "numeric_source": "deterministic invented endpoints, random seed 2601017",
        "pairing": "before/after on same device, assumed for DEMO",
        "statistical_operations": "none; no fit, mean, error bar, p value, or pooled test",
        "display_transforms": "linear axes; source endpoints rounded to 3 decimals; no values removed",
        "unknown": ["physical performance metric", "actual numeric values", "measurement conditions", "bandwidth cutoff definition", "all physical layer thicknesses", "carrier-transfer rate"],
        "qualitative_user_evidence": ["steady-state spectrum changes", "stability improves"],
        "mechanism_route": "No carrier-transfer arrows or rate claim; state unmeasured boundary explicitly.",
        "layers_bottom_to_top": ["glass", "ITO", "active film", "Au"],
        "schematic_scale": "not to scale; display thicknesses arbitrary; physical thicknesses unknown",
        "color_scopes": {
            "conditions": {"before": {"color": COLORS["before"], "shape": "open circle"}, "after": {"color": COLORS["after"], "shape": "filled diamond"}},
            "material_identity_only": {k: COLORS[k] for k in ["glass", "ITO", "active_film", "Au"]},
            "pairing": {"color": COLORS["pair"], "meaning": "within-device condition order, not physical transport"},
        },
        "font_family": "DejaVu Sans, sans-serif", "font_sizes_viewbox_units": [26, 27, 28, 29, 30, 31, 35, 36],
        "main_file": "demo_performance_bandwidth.svg", "source_data": "demo_data.csv", "generator": "make_figure.py",
        "external_assets": [], "author_software": "unknown; this original draft uses Python stdlib + Inkscape",
    }
    (ROOT / "design_config.json").write_text(json.dumps(config, ensure_ascii=False, indent=2)+"\n")
    make_sketches()
    make_figure(rows, config)
    print(f"Wrote {len(rows)} simulated endpoints for 15 devices and editable SVG in {ROOT}")

if __name__ == "__main__":
    main()
