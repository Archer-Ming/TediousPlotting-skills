### 包含了一系列绘图的模板

#### 3D曲面图

```
#----------data------------
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  注册 3d 投影

x = np.linspace(-3, 3, 80); y = np.linspace(-3, 3, 80)
X, Y = np.meshgrid(x, y)
Z = (np.exp(-(X**2 + Y**2)/3) * np.cos(X*1.2)
     + 0.3*np.sin(Y*1.5)*np.exp(-(X**2 + Y**2)/8))

#-----------draw--------------
fig = plt.figure(figsize=(14, 6))

# (a) 3D 曲面
ax1 = fig.add_subplot(1, 2, 1, projection='3d')
surf = ax1.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none',
                        alpha=0.92, antialiased=True, rstride=2, cstride=2)
ax1.contour(X, Y, Z, zdir='z', offset=Z.min() - 0.2,
            cmap='viridis', alpha=0.7)
ax1.set_xlabel('X (mm)'); ax1.set_ylabel('Y (mm)'); ax1.set_zlabel('Stress (MPa)')
ax1.set_title('(a) 3D Stress Surface', loc='left', fontweight='bold', pad=10)
ax1.view_init(elev=28, azim=-55)
fig.colorbar(surf, ax=ax1, shrink=0.55, pad=0.1, label='σ (MPa)')

# (b) 2D 等高线
ax2 = fig.add_subplot(1, 2, 2)
cf = ax2.contourf(X, Y, Z, levels=18, cmap='viridis')
cs = ax2.contour(X, Y, Z, levels=10, colors='white', linewidths=0.6, alpha=0.85)
ax2.clabel(cs, inline=True, fontsize=8, fmt='%.2f')

# 标记极值点
yi, xi = np.unravel_index(np.argmax(Z), Z.shape)
ax2.plot(X[yi, xi], Y[yi, xi], 'r*', markersize=18,
         markeredgecolor='white', markeredgewidth=1.2,
         label=f'Max σ = {Z.max():.2f}')
yi, xi = np.unravel_index(np.argmin(Z), Z.shape)
ax2.plot(X[yi, xi], Y[yi, xi], 'bv', markersize=12,
         markeredgecolor='white', markeredgewidth=1.2,
         label=f'Min σ = {Z.min():.2f}')

ax2.set_xlabel('X (mm)', fontweight='bold')
ax2.set_ylabel('Y (mm)', fontweight='bold')
ax2.set_title('(b) 2D Contour Projection', loc='left', fontweight='bold')
ax2.legend(loc='upper right', frameon=True, framealpha=0.9)
ax2.set_aspect('equal')
fig.colorbar(cf, ax=ax2, shrink=0.8, pad=0.04, label='σ (MPa)')

fig.suptitle('Stress Field Visualization — Surface + Contour',
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.show()

```

#### Joy图

```
#-------------data-----------
groups = [f'Batch {i+1}' for i in range(8)]
rng = np.random.default_rng(9)
#-----------draw---------------
fig, ax = plt.subplots(figsize=(10, 7))
cmap = plt.cm.viridis
xs = np.linspace(20, 80, 400)
offset = 0
step = 1.0
for i, g in enumerate(groups):
    mu = 50 + (i - 3.5)*1.5
    sd = 6 + rng.uniform(-1, 1)
    data = rng.normal(mu, sd, 400)
    kde = gaussian_kde(data, bw_method=0.35)
    y = kde(xs); y = y / y.max() * 0.85
    c = cmap(i / (len(groups) - 1))
    ax.fill_between(xs, offset, offset + y, color=c, alpha=0.85,
                    edgecolor='white', linewidth=1)
    ax.plot(xs, offset + y, color='black', lw=0.6)
    ax.text(19.5, offset + 0.05, g, va='bottom', ha='right',
            fontsize=10, fontweight='bold')
    offset += step

ax.set_xlim(18, 82); ax.set_ylim(-0.1, offset + 0.2)
ax.set_yticks([])
ax.set_xlabel('Measured Value', fontweight='bold')
ax.set_title('Ridge Plot — Distribution Across Production Batches',
             fontweight='bold', pad=12)
for s in ['top', 'right', 'left']:
    ax.spines[s].set_visible(False)
ax.grid(axis='x', alpha=0.3, linestyle='--'); ax.set_axisbelow(True)
plt.tight_layout()
plt.show()

```

#### ROC曲线/混淆矩阵图

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
