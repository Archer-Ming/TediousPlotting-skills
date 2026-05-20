# Parallel Coordinates 平行坐标 — 使用说明

## 何时使用
多记录（50-1000 条），每条有 4-15 个数值属性。最适合发现聚类、相关性、离群点——特别是当 brushing/筛选是核心任务时。

## 必填占位符
TITLE / EYEBROW / H1_LEFT / H1_EM / H1_RIGHT / LEDE / META_TITLE / META_SUB / META_DATA / LEGEND_TITLE / DEFAULT_HINT / UNIT / DATA / COLORS / **DIMENSIONS** / **GROUP_KEY**

- `DIMENSIONS` — 属性名数组（轴顺序，从左到右）
- `GROUP_KEY` — 用来给记录分类（决定颜色）的字段名

## 数据结构

记录数组。每条需要 `name`、`GROUP_KEY` 字段，以及每个维度一个数值。

```javascript
const data = [
  { name: "鸢尾-1",  species: "setosa",     sepal_length: 5.1, sepal_width: 3.5, petal_length: 1.4, petal_width: 0.2 },
  { name: "鸢尾-2",  species: "setosa",     sepal_length: 4.9, sepal_width: 3.0, petal_length: 1.4, petal_width: 0.2 },
  { name: "鸢尾-51", species: "versicolor", sepal_length: 7.0, sepal_width: 3.2, petal_length: 4.7, petal_width: 1.4 },
];

const dimensions = ["sepal_length", "sepal_width", "petal_length", "petal_width"];
const groupKey = "species";
```

Y 轴量程从各属性的 min/max 自动计算（`.nice()`）。

## 配色

```javascript
const groupColors = {
  "setosa":     "#e36a4a",
  "versicolor": "#f0c674",
  "virginica":  "#7fb8a4"
};
```

## 交互

| 操作 | 结果 |
|------|------|
| 沿任意轴拖动 | brush 刷选——只保留落入区间的线 |
| 再次点击已刷选区 | 释放该轴的 brush |
| 悬停一条线 | 高亮（右栏显示该记录所有属性）|
| 悬停图例 | 其他组变暗 |
| 点击图例 | 切换整组显隐 |
| 点击"清除所有筛选" | 重置所有 brush |

图保留 brush 状态——在第二个轴上加 brush 会做**交集**过滤（AND，不是 OR）。

## 定制需求

| 用户需求 | 怎么做 |
|---------|--------|
| 重排轴顺序 | 改 `DIMENSIONS` 字符串数组顺序 |
| 线条更不透明 | `.pc-line { stroke-opacity: 0.6 }`（默认 0.35）|
| 显示全部记录而非淡化 | `applyFilters` 里把不匹配的透明度调高 |
| 加分类轴 | 模板只假设数值轴；分类轴需要单独的 `scalePoint` 与自定义路径生成 |

## 限制
- 超过 ~500 条线 → 用 additive 混色（`mix-blend-mode: screen` 已开）并降低不透明度
- 类别属性不能做轴，用颜色编码（`groupKey`）
- 轴顺序强烈影响可见的规律。如果用户找不到相关性，建议互换相邻轴试试
