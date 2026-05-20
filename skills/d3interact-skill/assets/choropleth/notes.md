# Choropleth 地理分级填色图 — 使用说明

## 何时使用
数据与地理区域绑定（国家、省、县）。每个区域一个数值。最适合查看地理空间模式。

## 必填占位符
TITLE / EYEBROW / H1_LEFT / H1_EM / H1_RIGHT / LEDE / META_TITLE / META_SUB / META_DATA / LEGEND_TITLE / DEFAULT_HINT / UNIT / **GEOJSON** / **VALUES** / **ID_KEY** / **NAME_KEY** / **PROJECTION** / **INTERPOLATOR**

- `GEOJSON` — GeoJSON FeatureCollection（对象字面量）
- `VALUES` — 区域 ID → 数值的对象
- `ID_KEY` — GeoJSON `properties` 中用来匹配 `VALUES` 键的字段名（如 `"iso_a3"`、`"name"`、`"id"`）
- `NAME_KEY` — GeoJSON `properties` 中用作显示标签的字段（通常 `"name"`）
- `PROJECTION` — 之一：`"naturalEarth1"`、`"mercator"`、`"albersUsa"`
- `INTERPOLATOR` — D3 顺序插值器名（如 `"interpolateYlOrRd"`、`"interpolateViridis"`、`"interpolateBlues"`）

## 数据结构

```javascript
const geojson = {
  type: "FeatureCollection",
  features: [
    {
      type: "Feature",
      properties: { iso_a3: "USA", name: "United States" },
      geometry: { type: "Polygon", coordinates: [...] }
    },
    ...
  ]
};

const values = {
  "USA": 100,
  "CHN": 95,
  "DEU": 60,
  // 没出现在 values 里的区域会显示为灰色"无数据"
};
```

区域 ID 必须匹配——区分大小写。

## 怎么搞到 GeoJSON

模板不内置 GeoJSON。常见来源：
- **世界国家**：`https://raw.githubusercontent.com/nvkelso/natural-earth-vector/master/geojson/ne_110m_admin_0_countries.geojson`（用 `iso_a3` 作 ID key）
- **美国州**：`https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json`（TopoJSON——需用 topojson 转换）
- **自定义区域**：让用户自己提供 GeoJSON

如果用户没有 GeoJSON，建议用 natural-earth 国家数据 + ISO 三字代码匹配。

## 交互

| 操作 | 结果 |
|------|------|
| 悬停区域 | 高亮 + 其他变暗；tooltip + 右栏显示值、排名、对均值偏离、百分位 |
| 鼠标滚轮 | 缩放 |
| 拖拽地图 | 平移 |
| 悬停右上 top-N 行 | 在地图上高亮该区域 |

## 定制需求

| 用户需求 | 怎么做 |
|---------|--------|
| 换投影 | 改 `projection` 选项。美国本土用 `"albersUsa"`；导航用 `"mercator"`；世界视图用 `"naturalEarth1"`（默认）|
| 发散色阶 | `d3.scaleSequential` 换为 `d3.scaleDiverging`，用发散插值器（`"interpolateRdBu"`、`"interpolateBrBG"`）|
| 区域上显示标签 | `regions = ...` 之后追加 `zoomG.selectAll("text.region-label").data(geojson.features).join("text")...`，用 `path.centroid(d)` 定位 |
| 用气泡而非填色 | 这是另一种图（proportional symbol map），不在 choropleth 模板范围 |

## 限制
- 同屏 > 200 区域 → 小区域难点击；建议缩放或按子区域过滤
- 地图上的**面积**会扭曲感知——俄罗斯/加拿大不管值多少都显得很重。配套 top-N 列表（模板已含）做精确比较
- 错的投影会误导（Mercator 放大极地）。默认 `naturalEarth1` 是世界尺度最安全的选择

## 关键：数据必须与 GeoJSON 匹配

如果 `values` 里的区域 ID 与任何 GeoJSON feature 都不匹配，那些值会被静默丢弃。如果 `idKey` 写错，图看起来会"空空如也"。务必先验证：

```javascript
console.log(geojson.features.slice(0,3).map(f => f.properties[idKey]));
console.log(Object.keys(values).slice(0,3));
```

它们看起来应该像是能匹配的。
