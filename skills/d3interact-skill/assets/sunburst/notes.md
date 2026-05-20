# Sunburst 旭日图 — 使用说明

## 何时使用
层级数据，2-5 层，≤ 200 叶节点，任务是部分-整体 + 下钻。

## 必填占位符
| 占位符 | 填什么 | 示例 |
|--------|--------|------|
| `{{TITLE}}` | 浏览器标签页标题 | `全球碳排放结构` |
| `{{EYEBROW}}` | 顶部小标签（mono，大写）| `可视化习语 · 旭日图 · 2024` |
| `{{H1_LEFT}}` | 主标题第一段 | `碳排放的` |
| `{{H1_EM}}` | 高亮词（斜体强调色）| `重量` |
| `{{H1_RIGHT}}` | 主标题第三段 | `分布于各大洲。` |
| `{{LEDE}}` | 1-2 句引导，结尾给交互提示 | `点击任意扇形即可下钻……` |
| `{{META_TITLE}}` | 右上项目名 | `Skill 演示` |
| `{{META_SUB}}` | 子学科/类型 | `Sunburst · D3` |
| `{{META_DATA}}` | 数据来源标识 | `2024 (示意数据)` |
| `{{LEGEND_TITLE}}` | 左侧图例区段标题 | `大洲` |
| `{{ROOT_NAME}}` | 根节点显示名 | `全球排放` |
| `{{UNIT}}` | 数值单位（短）| `GT CO₂` |
| `{{DATA}}` | 层级数据的 JS 字面量 | 见下方 |
| `{{COLORS}}` | 顶层名 → 十六进制色的 JS 对象 | 见下方 |

## 数据结构

```javascript
const data = {
  name: "Root",
  children: [
    {
      name: "类目 A",
      children: [
        { name: "子 A1", value: 10 },
        { name: "子 A2", children: [
          { name: "叶 A2a", value: 3 },
          { name: "叶 A2b", value: 7 }
        ]}
      ]
    },
    { name: "类目 B", value: 25 }
  ]
};
```

规则：
- 每个叶节点必须有数值 `value`
- 非叶节点有 `children`（值自动求和）
- 一个节点要么是叶，要么有子，**不能同时**

## 配色

```javascript
const topLevelColors = {
  "类目 A":  "#e36a4a",
  "类目 B":  "#f0c674",
  "类目 C":  "#7fb8a4",
};
```

从分类色板（见 `references/design-system.md`）选。内层自动衍生同色相的更浅版本。

## 常见定制需求

| 用户需求 | 怎么做 |
|---------|--------|
| 多于 3 层 | `partition.size([2*PI, root.height + 1])` 自动适配；只需检查标签是否还能读 |
| 换主题色 | 覆盖 `--accent` 和 `--accent-2` CSS 变量 |
| 隐藏 tooltip | 删掉 `.tip` div 和 `mouseEnter` 里设置 tooltip 的代码 |
| 显示百分比而非数值 | 把 `centerNum` 文本改为 `(p.value/totalValue*100).toFixed(1)`，单位改 `%` |
| 限制只在顶层下钻 | 点击 handler 加 `if (d.depth > 1) return;` |

## 已知限制
- 超过 5 层深度，即使下钻外圈标签也会消失。建议改用 `treemap`，如果叶节点比层级更重要
- 极端不平衡的树（一支占 90% 体量）会塌成"一个扇形 + 一堆碎片"。建议把主导分支单独画一张
