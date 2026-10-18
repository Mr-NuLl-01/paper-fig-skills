# Science Figure Atlas · 绘图技能与研究材料归档

整理日期：2026-10-17；本次打包以已保存的 **Science-Figure-Atlas-2026-10-17** 资料库为来源。

## 文件结构

- `skills/`：九个独立的 `sci-figure-*` 技能，包含 `SKILL.md`、配置、参考规程、脚本和对应示例。
- `deliverables/`：26 页研究手册 PDF、89 篇论文逐图图谱（HTML、JSON、CSV）、配色图谱和诊断、可编辑 SVG/Blender 示例、构建脚本和试用数据。
- `review/`：技能验证、抽查与修复记录。
- `tools/`：随交付保存的工具代码和字体许可说明，不含独立字体文件。
- `ARCHIVE-MANIFEST.json`：本压缩包内实际文件的 SHA-256、大小和特殊说明，优先用于本归档的完整性核验。

## 阅读顺序

1. `deliverables/scientific-figure-handbook.pdf`：研究设计、视觉原则和九个模块。
2. `deliverables/paper-atlas.html`：可筛选的逐篇图像分析；`paper-atlas.json` 可用于机器读取。
3. `deliverables/color-atlas.html`：颜色用途、原创配色与有限模拟。
4. `skills/sci-figure-director/SKILL.md`：任务路由；再阅读对应专项 skill。
5. `deliverables/advanced-device-demo/`、`deliverables/forward-test-demo/`：原创可编辑样例。

## 本地 Codex 安装（未自动执行）

从本归档的 `science-figure-atlas/skills/` 中，选择需要的 `sci-figure-*` 文件夹复制到你当前 Codex 配置下的 Skills 根目录，通常是 `${CODEX_HOME:-$HOME/.codex}/skills/`。不建议未经比较就覆盖同名既有技能。安装后检查 `SKILL.md` 和其相对引用的 `references/`、`scripts/`、`assets/` 是否完整，并在新会话里试运行。

## 证据与版本边界

- 文献记录为 89 篇不同论文、178 张实际查看整图，66 篇主文连续阅读、23 篇围绕目标图精读；不是 89 篇全文及全部 SI 的通读声明。
- 技能已编写、经过结构验证和限定范围试用，但上一轮受运行环境写入审批限制，**未安装到受保护技能目录，也未做远程 git 同步**。
- `deliverables/source-inventory.json` 是上一轮保存时的原始快照；其中的研究手册 PDF 记录为较早版本，本归档保留已上传的较新 PDF。以 `ARCHIVE-MANIFEST.json` 为实际归档校验依据。
- 独立 `.ttf`、`.woff` 等字体文件未纳入此 ZIP。需要重建依赖字体的排版时，应在自己的环境中安装具有适当许可的字体。HTML 和 PDF 是已有自包含交付，不受独立字体文件缺席影响。
- 未附带第三方论文全文、期刊原图、下载缓存及机器执行环境。
- 演示数据均是教学用 DEMO，不代表真实器件数据或证据。

## 核验

Python：

```python
import hashlib, json, pathlib
root = pathlib.Path('science-figure-atlas')
m = json.loads((root / 'ARCHIVE-MANIFEST.json').read_text(encoding='utf-8'))
for e in m['files']:
    p = root / e['path']
    assert p.stat().st_size == e['bytes']
    assert hashlib.sha256(p.read_bytes()).hexdigest() == e['sha256']
print('All files verified:', len(m['files']))
```
