# 统一论文图、图注与可编辑绘制

先读方法／结果并确定图要回答的读者问题，再决定构图。用户请求“写图”时交付图计划；请求“画图”时实际生成源文件并检查渲染。用户只要一张图，不展开整篇论文流程。

## 一套语义与证据标准

对架构图核对节点、接口、箭头语义、参数来源、训练／推理状态和循环时钟；对结果图核对数据、样本、统计单位、误差定义、裁剪／时间点和对比条件。未知接口可能影响算法含义时先查实现，仍未知就明确标在草图中。

| 图的用途 | 通用构造 | 适用的 Mayue 案例／资源 | 实际交付 |
|---|---|---|---|
| Motivation / diagnostic | 固定其余条件，展示需要解释的失效／约束 | Canvas 的分辨率×面积扩展两轴；[motivation scaffold](../modules/mayue/assets/02-motivation.svg) | 实际诊断素材、布局源和受限解释；无诊断数据时仅交付标注草图 |
| Framework / method | 总路径、分区、关键模块放大、状态图例 | Pose/Emoji 的阶段与职责；[framework scaffold](../modules/mayue/assets/01-framework.svg) | JSON/SVG 或原生 PPTX、图注、检查过的预览 |
| Local context / correspondence | 全局到局部映射、索引、聚合关系 | Canvas/COVE 的对应路径；[window scaffold](../modules/mayue/assets/03-window-alignment.svg) | 可编辑节点和连接，准确表达采样／对齐／融合 |
| Streaming / caching | 历史、活动窗口、未来输出及更新时钟 | LiveLight；[streaming scaffold](../modules/mayue/assets/04-streaming.svg) | 时间轴和状态语义，区分吞吐、延迟及缓存成本 |
| Qualitative comparison | 同输入／控制、同时间、同裁剪，显示真实结果 | 多因素控制、身份／运动保持、失败样例 | 真实素材与确定性拼版脚本、可追踪 sample ID |
| Numerical / ablation / efficiency | 用日志绘图，展示协议、成本范围和不确定性 | 方法模块逐项消融；速度—质量或控制—保持权衡 | 数据、绘图代码、PDF/SVG、预览及图注 |

案例只在相关任务中使用。样本比例与视觉密度由实际方法、素材和版面决定；不能把模板布局解释为作者未公开的画图过程。

## 两条兼容的可编辑生产路线

**结构化图：** 使用本技能根目录的 `scripts/render_diagram_svg.py` 校验和渲染 JSON spec；需要原生 PPTX 时使用 `scripts/render_diagram_pptx.mjs`。同一套节点／边 ID 可对应不同 paper/slides 坐标，不要强行共用长宽比。脚本细节见 [figure-production](figure-production.md) 与 [ppt-diagrams](ppt-diagrams.md)。修改 spec 再生成，避免只改派生图。

**作者风格构图：** `modules/mayue/scripts/generate_templates.py` 生成四张原创 SVG scaffold，适合定制面板。可以直接编辑其分组 SVG，再从该源导出；这些自由 SVG 不是上述 JSON renderer 的输入，不声称可自动无损转换成原生 PPTX。指定 PPTX 时以同样语义重建原生形状并检查。作者研究图摘录在 `modules/mayue/assets/study-figures/`，保留归属，仅用于学习。

图表的通用信息层级见 [top-ML figure playbook](../modules/top-ml/references/figure-playbook.md)；Mayue 的具体案例、配色、分区与元数据证据见 [author figure playbook](../modules/mayue/references/figure-playbook.md) 和 [execution](../modules/mayue/references/figure-execution.md)。先按需要选一份，不同时加载所有图表资料。

## 图注与正文

根据真实图写：主题／任务→panel 或行列读法→符号、线型、状态或实验协议→图实际支持的认识。架构图解释计算路径，结果图给出比较条件与证据边界。不能在图注补出未运行的相同算力、统计显著性或不存在的去除分支。

贡献、模块、图标签与消融名称保持一致。把正文首引放在需要这张图的论证处；最终栏宽、单双栏跨度和浮动顺序使用论文版面计划。

## 验证和交付

先核对算法／数据，再检查最终尺寸下的字、箭头、遮挡、对齐和图例。过程预览压缩至尽量不超过 200,000 字节，小字问题局部裁剪；保留最终矢量和原始素材质量。

交付可编辑源、真实检查过的预览、可用的高质量导出与图注。数值图保留数据与脚本，定性图保留素材索引。将 SVG 嵌入 PPT 不能直接声称为原生形状可编辑；数值指标或原生编辑兼容性未验证时具体说明缺口。
