# TediousPlotting-Skills

---

## 更多绘图Skills持续蒸馏中...

AI绘制的图老达不到理想？
国外大模型太费token？
需求与出图相违背？

试试这些skills！将高质量期刊级别图表，流程架构图，亦或是交互式图表以及高性能AI的绘图逻辑联合蒸馏成的一份可在本地agent/claw进行绘制的技能。

***它可以用在你的期刊论文，竞赛，PPT等！甚至是企业公司，金融分析的可视化展示！***

---

 Want to test it easily? Try the **miniAgent** mentioned above – just clone it locally and connect your API, it supports domestic models like DeepSeek. More templates are continuously being improved, and I’d be very happy if you could provide suggestions for this skill!

## **快速体验**

### **Claude Code**

```
git clone https://github.com/Archer-Ming/TediousPlotting-skills.git
```

**将skills文件夹里你想要的skill添加到 *claude code*  里即可使用**

### **miniAgent(Personal Test)**

或者使用我们开发的网页 ***miniAgent*（它有点简陋但足以支撑skills测试和体验！持续开发改进中(0v0) ）**，为此你只需要接入大模型密钥即可体验！它支持*deepseek*和*OpenAI*

*具体说明参考见：*         [miniAgent介绍](./miniAgent/README.md)

*miniAgent 网页：*              [miniAgent网页](./miniAgent/miniAgent.html)

## **关于Skills的手册**

| Skill                            | 类型                 | 说明                                                       | 状态 |
| -------------------------------- | -------------------- | ---------------------------------------------------------- | ---- |
| [plot-skill](./skills/plot-skill)   | 覆盖各类型的常见图表 | 用于数据统计分析，趋势，分布，对比，相关性，误差范围       | 完善 |
| [frame-skill](./skills/frame-skill) | 期刊论文架构图       | 用于流程原理布局，模块架构，思维步骤决策                   | 测试 |
| [d3interact-skill](./skills/d3interact-skill)                                 | 可视化交互分析图表   | 用于"交互式可视化"、"可探索图表"、"下钻分析"、"可筛选图表" | 测试 |

---

## Plot-skill

### **特色**

    规范了期刊的图表参数设置,配色,风格；并提供了高质量从简单到多图层复合图表模板供大模型学习。

    规范了输入输出格式以及自检项，大幅度降低了Agent绘图时消耗无关紧要的token，确保了输出所需的高质量配图。

### **骨架**

```
plot-skill/        针对SCI论文，竞赛，PPT的高质量配图 --> PNG
├── references/ 
|   ├── 3Dplot_joy_ROC_flow_error.md    3D曲面，误差棒，joy图...
│   ├── heat_pie_histogram_radar.md	    热力图，饼图，雷达图...		 
│   ├── scatter_bar_line_box.md         散点图，柱状图，折线图，箱线图...
|
|   
├── SKILL.md   规则限制

```

<table>
  <tr>
    <td><img src="example\f1.png" width="800"></td>
  </tr>
  <tr>
    <td><img src="example\f2.png" width="800"></td>
  </tr>
  <tr>
    <td><img src="example\f3.png" width="800"></td>
  </tr>
  <tr>
    <td><img src="example\f4.png" width="800"></td>
  </tr>
  <tr>
    <td><img src="example\f5.png" width="800"></td>
  </tr>
  <tr>
    <td><img src="example\f6.png" width="800"></td>
  </tr>
  <tr>
    <td><img src="example\f7.png" width="800"></td>
  </tr>
  <tr>
    <td><img src="example\f8.png" width="800"></td>
  </tr>
  <tr>
    <td><img src="example\f9.png" width="800"></td>
  </tr>
  <tr>
    <td><img src="example\f10.png" width="800"></td>
  </tr>
  <tr>
    <td><img src="example\f11.png" width="800"></td>
  </tr>  
</table>

## Frame-skill

### 特色

   严格规范了期刊级别架构图的线框配色组合，整体布局平衡感，字体等设置。

  针对不同的用途（IEEE，Nature，SCI）提供了六种布局和五种高审美配色，供大模型学习捕捉风格，布局。

| 风格     | 系列色                           | 领域           |
| -------- | -------------------------------- | -------------- |
| 学术柔和 | 蓝色 薄荷 杏色 粉色 薰衣草 灰色  | ML/DL/计算机   |
| 自然科学 | 蓝色 绿色 琥珀色 玫瑰 石板       | 物理学/数学    |
| 机械工程 | 钢青色 蓝绿色 橙色 深红色 石墨色 | 材料/机械/工程 |
| 温暖生物 | 赤陶 鼠尾草色 沙色 石色          | 生物/化学/医学 |
| 简约对比 | 灰色 强调色                      | 0V0            |

### 骨架

```
frame-skill/                               针对SCI论文，竞赛的高质量架构图,流程图等 --> PNG SVG PPTX
├── references/
|   ├── styles.md                          六种布局架构类型
|   ├── style_01_layered_network.svg       with more frame... 细磨
|
├── palettes.md                            五种风格配色
├── render_helpers.py                         SVG转PPTX，PNG脚本
|
├── assets/ 
|   ├── reference1.png                     with more frame... 粗磨
|   
|   
├── SKILL.md    规则限制
```

<table>
  <tr>
    <td><img src="skills\frame-skill\assets\reference4.png" width="800"></td>
    <td><img src="skills\frame-skill\assets\reference5.png" width="800"></td>
  </tr>
</table>

## D3interact-skill

### 特色

### 骨架

```
d3interact-skill/
├── references/
|   ├──selection-guide.md            ← 决策树：何时用哪种习语
|   ├──design-system.md              ← 配色、字体、布局、动效、无障碍
|   
|   
├── SKILL.md    规则限制 
|   
|
├──assets/
|   ├──sunburst/  
|   ├──treemap/  
|   ├──sankey/           template.html  notes.md  sample-data.json
    ...
```

<table>
  <tr>
    <td><img src="example\i1.png" width="800"></td>
    <td><img src="example\i2.png" width="800"></td>
  </tr>
  <tr>
    <td><img src="example\i3.png" width="800"></td>
    <td><img src="example\i4.png" width="800"></td>
  </tr>
</table>
