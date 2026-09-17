# Mayue profile：接入统一流程的作者案例层

调用 `$mayue-paper-skill`、`$yue-ma-paper-style`，或用户已明确选择马跃风格时使用。本文件与统一写作、图表流程配合，不触发另一套完整技能。只读当前任务所需的作者 playbook 和 1–3 张匹配卡片。

## 风格如何发挥作用

从公开合作论文中提炼：**控制任务→已观察的失败或明确约束→可检验机制→具体操作→匹配证据**。这条链适用于与之相符的工作；不可把未验证判断写成实证发现。学习论证、模块和视觉组织，写用户自己的内容，不照抄句子或把作者成稿当作私人创作过程的记录。

- 写章节：读 [writing-playbook](../modules/mayue/references/writing-playbook.md)，包含各章节职责及 Canvas/Emoji/Motion 段落图谱。
- 改稿：读 [revision-playbook](../modules/mayue/references/revision-playbook.md)，交付实际改写和重要含义变化。
- Idea：读 [idea-evidence](../modules/mayue/references/idea-evidence.md)，将假设映射到最小诊断和对照。
- 画图：按 [统一图表流程](integrated-figures.md) 生产，使用 [figure-playbook](../modules/mayue/references/figure-playbook.md) 的案例和布局分析，或 [figure-execution](../modules/mayue/references/figure-execution.md) 的图注与执行细节。
- 学论文：先查 [初始核心卡片](../modules/mayue/references/paper-cards.md) 和 [新增核心卡片](../modules/mayue/references/core-cards-2025-2026.md)；其他合作者作品另查 [collaborator-cards](../modules/mayue/references/collaborator-cards.md)，不据此认定为个人风格。
- 整篇练习：需要时读 [practice](../modules/mayue/references/practice.md)。

## 根据技术问题选组织方式

数据／阶段拆分可参考 Pose、Calligrapher；诊断因素与残留问题可参考 Canvas；表示与监督可参考 Emoji；骨干／head 响应可参考 Motion；计算冗余可参考 EEdit、EVCtrl、SkipVAR、FastVMT；实例隔离可参考 MultiPose、InstanceAnimator；跨镜头上下文可参考 MSEditor；在线操作可参考 LiveLight。案例中的阶段数与模块数不是模板要求，MultiPose 也展示了将 Related Work 并入 Introduction 的结构。

正文、公式、图标签和消融使用相同模块命名与依赖。用统一的七项模块信息检查科学含义；是否成立由用户实现与实验决定。

## 保留的作者与科学证据边界

一作／共一依据等贡献署名，不能用排序或 GitHub 所有权推断。COVE、Canvas、DiT4Edit 的第二共一和 InstantSwap 的第三共一均在核心内。MultiPose 是已确认共一，但 2024 首发，2025/26 venue 未核实。Creation 的用户所列 ICLR 2026 未独立确认。同名候选不进入作者风格证据。版本、身份和范围见 [corpus ledger](../modules/mayue/references/corpus-2025-2026.md)。

使用相关案例时保留这些具体修正：

- Training-free 可以仍含推理优化（FastVMT）、预先概念训练（InstantSwap），或冻结生成器但训练轻量分类器（SkipVAR）。
- FastVMT 在采样 step 内复用梯度；InstantSwap SSGU 在 latent 优化迭代之间复用，缓存对象和更新时钟不同。
- FPS 是吞吐，不能替代交互延迟；局部显存收益不等于总计算量恒定；面积扩展倍率不等于边长倍率。
- Head 分组、正交目标和 mask 不独立证明严格解耦；FID 不证明时序一致性。
- Creation 的 video inpainting 不证明完整显式 4D 重建；MSEditor 的 sparse attention 继承 HoloCine，保留组件来源。
- 原文表格与强表述冲突时（例如 InstantSwap Table 3），以实际数值缩小结论。

[Drawing evidence](../modules/mayue/references/drawing-evidence.json) 仅支持特定文件中的 PowerPoint/WPS/Matplotlib 导出或字体信息；Quartz 不单独证明绘图软件。未获得原作者 PPTX/FIG/AI，四张 SVG 是原创结构脚手架。原图摘录保留归属，仅用于研究。
