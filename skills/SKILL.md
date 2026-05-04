---
name: 专业绘图技能
description:专业的科研绘图技能，包含箱线图，柱状图等各种常见的图形可视化绘制。用户通过提供数据，坐标标题，大标题等需求，你来完成准确的绘图并呈现给用户，本技能严格遵循固定的科研配色与字体规范,产出符合期刊投稿质量的可视化图表。
---
---

### 重要规则！

* 绘图严格按照以下模板代码来进行绘制，不得凭空捏造，除非用户提及的话语意思为延申扩展之类的，你才能在模板代码基础上适当延申，改进可视化配图的风格和类型。
* 对于用户提供的数据，名称等，按具体情况进行修正，比如：中文就对应SimHei等，确保生成的图不要有乱码，可视化位置正确，图幅大小请根据用于需求设定好。
* 如果可视化的图不符合预期，请自己去找出问题并重新绘制，直到达到预期。
* 模板代码提供的只是给你的模仿参考，里面的x坐标，y坐标数据，亦或是对数据的处理读取，标题名称，各种不同类型数据，请忽略。你要做的是学习模板的绘图逻辑，绘图风格，功能亮点。然后根据用户提供数据和要求绘制相似或者相同的模板可视化配图。
* 有些模板里面是多种类型图的整合，你学习完后必须按照用户需求选择性绘制，抑或是全部使用，具体情况具体考虑。
* 对于用户提及的可视化需求配图并不在模板里面的，你要按照在我这些模板中学习到的绘图风格技能，模仿并自主绘制适合用户需求的可视化配图。

### 前提

⚠️ 用户没明说图表类型时,先简短确认再画。

首先你得先确保绘图配置，确保符合科研级别，包含至少如下：

```
import matplotlib.pyplot as plt

# 字体:如果提供的数据有中文，请设置
plt.rcParams['font.serif'] = ['SimHei']
# 如果没有则Times New Roman 优先,fallback 到开源 serif(Linux 常见环境)
# 含中文标签时在列表前追加 'SimHei' 或 'Noto Sans CJK SC'
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman', 'Liberation Serif', 'DejaVu Serif']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.dpi'] = 400

# 字号与线宽(科研投稿标准)
plt.rcParams['axes.labelsize'] = 12
plt.rcParams['xtick.labelsize'] = 10
plt.rcParams['ytick.labelsize'] = 10
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['axes.linewidth'] = 0.8
plt.rcParams['patch.linewidth'] = 0.5
```

科研常见的可视化配图颜色大致如下，根据实际情况选取，请不要自己乱用配色：

```
colors = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D',"#649fca", "#c68f5f", "#63bd63", "#D05E5E", "#8F51C8"]
```

### 模板

#### 柱状图

```
#柱状图模板1
fig, ax = plt.subplots(figsize=(10, 5))  # 加宽图表尺寸
# 循环绘制每个特征的柱子
for i, (feature, color, offset) in enumerate(zip(features, colors, offsets)):
    y_data = df_normalized[feature].values  # 提取归一化后的F值数据
    # 绘制柱状图
    bars = ax.bar(x + offset, y_data, width=bar_width, color=color, 
                  label=feature, alpha=0.9, edgecolor='black')
    # 柱子顶部添加数值标签
    for bar_idx, bar in enumerate(bars):
        height = bar.get_height()
        # 条件：1. 高度大于0（排除前3个方向的第5根柱子） 2. 不是前3个方向的第5个特征
        if height > 1e-3:  # 过滤极小值（归一化后接近0的数值）
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.005,
                    f'{height:.3f}', ha='center', va='bottom', fontsize=8)
# 设置横坐标标签和位置
ax.set_xticks(x)
ax.set_xticklabels(x_labels, rotation=0)  # 横坐标标签不旋转，保持整洁
# 设置纵坐标标签（标注归一化，加粗突出）
ax.set_ylabel('Normalized F-value', fontweight='bold')
# 设置纵坐标范围（归一化后数据在[0,1]，预留20%空间避免标签遮挡）
ax.set_ylim(0, 1.2)
# 添加图例（位置在图表外部右侧，适配5个特征，避免遮挡柱子）
ax.legend( loc='upper right', bbox_to_anchor=(1, 1), frameon=False)
# 调整布局（防止图例、标签被截断，适配加宽后的图表）
plt.tight_layout(rect=[0, 0, 0.85, 1])
plt.show()

#柱状图模板2
methods = ["pre","gan","smoter","gpr"]
models = list(next(iter(data[direction]["gan"].values())) if False else data[direction]["gan"].keys())

fig, ax = plt.subplots(figsize=(8,5))
width = 0.12
x = np.arange(len(methods))

for i,model in enumerate(models):
    train_vals = []
    test_vals = []
    for m in methods:
        if model in data[direction][m]:
            train_vals.append(data[direction][m][model][0])
            test_vals.append(data[direction][m][model][1])
        else:
            train_vals.append(0)
            test_vals.append(0)
    offset = (i-1)*2*width

    ax.bar(x+offset, train_vals, width,
        color=colors[i],
        edgecolor="black",
        linewidth=0.8,
        label=f"{model} Training Set")
    ax.bar(x+offset+width, test_vals, width,
        color=colors[i],
        edgecolor="black",
        linewidth=0.8,
        hatch=hatch_test,
        label=f"{model} Test Set")

ax.set_xticks(x)
ax.set_xticklabels(["Pre-augmentation","GAN","SMOTER","GPR"])
ax.set_ylabel("R² Score")

#柱状图模板3
color = 'teal'  # 单个组的颜色
bar_width = 0.25  #柱子宽度
x = np.arange(len(labels)) 

fig_x, ax_x = plt.subplots(figsize=(16,8))
bars_x = ax_x.bar(x-bar_width, values1, width=bar_width, color='#1E40AF', edgecolor='white', label='Grid Search R²')
bars_x = ax_x.bar(x+bar_width, values2, width=bar_width, color='#EA580C', edgecolor='white', label='Random Search R²')
bars_x = ax_x.bar(x, values3, width=bar_width, color='#0F766E', edgecolor='white', label='Bayesian Optimization R²')

ax_x.set_xlabel('ML Models', fontsize=12, fontweight='bold', labelpad=10)
ax_x.set_ylabel('Evaluation Metrics', fontsize=12, fontweight='bold', labelpad=10)
ax_x.set_xticks(x)
ax_x.set_xticklabels(labels, fontsize=9, rotation=30, ha='right')
ax_x.set_title('Upright Direction ML Models Comparison')
ax_x.legend(prop={'size':16}, markerscale=1.5, frameon=True)
plt.tight_layout()
plt.show()
```

#### 箱线图+小提琴图

```
plt.figure(figsize=(10, 5))
ax = sns.violinplot(
    data=plot_df,
    x='Direction',
    y='Value',
    order=groups,
    palette=palette,
    inner=None,
    alpha=0.5,
    linewidth=1.2,
)
# 在小提琴图中央叠加箱线图
sns.boxplot(
    data=plot_df,
    x='Direction',
    y='Value',
    order=groups,
    width=0.15,
    boxprops=dict(facecolor='white', edgecolor='black'),
    medianprops=dict(color='red', linewidth=2),
    showfliers=False,
    ax=ax,
    zorder=2,
)

# 静态文本框
plt.text(
    x=0.5,  # 归一化x坐标：距离图左边界5%（0=最左，1=最右）
    y=0.1,  # 归一化y坐标：距离图下边界5%（0=最下，1=最上）
    s=f"           Data Points  \n           Outlier(Removed)  ",  # 你要输入的内容，\n换行
    fontsize=14,  # 文本框内文字大小
    bbox=dict(    # 配置文本框样式（核心，实现「框」的效果）
        boxstyle="round,pad=0.5",  # 框样式：圆角+内边距
        facecolor="white",     # 框背景色
        edgecolor="black",          # 框边框色
        alpha=0.8                  # 框透明度（0=完全透明，1=不透明）
    ),
    transform=plt.gca().transAxes,  # 关键：启用归一化坐标，固定在图窗上
)

# 添加样本散点（半透明，带抖动），放在最上层
sns.stripplot(
    data=plot_df,
    x='Direction',
    y='Value',
    order=groups,
    palette=palette,
    jitter=0.25,
    size=4,
    linewidth=0,
    ax=ax,
    zorder=3,
)

handles = [Patch(facecolor=palette[k], label=k) for k in groups]
ax.legend(handles=handles, title='Build Orientation', loc='upper left', fontsize=14, title_fontsize=14)
ax.set_xlabel('')
ax.set_ylabel('冲击强度')
plt.title('三方向冲击强度分布（小提琴 + 箱线 + 点）')
plt.tight_layout()
plt.show()
```

#### 折线图

```
# ---------------------- 定义绘图函数（生成单个方向的4子图） ----------------------
def plot_all_directions_combined(direction_data, save_path=None):
    """
    在同一张图的 2x2 子图中绘制每个自变量的多方向对比（每个子图包含所有 sheet 的曲线）
    不改变原有 process_data / features 配置逻辑
    """
    fig, axes = plt.subplots(2, 2, figsize=(6, 8), dpi=300)
    axes = axes.flatten()

    # 与原 plot_direction_figure 中相同的 features 配置（保持一致）
    features = [
        {'col': '层厚/ mm', 'title': '(a) Layer height', 'xlabel': 'Layer height (mm)', 'xticks': [0.1, 0.2, 0.3]},
        {'col': 'Printing speed/ mm·s-1', 'title': '(b) Printing speed', 'xlabel': 'Printing speed (mm・s⁻¹)', 'xticks': [30, 75, 120]},
        {'col': ' 热床温度/ °C', 'title': '(c) Bed temperature', 'xlabel': 'Bed temperature (°C)', 'xticks': [70, 80, 90]},
        {'col': '喷嘴挤出温度 /°C', 'title': '(d) Extrusion temperature', 'xlabel': 'Extrusion temperature (°C)', 'xticks': [300, 310, 320]}
    ]
    dir_items = list(direction_data.items())
    dir_names = [k for k, _ in dir_items]
    n_dirs = len(dir_items)

    # 为每个方向分配颜色（循环使用全局 colors）
    from itertools import cycle
    color_cycle = cycle(colors)

    # 主循环：每个子图绘制所有方向曲线
    for i, (feat, ax) in enumerate(zip(features, axes)):
        all_y_means = []
        all_y_stds = []
        all_xs = []
        # 为图例准备
        handles = []
        labels = []
        # 遍历每个方向并绘制其曲线（均值+误差）
        for j, (dir_name, df_dir) in enumerate(dir_items):
            processed_df = process_data(df_dir, feat['col'])
            if processed_df.empty:
                continue
            x = processed_df[feat['col']]
            y_mean = processed_df['mean']
            y_std = processed_df['std']

            col = colors[j % len(colors)]
            # 绘制线与误差棒
            line = ax.errorbar(
                x=x, y=y_mean, yerr=y_std,
                color=col,
                linestyle=line_style,
                marker=['o', 's', '^'][j % 3],  # 不同方向使用不同标记形状
                markersize=marker_size,
                linewidth=2,
                elinewidth=error_bar_width,
                capsize=error_bar_cap,
                capthick=error_bar_width,
                label=dir_name
            )

            handles.append(line)
            labels.append(dir_name)

            all_y_means.append(y_mean)
            all_y_stds.append(y_std)
            all_xs.append(x)

        # 设置横坐标刻度：优先使用配置中的 xticks，否则使用合并的所有 x 值（排序）
        if 'xticks' in feat and feat['xticks'] is not None:
            desired_ticks = np.array(feat['xticks'], dtype=float)
            # 取所有方向的 x 范围交集/并集作为参考
            if all_xs:
                xmin = min([xs.min() for xs in all_xs])
                xmax = max([xs.max() for xs in all_xs])
                valid_ticks = desired_ticks[(desired_ticks >= xmin) & (desired_ticks <= xmax)]
            else:
                valid_ticks = desired_ticks
            if len(valid_ticks) == 0:
                # 退回到合并 x 值位置
                combined_x = np.unique(np.concatenate([np.array(xs) for xs in all_xs]) if all_xs else np.array([]))
                ax.set_xticks(combined_x)
                ax.set_xticklabels([str(v) for v in combined_x], rotation=0)
            else:
                ax.set_xticks(valid_ticks)
                ax.set_xticklabels([str(t) for t in valid_ticks], rotation=0)
        else:
            combined_x = np.unique(np.concatenate([np.array(xs) for xs in all_xs]) if all_xs else np.array([]))
            ax.set_xticks(combined_x)
            ax.set_xticklabels([str(v) for v in combined_x], rotation=0)
        # 子图美化
        ax.set_title(feat['title'], fontsize=12, fontweight='bold', pad=10)
        ax.set_xlabel(feat['xlabel'], fontsize=10)
        ax.set_ylabel('Impact strength (kJ・m⁻²)', fontsize=10)
        ax.tick_params(axis='both', labelsize=8)

        # 合并 y 范围，确保误差棒不会超出
        if all_y_means:
            combined_mean = pd.concat(all_y_means, ignore_index=True)
            combined_std = pd.concat(all_y_stds, ignore_index=True)
            y_min = combined_mean.min() - 2 * (combined_std.max() if not np.isnan(combined_std.max()) else 0)
            y_max = combined_mean.max() + 2 * (combined_std.max() if not np.isnan(combined_std.max()) else 0)
            ax.set_ylim(y_min, y_max)
        # ax.legend( fontsize=12, title='Direction', title_fontsize=10, loc='lower right')

    # 全局标题与布局
    fig.suptitle(f'Impact strength of FDM specimens - combined directions', fontsize=12, fontweight='bold', y=0.98)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()
```

#### 热力图

```
#热力图模板1
# 转换为DataFrame
corr = pd.DataFrame(corr_values, index=features, columns=features)
# 创建下三角掩码
mask = np.triu(np.ones_like(corr, dtype=bool))
# 设置画布
plt.figure(figsize=(10, 8))

# 绘制热力图
sns.heatmap(
    corr,
    mask=mask,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    center=0,
    vmin=-0.15,
    vmax=0.15,
    linewidths=0.5,
    cbar_kws={"shrink": 0.8}
)
plt.title("SHAP Values Correlation Matrix", fontsize=14)
plt.xticks(rotation=45, ha="right")
plt.yticks(rotation=0)
plt.tight_layout()
plt.show()

#热力图模板2
features = df.index.tolist()
n = len(features)
fig, ax = plt.subplots(figsize=(8, 7), dpi=400)

vmin = df.values.min()
vmax = df.values.max()

#  画气泡
for i in range(n):
    for j in range(n):
        if j > i:  # 右上角
            value = df.iloc[i, j]
            ax.scatter(
                j,
                n - 1 - i,
                s=value * 2400,
                c=value,
                cmap="viridis",
                vmin=vmin,
                vmax=vmax,
                alpha=0.9,
                edgecolors='black',   # 黑色边框
                linewidths=1          # 边框宽度
            )
# 左下角写数值 
for i in range(n):
    for j in range(n):
        if j < i:
            value = df.iloc[i, j]
            ax.text(
                j,
                n - 1 - i,
                f"{value:.3f}",
                ha="center",
                va="center",
                fontsize=20
            )

# 坐标轴设置 
ax.set_xticks(range(n))
ax.set_yticks(range(n))

ax.set_xticklabels(features,fontsize=16)
ax.set_yticklabels(features[::-1],fontsize= 16)

ax.set_xlim(-0.5, n - 0.5)
ax.set_ylim(-0.5, n - 0.5)
# ax.set_xlabel("Feature")
# ax.set_ylabel("Feature")
# ax.set_title("SHAP Interaction Plot")

ax.grid(True, linestyle="--", alpha=0.4)
norm = plt.Normalize(vmin, vmax)
sm = plt.cm.ScalarMappable(norm=norm, cmap="viridis")
sm.set_array([])
cbar = fig.colorbar(sm, ax=ax)
cbar.set_label("SHAP Interaction Value")

fig.text(
    -0.03, 0.97,      # 左上角位置
    "(d-2)",
    fontsize=23,
    fontweight="bold",
    va="top"
)
plt.tight_layout()
plt.show()
```

### 输入格式

用户会以各种形式提供数据（可能直接文本输入，excel表格类型数据，图表类型数据？），标题（xy坐标，大标题，文本框？）等需求给你，既结构至少包含如下：

* 数据
* x标题，y标题
* 大标题
* 可能的其他

例如：

`帮我绘制一个柱状图，数据如下表格，其中x坐标为特征类型，y坐标为表格样本数量，大标题为“各类特征的样本数量统计”，添加图例。`

### 输出格式

你的输出是呈现一张符合用户需求的，格式为.png类型的图表。

### 出图前自检

每次画完图,在保存前过一遍:

- [ ] **字体无乱码**:如果数据出现中文标签时请确保使用SimHei字体优先。
- [ ] **标签不重叠**:x 轴主标签 vs 副标签、柱顶数值 vs 图例边界、tick label 旋转角度合适?
- [ ] **色阶适配数据**:热力图的 vmin/vmax 是否覆盖实际数据范围又不过宽?
- [ ] **y 轴留白足够**:柱顶数值标签上方是否预留 ≥15% 空间?(`ax.set_ylim(0, ymax * 1.18)`)
- [ ] **图例不遮挡数据**:`loc` 选对位置,必要时用 `bbox_to_anchor` 外置，不要导致遮挡。
- [ ] **数值精度合理**:整数计数用 `{int(h)}`,百分比 `.2f`,科学量 `.3e`
- [ ] **配色取自调色板**:没有用 matplotlib 默认色或随手挑的颜色
- [ ] **图幅与子图数量匹配**:子图越多 figsize 越大
- [ ] **大标题**:用户没要求就**不加**(很多用户用图嵌入论文已有 caption)

如果检查不通过,**自己 debug 重画**,不要把瑕疵图给用户。
