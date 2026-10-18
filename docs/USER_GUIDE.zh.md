# 使用手册 · paper-fig-skills 1.1.0

[English](USER_GUIDE.en.md) · [首页](../README.md)

## 从哪里开始

- 看展示效果：[互指电极与埋藏界面](../deliverables/advanced-device-demo/README_zh.md)，即首页主图。含原生Blender和独立SVG标注。
- 看基础到复杂的例子：[新版案例画廊](../examples/gallery/README.md)。数据与结构全部为明确模拟或概念示意。
- 选颜色：[配色HTML](../deliverables/color-atlas.html)、[SVG色表](../deliverables/color-atlas.svg)、[JSON参数](../deliverables/color-atlas.json)。类别色和连续色阶用途不同。
- 学表达方法：[26页原研究手册](../deliverables/scientific-figure-handbook.pdf)、[论文图谱](../deliverables/paper-atlas.html)。保留2026-10-17的阅读范围与历史状态，不当作本轮重新完成的调研。

GitHub普通文件页会显示HTML源码。下载仓库后用浏览器打开HTML，可离线浏览和筛选；论文原始链接需联网。无需开启GitHub Pages。Markdown、图片和PDF可直接在GitHub查看。

## 目录与职责

| 目录 | 内容 |
|---|---|
| skills | 九个稳定技能ID，中英文入口、参考资料与原有脚本 |
| examples/gallery | 本轮模拟案例、生成代码、数组、可编辑图及运行记录 |
| deliverables/advanced-device-demo | 原互指电极增强案例，首页主图来源 |
| deliverables/forward-test-demo | 原项目记录的独立前向试用案例 |
| deliverables | 原研究手册、论文/配色图谱、构建辅助脚本 |
| review | 原项目有范围验证记录，均保留历史日期 |
| docs | 当前使用指南、导入说明与历史清单 |
| tools/font-assets | 随原包保留的字体许可说明，不包含独立字体文件 |

## 导出一种语言，再安装

在仓库根目录执行：

```sh
python scripts/export_skills.py --language zh --output ../paper-fig-zh
```

英文用`--language en`。目标目录必须不存在，脚本不会覆盖旧目录，也不会安装或更改模型设置。英文导出将`SKILL.en.md`作为入口，并保留中文副本；所有相对引用的资产、参考资料和脚本一起复制。

将导出目录中的九个`sci-figure-*`文件夹复制到客户端实际识别的技能目录。沿用仓库现有安装说明时用户级目录为`$HOME/.agents/skills`，Windows为`$HOME\.agents\skills`；旧版或自定义环境先核对实际目录。同名技能更新前比较和备份，只安装一种语言版本，不要重复安装两个同名技能。下载仓库不等于安装完成，必要时刷新或重启技能发现。

## 给任务什么输入

提供：图要回答的问题、原始文件及列名、单位、样本/批次定义、观测/计算/假说边界、最终物理尺寸、需要的可编辑格式。不要只说“画得像顶刊”；让工具围绕具体科学比较选择表示。

```text
仅使用paper-fig-skills中的相关技能。
请先读取sci-figure-director以及所需专项模块。
问题：变化是普遍发生，还是由少数离群器件造成？
输入：CSV中的device_id、batch_id、before、after及单位。
保留配对、个体点、批次层级，不补造数值。
交付180mm宽的SVG、PDF、PNG，以及代码和数据。
实际打开导出图检查，并记录真实可核实的模型与推理档位；不可见就写未知。
```

没有真实数据而只想测试能力时，应明确要求模拟示例。不要把概念曲线、粒子数量或假设能级包装成实测结果。

## 按任务选择模块

- 配对/分布：data＋color＋review。箱线、半小提琴和散点可组合；写清四分位、须和带宽。小样本不必强行平滑成分布。
- 器件：device＋compose。先确认层序、接触与路径，再选择二维剖面或三维。爆炸间距与厚度夸张要说明。
- 机理：mechanism。区分空间与能量坐标，核对箭头起终点、电荷/电流及竞争路线。
- 生长：process，必要时配device或image。保持样品和状态ID，不将概念多面体认作真实晶面。
- 热图：data＋color。控制共同色阶、零点、缺测与归一化。发散色图须有有意义的中心。
- 堆叠/瀑布：data＋image＋compose。第三坐标可能是温度或时间，不能当成空间深度；保留不等间距，配二维视图方便读数。
- 体图：image。保存体素、轴序和切面位置，检查交叉切面的实际遮挡。
- 非等大组合：compose。按证据的重要性分配面积，保持读序和相关坐标一致。

复杂视图的具体规程在[专项参考](../skills/sci-figure-data/references/stacked-views.md)。简单任务不必全量加载全部资料。

## 复现新版案例

```sh
python -m pip install -r examples/gallery/requirements.txt
python examples/gallery/generate.py
python examples/gallery/check.py
```

这会生成八类基础视图并覆盖gallery/output内的对应文件。已确认的三维补图和最终生长合版按以下顺序生成：

```sh
blender -b -t 2 --python examples/gallery/device3d.py -- --out examples/gallery/output/device3d
python examples/gallery/compose3d.py
blender -b -t 2 --python examples/gallery/growth3d.py -- --out examples/gallery/output/growth3d
python examples/gallery/compose_growth.py
python examples/gallery/check.py
```

先运行基础生成器，生长脚本需要它输出的共享多边形坐标；合版脚本最后运行。Blender脚本清空的是独立后台进程场景，不要放到未保存的交互工程内运行。本轮新例在Blender 4.3.2检查，原增强例记录为4.5.0。原生层、晶域、材质、集合与相机可编辑；SVG中的渲染图不是原生三维，文字和二维标注仍可独立修改。

本轮仅使用这套科研绘图技能和常规代码/Blender工具，没有调用其他科研绘图技能或图像生成模型。具体模型ID和推理档位当前未暴露，运行记录如实记为未知，不冒称指定型号测试。

## 原始资料的使用与重建

原完整归档151文件，原71技能文件已在先前导入。此次补齐其余配套内容，不用旧技能覆盖当前更新。详见[归档导入说明](ARCHIVE_IMPORT.md)。

- 论文图谱直接打开HTML或读取JSON/CSV。用`python deliverables/rebuild_public_atlas.py --out /实际新目录/atlas.html`可从交付JSON重建。无可选独立字体时改用系统字体，原自包含HTML保持原样。
- 配色构建脚本`make_color_atlas.py`会改写旁边的配色产物，如要保留原件，请在工作副本内运行。
- 研究手册PDF直接可读。重新排版需要ReportLab及本地有许可的CJK TTF：`python deliverables/build_handbook.py --font-regular /实际/regular.ttf --font-bold /实际/bold.ttf`。不自动下载字体；本轮检查了命令入口，没有重排这份历史手册。
- 原案例保留原README和检查记录。配套教学案例与独立技能测试分开标注，不回填缺失的历史模型信息。

## 验收与改作真实研究

按最终尺寸检查文字、坐标、单位、颜色身份、箭头、缺测、样本定义、裁切和导出。确认数值图可从表或数组重建，原生结构能独立修改。自动检查不替代机制验证。替换真实数据后必须重新审查科学含义，不得像模拟示例一样为美观改值。
