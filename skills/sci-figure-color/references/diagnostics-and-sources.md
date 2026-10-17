# 诊断方法与适用范围

脚本将sRGB线性化，计算相对亮度Y，并以D65白点转换到CIELAB。两颜色欧氏距离为ΔE76，用于发现相近候选；它不是CIEDE2000，不能证明感知均匀。对比值为(Y亮+0.05)/(Y暗+0.05)，仅报告数值，不把网页文字标准自动强加给数据点。

色觉模拟使用Machado等2009模型在严重度1的矩阵：线性RGB乘矩阵，裁剪色域，重新编码sRGB。记录裁剪分量数。这是预览，不是个体诊断；显示器、纸张、尺寸、读者和布局影响可读性。

连续色标分别检验：顺序L*单调；发散看中心与两侧关系；周期看首尾及邻接连续，不能要求周期L*全程单调或灰度唯一。成熟色标仍需在当前数据与背景下检查。

## 初级来源

- Crameri, Shephard & Heron (2020), The misuse of colour in science communication, https://doi.org/10.1038/s41467-020-19160-7 。本任务读主文并看图1–6，未读SI；采用颜色语义、亮度不均匀和色觉差异依据，不将其流程图当全部情境的硬模板。
- Machado, Oliveira & Fernandes (2009), https://doi.org/10.1109/TVCG.2009.113 。作者修正版：https://profs.ic.uff.br/~laffernandes/content/publications/journal/2009_tvcg_15%286%29/machado_oliveira_fernandes-tvcg-15%286%29-2009-corrected.pdf 。仅定向核查模型/实现，不计入89篇。
- colorspace官方说明，明确使用线性RGB：https://colorspace.r-forge.r-project.org/reference/simulate_cvd.html
- QGIS官方代码中的严重度1矩阵用于常数核对，本脚本不复制其直接sRGB处理：https://api.qgis.org/api/3.28/qgsprevieweffect_8cpp_source.html
- Matplotlib官方色标说明：https://matplotlib.org/stable/users/explain/colors/colormaps.html
- Nature具体阶段要求：https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/ 和 https://www.nature.com/nature/for-authors/initial-submission 。主图、扩展数据、初稿和终稿要求可能不同，重新核对目标，不写成万能DPI或尺寸。

核查日期2026-10-17。诊断不检验数据真实性或机制正确性。
