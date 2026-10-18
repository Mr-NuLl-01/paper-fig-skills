# 独立证据与技能抽查

审查日期：2026-10-17。审查者：独立 evidence_audit 子任务。

## 范围与有限结论

按每组3篇进行目的抽查：A01/A14/A23、B01/B05/B17、C02/C03/C12、D01/D14/D20。实际打开24张完整选定图，核对对应原始全文片段/完整图注；完整阅读9个SKILL.md并抽查关键参考文件。覆盖2014、2017和2024研究、机构PDF、作者稿与XML图序异常。

**该样本中未发现阻断或重大图号/图像错配，也未发现把建议重建工具虚称为作者最终作图软件的情形。发现4项轻微精度/溯源问题及1项局限补充建议。**这不是通过分数，不能推出其余77篇全部正确；89篇、178图和66/23阅读层级为项目记录的全体声明，本审查只独立确认列出的12篇/24图。

## 逐篇实际核对

| ID / 年份 | 实际打开的图 | 核对结果与证据边界 |
|---|---|---|
| A01 / 2024 | 1；4 | Fig1堆叠/电路/光学模型、静态与动态成膜、红蓝紫器件曲线、正负偏压照片及Fig4串联/照片栏/相位波形均支持记录；原图Fig1i实为EQE-J、j为J-V-L，而caption i/j相反，记录已主动保留此来源矛盾。 |
| A14 / 2024 | 2；4 | Fig2（本地fig3）为2×3器件/性能/70器件统计/寿命；Fig4（本地fig9）为GIWAXS、角度分峰与相强度，红立方/蓝四方。主文明确双添加剂17h与control19h相近，支持不得写寿命同步提升。XML第2个是Extended Data Fig1，record未误把序号当图号。 |
| A23 / 2023 | 1；4 | 本地期刊排版PDF页3为Fig1九面板，页7为Fig4；State of ions横轴、LGP/HGP蓝/粉紫及真实阵列/模拟识别边界支持记录。正文开头明确诊断探索经由simulations；caption4e明确Simulated。PDF来源URL待补。 |
| B01 / 2017 | 3；5 | Fig3上层状态链分RT/annealing，下层离子笼到晶体；Fig5四帧绿褐显微像、虚圈、截面与蓝灰红概念浓度曲线。主文及图注明称schematically，支持不是实测浓度。 |
| B05 / 2014 | 2；5 | Fig2为AFM孪晶/空位/晶界/塑晶四区；Fig5六帧0、5、14、25、37、82min追踪I–IV与并合；caption明确向上扫描、并合超出CNT。构图和限制支持，标记概括有EA-01。 |
| B17 / 2024 | 2；6 | 作者接受稿页6明确Fig2，页14明确Fig6。三层共享时间、蓝无dmphen/红含dmphen、浅原始/深FFT平滑曲线与铜表面CO-[CuCO]+-Cu+循环支持记录；结论明确需要新operando技术确认瞬态身份。未独立复核最终publisher版只有5图这一外部版本数量。 |
| C02 / 2023 | 1；2 | 机构公开期刊格式PDF页2为Fig1、页3为Fig2。Fig1通道总图、6个时间帧红色手动着色单滴、观测位置到FRET分布；Fig2左右结合案例、紫/蓝时间与浓度序列、断轴动力学均支持。caption明确红滴是manually colored，并非自然红色液滴。 |
| C03 / 2022 | 1；2 | PMC页头明确author manuscript、final edited DOI一致；主图取publisher整图1/2。几何切核/径向展开、12孔板照片、操作图与Day×method显微矩阵支持记录；后段不同培养日的功能比较需保留EA-05边界。 |
| C12 / 2025 | 1；2 | 原XML第一个fig是Extended Data Fig1，但所选publisher PNG1/2确为主图。图1猕猴解剖/无线监测/ACC与LFP/AI分类四区；图2探针与记录器功能爆炸、实物/尺度/CT支持记录。主文说明customized smartphone app，图中界面只是系统概念示意。 |
| D01 / 2024 | Fig. 1；Fig. 2 | 主图1分子叠合、四类benchmark、底部inference流程；主图2顶部pairformer、左diffusion、右训练曲线、底部训练路径，色语义与直接标签支持。图注给出不同任务的不同metric/n，支持不可跨类型直接按柱高排名。单图notes有EA-02。 |
| D14 / 2014 | Figure 1；Figure 2 | 2014原文Fig1脉冲偏振/绿色LH2与紫色波包/二维谱；Fig2手性pump/probe两行、橙绿截线与右曲线相连。caption把波包称semiclassical、正负为左右圆偏振吸收差；建议发散色标属于审美/解码建议，不是作者数据错误。单图notes有EA-02。 |
| D20 / 2024 | Fig. 1；Fig. 2 | XML依次Fig1、Extended1、Extended2、Fig2；实际record第二图main_figure_02为Neuron categories，并非本地旧figure_02。图1资源生态和神经总览，图2双侧计数、聚合连接与类别形态支持；原caption明确mirror inverted。软件范围及单图notes见EA-02/EA-04。 |

原文位置、精确本地图路径及来源URL见同名JSON的`sample`。

## 具体发现

### EA-01 — 轻微

**位置：** `corpus/b/b_records.json:B05.color_observation`。

颜色概括称白虚线标孪晶/晶界；Fig2a/b用白虚线界定孪晶，Fig2c的晶界实际用白箭头。

**影响：** 不改变图号或科学对象，但降低标记语法复用的精确度。

**建议修复：** 分别写白虚线=孪晶边界、白箭头=独立簇晶界、黑箭头=空位或并合（按具体图）。

**依据：** `corpus/b/B05/figure_2.jpg`；`corpus/b/B05/fulltext.xml:Figure 2 caption`。

### EA-02 — 轻微

**位置：** `corpus/d/d_records.json:figures_viewed[].visual_notes`。

单图visual_notes不是逐图独立记录：第一图条目合并两幅构图/配色，第二图条目主要为两幅综合优点与局限。

**影响：** 整篇composition/color字段与实际图大体一致，但若按单图检索会把图2特征误分到图1。

**建议修复：** 将visual_notes按已记录number拆分；综合分析保留在篇级字段。

**依据：** `corpus/d/d_records.json:D01.figures_viewed`；`corpus/d/d_records.json:D14.figures_viewed`；`corpus/d/d_records.json:D20.figures_viewed`。

### EA-03 — 轻微

**位置：** `corpus/a/a_records.json:A23.source_refs and corpus/a/s41928-023-00950-y/metadata.json`。

当前source_refs仅为原会话turn引用；metadata列publisher figure页，未留实际机构PDF下载URL。已核本地PDF第一页、页3/7的标题、DOI、期刊排版和图号一致。

**影响：** 不构成图文错配；离开原会话后无法精确重取该PDF副本或核对获取版本。

**建议修复：** 补实际下载URL、取得日期和版本表述；保留publisher DOI与图页作为主出版身份。不能凭institution-hosted自动称accepted manuscript。

**依据：** `corpus/a/s41928-023-00950-y/article.pdf`；`corpus/a/s41928-023-00950-y/pdftext.txt`；`corpus/a/s41928-023-00950-y/metadata.json`。

### EA-04 — 轻微

**位置：** `corpus/d/d_records.json:D20.software_evidence`。

Neuroglancer名称确有原始来源，但出现于Methods→Proofreading annotations、致谢、作者贡献；本次查到的角色是校对/注释。当前“正文明确神经可视化平台Neuroglancer”未精确标其来源范围，且不在所声明主文图导向阅读小节中。

**影响：** 不能据此归属最终面板渲染或排版软件。当前记录已将最终排版/导出保留unknown，故不是最终软件误归。

**建议修复：** 明确主文/图1图注明示CAVE等工具生态；若保留Neuroglancer则注明定向补查Methods/作者贡献及proofreading用途，最终图渲染/排版unknown。

**依据：** `corpus/d/D20/article.xml:Methods/Proofreading annotations`；`corpus/d/D20/article.xml:Author contributions`；`corpus/d/D20/article.xml:Fig. 1 caption`。

### EA-05 — 轻微，建议补充限定

**位置：** `corpus/c/c_records.json:C03.limitations; skills/sci-figure-compose/references/layout-strategies.md:C03 case`。

C03 Fig2顶部Day5/10/14×培养法矩阵成立；后段功能/分化图却包含Drop D7与OCTOPUS D14，原图注说明其目的为考察延长培养。篇级记录和技能案例的概括没有复述这一局部限制。

**影响：** 目前没有明说同日因果比较，不判为错误；迁移案例时若一概当成同时间方法对照，可能混合培养时长和方法效应。

**建议修复：** 在案例补一句：顶部为同日矩阵；后段D7对D14用于延长培养效果，重建需逐面板保留day/condition，不把整图假设为等时长比较。

**依据：** `corpus/c/C03/article.html:Fig. 2 caption panels m/n`；`corpus/c/C03/figure_02_full.png`。

## 不应误判为错误的核对结果

- A01原图Fig1的i/j轴内容与图注对不上；记录已经指出。重建应按实际轴名核对，不默默复制源文矛盾。
- A14本地fig3.jpg和fig9.jpg分别对应真正主图2和4，XML中间插入Extended Data；record数字、URL及实际画面相符。底层metadata的number是抓取序号，不能当正式图号。
- C12的首个XML fig是Extended Data Fig1；当前record选取publisher主图1/2完整图，未将首XML图误作主图1。
- D20的本地旧figure_02.jpg不是当前选定第二图；record使用main_figure_02.jpg，画面与Fig2 Neuron categories图注相符。
- B17接受稿Fig6确在PDF页14，不能根据正式版不同图数判该记录不存在或错号。所用版本已标记；本次未独立复查正式版全部图数。

## 9个技能的规则与来源检查

| 技能 | 实际抽查的参考 | 判断 |
|---|---|---|
| sci-figure-director | `references/evidence-index.md:scope and sampled rows`；`references/visual-grammars.md`；`references/brief-contract.md` | 声明89篇为目的抽样、66通读/23定向、Methods/SI逐篇边界；多语法可组合，简单图直接制作。未将顶刊品牌等同质量。 |
| sci-figure-color | `references/color-semantics.md`；`references/diagnostics-and-sources.md` | 分类/顺序/发散/周期/二变量/缺测分开，12色卡标原创起点而非提取或认证。ΔE76、对比值、严重度1模拟与线性RGB均有限定；官方来源支持线性化和周期边界。未复算全部矩阵或色卡。 |
| sci-figure-compose | `references/layout-strategies.md`；`references/examples.md` | 任务决定矩阵/读序与空间不变量，不固定hero/底色；真实图和数据来源独立。C03后段时长边界见EA-05。正文“比较至少两种”是轻微流程强制，可考虑仅复杂布局触发，与director保持一致。 |
| sci-figure-data | `references/task-cases.md`；`references/scientific-checks.md` | 样本/批次、计量口径、寿命工况、双轴、归一和外推有边界；A14探测角度不直接当精确深度，A01 i/j来源矛盾保留。未核全部未抽查案例。 |
| sci-figure-device | `references/routes-and-evidence.md` | 按接触、装配、曲面或多尺度选择2D/3D；未知尺寸不编、爆炸间距不当真实、工具不可用可2D。领域例子的科学结论不称独立确认。 |
| sci-figure-process | `references/cases-and-counterexamples.md` | 过程箭头与时间/物料/因果分开，候选中间体、流路延迟、接受稿版本差异均明确；B01/B17迁移准确。 |
| sci-figure-image | `references/pixels-and-annotations.md`；`references/volume-fields-and-cases.md` | raw/展示副本/分析处理分开，ROI/注册/比例可追溯；负空间非身份鉴定、多模态不同样品不称共定位、每行归一不能比较绝对强度。 |
| sci-figure-mechanism | `references/physics-grammar.md`；`references/task-cases.md` | 空间/能级/k/状态/反应坐标分开，电子与传统电流区别，快PL不等于缺陷少。A23势垒与诊断模拟边界、A14辐射解释均与抽查源相符。 |
| sci-figure-review | `references/review-cases.md`；`references/svg-scan.md` | 科学、视觉、可编辑三项分开；SVG扫描限CSS/视口/字体/元数据且不构成科学证明，无综合分数或投稿成功承诺。未运行scanner或示例。 |

颜色来源的额外定向核查：本地M01原文支持按数据性质选连续/发散/周期等颜色语义；未把它计为第13篇整图抽查。colorspace官方文档明确先线性化RGB，再施加矩阵，再回编码，severity=1对应二色视觉模拟；这些支持技能的实现合同，但不能构成全部读者的色觉可达认证。[官方说明](https://colorspace.r-forge.r-project.org/reference/simulate_cvd.html) · [模拟边界](https://colorspace.r-forge.r-project.org/articles/color_vision_deficiency.html)。[Machado作者修正版](https://profs.ic.uff.br/~laffernandes/content/publications/journal/2009_tvcg_15(6)/machado_oliveira_fernandes-tvcg-15(6)-2009-corrected.pdf)只定向核查模型/矩阵，不称全篇推导复算。

[Matplotlib官方文档](https://matplotlib.org/stable/users/explain/colors/colormaps.html)将顺序、发散与周期色标分开；周期色标检查首尾和局部连续，不能要求整圈明度单调。技能保留这一限制，也未把网页文字对比阈值强塞给全部数据点。未复算全部12色卡、模拟矩阵或演示输出。

正文仍有一处轻微流程一致性建议：compose要求“比较至少两种”布局，而director允许简单图直接做；建议把前者限定于复杂或读序不明确的布局。这不影响本次样本的证据准确性，不作重大缺陷。

## 未审查范围

- 其余77篇及154张所选图未独立重新打开。
- 12篇所有Methods、SI、源数据、统计、物理机理与结果正确性未做完整重算/复制。D20仅为软件归属定向读了Methods/作者贡献相关段。
- 未逐一审查9技能的全部引用、所有外部URL、全部脚本、示例、Blender源、打包安装及技能同步。
- 未独立重新证明66篇主文论证通读/23篇定向阅读的历史过程。
- 未独立核对B17最终发表版全图数量；已验证所用接受稿Fig2/Fig6与其版本标记。
- 未将作者使用的软件从外观推断；unknown不是声明论文任何地方都没有软件名称。

## 交接状态

所有发现已逐项发给root。原始records与skills未修改；修复、定向回查及最终打包由root统筹。本文记录的是审查当时的状态，不预判后续修复已完成。
