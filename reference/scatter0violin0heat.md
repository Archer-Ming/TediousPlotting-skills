### 包含了一系列绘图的模板

#### 散点图

```
#----------data-----------
groups = ['Upright', 'On-edge', 'Flat','Unified']
plot_dfs = []
for grp, df_src in zip(groups, [df_2, df_3, df_1,df]):
    tmp = df_src[['冲击强度']].copy()
    tmp = tmp.rename(columns={'冲击强度': 'Value'})
    tmp['Direction'] = grp
    plot_dfs.append(tmp)

plot_df = pd.concat(plot_dfs, ignore_index=True)
plot_df = plot_df.dropna(subset=['Value'])

#-----------draw-------------
palette = {'Flat': '#1f77b4', 'Upright': '#ff7f0e', 'On-edge': '#2ca02c','Unified':"#a0982c"}
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

```
# 分组散点图 + 拟合线 + 95% 置信带
# --------data----------
np.random.seed(42)
n = 60
groups = ['Method A', 'Method B', 'Method C']
data_list = []
for i, g in enumerate(groups):
    x = np.random.uniform(0, 10, n)
    y = 0.6 * x + 1.2 * i + np.random.normal(0, 1.0, n)
    data_list.append(pd.DataFrame({'x': x, 'y': y, 'Group': g}))
df = pd.concat(data_list, ignore_index=True)

#-----------draw----------
fig, ax = plt.subplots(figsize=(6.4, 4.8))
markers = ['o', 's', '^']
for i, g in enumerate(groups):
    sub = df[df['Group'] == g]
    ax.scatter(sub['x'], sub['y'],
               s=55, c=SCI_COLORS[i], marker=markers[i],
               edgecolors='white', linewidths=0.8, alpha=0.85,
               label=g, zorder=3)
    coef = np.polyfit(sub['x'], sub['y'], 1)
    xx = np.linspace(sub['x'].min(), sub['x'].max(), 100)
    yy = np.polyval(coef, xx)
    ax.plot(xx, yy, color=SCI_COLORS[i], lw=1.6, zorder=2)
    resid = sub['y'] - np.polyval(coef, sub['x'])
    se = np.std(resid)
    ax.fill_between(xx, yy - 1.96*se, yy + 1.96*se,
                    color=SCI_COLORS[i], alpha=0.12, zorder=1)

ax.set_xlabel('Predictor X (a.u.)')
ax.set_ylabel('Response Y (a.u.)')
ax.set_title('Scatter with linear fit and 95% CI')
ax.legend(loc='upper left', frameon=True, framealpha=0.9, edgecolor='0.7')
ax.grid(alpha=0.3, ls='--', lw=0.5)
plt.tight_layout()
plt.show()
```

```
#边缘分布散点 (joint plot 风)
#---------data----------
np.random.seed(7)
x = np.random.normal(5, 1.5, 200)
y = 0.7 * x + np.random.normal(0, 1.0, 200)

#------------draw------------
fig = plt.figure(figsize=(6, 6))
gs = fig.add_gridspec(2, 2, width_ratios=[4, 1], height_ratios=[1, 4],
                      hspace=0.05, wspace=0.05)
ax_main  = fig.add_subplot(gs[1, 0])
ax_top   = fig.add_subplot(gs[0, 0], sharex=ax_main)
ax_right = fig.add_subplot(gs[1, 1], sharey=ax_main)

ax_main.scatter(x, y, s=30, c=SCI_COLORS[0], alpha=0.6,
                edgecolors='white', linewidths=0.5)
coef = np.polyfit(x, y, 1)
xx = np.linspace(x.min(), x.max(), 100)
ax_main.plot(xx, np.polyval(coef, xx), color=SCI_COLORS[3], lw=2)
r = np.corrcoef(x, y)[0, 1]
ax_main.text(0.05, 0.95, f'$r = {r:.3f}$\n$N = {len(x)}$',
             transform=ax_main.transAxes, va='top', ha='left', fontsize=11,
             bbox=dict(boxstyle='round,pad=0.4', fc='white', ec='0.7', alpha=0.9))
ax_main.set_xlabel('Variable X')
ax_main.set_ylabel('Variable Y')
ax_main.grid(alpha=0.3, ls='--', lw=0.5)

ax_top.hist(x, bins=25, color=SCI_COLORS[0], alpha=0.7, edgecolor='white')
ax_top.set_ylabel('Count', fontsize=9)
ax_top.tick_params(labelbottom=False)
ax_top.spines['top'].set_visible(False)
ax_top.spines['right'].set_visible(False)

ax_right.hist(y, bins=25, orientation='horizontal',
              color=SCI_COLORS[0], alpha=0.7, edgecolor='white')
ax_right.set_xlabel('Count', fontsize=9)
ax_right.tick_params(labelleft=False)
ax_right.spines['top'].set_visible(False)
ax_right.spines['right'].set_visible(False)
plt.show()

```

#### 热力图

```
#------------data-----------------
features = [
    "bmi",
    "medication_adherence",
    "physical_activity",
    "diet",
    "stress_level",
    "sleep_hours",
    "hydration_level",
    "blood_glucose",
    "height",
    "weight"
]

# 示例相关矩阵（对称矩阵）
corr_values = np.array([
    [ 1.00,  0.02, -0.03,  0.00, -0.10,  0.01,  0.03,  0.03,  0.04, -0.01],
    [ 0.02,  1.00,  0.03,  0.08,  0.02, -0.03, -0.03,  0.06,  0.10,  0.15],
    [-0.03,  0.03,  1.00,  0.02, -0.02, -0.04, -0.02,  0.04,  0.08,  0.01],
    [ 0.00,  0.08,  0.02,  1.00,  0.03, -0.05,  0.06,  0.04, -0.03, -0.04],
    [-0.10,  0.02, -0.02,  0.03,  1.00,  0.12,  0.01,  0.04, -0.11, -0.04],
    [ 0.01, -0.03, -0.04, -0.05,  0.12,  1.00, -0.01, -0.09, -0.08, -0.02],
    [ 0.03, -0.03, -0.02,  0.06,  0.01, -0.01,  1.00,  0.07, -0.09,  0.04],
    [ 0.03,  0.06,  0.04,  0.04,  0.04, -0.09,  0.07,  1.00,  0.00,  0.06],
    [ 0.04,  0.10,  0.08, -0.03, -0.11, -0.08, -0.09,  0.00,  1.00, -0.02],
    [-0.01,  0.15,  0.01, -0.04, -0.04, -0.02,  0.04,  0.06, -0.02,  1.00]
])

# 转换为DataFrame
corr = pd.DataFrame(corr_values, index=features, columns=features)


#------------draw------------------
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
```

```
#-----------data---------------
df = pd.read_excel(file_path, index_col=0)

features = df.index.tolist()
n = len(features)

#----------------draw-----------------
fig, ax = plt.subplots(figsize=(8, 7), dpi=400)
vmin = df.values.min()
vmax = df.values.max()

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
