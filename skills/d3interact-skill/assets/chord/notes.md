# Chord 和弦图 — 使用说明

## 何时使用
固定实体集合之间的双向流动（贸易、迁徙、引用）。最佳 6-15 个类目，超过 20 会崩塌。

## 必填占位符
TITLE / EYEBROW / H1_LEFT / H1_EM / H1_RIGHT / LEDE / META_TITLE / META_SUB / META_DATA / LEGEND_TITLE / ROOT_NAME / DEFAULT_HINT / UNIT / NAMES / DATA / COLORS

## 数据结构

方阵，`matrix[i][j]` 是从实体 i 到实体 j 的流量：

```javascript
const names = ["美国", "中国", "欧盟", "日本"];
const matrix = [
  [0,   50, 30, 20],
  [40,   0, 25, 18],
  [28,  22,  0, 12],
  [15,  10,  8,  0]
];
```

对角线通常为 0（无自循环）。非对角元素编码定向流——`matrix[i][j]` 可与 `matrix[j][i]` 不同，和弦图会用一条缎带两端不同粗细来表达。

## 配色

```javascript
const colorMap = {
  "美国":   "#e36a4a",
  "中国":   "#f0c674",
  "欧盟":   "#7fb8a4",
  "日本":   "#b88ec2"
};
```

## 交互

| 操作 | 结果 |
|------|------|
| 悬停弧 | 高亮该实体及其所有缎带；右栏显示 top 伙伴 |
| 悬停缎带 | 显示双向流量；右栏显示这一对 |
| 悬停图例 | 同悬停弧 |

## 定制需求

| 用户需求 | 怎么做 |
|---------|--------|
| 按总流量排序弧 | `d3.chord().sortGroups(d3.descending)` |
| 缎带间距加大 | 把 `chord.padAngle(0.04)` 加大到 0.08 |
| 缎带按目标色 | ribbon `fill` 改用 `colorMap[names[d.target.index]]` |

## 限制
- 超过 15 实体缎带严重重叠。建议合并小伙伴，或改用 Sankey
- 不能精确读绝对值，用户需要靠 tooltip/面板
