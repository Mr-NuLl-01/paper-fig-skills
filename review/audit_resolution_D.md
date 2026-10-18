# D组审查问题修复记录

日期：2026-10-17。修复范围：D组逐图观察，以及D20软件证据归属。

## 完成内容

对当前D组17篇的34幅选定整图实际逐幅查看；其中D01/D14/D20的6图此前已在独立12篇抽查中打开，本次再查看其余28幅，并按本地原始XML选定图label/图注定向核对身份与术语。这项工作是对逐图视觉观察的修复，不代表17篇全文、Methods、统计或科学结论均经独立审计。

### EA-02：逐图visual_notes已拆开

原生成器把“整篇composition＋color”写进第一张图、把“整篇strength＋limitation”写进第二张图。现为全部17篇编写34条独立观察，每条仅说明对应图的布局、对象、颜色和必要的局部解读限制。篇级分析仍保留在composition/color_observation/strengths/limitations中。

新增`corpus/d/figure_observations.json`作为生成源：每条同时记录正式number、实际asset文件名与note。`tools/finish_d.py`按该源生成记录，并要求17篇覆盖一致、每幅标签/文件名匹配、数量一致；不允许默默回落到旧的篇级拼接方式。

| ID | 第一幅独立观察 | 第二幅独立观察 |
|---|---|---|
| D01 | 分子叠合—分任务benchmark—inference总图 | pairformer—diffusion—训练路径—训练曲线 |
| D02 | 双支路筛选/DFT反馈、数量历史与6个晶体 | 稳定晶体/原型数量、相分离能及r²SCAN验证 |
| D03 | 自编码器与latent DeepONet双层工作流 | 三物理问题的小提琴误差与模型比较 |
| D05 | 断层切片—分类体图—六模板/得分场；修正膜品红 | 滤波/掩膜参数、微管旋转重叠与自相关 |
| D06 | 采集流程、透明装置、扫描序列与正交体图 | 多角融合、时间解混、去伪影及量化 |
| D07 | Au–Fe₃O₄超晶格HAADF/EELS与融合体 | Co₃O₄–Mn₃O₄核壳模态矩阵、切片与线剖面 |
| D08 | 偏振X射线光路、四倾角、投影及相位差 | 密度、取向短棒/色轮、分割和晶粒统计 |
| D09 | 神经符号循环、简单几何与缩写奥赛证明 | 单指标柱图及人类成绩折算限定 |
| D10 | 零温相图、交叉与缩放塌缩 | PBC/APBC和Euclidean τ平台；不称实验实时 |
| D11 | Corbino装置、环域主流线/差场和压力 | 侧支压力计、流线及不同范围压力差 |
| D12 | 信息datacube映射/重建循环 | 光谱和时间光路/剪切；区分实测场和时间块示意 |
| D14 | 脉冲偏振、LH2半经典波包和有符号谱 | 二维手性谱橙/绿截线与对应一维谱 |
| D16 | 自编码器、候选矩阵、稀疏系数与loss | 三系统的观测—方程/轨道—系数矩阵 |
| D17 | 完整与子采样数据的PDE-FIND两路 | Brownian轨迹、位移分布和序列长度/识别误差 |
| D18 | 动力核心与学习物理产生倾向及反馈 | 四指标行、三变量曲线和双模型地图/掩膜 |
| D19 | 原始断层、分类体图和不同条件组成比例 | 四构象侧/顶成对视图和开口几何 |
| D20 | 全脑/资源/工具生态及电镜定位；保留镜像限定 | 真正Neuron categories主图2；双侧计数/聚合边权/类别形态 |

### EA-04：D20软件证据已收窄

主文/图1图注的工具生态为CAVE、CAVEclient、navis、fafbseg、natverse与浏览器工具；Neuroglancer的具体证据来自定向查阅Methods > Proofreading annotations段落、致谢及作者贡献，所述用途为校对/注释。记录现明确这些证据均不指定最终面板的渲染、排版或导出软件，后者仍为unknown。

D20新增`targeted_read_scope`，记录目的为software attribution only、具体查阅段落、本地XML来源、日期与审查角色。`methods_read=false`、`supplement_read=false`和`read_scope=FIGURE_FOCUSED_MAIN_TEXT`保持原来的有限含义，没有升级为完整Methods阅读。

### 同步纠正的两处篇级颜色精度

- D05：图1膜的颜色由错误的“黄色膜”改为“膜品红”，核糖体改为更贴合画面的黄绿；已同步raw源、observations与records。
- D20：删除“节点大小与边宽有单独数量图例”中的未获此图支持部分，改为“聚合图的边宽有Synapses数量图例”。可见边宽图例保留，未为节点大小补造图例。

## 修改文件

- `tools/finish_d.py`：读取独立逐图源；标签/asset校验；D20软件证据与targeted_read_scope；上述两处颜色语句。
- `corpus/d/figure_observations.json`：新增17篇/34图的逐图观察源。
- `corpus/d/observations.json`：生成源中的D05、D20颜色概括更新。
- `corpus/d/d_records.json`：34个visual_notes、D05/D20篇级颜色、D20软件证据与定向阅读范围。

## 实际验证

已运行`python figure-atlas/tools/finish_d.py`，生成17篇/34图。随后逐项检查：34条record文本与独立源相等、正式label存在于对应原始XML、asset与当前选定路径一致且存在、每篇methods_read仍为false、D20保持图导向主文范围且第二图仍选`main_figure_02.jpg`。这些是有限的一致性检查，不是科学证明或全部图像质量认证。

实际观察包括完整整图；原始压缩JPEG中较小文字仍有分辨率限制。新笔记不据缩略字形评价原印刷稿字体质量，不从外观推断软件。

## 保留与未做事项

原始`review/evidence_audit.md`和`review/evidence_audit.json`作为审查当时记录保留，未改其发现或覆盖声明。该报告的EA-02、EA-04在本次D组修复范围内已处理；A/B/C及compose案例的后续修复由root和对应任务处理。

没有重新审读全部17篇主文、Methods或SI，没有复算研究结果或统计，没有新增论文或图数，没有重新生成director atlas、skills或打包产物。root可在各组修复完成后统一再生成atlas。

残余：本次未做第二位审查者对新34条笔记的再审；最终交付atlas需由root从修复后的records统一更新。
