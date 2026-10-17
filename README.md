# paper-fig-skills

一套面向科研论文配图的九模块技能：从科学问题与证据出发，选择表达方式，制作可编辑图，再分别检查科学语义、可读性和交付完整性。

适用于数据图、机制图、器件结构、实验过程、显微/场图及多面板组合。它们提供工作规程、参考案例与可复用脚本，不是固定期刊模板，也不保证科学结论正确或投稿成功。

## 九个模块

| 技能 | 负责什么 | 典型输入与输出 |
| --- | --- | --- |
| [sci-figure-director](skills/sci-figure-director/SKILL.md) | 总体规划与任务路由 | 主张、证据、目标尺寸 → 图形路线与制作合同 |
| [sci-figure-data](skills/sci-figure-data/SKILL.md) | 数值、分布、趋势、误差与权衡 | 原始数据及统计定义 → 可追溯的数据图 |
| [sci-figure-mechanism](skills/sci-figure-mechanism/SKILL.md) | 能级、载流子、反应与竞争机制 | 对象、参考系、证据 → 可编辑机制图 |
| [sci-figure-device](skills/sci-figure-device/SKILL.md) | 层序、接触、剖面、爆炸与空间结构 | 几何和连接信息 → SVG 或可编辑三维示意 |
| [sci-figure-process](skills/sci-figure-process/SKILL.md) | 生长、制备、操作与状态演变 | 步骤、时间、样品和物种 → 过程图 |
| [sci-figure-image](skills/sci-figure-image/SKILL.md) | 显微、体数据、场图与注释 | 原始图像、尺度、ROI → 证据保真的图版 |
| [sci-figure-compose](skills/sci-figure-compose/SKILL.md) | 多面板读序与比较关系 | 各面板及主张 → 成组的可编辑版式 |
| [sci-figure-color](skills/sci-figure-color/SKILL.md) | 类别、顺序、发散等颜色语义 | 数据类型和背景 → 色板及有限诊断 |
| [sci-figure-review](skills/sci-figure-review/SKILL.md) | 科学、视觉与编辑性交付检查 | 源文件、导出图、图注 → 有范围的审查报告 |

不确定从哪里开始时使用 `sci-figure-director`；仅有单一任务时可以直接指定专业模块。九个技能可一起安装，也可按需要选择。

## 内容与边界

- `skills/` 包含 9 个独立技能、共 71 个原始文件：说明、代理配置、参考规程、6 个 Python 脚本和 DEMO 资产。
- 文献图谱记录 89 篇不同论文与 178 张关键整图。其中 66 篇为主文连续阅读，23 篇为围绕目标图的定向精读。这是来源项目记录的范围，不表示所有论文全文、Methods、SI 或全部图像均已核验，也不是本次发布重新完成的阅读。
- 文献元数据、来源链接及设计分析见 [证据索引](skills/sci-figure-director/references/evidence-index.md) 和 [机器可读图谱](skills/sci-figure-director/references/corpus-atlas.json)。不附带第三方论文全文或原图。
- 示例数据、几何与机制均明确标记为 DEMO，不能作为真实研究结果。三维预览包含渲染位图；几何编辑使用 `.blend`，标注编辑使用相应 SVG。
- 本次发布保留全部 71 个技能文件原始字节；没有修复脚本逻辑。已知问题请先读 [KNOWN_ISSUES.md](KNOWN_ISSUES.md)。

## 安装：macOS / Linux / Windows

先下载本仓库 ZIP 并解压，或克隆：

```sh
git clone https://github.com/Mr-NuLl-01/paper-fig-skills.git
```

当前官方本地技能文档将用户级目录列为 `$HOME/.agents/skills`，项目级目录为项目内的 `.agents/skills`。下面使用用户级目录；旧版或自定义环境请以实际识别的 Skills 根目录为准，不要向多个目录重复安装同名技能。参见 [OpenAI 官方技能文档](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)（核对日期：2026-10-17）。

### macOS / Linux

在下载的仓库根目录运行。先检查是否存在同名目录，若存在则停止，比较并自行备份后再更新：

```sh
dest="$HOME/.agents/skills"
mkdir -p "$dest"
(
  for src in skills/sci-figure-*; do
    name="${src##*/}"
    if [ -e "$dest/$name" ]; then
      printf '已有同名技能，请先比较和备份：%s\n' "$dest/$name"
      exit 1
    fi
  done
  for src in skills/sci-figure-*; do cp -R "$src" "$dest/"; done
)
```

### Windows PowerShell

在下载的仓库根目录运行；已有同名目录时停止，不直接覆盖：

```powershell
$dest = Join-Path $HOME '.agents\skills'
New-Item -ItemType Directory -Path $dest -Force | Out-Null
$sources = @(Get-ChildItem '.\skills\sci-figure-*' -Directory)
if ($sources.Count -ne 9) { throw '请在仓库根目录运行，并确认九个技能目录齐全。' }
foreach ($src in $sources) {
    if (Test-Path (Join-Path $dest $src.Name)) {
        throw "已有同名技能，请先比较和备份：$($src.Name)"
    }
}
foreach ($src in $sources) {
    Copy-Item -LiteralPath $src.FullName -Destination $dest -Recurse
}
```

如果在 WSL 内运行，应安装到 WSL 对应的用户目录，按上面的 Linux 方法操作。复制的是九个 `sci-figure-*` 文件夹本身，不能只复制 `SKILL.md`；相对引用的 `references/`、`scripts/`、`assets/` 也要保留。仓库中的普通 `skills/` 目录是分发目录，克隆仓库不等于已安装。

安装后检查技能列表；未显示时重启客户端，并先用合成数据试运行。这里提供的是手动安装说明，本仓库发布不代表已在你的电脑完成安装或验证。

## 怎么调用

可以在支持显式技能调用的 Codex 界面使用 `$技能名`，或直接说“使用 sci-figure-data 技能”。例如：

- `使用 $sci-figure-director：根据我提供的数据和图注设计一组论文图。先列主张、证据和比较关系，缺失科学信息标为待补。交付可编辑源文件和预览。`
- `使用 $sci-figure-data：把这份 CSV 的配对样本与批次差异画清楚。保留个体点，说明误差和重复的定义，不补造数据。`
- `使用 $sci-figure-device：按这份层序表制作器件剖面与爆炸图。未知尺寸标 unknown，夸张厚度写入图注，保留可编辑几何与独立标签。`
- `使用 $sci-figure-review：检查这份 SVG 和导出的 PDF，目标宽度 180 mm。分别报告科学语义、最终尺寸可读性和可编辑性；不要把机械扫描当成科学验证。`

最好同时提供：图要回答的问题、原始数据/图像、图注、单位与尺度、观察/计算/假说边界、目标物理尺寸和可编辑格式要求。

## 脚本与 DEMO

技能文字本身不需要安装绘图库。运行特定脚本才需要对应环境：

| 脚本 | 依赖与用途 |
| --- | --- |
| `sci-figure-color/scripts/palette_audit.py` | Python 标准库；配色 JSON 与 SVG 诊断 |
| `sci-figure-review/scripts/check_svg.py` | Python 标准库；SVG 的有限机械扫描 |
| `sci-figure-review/scripts/test_check_svg.py` | Python 标准库；扫描器的 7 个契约测试 |
| `sci-figure-data/scripts/make_demo.py` | Matplotlib、NumPy；合成数据图 |
| `sci-figure-mechanism/scripts/make_demo.py` | Matplotlib；合成机制示例 |
| `sci-figure-device/scripts/device_demo.py` | Blender 4.x 自带 Python、`bpy`、`mathutils`；三维示例 |

下列命令从仓库根目录运行；Windows 可按环境把 `python` 改为 `py`：

```sh
python skills/sci-figure-color/scripts/palette_audit.py --palette indigo-copper --out outputs/color-demo
python skills/sci-figure-review/scripts/check_svg.py skills/sci-figure-data/assets/demo/demo-paired-batches.svg
python skills/sci-figure-review/scripts/test_check_svg.py
python skills/sci-figure-data/scripts/make_demo.py --output-dir outputs/data-demo
python skills/sci-figure-mechanism/scripts/make_demo.py --output-dir outputs/mechanism-demo
blender -b --python skills/sci-figure-device/scripts/device_demo.py -- --out outputs/device-demo --render
```

运行 Blender 脚本会清空当前场景中的对象；请使用独立后台进程或新的文件，先保存自己的工作。已有 `.blend` 保留原始生成时的渲染输出设置，在新机器上打开后应先改为自己的可写输出目录。本次未重新打开或渲染 `.blend`。SVG 扫描器可能读取 SVG 引用的本地图像，只对你信任且有权读取的文件运行。

各操作系统、字体与软件版本的兼容性未做完整测试，依赖也未锁定；可选三维工具不可用时仍可按技能说明走二维路线。

## 核验、贡献与许可

- [PROVENANCE.md](PROVENANCE.md)：来源、纳入范围和检查边界
- [SKILL-MANIFEST.json](SKILL-MANIFEST.json)：71 个技能文件的字节数与 SHA-256
- [KNOWN_ISSUES.md](KNOWN_ISSUES.md)：当前脚本限制与使用提醒
- [CONTRIBUTING.md](CONTRIBUTING.md)：提交问题和改动的要求
- [CHANGELOG.md](CHANGELOG.md)：变更记录

沿用仓库已有的 [MIT License](LICENSE)。论文、第三方素材及其商标的权利仍归原权利人；文献链接不授予复制或再分发其内容的许可。
