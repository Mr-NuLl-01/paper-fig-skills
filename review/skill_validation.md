# 九技能结构验证与有限机械审查

本记录覆盖 `skills/` 下当前九个 `sci-figure-*` 技能的官方结构验证、文件引用和代理元数据，以及所有当前已导出 bundled DEMO SVG 的机械扫描。**没有把机械扫描称为视觉审图或科学语义验证。** 原始前向试用仅覆盖一个七模块的器件—统计混合路线；process 和 image 路线没有实际前向执行。

完整命令、返回码、stdout/stderr、逐项元数据、全部引用和每个 SVG 的扫描结果保存在 `skill_validation.json`。可运行 `python review/validate_skills.py` 重复本次结构与机械验证。

## 结果

| 检查 | 实际结果 | 范围与限制 |
|---|---|---|
| 官方 `quick_validate.py` | 9 / 9 返回 0，均为 `Skill is valid!` | 校验 YAML frontmatter、name、description；不校验图的质量 |
| 名称与代理配置 | 9 / 9 通过；display_name 互异 | folder/name 一致；display_name 非空且与模块角色相符；short_description 为 25–64 字符；default_prompt 含正确 `$sci-figure-*` ID；接口字符串带引号 |
| Markdown 相对链接 | 26 个引用位置，零缺失 | 按所在文档目录解析；包含已修复的跨技能脚本链接 |
| 实际资源路径提及 | 9 个引用位置，零缺失 | 检查 scripts/references/assets/agents 路径；示例 JSON 的虚构 chip_photo.tif 不作为随包资产 |
| SVG 扫描器契约测试 | 7 / 7 通过 | 原有 5 项 + 本次新增 2 项 base64 导出兼容测试 |
| 当前 bundled DEMO SVG | 8 / 8 扫描完成，零 findings | 其中 4 个 Matplotlib SVG 保留 stylesheet 未完整解析的 uncertainty；不能称全部视觉通过 |

九个技能为 director、data、mechanism、device、process、image、compose、color 和 review。官方验证器只读运行，未修改；未修改已安装技能、未安装或发布。color 脚本由主 agent 单独处理，本次没有编辑。

## 运行命令

在项目根目录中，汇总命令为：

```bash
python review/validate_skills.py
```

脚本实际对每个技能分别调用下列官方命令，九次返回码均为 0，逐次 argv 已存入 JSON：

```bash
python /root/.codex/skills/oai/skill-creator/scripts/quick_validate.py skills/<skill-name>
```

扫描器测试和 bundled demo 扫描实际使用：

```bash
python skills/sci-figure-review/scripts/test_check_svg.py
python skills/sci-figure-review/scripts/check_svg.py skills/<skill-name>/assets/demo/<exported-demo>.svg
```

没有为未提供的期刊要求自行设置 `--min-label-pt` 门槛。

## 精确修订

### 1. 双布局比较适用范围

文件：`skills/sci-figure-compose/SKILL.md`，第 2 节。

原句：

> 比较至少两种适合当前任务的组织方法，再直接制作最合适的一种。

改为：

> 遇到复杂复合图、读序不确定或需要重排的任务，快速比较至少两种适合的组织方法，再直接制作最合适的一种。关系清楚的简单单面板可直接制作，简述所选表示为何足以回答读者问题，不强制追加备选草图。

检索 compose 全目录，没有其他把两种布局比较设为无条件门槛的引用。`editable-production.md` 的“两种尺度”指最终尺寸和细节预览，不是两个候选布局，因此保留。

### 2. C03 培养日与条件边界

文件：`skills/sci-figure-compose/references/layout-strategies.md` 的 C03 条目。原来只概括“几何变换＋培养法×时间矩阵”；现在补充精确限定：

> Fig2顶部是Day5/10/14的同日培养法对照矩阵；m的分化比较包含Drop D7、OCTOPUS D7和OCTOPUS D14三条件；n的葡萄糖诱导Ca²⁺响应则比较Drop D7与OCTOPUS D14，图注明确用于考察延长培养贡献。并非整图均为同龄对照；迁移布局时逐面板保留day与condition，不把不同培养时长的差异只归因于方法。

同样在 `references/examples.md` 的“多条件显微结果”验收中增加逐面板核对 day/condition 的要求，并提醒 C03 顶部同日矩阵不能让后段 Drop D7 对 OCTOPUS D14 的功能比较被误读为同龄对照。

依据：本次实际打开 `corpus/c/C03/figure_02_full.png`，并读取 `corpus/c/C03/article.html` 中 figure#F2 完整图注。未把所有后段面板概括成跨龄比较。raw C03 corpus 记录由 corpus_opto agent 单独修复，本次没有编辑 raw corpus 或原审计报告。

### 3. 可解析的扫描器引用

文件：`skills/sci-figure-compose/references/editable-production.md` 末段。

原先不可解析的代码路径 `review/scripts/check_svg.py` 改成指向相邻技能的真实 Markdown 相对链接 `../../sci-figure-review/scripts/check_svg.py`，并明确该脚本属于 `sci-figure-review` 模块。

### 4. 正常导出 base64 的机械扫描误报

实际扫描 `sci-figure-data/assets/demo/demo-tradeoff.svg` 时，旧扫描器报出 `invalid_data_uri: Only base64 data is allowed`。检查导出的 image href，发现 PNG base64 正文带有导出器换行被 XML 规范化后的空格。不能据此认定图像资产损坏。

在 `skills/sci-figure-review/scripts/check_svg.py` 中，仅为 base64 正文移除 ASCII 空白后继续执行严格验证：

```python
base64.b64decode(re.sub(r'[\t\n\r\f ]', '', body), validate=True)
```

`test_check_svg.py` 新增两个实际执行的契约：含换行、空格和制表的 base64 仍读到 PNG 尺寸；插入非空白字符 `?` 仍报告损坏。`references/svg-scan.md` 同步说明这一边界。测试由 5 项增至 7 项，全部通过，原实际 tradeoff SVG 重新扫描后不再误报。

## 当前八个 DEMO SVG 的机械清单

| 模块与文件 | live text | image | findings | 保留的 uncertainty |
|---|---:|---:|---:|---|
| color / palette_diagnostic.svg | 64 | 0 | 0 | 无 |
| data / demo-paired-batches.svg | 14 | 0 | 0 | stylesheet 未完整解析 |
| data / demo-tradeoff.svg | 29 | 1 | 0 | stylesheet 未完整解析 |
| device / device_demo_overlay.svg | 3 | 0 | 0 | 无 |
| device / device_demo_preview.svg | 7 | 3 | 0 | 无 |
| device / device_demo_side_section.svg | 9 | 0 | 0 | 无 |
| mechanism / demo-energy-alignment.svg | 20 | 0 | 0 | stylesheet 未完整解析 |
| mechanism / demo-spatial-drift.svg | 8 | 0 | 0 | stylesheet 未完整解析 |

上表来自实际存在的导出 SVG，不是只检查生成脚本。这里核对了可解析性、文字清单、局部/嵌入图像和路径引用。没有逐一视觉打开这八个 DEMO，也未以扫描结果断言其科学语义、箭头含义、实际文字重叠或外部编辑器导入行为正确。三个 device SVG 的 metadata 节点缺省，另有同目录参数源文件；本次只记录存在性，不把 metadata 缺省设为未授权的统一门槛。

## 前向试用覆盖声明

`review/forward-test/` 中原创器件图实际执行了 director + data + device + mechanism + compose + color + review，共七模块。该张图的 PNG、缩小预览和灰度预览确实打开检查过，保留了 3 批各 5 个配对器件、未知厚度和未测量转移速率边界。此次结构验证扩展到九个技能，但没有因此声称 process/image 路线或全部 DEMO 已通过前向任务、视觉或科学验证。
