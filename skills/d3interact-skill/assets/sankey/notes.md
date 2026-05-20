# Sankey 桑基图 — 使用说明

## 何时使用
流向数据：物质/能量/资金从源头穿过若干阶段到达汇点。2-5 阶段，每阶段 ≤ 15 节点，总连接 ≤ 100。

## 必填占位符
同 Sunburst 加：
- `{{STAGE_LABELS}}` — 阶段列标签数组，如 `["源头", "处理", "汇点"]`
- `{{DEFAULT_HINT}}` — 右栏占位提示文本，如 `"点击或悬停节点查看详情"`

## 数据结构

```javascript
{
  nodes: [
    { name: "煤炭" },
    { name: "石油" },
    { name: "电厂" },
    { name: "家庭" }
  ],
  links: [
    { source: "煤炭",     target: "电厂", value: 30 },
    { source: "石油",     target: "电厂", value: 20 },
    { source: "电厂",     target: "家庭", value: 45 }
  ]
}
```

节点 name 必须唯一字符串。用 name（非索引）作为 source/target。

## 配色

```javascript
const colorMap = {
  "煤炭": "#5b6068",
  "石油": "#c98a5b",
  "电厂": "#e36a4a",
  "家庭": "#7fb8a4"
};
```

只给"重点"节点上色——中间节点会自动继承。连接渐变从源色 → 目标色（格式塔连续性）。

## 交互

| 操作 | 结果 |
|------|------|
| 悬停节点 | 高亮该节点 + 所有连接；其他变暗；tooltip + 右栏显示节点统计 |
| 悬停连接 | 仅高亮该连接；tooltip 显示 源→目标 流量 |
| 点击节点 | （可选）切换持久聚焦 |

## 定制需求

| 用户需求 | 怎么做 |
|---------|--------|
| 节点间垂直间距更大 | `sankey.nodePadding(14)` 加大到 24 |
| 节点条更宽 | `sankey.nodeWidth(14)` 加大到 24 |
| 节点贴边对齐 | `sankeyJustify` 改为 `sankeyLeft`、`sankeyRight` 或 `sankeyCenter` |
| 连接只用源色 | 渐变两个 stop 都设为源色 |
| 显示方向箭头 | 加 `<marker>` defs，在连接上设 `marker-end` |

## 限制
- 每阶段超过 15 节点会严重交叉。建议拆为多张图
- 不支持循环流（`d3-sankey` 要求 DAG）。如有循环建议改用力导向图
