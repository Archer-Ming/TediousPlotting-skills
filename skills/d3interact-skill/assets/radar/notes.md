# Radar 雷达图 — 使用说明

## 何时使用
在相同的 4-8 个属性上比较 2-5 个条目，属性量纲可比（如 0-100 评分）。

## 必填占位符
TITLE / EYEBROW / H1_LEFT / H1_EM / H1_RIGHT / LEDE / META_TITLE / META_SUB / META_DATA / LEGEND_TITLE / DEFAULT_HINT / UNIT / DATA / COLORS / **MAX_VAL**

`MAX_VAL` 是所有轴的上限（如百分制就填 100）。

## 数据结构

```javascript
{
  axes: ["速度", "动力", "舒适", "续航", "价格"],
  items: [
    { name: "车 A", values: [80, 60, 90, 70, 40] },
    { name: "车 B", values: [60, 90, 50, 80, 60] },
    { name: "车 C", values: [70, 70, 70, 60, 75] }
  ]
}
```

所有 `values` 数组长度必须与 `axes` 相同。数值应在可比的量纲上（图默认 0 → `MAX_VAL`）。

## 配色

```javascript
const colorMap = {
  "车 A": "#e36a4a",
  "车 B": "#f0c674",
  "车 C": "#7fb8a4"
};
```

每个条目一种色。多边形默认 18% 填充透明度，重叠仍可读。

## 交互

| 操作 | 结果 |
|------|------|
| 悬停多边形 | 高亮该条目，其他变暗 |
| 悬停顶点 dot | tooltip 显示 条目×轴 值 + 该轴排名 |
| 悬停图例 | 同悬停多边形 |
| 点击图例 | 切换显隐 |

## 定制需求

| 用户需求 | 怎么做 |
|---------|--------|
| 各轴用不同量纲 | 入参前把值归一化到 0-1；`MAX_VAL = 1` |
| 更多网格圈 | 改脚本中的 `levels = 5` |
| 实心多边形 | `.shape { fill-opacity: 0.5 }` |
| 隐藏顶点 dot | 删掉 `dotGroup` 整段 |

## 限制
- 条目超过 5 个 → 多边形交织成乱麻。建议改用 small multiples（每条目一张图）
- 轴的顺序很重要——不同顺序会暗示不同规律。记录使用的顺序
- 不要用雷达表达有序数据（轴应是定类类别）
