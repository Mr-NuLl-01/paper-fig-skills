#!/usr/bin/env python3
"""Reproducible structure/resource/metadata and SVG mechanical inventory.

This does not visually review every demo or validate their scientific claims.
The official quick_validate.py is invoked read-only, without modification.
"""
import datetime
import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
OUT = ROOT / "review"
VALIDATOR = Path("/root/.codex/skills/oai/skill-creator/scripts/quick_validate.py")
SCANNER = SKILLS / "sci-figure-review/scripts/check_svg.py"

def command(args):
    run = subprocess.run([str(x) for x in args], capture_output=True, text=True)
    return {"argv": [str(x) for x in args], "returncode": run.returncode,
            "stdout": run.stdout.strip(), "stderr": run.stderr.strip()}

def md_link_inventory(skill):
    links, code_resources = [], []
    for source in sorted(skill.rglob("*.md")):
        text = source.read_text()
        for m in re.finditer(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+[^)]*)?\)", text):
            target = m.group(1).strip("<>")
            uri = urlsplit(target)
            if uri.scheme or uri.netloc or not uri.path:
                continue
            dest = (source.parent / unquote(uri.path)).resolve()
            links.append({"source": str(source.relative_to(ROOT)), "target": target,
                          "resolved": str(dest), "exists": dest.exists(),
                          "within_same_skill": dest.is_relative_to(skill)})
        # Skill-root resource paths in prose/commands are also checked. Example
        # placeholder filenames and DOI tokens do not match this resource grammar.
        # Markdown links were resolved above; exclude example JSON manifests
        # and avoid interpreting a suffix of a cross-skill path as local.
        mentions = re.sub(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+[^)]*)?\)", "", text)
        mentions = re.sub(r"```json\s*\n.*?```", "", mentions, flags=re.S)
        for token in sorted(set(re.findall(r"(?<![A-Za-z0-9_./-])(?:scripts|references|assets|agents)/[A-Za-z0-9_./-]+\.[A-Za-z0-9]+", mentions))):
            dest = (skill / token).resolve()
            code_resources.append({"source": str(source.relative_to(ROOT)), "target": token,
                                   "resolved": str(dest), "exists": dest.exists()})
    return links, code_resources

def main():
    skills = sorted(p for p in SKILLS.iterdir() if p.is_dir() and (p / "SKILL.md").is_file())
    validations, metadata, links, code_resources = [], [], [], []
    for skill in skills:
        validations.append({"skill": skill.name, **command([sys.executable, VALIDATOR, skill])})
        fm = yaml.safe_load(skill.joinpath("SKILL.md").read_text().split("---", 2)[1])
        raw = skill.joinpath("agents/openai.yaml").read_text()
        agents = yaml.safe_load(raw)
        ui = agents.get("interface", {})
        checks = {
            "folder_matches_frontmatter_name": skill.name == fm.get("name"),
            "display_name_present": isinstance(ui.get("display_name"), str) and bool(ui["display_name"].strip()),
            "short_description_length_25_to_64": isinstance(ui.get("short_description"), str) and 25 <= len(ui["short_description"]) <= 64,
            "default_prompt_mentions_correct_skill_id": isinstance(ui.get("default_prompt"), str) and re.search(r"\$" + re.escape(skill.name) + r"(?![a-z0-9-])", ui["default_prompt"]) is not None,
            "all_interface_strings_double_quoted": all(re.search(r"^\s+"+re.escape(k)+r':\s+".*"\s*$',raw,re.M) is not None for k,v in ui.items() if isinstance(v,str)),
        }
        metadata.append({"skill": skill.name, "interface": ui, "checks": checks})
        local_links, resources = md_link_inventory(skill)
        links.extend(local_links)
        code_resources.extend(resources)
    names = [m["interface"]["display_name"] for m in metadata]
    unique_display_names = len(names) == len(set(names))
    tests = command([sys.executable, SKILLS / "sci-figure-review/scripts/test_check_svg.py"])
    demo_results = []
    for svg in sorted(SKILLS.glob("*/assets/demo/*.svg")):
        result = command([sys.executable, SCANNER, svg])
        if result["returncode"] == 0:
            result["inventory"] = json.loads(result.pop("stdout"))
        demo_results.append({"svg": str(svg.relative_to(ROOT)), **result})
    missing = [r for r in links + code_resources if not r["exists"]]
    failed_metadata = [m["skill"] for m in metadata if not all(m["checks"].values())]
    findings = [{"svg": d["svg"], "findings": d.get("inventory",{}).get("findings",[]),
                 "uncertainties":d.get("inventory",{}).get("uncertainties",[])}
                for d in demo_results if d.get("inventory",{}).get("findings") or d.get("inventory",{}).get("uncertainties")]
    report = {
        "generated_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "scope": "All nine skill packages: official frontmatter validation, local Markdown/resource references, agents metadata, seven SVG-scanner contract tests and mechanical inventories of every current bundled demo SVG. Not a visual or scientific review of all demos.",
        "validator": str(VALIDATOR), "skill_count": len(skills),
        "official_validation": validations, "agents_metadata": metadata,
        "display_names_unique": unique_display_names,
        "relative_markdown_links": links, "skill_root_resource_mentions": code_resources,
        "scanner_contract_tests": tests, "bundled_demo_svg_mechanical_scans": demo_results,
        "summary": {"official_passed": sum(v["returncode"] == 0 for v in validations),
                    "agents_failed": failed_metadata, "relative_markdown_links_count": len(links),
                    "skill_root_resource_mentions_count": len(code_resources), "missing_local_references": missing,
                    "bundled_demo_svg_count": len(demo_results), "demo_scans_nonzero_exit": [d["svg"] for d in demo_results if d["returncode"]],
                    "demo_scan_flags": findings},
        "exact_edits": [
            {"file":"skills/sci-figure-compose/SKILL.md", "section":"2. 用读序选择布局", "change":"Limit two-layout comparison to complex composites, uncertain reading order or re-layout; allow clear single panels to proceed with a reason."},
            {"file":"skills/sci-figure-compose/references/layout-strategies.md", "section":"C03", "change":"Separate Day5/10/14 same-day matrix, panel m three conditions, and panel n Drop D7 vs OCTOPUS D14 extended-culture comparison; preserve day/condition per panel."},
            {"file":"skills/sci-figure-compose/references/examples.md", "section":"多条件显微结果 验收", "change":"Require panel-specific day/condition and warn that C03 later functional comparison is not matched-age."},
            {"file":"skills/sci-figure-compose/references/editable-production.md", "section":"final paragraph", "change":"Replace nonresolving review/scripts/check_svg.py prose path with actual ../../sci-figure-review/scripts/check_svg.py Markdown link."},
            {"file":"skills/sci-figure-review/scripts/check_svg.py", "section":"embedded base64 decode", "change":"Strip only ASCII whitespace inserted by SVG exporters before strict base64 validation, fixing the false invalid_data_uri on the actual Matplotlib tradeoff demo."},
            {"file":"skills/sci-figure-review/scripts/test_check_svg.py", "section":"SVGScanContract", "change":"Add wrapped/whitespace base64 acceptance and nonwhitespace-corruption rejection tests; seven contract tests total."},
            {"file":"skills/sci-figure-review/references/svg-scan.md", "section":"实际计算", "change":"Document ASCII-whitespace normalization and continued strict validation of other base64 characters."},
        ],
        "forward_test_coverage": {"path":"review/forward-test", "actual_modules":["sci-figure-director","sci-figure-data","sci-figure-device","sci-figure-mechanism","sci-figure-compose","sci-figure-color","sci-figure-review"], "module_count":7, "actual_visual_checks":"one original optoelectronic-device DEMO figure, full PNG/reduced PNG/grayscale", "not_covered":"process and image task routes; full scientific or visual review of all bundled demos; alternate editor import"},
        "observed_before_fixes":[
            {"location":"skills/sci-figure-compose/SKILL.md:layout rule", "finding":"Two-layout comparison was unconditional despite director allowing simple single panels to proceed directly."},
            {"location":"skills/sci-figure-compose/references/layout-strategies.md:C03", "finding":"Case summary did not preserve Fig2 later-panel age conditions; checked against local figure_02_full.png and article.html figure#F2."},
            {"location":"skills/sci-figure-compose/references/editable-production.md", "finding":"review/scripts/check_svg.py prose path did not resolve to a bundled resource."},
            {"location":"skills/sci-figure-data/assets/demo/demo-tradeoff.svg", "finding":"Actual exported embedded PNG has ASCII whitespace after data:image/png;base64,; old scanner emitted invalid_data_uri: Only base64 data is allowed."},
        ],
        "not_changed":["color script", "raw C03 corpus record (handled by corpus_opto)", "installed skills", "official validator"],
    }
    OUT.joinpath("skill_validation.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps(report["summary"],ensure_ascii=False,indent=2))
    print(f"Contract tests exit: {tests['returncode']}; display names unique: {unique_display_names}")
    demo_errors = [f for d in demo_results for f in d.get("inventory",{}).get("findings",[]) if f.get("level")=="error"]
    return 0 if all(v["returncode"]==0 for v in validations) and not missing and not failed_metadata and unique_display_names and tests["returncode"]==0 and not any(d["returncode"] for d in demo_results) and not demo_errors else 1

if __name__ == "__main__":
    raise SystemExit(main())
