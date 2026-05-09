---
name: Professional Plotting Skill
description: A professional scientific plotting skill that includes various common chart visualizations such as box plots, bar charts, scatter plots, and more. Use this skill when the user provides data and needs you to create high-quality charts involving data trend analysis, variations, distributions, etc. This skill strictly follows fixed scientific color schemes and font specifications, producing visualization charts that meet journal submission quality standards.
---
---

### Important Rules!

* The plotting style techniques are all in the reference template code. Please strictly follow the plotting prerequisite settings and the template's plotting style, and create research-grade charts according to different user requirements.
* For names in the data provided by the user, make corrections according to specific situations. For example: Chinese should correspond to fonts like SimHei to ensure the generated chart has no garbled text and visualization positions are correct; if the data names are in English, use Times New Roman.
* If the visualized chart does not meet expectations, please self-check and re-draw until expectations are met.
* The template code provided is only a reference for you to imitate. Please ignore the sample data inside. What you need to do is learn the plotting logic, plotting style, and feature highlights of the templates. Then create similar or identical template visualization charts based on the data and requirements provided by the user.
* Each type in the reference templates is divided into Part One and other parts. Part One contains 4 chart templates ranging from simple to complex, while the other parts contain complex chart templates with multiple types and multi-layer composites. After fully learning all of them, you must selectively draw according to user requirements—whether to use one of the subplots, a layer, or use all of them? Consider the specific situation!!
* The four subplots provided in Part One are for you to learn charts of one type at different complexity levels. In actual user requirements, you should select one for drawing based on the user's needs.
* For visualization needs mentioned by the user that are not in the templates, you should follow the plotting style techniques learned from these templates, imitate and independently draw visualization charts suitable for user needs.
* Sometimes, you don't have to completely copy the template. While strictly adhering to the prerequisite format requirements, you can appropriately diverge your plotting logic based on the template, ensuring you are not constrained by the template charts I provided.

### Prerequisites

⚠️ When users don't explicitly specify the chart type, briefly confirm before drawing.

**First ensure plotting configuration meets research-grade standards, including at least the following:**

```
import matplotlib.pyplot as plt

# Font: If the user-provided data contains Chinese, prioritize 'SimHei'. If not, prioritize 'Times New Roman'.
# plt.rcParams['font.family'] = 'serif'
# plt.rcParams['font.serif'] = ['SimHei','Times New Roman', 'Liberation Serif', # 'DejaVu Serif']

# Journal-grade chart configuration:
plt.rcParams.update({
    'font.size': 14,
    'axes.labelsize': 18,
    'axes.titlesize': 16,
    'xtick.labelsize': 16,
    'ytick.labelsize': 16,
    'legend.fontsize': 12,
    'figure.dpi': 500,
    'axes.linewidth':1.2,
    'xtick.major.width': 1.2,
    'ytick.major.width': 1.2,
    'xtick.major.size': 6,
    'ytick.major.size': 6,
    'xtick.minor.size': 3,
    'ytick.minor.size': 3,
    'axes.spines.top': True,
    'axes.spines.right': True,
    'axes.unicode_minus': False
})
```

**Figure size**

| Chart Type                                                                          | Chart Size         |
| ----------------------------------------------------------------------------------- | ------------------ |
| Line charts, bar charts, box plots, violin plots and other horizontal single charts | (12, 8) or (10, 6) |
| Pie charts, heatmaps, 3D surface plots and other square charts                      | (8-16, 8-16)       |
| Charts containing multiple subplots                                                 | (12-22, 5-15)      |

**Common scientific visualization chart colors are as follows. Select from the list below according to actual situations. Do not use random colors of your own:**

```
colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D',"#649fca", "#c68f5f", "#63bd63", "#D05E5E", "#8F51C8"]
```

---

### Reference Template Python

|                           Reference File                           | When to Open                                                                                                                                                       |
| :----------------------------------------------------------------: | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
|        [references\bar_line_box.md](reference\bar_line_box.md)        | When user requirements involve trend changes, bar charts, line charts, box plots, and their variants and composite charts                                          |
| [references\scatter_violin_heat.md](reference\scatter_violin_heat.md) | When user requirements involve sample distribution. Scatter plots, violin plots, KDE kernel density curve plots, heatmaps, and their variants and composite charts |
|   [references\3Dsurface_joy_ROC.md](reference\3Dsurface_joy_ROC.md)   | When user requirements involve error analysis, 3D surfaces, 2D field plots, joy plots, confusion matrices, ROC curves, and their variants and composite charts     |

### Input Format

Users will provide data in various forms (possibly direct text input, Excel table type data, chart type data?), titles (xy titles, main title, text boxes?), and other chart setting requirements, but at minimum will include:

* Data
* Requirement description

For example:

`Help me draw a bar chart with data as follows in the table, where the x-axis is the feature type, the y-axis is the sample count from the table, the main title is "Sample Count Statistics for Various Feature Types", and add a legend.`

### Output Format

Your output is to present a chart in .png/.svg format that meets the user's requirements.

### Self-check Before Output!!

After each drawing, before saving, go through this checklist:

- [ ] **No font garbled text**: When data contains Chinese labels, please ensure SimHei font is prioritized. If physical unit symbols cannot be displayed in the chart, remove the units to ensure the chart has no garbled text!
- [ ] **No label overlap**: x-axis main labels vs sub-labels, bar-top values vs legend boundaries, are tick label rotation angles appropriate?
- [ ] **Color scale fits data**: Does the heatmap's vmin/vmax cover the actual data range without being too wide?
- [ ] **Sufficient y-axis whitespace**: Is there ≥15% space reserved above the bar-top value labels? (`ax.set_ylim(0, ymax * 1.18)`)
- [ ] **Legend doesn't obscure data**: Is `loc` set to the right position? Use `bbox_to_anchor` to place externally if necessary, don't cause obstruction.
- [ ] **Reasonable numerical precision**: Use `{int(h)}` for integer counts, `.2f` for percentages, `.3e` for scientific quantities
- [ ] **Colors taken from the palette**: Did not use matplotlib defaults or randomly picked colors
- [ ] **Figure size matches subplot count**: The more subplots, the larger the figsize
- [ ] **Main title**: **Don't add** if user doesn't request it (many users embed charts in papers that already have captions)
- [ ] User data adaptability: Does the type of chart drawn fit the data? Can it effectively present the data?

If the check fails, **debug and redraw yourself**, don't give the user a flawed chart!
