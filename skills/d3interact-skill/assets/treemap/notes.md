# Treemap 矩形树图 — 使用说明

## 何时使用
层级数据，但你更关心叶节点的大小而非层级本身。最适合 2-3 层、多叶节点的"什么主导整体？"任务。

## 必填占位符
同 Sunburst（TITLE / EYEBROW / H1_LEFT / H1_EM / H1_RIGHT / LEDE / META_TITLE / META_SUB / META_DATA / ROOT_NAME / UNIT / DATA / COLORS）。

## 数据结构
与 Sunburst 完全一致：
```javascript
{ name: "Root", children: [
  { name: "类目 A", children: [
    { name: "叶 A1", value: 10 },
    { name: "叶 A2", value: 5 }
  ]},
  { name: "类目 B", value: 20 }
]}
```

## 交互

| 操作 | 结果 |
|------|------|
| 悬停单元格 | tooltip + 其他单元格变暗 + 详情面板更新 |
| 点击有子的单元格 | 下钻到该子树（成为新根） |
| 点击面包屑 | 跳回该层级 |
| 悬停右侧 top-list | 联动高亮对应单元格 |

## 定制需求

| 用户需求 | 怎么做 |
|---------|--------|
| 不同的方块算法 | D3 默认 squarified；备选 `d3.treemapBinary` 或 `d3.treemapSlice` |
| 显示更小标签 | 调整可见阈值 `(d.x1-d.x0) > 60`，比如改为 `40` |
| 各层级对比更强 | 在 `colorFor` 里加大层级间的 `hsl.l` 跳跃 |
| 扁平 treemap，不要下钻 | 预先把数据拍扁为 1 层；移除 `render(c)` 调用 |

## 限制
- 同屏可见叶节点超过 ~500 → 标签消失；建议过滤或把小项合并为"其他"
- 极细的矩形（长宽比悬殊）变得不可读。如果数据极度不平衡，建议改用 Sunburst
