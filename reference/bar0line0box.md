### 包含了一系列绘图的模板

#### 柱状图

```
#----------data---------------
data = {
    'Extrusion Temperature/℃': [1.16, 4.50, 0.4237,0.6584],
    'Bed Temperature/℃': [0.0549, 0.2641, 4.46, 0.0121],
    'Printing Speed/mm∙s-1': [0.5753, 0.3722, 41.86, 0.5822],
    'Layer Height/mm': [6.75, 0.5403, 100.53, 0.0891],
    # 新增第5个特征，仅Combine方向有有效数值，其他方向设为0（避免干扰）
    'Printing direction': [0, 0, 0, 11.31]
}
df = pd.DataFrame(data, index=['Upright', 'On-edge', 'Flat', 'Combine'])

#----------process-----------
# 提取原始数据矩阵
raw_data = df.values
# 进行Min-Max归一化，避免除以0错误（添加微小常数eps）
eps = 1e-8
min_val = raw_data.min()
max_val = raw_data.max()
normalized_data = (raw_data - min_val) / (max_val - min_val + eps)
# 将归一化后的数据赋值回新的DataFrame
df_normalized = pd.DataFrame(normalized_data, index=df.index, columns=df.columns)
bar_width = 0.15  # 调整柱子宽度（5个特征需比4个更窄）
x_labels = df_normalized.index.tolist()  # 横坐标标签（打印方向）
features = df_normalized.columns.tolist()  # 5个特征名称
n_features = len(features)  # 特征数量（5）
n_x = len(x_labels)  # 横坐标类别数量（4）
x = np.arange(n_x)  # 横坐标基准位置（0,1,2,3）
# 每个特征对应的柱子偏移量（使同一打印方向的柱子并列）
offsets = np.linspace(-(n_features-1)*bar_width/2, (n_features-1)*bar_width/2, n_features)

colors = ["#649fca", "#c68f5f", "#63bd63", "#D05E5E", "#8F51C8"]  # 新增深紫色对应第5个特征

#--------draw---------
fig, ax = plt.subplots(figsize=(10, 5))  # 加宽图表尺寸（适配5个特征，避免拥挤）
# 循环绘制每个特征的柱子
for i, (feature, color, offset) in enumerate(zip(features, colors, offsets)):
    y_data = df_normalized[feature].values  # 提取归一化后的F值数据
    # 绘制柱状图
    bars = ax.bar(x + offset, y_data, width=bar_width, color=color, 
                  label=feature, alpha=0.9, edgecolor='black')
  
    # 柱子顶部添加数值标签（优化：前3个方向的第5根柱子（值为0）不显示标签，Combine方向正常显示）
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
```

```
#------------data---------------
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

#-------------draw---------------
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
# ax.set_title(direction.capitalize())

ax.spines["top"].set_visible(True)
ax.spines["right"].set_visible(True)

ax.legend(
loc="lower center",           # 图例锚点在底部中间
bbox_to_anchor=(0.5, 0.98),  # 0.5表示x轴正中，1.08表示y轴略高于图表
frameon=False,
ncol=len(models),              # 如果想让图例横向排列
fontsize=12
)

plt.tight_layout()
plt.show()
plt.close(fig) 
```

```
#-----------draw------------
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

#### 折线图

```
def plot_all_directions_combined(direction_data, save_path=None):
    """
    在同一张图的 2x2 子图中绘制每个自变量的多方向对比（每个子图包含所有 sheet 的曲线）
    """

  #---------data---------
    features = [
        {'col': '层厚/ mm', 'title': '(a) Layer height', 'xlabel': 'Layer height (mm)', 'xticks': [0.1, 0.2, 0.3]},
        {'col': 'Printing speed/ mm·s-1', 'title': '(b) Printing speed', 'xlabel': 'Printing speed (mm・s⁻¹)', 'xticks': [30, 75, 120]},
        {'col': ' 热床温度/ °C', 'title': '(c) Bed temperature', 'xlabel': 'Bed temperature (°C)', 'xticks': [70, 80, 90]},
        {'col': '喷嘴挤出温度 /°C', 'title': '(d) Extrusion temperature', 'xlabel': 'Extrusion temperature (°C)', 'xticks': [300, 310, 320]}
    ]

    dir_items = list(direction_data.items())
    dir_names = [k for k, _ in dir_items]
    n_dirs = len(dir_items)

    #-------draw------------
    fig, axes = plt.subplots(2, 2, figsize=(6, 8), dpi=300)
    axes = axes.flatten()
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

```
# 多曲线 + 误差带 (shaded ±1σ)
#--------data-----------
np.random.seed(1)
x = np.linspace(0, 100, 50)
methods = ['Baseline', 'Proposed', 'Ablation-1', 'Ablation-2']

#----------draw-------------
fig, ax = plt.subplots(figsize=(6.5, 4.5))
for i, m in enumerate(methods):
    base = 0.3 + 0.5*(1 - np.exp(-x/(20+i*8))) + i*0.05
    err  = np.random.normal(0, 0.015 + 0.01*i, (10, len(x)))
    runs = base + err
    mean = runs.mean(0); std = runs.std(0)
    ax.plot(x, mean, color=SCI_COLORS[i], lw=2, label=m,
            marker='os^D'[i], markersize=5, markevery=5,
            markeredgecolor='white', markeredgewidth=0.6)
    ax.fill_between(x, mean-std, mean+std, color=SCI_COLORS[i], alpha=0.15)

ax.set_xlabel('Training epoch')
ax.set_ylabel('Validation accuracy')
ax.set_title(r'Learning curves with $\pm 1\sigma$ shaded band')
ax.legend(loc='lower right', frameon=True, framealpha=0.9, edgecolor='0.7', fontsize=9)
ax.grid(alpha=0.3, ls='--', lw=0.5)
ax.set_ylim(0.3, 1.0)
plt.tight_layout()
plt.show()

```

```
#双 y 轴折线
#--------------data----------------
np.random.seed(3)
x = np.arange(1, 13)
y_left  = 100 + 15 * np.cumsum(np.random.normal(0.3, 0.6, 12))
y_right = 0.6 + 0.04 * np.cumsum(np.random.normal(-0.2, 0.5, 12))

#----------------draw---------------
fig, ax1 = plt.subplots(figsize=(6.5, 4.5))
c1, c2 = SCI_COLORS[0], SCI_COLORS[3]
ax1.plot(x, y_left, color=c1, lw=2.2, marker='o', markersize=7,
         markeredgecolor='white', markeredgewidth=0.8, label='Throughput')
ax1.set_xlabel('Month')
ax1.set_ylabel('Throughput (units $\\cdot$ month$^{-1}$)', color=c1)
ax1.tick_params(axis='y', colors=c1)
ax1.spines['left'].set_color(c1)

ax2 = ax1.twinx()
ax2.plot(x, y_right, color=c2, lw=2.2, marker='s', markersize=7,
         markeredgecolor='white', markeredgewidth=0.8, label='Defect rate')
ax2.set_ylabel('Defect rate', color=c2)
ax2.tick_params(axis='y', colors=c2)
ax2.spines['right'].set_color(c2)
ax2.spines['left'].set_color(c1)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1+lines2, labels1+labels2, loc='upper left',
           frameon=True, framealpha=0.9, edgecolor='0.7')
ax1.grid(alpha=0.3, ls='--', lw=0.5)
plt.title('Dual-axis: production vs. quality')
plt.tight_layout()
plt.show()

```

#### 箱线图

```
def create_density_boxplot(sheet_name, data, color):
    """
    创建核密度曲线和横放箱线图的组合图
    """
#-------data------------
    # 提取冲击强度数据，去除可能的NaN值
    impact_strength = data['冲击强度'].dropna()
  
    # 计算核密度估计
    kde = gaussian_kde(impact_strength)
    x_range = np.linspace(impact_strength.min() * 0.9, impact_strength.max() * 1.1, 1000)
    density = kde(x_range)
  

#--------draw----------
    #创建图形
    fig, ax = plt.subplots(figsize=(10, 6))
    #绘制核密度曲线
    ax.plot(x_range, density, color=color, linewidth=4.5, label=f'{sheet_name} Dataset')
 
    # 创建第二个y轴用于箱线图（位置在y=0附近）
    ax2 = ax.twinx()
  
    # 绘制横放箱线图，设置在y=0位置
    bp = ax2.boxplot(impact_strength, vert=False, positions=[0], 
                     widths=0.1 * max(density), patch_artist=True,
                     boxprops=dict(facecolor=color, alpha=0.7, edgecolor='black', linewidth=1.2),
                     medianprops=dict(color='black', linewidth=1.5),
                     whiskerprops=dict(color='black', linewidth=1.2),
                     capprops=dict(color='black', linewidth=1.2),
                     flierprops=dict(marker='o', markerfacecolor=color, markersize=4, alpha=0.6))
  
    # 设置第二个y轴的范围和标签
    ax2.set_ylim(-0.05 * max(density), 0.15 * max(density))
    ax2.set_yticks([0])
    ax2.set_yticklabels([f'{sheet_name}'], fontsize=12, fontweight='bold')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(False)
  
    # 设置主坐标轴
    ax.set_xlabel('Impact Strength (kJ・m⁻²)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Kernel Density', fontsize=16, fontweight='bold')
  
    # ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.8)
  
    # 设置标题
    # title = f'Kernel Density Estimation and Distribution of Impact Strength\\nfor {sheet_name} Augmented Dataset'
    # ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
  
    ax.set_xlim(impact_strength.min() * 0.8, impact_strength.max() * 1.2)
    ax.set_ylim(0, max(density) * 1.15)
  
    # 添加统计信息文本框
    # stats_text = f'Sample Size: {len(impact_strength):,}\nMean: {impact_strength.mean():.3f}\nStd: {impact_strength.std():.3f}\nMin: {impact_strength.min():.3f}\nMax: {impact_strength.max():.3f}'
    # ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=14,
    #         verticalalignment='top',horizontalalignment='left', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor=color))
  
    plt.tight_layout()
    plt.show()
  
    return filename

```

```
#分组箱线图 + 显著性 bracket
#--------data------------
np.random.seed(13)
groups = ['Control', 'Low dose', 'High dose']
conds  = ['Day 1', 'Day 7', 'Day 14']
records = []
means = {('Control','Day 1'): 5.0,  ('Control','Day 7'): 5.2,  ('Control','Day 14'): 5.1,
         ('Low dose','Day 1'): 5.6, ('Low dose','Day 7'): 6.4, ('Low dose','Day 14'): 6.9,
         ('High dose','Day 1'): 5.9,('High dose','Day 7'): 7.3,('High dose','Day 14'): 8.5}
for g in groups:
    for c in conds:
        for v in np.random.normal(means[(g,c)], 0.65, 14):
            records.append((g, c, v))
df = pd.DataFrame(records, columns=['Group', 'Condition', 'Value'])
palette = dict(zip(groups, SCI_COLORS[:3]))

#------draw----------
fig, ax = plt.subplots(figsize=(7.2, 4.8))
sns.boxplot(data=df, x='Condition', y='Value', hue='Group',
            palette=palette, width=0.66, linewidth=0.9, fliersize=0, ax=ax)
sns.stripplot(data=df, x='Condition', y='Value', hue='Group',
              dodge=True, palette=palette, size=3.2, alpha=0.55,
              edgecolor='white', linewidth=0.3, ax=ax, legend=False)

ax.set_xlabel('')
ax.set_ylabel('Biomarker level (a.u.)')
ax.set_title('Treatment effect across time points')
ax.legend(title='Group', loc='upper left', frameon=True,
          framealpha=0.9, edgecolor='0.7')

def add_bracket(ax, x1, x2, y, h, p_text):
    ax.plot([x1, x1, x2, x2], [y, y+h, y+h, y], color='0.2', lw=1.0)
    ax.text((x1+x2)/2, y+h+0.02, p_text, ha='center', va='bottom', fontsize=10)

y_top = df['Value'].max()
add_bracket(ax, 1-0.27, 1+0.27, y_top+0.3, 0.15, '**')
add_bracket(ax, 2-0.27, 2+0.27, y_top+1.0, 0.15, '***')
add_bracket(ax, 2-0.27, 2,      y_top+0.5, 0.10, 'n.s.')

ax.set_ylim(df['Value'].min()-0.5, y_top + 1.6)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.show()

```
