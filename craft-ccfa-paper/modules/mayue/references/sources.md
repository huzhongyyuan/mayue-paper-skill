## 09｜来源、版本与本次学习的边界

### 9.1 原始论文与官方入口

下表是可回查的来源索引；逐篇分析使用固定 arXiv 版本。作者／会议信息有时来自项目页，已在第 2 节分别注明。访问与本地核查日期为 2026-09-16。

| 编号 | 固定版本／正式记录 | 官方项目或代码 |
|---|---|---|
| P01 Pose | [2304.01186v2](https://arxiv.org/abs/2304.01186v2) | [FollowYourPose](https://github.com/mayuelala/FollowYourPose) |
| P02 MagicStick | [2312.03047v2](https://arxiv.org/abs/2312.03047v2) | [项目](https://magic-stick-edit.github.io/) |
| P03 Click | [2403.08268v1](https://arxiv.org/abs/2403.08268v1) | [项目](https://follow-your-click.github.io/) |
| P04 Emoji | [2406.01900v3](https://arxiv.org/abs/2406.01900v3) | [项目](https://follow-your-emoji.github.io/) |
| P05 COVE | [2406.08850v2](https://arxiv.org/abs/2406.08850v2) | [项目](https://cove-video.github.io/) |
| P06 Canvas | [2409.01055v1](https://arxiv.org/abs/2409.01055v1) | [项目](https://follow-your-canvas.github.io/) |
| P07 DiT4Edit | [2411.03286v2](https://arxiv.org/abs/2411.03286v2) | [代码](https://github.com/fkyyyy/DiT4Edit) |
| P08 Creation | [2506.04590v1](https://arxiv.org/abs/2506.04590v1) | [项目](https://follow-your-creation.github.io/) |
| P09 Motion | [2506.05207v4](https://arxiv.org/abs/2506.05207v4) | [代码](https://github.com/mayuelala/FollowYourMotion) |
| P10 Faster | [2509.16630v1](https://arxiv.org/abs/2509.16630v1)；[IJCV DOI](https://doi.org/10.1007/s11263-025-02685-z) | [Emoji 项目](https://follow-your-emoji.github.io/) |
| P11 FastVMT | [2602.05551v3](https://arxiv.org/abs/2602.05551v3) | [代码](https://github.com/mayuelala/FastVMT) |
| P12 Group Editing | [2603.22883v3](https://arxiv.org/abs/2603.22883v3) | [项目](https://group-editing.github.io/) |
| P13 EasyVFX | [2605.22051v1](https://arxiv.org/abs/2605.22051v1) | [项目](https://easy-vfx.github.io/) |
| P14 LiveLight | [2608.01771v1](https://arxiv.org/abs/2608.01771v1) | [项目](https://living-lighting.github.io/) |
| P15 Survey | [2507.16869v3](https://arxiv.org/abs/2507.16869v3) | [综述列表](https://github.com/mayuelala/Awesome-Controllable-Video-Generation) |
| P16 AKU | [ACM DOI](https://doi.org/10.1145/3503161.3548257) | [官方仓库](https://github.com/mayuelala/AKU)；未取得全文 |

作者入口：[GitHub](https://github.com/mayuelala) · [主页](https://mayuelala.github.io/) · [Scholar](https://scholar.google.com/citations?user=kwBR1ygAAAAJ&hl=zh-CN)。作者顺序与共一符号优先核对 PDF 首页；主页和仓库用于身份及项目交叉核查。

作者身份排查用的其他版本：[Rectified Flow 2411.04746v3](https://arxiv.org/abs/2411.04746v3)、[Bridging the Gap 2311.16464v1](https://arxiv.org/abs/2311.16464v1)、[MultiBooth 2404.14239v3](https://arxiv.org/abs/2404.14239v3)、[Follow-Your-Shape 2508.08134v4](https://arxiv.org/abs/2508.08134v4)。这些不作为本手册的核心一作／共一风格样本。

### 9.2 图与源码的可回查记录

四个源码入口：[Pose](https://arxiv.org/src/2304.01186v2)、[Emoji](https://arxiv.org/src/2406.01900v3)、[Canvas](https://arxiv.org/src/2409.01055v1)、[Motion](https://arxiv.org/src/2506.05207v4)。图中文字、路径和字体结论应结合第 7.1 节文件名回查。

随包提供 [source-manifest.json](source-manifest.json)，记录论文版本、本地核查文件的 SHA-256 与图预览来源；[drawing-evidence.json](drawing-evidence.json) 保存四个源码包的图 metadata 与关键字体提取结果。它们用于定位版本与证据，不替代阅读论文。

学习图为作者团队公开论文／仓库图的压缩预览，版权与学术贡献归原作者团队。本手册没有将其重新标成原创，也没有提供整套论文 PDF 镜像。`templates/` 中四张结构图与其代码是本次原创模板，不含原作样例图像。

### 9.3 覆盖范围与未做事项

本次重点覆盖 24 篇确认一作／共一的方法论文、1 篇综述的章节与核心模块，并补充 33 篇合作论文的结构／模块阅读；Canvas、Emoji、Motion 进一步做了 Introduction 的逐段功能分析，并结合源码阅读摘要、方法、实验和结论。其余作品提供逐章节功能地图，**不是每一自然段的全文精注，也不是全论文逐字翻译**。

已阅读公开 PDF／项目／部分 TeX 源码，并检查关键静态图。未复现实验、未验证运行速度、未系统播放并评测所有视频，也未取得作者内部写作记录和图的编辑原稿。AKU 只提供有限的框架分析。这个范围足以形成可复用写作与图形组织规则，但不能据此宣称掌握作者所有作品或真实创作心理。

未来用于新论文时，还需围绕你的具体任务更新最近邻文献、读取真实实验与目标 venue 规则。这份手册提供组织与诊断方法，不预先替你的研究证明新颖性或效果。


扩展版本与身份请查 [2025–2026 账本](corpus-2025-2026.md)，新增核心卡见 [逐章扩展](core-cards-2025-2026.md)，其他合作论文见 [结构索引](collaborator-cards.md)。
