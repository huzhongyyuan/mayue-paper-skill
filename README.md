# Mayue Paper Skill

将 Yue Ma（马跃）一作／共一论文的写作与图表案例，接入 CCF-A 研究、实验、改稿和排版流程的 Codex 技能包。

这是独立整理的学习工具，与 Yue Ma 及其合作者无隶属或官方背书关系。学习公开论文中的论证与视觉组织，用于撰写用户自己的原创研究。

## 能做什么

- **研究与 idea：** 明确问题、机制假设、模块接口和最小对照实验。
- **逐节写作与改稿：** 标题、摘要、引言、相关工作、方法各模块、训练／推理、实验、局限与附录。
- **写图与画图：** 动机图、框架图、模块放大、时间轴、真实结果拼版、数值与消融图、caption。
- **可编辑制作：** SVG 模板，以及从结构化 JSON 生成 SVG／原生 PowerPoint 形状的工具。
- **整篇论文：** 页数预算、双栏排版、浮动体、证据检查、rebuttal 与报告准备。

## 安装

本仓库包含四个并列技能目录。`mayue-paper-skill/SKILL.md` 是入口，必须同时安装 `craft-ccfa-paper`；不要只下载单个 Markdown 文件。

在 Codex 中可直接请求：

> 从 https://github.com/huzhongyyuan/mayue-paper-skill 安装 craft-ccfa-paper、mayue-paper-skill、write-top-ml-paper 和 yue-ma-paper-style 四个路径，保持它们在同一个技能根目录下。若已有旧版本，先保留备份再更新。

或者使用 Codex 自带的技能安装器（全新安装；已有同名技能时安装器会拒绝覆盖）：

```bash
python3 "${CODEX_HOME:-$HOME/.codex}/skills/.system/skill-installer/scripts/install-skill-from-github.py" \
  --repo huzhongyyuan/mayue-paper-skill \
  --path craft-ccfa-paper mayue-paper-skill write-top-ml-paper yue-ma-paper-style
```

## 使用

```text
使用 $mayue-paper-skill，基于我的方法和实验逐节修改 Introduction，
让问题、洞察、模块和证据对应。给出实际改写，不补造结果。
```

```text
使用 $mayue-paper-skill，读取方法说明和代码，实际画一张论文框架图。
参考匹配的一作／共一案例，交付可编辑 SVG、原生形状 PPTX、预览和 caption。
```

```text
使用 $craft-ccfa-paper，检查并修改我的 LaTeX 双栏布局、图表位置和分页，
编译检查最终 PDF。
```

| 入口 | 行为 |
|---|---|
| [craft-ccfa-paper](craft-ccfa-paper/SKILL.md) | 统一研究、写作、图表与排版流程；按任务选择模式 |
| [mayue-paper-skill](mayue-paper-skill/SKILL.md) | 统一流程 + Mayue 一作／共一案例 |
| [write-top-ml-paper](write-top-ml-paper/SKILL.md) | 顶会通用模式；延续对话中已经选择的作者模式 |
| [yue-ma-paper-style](yue-ma-paper-style/SKILL.md) | 旧名称兼容入口 |

## 画图如何学习和执行

颜色表达稳定语义；总图定位模块，局部放大解释计算；显式表示训练状态、时间与缓存；动机图回应方法设计；正文、公式、箭头、图注与消融保持一致。

参见 [统一图表流程](craft-ccfa-paper/references/integrated-figures.md)、[作者图表案例](craft-ccfa-paper/modules/mayue/references/figure-playbook.md) 和 [逐节写作流程](craft-ccfa-paper/references/integrated-writing.md)。

Python 标准库即可生成四张原创 SVG 模板，以及运行结构化 SVG 工具。原生 PPTX 工具需要 Node.js 与 `pptxgenjs`；其他语料分析工具的依赖按对应脚本与参考说明配置。数值图需要用户的真实数据，定性图需要真实结果素材。

## 覆盖与验证边界

截至 2026-09-16，作者资料记录 24 篇一作／共一方法论文及 1 篇综述的章节、主要模块和实验研读；合作作品另有结构概览。Canvas、Emoji、Motion 有逐段图谱。图形资料包含 25 张带归属的代表性图摘录与 4 张原创 SVG 模板。

会议库快照为 2026-08-04：25,421 条官方源元数据与 55 篇成功提取 PDF 结构特征的样本。元数据不等于精读全文；以上范围不代表全网穷尽、所有图逐张研读或实验已复现。未取得原作者的 PPTX／FIG／AI 编辑工程。

本次合并检查了四个技能格式、101 个内部链接、来源文件保留、语料查询、初始化防覆盖、提交模式检查、SVG 生成与原生 PPTX 结构。未做 PowerPoint 应用内编辑测试、全量语料分析或独立写作行为评测。

详情见 [证据与维护说明](craft-ccfa-paper/references/merged-evidence.md) 和 [固定版本来源账本](craft-ccfa-paper/modules/mayue/references/source-manifest.json)。

## 来源与许可

保留原 `craft-ccfa-paper` 的 [MIT 许可](craft-ccfa-paper/LICENSE.txt)。第三方论文、图摘录及来源资料保留各自权利，不因收录而改为 MIT；详见 [来源归属说明](THIRD_PARTY_NOTICES.md)。仓库不附完整论文 PDF、私人会话、实验日志或原作者编辑工程。
