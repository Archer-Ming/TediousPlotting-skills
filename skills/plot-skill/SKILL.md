---
name: Plot Skill
description: A professional scientific plotting skill that includes various common chart visualizations such as scatter plots, bar charts, line charts, box plots, violin plots, histograms, density curves, heatmaps, pie charts, radar charts, 3D surface plots, field plots, joy plots, ROC curves, confusion matrices, error/uncertainty plots, and flow/relationship diagrams. Use this skill when the user provides data and wants to perform analysis, variation, distribution, comparison, or trend visualization, and needs you to create high-quality charts. This skill strictly follows fixed scientific color schemes and font specifications, and performs self-checks before output, producing visualization charts that meet journal submission quality standards.
---
### Important Rules!

* All plotting style techniques are in the reference template code. Please strictly follow the plotting prerequisite settings as well as the template's plotting style, and create scientific-grade charts according to different user requirements.
* For names in the data provided by the user, make corrections according to the specific situation. For example: Chinese should correspond to fonts like SimHei, ensuring that the generated chart has no garbled characters and that the visualization position is correct; if the data names are in English, use Times New Roman.
* If the visualized chart does not meet expectations, please self-check and redraw until expectations are met.
* The template code provided is only for your reference and imitation; please ignore the sample data within. What you should do is learn the plotting logic, plotting style, and feature highlights of the templates. Then create similar or identical template visualizations based on the data and requirements provided by the user.
* In the reference templates, each type is divided into a first part and other parts. The first part contains 4 chart templates ranging from simple to complex, and the other parts are complex chart templates with multiple types and multi-layer composites. After you have learned all of them, you must selectively draw based on user needs—either use one of the subplots/layers, or use all of them. Consider each case specifically!!
* The four sub-charts provided in the first part are for you to learn charts of different complexity levels of one type. In actual user requirements, you should select one to draw based on user needs.
* For visualization needs mentioned by the user that are not in the templates, you should follow the plotting style skills you learned from these templates and independently create visualizations suitable for user needs through imitation.
* Sometimes, you don't need to completely copy the template. Under the strict premise of following the format requirements, you can appropriately diverge your plotting logic on the basis of the template, ensuring that you are not rigidly fixed by the template charts I provide.

### When to Use This Skill

✅ The user provides data (tables, CSV, Excel, manually provided data in conversation) and requests plotting/visualization.
✅ The user requests display of distribution / trend / comparison / correlation / classification performance.
✅ The user wants charts of "journal-grade", "paper-grade" quality, or for use in modeling competitions or experiments.

❌ Schematic diagrams without data (architecture diagrams, flowcharts, mind maps).
❌ Interactive dashboards.
❌ Pure data cleaning, regression modeling, or statistical computation without visualization output.

### Prerequisites

⚠️ When the user does not explicitly state the chart type, briefly confirm before drawing.

**First ensure that the plotting configuration meets scientific-grade standards, including at least the following:**

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

| Chart Type                                                                          | Figure Size                                        |
| ----------------------------------------------------------------------------------- | -------------------------------------------------- |
| Line charts, bar charts, box plots, violin plots and other horizontal single charts | `(12, 8)` or `(10, 6)`                         |
| Pie charts, heatmaps, 3D surface plots and other square charts                      | `(8, 8)` to `(16, 16)`                         |
| Multi-subplot charts                                                                | Based on subplot count `(12, 5)` to `(22, 15)` |

**Common scientific visualization colors are listed below. Select from the following based on actual situation; do not arbitrarily use other colors:**

**Categorical colors:**

```
colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D',"#649fca", "#c68f5f", "#63bd63", "#D05E5E", "#8F51C8"]
```

**Sequential colors (heatmap, density, magnitude):**
`'viridis'`, `'cividis'`, `'magma'`, `'YlGnBu'`, `'Blues'`  Prefer `viridis`/`cividis` (perceptually uniform, colorblind-friendly)

**Diverging colors (correlation, signed differences, residuals near zero):**
`'RdBu_r'`, `'coolwarm'`, `'PuOr_r'`. Be sure to center the color scale at a meaningful midpoint, using `vmin=-v, vmax=v` or `TwoSlopeNorm`

---

### Reference Template Python

|                              Reference File                              | Chart Type                                                                                                                   | When to Open                                                                                                                                                  |
| :----------------------------------------------------------------------: | ---------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
|       [references/scatter_bar_line_box.md](reference\bar_line_box.md)       | Scatter plots, bar charts, line charts, box plots and their variants and composite charts                                    | When user needs involve time/category trends, inter-group comparison, distribution, scatter correlation                                                       |
| [references/heat_pie_histogram_radart.md](reference\scatter_violin_heat.md) | Pie charts, histograms, KDE density curves, radar charts, heatmaps and their variants and composite charts                   | When user needs involve matrix/correlation data, univariate distribution, proportion, multi-axis feature comparison                                           |
|  [references/3Dplot_joy_ROC_flow_error.md](reference\3Dsurface_joy_ROC.md)  | 3D surfaces, 2D field plots, joy plots, confusion matrices, ROC curves ,Time series and their variants and composite charts | When user needs involve 3D structure, vector/scalar fields, stacked distributions, classifier evaluation, time analyse, uncertainty bands, model diagnostics |

If the requirements span multiple files, you can open them all.

### Input Format

The user will provide data in various forms (possibly direct text input, Excel-type data, chart-type data?), titles (x/y titles, main title, text boxes?), and other chart setting requirements, but at minimum will include:

* Data
* Requirement description

For example:

`Help me draw a bar chart with the data shown in the table below, where the x-axis is feature type, the y-axis is the sample count from the table, the main title is "Sample Count Statistics for Each Feature Type", and add a legend.`

If the user's data is irregular (missing values, mixed types, numeric strings with embedded units), clean it first and inform the user about the processing.

### Output Format

Your output is a chart in .png/.svg format that meets the user's requirements.

### Self-check Before Output!!

Each time you finish drawing a chart, run through this list before saving:

- [ ] **No garbled fonts**: If Chinese labels appear in the data, ensure SimHei font is prioritized. If physical unit symbols cannot display in the chart, remove the units to ensure no garbled characters appear in the chart!
- [ ] **No overlapping labels**: Are x-axis main labels vs. secondary labels, bar-top values vs. legend boundary, and tick label rotation angles appropriate?
- [ ] **Color scale fits the data**: Do the heatmap's vmin/vmax cover the actual data range without being too wide?
- [ ] **Sufficient y-axis margin**: Is there ≥15% space reserved above the bar-top value labels? (`ax.set_ylim(0, ymax * 1.18)`).
- [ ] **Legend does not obscure data**: Choose the right position with `loc`; if necessary, use `bbox_to_anchor` to place it outside, and do not cause occlusion.
- [ ] **Reasonable numerical precision**: Use `{int(h)}` for integer counts, `.2f` for percentages, `.3e` for scientific quantities.
- [ ] **Colors taken from the palette**: Do not use matplotlib defaults, do not pick colors arbitrarily.
- [ ] **Figure size matches subplot count**: The more subplots, the larger the figsize.
- [ ] **Main title**: If the user does not request one, **do not add** (many users embed the chart in a paper that already has a caption).
- [ ] User data fit: Does the type of chart drawn fit the data? Can it effectively present the data?

If the check does not pass, **debug and redraw it yourself**; do not give a flawed chart to the user!

---

### Quick Execution Process

1. Read user data and requirements; if the chart type is unclear, ask one short clarifying question.
2. Open the corresponding template file and review the style.
3. Pick **one** template panel of appropriate complexity (don't draw them all).
4. Write the plotting code using the prerequisite rcParams + palette + the user's actual data.
5. Run the self-check list; redraw if any item fails.
