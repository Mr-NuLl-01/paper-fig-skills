# 科学绘图证据图谱与新技能手册

## 从89篇论文、178张整图到按科学任务选择的绘图系统

研究与记录日期：2026-10-17。版本：1.0，已完成内容编写、实例制作与有范围验证；技能目录安装及远程git同步尚未完成。

本项目的主要成果是一套由九个模块组成的科学绘图系统。它根据读者需要理解的关系选择表示方式：器件的空间关系、材料的状态演化、实验的操作与观察、样本之间的差异、物理量的连续分布，分别采用不同语法。设计目标是提高证据的可读性、表达的准确性、画面的完成度与后续修改能力。复杂度、三维效果或某种配色不单独构成质量标准。

已审读89篇不同DOI的原始研究论文，实际查看178张选定完整图。66篇连续阅读主文科学论证与结语，23篇进行图导向的相关正文精读；未把全部Methods、SI或论文所有图像记为已读。每篇的具体阅读范围、实际图号、来源、视觉观察、优点、局限和建议重建路线均保留在配套图谱中。

配套文件中，paper-atlas.html用于逐篇检索、筛选和展开阅读；paper-atlas.csv与paper-atlas.json用于再分析。color-atlas.html包含12组原创离散配色、14种连续色图候选，以及每组配色的有限色觉与灰度诊断。论文原始图像与全文不随成果分发，图谱保留原始来源链接。

## 1. 阅读了什么，能得出什么结论

### 1.1 样本覆盖

| 科学任务 | 论文数 | 主要观察对象 |
| --- | ---: | --- |
| 发光材料与LED | 12 | 层状器件、能级、光谱、效率与稳定性 |
| 光电探测、晶体管与神经器件 | 12 | 接触结构、器件状态、传感与计算数据 |
| 成核、生长与材料加工 | 16 | 原位时序、物种变化、晶体形貌、制造过程 |
| 催化与电池原位表征 | 8 | 反应界面、脉冲响应、谱像与化学赋值 |
| 微流控、类器官与组织芯片 | 8 | 流路、几何改造、培养条件与观察位置 |
| 可穿戴与植入式生物电子 | 6 | 多层系统、组织界面、功能与实体照片 |
| 软体机器人与致动 | 6 | 制造、流体控制、结构和运动 |
| 水凝胶与生物黏附 | 4 | 界面、网络、轨迹和黏附测试 |
| 科学计算、动力学与理论 | 9 | 模型结构、方程、训练与验证、相图 |
| 成像、光谱与结构解析 | 8 | 原始影像、重建、切片、体场与频谱 |
| 合计 | 89 | 每篇实际看2张选定整图，共178张 |

样本发表年份为2014—2025，覆盖15种期刊。Nature Communications占47篇，Nature占12篇，Science Advances占8篇，PNAS占5篇；其余包括Nature Methods、Nature Materials、Nature Biomedical Engineering、Nature Electronics、Nature Catalysis、Nature Nanotechnology、Nature Biotechnology、Science及ACS期刊等。

这个分布有明显的开放获取与材料/器件方向偏重。它是为获得不同视觉任务而构建的目的性样本，不能代表各领域论文的真实比例，也不是截至2026年全部最新研究的穷尽系统综述。本文没有声称这些论文的图都优秀，也没有把期刊名称当成审美合格证。

### 1.2 检索与阅读方法

检索围绕任务簇展开，并用代表性论文的相关工作继续扩展。例如，器件簇组合LED、photodetector、transistor、interface和device structure；生长簇组合nucleation、in situ、crystallization、growth与operando；交叉簇覆盖microfluidics、organoid、soft robot、hydrogel与implant；计算和成像簇覆盖scientific machine learning、tomography、spectroscopy、cryo-ET、connectome与field visualization。来源优先为出版社正文与图页、Europe PMC/PMC原文、作者或机构公开副本。

实际计数要求同时存在可读科学上下文与已查看的完整图像。仅看到搜索摘要、图题、缩略图，或无法取到所需正文的候选，不计入89篇。读图以整幅多面板图为单位，每篇选择两张能够揭示主要表达策略的图；它们不是从178个单独子面板凑成的数目。

每篇记录以下问题：图在回答什么科学问题？各面板如何组织证据？颜色表示身份还是数值？作者如何连接结构、原始观测和解释？哪些细节提高效率，哪些细节增加误读？若重建，应选择何种数据结构与工具路线？作者实际最终绘图软件是否有明确来源？

阅读层级始终保留。66篇的“主文通读”不自动包含全部Methods；23篇的“图导向精读”不被升级为整篇通读。额外阅读的Crameri等颜色方法论文及Machado色觉模型来源不计入89篇原始研究。已读论文有接受稿或机构副本时，记录具体版本；同一DOI的版本差异不增加篇数。

### 1.3 评价方法

评价采用有来源的定性判断，没有虚构“高级感85分”之类标尺。科学结论、图形表达和重建建议分别陈述。我们能够评价已看图中的层次、标记、比较条件和解释成本；没有重算所有原始统计，也没有独立复现实验或证明所有机理。

| 评价维度 | 具体问题 | 应留下的证据 |
| --- | --- | --- |
| 科学语义 | 箭头、坐标、颜色与形状是否表达正确关系？ | 定义、单位、对象身份、实测/模型/假说范围 |
| 比较效率 | 读者能否直接比较需要比较的项目？ | 相同尺度、条件、时间、样本单位与对照 |
| 信息层次 | 首先看到的内容是否是主要结论的证据？ | 面板面积、视觉权重、读序与局部放大 |
| 视觉完成度 | 缩至目标尺寸后，线条、标签和影像是否清楚？ | 实际导出与目视检查，不只源文件参数 |
| 数据与图像完整性 | 处理、裁切、映射是否保留可追溯性？ | 原始来源、处理记录、ROI、色域与缺失值 |
| 可维护性 | 能否改数据、标签、结构和视角而不重画全图？ | 矢量对象、图层、脚本、参数与三维源文件 |

## 2. 对现有nature-skills的具体判断

本次检查了Yuan1z0825/nature-skills公开仓库当日可访问的nature-figure内容。没有取得用户本机安装版本的完整实现，因此以下评价针对公开版本，不能自动归到用户正在使用的那一版。

公开版本并非只有一组Matplotlib参数：它已经区分定量图、示意图、影像组合等路线，也重视可编辑文字、最终尺寸、导出和检查。这些原则值得保留。问题主要出现在局部默认值被当成广泛适用的视觉规范时。

例如，公开矢量示意规则对饱和颜色数、红色用途、白色画布、渐变和三维效果、正交连线等设置了共同默认值。该文件也允许在图的科学故事需要时例外，并要求在简报中说明；这里评价的是这些默认值的适用范围，而非把它们说成绝对禁令。这些限制对紧凑的方法流程图可能有效；当任务变为组织中的植入结构、多组分材料、角度场或弯曲微流路时，就容易损失必要语义。偏向主视觉加附属面板的构图，也不总适合等权的时间×条件矩阵。[外部来源E01、E02]

新系统把这类规范改为带条件的选择：颜色数量由必须区分的身份决定；三维由空间遮挡和界面关系决定；渐变由连续物理量或受控材质表达决定；曲线连线由真实拓扑决定。仍然要求克制，但克制的是无信息的视觉干扰。

Python不导致粗糙。它既能生成精确数据图，也能驱动SVG、三维几何和参数化布局。问题常发生在表示方式未被认真选择、材料几何缺少细节、默认配色被机械复用、最终尺寸没有检查，以及编辑源与证据来源脱节的时候。

## 3. 可以迁移的14种视觉语法

“视觉语法”指对象与关系的组织方式。它不规定所有稿件用相同模板。下面每条均给出适用问题及停止使用的条件；同一张复合图可以合理组合数条。

| 语法 | 适用问题与样本线索 | 何时更换表示 |
| --- | --- | --- |
| 简洁点图、柱图或折线 | 少量明确比较；D09的基准成绩图 | 分布、配对或批次本身重要时，不能只剩均值 |
| 条件×时间或参数矩阵 | C03培养方法与时间；D18模型与指标 | 面板条件不匹配时须逐项标明，不能假装统一实验 |
| 因果/状态网络 | 物种转换、反应支路、器件工作状态 | 只有相关证据时降低因果强度，保留候选路径 |
| 能量/自由能图 | A23离子状态与能垒；能级排列 | 横轴不是空间距离时不得画成运动轨迹 |
| 二维剖面 | 层序、接触和界面；薄膜器件 | 关键关系在平面之外或被遮挡时补三维视角 |
| 爆炸结构图 | C12异质功能层与装配；材料身份 | 主要问题只需层序时，爆炸间距会浪费面积 |
| 三维体场＋切片 | D07、D08化学/取向重建 | 缺少真实体数据时不能把概念渲染当重建结果 |
| 操作—观察对照 | B20谱像装置；C02观测位置 | 设备外观不影响读数时，不应占据主要面积 |
| 阶段演化/时间序列 | B01、B05、B07生长与成核 | 来自不同对象的帧不能画成同一物体连续轨迹 |
| 原始—推断—量化 | D05、D06、B20成像与分析 | 分割结果不能覆盖原始像素；谱库约束必须保留 |
| 多尺度关联 | 组织—器件—微结构—局部性能 | 放大框没有真实对应ROI时，应明确为概念关联 |
| 轨迹、分布、残差与权衡 | D16/D17动力学；A组批次和多指标 | 一个冠军值不能代表多目标取舍或失败区域 |
| 聚合网络与分组结构 | D20连接组 | 全图边线不可读时做聚合、分层或交互，不靠再加颜色 |
| 方程—矩阵—模型对应 | D16/D17稀疏模型；科学计算流程 | 系数存在性与系数大小要用不同图例表达 |

这些语法保留了简单图的价值。一张只有几根柱子的图可以准确回答一个问题；一张三维结构图也可以因遮挡而失败。选择的依据是读者需要恢复哪些关系，而不是给所有图统一增加细节。

## 4. 代表性论文的深入读图结论

### 4.1 器件性能应有分布和代价：A14

A14《Acceleration of radiative recombination for efficient perovskite LEDs》的主图2把结构、性能曲线、70器件的峰值EQE分布和寿命放在同一证据组中。它的价值在于把冠军表现、可重复性和工作稳定性连在一起，而不只突出一条最好曲线。

正文同时给出一个必须保留的边界：该条件下寿命与对照接近，并非与效率一起提高。因此，重绘不能因为标题强调效率，就把机理图、配色和箭头全部改成“各方面更好”。图2的统计分布也仍不能代替批次、制造过程和每个原始样本的登记。迁移到data模块的规则是：凡性能改进涉及分布、重复性或代价，优先保留这些维度。[A14]

### 4.2 时间序列的高级感来自对象可追踪：B05

B05使用连续AFM影像观察分子簇。棕金影像本身已经承载强度和形貌，不需要额外以大量彩色描边重画所有分子。图2a/b的白虚线标孪晶边界，图2c的白箭头标晶界，图2a的黑箭头指空位；图5以白实圈/虚圈及I—IV编号追踪不同簇，黑箭头另指并合。逐图定义标记，读者才能追踪相同对象及不同事件。

原图还指出部分簇通过并合变化，不能把全部过程概括为单体附着。AFM扫描本身需要时间，帧的时间与扫描方向也影响“同时性”。迁移规则是：过程图必须保留对象身份、操作时点和观测时点；示意序列与实际观测序列分开，避免为了连贯故事补造中间状态。[B05]

### 4.3 材料生长需要“物种—状态—形貌”三层解释：B01、B07

B01分别组织物种变化和形貌形成，显微时间序列通过圈选保持局部对象对应。B07进一步把不同状态中的相对物种量与微观示意相连，让读者理解胶体、游离离子和晶体之间的关系。

这类图能比“溶液→晶核→大晶体”三格流程提供更多机制内容。但浓度条、粒子数量与示意曲线若不是测量值，就必须明确不按比例，不能据图形长度反推化学计量或守恒。生长模块因此要求先识别控制变量、被观察状态和证据，再决定是否需要分支、连续阶段或局部放大。[B01、B07]

### 4.4 原始噪声也是表达的一部分：B17、B20

B17接受稿的时域图保留浅色原始波动，同时显示处理后的趋势；脉冲时段使响应尾部具有可解释的时间参照。其候选络合与表面重构机理综合了间接证据和计算，图示不等于直接观察到每个分子步骤。该接受稿与最终版的图数不同，重建时必须带版本引用。[B17]

B20把ROI、谱像和对应光谱连接起来，让化学赋值能返回影像位置核对。其组分识别受参考谱库约束，扫描慢轴同时带有时间含义。迁移规则是：保留原始层、推断层和量化层，写清谱库、阈值、采样顺序和映射范围。[B20]

### 4.5 条件矩阵必须逐面板核对：C03

C03的几何改造图使用切开与展开说明培养几何；主图2上部按培养法与Day5/10/14组织比较，结构具有很高的阅读效率。这个矩阵形式可以迁移，但后面的功能比较不能自动继承“同龄”的解释。

具体而言，图2m有Drop D7、OCTOPUS D7、OCTOPUS D14三个条件；图2n的葡萄糖诱导Ca²⁺响应比较为Drop D7与OCTOPUS D14，用来考察延长培养的贡献。于是新compose模块要求day与condition逐面板登记。整齐布局只能呈现实验设计，不能替实验制造匹配。[C03]

### 4.6 三维在功能层与界面问题中确有用途：C12、C24

C12的层状神经记录系统用爆炸视图解释各层功能，再用光学照片和植入影像说明实体存在及位置。三维承担的是空间组织；功能文字对齐相应层，才能让分层不止是漂亮的叠片。设备渲染的拟真程度不能充当神经功能或生物相容性的证据。[C12]

C24将制造步骤、材料性质、打印几何和实体机器人连接。图2a本身包含红/蓝埋入通路；同一页右栏图3则承担流体控制、等效电路和时序解释。跨图版本或整页截图检索时，必须按正式图注重新辨认对象。迁移规则是：先选择装配、制造或工作原理这一个读者问题，再给它对应的空间视角。[C24]

### 4.7 真正的体数据需要切片约束：D07、D08

D07的多模态化学断层成像使用体重建配合切片、频域覆盖等证据。其主图2以不同颜色区分Co₃O₄–Mn₃O₄颗粒的核心与外壳，并给出切面和线剖面；三维是科学结果本身的一部分。只保留一个平滑透明体会丢失分辨率、局部成分与覆盖范围的问题。[D07]

D08还区分电子密度、取向和分割。取向属于有周期结构的变量，循环色图与方向杆配合具有合理语义；这与用不均匀彩虹色表达普通幅值不是同一个问题。image模块要求体场提供坐标、切片位置、色标及单位，并保留模型、重建与原始测量之间的层级。[D08]

### 4.8 小样本不因平滑而增加证据：D03；简单图也能有效：D09

D03部分小提琴图反映五次训练重复。平滑密度轮廓有视觉吸引力，但样本很少时容易产生超出数据的信息感；新data模块优先让重复点可见，并说明汇总或密度估计的范围。[D03]

D09的几何推理论文使用普通柱图比较基准成绩，复杂度很低但任务明确。需要注意的仍是分数定义和不同参照的可比性，而不是把柱子改成带透视的立体图。这是本项目保留简洁语法的重要反例。[D09]

### 4.9 一个统一热图可能掩盖量纲差别：D18

D18把不同气象变量、误差曲线和空间分布分组组织。多模型、多变量或多工况结果虽然可以排成规则矩阵，却不应因此默认共享一个数值色标。新compose与color模块要求明确哪些面板可共用轴限和色域，哪些必须保留各自的单位与范围。缺失/遮罩另有含义，不能默认为零。[D18]

### 4.10 密集网络应改变抽象层级：D20

D20连接组图把完整结构、数据资源、聚合连接和分组形态结合。全脑画面传达规模，但局部结构的比较依赖后续聚合或分组。关系过密时，再增加颜色通常无法解决边线相互覆盖；应改变聚合层级、只显示必要子图或采用交互。

视觉解释仍要贴近图例：聚合边宽具有Synapses数量图例，不能无依据地给节点大小附加另一套定量含义；解剖连接计数也不自动等于生理效应强度。来源中的Neuroglancer用于校对/注释的证据，与最终图像排版软件是不同角色。[D20]

## 5. 颜色体系：扩展选择，也保留语义

### 5.1 四种用途分别处理

类别色区分材料、样本、物种和条件，通常不暗示大小。顺序色表达有序强度、浓度或其他连续数值，应检查亮度结构与局部对比。发散色表达相对于有意义参考值的正负偏差，应登记中心和两侧范围。周期色用于首尾相接的角度或相位，必须说明周期。[E03、E04]

材料颜色和数据颜色可以在同一图中共存，但需要作用域。例如，金色只在器件结构中表示电极，数据区用靛蓝/铜色表示不同条件；不能让一个读者必须连续追踪的对象在面板间无解释地换色，也不能要求全稿所有不同物理量共享同一种色标。

显微伪彩应与通道和映射绑定。原始影像、分割掩膜、标注线、ROI与误差显示是不同层。黑色背景可以合理服务于发光、频谱或体数据；浅背景也可以服务于曲线与结构。背景由信号和最终载体决定，不强制所有面板全白。

### 5.2 12组原创离散配色

下表配色为本项目原创起点，没有从论文像素反推所谓“顶刊HEX”。它们不限定学科，也不要求每次使用全部五色。图中只需要两类时可取适合的两色；多类别任务可选择其他组合、分面或直接标注。

| 名称 | 五个候选色 |
| --- | --- |
| 靛蓝与铜 indigo-copper | #334E8C · #C77945 · #759891 · #90648C · #48515D |
| 梅紫与青瓷 plum-celadon | #6F496C · #4A8C83 · #BF9A50 · #566A8A · #BB6974 |
| 森林与玫瑰 forest-rose | #34715D · #B85F79 · #8C742E · #5B7598 · #6F617A |
| 钴蓝与朱红 cobalt-vermillion | #255FB1 · #C6513D · #358E91 · #9069A4 · #8C784B |
| 赭石与湖蓝 ochre-lagoon | #A9792A · #2D7F99 · #8A4C69 · #4D7B57 · #786CA0 |
| 浆果与橄榄 berry-olive | #A03E68 · #6F823D · #517DA4 · #C07B53 · #5B596A |
| 海军蓝与薄荷 navy-mint | #263E66 · #3A9589 · #BC728F · #A88640 · #817C9F |
| 陶土与青蓝 terracotta-cyan | #AD5A4E · #338D9D · #58669A · #829252 · #98638B |
| 紫罗兰与黄绿 violet-chartreuse | #7557A3 · #82933B · #B96659 · #307D8C · #785F4F |
| 石墨与藏红 graphite-saffron | #404B58 · #BA8530 · #348780 · #9C587B · #536DA0 |
| 海蓝与酒红 marine-burgundy | #2D7192 · #853E59 · #85884A · #BD7658 · #626698 |
| 鼠尾草与鸢尾 sage-iris | #627C60 · #776397 · #B46C55 · #3F8495 · #A27685 |

连续色图候选共14种：顺序色viridis、cividis、magma、inferno、Blues、Purples、YlGnBu、YlOrBr；发散色RdBu_r、BrBG、PuOr、PRGn；周期色twilight、twilight_shifted。这些是已存在的Matplotlib色图名称，不能说成原创，也不能把离散五色卡直接插值后当作科学连续色标。[E04]

### 5.3 诊断实际做了什么

配色脚本使用sRGB D65、线性相对亮度和CIELAB，色差为ΔE76而非CIEDE2000。三种色觉模拟采用Machado 2009严重度1矩阵，在线性RGB中作用，超出色域的分量截断后再编码回sRGB，并记录截断数量。灰度从线性亮度得到。它不会修改研究数据或原始影像。[E05]

12组五色组合的原始最近色对ΔE76范围为15.673—29.675；在部分有限模拟中，最近色对降至约2.5—3.6。灰度最近色对范围为0—1.175，意味着不少等权类别在灰度中相近。这里没有设定通用通过阈值，这些数值也不能代表细线、字体、邻接颜色、打印环境或全部观察者的实际可辨性。需要保留身份时，应增加形状、线型、直接标签或分面。

独立器件试用中的两状态色诊断也发现差异缩小，最终因此同时采用空心圆与实心菱形。颜色诊断的价值在于暴露具体风险并改变表示，而不是给色卡盖一个“安全”章。

## 6. 工具路线由对象决定

| 对象与任务 | 建议制作路线 | 必须留下的可编辑来源 |
| --- | --- | --- |
| 数值、统计与频谱 | 数据整理→适当统计表示→脚本导出矢量图 | 原始表、处理代码、单位、参数、SVG/PDF |
| 状态、流程、能量与关系 | 先写语义/对象ID→SVG或其他矢量编辑 | 独立文字、线、箭头、图层与符号定义 |
| 层状结构、加工几何 | 二维剖面或参数化三维；必要时并列顶视/剖视 | CAD/Blender等原生几何、相机、材质、SVG标注 |
| 原始显微/谱像 | 保留原图→可追踪处理→单独标注→量化 | 原始像素、ROI、标尺、映射和处理记录 |
| 真实三维场 | 体数据渲染＋切片/方向/定量；可采用专业体可视化工具 | 数据、坐标、色域、传递函数、切片和视角 |
| 化学/分子结构 | 根据明确结构式或坐标，用对应结构工具产生图元 | 原始分子定义、构象/坐标、标注与视角 |
| 多类型论文复合图 | 各面板独立制作→统一语义与物理尺寸→矢量合版 | 面板源、布局源、字体、图层与最终预览 |

这里的工具名称是建议，不是作者软件溯源。来源未明确时，作者最终作图软件记为unknown。一个图注声明某个子图使用BioRender，不应外推到整篇；数据处理、三维重建、校对平台、最终渲染和版面合成也须区分。

真实体场可以考虑ParaView等专业可视化工具；Blender用于参数化器件和可控空间视角，SVG适合保留可改的文字与线条。本项目实际运行了Python、Inkscape和Blender；没有声称上述所有候选软件都已在本环境安装或验证。[E06、E07]

图像生成可用于明确标为概念的辅助插画或视觉探索，但不能代替真实显微图、数据点、精确结构或可核查的物理路径。含精确标签、材料接触和数据映射的主体应保留可编辑、可追踪来源。本轮用于交付的科学示例由标准绘图与三维工具制作。

## 7. 九个新绘图技能的实际职责

### 7.1 sci-figure-director：任务判断与路由

输入研究目标、数据/影像/结构来源、目标载体与已知限制。先明确图的一句话科学任务，再登记证据、观察单位、比较条件、坐标/尺度、颜色身份、未知信息与导出要求。根据对象加载必要子模块，不默认全部模块，也不把工具选择变成不必要的用户问答。

输出包括可审查的设计简报、选用语法、模块路线和待保留的证据边界。复杂复合图或读序不确定时比较不同低保真布局；清楚的单面板直接制作并说明选择。缺少真实数据时用占位或明确DEMO，未知厚度不补造数值。内含14种语法、89篇证据索引和完整可移植图谱。

### 7.2 sci-figure-data：统计与实验数据

先识别观察单位、重复层级、配对、批次、删失/缺失和工况，再选择散点、配对、分布、轨迹、响应面、残差或多目标权衡。样本少时让点可见；均值、误差条、密度、归一化和拟合必须有定义。冠军值不代表分布，技术重复不自动当独立样本。

交付数据表、计算脚本、表示理由、轴和统计定义，以及可编辑矢量图。已有原创批次配对与多目标权衡示例，所有数值明确为DEMO。其目标是让数据表示服务于结论和边界，而不是统一改成小提琴或漂亮的散点。

### 7.3 sci-figure-mechanism：机理、状态与物理关系

建立实体、状态和有类型的箭头表：输运、反应、能量跃迁、操作顺序、信息传递和假说不能混用。先区分位置轴、能量轴、时间轴与类别轴，再检查方向、符号、能量参照和模型假设。

没有动力学证据时，稳态光谱变化不能自动画成转移速率增加；电子粒子运动、空穴粒子运动与约定电流也不能靠同一种箭头含混表示。输出机制语义表、证据层级、矢量对象与来源。现有能级和漂移示例强调这些区别，不假冒真实材料能级。

### 7.4 sci-figure-device：器件结构、装配与空间视角

输入材料身份、层序、接触、尺度和功能。先判断二维剖面是否足够，再决定装配、爆炸、剖切、局部放大或三维视角。对薄层可有明确标注的厚度夸张；未知尺寸不画可信标尺。透视应帮助理解接触和遮挡，而不能改变接触关系。

输出几何参数、独立材料/部件、相机与材质、可编辑标注和原生源文件。基础示例实际保留装配、爆炸与剖切三套视图的Blender源；补充示例使用互指接触与局部剖切展示更复杂的空间任务。渲染层与文字标注层分开，便于修改材料、视角或文字。

### 7.5 sci-figure-process：生长调控、实验与制造过程

输入控制变量、操作、时间/阶段、可观察状态和测量依据。区分操作图、反应机理图与观测序列，保留对象身份和各阶段条件。生长轨迹需要处理晶核、颗粒/晶粒、表面、溶液与物种的不同尺度；必要时加入分支或同条件对照，避免统一三格箭头。

输出状态/操作登记、跨帧对象ID、比例和假设、过程图与数据/影像关联。示意粒子数量和浓度条不能被读成真实粒子计数或质量守恒证据。扫描时间、样本替换和不同观察位置均须明确。

### 7.6 sci-figure-image：影像、谱像与真实体场

输入原始图像、采样坐标、通道、单位、ROI和处理来源。保存原始层，登记裁切、强度变换、配准、分割、滤波和重建，分别表达原始观测、算法输出和定量结论。比较面板是否共享色域必须由比较目的决定。

输出含标尺与方向的图像面板、可追踪ROI、色标/传递函数、处理记录与定量链接。不得局部“美化”真实科研像素以制造结构。体数据应有切片或其他证据约束，概念三维示意不能冒充重建结果。

### 7.7 sci-figure-color：颜色语义与有限诊断

输入对象身份、数值类型、背景、目标尺寸与输出载体。先定分类、顺序、发散或周期，再选颜色与冗余编码。提供12组原创配色起点、连续色图候选及可运行诊断脚本；允许根据任务变化扩展或替换，不强制五色、两色或某一固定主题。

输出作用域明确的颜色表、色标中心与范围、缺失值规则、灰度/CVD有限预览和针对实际成图的判断。诊断程序计算色块特征，不能代替文字、细线、拥挤与图例检查；它不颁发通用可达性证书。

### 7.8 sci-figure-compose：多面板结构与合版

输入独立面板、科学论证顺序、比较关系、物理尺寸和文字密度。依据读者任务选择矩阵、路径、总览与局部、多尺度、原始/推断/量化等布局。只有复杂、模糊或重排任务才要求比较至少两条布局路线；简单图可直接完成。

输出面板面积分配、共享轴/色标规则、读序、统一身份表、可编辑合版与目标尺寸预览。整齐不代表条件一致：必须逐面板核对时间、样本、工况和单位。跨面板关联通过直接标签、位置、ID和有限颜色建立，不以所有面板同样大为原则。

### 7.9 sci-figure-review：科学、视觉与源文件审查

检查坐标/单位、箭头与证据层级、样本与比较条件、颜色与影像处理、文字可读性、图层和外链。机械SVG扫描只报告它能检查的部分，如物理尺寸、文字、嵌入图像元数据、资源引用与部分变换；不声称能发现所有真实字形遮挡或解释错误。

输出分层审查记录、明确阻断项、已修复问题、剩余不确定性，以及实际打开导出图的记录。不得只因脚本没有报错就宣称可发表。期刊尺寸与格式要求按具体刊物、稿件阶段和当前官方说明核实。[E08、E09]

## 8. 使用流程与任务示例

流程为：明确读者问题与证据→选择语法和必要模块→制作最小但足够的结构→增加有信息的细节→统一语义和尺寸→实际导出审图→保留源文件。复杂任务可在早期比较不同构图；简单任务不加无用审批或草图环节。

示例一：调用sci-figure-director，使用三批器件的前后配对数据，展示性能与带宽之间的取舍；结构仅需层序，厚度未知。要求保留批次、原始点和每个器件身份，给SVG与生成脚本。这会路由到data、device、compose、color与review；如涉及机理主张，再用mechanism审查证据。

示例二：调用sci-figure-process，比较两种添加剂条件下的晶体生长。现有原位帧、温度程序和相应谱图，需要区分同一晶粒追踪与独立位置观测。要求先建立阶段、对象ID和证据表，再决定用矩阵、时间序列或带分支的状态图，最后保留原始影像与标注层。

示例三：调用sci-figure-device，展示多层植入器件的装配及组织接触。已有材料层序、CAD尺寸和功能说明。先比较剖面与爆炸图对当前读者问题的作用；需要三维时提交原生几何、相机、材质和独立矢量标注，避免把层状材料压成不可修改的一张位图。

示例四：调用sci-figure-image，制作原始谱像、组分拟合、ROI谱线和空间量化图。要求登记谱库、滤波、色域、时间顺序和缺失值；不能因为图片看起来相似就宣称使用了同一处理条件。

## 9. 已制作的示例与实际试用

本轮所有原创示例均明确为DEMO，不能当作实验结果。数据模块提供批次配对和多目标权衡两例；机理模块提供空间漂移与能量排列两例。它们有意保持简洁，用来检验语义与可编辑性，不用图形复杂度充当质量证据。

器件模块基础示例实际生成了装配、爆炸和剖切视图，并保留可重新打开的Blender文件、15个网格对象与三套集合。新增互指器件示例补足平面电极图案与埋藏界面的空间表达；其任意尺寸和厚度夸张均明确说明，不能作为特定器件设计或制造尺寸。

独立前向试用从空白开始，以三批各五个器件、处理前后两个状态为题，产生180×104 mm的SVG与30行模拟端点数据。实际加载director及data、device、mechanism、compose、color、review，共七模块，未复用已有DEMO源码或数据。

最终图使用紧凑二维层序与三批同尺度配对散点。输入没有真实光谱、稳定性曲线或动力学速率，图中因此只保留定性提示，把transfer rate标为unmeasured，没有补造“转移加速”的机制箭头。这个决定体现了技能对证据的约束能力。

首版实际打开后发现文字侵入纵轴和局部点过近，随后修复。第二个问题通过调整明确自造的DEMO示例值解决；真实数据不能这样改数，应改表示或布局。最终查看了整图、缩小和灰度预览，并用实际字形包围框辅助检查。

## 10. 验证、修正与仍然有限的结论

独立证据抽查最初覆盖12篇、24张完整选定图以及九个SKILL.md，在这个样本内没有发现阻断或重大图号/图像错配。轻微项包括B05标记语义、D组逐图观察混并、A23实际PDF副本来源缺失，以及D20软件证据的角色与范围。C03跨培养天数条件作为补充限定加入。

修复中找回A23机构PDF，重新取得的副本与原已读文件逐字节一致；D组17篇的34条逐图笔记已分别重写并核对实际图像，未因此升级全文阅读范围。又定向修正D05膜颜色、D20图例范围和C24同页图2/图3语义。这些更正保留在审查与修复记录中，没有抹去原始审查时状态。

| 实际验证 | 结果与范围 |
| --- | --- |
| 官方技能结构验证 | 九个技能均通过 |
| agents元数据 | 九个技能的名称、默认提示与描述检查通过 |
| 本地引用解析 | 26处Markdown相对链接与9处资源路径提及无缺失 |
| SVG检查器契约测试 | 七项通过，包括正常base64空白和真实损坏区分 |
| bundled示例SVG机械扫描 | 八张完成，零findings；四张Matplotlib图保留CSS解析uncertainty |
| 配色数值检查 | 黑/白亮度与对比、sRGB往返、灰色模拟与非法HEX等检查通过；12组已运行诊断 |
| 独立前向试用 | 一条器件—统计混合路线；58个live text、34个命名组、零外链图像 |
| 三维示例 | 实际渲染，并重新打开Blender源检查几何对象 |

检查器在真实Matplotlib导出上发现了一个兼容问题：正常base64换行经XML规范化后成为空格，旧实现误报图像损坏。已允许ASCII空白后仍严格检查其余字符，并增加对应测试。构图模块原先无条件要求两套布局，也已限定为复杂或不确定任务。

这些结果支持本次已执行路线、接口与示例的有限可运行性，不能证明九个模块的全部分支都优于旧技能。前向任务仅执行七模块的器件—统计混合路线，mechanism用于判定证据边界；process与image没有前向执行。独立制作的三维器件示例也不等同于真实体数据、显微、光路或频谱路线的验证，这些分支仍需要在后续真实项目中逐类试用。没有声称通过审查等于可发表，也没有进行随机对照的审美偏好实验。

## 11. 安装状态与交付范围

九个技能的正文、参考资料、脚本、元数据和示例已经编写完成。当前工作目录中的内容可用于审查，配套研究手册与图谱给出完整的设计判断和使用路径。

安装步骤曾被自动审批拒绝：环境策略禁止通过提权命令写入/root/.codex/skills/remote-skills。skill-creator要求通过技能目录中的git流程持久化；本轮没有绕过这个拒绝，也没有把未执行的安装、git提交或远程同步写成成功。安装及远程同步仍是待完成项，需在允许写入该技能目录的授权环境中执行。

这与内容质量验证是不同状态：正文和可运行示例已经完成；“九个技能已在用户环境启用”尚不成立。没有用交付一份压缩包替代安装成功的声明。后续启用时应沿用这里已验证的名称和目录结构，并保留对应文献索引与资源路径。

## 12. 外部方法与规范来源

E01. Yuan1z0825/nature-skills公开nature-figure，访问2026-10-17。https://github.com/Yuan1z0825/nature-skills/blob/main/skills/nature-figure/SKILL.md

E02. 同仓库vector-schematic-style-rules.md，访问2026-10-17。https://github.com/Yuan1z0825/nature-skills/blob/main/skills/nature-figure/references/vector-schematic-style-rules.md

E03. Crameri, F., Shephard, G. E. & Heron, P. J. The misuse of colour in science communication. Nature Communications 11, 5444 (2020). https://doi.org/10.1038/s41467-020-19160-7

E04. Matplotlib官方Choosing Colormaps说明；本轮色卡生成实际使用Matplotlib 3.10.8。https://matplotlib.org/stable/users/explain/colors/colormaps.html

E05. Machado, G. M., Oliveira, M. M. & Fernandes, L. A. F. A Physiologically-based Model for Simulation of Color Vision Deficiency (2009). https://doi.org/10.1109/TVCG.2009.113 。线性RGB实施另核对colorspace官方说明：https://colorspace.r-forge.r-project.org/reference/simulate_cvd.html

E06. Blender官方4.5分发目录；本轮运行便携版4.5.0。https://download.blender.org/release/Blender4.5/

E07. ParaView官方项目与功能入口。https://www.paraview.org/

E08. Nature Research Figure Guide，Preparing figures: our specifications，访问2026-10-17。https://research-figure-guide.nature.com/figures/preparing-figures-our-specifications/

E09. Nature Research Figure Guide，Building and exporting，访问2026-10-17。https://research-figure-guide.nature.com/figures/building-and-exporting-figure-panels/

期刊规范按稿件阶段、主图/扩展数据和具体刊物区别适用。例如官方页面对于文字、宽度、位图分辨率与导出格式的说明并非处处使用同一数值；本技能没有将某个旧版尺寸或统一DPI提升为全部期刊的固定标准。

## 附录：89篇论文索引

下列编号对应paper-atlas.html内逐篇记录。每条均有正式DOI；阅读范围、实际图号和来源版本以图谱中的具体字段为准。完整逐图分析在图谱中，不以本索引替代已读证据。

A01 · Household alternating current electricity plug-and-play quantum-dot light-emitting diodes

Nature Communications (2024). https://doi.org/10.1038/s41467-024-47891-4

A02 · Stable and efficient pure blue quantum-dot LEDs enabled by inserting an anti-oxidation layer

Nature Communications (2024). https://doi.org/10.1038/s41467-024-44894-z

A03 · Ultrabright and stable top-emitting quantum-dot light-emitting diodes with negligible angular color shift

Nature Communications (2024). https://doi.org/10.1038/s41467-024-49574-6

A04 · Tracing the electron transport behavior in quantum-dot light-emitting diodes via single photon counting technique

Nature Communications (2024). https://doi.org/10.1038/s41467-024-52521-0

A05 · Ultrasensitive dim-light neuromorphic vision sensing via momentum-conserved reconfigurable van der Waals heterostructure

Nature Communications (2024). https://doi.org/10.1038/s41467-024-53268-4

A06 · Reconfigurable optoelectronic transistors for multimodal recognition

Nature Communications (2024). https://doi.org/10.1038/s41467-024-47580-2

A07 · Optoelectronic synapses with chemical-electric behaviors in gallium nitride semiconductors for biorealistic neuromorphic functionality

Nature Communications (2024). https://doi.org/10.1038/s41467-024-51194-z

A08 · Tunable anti-ambipolar vertical bilayer organic electrochemical transistor enable neuromorphic retinal pathway

Nature Communications (2024). https://doi.org/10.1038/s41467-024-50496-6

A09 · Programmable nonlinear optical neuromorphic computing with bare 2D material MoS2

Nature Communications (2024). https://doi.org/10.1038/s41467-024-54776-z

A10 · Birdlike broadband neuromorphic visual sensor arrays for fusion imaging

Nature Communications (2024). https://doi.org/10.1038/s41467-024-52563-4

A11 · Low-power scalable multilayer optoelectronic neural networks enabled with incoherent light

Nature Communications (2024). https://doi.org/10.1038/s41467-024-55139-4

A12 · Visualized in-sensor computing

Nature Communications (2024). https://doi.org/10.1038/s41467-024-47630-9

A13 · Multi-dimensional optical information acquisition based on a misaligned unipolar barrier photodetector

Nature Communications (2024). https://doi.org/10.1038/s41467-024-51378-7

A14 · Acceleration of radiative recombination for efficient perovskite LEDs

Nature (2024). https://doi.org/10.1038/s41586-024-07460-7

A15 · Anisotropic nanocrystal superlattices overcoming intrinsic light outcoupling efficiency limit in perovskite quantum dot light-emitting diodes

Nature Communications (2022). https://doi.org/10.1038/s41467-022-29812-5

A16 · Optoelectronic system and device integration for quantum-dot light-emitting diode white lighting with computational design framework

Nature Communications (2022). https://doi.org/10.1038/s41467-022-31853-9

A17 · Stable and efficient CsPbI 3  quantum-dot light-emitting diodes with strong quantum confinement

Nature Communications (2024). https://doi.org/10.1038/s41467-024-50022-8

A18 · Surface-binding molecular multipods strengthen the halide perovskite lattice and boost luminescence

Nature Communications (2024). https://doi.org/10.1038/s41467-024-49751-7

A19 · Transparent organic upconversion devices displaying high-resolution, single-pixel, low-power infrared images perceived by human vision

Science Advances (2023). https://doi.org/10.1126/sciadv.add7526

A20 · Self-assembled monolayer–based blue perovskite LEDs

Science Advances (2023). https://doi.org/10.1126/sciadv.adh2140

A21 · Lattice strain modulation toward efficient blue perovskite light-emitting diodes

Science Advances (2022). https://doi.org/10.1126/sciadv.abq0138

A22 · Ultralow voltage–driven efficient and stable perovskite light-emitting diodes

Science Advances (2024). https://doi.org/10.1126/sciadv.adp8473

A23 · An organic electrochemical transistor for multi-modal sensing, memory and processing

Nature Electronics (2023). https://doi.org/10.1038/s41928-023-00950-y

A24 · High-performance inorganic metal halide perovskite transistors

Nature Electronics (2022). https://doi.org/10.1038/s41928-022-00712-2

B01 · In situ dynamic observations of perovskite crystallisation and microstructure evolution intermediated from [PbI6]4− cage nanoparticles

Nature Communications (2017). https://doi.org/10.1038/ncomms15688

B02 · Crystal growth in confinement

Nature Communications (2022). https://doi.org/10.1038/s41467-022-34330-5

B03 · Oriented nucleation in formamidinium perovskite for photovoltaics

Nature (2023). https://doi.org/10.1038/s41586-023-06208-z

B04 · Direct observation of liquid nucleus growth in homogeneous melting of colloidal crystals

Nature Communications (2015). https://doi.org/10.1038/ncomms7942

B05 · Observing classical nucleation theory at work by monitoring phase transitions with molecular precision

Nature Communications (2014). https://doi.org/10.1038/ncomms6598

B06 · In situ observation of coalescence of nuclei in colloidal crystal-crystal transitions

Nature Communications (2023). https://doi.org/10.1038/s41467-023-40627-w

B07 · Mechanism for rapid growth of organic–inorganic halide perovskite crystals

Nature Communications (2016). https://doi.org/10.1038/ncomms13303

B08 · Light-driven nucleation, growth, and patterning of biorelevant crystals using resonant near-infrared laser heating

Nature Communications (2023). https://doi.org/10.1038/s41467-023-42126-4

B09 · Moisture-triggered fast crystallization enables efficient and stable perovskite solar cells

Nature Communications (2022). https://doi.org/10.1038/s41467-022-32482-y

B10 · High-quality bulk hybrid perovskite single crystals within minutes by inverse temperature crystallization

Nature Communications (2015). https://doi.org/10.1038/ncomms8586

B11 · Shaping Perovskites: In Situ Crystallization Mechanism of Rapid Thermally Annealed, Prepatterned Perovskite Films

ACS Applied Materials & Interfaces (2021). https://doi.org/10.1021/acsami.0c20958

B12 · Hierarchical structure formation by crystal growth-front instabilities during ice templating

Proceedings of the National Academy of Sciences (2023). https://doi.org/10.1073/pnas.2210242120

B13 · In situ studies of a platform for metastable inorganic crystal growth and materials discovery

Proceedings of the National Academy of Sciences (2014). https://doi.org/10.1073/pnas.1406211111

B14 · In situ imaging of two-dimensional surface growth reveals the prevalence and role of defects in zeolite crystallization

Proceedings of the National Academy of Sciences (2020). https://doi.org/10.1073/pnas.2011806117

B15 · Programmable and coherent crystallization of semiconductors

Science Advances (2017). https://doi.org/10.1126/sciadv.1602462

B16 · A Nanoparticle-Based Model System for the Study of Heterogeneous Nucleation Phenomena

Langmuir (2023). https://doi.org/10.1021/acs.langmuir.2c03034

B17 · Solution-based Cu+ transient species mediate the reconstruction of copper electrocatalysts for CO2 reduction

Nature Catalysis (2024). https://doi.org/10.1038/s41929-023-01070-8

B18 · Exploring the influence of cell configurations on Cu catalyst reconstruction during CO2 electroreduction

Nature Communications (2024). https://doi.org/10.1038/s41467-024-52692-w

B19 · Alkali cation-induced cathodic corrosion in Cu electrocatalysts

Nature Communications (2024). https://doi.org/10.1038/s41467-024-49492-7

B20 · Operando spectral imaging of the lithium ion battery’s solid-electrolyte interphase

Science Advances (2023). https://doi.org/10.1126/sciadv.adg5135

B21 · Operando visualisation of battery chemistry in a sodium-ion battery by 23Na magnetic resonance imaging

Nature Communications (2020). https://doi.org/10.1038/s41467-020-15938-x

B22 · 4D imaging of lithium-batteries using correlative neutron and X-ray tomography with a virtual unrolling technique

Nature Communications (2020). https://doi.org/10.1038/s41467-019-13943-3

B23 · On the Cobalt Carbide Formation in a Co/TiO2 Fischer–Tropsch Synthesis Catalyst as Studied by High-Pressure, Long-Term Operando X-ray Absorption and Diffraction

ACS Catalysis (2021). https://doi.org/10.1021/acscatal.0c04695

B24 · Copper catalysis at operando conditions—bridging the gap between single nanoparticle probing and catalyst-bed-averaging

Nature Communications (2020). https://doi.org/10.1038/s41467-020-18623-1

C01 · spinDrop: a droplet microfluidic platform to maximise single-cell sequencing information content

Nature Communications (2023). https://doi.org/10.1038/s41467-023-40322-w

C02 · Rapid droplet-based mixing for single-molecule spectroscopy

Nature Methods (2023). https://doi.org/10.1038/s41592-023-01995-9

C03 · Geometric engineering of organoid culture for enhanced organogenesis in a dish

Nature Methods (2022). https://doi.org/10.1038/s41592-022-01643-8

C04 · High throughput intracellular delivery by viscoelastic mechanoporation

Nature Communications (2024). https://doi.org/10.1038/s41467-023-44447-w

C05 · A microfluidic platform integrating functional vascularized organoids-on-chip

Nature Communications (2024). https://doi.org/10.1038/s41467-024-45710-4

C06 · A multi-organ chip with matured tissue niches linked by vascular flow

Nature Biomedical Engineering (2022). https://doi.org/10.1038/s41551-022-00882-6

C07 · A microphysiological model of human trophoblast invasion during implantation

Nature Communications (2022). https://doi.org/10.1038/s41467-022-28663-4

C08 · Organ-on-e-chip: Three-dimensional self-rolled biosensor array for electrical interrogations of human electrogenic spheroids

Science Advances (2019). https://doi.org/10.1126/sciadv.aax0729

C09 · Fully integrated wearable sensor arrays for multiplexed in situ perspiration analysis

Nature (2016). https://doi.org/10.1038/nature16521

C10 · A wearable electrochemical biosensor for the monitoring of metabolites and nutrients

Nature Biomedical Engineering (2022). https://doi.org/10.1038/s41551-022-00916-z

C11 · A wireless patch for the monitoring of C-reactive protein in sweat

Nature Biomedical Engineering (2023). https://doi.org/10.1038/s41551-023-01059-5

C12 · A stealthy neural recorder for the study of behaviour in primates

Nature Biomedical Engineering (2025). https://doi.org/10.1038/s41551-024-01280-w

C13 · Syringe-injectable electronics

Nature Nanotechnology (2015). https://doi.org/10.1038/nnano.2015.115

C14 · Morphing electronics enable neuromodulation in growing tissue

Nature Biotechnology (2020). https://doi.org/10.1038/s41587-020-0495-2

C15 · Ultrafast small-scale soft electromagnetic robots

Nature Communications (2022). https://doi.org/10.1038/s41467-022-32123-4

C16 · Spinning-enabled wireless amphibious origami millirobot

Nature Communications (2022). https://doi.org/10.1038/s41467-022-30802-w

C17 · Touchless interactive teaching of soft robots through flexible bimodal sensory interfaces

Nature Communications (2022). https://doi.org/10.1038/s41467-022-32702-5

C18 · Modular multi-degree-of-freedom soft origami robots with reprogrammable electrothermal actuation

Proceedings of the National Academy of Sciences (2024). https://doi.org/10.1073/pnas.2322625121

C19 · An inhaled bioadhesive hydrogel to shield non-human primates from SARS-CoV-2 infection

Nature Materials (2023). https://doi.org/10.1038/s41563-023-01475-7

C20 · Photocurable bioresorbable adhesives as functional interfaces between flexible bioelectronic devices and soft biological tissues

Nature Materials (2021). https://doi.org/10.1038/s41563-021-01051-x

C21 · Hydraulic hydrogel actuators and robots optically and sonically camouflaged in water

Nature Communications (2017). https://doi.org/10.1038/ncomms14230

C22 · Skin-inspired hydrogel-elastomer hybrids with robust interfaces and functional microstructures

Nature Communications (2016). https://doi.org/10.1038/ncomms12028

C23 · Tough adhesives for diverse wet surfaces

Science (2017). https://doi.org/10.1126/science.aah6362

C24 · An integrated design and fabrication strategy for entirely soft, autonomous robots

Nature (2016). https://doi.org/10.1038/nature19100

D01 · Accurate structure prediction of biomolecular interactions with AlphaFold 3.

Nature (2024). https://doi.org/10.1038/s41586-024-07487-w

D02 · Scaling deep learning for materials discovery.

Nature (2023). https://doi.org/10.1038/s41586-023-06735-9

D03 · Learning nonlinear operators in latent spaces for real-time predictions of complex dynamics in physical systems.

Nature Communications (2024). https://doi.org/10.1038/s41467-024-49411-w

D05 · High-confidence 3D template matching for cryo-electron tomography.

Nature Communications (2024). https://doi.org/10.1038/s41467-024-47839-8

D06 · Photoacoustic Tomography with Temporal Encoding Reconstruction (PATTERN) for cross-modal individual analysis of the whole brain.

Nature Communications (2024). https://doi.org/10.1038/s41467-024-48393-z

D07 · Imaging 3D chemistry at 1 nm resolution with fused multi-modal electron tomography.

Nature Communications (2024). https://doi.org/10.1038/s41467-024-47558-0

D08 · X-ray linear dichroic tomography of crystallographic and topological defects.

Nature (2024). https://doi.org/10.1038/s41586-024-08233-y

D09 · Solving olympiad geometry without human demonstrations.

Nature (2024). https://doi.org/10.1038/s41586-023-06747-5

D10 · The quantum transition of the two-dimensional Ising spin glass.

Nature (2024). https://doi.org/10.1038/s41586-024-07647-y

D11 · Electron hydrodynamics in anisotropic materials.

Nature Communications (2020). https://doi.org/10.1038/s41467-020-18553-y

D12 · Snapshot multidimensional photography through active optical mapping.

Nature Communications (2020). https://doi.org/10.1038/s41467-020-19418-0

D14 · Dynamic localization of electronic excitation in photosynthetic complexes revealed with chiral two-dimensional spectroscopy.

Nature Communications (2014). https://doi.org/10.1038/ncomms4286

D16 · Data-driven discovery of coordinates and governing equations.

Proceedings of the National Academy of Sciences (2019). https://doi.org/10.1073/pnas.1906995116

D17 · Data-driven discovery of partial differential equations.

Science Advances (2017). https://doi.org/10.1126/sciadv.1602614

D18 · Neural general circulation models for weather and climate.

Nature (2024). https://doi.org/10.1038/s41586-024-07744-y

D19 · Visualizing chaperonin function in situ by cryo-electron tomography.

Nature (2024). https://doi.org/10.1038/s41586-024-07843-w

D20 · Neuronal wiring diagram of an adult brain.

Nature (2024). https://doi.org/10.1038/s41586-024-07558-y
