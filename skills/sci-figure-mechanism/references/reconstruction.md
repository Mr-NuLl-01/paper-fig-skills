# 重建路线与审图

## 自主选工具

- 平面器件、电路、状态切换用参数化SVG或现有矢量工程，分对象/注释/状态/过程图层，保持符号可编辑。
- 能级/能带从真实数据生成坐标，矢量标参考与跃迁；示意梯图写not to scale，不手画伪精确曲线。
- 分子/晶格优先CIF、XYZ或计算坐标与结构工具；装饰球棍不承担物质身份。
- 确有遮挡/接触/曲率问题才用Blender或程序三维，保留正交剖面、尺度和图例；三维不是门槛。
- 光场、密度、等值面使用真实求解数据，保留单位、阈值与色条；生成图不负责精确场。

A15明确披露Setfos光学模拟，其他作图软件未知；上述均为本次建议路线。

为面板保存`representation、coordinate、reference、objects、states、processes、drivers、evidence、limitations`。每条过程给`from、to、entity、direction_basis、evidence_type`；数字保存来源和条件，没有数字则标定性。

先画骨架，再核：层序/极性/晶轴；能量上下及参考；e−/h+/粒子流/电流/电场；箭头端点与源汇；测量/模型/假说和竞争路线。渲染后按目标尺寸实际看上下标、端点、遮挡、图例及图注。

交付SVG/PDF、预览、可重跑源、状态/过程表与来源；不要只交不可改字和箭头的截图。

## 原创DEMO

运行`python scripts/make_demo.py --output-dir /tmp/sci-mechanism-demo`，生成空间输运与能量对齐两个独立DEMO面板，SVG可编辑、JSON给声明。演示刻意分开坐标并标proposed竞争路径；所有值和路线为合成。真实项目必须替换状态、证据与边界，不能只换材料名。
