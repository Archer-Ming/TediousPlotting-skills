# Force-Directed 力导向图 — 使用说明

## 何时使用
图谱数据（节点 + 边），无固定层级。最适合发现聚类、关键节点、桥梁。最多约 200 节点，理想 < 50 节点。

## 必填占位符
TITLE / EYEBROW / H1_LEFT / H1_EM / H1_RIGHT / LEDE / META_TITLE / META_SUB / META_DATA / LEGEND_TITLE / UNIT / DEFAULT_HINT / DATA / COLORS

## 数据结构

```javascript
{
  nodes: [
    { id: "张三", group: "工程", value: 5 },
    { id: "李四", group: "设计", value: 3 },
    { id: "王五", group: "工程", value: 8 }
  ],
  links: [
    { source: "张三", target: "李四", value: 2 },
    { source: "张三", target: "王五", value: 5 }
  ]
}
```

用 `id`（字符串）作 source/target，**不要用索引**。`value` 可选（默认 1，决定连线粗细）。

## 配色

```javascript
const groupColors = {
  "工程": "#e36a4a",
  "设计": "#f0c674",
  "产品": "#7fb8a4"
};
```

## 交互

| 操作 | 结果 |
|------|------|
| 悬停节点 | 高亮该节点 + 邻居；其他变暗 |
| 拖拽节点 | 移动节点；松开后回归模拟 |
| 鼠标滚轮 | 缩放 |
| 拖拽背景 | 平移 |
| 悬停图例组 | 该组以外的变暗 |
| 悬停详情面板的连接 | 高亮对应那条边 |

## 调节模拟力

默认力参数面向中等规模图谱。需要时调整：

```javascript
.force("link", d3.forceLink().distance(70))      // 边长——太挤就加大
.force("charge", d3.forceManyBody().strength(-220))  // 排斥力——负值越大越分散
.force("collide", d3.forceCollide().radius(...))  // 防重叠
```

密集图（>100 节点）建议 `charge.strength` 调到 -400，`link.distance` 调到 120。

## 限制
- 超过 ~150 节点变"毛球"，建议预先过滤或做社群检测
- 力布局非确定性；同样数据每次位置不同。如果用户需要稳定位置，预计算并设 `fx`/`fy`
