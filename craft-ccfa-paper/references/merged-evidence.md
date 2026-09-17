# 合并来源、覆盖与维护位置

合并日期：2026-09-17。本次整合已存在的资料和工具，没有新增一轮会议／作者论文检索，也没有重跑科学实验。

## 保留的三个来源

| 原技能 | 整合内容 | 维护位置 |
|---|---|---|
| craft-ccfa-paper | 研究、实验、证据记录、排版、审稿、SVG/PPTX 生产 | 根目录 `references/`、`scripts/`、`assets/` |
| write-top-ml-paper | 分章节、图表、整篇布局模式，会议元数据、全文结构样本和检索工具 | `modules/top-ml/` |
| mayue-paper-skill | 一作／共一核心研读、合作作品概览、章节／模块／图表案例、四张 SVG 模板 | `modules/mayue/` |

统一决策在主 `SKILL.md`、[integrated-writing](integrated-writing.md)、[integrated-figures](integrated-figures.md)。作者差异在 [mayue-overlay](mayue-overlay.md)，其他详细参考按需读。模块内沿用的命令路径相对于相应模块根目录；从外部执行时用明确的绝对路径或 [corpus tools](corpus-tools.md) 的根目录命令。

`$write-top-ml-paper`、`$mayue-paper-skill`、`$yue-ma-paper-style` 是兼容／profile 入口，均直接读取主技能，没有回调链。本机保留其原资源路径供旧脚本兼容，新任务维护和执行使用主技能内的资料。发行包包含主技能全部资料和三个入口，因此无需依赖旧版独立技能。原始入口也在合并前备份；[merge-manifest.json](merge-manifest.json) 记录来源文件哈希、映射与修改。

## 会议库：元数据与全文样本分开

快照日期 **2026-08-04**：官方源收集的 **25,421 条元数据**；成功提取全文结构的分层样本 **55 篇**，另有 13 个样本访问失败。标题／展示类别统计来自元数据，章节长度与结构统计来自成功的 PDF 样本。ICML 2026 在此快照中贡献元数据，未贡献成功全文样本。

会议、年份、来源状态及抽样方法见 [evidence-base](../modules/top-ml/references/evidence-base.md)，具体元数据见 [manifest](../modules/top-ml/references/corpus/manifest.json)，提取统计见 [analysis summary](../modules/top-ml/references/analysis/analysis_summary.json)。本包未附完成的全量全文报告，不把可续跑分析器等同于已完成分析。

当年尚未公开或未来的 venue 状态是快照记录，不代表合并当天或未来仍未公开。只有需要当前数据时才刷新官方源。通用流程可支持其他 CCF-A 学科，但本会议语料主要是 ML/CV，不能据此声称覆盖了所有 CCF-A 会议、学科或每篇全文。

## 作者库：核心研读与结构概览分开

核查截至 **2026-09-16**：**24 篇一作／共一方法论文 + 1 篇综述**进行了章节、主要模块和实验研读；**33 篇其他合作论文**为结构／模块阅读，部分协议补读；另有 **6 篇未确认同名候选、3 篇较早背景 PDF**。记录 **67 个唯一固定版本 PDF** 的来源，但发行包不包含完整 PDF。AKU 仅有框架学习，不计入核心方法数量。

**53 条已确认身份记录**满足首发年或已独立核验 venue 年在 2025/26。Canvas、Emoji、Motion 另有逐段图谱；并非所有记录都逐句精读。核查采用作者主页、项目／官方来源及 arXiv 等有界检索，不能承诺全网穷尽；实验、延迟和全部视频效果未复现。

详情和固定版本见 [作者账本](../modules/mayue/references/corpus-2025-2026.md)、[JSON 账本](../modules/mayue/references/corpus-2025-2026.json) 和 [source manifest](../modules/mayue/references/source-manifest.json)。不同库可能重叠，不把元数据、全文样本、作者卡片数量直接相加为“精读论文总数”。来源图摘录及原文件许可证／归属保持不变。

## 验证能说明什么

技能格式、内部链接、来源文件保留、语料查询及绘图工具的运行检查可验证整合和可用性；它们不验证研究结论，不证明作者个人写法，也不保证录用。对于实际论文，仍需按用户材料完成真正写作、实验解释、编译与视觉检查。
