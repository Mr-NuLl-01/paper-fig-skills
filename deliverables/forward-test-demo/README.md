# 光电器件前向试用图：DEMO

这张原创草案用于演示如何展示 **3 批、每批 5 个独立器件的处理前后性能与带宽权衡**。所有数值均为自造的 DEMO 端点，不能用作研究结果。真实性能指标、测试工况和带宽截止定义尚未提供，因此横轴使用泛化的 performance index，纵轴的 MHz 范围也只用于布局演示。

## 成品与来源

- `demo_performance_bandwidth.svg`：180 × 104 mm 的可编辑主文件。58 个 live text、34 个命名组，无嵌入位图或外链资产。材料、单个器件的前后端点、配对线、坐标和说明可独立修改。
- `demo_performance_bandwidth.png`：2126 × 1228 px、300 dpi 的查看版。
- `demo_data.csv`：30 行 DEMO 端点，对应 15 个独立器件；包含 sample_id、batch_id、condition、measurement_type、单位和来源声明。
- `make_figure.py`：独立原创生成脚本，只使用 Python 标准库；没有引用技能包中的 DEMO 图、数据或生成脚本。
- `design_config.json`：层序、轴、配对假设、颜色作用域、未知信息和文件关系。
- `layout_routes.svg`：两种结构不同的低保真布局草图。选择紧凑结构区加三批分面，避免在同一散点图中额外编码批次并堆积配对线。
- `review_report.md`、`svg_scan.json`、`runtime_checks.json`：本次有范围的审图记录。

## 读图与图注

**a，层序语境。** 自下而上为 glass / ITO / active film / Au。图仅表达层序，所有厚度未知，非按比例，不得从显示厚度推导真实尺寸。未补加极性、接线、入射方向或材料功能。

**b–d，分批配对权衡。** 每批 5 个独立器件，DEMO 假设同一器件处理前后配对。空心灰圆表示处理前，实心蓝绿色菱形表示处理后；细箭头只表示条件顺序，不代表载流子运动或动力学速率。各面板使用相同线性轴限，每一个端点均保留。两轴“越高越好”仅是 DEMO 定义。未做拟合、均值聚合、误差条、显著性检验或批次间推断。

用户提供的定性证据为稳态光谱变化和稳定性提高。未提供光谱、寿命曲线或转移速率，故图中只列出定性证据边界，不虚构相应曲线，不据此画“载流子转移加快”的机制。该图的科学用途是演示表达方式，不支持任何器件性能结论。

## 重生成

在此目录运行：

```bash
python make_figure.py
INKSCAPE_PROFILE_DIR=/tmp/figure-forward-inkscape XDG_CONFIG_HOME=/tmp/figure-forward-config XDG_CACHE_HOME=/tmp/figure-forward-cache XDG_DATA_HOME=/tmp/figure-forward-data inkscape demo_performance_bandwidth.svg --export-type=png --export-dpi=300 --export-filename=demo_performance_bandwidth.png
```

字体为 DejaVu Sans。Inkscape 成功导出；运行中出现 GtkRecentManager 警告，但进程返回 0，PNG 实际打开后没有缺字或丢对象。未在 Illustrator、Affinity Designer 或其他编辑器中另行验证字体替换行为。
