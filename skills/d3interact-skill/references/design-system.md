# 设计系统 — d3-interactive-viz

本文档定义所有模板共享的视觉语言。每张图都遵循这些规则。**每一条规则都基于感知科学，而非个人审美**——当你调整模板时，请保留其背后逻辑。

---

## 目录
1. [配色系统](#配色系统)
2. [字体排印](#字体排印)
3. [布局与构图](#布局与构图)
4. [交互模式](#交互模式)
5. [动效](#动效)
6. [背景氛围](#背景氛围)
7. [无障碍核查清单](#无障碍核查清单)

---

## 配色系统

### 基础色板（CSS 变量）

所有模板都使用以下变量。仅当用户要求换主题时才覆盖。

```css
:root{
  --bg-0:      #0b0d12;   /* 页面背景 */
  --bg-1:      #11141b;   /* 面板背景 */
  --bg-2:      #181c25;   /* 升起表面 */
  --line:      rgba(255,255,255,0.08);
  --line-2:    rgba(255,255,255,0.16);
  --ink:       #ecedef;   /* 主文本 */
  --ink-dim:   #9aa0aa;   /* 次文本 */
  --ink-mute:  #5b6068;   /* 三级 / 标签 */
  --accent:    #f0c674;   /* 暖琥珀，主强调 */
  --accent-2:  #e36a4a;   /* 赤陶，次强调 */
}
```

### 分类色板（编码类别时使用）

7 种色相，明度都在 60-70 区间，挑选时遵循：
- 红绿不单独承载语义（绿色弱视安全）
- 转为灰度后每种色相通过明度仍可区分
- 同时适配偏暖与偏冷的数据主题

```javascript
const categoricalPalette = [
  "#e36a4a",  // 赤陶
  "#f0c674",  // 琥珀
  "#7fb8a4",  // 鼠尾草绿
  "#c98a5b",  // 焦糖
  "#b88ec2",  // 丁香
  "#6a9bd1",  // 钢蓝
  "#d6b85a",  // 麦秆
];
```

### 顺序色板（编码有序/连续值）

使用感知均匀的单色相梯度。优先用保留色相、仅变明度/饱和度的插值器：

```javascript
// 好：保留色相，变明度
const sequentialAmber = d3.interpolateRgb("#3a2a1a", "#f0c674");

// 或用 d3-scale-chromatic
d3.interpolateYlOrRd  // 顺序暖色
d3.interpolateViridis // 感知均匀，色盲安全
```

### 发散色板（围绕中性中点编码 +/-）

双色经过中性灰渐变，**绝不能从纯红渐变到纯绿**。

```javascript
const diverging = d3.scaleDiverging()
  .interpolator(d3.interpolateRdBu)   // 红→白→蓝，安全
  .domain([-1, 0, 1]);
```

### 配色规则（含感知学依据）

1. **不要单独依赖颜色。** 色相必须搭配第二通道（标签、形状、明度）。约 8% 男性有某种红绿色盲；冗余编码不可妥协。

2. **色相只编码定类（类别）。** 有序数据应该用明度或饱和度——人眼无法感知"黄 > 蓝"这种色相顺序。

3. **分类色相不超过 7-8 种。** 超过后色相互相干扰难辨。再多就把小类合并成"其他"，或用空间分隔代替颜色。

4. **背景与前景对比 ≥ 4.5:1**（WCAG AA 标准）。对所有弧/元素填色与 `--bg-0` 做对比测试。

5. **强调色稀缺为贵。** `--accent` 和 `--accent-2` 仅用于：焦点元素、悬停态、激活选区、主要操作按钮。强调色撒得到处都是，预注意性弹出效应就死了（preattentive 处理需要稀缺性）。

---

## 字体排印

### 字体堆栈

```html
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,300;9..144,400;9..144,600;9..144,800&family=JetBrains+Mono:wght@300;400;500&family=Inter+Tight:wght@300;400;500;600&display=swap" rel="stylesheet">
```

| 角色 | 字体 | 理由 |
|------|------|------|
| **大标题 / 标题** | `Fraunces`（可变衬线） | 独特的光学尺寸轴，编辑设计感强；衬线确立视觉层级 |
| **正文 / UI** | `Inter Tight` | x-height 高、字距紧凑、小尺寸下极佳 |
| **等宽 / 标签 / 数字** | `JetBrains Mono` | 表格化数字对齐；提供"仪表盘"般的技术声调 |

**禁用：** Inter、Arial、Roboto、Helvetica、system-ui（都是 AI 默认味的字体）。

### 类型层级

```css
h1 { font-family: 'Fraunces', serif; font-weight: 300; font-size: clamp(38px, 4.4vw, 64px); line-height: 1.02; letter-spacing: -.02em; }
h1 em { font-style: italic; font-weight: 400; color: var(--accent); }

h2 { font-family: 'Fraunces', serif; font-weight: 300; font-size: 26px; letter-spacing: -.01em; }

.lede { font-size: 14px; line-height: 1.55; color: var(--ink-dim); max-width: 540px; }

.eyebrow { /* 类目小标签 */
  font-family: 'JetBrains Mono', monospace; font-size: 11px;
  letter-spacing: .28em; text-transform: uppercase; color: var(--ink-mute);
}

.label { font-family: 'JetBrains Mono', monospace; font-size: 10px; letter-spacing: .22em; text-transform: uppercase; }

.value { font-family: 'Fraunces', serif; font-weight: 300; font-size: 22px; }
.value small { font-family: 'JetBrains Mono', monospace; font-size: 11px; color: var(--ink-mute); margin-left: 4px; }
```

### 字体规则

1. **恰好混搭 3 种字体家族。** 再多视觉嘈杂，再少层级扁平。
2. **`<em>` 仅用于英雄词。** 只有一个高亮焦点，绝不多处。
3. **所有数值用表格化数字。** JetBrains Mono 本身等宽；对于比例字体用 `font-variant-numeric: tabular-nums`。
4. **标签用等宽 + 大写 + 宽字距。** 这种模式呼应科学/编辑类 UI。

---

## 布局与构图

### 页面外框

```css
.frame {
  position: relative; z-index: 1;
  max-width: 1400px; margin: 0 auto;
  padding: 48px 56px 64px;
}
```

### 标准三栏舞台

大多数模板的图表区域使用此布局：

```css
.stage {
  display: grid;
  grid-template-columns: 220px 1fr 280px;
  gap: 32px;
  align-items: start;
}
```

- **左 (220px)：** 图例、控件、过滤器
- **中 (1fr)：** 图表本体
- **右 (280px)：** 详情面板（联动视图）

### 头部区

放在 `.stage` 之上：

```html
<header class="title">
  <div>
    <div class="eyebrow"><span class="dot"></span> 可视化习语 · [图类型] · [上下文]</div>
    <h1>[主题] 的 <em>[关键词]</em><br>[从句]。</h1>
    <p class="lede">[1-2 句描述，结尾给一个交互提示]</p>
  </div>
  <div class="meta">
    <b>[项目/课程]</b> &nbsp; / &nbsp; [学科] <br>
    Dataset · [来源 / 年份] <br>
    Idiom · <b>[图名]</b> &nbsp; / &nbsp; Marks · [主要标记]
  </div>
</header>
```

### 构图原则（含格式塔依据）

1. **非对称头部**（grid 1fr auto）创造视觉张力；对称布局显得模板化。
2. **图表周围充裕的负空间**将图表作为"图形"从"背景"中分离——利用图地原则。
3. **垂直节奏**通过一致的 14/18/24/32px 间距单位形成；邻近性分组相关控件。
4. **细线边框**（`1px solid var(--line)`）替代重盒子，分组而不喧宾夺主。

### 响应式折叠

`< 1100px` 时：
```css
.stage { grid-template-columns: 1fr; }
.frame { padding: 32px 24px; }
header.title { grid-template-columns: 1fr; gap: 20px; }
.meta { text-align: left; }
```

---

## 交互模式

所有模板支持以下五种交互原语。按图类型选择适用的。

### 1. 悬停 → 高亮 + 其他变暗（弹出效应）

```javascript
function mouseEnter(event, d){
  const ancestors = new Set(d.ancestors ? d.ancestors() : [d]);
  marks.classed("dim", n => !ancestors.has(n))
       .filter(n => n === d).classed("glow", true);
  tip.classed("on", true);
  updateDetail(d);
}
```

**感知依据：** 通过明度对比的选择性注意。变暗元素降至 18% 透明度——既保留上下文，又低到让被高亮元素在 <250ms（预注意阈值）内弹出。

### 2. Tooltip（按需细节）

固定定位，跟随光标，偏移 `+18px, +18px`。包含：
- 元素名（Fraunces，较大）
- 路径/面包屑（mono，dim）
- 1-3 项数值（mono，tabular）
- 可选色带

背景虚化，半透明，细线边框。淡入 150ms。

### 3. 点击 → 缩放 / 下钻

适用于层级或可缩放习语（Sunburst、Treemap、Force、Choropleth）。过渡用 820ms cubic-in-out——慢到能保持对象恒常性（追踪移动元素），快到不令人不耐烦。

### 4. 联动详情面板

右栏在悬停或点击时更新。展示：
- 选区名称 + 面包屑
- 3 行统计：值 / 占父级比例 / 占总体比例（或类似）
- 进度条
- 子组件列表（按值排序的条）

这补偿了视觉习语无法精确读数的问题（所有人——人眼对角度和面积比较都很差）。

### 5. 图例过滤（联动高亮）

左栏图例条响应悬停（高亮该类别的图表元素）和点击（下钻或过滤）。呼应图表的颜色编码。

---

## 动效

### 时间常量

```javascript
const T = {
  enter:    700,   // 初始挂载错峰
  hover:    250,   // dim/glow 过渡
  zoom:     820,   // 主要视图变化
  tooltip:  150,   // 淡入
  number:   820,   // 数值插值
};
```

### 标准缓动

- **`d3.easeCubicOut`** 用于入场（快起，缓收）
- **`d3.easeCubicInOut`** 用于缩放过渡（对称，显得审慎）
- **`d3.easeQuadOut`** 用于微交互（低调）

### 入场错峰

总是让标记以逐元素延迟方式入场：

```javascript
marks.attr("opacity", 0)
  .transition()
  .delay((d,i) => 30 + i * 12)
  .duration(700)
  .ease(d3.easeCubicOut)
  .attr("opacity", 1);
```

**感知依据：** 共同命运（格式塔）——同步扫入告诉观察者"这些元素属于一组"。同时也引导注意力沿数据方向（径向外、左到右等）。

### 数值插值

当交互导致数值变化时，**永远插值，绝不跳变**：

```javascript
selection.transition().duration(820)
  .tween("text", function(){
    const i = d3.interpolateNumber(oldVal, newVal);
    return function(t){ this.textContent = i(t).toFixed(2); };
  });
```

---

## 背景氛围

纯色背景显得平板。每个模板都叠加两层微妙氛围：

```css
/* 第 1 层：径向光斑，增加温度，打破平整感 */
body::before {
  content:""; position:fixed; inset:0; pointer-events:none; z-index:0;
  background:
    radial-gradient(800px 600px at 18% 12%, rgba(240,198,116,.06), transparent 60%),
    radial-gradient(900px 700px at 85% 88%, rgba(227,106,74,.05), transparent 60%);
}

/* 第 2 层：分形噪点叠加，增加质感，防止色带 */
body::after {
  content:""; position:fixed; inset:0; pointer-events:none; z-index:0; opacity:.35;
  background-image: url("data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' width='160' height='160'><filter id='n'><feTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2' stitchTiles='stitch'/><feColorMatrix values='0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .04 0'/></filter><rect width='100%' height='100%' filter='url(%23n)'/></svg>");
  mix-blend-mode: overlay;
}
```

**感知依据：** 图地分离。轻微纹理的低对比度背景比平面背景更可靠地后退——图表元素作为"图形"获得突出地位。

---

## 无障碍核查清单

宣告模板完成之前请走一遍。

### 色觉障碍
- [ ] 所有分类色在灰度下可区分（用 `filter: grayscale(100%)` 测试图表）
- [ ] 没有信息仅靠红绿表达
- [ ] 颜色始终搭配至少一个其他通道（标签、位置、形状）

### 对比度（WCAG AA）
- [ ] 正文 ≥ 4.5:1
- [ ] 大标题 ≥ 3:1
- [ ] 图表标记对背景 ≥ 3:1
- [ ] tooltip 文本 ≥ 4.5:1

### 预注意特征
- [ ] 悬停状态变化在 <250ms 内可察觉（用透明度或明度，不要用细微色相变化）
- [ ] 选中/聚焦元素毫无疑问是屏幕最亮/最饱和的
- [ ] 强调色用量稀疏，使其使用时能真正弹出

### 动效
- [ ] 所有过渡 ≤ 900ms
- [ ] 入场动画不阻塞首次交互（动画期间仍可点）
- [ ] 没有无限循环动画可能引起晕动症

### 格式塔原则
- [ ] **邻近性：** 相关控件在视觉上成组
- [ ] **相似性：** 同类元素至少共享一个视觉属性（颜色或形状）
- [ ] **共同区域：** 面板有清晰的边界
- [ ] **连续性：** 阅读顺序由布局方向强化（上→下，左→右，或径向外扩）
- [ ] **图地：** 图表与背景明显分离

### 认知负荷
- [ ] 分类色不超过 7-8 个
- [ ] 字体家族不超过 3 个
- [ ] tooltip 显示 ≤ 3 个数值
- [ ] 详情面板 ≤ 1 屏（主要信息无需滚动）
