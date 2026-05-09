## Contains a series of plotting templates

### Important Rules!

* The first part of the code in each type of template presents charts from simple to complex. You need to learn these templates progressively.
* The remaining template code in each type contains charts with specific unique styles and designs. You should also learn these templates.
* For the x-coordinates, y-coordinates, data title names in the sample data of the reference templates, or the data processing/reading, please strictly ignore them!!!

#### Scatter Plot

```
#-------Part One Code---------
#-----draw-----
fig = plt.figure(figsize=FIGSIZE)
gs = GridSpec(1, 4, figure=fig, wspace=0.30)
fig.suptitle('Fig 1. Scatter Plots — simple to complex',
             fontsize=14, fontweight='bold', y=1.02)

# (a) basic
ax = fig.add_subplot(gs[0])
n = 80
x = rng.normal(0, 1, n); y = 0.6*x + rng.normal(0, 0.5, n)
ax.scatter(x, y, s=35, color=C[0], alpha=0.7, edgecolor='white', linewidths=0.6)
ax.set_xlabel('X'); ax.set_ylabel('Y')
panel(ax, 'a', 'Basic scatter')

# (b) grouped + regression
ax = fig.add_subplot(gs[1])
for i, g in enumerate(['Group A', 'Group B', 'Group C']):
    xg = rng.normal(i*1.5, 0.8, 50)
    yg = 0.7*xg + i*0.5 + rng.normal(0, 0.5, 50)
    ax.scatter(xg, yg, s=35, color=C[i], alpha=0.7,
               edgecolor='white', linewidths=0.6, label=g)
    m, b = np.polyfit(xg, yg, 1)
    xfit = np.linspace(xg.min(), xg.max(), 30)
    ax.plot(xfit, m*xfit + b, color=C[i], lw=1.6, alpha=0.9)
ax.set_xlabel('X'); ax.set_ylabel('Y')
ax.legend(loc='upper left', frameon=True, framealpha=0.9)
panel(ax, 'b', 'Grouped + regression lines')

# (c) bubble
ax = fig.add_subplot(gs[2])
n = 80
x = rng.uniform(0, 10, n); y = rng.uniform(0, 10, n)
s = rng.uniform(40, 600, n); cv = rng.uniform(0, 1, n)
sc = ax.scatter(x, y, s=s, c=cv, cmap='viridis',
                alpha=0.75, edgecolor='white', linewidths=0.7)
cb = fig.colorbar(sc, ax=ax, shrink=0.85, pad=0.02)
cb.set_label('Intensity', fontsize=8)
ax.set_xlabel('X'); ax.set_ylabel('Y')
panel(ax, 'c', 'Bubble chart (4D)')

# (d) joint plot with KDE + outlier annotations
ax = fig.add_subplot(gs[3])
n = 220
x = rng.normal(0, 1, n); y = 0.7*x + rng.normal(0, 0.5, n)
ax.scatter(x, y, s=18, color=C[0], alpha=0.55, edgecolor='white', linewidths=0.3)
sns.kdeplot(x=x, y=y, ax=ax, levels=6, colors='black',
            linewidths=0.8, alpha=0.6)
z = (x - x.mean())**2 + (y - y.mean())**2
out = np.argsort(z)[-3:]
ax.scatter(x[out], y[out], s=110, facecolor='none',
           edgecolor=C[3], linewidth=2, zorder=5)
for i in out:
    ax.annotate(f'#{i}', (x[i], y[i]), xytext=(7, 7),
                textcoords='offset points', fontsize=8,
                color=C[3], fontweight='bold')
r, _ = stats.pearsonr(x, y)
ax.text(0.04, 0.96, f'r = {r:.3f}\nn = {n}',
        transform=ax.transAxes, va='top', fontsize=8.5,
        bbox=dict(boxstyle='round,pad=0.35', facecolor='white',
                  edgecolor='gray', alpha=0.9))
ax.set_xlabel('X'); ax.set_ylabel('Y')
panel(ax, 'd', 'KDE contours + outliers')

plt.show()
```

```
# Scatter + Box plot + Violin
#----------data-----------
groups = ['Upright', 'On-edge', 'Flat','Unified']
plot_dfs = []
for grp, df_src in zip(groups, [df_2, df_3, df_1,df]):
    tmp = df_src[['Impact Strength']].copy()
    tmp = tmp.rename(columns={'Impact Strength': 'Value'})
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
# Overlay box plot in the center of the violin plot
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
# Static text box
plt.text(
    x=0.5,  # Normalized x-coordinate: 5% from left edge of plot (0=leftmost, 1=rightmost)
    y=0.1,  # Normalized y-coordinate: 5% from bottom edge of plot (0=bottom, 1=top)
    s=f"           Data Points  \n           Outlier(Removed)  ",  # Content to input, \n for newline
    fontsize=14,  # Text size inside the box
    bbox=dict(    # Configure text box style (key for "frame" effect)
        boxstyle="round,pad=0.5",  # Box style: rounded corners + padding
        facecolor="white",     # Box background color
        edgecolor="black",          # Box border color
        alpha=0.8                  # Box transparency (0=fully transparent, 1=opaque)
    ),
    transform=plt.gca().transAxes,  # Key: enable normalized coordinates, fixed on the figure window

)
# Add sample scatter points (semi-transparent with jitter), placed on top
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
ax.set_ylabel('Impact Strength')
plt.title('Three-direction Impact Strength Distribution (Violin + Box + Points)')
plt.tight_layout()
plt.show()
```

```
# Grouped scatter + fit lines + 95% confidence band
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
# Marginal distribution scatter (joint plot style)
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

```
# Pareto front scatter plot
#--------------data---------------
rng = np.random.default_rng(15)
n = 250
f1 = rng.uniform(0.2, 1.0, n)
f2 = 1.0 / (f1 + 0.1) + rng.normal(0, 0.3, n) + rng.uniform(0, 0.5, n)
cost = rng.uniform(0, 100, n)

# Compute Pareto front (minimizing two objectives)
idx = np.argsort(f1)
f1_s, f2_s, cost_s = f1[idx], f2[idx], cost[idx]
pareto_mask = np.ones(n, dtype=bool)
cur_min = np.inf
for i in range(n):
    if f2_s[i] < cur_min:
        cur_min = f2_s[i]
    else:
        pareto_mask[i] = False
#-----------------draw------------
fig, ax = plt.subplots(figsize=(10, 7))
sc = ax.scatter(f1_s[~pareto_mask], f2_s[~pareto_mask], c=cost_s[~pareto_mask],
                cmap='plasma', s=45, alpha=0.55,
                edgecolor='white', linewidth=0.4,
                label='Dominated solutions')
ax.scatter(f1_s[pareto_mask], f2_s[pareto_mask], c=cost_s[pareto_mask],
           cmap='plasma', s=140, alpha=1, edgecolor='black', linewidth=1.2,
           marker='*', label='Pareto front')
ax.plot(f1_s[pareto_mask], f2_s[pareto_mask], '--',
        color='#C73E1D', lw=1.5, alpha=0.7, zorder=1)

cb = fig.colorbar(sc, ax=ax, label='Cost ($k)')
cb.outline.set_linewidth(0.5)
ax.set_xlabel('Objective 1: Strength (normalized)', fontweight='bold')
ax.set_ylabel('Objective 2: Weight (normalized)', fontweight='bold')
ax.set_title('Multi-objective Optimization — Pareto Front',
             fontweight='bold', pad=12)
ax.legend(loc='upper right', frameon=True, framealpha=0.95)
ax.grid(alpha=0.3, linestyle='--'); ax.set_axisbelow(True)
plt.tight_layout()
plt.show()
```

```
# Correlation + marginal distribution + density (4-panel)
#---------------data------------------
n = 200
x = np.random.normal(0, 1, n)
y = 0.7 * x + np.random.normal(0, 0.6, n)
z = -0.5 * x + np.random.normal(0, 0.7, n)
#-------------draw---------------
fig = plt.figure(figsize=(12, 9))
gs = GridSpec(3, 2, figure=fig, hspace=0.50, wspace=0.22,
              height_ratios=[1, 4, 4])

# Top marginal histograms
ax_top1 = fig.add_subplot(gs[0, 0])
ax_top1.hist(x, bins=25, color=SCI_COLORS[0], edgecolor='white', alpha=0.85)
ax_top1.set_xticks([]); ax_top1.set_yticks([])
for s in ['top', 'right', 'left']:
    ax_top1.spines[s].set_visible(False)

ax_top2 = fig.add_subplot(gs[0, 1])
ax_top2.hist(x, bins=25, color=SCI_COLORS[1], edgecolor='white', alpha=0.85)
ax_top2.set_xticks([]); ax_top2.set_yticks([])
for s in ['top', 'right', 'left']:
    ax_top2.spines[s].set_visible(False)

# Second row: regression scatter with confidence band
ax1 = fig.add_subplot(gs[1, 0])
sns.regplot(x=x, y=y, ax=ax1, color=SCI_COLORS[0],
            scatter_kws={'s': 28, 'alpha': 0.65, 'edgecolor': 'white', 'linewidths': 0.6},
            line_kws={'color': SCI_COLORS[3], 'linewidth': 2})
r1, p1 = stats.pearsonr(x, y)
ax1.text(0.05, 0.95, f'r = {r1:.3f}\np < 0.001',
         transform=ax1.transAxes, fontsize=10, va='top',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                   edgecolor='gray', alpha=0.85))
ax1.set_xlabel('Predictor X'); ax1.set_ylabel('Response Y')
ax1.set_title('(a) Linear regression — positive correlation', loc='left', fontweight='bold')
ax1.grid(alpha=0.3, linestyle='--')

ax2 = fig.add_subplot(gs[1, 1])
sns.regplot(x=x, y=z, ax=ax2, color=SCI_COLORS[1],
            scatter_kws={'s': 28, 'alpha': 0.65, 'edgecolor': 'white', 'linewidths': 0.6},
            line_kws={'color': SCI_COLORS[3], 'linewidth': 2})
r2, p2 = stats.pearsonr(x, z)
ax2.text(0.05, 0.95, f'r = {r2:.3f}\np < 0.001',
         transform=ax2.transAxes, fontsize=10, va='top',
         bbox=dict(boxstyle='round,pad=0.4', facecolor='white',
                   edgecolor='gray', alpha=0.85))
ax2.set_xlabel('Predictor X'); ax2.set_ylabel('Response Z')
ax2.set_title('(b) Linear regression — negative correlation', loc='left', fontweight='bold')
ax2.grid(alpha=0.3, linestyle='--')

# Third row: density panels
ax3 = fig.add_subplot(gs[2, 0])
hb = ax3.hexbin(x, y, gridsize=22, cmap='Blues', mincnt=1,
                edgecolors='white', linewidths=0.2)
fig.colorbar(hb, ax=ax3, shrink=0.85, label='Count', pad=0.02)
ax3.set_xlabel('Predictor X'); ax3.set_ylabel('Response Y')
ax3.set_title('(c) Hexbin density', loc='left', fontweight='bold')

ax4 = fig.add_subplot(gs[2, 1])
sns.kdeplot(x=x, y=z, ax=ax4, cmap='RdPu', fill=True, levels=10, alpha=0.9)
ax4.scatter(x, z, s=8, color='white', alpha=0.45, edgecolor='black', linewidths=0.3)
ax4.set_xlabel('Predictor X'); ax4.set_ylabel('Response Z')
ax4.set_title('(d) 2D KDE contours', loc='left', fontweight='bold')

fig.suptitle('Correlation Analysis with Marginal Distributions and Density Estimates',
             fontsize=14, fontweight='bold', y=0.995)
plt.show()
```

#### Bar Chart

```
#-----------Part One Code------------
#-------draw---------
fig = plt.figure(figsize=FIGSIZE)
gs = GridSpec(1, 4, figure=fig, wspace=0.32)
fig.suptitle('Fig 2. Bar Charts — simple to complex',
             fontsize=14, fontweight='bold', y=1.02)

cats = ['A', 'B', 'C', 'D', 'E']

# (a) basic
ax = fig.add_subplot(gs[0])
vals = rng.uniform(20, 80, 5)
bars = ax.bar(cats, vals, color=C[0], edgecolor='black', linewidth=0.6)
for b, v in zip(bars, vals):
    ax.text(b.get_x() + b.get_width()/2, v + 1.5, f'{v:.0f}',
            ha='center', fontsize=8.5)
ax.set_ylabel('Value'); ax.set_xlabel('Category')
ax.set_ylim(0, max(vals)*1.18)
panel(ax, 'a', 'Basic bars')

# (b) grouped
ax = fig.add_subplot(gs[1])
x = np.arange(len(cats))
train = rng.uniform(40, 80, 5); test = train - rng.uniform(2, 12, 5)
w = 0.35
ax.bar(x - w/2, train, w, color=C[0], edgecolor='black', label='Train')
ax.bar(x + w/2, test, w, color=C[2], edgecolor='black', label='Test', hatch='///')
ax.set_xticks(x); ax.set_xticklabels(cats)
ax.set_ylabel('Score'); ax.legend(frameon=False, loc='upper right')
panel(ax, 'b', 'Grouped (train vs test)')

# (c) stacked + errorbar + significance
ax = fig.add_subplot(gs[2])
parts = ['α', 'β', 'γ']
data = rng.uniform(8, 25, (3, 5))
err  = rng.uniform(0.8, 2.0, 5)
bottom = np.zeros(5)
for i, p in enumerate(parts):
    ax.bar(cats, data[i], bottom=bottom, color=C[i], edgecolor='white',
           linewidth=0.8, label=f'Component {p}')
    bottom += data[i]
ax.errorbar(cats, bottom, yerr=err, fmt='none', ecolor='black',
            capsize=5, capthick=1.2, lw=1.2)
# significance bracket
y0 = bottom.max() + 4
ax.plot([0, 0, 4, 4], [y0-1, y0, y0, y0-1], color='black', lw=1)
ax.text(2, y0 + 0.5, '**', ha='center', fontsize=12, fontweight='bold')
ax.set_ylim(0, y0 + 6)
ax.set_ylabel('Total'); ax.legend(frameon=False, loc='lower right', fontsize=8)
panel(ax, 'c', 'Stacked + error bars + sig.')

# (d) diverging horizontal (positive/negative) sorted
ax = fig.add_subplot(gs[3])
items = [f'Item {i}' for i in range(10)]
vals = rng.normal(0, 1, 10)
order = np.argsort(vals)
items = [items[i] for i in order]; vals = vals[order]
colors = [C[0] if v > 0 else C[3] for v in vals]
ax.barh(items, vals, color=colors, edgecolor='black', linewidth=0.5, alpha=0.9)
for i, v in enumerate(vals):
    ax.text(v + (0.05 if v > 0 else -0.05), i, f'{v:+.2f}',
            va='center', ha='left' if v > 0 else 'right', fontsize=8)
ax.axvline(0, color='black', lw=0.8)
pad = max(abs(vals.min()), abs(vals.max())) * 0.25
ax.set_xlim(vals.min() - pad, vals.max() + pad)
ax.set_xlabel('Deviation from mean')
panel(ax, 'd', 'Diverging horizontal bars')

plt.show()

```

```
#----------data---------------
data = {
    'Extrusion Temperature/℃': [1.16, 4.50, 0.4237,0.6584],
    'Bed Temperature/℃': [0.0549, 0.2641, 4.46, 0.0121],
    'Printing Speed/mm∙s-1': [0.5753, 0.3722, 41.86, 0.5822],
    'Layer Height/mm': [6.75, 0.5403, 100.53, 0.0891],
    # Added 5th feature, only Combine direction has valid values, others set to 0 (avoid interference)
    'Printing direction': [0, 0, 0, 11.31]
}
df = pd.DataFrame(data, index=['Upright', 'On-edge', 'Flat', 'Combine'])

#----------process-----------
# Extract raw data matrix
raw_data = df.values
# Perform Min-Max normalization, avoid division by 0 error (add tiny constant eps)
eps = 1e-8
min_val = raw_data.min()
max_val = raw_data.max()
normalized_data = (raw_data - min_val) / (max_val - min_val + eps)
# Assign normalized data back to a new DataFrame
df_normalized = pd.DataFrame(normalized_data, index=df.index, columns=df.columns)
bar_width = 0.15  # Adjust bar width (5 features need narrower bars than 4)
x_labels = df_normalized.index.tolist()  # x-axis labels (printing direction)
features = df_normalized.columns.tolist()  # 5 feature names
n_features = len(features)  # Number of features (5)
n_x = len(x_labels)  # Number of x-axis categories (4)
x = np.arange(n_x)  # x-axis base positions (0,1,2,3)
# Bar offset for each feature (so bars in the same printing direction are side by side)
offsets = np.linspace(-(n_features-1)*bar_width/2, (n_features-1)*bar_width/2, n_features)

colors = ["#649fca", "#c68f5f", "#63bd63", "#D05E5E", "#8F51C8"]  # Added dark purple corresponding to the 5th feature

#--------draw---------
fig, ax = plt.subplots(figsize=(10, 5))  # Widen chart size (fits 5 features, avoids crowding)
# Loop to draw bars for each feature
for i, (feature, color, offset) in enumerate(zip(features, colors, offsets)):
    y_data = df_normalized[feature].values  # Extract normalized F-value data
    # Draw bar chart
    bars = ax.bar(x + offset, y_data, width=bar_width, color=color, 
                  label=feature, alpha=0.9, edgecolor='black')
  
    # Add value labels at top of bars (optimization: don't show labels for the 5th bar (value=0) in first 3 directions; show normally for Combine direction)
    for bar_idx, bar in enumerate(bars):
        height = bar.get_height()
        # Conditions: 1. Height > 0 (exclude 5th bar in first 3 directions) 2. Not the 5th feature in first 3 directions
        if height > 1e-3:  # Filter very small values (close to 0 after normalization)
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.005,
                    f'{height:.3f}', ha='center', va='bottom', fontsize=8)

# Set x-axis labels and positions
ax.set_xticks(x)
ax.set_xticklabels(x_labels, rotation=0)  # x-axis labels not rotated, keep clean

# Set y-axis label (annotated as normalized, bold for emphasis)
ax.set_ylabel('Normalized F-value', fontweight='bold')
# Set y-axis range (data is in [0,1] after normalization, reserve 20% space to avoid label obstruction)
ax.set_ylim(0, 1.2)
# Add legend (positioned outside on right side of chart, fits 5 features, avoids covering bars)
ax.legend( loc='upper right', bbox_to_anchor=(1, 1), frameon=False)
# Adjust layout (prevent legend and labels from being cut off, fits widened chart)
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
loc="lower center",           # Legend anchor at bottom center
bbox_to_anchor=(0.5, 0.98),  # 0.5 means x-axis center, 1.08 means slightly above the chart on y-axis
frameon=False,
ncol=len(models),              # If you want the legend arranged horizontally
fontsize=12
)

plt.tight_layout()
plt.show()
plt.close(fig) 
```

```
#-----------draw------------
color = 'teal'  # Color for a single group
bar_width = 0.25  # Bar width
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

#### Line Chart

```
#---------Part One Code--------------
#------draw-------
fig = plt.figure(figsize=FIGSIZE)
gs = GridSpec(1, 4, figure=fig, wspace=0.32)
fig.suptitle('Fig 3. Line Plots — simple to complex',
             fontsize=14, fontweight='bold', y=1.02)

x = np.linspace(0, 10, 50)

# (a) basic
ax = fig.add_subplot(gs[0])
ax.plot(x, np.sin(x), color=C[0], lw=2)
ax.set_xlabel('Time (s)'); ax.set_ylabel('Signal')
panel(ax, 'a', 'Single line')

# (b) multi-series with markers
ax = fig.add_subplot(gs[1])
ax.plot(x, np.sin(x), color=C[0], lw=2, marker='o', ms=4, label='sin')
ax.plot(x, np.cos(x), color=C[1], lw=2, marker='s', ms=4, label='cos')
ax.plot(x, np.sin(x)*np.cos(x), color=C[2], lw=2, marker='^', ms=4, label='sin·cos')
ax.set_xlabel('Time (s)'); ax.set_ylabel('Signal')
ax.legend(frameon=True, framealpha=0.9, loc='lower left')
panel(ax, 'b', 'Multi-series + markers')

# (c) confidence band + smoothing
ax = fig.add_subplot(gs[2])
xs = np.linspace(0, 10, 30)
for i, mu_off in enumerate([0, 0.8, -0.6]):
    ymean = np.sin(xs - i*0.5) + mu_off
    yerr  = 0.15 + 0.05*rng.uniform(0, 1, len(xs))
    ax.plot(xs, ymean, color=C[i], lw=2, marker='o', ms=5,
            markeredgecolor='white', mew=0.8, label=f'Series {i+1}')
    ax.fill_between(xs, ymean - yerr, ymean + yerr, color=C[i], alpha=0.18)
ax.set_xlabel('X'); ax.set_ylabel('Y')
ax.legend(frameon=True, framealpha=0.9)
panel(ax, 'c', 'Mean ± CI band')

# (d) annotated event timeline + dual-axis
ax = fig.add_subplot(gs[3])
t = np.arange(0, 100)
y1 = 50 + 10*np.sin(t/8) + np.cumsum(rng.normal(0, 0.3, 100))
y2 = 100 + 30*np.cos(t/12) + np.cumsum(rng.normal(0, 0.5, 100))
ax.plot(t, y1, color=C[0], lw=1.8, label='Metric A')
ax.fill_between(t, y1.min()-5, y1, color=C[0], alpha=0.10)
ax2 = ax.twinx()
ax2.plot(t, y2, color=C[3], lw=1.8, label='Metric B')
ax2.set_ylabel('Metric B', color=C[3])
ax2.tick_params(axis='y', labelcolor=C[3])
# event markers
events = [(20, 'Launch'), (55, 'Update'), (80, 'Spike')]
for ev_t, ev_lbl in events:
    ax.axvline(ev_t, color='gray', ls='--', lw=0.8, alpha=0.7)
    ax.annotate(ev_lbl, xy=(ev_t, y1.max()), xytext=(ev_t, y1.max()+3),
                ha='center', fontsize=8,
                bbox=dict(boxstyle='round,pad=0.25', facecolor='lightyellow',
                          edgecolor='gray', alpha=0.95))
ax.set_xlabel('Time'); ax.set_ylabel('Metric A', color=C[0])
ax.tick_params(axis='y', labelcolor=C[0])
ax.set_title('(d) Dual-axis + event annotations',
             loc='left', fontweight='bold', fontsize=10.5, pad=8)
ax.grid(alpha=0.3, linestyle='--'); ax.set_axisbelow(True)

# combined legend
h1, l1 = ax.get_legend_handles_labels()
h2, l2 = ax2.get_legend_handles_labels()
ax.legend(h1 + h2, l1 + l2, frameon=True, framealpha=0.9, loc='lower right')

plt.show()

```

```
def plot_all_directions_combined(direction_data, save_path=None):
    """
    Draw multi-direction comparison for each independent variable in the same 2x2 subplot figure (each subplot contains curves for all sheets)
    """

  #---------data---------
    features = [
        {'col': 'Layer Thickness/ mm', 'title': '(a) Layer height', 'xlabel': 'Layer height (mm)', 'xticks': [0.1, 0.2, 0.3]},
        {'col': 'Printing speed/ mm·s-1', 'title': '(b) Printing speed', 'xlabel': 'Printing speed (mm・s⁻¹)', 'xticks': [30, 75, 120]},
        {'col': ' Bed Temperature/ °C', 'title': '(c) Bed temperature', 'xlabel': 'Bed temperature (°C)', 'xticks': [70, 80, 90]},
        {'col': 'Nozzle Extrusion Temperature /°C', 'title': '(d) Extrusion temperature', 'xlabel': 'Extrusion temperature (°C)', 'xticks': [300, 310, 320]}
    ]

    dir_items = list(direction_data.items())
    dir_names = [k for k, _ in dir_items]
    n_dirs = len(dir_items)

    #-------draw------------
    fig, axes = plt.subplots(2, 2, figsize=(6, 8), dpi=300)
    axes = axes.flatten()
    from itertools import cycle
    color_cycle = cycle(colors)

    # Main loop: draw all direction curves in each subplot
    for i, (feat, ax) in enumerate(zip(features, axes)):
        all_y_means = []
        all_y_stds = []
        all_xs = []

        # Prepare for legend
        handles = []
        labels = []

        # Iterate through each direction and draw its curve (mean + error)
        for j, (dir_name, df_dir) in enumerate(dir_items):
            processed_df = process_data(df_dir, feat['col'])
            if processed_df.empty:
                continue
            x = processed_df[feat['col']]
            y_mean = processed_df['mean']
            y_std = processed_df['std']

            col = colors[j % len(colors)]
            # Draw line and error bars
            line = ax.errorbar(
                x=x, y=y_mean, yerr=y_std,
                color=col,
                linestyle=line_style,
                marker=['o', 's', '^'][j % 3],  # Different markers for different directions
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

        # Set x-axis ticks: prefer xticks from config, otherwise use combined sorted x values
        if 'xticks' in feat and feat['xticks'] is not None:
            desired_ticks = np.array(feat['xticks'], dtype=float)
            # Use intersection/union of x ranges from all directions as reference
            if all_xs:
                xmin = min([xs.min() for xs in all_xs])
                xmax = max([xs.max() for xs in all_xs])
                valid_ticks = desired_ticks[(desired_ticks >= xmin) & (desired_ticks <= xmax)]
            else:
                valid_ticks = desired_ticks
            if len(valid_ticks) == 0:
                # Fall back to combined x value positions
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

        # Subplot beautification
        ax.set_title(feat['title'], fontsize=12, fontweight='bold', pad=10)
        ax.set_xlabel(feat['xlabel'], fontsize=10)
        ax.set_ylabel('Impact strength (kJ・m⁻²)', fontsize=10)
        ax.tick_params(axis='both', labelsize=8)

        # Combine y range to ensure error bars don't go out of bounds
        if all_y_means:
            combined_mean = pd.concat(all_y_means, ignore_index=True)
            combined_std = pd.concat(all_y_stds, ignore_index=True)
            y_min = combined_mean.min() - 2 * (combined_std.max() if not np.isnan(combined_std.max()) else 0)
            y_max = combined_mean.max() + 2 * (combined_std.max() if not np.isnan(combined_std.max()) else 0)
            ax.set_ylim(y_min, y_max)

   
        # ax.legend( fontsize=12, title='Direction', title_fontsize=10, loc='lower right')

    # Global title and layout
    fig.suptitle(f'Impact strength of FDM specimens - combined directions', fontsize=12, fontweight='bold', y=0.98)
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

```

```
# Multiple curves + error band (shaded ±1σ)
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
# Dual y-axis line plot
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

#### Box Plot, Violin Plot

```
#-----------Part One Code------------
#-----draw-------
fig = plt.figure(figsize=FIGSIZE)
gs = GridSpec(1, 4, figure=fig, wspace=0.30)
fig.suptitle('Fig 4. Distribution Comparison — Box / Violin',
             fontsize=14, fontweight='bold', y=1.02)

groups = ['A', 'B', 'C', 'D']
rows = []
for g in groups:
    for v in rng.normal({'A':50,'B':55,'C':48,'D':60}[g], 6, 80):
        rows.append({'g': g, 'v': v, 'sex': rng.choice(['M', 'F'])})
df = pd.DataFrame(rows)

# (a) basic box
ax = fig.add_subplot(gs[0])
sns.boxplot(data=df, x='g', y='v', palette=C[:4], ax=ax, linewidth=1)
ax.set_xlabel('Group'); ax.set_ylabel('Value')
panel(ax, 'a', 'Basic box plot')

# (b) notched box + swarm
ax = fig.add_subplot(gs[1])
sns.boxplot(data=df, x='g', y='v', palette=C[:4], ax=ax,
            notch=True, linewidth=1, showfliers=False,
            medianprops=dict(color='red', lw=1.8))
sns.stripplot(data=df, x='g', y='v', ax=ax, color='black',
              size=2.5, alpha=0.5, jitter=0.2)
ax.set_xlabel('Group'); ax.set_ylabel('Value')
panel(ax, 'b', 'Notched box + strip points')

# (c) split violin by sex
ax = fig.add_subplot(gs[2])
sns.violinplot(data=df, x='g', y='v', hue='sex', split=True,
               palette={'M': C[0], 'F': C[1]}, inner='quart',
               linewidth=1, ax=ax)
ax.set_xlabel('Group'); ax.set_ylabel('Value')
ax.legend(title='Sex', frameon=True, loc='lower right')
panel(ax, 'c', 'Split violin (by hue)')

# (d) violin + box + strip stacked
ax = fig.add_subplot(gs[3])
sns.violinplot(data=df, x='g', y='v', palette=C[:4], inner=None,
               linewidth=1, alpha=0.55, ax=ax, cut=0)
sns.boxplot(data=df, x='g', y='v', width=0.18,
            boxprops=dict(facecolor='white', edgecolor='black'),
            medianprops=dict(color='red', lw=1.8),
            showfliers=False, ax=ax)
sns.stripplot(data=df, x='g', y='v', palette=C[:4],
              size=2.2, alpha=0.45, jitter=0.18, ax=ax,
              edgecolor='auto', linewidth=0.2)
# mean diamonds
means = df.groupby('g')['v'].mean()
for i, g in enumerate(groups):
    ax.scatter(i, means[g], marker='D', s=55, color='gold',
               edgecolor='black', linewidth=0.8, zorder=5)
ax.set_xlabel('Group'); ax.set_ylabel('Value')
panel(ax, 'd', 'Violin + box + strip + mean')

plt.show()

```

```
def create_density_boxplot(sheet_name, data, color):
    """
    Create a combined plot of kernel density curve and horizontal box plot
    """
#-------data------------
    # Extract impact strength data, removing possible NaN values
    impact_strength = data['Impact Strength'].dropna()
  
    # Compute kernel density estimation
    kde = gaussian_kde(impact_strength)
    x_range = np.linspace(impact_strength.min() * 0.9, impact_strength.max() * 1.1, 1000)
    density = kde(x_range)
  

#--------draw----------
    # Create figure
    fig, ax = plt.subplots(figsize=(10, 6))
    # Draw kernel density curve
    ax.plot(x_range, density, color=color, linewidth=4.5, label=f'{sheet_name} Dataset')
 
    # Create second y-axis for box plot (positioned near y=0)
    ax2 = ax.twinx()
  
    # Draw horizontal box plot, positioned at y=0
    bp = ax2.boxplot(impact_strength, vert=False, positions=[0], 
                     widths=0.1 * max(density), patch_artist=True,
                     boxprops=dict(facecolor=color, alpha=0.7, edgecolor='black', linewidth=1.2),
                     medianprops=dict(color='black', linewidth=1.5),
                     whiskerprops=dict(color='black', linewidth=1.2),
                     capprops=dict(color='black', linewidth=1.2),
                     flierprops=dict(marker='o', markerfacecolor=color, markersize=4, alpha=0.6))
  
    # Set range and labels for second y-axis
    ax2.set_ylim(-0.05 * max(density), 0.15 * max(density))
    ax2.set_yticks([0])
    ax2.set_yticklabels([f'{sheet_name}'], fontsize=12, fontweight='bold')
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['left'].set_visible(False)
  
    # Set main axes
    ax.set_xlabel('Impact Strength (kJ・m⁻²)', fontsize=14, fontweight='bold')
    ax.set_ylabel('Kernel Density', fontsize=16, fontweight='bold')
  
    # ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.8)
  
    # Set title
    # title = f'Kernel Density Estimation and Distribution of Impact Strength\\nfor {sheet_name} Augmented Dataset'
    # ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
  
    ax.set_xlim(impact_strength.min() * 0.8, impact_strength.max() * 1.2)
    ax.set_ylim(0, max(density) * 1.15)
  
    # Add statistics info text box
    # stats_text = f'Sample Size: {len(impact_strength):,}\nMean: {impact_strength.mean():.3f}\nStd: {impact_strength.std():.3f}\nMin: {impact_strength.min():.3f}\nMax: {impact_strength.max():.3f}'
    # ax.text(0.02, 0.98, stats_text, transform=ax.transAxes, fontsize=14,
    #         verticalalignment='top',horizontalalignment='left', bbox=dict(boxstyle='round', facecolor='white', alpha=0.8, edgecolor=color))
  
    plt.tight_layout()
    plt.show()
  
    return filename

```

```
# Grouped box plot + significance bracket
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
