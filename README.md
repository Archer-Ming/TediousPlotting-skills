# TediousPlotting-Skills

---

## 更多绘图Skills持续蒸馏中...

AI绘制的图老达不到理想？
国外大模型太费token？
需求与出图相违背？

试试这些skills！将高质量期刊级别图表，流程架构图以及高性能AI的绘图逻辑联合蒸馏成的一份可在本地agent/claw进行绘制的技能。

***它可以用在你的期刊论文，竞赛，PPT等！***

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

*具体说明参考见：*         [miniAgent\README.md](miniAgent\README.md)

*miniAgent 网页:*            [miniAgent\miniAgent.html](miniAgent\miniAgent.html)

## **关于Skills的手册**

| Skill                                                      | 类型                 | 说明                                                 | 状态 |
| ---------------------------------------------------------- | -------------------- | ---------------------------------------------------- | ---- |
| [TediousPlotting-skills/skills/Plot-skill](TediousPlotting-skills/skills/Plot-skill) | 覆盖各类型的常见图表 | 用于数据统计分析，趋势，分布，对比，相关性，误差范围 | 完善 |
| [TediousPlotting-skills/skills/Flow-skill](skills/DL-skill)   | 流程图，架构图       | 用于流程布局，模块架构，步骤决策                     | 草稿 |

---

## Plot-skill

### **特色**

    规范了期刊的**图表参数设置,配色,风格**；并提供了高质量从简单到多图层复合图表模板供大模型学习。

    规范了输入输出格式以及自检项，大幅度降低了Agent绘图时消耗无关紧要的token，确保了输出所需的高质量配图。

### **骨架**

```
plot-skill/        针对SCI论文，竞赛，PPT的高质量配图 --> PNG
|   ├── references/ 
|   |   ├── 3Dplot_joy_ROC_flow_error.md    3D曲面，误差棒，joy图...
│   |   ├── heat_pie_histogram_radar.md	    热力图，饼图，雷达图...		 
│   |   ├── scatter_bar_line_box.md         散点图，柱状图，折线图，箱线图...
|   |
|   ├── SKILL.md   规则限制

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
