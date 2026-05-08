## 包含了一系列绘图的模板

### 重要规则！

* 每个类型的模板第一部分代码呈现的是从简单到复杂的图表，你需要渐进的去学习这些模板。
* 每个类型的剩余部分模板代码为具体带有独特风格和设计的图表，你也要去学习这些模板。
* 参考模板里面的样例数据的x坐标，y坐标，数据标题名称，亦或是对数据的处理读取，请严格忽略！！！

#### 热力图

```
#-------------第一部分代码------------
#-----draw---------
fig = plt.figure(figsize=FIGSIZE)
gs = GridSpec(1, 4, figure=fig, wspace=0.55)
fig.suptitle('Fig 5. Heatmaps — simple to complex',
             fontsize=14, fontweight='bold', y=1.02)

feats = ['F1','F2','F3','F4','F5','F6']
n = len(feats)
M = rng.uniform(-1, 1, (n, n)); M = (M + M.T)/2; np.fill_diagonal(M, 1)
df_corr = pd.DataFrame(M, index=feats, columns=feats)

# (a) basic heatmap
ax = fig.add_subplot(gs[0])
sns.heatmap(df_corr, cmap='RdBu_r', center=0, vmin=-1, vmax=1,
            ax=ax, square=True, cbar_kws={'shrink': 0.8})
ax.set_title('(a) Basic heatmap', loc='left', fontweight='bold', fontsize=10.5, pad=8)

# (b) annotated, masked upper triangle
ax = fig.add_subplot(gs[1])
mask = np.triu(np.ones_like(df_corr, dtype=bool), k=1)
sns.heatmap(df_corr, mask=mask, annot=True, fmt='.2f',
            cmap='RdBu_r', center=0, vmin=-1, vmax=1,
            ax=ax, square=True, linewidths=0.5,
            cbar_kws={'shrink': 0.8}, annot_kws={'fontsize': 8})
ax.set_title('(b) Annotated + masked', loc='left',
             fontweight='bold', fontsize=10.5, pad=8)

# (c) clustered heatmap (manual reorder by hierarchical clustering)
ax = fig.add_subplot(gs[2])
from scipy.cluster.hierarchy import linkage, leaves_list
link = linkage(df_corr.values, method='average')
order = leaves_list(link)
df_c = df_corr.iloc[order, :].iloc[:, order]
sns.heatmap(df_c, cmap='RdBu_r', center=0, vmin=-1, vmax=1,
            annot=True, fmt='.2f', ax=ax, square=True,
            linewidths=0.5, cbar_kws={'shrink': 0.8},
            annot_kws={'fontsize': 8})
ax.set_title('(c) Clustered (re-ordered)', loc='left',
             fontweight='bold', fontsize=10.5, pad=8)

# (d) bubble heatmap (size + color)
ax = fig.add_subplot(gs[3])
norm = Normalize(-1, 1); cmap = plt.cm.RdBu_r
for i in range(n):
    for j in range(n):
        v = df_corr.iloc[i, j]
        ax.scatter(j, n-1-i, s=abs(v)*900 + 30,
                   c=[cmap(norm(v))], edgecolor='black',
                   linewidth=0.6, alpha=0.9)
        if abs(v) > 0.4:
            ax.text(j, n-1-i, f'{v:.2f}', ha='center', va='center',
                    fontsize=7, color='white' if abs(v) > 0.6 else 'black')
ax.set_xticks(range(n)); ax.set_yticks(range(n))
ax.set_xticklabels(feats); ax.set_yticklabels(feats[::-1])
ax.set_xlim(-0.6, n-0.4); ax.set_ylim(-0.6, n-0.4)
ax.set_aspect('equal'); ax.grid(alpha=0.25, ls=':')
ax.set_axisbelow(True)
sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap); sm.set_array([])
fig.colorbar(sm, ax=ax, shrink=0.8, pad=0.05)
ax.set_title('(d) Bubble heatmap', loc='left',
             fontweight='bold', fontsize=10.5, pad=8)

plt.show()

```

```
#下三角掩码热力图
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
#气泡图
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

```
#非对称相关矩阵（上气泡 / 下数值）
#---------------data-----------
features = ['Strength', 'Modulus', 'Toughness', 'Hardness', 'Density', 'Strain']
n = len(features)
rng = np.random.default_rng(7)
A = rng.uniform(-1, 1, (n, n))
M = (A + A.T) / 2
np.fill_diagonal(M, 1.0)
df_corr = pd.DataFrame(M, index=features, columns=features)
#-----------draw-----------
fig, ax = plt.subplots(figsize=(8.5, 7.5))
vmin, vmax = -1, 1
cmap = plt.cm.RdBu_r
norm = plt.Normalize(vmin, vmax)

for i in range(n):
    for j in range(n):
        v = df_corr.iloc[i, j]
        if j > i:                           # 上三角：气泡
            ax.scatter(j, n-1-i, s=abs(v)*1400 + 50, c=[cmap(norm(v))],
                       edgecolor='black', linewidth=0.8, alpha=0.92)
        elif j < i:                         # 下三角：数值 + 淡色背景
            ax.add_patch(plt.Rectangle((j-0.45, n-1-i-0.45), 0.9, 0.9,
                                       facecolor=cmap(norm(v)), alpha=0.35,
                                       edgecolor='white', linewidth=1))
            ax.text(j, n-1-i, f'{v:.2f}', ha='center', va='center',
                    fontsize=11, fontweight='bold',
                    color='black' if abs(v) < 0.6 else 'white')
        else:                               # 对角线：变量名
            ax.add_patch(plt.Rectangle((j-0.45, n-1-i-0.45), 0.9, 0.9,
                                       facecolor='#2c3e50', edgecolor='white'))
            ax.text(j, n-1-i, features[i], ha='center', va='center',
                    fontsize=10, fontweight='bold', color='white', rotation=45)

ax.set_xticks(range(n)); ax.set_yticks(range(n))
ax.set_xticklabels(features, rotation=45, ha='right')
ax.set_yticklabels(features[::-1])
ax.set_xlim(-0.6, n-0.4); ax.set_ylim(-0.6, n-0.4)
ax.set_aspect('equal'); ax.grid(alpha=0.25, linestyle=':')
ax.set_axisbelow(True)
for s in ['top', 'right']:
    ax.spines[s].set_visible(False)

sm = plt.cm.ScalarMappable(norm=norm, cmap=cmap); sm.set_array([])
cbar = fig.colorbar(sm, ax=ax, shrink=0.75, pad=0.04)
cbar.set_label('Pearson Correlation', fontweight='bold')

ax.set_title('Feature Correlation Matrix\n'
             '(upper-right: bubbles by |r|;  lower-left: values)',
             fontweight='bold', pad=14)
plt.tight_layout()
plt.show()

```

#### 直方图，密度曲线图

```
#---------第一部分代码---------
#-----draw------
fig = plt.figure(figsize=FIGSIZE)
gs = GridSpec(1, 4, figure=fig, wspace=0.30)
fig.suptitle('Fig 6. Histogram / Density — simple to complex',
             fontsize=14, fontweight='bold', y=1.02)

data1 = rng.normal(50, 8, 800)
data2 = rng.normal(65, 10, 800)
bimodal = np.concatenate([rng.normal(45, 5, 400), rng.normal(70, 6, 400)])

# (a) basic histogram
ax = fig.add_subplot(gs[0])
ax.hist(data1, bins=30, color=C[0], edgecolor='white', alpha=0.85)
ax.set_xlabel('Value'); ax.set_ylabel('Count')
panel(ax, 'a', 'Basic histogram')

# (b) overlapping + KDE
ax = fig.add_subplot(gs[1])
ax.hist(data1, bins=30, density=True, color=C[0], alpha=0.55,
        edgecolor='white', label='A')
ax.hist(data2, bins=30, density=True, color=C[2], alpha=0.55,
        edgecolor='white', label='B')
xs = np.linspace(20, 100, 200)
ax.plot(xs, gaussian_kde(data1)(xs), color=C[0], lw=2)
ax.plot(xs, gaussian_kde(data2)(xs), color=C[2], lw=2)
ax.set_xlabel('Value'); ax.set_ylabel('Density')
ax.legend(frameon=False)
panel(ax, 'b', 'Overlap + KDE overlay')

# (c) bimodal + ECDF inset
ax = fig.add_subplot(gs[2])
ax.hist(bimodal, bins=40, density=True, color=C[1], alpha=0.6,
        edgecolor='white')
xs = np.linspace(bimodal.min(), bimodal.max(), 300)
ax.plot(xs, gaussian_kde(bimodal)(xs), color=C[3], lw=2.2, label='KDE')
ax.axvline(bimodal.mean(), color='black', ls='--', lw=1,
           label=f'μ = {bimodal.mean():.1f}')
ax.axvline(np.median(bimodal), color='gray', ls=':', lw=1,
           label=f'median = {np.median(bimodal):.1f}')
ax.set_xlabel('Value'); ax.set_ylabel('Density')
# inset: ECDF
inset = ax.inset_axes([0.62, 0.55, 0.36, 0.40])
sorted_d = np.sort(bimodal)
ecdf = np.arange(1, len(sorted_d)+1)/len(sorted_d)
inset.plot(sorted_d, ecdf, color=C[1], lw=1.5)
inset.set_title('ECDF', fontsize=8); inset.tick_params(labelsize=7)
inset.grid(alpha=0.3)
ax.legend(frameon=False, loc='upper left', fontsize=7)
panel(ax, 'c', 'Bimodal + ECDF inset')

# (d) ridge plot (multiple groups stacked KDE)
ax = fig.add_subplot(gs[3])
n_groups = 6
cmap = plt.cm.viridis
xs = np.linspace(20, 90, 300)
offset = 0; step = 0.9
for i in range(n_groups):
    d = rng.normal(40 + i*5, 6, 300)
    y = gaussian_kde(d, bw_method=0.35)(xs)
    y = y/y.max() * 0.85
    col = cmap(i/(n_groups-1))
    ax.fill_between(xs, offset, offset + y, color=col, alpha=0.85,
                    edgecolor='white', linewidth=0.8)
    ax.plot(xs, offset + y, color='black', lw=0.5)
    ax.text(19, offset + 0.05, f'Batch {i+1}',
            ha='right', va='bottom', fontsize=8, fontweight='bold')
    offset += step
ax.set_xlim(15, 92); ax.set_yticks([])
ax.set_xlabel('Value')
for s in ['top','right','left']: ax.spines[s].set_visible(False)
ax.set_title('(d) Ridge / Joy plot', loc='left',
             fontweight='bold', fontsize=10.5, pad=8)
ax.grid(axis='x', alpha=0.3, ls='--'); ax.set_axisbelow(True)

plt.show()

```

```
#-----------data-------------
rng = np.random.default_rng(11)
classes = ['Class A', 'Class B', 'Class C', 'Class D']
cm = np.array([[78, 4, 2, 1],
               [3, 85, 5, 2],
               [2, 6, 72, 8],
               [1, 3, 7, 81]])
cm_norm = cm / cm.sum(axis=1, keepdims=True)
#----------draw--------------------
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# (a) 混淆矩阵
ax = axes[0]
sns.heatmap(cm_norm, annot=cm, fmt='d', cmap='Blues',
            xticklabels=classes, yticklabels=classes,
            square=True, linewidths=1, linecolor='white',
            cbar_kws={'label': 'Proportion'}, ax=ax,
            annot_kws={'fontsize': 12, 'fontweight': 'bold'})
ax.set_xlabel('Predicted Label', fontweight='bold')
ax.set_ylabel('True Label', fontweight='bold')
ax.set_title('(a) Confusion Matrix (count + normalized)',
             loc='left', fontweight='bold')
# 红框高亮对角线
for i in range(len(classes)):
    ax.add_patch(plt.Rectangle((i, i), 1, 1, fill=False,
                               edgecolor='#C73E1D', lw=2.2))

# (b) ROC 曲线
ax = axes[1]
fpr_grid = np.linspace(0, 1, 100)
aucs = [0.94, 0.91, 0.87, 0.92]
for i, (cls, auc) in enumerate(zip(classes, aucs)):
    tpr = 1 - (1 - fpr_grid)**(1/(1-auc + 0.1)*0.5)
    tpr = np.clip(tpr + rng.normal(0, 0.01, len(tpr)), 0, 1)
    tpr[0] = 0; tpr[-1] = 1
    ax.plot(fpr_grid, tpr, color=SCI_COLORS[i], lw=2.2,
            label=f'{cls} (AUC = {auc:.2f})')
    ax.fill_between(fpr_grid, tpr, alpha=0.10, color=SCI_COLORS[i])
ax.plot([0, 1], [0, 1], '--', color='gray', lw=1)
ax.set_xlabel('False Positive Rate', fontweight='bold')
ax.set_ylabel('True Positive Rate', fontweight='bold')
ax.set_title('(b) ROC Curves (one-vs-rest)', loc='left', fontweight='bold')
ax.legend(loc='lower right', frameon=True, framealpha=0.95)
ax.grid(alpha=0.3, linestyle='--'); ax.set_axisbelow(True)
ax.set_xlim(-0.01, 1.01); ax.set_ylim(-0.01, 1.02)

fig.suptitle('Classification Diagnostics', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()
```

#### 饼图

```
#----------------第一部分代码-------------
#------draw-------
fig = plt.figure(figsize=FIGSIZE)
gs = GridSpec(1, 4, figure=fig, wspace=0.30)
fig.suptitle('Fig 7. Pie / Donut Charts — simple to complex',
             fontsize=14, fontweight='bold', y=1.02)

sizes = [38, 27, 18, 12, 5]
labels = ['α','β','γ','δ','Other']

# (a) basic pie
ax = fig.add_subplot(gs[0])
ax.pie(sizes, labels=labels, colors=C[:5], autopct='%1.1f%%',
       startangle=90, textprops={'fontsize': 9})
ax.set_title('(a) Basic pie', loc='left', fontweight='bold', fontsize=10.5, pad=8)

# (b) exploded + shadow + custom autopct
ax = fig.add_subplot(gs[1])
explode = [0.08 if s == max(sizes) else 0 for s in sizes]
ax.pie(sizes, labels=labels, colors=C[:5], explode=explode,
       autopct=lambda p: f'{p:.1f}%\n({int(p*sum(sizes)/100)})',
       startangle=90, shadow=True,
       wedgeprops=dict(edgecolor='white', linewidth=1.5),
       textprops={'fontsize': 8})
ax.set_title('(b) Exploded + shadow', loc='left',
             fontweight='bold', fontsize=10.5, pad=8)

# (c) donut with center text
ax = fig.add_subplot(gs[2])
w, t, at = ax.pie(sizes, labels=labels, colors=C[:5],
                  autopct='%1.1f%%', startangle=90,
                  pctdistance=0.78,
                  wedgeprops=dict(width=0.42, edgecolor='white', linewidth=2),
                  textprops={'fontsize': 9})
for a in at:
    a.set_color('white'); a.set_fontweight('bold')
ax.text(0, 0, f'Total\n{sum(sizes)}', ha='center', va='center',
        fontsize=13, fontweight='bold')
ax.set_title('(c) Donut + center label', loc='left',
             fontweight='bold', fontsize=10.5, pad=8)

# (d) nested donut (outer category, inner sub-category)
ax = fig.add_subplot(gs[3])
outer = [40, 35, 25]
outer_lbls = ['Cat I', 'Cat II', 'Cat III']
inner = [25, 15, 20, 15, 12, 13]
inner_lbls = ['I-a','I-b','II-a','II-b','III-a','III-b']
outer_colors = [C[0], C[1], C[2]]
inner_colors = [to_rgba(C[0], 0.6), to_rgba(C[0], 0.35),
                to_rgba(C[1], 0.6), to_rgba(C[1], 0.35),
                to_rgba(C[2], 0.6), to_rgba(C[2], 0.35)]
ax.pie(outer, radius=1.0, colors=outer_colors,
       labels=outer_lbls, labeldistance=1.08,
       wedgeprops=dict(width=0.32, edgecolor='white', linewidth=2),
       textprops={'fontsize': 9, 'fontweight': 'bold'})
ax.pie(inner, radius=0.68, colors=inner_colors,
       labels=inner_lbls, labeldistance=0.78,
       wedgeprops=dict(width=0.32, edgecolor='white', linewidth=1.5),
       textprops={'fontsize': 7})
ax.set_title('(d) Nested (sunburst-like)', loc='left',
             fontweight='bold', fontsize=10.5, pad=8)

plt.show()

```

#### 雷达图

```
#-----------第一部分代码-----------
#-------draw------
fig = plt.figure(figsize=FIGSIZE)
gs = GridSpec(1, 4, figure=fig, wspace=0.40)
fig.suptitle('Fig 8. Radar / Polar Charts — simple to complex',
             fontsize=14, fontweight='bold', y=1.02)

cats = ['Acc','Speed','Robust','Interp','Memory','Gen']
N = len(cats)
angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
angles_c = angles + angles[:1]

# (a) single
ax = fig.add_subplot(gs[0], projection='polar')
vals = [0.85, 0.7, 0.88, 0.8, 0.65, 0.78] + [0.85]
ax.plot(angles_c, vals, color=C[0], lw=2, marker='o')
ax.fill(angles_c, vals, color=C[0], alpha=0.25)
ax.set_xticks(angles); ax.set_xticklabels(cats, fontsize=8)
ax.set_ylim(0, 1); ax.set_yticks([0.25, 0.5, 0.75, 1])
ax.set_yticklabels(['0.25','0.5','0.75','1'], fontsize=7)
ax.set_theta_offset(np.pi/2); ax.set_theta_direction(-1)
ax.set_title('(a) Single model', loc='left',
             fontweight='bold', fontsize=10.5, pad=18)

# (b) multi-overlay
ax = fig.add_subplot(gs[1], projection='polar')
models = {'RF':[0.85,0.7,0.88,0.8,0.65,0.78],
          'XGB':[0.91,0.85,0.85,0.55,0.75,0.82],
          'NN':[0.93,0.4,0.7,0.3,0.45,0.88]}
for i, (n, v) in enumerate(models.items()):
    v_ = v + v[:1]
    ax.plot(angles_c, v_, color=C[i], lw=1.8, marker='o', ms=4, label=n)
    ax.fill(angles_c, v_, color=C[i], alpha=0.13)
ax.set_xticks(angles); ax.set_xticklabels(cats, fontsize=8)
ax.set_ylim(0, 1); ax.set_yticks([0.25, 0.5, 0.75, 1])
ax.set_yticklabels(['0.25','0.5','0.75','1'], fontsize=7)
ax.set_theta_offset(np.pi/2); ax.set_theta_direction(-1)
ax.legend(loc='upper right', bbox_to_anchor=(1.25, 1.10), fontsize=7)
ax.set_title('(b) Multi-model overlay', loc='left',
             fontweight='bold', fontsize=10.5, pad=18)

# (c) polar bar (rose chart)
ax = fig.add_subplot(gs[2], projection='polar')
n = 16
theta = np.linspace(0, 2*np.pi, n, endpoint=False)
r = rng.uniform(0.3, 1, n)
ax.bar(theta, r, width=2*np.pi/n*0.9, bottom=0.05,
       color=plt.cm.plasma(r/r.max()), edgecolor='white', linewidth=1)
ax.set_xticks(theta[::2])
ax.set_xticklabels([f'{int(np.degrees(a))}°' for a in theta[::2]], fontsize=7)
ax.set_yticklabels([])
ax.set_title('(c) Polar bar / rose chart', loc='left',
             fontweight='bold', fontsize=10.5, pad=18)

# (d) wind-rose / dual-layer polar
ax = fig.add_subplot(gs[3], projection='polar')
n = 12
theta = np.linspace(0, 2*np.pi, n, endpoint=False)
layer1 = rng.uniform(0.2, 0.5, n)
layer2 = rng.uniform(0.1, 0.4, n)
layer3 = rng.uniform(0.05, 0.3, n)
w = 2*np.pi/n*0.85
ax.bar(theta, layer1, width=w, color=C[0], edgecolor='white',
       linewidth=0.8, label='0–5 m/s')
ax.bar(theta, layer2, width=w, bottom=layer1, color=C[2],
       edgecolor='white', linewidth=0.8, label='5–10 m/s')
ax.bar(theta, layer3, width=w, bottom=layer1+layer2, color=C[3],
       edgecolor='white', linewidth=0.8, label='>10 m/s')
ax.set_xticks(theta)
dirs = ['N','NNE','NE','ENE','E','ESE','SE','SSE','S','SSW','SW','WSW']
ax.set_xticklabels(dirs, fontsize=7)
ax.set_theta_zero_location('N'); ax.set_theta_direction(-1)
ax.set_yticks([0.3, 0.6, 0.9])
ax.set_yticklabels(['0.3','0.6','0.9'], fontsize=6)
ax.legend(loc='upper right', bbox_to_anchor=(1.30, 1.10), fontsize=7)
ax.set_title('(d) Wind rose (stacked polar)', loc='left',
             fontweight='bold', fontsize=10.5, pad=18)

plt.show()

```
