---
name: Professional Plotting Skill
description: A professional scientific plotting skill that includes various common chart visualizations such as scatter plots, bar charts, line charts, box plots, violin plots, histograms, density curves, heatmaps, pie charts, radar charts, 3D surface plots, field plots, joy plots, ROC curves, confusion matrices, error/uncertainty plots, flow relationship diagrams, and more. Use this skill when users provide data and want analysis, variation, distribution, comparison, or trend visualizations, requiring you to create high-quality charts. This skill strictly follows fixed scientific color schemes and font specifications, producing visualization charts that meet journal submission quality standards.
---
### Important Rules!

* All plotting style techniques are in the reference template code. Please strictly follow the plotting prerequisite settings and the template's plotting style, drawing scientific-grade charts according to different user needs.
* For names in user-provided data, make corrections according to the specific situation. For example: Chinese should correspond to SimHei, etc., to ensure the generated charts do not have garbled characters and visualization positions are correct; if data names are in English, use Times New Roman.
* If the visualized chart does not meet expectations, please self-check and redraw until expectations are met.
* The template code provided is only for your imitation reference. Please ignore the sample data inside. What you need to do is learn the template's plotting logic, plotting style, and feature highlights. Then, draw similar or identical template visualization charts based on user-provided data and requirements.
* In the reference templates, each type is divided into Part One and other parts. Part One contains 4 chart templates from simple to complex, and the other parts are complex chart templates with multiple types and multi-layer composites. After learning all of them, you must selectively draw according to user needs—whether to use one of the subplots, layers, or all of them. Consider the specific situation carefully!!
* The four sub-charts provided in Part One are for you to learn charts of different complexity levels of one type. In actual user needs, you should select one to draw based on user requirements.
* For visualization needs mentioned by users that are not in the templates, you should follow the plotting style skills you learned from these templates, and imitate and independently draw visualization charts suitable for user needs.
* Sometimes, you don't have to completely copy the templates. Under the strict premise of following the prerequisite format requirements, you can appropriately diverge your plotting logic based on the templates, ensuring you are not constrained by the template charts I provided.

### When to Use This Skill

✅ User provides data (tables, CSV, Excel, manually provided data in conversation) and requests plotting/visualization.
✅ User requests display of distribution / trend / comparison / correlation / classification performance.
✅ User wants "journal-grade", "paper-grade" charts, or charts for modeling competitions or experiments.

❌ Schematic diagrams without data (architecture diagrams, flowcharts, mind maps).
❌ Interactive dashboards.
❌ Pure data cleaning, regression modeling, statistical computation without visualization output.

### Prerequisites

⚠️ When the user doesn't explicitly state the chart type, briefly confirm before drawing.

**First ensure plotting configuration is at scientific-grade level, including at least the following:**

```
import matplotlib.pyplot as plt

#---Font---
data_has_chinese = False  # If any data/labels/titles/ticks contain Chinese characters, change to True

if data_has_chinese:
    plt.rcParams['font.family'] = ['SimHei', 'Microsoft YaHei', 'Noto Sans CJK SC', 'sans-serif']
else:
    plt.rcParams['font.family'] = ['Times New Roman', 'Liberation Serif', 'DejaVu Serif', 'serif']

# Journal-grade figure configuration:
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

| Chart Type                                                                          | Figure Size                                       |
| ----------------------------------------------------------------------------------- | ------------------------------------------------- |
| Line charts, bar charts, box plots, violin plots and other horizontal single charts | `(12, 8)` or `(10, 6)`                        |
| Pie charts, heatmaps, 3D surface plots and other square charts                      | `(8, 8)` to `(16, 16)`                        |
| Charts with multiple subplots                                                       | By number of subplots `(12, 5)` to `(22, 15)` |

**Common scientific visualization colors are as follows. Select from the list below according to the actual situation. Do not use random colors yourself:**

**Categorical colors:**

```
colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D',"#649fca", "#c68f5f", "#63bd63", "#D05E5E", "#8F51C8"]
```

**Sequential colors (heatmaps, density, magnitude):**
`'viridis'`, `'cividis'`, `'magma'`, `'YlGnBu'`, `'Blues'`  Prefer `viridis`/`cividis` (perceptually uniform, colorblind-friendly)

---

### Reference Template Python

|                              Reference File                              | Chart Type                                                                                                  | When to Open                                                                                                                                    |
| :----------------------------------------------------------------------: | ----------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------- |
|       [references/scatter_bar_line_box.md](reference\bar_line_box.md)       | Scatter plots, bar charts, line charts, box plots and variants and composite charts                         | When user needs involve time/category trends, group comparisons, distributions, scatter correlations                                            |
| [references/heat_pie_histogram_radart.md](reference\scatter_violin_heat.md) | Pie charts, histograms, KDE kernel density curves, radar charts, heatmaps and variants and composite charts | When user needs involve matrix/correlation data, univariate distributions, proportions, multi-axis feature comparisons                          |
|  [references/3Dplot_joy_ROC_flow_error.md](reference\3Dsurface_joy_ROC.md)  | 3D surfaces, 2D field plots, joy plots, confusion matrices, ROC curves and variants and composite charts    | When user needs involve 3D structures, vector/scalar fields, stacked distributions, classifier evaluation, uncertainty bands, model diagnostics |

If the requirements span multiple files, you can open them all.

### Input Format

Users will provide data in various forms (possibly direct text input, Excel table data, chart-type data?), titles (xy titles, main title, text boxes?), and other chart setting requirements to you, but at minimum it includes:

* Data
* Requirement description

For example:

`Help me draw a bar chart with the following data table, where the x-axis is the feature type, the y-axis is the sample count from the table, the main title is "Sample Count Statistics for Each Feature Type", and add a legend.`

### Output Format

Your output is a chart in .png/.svg format that meets the user's requirements.

### Self-Check Before Output!!

After each drawing, before saving, go through:

- [ ] **No font garbled characters**: When Chinese labels appear in data, please ensure SimHei font is prioritized. If physical unit symbols cannot be displayed in the chart, remove the units to ensure the chart does not have garbled characters!
- [ ] **Labels do not overlap**: x-axis primary labels vs. secondary labels, bar-top values vs. legend boundaries, are tick label rotation angles appropriate?
- [ ] **Color scale fits data**: Do heatmap vmin/vmax cover the actual data range without being too wide?
- [ ] **Sufficient y-axis whitespace**: Is there ≥15% space reserved above bar-top value labels? (`ax.set_ylim(0, ymax * 1.18)`)
- [ ] **Legend does not block data**: Choose the right `loc` position, use `bbox_to_anchor` for external placement when necessary, do not cause blockage.
- [ ] **Reasonable numerical precision**: Use `{int(h)}` for integer counts, `.2f` for percentages, `.3e` for scientific quantities
- [ ] **Colors taken from palette**: Did not use matplotlib default colors or randomly picked colors
- [ ] **Figure size matches subplot count**: The more subplots, the larger the figsize
- [ ] **Main title**: **Don't add** if the user doesn't request it (many users embed the figure into a paper that already has a caption)
- [ ] User data adaptability: Does the chart type drawn fit the data? Can it effectively present the data?

If the check fails, **debug and redraw yourself**, don't give a flawed chart to the user!

---

### Quick Execution Process

1. Read user data and requirements; when the chart type is unclear, ask a brief clarification question.
2. Open the corresponding template file and review the style.
3. Pick **one** template panel of appropriate complexity (don't draw all of them).
4. Write plotting code with the prerequisite rcParams + color palette + user's actual data.
5. Run the self-check list; redraw if any item fails.
