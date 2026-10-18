#!/usr/bin/env python3
"""Assemble the reviewed corpus without changing its underlying reading records."""
from __future__ import annotations

import copy
import base64
import csv
import hashlib
import html
import json
import re
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

BASE = Path(__file__).resolve().parents[1]
OUT = BASE / "deliverables"
REF = BASE / "skills/sci-figure-director/references"
ACCESS_DATE = "2026-10-17"
TIERS = {
    "main_narrative": "主文通读",
    "targeted_figure_read": "图导向定向精读",
}
TIER_DEFS = {
    "main_narrative": "连续阅读主文科学论证与结语；不自动包含全部Methods或SI，具体范围保留在read_scope。",
    "targeted_figure_read": "精读已看图对应的主文设计、机制或验证段落；未将其余全部主文记为已通读。",
}
JOURNAL_ALIASES = {
    "Nat Commun": "Nature Communications",
    "Sci Adv": "Science Advances",
    "PNAS": "Proceedings of the National Academy of Sciences",
    "Proc Natl Acad Sci U S A": "Proceedings of the National Academy of Sciences",
    "Proceedings of the National Academy of Sciences of the United States of America":
        "Proceedings of the National Academy of Sciences",
}
CATEGORY_IDS = [
    ("发光材料与LED", [f"A{i:02}" for i in [1, 2, 3, 4, 14, 15, 16, 17, 18, 20, 21, 22]]),
    ("光电探测、晶体管与神经器件", [f"A{i:02}" for i in [5, 6, 7, 8, 9, 10, 11, 12, 13, 19, 23, 24]]),
    ("成核、生长与材料加工", [f"B{i:02}" for i in range(1, 17)]),
    ("催化与电池原位表征", [f"B{i:02}" for i in range(17, 25)]),
    ("微流控、类器官与组织芯片", [f"C{i:02}" for i in range(1, 9)]),
    ("可穿戴与植入式生物电子", [f"C{i:02}" for i in range(9, 15)]),
    ("软体机器人与致动", [f"C{i:02}" for i in [15, 16, 17, 18, 21, 24]]),
    ("水凝胶与生物黏附", [f"C{i:02}" for i in [19, 20, 22, 23]]),
    ("科学计算、动力学与理论", [f"D{i:02}" for i in [1, 2, 3, 9, 10, 11, 16, 17, 18]]),
    ("成像、光谱与结构解析", [f"D{i:02}" for i in [5, 6, 7, 8, 12, 14, 19, 20]]),
]
CATEGORIES = {pid: cat for cat, ids in CATEGORY_IDS for pid in ids}
ANALYSIS_FIELDS = [
    ("science_story", "科学任务与主张"),
    ("composition", "构图与阅读路径"),
    ("color_observation", "颜色观察与语义"),
    ("visual_form", "表现形式"),
    ("strengths", "呈现优点"),
    ("limitations", "局限与误读风险"),
    ("reconstruction_route", "建议绘图与重建路线"),
    ("software_evidence", "作者实际软件证据"),
    ("transferable_rule", "可迁移规则"),
]
BOUNDARIES = [
    "89篇为本项目实际审读的原始研究样本，DOI各不相同；不是系统综述的穷尽检索，也不代表截至访问日的全部最新研究。",
    "178张为实际查看过的关键整图，每篇2张；不表示已经目视核验论文内全部图像。",
    "66篇主文通读，23篇图导向定向精读。原始read_scope、sections_read及已登记的Methods/SI限制逐篇保留；未宣称全部Methods或SI已读。",
    "优点、局限与迁移规则是针对所读范围及已看图像的设计分析，不等同于独立复现实验、证明科学结论或期刊统一风格规范。",
    "建议工具与重建路线是本项目的建议。没有确切来源时作者实际绘图软件记为unknown；局部软件署名不外推到整图。",
    "不内嵌第三方论文图像，不分发论文全文或原文图注。仅保留文献元数据、阅读范围、自己的视觉分析和原始来源链接。",
]


def dump_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def source_links(record: dict) -> list[str]:
    urls = [record["url"], "https://doi.org/" + record["doi"]]
    for ref in record.get("source_refs", []):
        if isinstance(ref, str) and ref.startswith(("https://", "http://")):
            urls.append(ref)
        elif isinstance(ref, dict) and ref.get("url"):
            urls.append(ref["url"])
    return list(dict.fromkeys(urls))


def portable(value: object) -> object:
    """Remove machine paths, while retaining our analysis and original read_scope."""
    if isinstance(value, list):
        return [portable(v) for v in value]
    if isinstance(value, dict):
        return {
            k: portable(v) for k, v in value.items()
            if not (k in {"local_path", "evidence_dir", "main_text_local_path"}
                    or (isinstance(k, str) and k.endswith("_local_path")))
        }
    if isinstance(value, str) and value.startswith(("/workspace/", "/tmp/", "/root/")):
        return "[local evidence path omitted]"
    return value


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def prose(value: object) -> str:
    if isinstance(value, dict):
        return '<dl class="nested">' + "".join(
            f"<dt>{esc(k)}</dt><dd>{prose(v)}</dd>" for k, v in value.items()
        ) + "</dl>"
    if isinstance(value, list):
        return "<ul>" + "".join(f"<li>{prose(v)}</li>" for v in value) + "</ul>"
    if isinstance(value, bool):
        return "是" if value else "否"
    return "<p>" + esc(value).replace("\n", "<br>") + "</p>"


def link(url: str, label: str, cls: str = "") -> str:
    return (f'<a class="{esc(cls)}" href="{esc(url)}" target="_blank" '
            f'rel="noopener noreferrer">{esc(label)}<span class="sr-only">（外部链接）</span></a>')


def fig_label(number: object) -> str:
    text = str(number)
    return text if text.lower().startswith(("fig", "图")) else "图 " + text


def card(record: dict) -> str:
    r = record
    haystack = " ".join(str(r.get(k, "")) for k in [
        "id", "title", "doi", "domain", "science_story", "composition", "color_observation",
        "visual_form", "strengths", "limitations", "transferable_rule", "skill_tags", "journal",
    ]).lower()
    blocks = []
    for key, label in ANALYSIS_FIELDS:
        special = " featured" if key in {"science_story", "transferable_rule"} else ""
        blocks.append(f'<section class="analysis-block{special}"><h4>{label}</h4>{prose(r[key])}</section>')
    figs = []
    for figure in r["figures_viewed"]:
        version = figure.get("version", "")
        figs.append('<section class="figure-note"><h4>' +
                    link(figure["url"], fig_label(figure["number"]) + " · 原始图像/图页链接") +
                    '</h4>' + prose(figure["visual_notes"]) +
                    (f'<p class="muted">版本：{esc(version)}</p>' if version else "") + '</section>')
    readextras = []
    for key, label in [
        ("methods_read", "Methods记录"),
        ("supplementary_information_read", "Supplementary Information记录"),
        ("supplement_read", "Supplementary Information记录"),
        ("version_note", "版本说明"),
        ("source_version", "来源版本"),
        ("software_notes", "软件补充说明"),
    ]:
        if key in r:
            readextras.append(f'<h5>{label}</h5>{prose(r[key])}')
    sources = " ".join(link(url, f"来源 {i + 1}", "source-link") for i, url in enumerate(r["source_links"]))
    tags = " ".join(f'<span class="tag">{esc(tag)}</span>' for tag in r.get("skill_tags", []))
    return f'''<article class="paper" id="{esc(r['id'])}" data-category="{esc(r['category'])}"
      data-tier="{esc(r['read_tier'])}" data-journal="{esc(r['journal'])}" data-year="{r['year']}"
      data-search="{esc(haystack)}">
      <details class="paper-details">
        <summary><span class="paper-id">{esc(r['id'])}</span><span class="paper-heading">
          <span class="paper-title">{esc(r['title'])}</span>
          <span class="paper-meta">{esc(r['journal'])} · {r['year']} · {esc(r['domain'])}</span>
          </span><span class="tier {esc(r['read_tier'])}">{esc(r['read_tier_label'])}</span></summary>
        <div class="paper-body">
          <div class="record-links">{link(r['url'], '论文原始来源', 'button-link')} {link('https://doi.org/' + r['doi'], r['doi'], 'doi-link')}
          <span class="muted">访问：{esc(r['access_date'])}</span></div>
          <p class="category-line">类别：{esc(r['category'])}</p>
          <div class="analysis-grid">{''.join(blocks)}</div>
          <section class="figures"><h3>实际查看的两张整图</h3><p class="muted">本页展示自己的观察记录；第三方图像通过原始链接访问。</p>
            <div class="figure-grid">{''.join(figs)}</div></section>
          <details class="read-details"><summary>阅读范围、版本与来源</summary>
            <p>{esc(TIER_DEFS[r['read_tier']])}</p><h5>原始阅读范围（保留原值）</h5>{prose(r['read_scope'])}
            <h5>已登记阅读章节</h5>{prose(r['sections_read'])}{''.join(readextras)}
            <h5>直接来源链接</h5><div class="sources">{sources}</div>
          </details><div class="tags" aria-label="图像方法标签">{tags}</div>
        </div>
      </details>
    </article>'''


CSS = r'''
:root{--ink:#202c3a;--muted:#617080;--line:#d9e1e5;--paper:#fff;--bg:#f3f5f6;--accent:#316b6e;--accent-light:#e2efee;--violet:#65548e;--violet-light:#eeebf5;--shadow:0 3px 16px #263e4b08}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.8 "Atlas CJK",system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans CJK SC","Microsoft YaHei",sans-serif}a{color:#265f79;text-decoration-thickness:1px;text-underline-offset:3px}a:hover{color:#143f55}button,input,select{font:inherit}button{cursor:pointer}a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible,summary:focus-visible{outline:3px solid #be8d32;outline-offset:3px}.wrap{width:min(1220px,calc(100% - 56px));margin:auto}.masthead{padding:58px 0 35px;background:#eaf0f0;border-bottom:1px solid #d5e0e0}.eyebrow{color:var(--accent);font-size:12px;font-weight:750;letter-spacing:.15em}h1{font-size:clamp(30px,4vw,49px);line-height:1.3;letter-spacing:-.035em;margin:15px 0 20px;font-weight:750}.intro{max-width:840px;font-size:17px;color:#415463}.intro p{margin:.5em 0}.meta-row{display:flex;flex-wrap:wrap;gap:9px 24px;margin-top:22px;font-size:13px;color:var(--muted)}.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:18px;margin:28px 0}.stat{background:var(--paper);padding:20px 24px;border:1px solid var(--line);border-radius:12px;box-shadow:var(--shadow)}.stat strong{display:block;font-size:37px;line-height:1.25;font-variant-numeric:tabular-nums;letter-spacing:-.04em}.stat span{font-size:13px;color:var(--muted)}.stat.full strong{color:var(--accent)}.stat.targeted strong{color:var(--violet)}.scope{background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:22px 26px}.scope h2,.statistics h2{font-size:18px;margin:0 0 8px}.scope p{margin:.6em 0}.scope summary{font-weight:650;cursor:pointer}.scope ul{padding-left:23px;margin:10px 0}.tierbar{height:8px;display:flex;overflow:hidden;border-radius:8px;margin:18px 0 8px}.tierbar .full{background:var(--accent)}.tierbar .targeted{background:var(--violet)}.tierlegend{display:flex;justify-content:space-between;flex-wrap:wrap;font-size:12px;color:var(--muted)}.statistics{margin:24px 0;background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:20px 26px}.statistics summary{font-weight:650;cursor:pointer}.stat-tables{display:grid;grid-template-columns:1.5fr 1fr;gap:28px}table{border-collapse:collapse;width:100%;margin:10px 0;font-size:13px}caption{text-align:left;font-weight:650;margin:8px 0}th,td{text-align:left;border-bottom:1px solid #e9edef;padding:7px 6px}th:last-child,td:last-child{text-align:right;font-variant-numeric:tabular-nums}.toolbar{position:sticky;top:0;z-index:10;padding:15px 0 12px;background:#f3f5f6f5;backdrop-filter:blur(12px);border-bottom:1px solid var(--line);margin-top:28px}.filters{display:grid;grid-template-columns:minmax(240px,2fr) 1.2fr 1fr;gap:14px}.filter label{display:block;font-size:12px;font-weight:650;color:#526475;margin-bottom:4px}input,select{width:100%;padding:10px 12px;border:1px solid #c4d0d6;border-radius:7px;background:#fff;color:var(--ink);min-height:45px}input::placeholder{color:#83929f}.actions{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-top:11px}.actions button{border:1px solid #c8d5da;border-radius:6px;background:#fff;color:#354d5c;padding:5px 11px;font-size:12px}.result-count{margin-right:auto;font-size:13px;font-weight:650}main{padding:24px 0 50px}.paper{background:var(--paper);border:1px solid var(--line);border-radius:10px;margin:0 0 12px;box-shadow:var(--shadow);scroll-margin-top:190px}.paper[hidden]{display:none}.paper-details>summary{display:flex;align-items:flex-start;gap:15px;cursor:pointer;list-style:none;padding:20px 22px}.paper-details>summary::-webkit-details-marker{display:none}.paper-details>summary:after{content:"＋";color:#82909a;font-size:20px;line-height:1.5;flex:0 0 18px}.paper-details[open]>summary:after{content:"−"}.paper-details[open]>summary{border-bottom:1px solid #e3e9ec}.paper-id{font-size:12px;font-weight:750;color:var(--accent);padding:4px 7px;min-width:46px;background:var(--accent-light);border-radius:5px;text-align:center}.paper-heading{flex:1;min-width:0}.paper-title{display:block;font-size:17px;font-weight:650;line-height:1.55;overflow-wrap:anywhere}.paper-meta{display:block;color:var(--muted);font-size:12px;margin-top:6px}.tier{white-space:nowrap;font-size:11px;padding:3px 8px;border-radius:20px;line-height:1.7}.main_narrative{color:#286367;background:var(--accent-light)}.targeted_figure_read{color:#5f4d86;background:var(--violet-light)}.paper-body{padding:22px 26px 24px}.record-links{display:flex;gap:12px;flex-wrap:wrap;align-items:center;font-size:12px}.button-link{display:inline-block;background:#eaf1f5;border-radius:5px;padding:3px 9px;text-decoration:none;font-weight:650}.doi-link{font-family:ui-monospace,SFMono-Regular,Consolas,monospace;overflow-wrap:anywhere}.category-line{font-size:12px;color:var(--muted);margin:15px 0}.analysis-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px 30px}.analysis-block h4,.figure-note h4{font-size:13px;color:#386275;letter-spacing:.02em;margin:0 0 6px}.analysis-block p{margin:0}.analysis-block.featured{grid-column:1/-1;background:#f1f6f6;padding:15px 18px;border-radius:6px}.analysis-block.featured:last-child{background:#f4f1f8}.analysis-block.featured:last-child h4{color:#675183}.nested{margin:0;font-size:13px}.nested dt{font-weight:650;color:#596878;margin-top:4px}.nested dd{margin:0 0 9px}.nested p{margin:0}.nested ul{margin:0;padding-left:21px}.figures{margin-top:24px;padding-top:18px;border-top:1px solid var(--line)}.figures h3{font-size:15px;margin:0}.figures>.muted{font-size:12px;margin:4px 0 14px}.figure-grid{display:grid;grid-template-columns:1fr 1fr;gap:22px}.figure-note{background:#f8fafb;border:1px solid #e6ecef;padding:15px;border-radius:7px}.figure-note p{font-size:13px;margin:0}.figure-note h4{line-height:1.6}.read-details{margin-top:22px;font-size:13px}.read-details>summary{cursor:pointer;font-weight:650;color:#475d6b}.read-details h5{font-size:12px;color:#5d7180;margin:16px 0 5px}.read-details p{margin:.35em 0}.read-details ul{margin:.3em 0;padding-left:22px}.sources{display:flex;flex-wrap:wrap;gap:8px 16px}.source-link{font-size:12px}.tags{display:flex;flex-wrap:wrap;gap:6px;margin-top:20px}.tag{font:11px/1.8 ui-monospace,SFMono-Regular,Consolas,monospace;border:1px solid #e0e7eb;color:#657887;border-radius:4px;padding:1px 6px}.muted{color:var(--muted)}.empty{padding:50px;text-align:center;background:#fff;border:1px dashed #cad6db;border-radius:10px}.sr-only{position:absolute;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}footer{border-top:1px solid var(--line);padding:24px 0;color:var(--muted);font-size:12px;background:#eaf0f0}.noscript{padding:12px;background:#fff3d9;border-radius:8px}
@media(max-width:850px){.wrap{width:calc(100% - 32px)}.masthead{padding-top:35px}.stats{gap:10px}.stat{padding:15px}.stat strong{font-size:30px}.filters{grid-template-columns:1fr 1fr}.filter.search{grid-column:1/-1}.stat-tables{grid-template-columns:1fr}.paper-details>summary{display:grid;grid-template-columns:46px minmax(0,1fr) 18px;gap:10px;padding:17px 15px}.paper-heading{grid-column:2;grid-row:1}.paper-id{grid-column:1;grid-row:1}.paper-title{font-size:16px}.tier{margin-left:0;grid-column:2;grid-row:2;justify-self:start}.paper-details>summary:after{margin-left:0;grid-column:3;grid-row:1}.paper-body{padding:18px}.analysis-grid,.figure-grid{grid-template-columns:1fr}.paper{scroll-margin-top:245px}}
@media(max-width:600px){.stats{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media print{body{background:#fff;font-size:10pt}.masthead{padding:10px 0;background:#fff}.wrap{width:100%}.toolbar,.actions,.statistics,footer{display:none}.paper{break-inside:avoid;box-shadow:none}.paper-details>summary{padding:10px}.paper-body{padding:12px}.analysis-grid,.figure-grid{gap:10px 18px}.stats{margin:12px 0}.stat{padding:8px}.stat strong{font-size:24px}a{color:inherit}.read-details{font-size:9pt}}
'''

JS = r'''
"use strict";
(() => {
  const papers = Array.from(document.querySelectorAll("article.paper"));
  const search = document.getElementById("search");
  const category = document.getElementById("category");
  const tier = document.getElementById("tier");
  const status = document.getElementById("result-count");
  const empty = document.getElementById("empty");
  const normalize = value => value.toLocaleLowerCase().normalize("NFKC");
  function applyFilters() {
    const terms = normalize(search.value).trim().split(/\s+/u).filter(Boolean);
    let count = 0;
    for (const paper of papers) {
      const match = (!category.value || paper.dataset.category === category.value)
        && (!tier.value || paper.dataset.tier === tier.value)
        && terms.every(term => normalize(paper.dataset.search).includes(term));
      paper.hidden = !match;
      if (match) count += 1;
    }
    status.textContent = `显示 ${count} / ${papers.length} 篇`;
    empty.hidden = count !== 0;
  }
  search.addEventListener("input", applyFilters);
  category.addEventListener("change", applyFilters);
  tier.addEventListener("change", applyFilters);
  document.getElementById("reset").addEventListener("click", () => {
    search.value = ""; category.value = ""; tier.value = ""; applyFilters(); search.focus();
  });
  document.getElementById("expand").addEventListener("click", () => {
    papers.filter(p => !p.hidden).forEach(p => {p.querySelector(".paper-details").open = true;});
  });
  document.getElementById("collapse").addEventListener("click", () => {
    papers.filter(p => !p.hidden).forEach(p => {p.querySelector(".paper-details").open = false;});
  });
  function openHash() {
    const id = decodeURIComponent(location.hash.slice(1));
    const paper = papers.find(p => p.id === id);
    if (!paper) return;
    search.value = ""; category.value = ""; tier.value = ""; applyFilters();
    paper.querySelector(".paper-details").open = true;
    requestAnimationFrame(() => paper.scrollIntoView({block: "start"}));
  }
  window.addEventListener("hashchange", openHash);
  applyFilters(); openHash();
})();
'''


def stats_table(counter: dict, caption: str) -> str:
    return f'<table><caption>{esc(caption)}</caption><tbody>' + "".join(
        f'<tr><th scope="row">{esc(label)}</th><td>{count}</td></tr>' for label, count in counter.items()
    ) + "</tbody></table>"


def make_html(records: list[dict], statistics: dict) -> str:
    n = len(records)
    full = statistics["reading_tiers"]["main_narrative"]
    targeted = statistics["reading_tiers"]["targeted_figure_read"]
    options = "".join(f'<option value="{esc(cat)}">{esc(cat)}（{statistics["categories"][cat]}）</option>' for cat, _ in CATEGORY_IDS)
    font_dir = BASE / "tools/font-assets"
    font_path = font_dir / "atlas-cjk-subset.woff"
    font_style = ""
    if font_path.exists():
        font_data = base64.b64encode(font_path.read_bytes()).decode("ascii")
        font_style = '@font-face{font-family:"Atlas CJK";src:url(data:font/woff;base64,' + font_data + ') format("woff");font-style:normal;font-weight:400;font-display:swap;}'
    font_license = (font_dir / "OFL.txt").read_text(encoding="utf-8") if (font_dir / "OFL.txt").exists() else ""
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="89篇原始研究、178张实际审读整图的中文科学绘图证据图谱，区分66篇主文通读与23篇定向精读。">
<meta name="color-scheme" content="light"><title>科学绘图证据图谱 · 89篇原始研究</title><style>{font_style}{CSS}</style></head>
<body><header class="masthead"><div class="wrap"><div class="eyebrow">SCIENTIFIC FIGURE ATLAS · EVIDENCE & DESIGN</div>
<h1>让科学任务决定图像形式</h1><div class="intro"><p>89篇原始研究的图像论证方法：从构图、颜色与证据组织，到可编辑的重建路线。</p>
<p>逐篇记录实际看过的整图、读到的主文范围，以及能够迁移的方法与边界。</p></div>
<div class="meta-row"><span>文献年份：2014—2025</span><span>审读访问日：{ACCESS_DATE}</span><span>不加载外部脚本或第三方图像</span></div></div></header>
<div class="wrap"><section class="stats" aria-label="样本规模">
<div class="stat"><strong>{n}</strong><span>篇独立DOI原始研究</span></div><div class="stat"><strong>{statistics['figures_viewed']}</strong><span>张实际查看的关键整图</span></div>
<div class="stat full"><strong>{full}</strong><span>篇主文通读</span></div><div class="stat targeted"><strong>{targeted}</strong><span>篇图导向定向精读</span></div></section>
<section class="scope"><h2>如何使用这份图谱</h2><p>按科学问题和图像任务寻找案例，打开条目查看完整分析。重建路线是建议，原图仅提供来源链接；请以各篇原始阅读范围判断分析的适用程度。</p>
<div class="tierbar" role="img" aria-label="66篇主文通读，23篇图导向定向精读"><span class="full" style="width:{full/n*100:.6f}%"></span><span class="targeted" style="width:{targeted/n*100:.6f}%"></span></div>
<div class="tierlegend"><span>主文通读 {full}篇</span><span>图导向定向精读 {targeted}篇</span></div>
<details><summary>阅读层级与真实证据边界</summary><ul>{''.join('<li>'+esc(s)+'</li>' for s in BOUNDARIES)}</ul>
<p>离线可阅读与检索本页全部分析；访问论文、DOI及原图链接需要联网。这里的“局限”针对视觉呈现及当前阅读范围，不是论文整体质量评分。</p></details></section>
<details class="statistics"><summary>期刊、年份与类别分布（样本计数）</summary><div class="stat-tables">
{stats_table(statistics['journals'], '归一化期刊名称')}{stats_table(statistics['years'], '发表年份')}
{stats_table(statistics['categories'], '按主要科学任务归类；每篇仅计一类')}</div></details>
<div class="toolbar"><div class="filters">
<div class="filter search"><label for="search">检索标题、领域、主张与设计分析</label><input id="search" type="search" placeholder="例如：A24、paired、成核、寿命、photodetector" autocomplete="off"></div>
<div class="filter"><label for="category">科学任务类别</label><select id="category"><option value="">全部类别</option>{options}</select></div>
<div class="filter"><label for="tier">阅读层级</label><select id="tier"><option value="">全部阅读层级</option><option value="main_narrative">主文通读（66）</option><option value="targeted_figure_read">图导向定向精读（23）</option></select></div></div>
<div class="actions"><span id="result-count" class="result-count" role="status" aria-live="polite">显示 89 / 89 篇</span><button id="reset" type="button">重置筛选</button><button id="expand" type="button">展开当前结果</button><button id="collapse" type="button">收起当前结果</button></div></div>
<main id="papers" aria-label="逐篇完整分析"><noscript><p class="noscript">JavaScript已停用：全部89条分析仍可通过下方条目展开阅读；检索与筛选需要启用JavaScript。</p></noscript>
{''.join(card(r) for r in records)}<p id="empty" class="empty" hidden>没有匹配的条目。请减少检索词或重置筛选。</p></main></div>
<footer><div class="wrap">科学绘图证据图谱 · 元数据与本项目视觉分析 · {ACCESS_DATE}<br>本页不包含论文全文、原文图注或第三方图像文件。文献与图像的权利归各自权利人，外链指向原始公开来源。</div></footer>
<template id="embedded-font-license" data-source="https://github.com/google/fonts/tree/main/ofl/notosanssc"><pre>{esc(font_license)}</pre></template>
<script>{JS}</script></body></html>'''


def make_index(records: list[dict], statistics: dict) -> str:
    byid = {r["id"]: r for r in records}
    lines = [
        "# 绘图证据简索引", "",
        "本索引只在需要领域实例、具体图型或来源追踪时读取。核心执行流程见上级SKILL.md；完整自己的视觉分析见同目录`corpus-atlas.json`。", "",
        "## 范围与阅读层级", "",
        "89篇不同DOI、178张实际看过的整图；66篇主文科学论证通读，23篇图导向定向精读。后者不能当作全部主文已读。每篇原始`read_scope`和`sections_read`均保留；Methods/SI限制逐篇记录，不默认已读。文献覆盖2014—2025年，审读访问日2026-10-17；这是有目的的绘图样本，不是穷尽最新文献的系统综述。", "",
        "以下优点/局限是图像方法观察，不是论文质量评分。最终绘图软件没有来源证据时为unknown；建议重建工具不等于作者实际工具。原图与全文不随技能分发。", "",
        "## 按图像任务快速导航", "",
        "| 需要解决的图像任务 | 可先查的实例 |", "|---|---|",
        "| 重复器件、批次与性能比较 | A24（十批器件）、A02/A22（效率与稳定性）、D18（多变量模型误差） |",
        "| 时域、频域与带符号谱图 | A04（时域载流子诊断）、A13（多维探测；频域主文已读但未将图3计为目视图）、D14（手性二维谱） |",
        "| 状态、载流子与反应路线 | A18（竞争配体路径）、A23（离子状态与势垒）、B07（溶液平衡）、B17（催化重构） |",
        "| 生长时序、相图与跨尺度结构 | B01/B02/B06/B12/B14 |",
        "| 装置与实物对应、流程与操作 | C01/C05/C08、D06/D12 |",
        "| 场、体数据、结构与计算架构 | D01/D03/D05/D07/D08/D19/D20 |",
        "| 机器人动作、界面与应用证据 | C15/C16/C18/C19/C20/C21/C23/C24 |", "",
        "## 按科学任务分类的89篇索引", "",
    ]
    for cat, ids in CATEGORY_IDS:
        lines.extend([f"### {cat}（{len(ids)}篇）", "", "| ID | 原始研究与来源 | 期刊 / 年 | 阅读层级 | 实际看图 |", "|---|---|---|---|---|"])
        for pid in ids:
            r = byid[pid]
            title = r["title"].replace("|", "\\|")
            journal = "PNAS" if r["journal"].startswith("Proceedings of") else r["journal"]
            figures = "、".join(f"[{fig_label(f['number'])}]({f['url']})" for f in r["figures_viewed"])
            lines.append(f"| {pid} | [{title}]({r['url']}) · DOI `{r['doi']}` | {journal} / {r['year']} | {r['read_tier_label']} | {figures} |")
        lines.append("")
    lines.extend(["## 期刊别名归一", "",
                  "`Nat Commun`→`Nature Communications`；`Sci Adv`→`Science Advances`；`PNAS`、`Proc Natl Acad Sci U S A`及含`of the United States of America`的长名→`Proceedings of the National Academy of Sciences`。便携数据同时保留`journal_original`。", ""])
    return "\n".join(lines)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    REF.mkdir(parents=True, exist_ok=True)
    records, hashes, original_scopes = [], {}, {}
    for group in "abcd":
        path = BASE / "corpus" / group / (group + "_records.json")
        hashes[str(path.relative_to(BASE))] = hashlib.sha256(path.read_bytes()).hexdigest()
        source = json.loads(path.read_text(encoding="utf-8"))
        for raw in source:
            r = copy.deepcopy(raw)
            original_scopes[r["id"]] = copy.deepcopy(r["read_scope"])
            r["source_group"] = group.upper()
            r["journal_original"] = r["journal"]
            r["journal"] = JOURNAL_ALIASES.get(r["journal"], r["journal"])
            r["year"] = int(r["year"])
            r["doi"] = r["doi"].strip().removeprefix("https://doi.org/").lower()
            scope = str(r["read_scope"])
            full = group in "ab" or scope.startswith(("FULL_MAIN_TEXT_RESULTS", "FULL_MAIN_NARRATIVE_READ"))
            r["read_tier"] = "main_narrative" if full else "targeted_figure_read"
            r["read_tier_label"] = TIERS[r["read_tier"]]
            r["read_tier_definition"] = TIER_DEFS[r["read_tier"]]
            r["category"] = CATEGORIES[r["id"]]
            r["source_links"] = source_links(r)
            for figure in r["figures_viewed"]:
                if "caption" in figure:
                    figure.pop("caption")
                    figure["source_caption_omitted"] = True
            records.append(r)
    records.sort(key=lambda r: r["id"])
    assert len(records) == 89
    assert len({r["id"] for r in records}) == 89
    assert len({r["doi"] for r in records}) == 89
    assert set(CATEGORIES) == {r["id"] for r in records}
    assert all(r["read_scope"] == original_scopes[r["id"]] for r in records)
    assert Counter(r["read_tier"] for r in records) == {"main_narrative": 66, "targeted_figure_read": 23}
    urls, paths = set(), []
    for r in records:
        assert re.fullmatch(r"10\.\d{4,9}/\S+", r["doi"]), (r["id"], r["doi"])
        assert len(r["figures_viewed"]) == 2
        for key, _ in ANALYSIS_FIELDS:
            assert r.get(key), (r["id"], key)
        for f in r["figures_viewed"]:
            path = Path(f["local_path"])
            assert path.is_file() and path.stat().st_size > 0, (r["id"], path)
            paths.append(str(path))
            urls.add(f["url"])
        urls.update(r["source_links"])
    for url in urls:
        parsed = urlparse(url)
        assert parsed.scheme in {"http", "https"} and parsed.hostname, url
        assert not re.search(r"[\s<>\"]", url), url
    stats = {
        "papers": len(records), "unique_doi": len({r["doi"] for r in records}),
        "figures_viewed": sum(len(r["figures_viewed"]) for r in records),
        "reading_tiers": dict(Counter(r["read_tier"] for r in records)),
        "source_groups": dict(Counter(r["source_group"] for r in records)),
        "journals": dict(sorted(Counter(r["journal"] for r in records).items(), key=lambda x: (-x[1], x[0]))),
        "years": dict(sorted(Counter(r["year"] for r in records).items())),
        "categories": {cat: len(ids) for cat, ids in CATEGORY_IDS},
        "unique_domain_strings": len({r["domain"] for r in records}),
    }
    metadata = {
        "schema_version": "1.0", "title": "科学绘图证据图谱", "access_date": ACCESS_DATE,
        "reading_tier_definitions": TIER_DEFS, "scope_boundaries": BOUNDARIES,
        "journal_aliases": JOURNAL_ALIASES,
        "publication_policy": "Only bibliographic metadata, reading scope, original source links, and our own visual analysis; no article full text, source figure captions, or embedded third-party images.",
        "source_caption_policy": "Verbatim caption fields from input records are omitted; all original analytical fields are preserved.",
    }
    atlas = {"metadata": metadata, "statistics": stats, "records": records}
    dump_json(OUT / "paper-atlas.json", atlas)
    dump_json(REF / "corpus-atlas.json", portable(atlas))
    ordered = ["id", "title", "doi", "url", "journal", "journal_original", "year", "category", "domain",
               "read_tier", "read_tier_label", "read_tier_definition", "read_scope", "sections_read",
               "figures_viewed", "science_story", "composition", "color_observation", "visual_form", "strengths",
               "limitations", "reconstruction_route", "software_evidence", "transferable_rule", "skill_tags",
               "source_links", "source_refs", "access_date", "source_group"]
    extra = sorted({key for r in records for key in r} - set(ordered))
    fields = ordered + extra
    with (OUT / "paper-atlas.csv").open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for r in records:
            writer.writerow({key: json.dumps(value, ensure_ascii=False) if isinstance(value, (dict, list)) else value for key, value in r.items()})
    (OUT / "paper-atlas.html").write_text(make_html(records, stats), encoding="utf-8")
    (REF / "evidence-index.md").write_text(make_index(records, stats), encoding="utf-8")
    (OUT / "atlas-script-check.js").write_text(JS, encoding="utf-8")
    report = {
        "status": "static_validation_passed", "statistics": stats,
        "source_sha256": hashes, "original_read_scope_preserved": True,
        "all_89_unique_ids_and_dois": True,
        "all_178_local_figure_paths_exist_and_nonempty": True,
        "unique_local_figure_paths": len(set(paths)),
        "unique_external_urls_syntax_checked": len(urls),
        "external_url_validation_scope": "Protocol/hostname/whitespace and article/DOI/figure link generation checked; remote availability not re-probed in this assembly task.",
        "csv_encoding": "UTF-8 BOM; dict/list cells use JSON strings", "csv_columns": fields,
        "portable_paths_removed": True,
        "html_external_images_scripts_styles": 0,
        "source_files_modified": False,
    }
    portable_text = (REF / "corpus-atlas.json").read_text(encoding="utf-8")
    assert not re.search(r"/(?:workspace|tmp|root)/", portable_text)
    dump_json(OUT / "atlas-validation.json", report)
    print(json.dumps({"files_written": [str(OUT / f) for f in ["paper-atlas.json", "paper-atlas.csv", "paper-atlas.html", "atlas-validation.json"]] + [str(REF / f) for f in ["corpus-atlas.json", "evidence-index.md"]], "statistics": stats}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
