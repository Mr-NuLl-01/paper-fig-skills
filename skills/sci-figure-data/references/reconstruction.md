# 数据图重建与可编辑交付

## 根据现有工程选工具

- 已有Python/NumPy/Matplotlib或R/ggplot工程：沿用导入、单位和模型，再调整比较逻辑；不为样式重写计算。
- 只有Origin/仪器表：导出真实数据与处理设置，保留原工程，自主选合适脚本重建；无需为工具选择打断用户。
- 复杂拼图：数据保持矢量，显微/热像保留原栅格，在SVG/PDF或矢量排版工具统一单位与索引，不重画像素数据。
- 三维科学数据使用真实坐标/网格与量纲色条，不以装饰透视替代定量。

保留原始数据、处理后长表、变换说明、脚本、SVG/PDF、目标尺寸预览和图注。清单至少给`figure_id、panel_id、source、evidence_type、units、conditions、normalization、n_definition、software_version`。作者披露软件与本次工具分开记录。

只有论文图片时先区分视觉重建与数值复现；无原始数据不声称精确复现，也不从低分辨率曲线编数值。合法数字化保留工具、校准点与估计误差。

## 原创DEMO

运行`python scripts/make_demo.py --output-dir /tmp/sci-data-demo`，生成个体/批次原始点图和参数折中图的SVG、PNG、JSON。全部数值为合成DEMO，文件和图中均明示；两图说明不同任务需要不同表示，不是固定论文版式。换真实数据前重新定义单位、任务与不确定度，不能只换标题。
