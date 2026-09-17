# 合作论文扩展：2025–2026 的结构与模块索引

下列 33 篇已读摘要、章节结构与主要方法片段，部分补读实验协议；属于**结构／模块级阅读**，不声称全部逐段精读、公式校验或视频评价。Yue Ma 身份在这些作品中已通过 PDF 署名／邮箱／主页等材料交叉识别，但没有据此认定一作或共一。UniPaint 预印本为 2024，会议年份未确认，单独作为背景参照。首发与 venue 分列见 `corpus-2025-2026.md`。

这里的功能是补充可比较的研究路径。读具体技术、引用数值或写 novelty 时，回到所链接的固定版本及最新官方记录。C 编号不表示质量排名。

## C01｜EchoWM：数据条件先于世界模型能力

[2608.23189v1](https://arxiv.org/abs/2608.23189v1)，第 17 作者。第 3 节数据引擎，第 4 节相机意图、渐进视听控制与流式后训练，第 5 节评估，第 6–8 节讨论、限制与结论。已重点补读数据，未深读全部第 4 节。游戏、UE、网络视频通过位姿估计与尺度校准组织到相对 6DoF 条件；ViPE/VGGT 等估计与 UE 真值来源分开，时间戳插值保持同步。数据混合阶段也要防动作描述泄漏。**迁移**：先画数据来源→规范化→训练阶段，再画推理链；camera intent、实际相机轨迹、原生动作日志不是同一对象，无音轨素材也不等于静音监督。

## C02｜PILOT：把意图表示与动作轨迹的职责分开

[2608.06994v1](https://arxiv.org/abs/2608.06994v1)，第二作者，未标共一。3.1 任务、3.2 表示纠缠、3.3 MotionCoT query、3.4 CDE dynamics、3.5 世界模型目标；再实验。利用未来世界辅助信息与动作 flow，V-JEPA 转换目标约束表示。**迁移**：先给“不同表示负责什么”的问题，再给各自监督；方法图将查询、连续动力学和世界预测分支标清。第二作者和“representation decoupling”都不自动意味着共一或统计独立性证明。

## C03｜EgoGenesis：记忆更新必须有可执行的时机

[2607.28243v1](https://arxiv.org/abs/2607.28243v1)，第三作者。第 3 节基础，第 4 节 Online Anchored Projective Memory 与 Action-3D RoPE，第 5 节实验，第 6 节结论。首帧 3D 锚点、近期记忆和定期刷新服务于 chunk autoregression，真实机器人数据扩充承接训练。**迁移**：图中分别标长期锚点、短期缓存、刷新事件，不能把一个 memory 方框代替状态更新算法。

## C04｜MagicPrompt：小参数方法也要报告实际成本范围

[2607.14595v2](https://arxiv.org/abs/2607.14595v2)，第四作者／项目负责人标记，非共一。第 3 节任务、soft prompts、reward，第 4 节实验，第 5 节讨论。固定 backbone，在视觉 self-attention 的 K/V 与文本 cross-attention 加 soft prompt，结合 HPS/MPS reward 与 latent 自监督。**迁移**：图中放大插入点，正文明确可训练参数和目标。prompt 参数少不等于包含生成和奖励计算的整个训练便宜。

## C05｜OPSD-V：把训练分布偏移写成可检查的轨迹

[2607.08766v1](https://arxiv.org/abs/2607.08766v1)，第五作者。第 4 节方法、第 5 节实验、第 6 节分析、第 7 节结论。学生使用与真实推理一致的自身 KV rollout；教师看到相同当前噪声与更干净的历史 cache，dense velocity 目标 stop-gradient，首个真实 chunk 不算该损失，并逐步增加 rollout 长度。**迁移**：对比图画清 teacher/student 的当前输入相同在哪里、历史不同在哪里；“on-policy”应由数据路径支撑。

## C06｜GeoEdit：几何代理和生成补全各自承担一半问题

[2606.30003v1](https://arxiv.org/abs/2606.30003v1)，末位／通信作者。第 3 节基础、重建代理、双分支去噪，第 4 节 benchmark 与实验，后有明确限制。分别 lift scene/object 后对齐和渲染，前景 variance-matched geometry 引导，背景自由补全。**迁移**：画代理生成与 denoising 的接口；继承的 lifting 不包装成原创，几何失败应回溯代理误差。

## C07｜LiveEdit：流式能力要从蒸馏到缓存完整交代

[2606.26740v2](https://arxiv.org/abs/2606.26740v2)，末位／通信作者。3.1 双向→因果 attention 的分布问题，3.2 三阶段蒸馏，3.3 autoregressive mask/cache，4 实验，5 结论。重点读动机及前景刷新／背景缓存，未逐项深读三个蒸馏阶段。**迁移**：总图拆训练转换与在线执行；12.66 FPS 属吞吐，不能替代用户控制到画面改变的延迟。

## C08｜Focused Forcing：从选择规则写到真实加速实现

[2605.18346v1](https://arxiv.org/abs/2605.18346v1)，第七作者。第 3 节基础、head budget、评分、packing，第 4 节比较与消融。每 query/head 以 attention 和历史多样性选择 KV，保留 anchor/recent，再把变长 QKV 打包进 FlashAttention 并 scatter 回去。**迁移**：选择策略和高效执行是两个模块；只少选 token 而没有 kernel 路径，不能推断端到端收益。

## C09｜Bridging the Embodiment Gap：无配对监督需要明确替代信号

[2605.03637v1](https://arxiv.org/abs/2605.03637v1)，第四作者。第 3 节任务、目标、结构与数据，第 4 节基线和机器人结果，第 5 节结论。task/agent latent 的双重对比目标，训练 encoder adapter、固定 VACE，完成 unpaired human→robot 视频编辑。**迁移**：把任务内容与执行主体两条监督画开；正交损失不自动证明独立，ICML 模板不作为录用证据。

## C10｜AvatarPointillist：表示设计可决定整篇章节次序

[2604.04787v2](https://arxiv.org/abs/2604.04787v2)，第六作者。第 3 节数据和表示，第 4 节自回归模型与 Gaussian 解码，第 5 节实验。Nersemble/GaussianAvatars、FLAME 绑定，量化坐标按 y-z-x 排序并带面索引，再解码可驱动高斯。已重点读第 3 节，未深读第 4 节全部损失。**迁移**：先解释序列中一个 token 是什么，再画生成器；量化和排序是复现所需定义。

## C11｜Manifold-Aware Exploration / SAGE-GRPO：局部稳定与全局约束分层写

[2603.21872v1](https://arxiv.org/abs/2603.21872v1)，第五作者。第 3 节基础和框架，第 4 节评估，第 5 节结论。微观层处理积分 SDE 的方差与梯度范数，宏观层使用 moving anchor 和逐步双重 trust region；以 Hunyuan/VideoAlign 奖励实验。**迁移**：将更新公式的稳定性目标与策略偏移约束分开；不能以一个奖励提高证明所有视觉指标提高。

## C12｜GlyphBanana：agent 系统要在每步定义中间产物

[2603.12155v1](https://arxiv.org/abs/2603.12155v1)，第三作者。流程为文字／风格提取、draft/typography、glyph 频率和 attention reweight 注入、风格修订；第 5 节 benchmark、第 6 节实验。还处理 LaTeX 公式和字体控制，后部模块未逐段深读。**迁移**：用输入／输出文件或对象界定各 agent，评价文字正确性与风格一致性，不能把多轮处理次数当作有效性证据。

## C13｜CARE-Edit：共享骨干内的专家分工需要可观察证据

[2603.08589v1](https://arxiv.org/abs/2603.08589v1)，第四作者。3.1 基础、3.2 路由总览、3.3 mask repaint、3.4 latent mixture、3.5 loss、3.6 数据；第 4 节任务比较、消融、专家分析，第 5 节讨论。Text/Mask/Reference/Base experts 由 top-k 路由，配负载均衡。**迁移**：路由矩阵图与分任务结果共同解释专家作用；动态路由不能直接命名为已证明的因果解耦。

## C14｜Video2LoRA：适配器的体积要和整个系统分账

[2603.08210v3](https://arxiv.org/abs/2603.08210v3)，第五／通信作者。第 3 节 LightLoRA、hypernetwork 和端到端适配，第 4 节数据、指标、定性与消融，第 5 节结论。冻结 CogVideoX5B I2V，由参考预测 rank-1 因子并使用共享辅助矩阵。**迁移**：图上分超网络、被调制层与固定骨干；小于 150MB 指适配部分。正文有关 joint optimization 与冻结表述需回查实现，不能原样延伸。

## C15｜ST-BiBench：benchmark 的主张由任务和评分共同限定

[2602.08392v2](https://arxiv.org/abs/2602.08392v2)，第三／通信作者。第 3 节指标，第 4 节任务分类与视觉 agent，第 5 节结果、融合与错误，第 6 节限制。区分战略规划、空间 grounding 与 16D 动作；成功由终态目标判断，Gaussian 加权手臂 grounding 是代理指标。**迁移**：先画任务→观测→动作→评分，避免把与黄金轨迹不同一概当错。

## C16｜LongVideoAgent：多 agent 的贡献要区分模型与数据整理

[2512.20618v1](https://arxiv.org/abs/2512.20618v1)，第四作者。第 3 节 master/grounding/vision agents，GRPO 只训练 master，决策预算固定；第 4 节 LongTVQA/+ 与比较消融，第 5 节结论。长视频数据由 TVQA 剧集合并并重建时间戳，保留原验证拆分。**迁移**：图中标工具返回物与调用预算；聚合已有 QA 不等于产生独立新标注。

## C17｜VideoCoF：reasoning token 的接口比名称更重要

[2512.07469v2](https://arxiv.org/abs/2512.07469v2)，第四作者。3.1 框架、3.2 see→reason→edit、3.3 RoPE、3.4 训练推理、3.5 数据，第 4 节 benchmark/消融，第 5 节结论。源视频保持 clean，reason/target 去噪；reason 索引 0、source/target 使用 1…F，减少伪影泄漏并处理长度扩展。**迁移**：用 token 时间轴解释信息流；latent reasoner 不等于可审阅的语言推理链。

## C18｜Cache Survey：综述的 taxonomy 应能指导选择

[2510.19755v3](https://arxiv.org/abs/2510.19755v3)，第 12 作者。I 引言分背景／挑战／动机，II 对照蒸馏、剪枝与硬件，III 按静态／动态等组织缓存。仅完成摘要、结构和 taxonomy 重点阅读，未逐段读完全部长篇内容。**迁移**：缓存对象、时间策略、决策信号、训练需求、执行收益组成可查询比较轴；不能由部分免训练方法推成缓存普遍无训练。

## C19｜DiTraj：控制接口与内部坐标不要混淆

[2509.21839v2](https://arxiv.org/abs/2509.21839v2)，第三／通信作者。第 3 节基础、前景／背景 prompt 区域引导与 STD-RoPE，第 4 节 Wan/CogVideoX 质量、控制和消融，第 5 节结论。以前景跨帧坐标对齐与密度变化调 apparent depth。**迁移**：图上分别画用户框轨迹与 attention 坐标变化；bbox 尺度变化不是测得的物理 3D 深度。

## C20｜ContextFlow：继承的数值方法和新增上下文机制分开认领

[2509.17818v2](https://arxiv.org/abs/2509.17818v2)，末位／通信作者。第 3 节动机、高阶 RF inversion、adaptive KV concat 和关键层分析，第 4 节比较消融，第 5 节结论，附录补协议。首帧用已有编辑器，高阶 solver 有既有来源。**迁移**：总图按 inversion、首帧编辑、视频传播分阶段，标清继承组件；没有额外权重不等于没有 inversion 开销。

## C21｜HiCache：理论主张必须保留假设

[2508.16984v2](https://arxiv.org/abs/2508.16984v2)，第十作者，PDF 列 ICLR 2026。第 3 节从 Taylor 有限差分问题到 Hermite 与双尺度，第 4 节任务及消融，第 5 节讨论，第 6 节结论。**迁移**：诊断图、近似公式、误差和实际耗时分别提供证据；经验 Gaussian 拟合及其假设不是任意特征分布的普遍定理。

## C22｜Forecast then Calibrate / FoCa：让预测与校正各有职责

[2508.16211v1](https://arxiv.org/abs/2508.16211v1)，第十作者。Related Work→Method（基础、总览、predict/correct）→Experiments→Conclusion。把 feature 演化组织为 ODE，历史 predictor 后接以最近完整计算特征为锚点的 Heun 校正；比较 T2I/T2V/SR 的质量和时间。**迁移**：时间图标历史、预测、真实刷新，研究激进缓存间隔的误差；feature ODE 不等于原采样 ODE。

## C23｜MILD：将局部泄漏连回分层生成

[2508.06543v2](https://arxiv.org/abs/2508.06543v2)，第四作者，PDF 标题有版本变化。第 3 节 CAG leakage、前景／背景层去噪、pose/parsing 形态学处理、空间 mask attention 和 loss；第 4 节实验，第 5 节频率／重组讨论，后有结论、伦理、复现。**迁移**：样例中圈出泄漏，再用层图说明信息隔离；未核查全部定理假设，不能宣称已验证严格解耦证明。

## C24｜GR-Gaussian：逆问题论文先定义可测的物理量

[2508.02408v2](https://arxiv.org/abs/2508.02408v2)，第二／通信作者，非共一。第 3 节 radiative Gaussian 基础、图表示与训练，第 4 节 X3D、真实 CT 和消融，第 5 节结论。去噪 FDK 初始化、KNN pixel graph、梯度驱动分裂。**迁移**：先给 forward projection 和重建目标，再解释 graph 正则与拓扑；生成视频的审美指标不能直接套入 CT 评价。

## C25｜MagicAnime：数据论文的样例和统计图各有责任

[2507.20368v1](https://arxiv.org/abs/2507.20368v1)，第五作者。I 引言、II 相关、III 来源／统计／处理、IV 任务／基线／指标／流程、V 结论。400k clips、50k pose、12k face、2.9k audio 是不同规模的标注或子集，不应默认互斥后相加；四类任务分别评估。**迁移**：数据流程、覆盖统计、任务样例三图分工；规模不能替代数据质量与划分说明。

## C26｜AvatarArtist：数据引擎→表示→渲染器组成闭环

[2503.19906v2](https://arxiv.org/abs/2503.19906v2)，第四作者，CVPR 2025 官方记录确认。第 3 节 GAN 多域 image/triplane 数据、latent DiT triplane、motion-aware cross-domain renderer；第 4 节定性定量与消融，第 5 节结论。**迁移**：每个表示转换注明输入输出；2D diffusion prior 与 GAN 数据来源承担不同角色，不能用一个“生成先验”框遮盖。

## C27｜Progressive Prompts：prompt 设计也应从骨干观察出发

[2501.07070v1](https://arxiv.org/abs/2501.07070v1)，末位／通信作者。方法按区域、prompt、embedding 组织；LLM 生成高／低层提示，DiT 深度诊断引导区域 cross-attention，区域正提示结合全局负提示，T5/CLIP 经 MLP 融合。**迁移**：提示内容、层位置和区域 mask 分开画；深浅层职责是特定模型的观察，不是通用认知定律。

## C28｜H-MBA：多尺度的组合需要清楚的索引

[2501.04302v1](https://arxiv.org/abs/2501.04302v1)，第三作者，PDF 列 AAAI 2025。第 3 节 Shikra/固定 CLIP/Vicuna 总览、C-Mamba、Q-Mamba，第 4 节实验，第 5 节结论。高低时间采样分别进入 temporal/divided/joint SSM，再以 query 自适应融合和当前帧残差输出。**迁移**：网格图标采样尺度与扫描维度，别把六条支路画成同义装饰；O(n) 不等于端到端延迟实测。

## C29｜UniPaint：任务统一由 mask 合同来定义

[2412.06340v2](https://arxiv.org/abs/2412.06340v2)，末位／通信作者。2024 首发，2025/26 venue 未核实。第 3 节基础、空间／时间双支路、MoE attention、时空 mask 训练，第 4 节比较消融，第 5 节限制，第 6 节结论。**迁移**：同一输入 mask 如何表达 inpainting、outpainting、interpolation 要在 formulation 中给清楚；共享结构不代表每个子任务都有同等充分的结果。

## C30｜Follow-Your-Pose v2：身份、遮挡与背景是不同残留问题

[2406.03035v4](https://arxiv.org/abs/2406.03035v4)，第四作者；主页列 ICLR 2025；当前标题为 Towards Multiple Character Image Animation Through Enhancing Implicit Decoupling。第 3 节基础，第 4 节 flow guider、depth order、reference pose、dilation mask 与结构，第 5 节比较消融，第 6 节结论。**迁移**：每个 guider 对齐一类错误并注明训练／推理差异，例如背景 flow 的推理处理；implicit decoupling 不可改写成数学独立。

## C31｜Taming Rectified Flow：数值保真与编辑可控分别评价

[2411.04746v3](https://arxiv.org/abs/2411.04746v3)，第五作者，ICML 2025。第 3 节 RF 基础→高阶 solver→RFEdit/V 特征注入，第 4 节采样／inversion／编辑及消融，第 5 节结论。**迁移**：先验证 inversion fidelity，再评估编辑与保留；更准确重建不是更强编辑的充分证据，solver 和编辑路径分图或分面板表达。

## C32｜MultiBooth：多概念联合使用需要额外的组合机制

[2404.14239v3](https://arxiv.org/abs/2404.14239v3)，第三作者，AAAI 2025。第 3 节基础、多模态概念图像与名称编码、单概念学习、区域定制 attention，第 4 节比较、消融和随概念数量的成本，第 5 节结论。**迁移**：区分单概念获取与多概念组合，说明 box 重叠时如何处理；只展示独立概念效果不足以证明组合能力。

## C33｜Follow-Your-Shape：先定位注入过强导致的失败

[2508.08134v4](https://arxiv.org/abs/2508.08134v4)，末位／通信作者，ICLR 2026。3.1 诊断过早／过强 KV 注入抑制形变，3.2 TDM 速度差与时序选择；第 4 节 ReShapeBench 120，第 5 节 PIE/新 benchmark/消融，第 6 节结论。先用早期 unconditional KV，再用后期 token 选择。**迁移**：同一控制机制在不同阶段可能利弊相反，时间轴应标切换依据；mask-free 可以存在内部区域图，早期 TDM 噪声也是适用边界。

## 身份待确认与范围外材料

下列六项保留候选身份，**不计入已确认作者作品和风格证据**：Follow-Your-Preference（2509.23082v1）、Preference++（2606.03216v1）、MultiMotion（2512.07500v2）、Unified Long Video Inpainting and Outpainting（2511.03272v2）、HERO（2508.17588v2）、GenAI Models Capture Urban Science（2505.13803v4）。同名、Tsinghua 署名、相似合作者或 Follow-Your 名称本身不足以完成身份消歧。

较早背景：Bridging the Gap（2311.16464v1，CVPR 2024）已核作者角色；MagicScroll（2312.10899v1，已读布局／逐层去噪／风格模块，项目标题有变）与 M-BEV（2312.12144v1）的 2025/26 venue 未确认或不在范围；主页注释块中的 SemanticAC 等只记为进一步补查线索，未称全文已读。AKU 只读官方框架材料。2019 区块链论文同名身份未确认。

“2025–2026 扩展”表示按首发年或已核验会议年检索、清理了本次找到的候选；受主页更新、索引与身份消歧限制，这不是对全网所有未来或未公开记录的穷尽保证。
