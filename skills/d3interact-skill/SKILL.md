---
name: d3interact-skill
description: 用D3.js构建高质量交互式可视化，输出独立可运行的HTML文件——支持旭日图、矩形树图、桑基图、力导向网络、和弦图、雷达图、平行坐标、地理分级填色图。当用户要求制作、设计、渲染或可视化层级数据、流向数据、网络/图谱数据、双向关系矩阵、多维属性、地理数据时使用本skill，或用户直接点名这些图类型时使用，也适用于"交互式可视化"、"可探索图表"、"下钻分析"、"可筛选图表"等需求。输出深色主题的单文件HTML，使用d3.v7、自定义字体排印、三栏布局（图例/图表/详情面板），内置丰富交互（悬停高亮、点击下钻、tooltip、刷选、联动视图）。不用于静态条形/折线/散点图等常规类型图。
---
# d3-interactive-skill

构建打磨精良、可交互的 D3.js 可视化，输出单文件 HTML。支持 8 种图类型：**旭日图（sunburst）**、**矩形树图（treemap）**、**桑基图（sankey）**、**力导向图（force-directed）**、**和弦图（chord）**、**雷达图（radar）**、**平行坐标（parallel coordinates）**、**地理分级填色（choropleth）**。

## 什么情况下使用本 skill

仅当以下三条**全部**成立时触发：

1. 用户想要的是**交互式可视化**（悬停、点击、下钻），而非静态图表
2. 数据形态匹配上述 8 种习语之一（层级、流向、网络、矩阵、多维、地理）
3. 交付物是**独立可运行的 HTML 文件**，用户会打开或嵌入它

如果用户只是想要"一张月销售额图表"或要求条形/折线/散点图，本 skill 不适用——直接说明并建议其他方式。

## 工作流

按顺序执行以下步骤。**不要跳过第 2 步**。

### 第 1 步——理解数据与任务

询问用户（或根据已有信息推断）：

- 数据是什么形态？（树？流？网络？矩阵？多维记录？地理？）
- 用户希望读者从图中看出什么？（占比？路由？聚类？相关性？地理模式？）
- 大概多少条目/层级/节点？

### 第 2 步——读决策指南

```
读取：references/selection-guide.md
```

这份文件包含从"数据形态 + 任务"到"图类型"的完整决策树，列出每种习语的优点、局限和扩展能力上限。**不要凭印象或感觉选图——逐条走决策树**。

### 第 3 步——推荐 1-2 个候选并说明理由

跟用户说类似这样的话：

> 根据你描述的——[复述数据 + 任务]——我建议：
>
> **首选：[X]**——[理由，结合数据形态与任务]。
>
> **备选：[Y]**——[另一个角度的解法]。如果 [条件] 则选这个。
>
> 你想要哪个？或者我帮你决定？

不要列出全部 8 个选项——那等于把决策推回给用户。两个有理有据的候选既给用户选择权，又不过载。

### 第 4 步——等用户确认

让用户决定。如果用户不确定，推荐首选并简要说明。在用户明确表态前**不要**开始动工。

### 第 5 步——读对应模板的资源

```
读取：assets/<图类型>/template.html  （要填的 HTML 主体）
读取：assets/<图类型>/notes.md       （占位符列表、定制提示、已知限制）
读取：assets/<图类型>/sample-data.json  （只在用户未提供数据时用作回退示例）
```

### 第 6 步——读设计规范（如需定制）

```
读取：references/design-system.md
```

仅当用户要求改色、改字体、改布局时需要。模板默认已遵循设计规范。

### 第 7 步——填模板

把 `template.html` 里的每一个 `{{占位符}}` 替换成实际内容。每张图的 notes 文件都列出了完整占位符清单和每项填什么。

所有图都需要的通用占位符：

- `{{TITLE}}`——浏览器标签页标题
- `{{EYEBROW}}`——顶部小标签，等宽大写
- `{{H1_LEFT}}` / `{{H1_EM}}` / `{{H1_RIGHT}}`——主标题三段拆分（中间词为斜体高亮）
- `{{LEDE}}`——1-2 句引导文，结尾给一个交互提示
- `{{META_TITLE}}` / `{{META_SUB}}` / `{{META_DATA}}`——右上角项目元信息
- `{{UNIT}}`——单位短串（如 `GT CO₂`、`users`、`$M`）
- `{{DATA}}`——数据字面量（对象、数组或矩阵，按图类型而定）
- `{{COLORS}}`——分类色映射对象（类目名 → 十六进制色）

每张图特有的占位符在各自的 notes.md 中说明。

### 第 8 步——输出文件

把填好的 HTML 写到 `/mnt/user-data/outputs/<有意义的文件名>.html`，然后调用 `present_files` 让用户能下载/打开。

## 重要规则

### 数据保真

- 用户给的真实数据，**原样使用**。不要伪造或"四舍五入"用户的数字。
- 用户没给数据时，用对应图的 `sample-data.json` 作为合理占位符，**并主动告知用户**。
- 数据必须合法（不能有 NaN，尺寸编码的标记不能为负值）。

### 遵循设计规范

- 默认深色主题 + 琥珀色强调（`--accent: #f0c674`）。除非用户明确要求改色，否则不要改。
- 字体只用 Fraunces + Inter Tight + JetBrains Mono 三件套。**禁用 Inter、Arial、Roboto、Helvetica** 这些 AI 默认味的字体。
- 分类色板是 `references/design-system.md` 里定义的 7 种色相——不要自创新色。
- 每张图必须包含：悬停高亮+其他变暗、tooltip、联动详情面板、入场错峰动画。

### 用户常见定制请求

每张图的 notes.md 都有一张定制对照表。最常见的几条：

- 改强调色 → 覆盖 `--accent` CSS 变量
- 换整体配色主题 → 替换分类色板
- 隐藏 tooltip / 详情面板 → 删掉相应 div 和事件绑定
- 数据条目超过图能承受的上限 → 建议换图，或把小类目预聚合为"其他"

### 不要过度工程化

- 一个 artifact = 一张图。除非用户要求，不要在一个文件里混搭多种图类型。
- 不要添加用户没要求的功能。模板已经功能完整。
- 用户要求"导出 PNG 按钮"、"搜索"、"图片"等额外功能 → 说明这些超出 skill 范围，可以单独再做。

## Skill 文件清单

```
SKILL.md                        ← 本文件
references/
  selection-guide.md            ← 决策树：何时用哪种习语
  design-system.md              ← 配色、字体、布局、动效、无障碍
assets/
  sunburst/         template.html  notes.md  sample-data.json
  treemap/          template.html  notes.md  sample-data.json
  sankey/           template.html  notes.md  sample-data.json
  force-directed/   template.html  notes.md  sample-data.json
  chord/            template.html  notes.md  sample-data.json
  radar/            template.html  notes.md  sample-data.json
  parallel-coords/  template.html  notes.md  sample-data.json
  choropleth/       template.html  notes.md  sample-data.json
```

每个 template 都是独立运行的 HTML 文件（从 CDN 加载 D3），无构建步骤、无依赖，只需现代浏览器即可打开。
