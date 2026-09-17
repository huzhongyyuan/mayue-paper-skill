## 05｜每一章节怎么写：可直接用于你自己论文的规则

以下英文句式均为**本手册原创的可复用模板**，方括号是待填内容，不是论文原句，也不是已有实验结论。章节长度按论证需要与 venue 调整；这些作品存在不同篇幅与模板，没有统一的“每节必须几段”。

### 5.1 Title：让读者知道“控制什么”和“凭什么做到”

常见结构有三种：

| 类型 | 原作例子 | 适合什么贡献 |
|---|---|---|
| 名称 + 任务 + 特殊条件 | Pose：Pose-Guided … using Pose-Free Videos | 数据／监督方式有反差 |
| 名称 + 能力边界 | Canvas：Higher-Resolution … with Extensive Content Generation | 原任务的规模或范围被扩展 |
| 名称 + 机制／瓶颈 | Motion：… Efficient Spatial-Temporal Decoupled Finetuning；FastVMT：Eliminating Redundancy … | 关键机制或成本来源清楚 |

“Follow-Your-X”建立了系列辨识度，但为你的论文命名时应根据自己的项目和贡献决定。真正可迁移的是副标题的信息密度：任务、关键操作、主要条件。标题中的“real-time”“training-free”“4D”“universal”都需要明确定义并有对应实验。

**落笔前写三个版本：** 任务导向、机制导向、约束导向。用一个不熟悉项目的读者能否猜到输入、输出与贡献来选择。不要让模块缩写占满标题却不告诉读者在解决什么问题。

### 5.2 Abstract：一段内完成一个小型论证

高频功能顺序是：

1. **任务与承诺：** 定义本文处理的输入、操作和输出。
2. **瓶颈：** 指明当前方案在目标设置下为什么不够。
3. **核心观察／转向：** 提出解决方式的依据。
4. **机制 A：** 一个动作加一个目的。
5. **机制 B：** 处理另一个瓶颈或 A 留下的问题。
6. **训练／评价资源：** 只有数据集或 benchmark 真正构成贡献时才写。
7. **证据与边界：** 用关键实验说明支持哪些能力；数值需条件齐全。

可写成：

> We study [task], where [input/control] is used to [desired change] while preserving [invariant]. Existing approaches struggle with [specific failure] under [setting]. Our analysis indicates that [supported observation]. Based on this observation, we introduce [method], which [core operation]. To address [remaining issue], we further [second operation]. Evaluations on [verified protocol] show [supported result] under [conditions].

**从原作学句间连接。** Canvas 的“两类设计”每类都接一句“产生什么作用”；Emoji 不止列 landmark／loss 名称，还解释身份泄漏和小表情；Motion 用 Stage 1／2／3 让摘要与 Method 对齐。FastVMT 的两种 redundancy 是问题命名，也成为方法的组织词。

**自检。** 去掉方法名和形容词后，还能否看出真正的操作？“excellent”“powerful”“novel”“extensive”不能代替因果或实验。若尚无结果，摘要可以保留方法部分，将结果句明确标成待完成，不补写“achieves SOTA”。

### 5.3 Introduction：把读者从任务带到不可回避的设计

你通常需要以下论证功能，但不必每项独占一段：

| 段落功能 | 段首回答 | 段内必须补足 | 通向下一段的连接 |
|---|---|---|---|
| 任务与价值 | 用户要改变什么 | 输入、输出、不变量；少量具体应用 | 现有模型为何接近但尚未满足 |
| 已有路线 | 最近的方法做到了什么 | 按关键假设分组，准确引用 | 哪个假设在目标设置下失效 |
| 具体失败 | 直接方案如何失败 | 输入、基线、设置、可见错误 | 原因可能是什么 |
| 诊断观察 | 哪种因素导致失败 | 控制变量或表示分析，区分观察与推断 | 哪类干预可能有效 |
| 方法概览 | 我们据此怎么改 | 每个操作对应前述问题 | 还剩什么新问题 |
| 结果与贡献 | 证据支持了什么 | 主要协议、结果范围和贡献边界 | 进入正式方法 |

**过渡句的功能比词更重要。** “However”应引出同一话题中的具体不足；“Based on this observation”前面需要真的有观察；“To address this issue”中的 issue 必须可定位；“Specifically”后面应给机制而非再次说效果。

原创骨架：

> Directly applying [baseline] to [setting] produces [failure], as shown in Fig. [verified figure]. We investigate whether this behavior is caused by [factor A] or [factor B] by varying each factor while fixing the other. The results suggest [bounded conclusion]. This motivates [operation A]. However, [residual failure] remains because [mechanism]. We therefore introduce [operation B].

**贡献列表怎么写。** 每条给一个可评价的贡献单位，例如新任务／诊断、新方法／表示、新数据／评价。若第二条只重复第一条的方法名称，合并。基准不能仅因“我们也测试了数据”就算新 benchmark。把“首次”写入贡献前，需要完成相应文献检索。

### 5.4 Related Work：为方法定位，避免变成参考文献目录

原作的分组方式通常跟论证有关：

- Pose：T2V／Pose-to-Video／Controllable Diffusion，对应先验、目标任务与条件接口。
- Emoji：GAN-based／Diffusion-based portrait animation，对应不同生成范式及剩余细节问题。
- Canvas：Diffusion／Video Outpainting，迅速进入目标任务的分辨率与比例。
- Creation：Camera Control／Video Inpainting／Dynamic Novel View，对应被统一的三个邻域。
- Faster：增加 Acceleration，反映新版本新增的研究维度。
- LiveLight：Relighting／Real-time Generation／Controllable Generation，说明交互条件需要多个技术邻域。

**一组相关工作内部可写四步：** 共同目标 → 按机制归纳代表路线 → 明确可比的限制 → 本文处理的不同条件。无需为每篇文献写一句。准确区分最近邻基线和仅提供背景的工作。

原创模板：

> Methods in this family use [shared mechanism] to achieve [capability]. Recent extensions improve [dimension] through [two representative approaches]. These designs assume [condition], whereas our setting requires [different condition]. We therefore investigate [specific design question].

这里的限制要有文献或自己的比较支持；不要把所有前人概括成“无法处理复杂场景”。引用作者自己的作品可以补研究脉络，但不能替代最接近的外部工作。

### 5.5 Preliminaries / Problem Formulation：把全文的“合同”写清楚

**Problem Formulation 负责边界。** 写输入张量／控制信号、输出、需要变化的属性、不变量、训练／推理可见信息。Click 先明确图像、区域与短动作条件；LiveLight 还需要明确控制条件在时间上何时到达。

**Preliminaries 负责共同语言。** 只保留后文会使用的 diffusion／flow、attention、LoRA、RoPE 符号。DiT4Edit 需要解释架构差异，因为编辑机制依赖它；COVE 需要 attention 与反演基础，因为对应 token 会改变计算。

原创模板：

> Given [input] and [control], our goal is to generate [output] such that [changed property] follows the control while [invariant] is preserved. During training, [supervision] is available; at inference, the method only requires [inference inputs].

建议随稿维护符号表：张量是什么、维度、属于源／目标、当前视频帧索引、扩散时间步和优化步索引。FastVMT 类方法尤其不能把视频帧、去噪步、内循环优化步共用一个含混的 t。

### 5.6 Method 总览：先给一条能走通的路径

总览段需要四件事：输入如何进入、关键表示如何产生、核心模型做什么、输出如何得到。图中的每条实线都应在文字里有语义，训练专用分支与推理流程区分清楚。

**按什么顺序写？** 依据依赖关系决定：

- Pose／Motion：阶段顺序；
- COVE：获取对应 → 使用对应；
- Creation：构造条件 → 调适 → 推理；
- Group Editing：获得数据 → 对齐与编辑；
- LiveLight：数据 → 光照表示 → 少步质量 → 流式计算 → objectives。

不要为了统一“Ma Yue 风格”，把所有工作都写成三阶段。模块越多，越需要用问题来分组，而不是让读者记住更多缩写。

### 5.7 每个 Method 子节：七件事构成一个完整模块段落

一个模块可以跨若干自然段，但以下信息不能缺：

1. **目的：** 前文哪个错误由这个模块处理。
2. **现象／原因：** 直接做法为何不足，引用动机图或分析。
3. **输入：** 模块接收什么，来源与形状是什么。
4. **操作：** 如何编码、选择、组合或更新；给必要公式。
5. **输出与接入点：** 结果流向哪个层／阶段。
6. **训练与推理：** 更新哪些参数，损失如何作用，推理是否仍使用。
7. **验证预期：** 移除／替换该模块应该出现哪类变化，在实验哪处验证。

**以 Canvas RRE 为例。**

- 目的：单窗不知道自己相对源窗口的位置。
- 输入：两个窗口的偏移与尺寸。
- 操作：编码、映射到 embedding。
- 输出：与 LE 输出的布局 tokens 结合，再进入条件通路。
- 验证：去掉 RRE 后，局部内容可能合理，但与全局场景位置关系不协调。
- 文字重点：为什么“同样的布局特征”在不同 target window 必须有不同含义。

原创模块段落：

> Although [existing component] provides [useful information], it does not specify [missing relation]. We encode [variables] into [representation] using [operation], and inject the resulting features into [location]. This allows [receiving component] to distinguish [cases previously conflated]. The module is optimized with [objective/update scope] during [stage] and [inference behavior]. We evaluate its role by [controlled ablation].

**公式怎么接。** 先用话说明要算什么，再列公式，紧跟解释每个变量和直觉。若改动是拼接／位置映射，公式应揭示数据流；若是新损失，说明零值／极端值意味着什么。不要用公式包装没有实现的机制。

### 5.8 Training / Inference：将参数状态作为论证的一部分

至少交代：

| 项目 | 需要写到什么程度 |
|---|---|
| 基础模型 | 名称、版本与实际使用模块 |
| 数据与采样 | 从何处来，是否配对，抽帧／裁剪／mask 如何构造 |
| 参数更新 | 各阶段 trainable／frozen；LoRA 插入位置与 rank |
| 损失 | 每项的目的、系数、计算区域、梯度流向 |
| 优化设置 | 步数、batch、学习率、硬件与时间范围 |
| 推理输入 | 训练时可见的真值是否仍被使用 |
| 推理成本 | inversion、特征提取、优化、去噪、解码是否计入 |

从 Pose／Motion 学分阶段的参数职责；从 Emoji 学局部 loss 区域；从 Creation 学条件构造；从 LiveLight 学训练专用几何反馈与实时推理的区别。火焰／雪花标志只是视觉摘要，不能替代正文的明确说明。

### 5.9 Experiments：按主张组织问题，而不是只按指标列结果

可先在内部将每个实验写成一个问题：

- 是否完成了论文定义的控制任务？
- 是否保持应保留的属性？
- 每个模块是否解决它声称处理的问题？
- 提速来自何处，牺牲了什么？
- 在什么条件下失效？

随后根据 venue 和材料组织为 Setup、Comparison、Ablation、Application、Limitations。原作有先定性后定量、也有先应用后比较的安排；采用哪个顺序，取决于读者先需要理解任务能力还是数值证据。

**Setup。** 数据切分、预处理、统一分辨率、生成长度、随机性、基线适配、硬件与计时范围。新 benchmark 要解释构成与采样，而不只是起一个名字。

**Quantitative。** 一段只回答一个主要问题。先报比较条件，再给关键结果，解释支持哪条主张，最后交代其他维度的权衡。避免把所有指标“升降了多少”机械复述一遍。

**Qualitative。** 固定输入、动作、时间采样与裁剪尺度。正文指出哪一行哪一区域表现出什么差异，并连接指标难覆盖的属性。视频论文应额外检查真实播放；本手册只做了静态图阅读。

**Ablation。** 对照方案尽量只改变待检验因素。Canvas 可以分开移除 LE／RRE；Click 要分清数据与网络改动；Motion 要区分 head 分组、稀疏采样、RoPE；FastVMT 要将时间和质量放在同一比较里。额外参数、训练步数或数据不能悄悄改变。

原创实验段落：

> We test whether [component] improves [claimed property] by comparing [controlled variants] under the same [budget/data/settings]. Removing [component] leads to [observed change], especially in [condition]. This supports [bounded interpretation], while [remaining uncertainty] is not resolved by this experiment.

**User Study / Applications。** 有用户评价时，报告参与人数、任务、顺序随机化、盲测与聚合方法。应用展示证明操作可实现，但不能自动证明易用性或用户偏好；LiveLight 的 GUI 图要配真实响应测量才足以支持交互质量。

### 5.10 Discussion / Limitations：将失败连回设计假设

可用三句结构：方法依赖什么 → 哪种输入破坏该假设 → 会出现什么后果，并给出已观察证据或明确的待检验风险。

Canvas 明确承认窗口增加推理时间；DiT4Edit 指出分词与颜色问题；Faster 另设 Discussion；LiveLight 在 Conclusion 前单列 Limitation。这些组织方式都成立。

原创模板：

> Our design relies on [assumption]. When [failure condition], [component] may produce [specific error], which affects [output property]. This limitation is observed in [verified case] / remains to be evaluated under [untested setting].

不要把可能的风险冒充论文已展示的失败，也不要只写泛泛的“requires more data”。更重要的是在最终稿中保留与核心主张相关的真实限制。

### 5.11 Conclusion：用最短路径回收贡献

常见顺序：完成了什么任务 → 核心机制为何有效 → 实验支持什么范围 → 必要边界。Canvas 用很短的段落总结窗口和布局；Emoji 总结表示、损失、数据、长期生成和 benchmark；Motion 重提两类问题。

你的结论可控制在真正需要的信息量，不必重新介绍领域背景。不要在结论里突然加入正文从未证明的新能力或新数值。

原创模板：

> We presented [method] for [task]. By [mechanism A] and [mechanism B], the method addresses [specific bottlenecks]. Results under [evaluated setting] support [main conclusion]. Further work is needed to [limitation-linked next step].

### 5.12 Appendix / Supplement：让审稿人能够回查与复现

附录适合放：完整算法、参数表、数据过滤规则、额外基线配置、更多失败例、敏感性、长序列案例、视频协议。每一块在正文有明确指引，并保持符号／版本一致。

正文仍需保留：核心观察、主要机制、关键设置概述、决定主张是否成立的对照。把所有失败和复现信息藏到未提供的 supplementary 会削弱可信度。

COVE 的附录把 window、merging、inversion 等分析继续展开；Motion 对 head 分类补算法；Creation 继续给多视角与局限；期刊篇幅的 Faster 让 Discussion 与应用直接进入主文。应按任务需要安排，不能把某一个模板的 appendix 长度当成个人风格定律。

## 06｜三篇代表作的逐段精读

### 6.1 Canvas：Introduction 的六步推导

以下按源码有效段落归纳，忽略浮动图的插入位置。依据 P06 的 introduction、abstract、method、experiment 与 conclusion 源码。

| 段落 | 它实际做的事 | 句间如何推进 | 你写自己的论文时替换什么 |
|---|---|---|---|
| 1 | 定义 video outpainting，给调整长宽比的使用例 | 定义 → 具体用途 | 输入／输出与真实操作 |
| 2 | 承认扩散与已有 outpainting 成果，列分辨率和扩展比限制 | 能力 → 有量纲的范围 → 新问题 | 最近邻基线的已验证边界 |
| 3 | 将已有方法放进更大扩画设置，受显存限制先 resize，再观察低质结果 | 实际约束 → 基线处理 → 两因素假设 → 控制变量实验 | 你的直接方案和诊断图 |
| 4 | 根据诊断提出 spatial windows，并讲训练采样与逐步融合 | 原因 → 最小干预 → 训练／推理落地 | 如何把难题分成可处理子任务 |
| 5 | 承认分窗仍出现布局冲突，指出局部上下文缺全局与位置关系 | 新方法的残留错误 → LE → RRE → 联合作用 | 为什么还需要第二个模块 |
| 6 | 给扩展实例、比较结果，再总结贡献 | 可见能力 → 定量证据 → 贡献清单 | 仅填你的真实结果与范围 |

**关键转折。** 第 5 段不是给模块 B 找一个独立卖点，而是解释模块 A 的局限。这让整篇形成连续的技术问题。你若无法写出这样的衔接，应检查模块是否只是并列堆叠。

**摘要逐句功能。** 开头定义高分辨率大范围扩画；下一句列低质量与显存限制；随后引出方法与“两项设计”；第一项讲分窗及合并，接能力；第二项讲源视频与相对位置，接布局；最后将两者合起来给尺度例子和比较结论。源码对“任意分辨率／不受显存限制”的措辞较强，你应改写为受单窗显存约束的可扩展方案，并保留总耗时和资源限制。

**Method 段落怎么借鉴。** LE 负责“全局是什么”，RRE 负责“当前窗口在哪里”。二者的描述不能重复写成“提供 global context”；相似目标下不同的信息职责需要明确。

**Experiments 段落怎么借鉴。** 将高分辨率／高比例设置和低分辨率设置分开报告，避免只挑一个有利条件；布局消融紧接机制；runtime 回答分窗带来的实际代价。Conclusion 的 limitations 与 runtime 表相连，是可核验的边界。

### 6.2 Emoji：从“保身份”推进到“保表情细节”

| 段落 | 论证功能 | 值得学的连接 |
|---|---|---|
| 1 | 定义 portrait animation 与应用 | 驱动序列和参考图的角色一开始就清楚 |
| 2 | 介绍 GAN 的 warping/rendering，再谈 diffusion 先验 | 生成模型变强后，任务特定挑战仍然存在 |
| 3 | 介绍 appearance net、CLIP、temporal attention 等已有适配，再给跨域失真与原因 | 不把这些已有组件全部当成自己的创新 |
| 4 | 针对表示不稳和细节关注不足，解释 landmarks 与 facial loss | 一个问题接一种信息或监督改造 |
| 5 | 扩展到训练数据、长期生成和 EmojiBench，并报告泛化 | 核心机制成立后再讲系统覆盖范围 |

**摘要的取舍。** 有效摘要重点展开 expression-aware landmarks 与 facial fine-grained loss，appearance net 等背景组件没有占据同等篇幅。写摘要时先分清“框架不可缺少”和“本文新证据支持的改动”。

**公开源码提供的一点写作证据。** Emoji 的 abstract 文件还保留了注释掉的候选文本，有的更突出 adapter，有的更突出 landmarks 和 loss。它说明公开材料中存在不同叙述取舍；没有时间戳与完整版本史，不能据此断言哪段先写、谁修改或真实 idea 顺序。

**Related Work 的段尾功能。** 分类后回到细表情、跨风格画像，而不是以“therefore ours is better”结束。**Method** 则将信号设计和局部监督分别展开。**实验** 分自重演与跨重演，避免仅用同一身份重建支持跨身份泛化。**结论** 回收数据与 benchmark，但你的稿件仍应清晰区分训练集和测试集。

### 6.3 Motion：让两个问题贯穿全文

依据 P09 v4 的有效 Introduction 文本：

1. 定义 motion transfer，并与保持低层外观的 video-to-video translation 区分。
2. 交代 diffusion／DiT 背景，将方法分成 training-free 和 tuning-based。
3. 单讲 training-free：如何操作中间表示，能力受何种先验限制。
4. 单讲 tuning-based：为什么要适配参考运动，旧 UNet 分工移到 DiT 有何困难。
5. 给 naive／两阶段方案，再明确列出 **motion inconsistency** 与 **tuning inefficiency**。
6. 按问题给方案：head 分组及分阶段更新对应一致性；稀疏采样与 adaptive RoPE 对应效率。
7. 介绍 MotionBench 的覆盖范围、结果与贡献。

**摘要映射。** 两个问题 → 三个阶段 → benchmark；**方法映射。** head 分类 → 空间 LoRA → 稀疏时间 LoRA／RoPE；**图映射。** 失败与 head 观察 → 流程 → 位置编码；**实验映射。** motion quality、训练时间、各模块消融。写得连贯的原因是这四种映射共用名词。

**你可以直接做的写作练习。** 给自己的项目写两列：左边最多几个真实瓶颈，右边列每个模块。若一个模块对应不了任何瓶颈，先解释其必要性；若一个核心瓶颈没有实验检验，先补证据。不要为了像原作而强行把所有项目拆成两个问题。

### 6.4 全文一致性账本

| 核心主张 | 摘要／Intro 中的问题 | Method 中的操作 | 图应展示 | 实验应隔离 |
|---|---|---|---|---|
| 姿态控制无需完整视频姿态配对 | 配对监督缺口 | 图像控制＋视频时序两阶段 | 数据路线与参数状态 | 各阶段和注入位置 |
| 大画布保持局部细节及布局 | 分辨率／比例与局部上下文 | 窗口＋LE＋RRE | 双因素图、布局冲突、流程 | 两因素、两模块、总成本 |
| 跨身份细表情 | 控制信号泄漏与局部监督不足 | landmarks＋facial loss | 控制差异、mask、结果 | 表示与损失分别替换 |
| DiT motion transfer 的一致性／效率 | head 耦合和帧冗余 | 分类＋分阶段 LoRA＋稀疏／RoPE | head 模式与训练数据路由 | 分组、采样、RoPE、时间 |
| 推理运动迁移提速 | 全局匹配和梯度冗余 | 窗口、对应损失、梯度复用 | 局部性、复用循环 | 质量—时间联合比较 |
| 在线光照控制 | 离线全段条件与高延迟 | MPLI、少步几何训练、rolling window | 动态条件到输出的时间线 | 质量、响应、历史一致性 |

这张表是未来写论文时最先生成、最后再核验一次的工作文件。
