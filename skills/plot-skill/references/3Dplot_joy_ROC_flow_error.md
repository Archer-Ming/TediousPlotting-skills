Contains a series of plotting templates

### Important Rules!

* The first part of the code in each type of template presents charts from simple to complex. You need to learn these templates progressively.
* The remaining template code in each type contains charts with specific unique styles and designs. You should also learn these templates.
* For the x-coordinates, y-coordinates, data title names in the sample data of the reference templates, or the data processing/reading, please strictly ignore them!!!

#### 3D Surface Plot

```
#----------Part One Code--------
#----draw-----
from mpl_toolkits.mplot3d import Axes3D  # noqa
fig = plt.figure(figsize=FIGSIZE)
fig.suptitle('Fig 9. 3D Plots — simple to complex',
             fontsize=14, fontweight='bold', y=1.02)

# (a) 3D scatter
ax = fig.add_subplot(1, 4, 1, projection='3d')
n = 200
x, y, z = rng.normal(0, 1, n), rng.normal(0, 1, n), rng.normal(0, 1, n)
ax.scatter(x, y, z, c=z, cmap='viridis', s=22, alpha=0.7,
           edgecolor='white', linewidths=0.3)
ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Z')
ax.set_title('(a) 3D scatter', fontweight='bold', fontsize=10.5, loc='left')

# (b) 3D surface
ax = fig.add_subplot(1, 4, 2, projection='3d')
X, Y = np.meshgrid(np.linspace(-3, 3, 50), np.linspace(-3, 3, 50))
Z = np.exp(-(X**2 + Y**2)/3) * np.cos(X*1.2)
surf = ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none',
                        alpha=0.9, antialiased=True)
ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Z')
ax.set_title('(b) Surface', fontweight='bold', fontsize=10.5, loc='left')

# (c) wireframe + contour projection
ax = fig.add_subplot(1, 4, 3, projection='3d')
ax.plot_wireframe(X, Y, Z, color=C[0], linewidth=0.5, alpha=0.7,
                  rstride=3, cstride=3)
ax.contour(X, Y, Z, zdir='z', offset=Z.min()-0.5, cmap='viridis', alpha=0.8)
ax.contour(X, Y, Z, zdir='x', offset=-3.5, cmap='plasma', alpha=0.5)
ax.set_zlim(Z.min()-0.5, Z.max()+0.1)
ax.set_xlim(-3.5, 3); ax.set_ylim(-3, 3)
ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Z')
ax.set_title('(c) Wireframe + projections',
             fontweight='bold', fontsize=10.5, loc='left')

# (d) mixed: surface + scatter + critical points
ax = fig.add_subplot(1, 4, 4, projection='3d')
ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none',
                alpha=0.55, antialiased=True)
# Sampled points "above" surface
n = 35
sx = rng.uniform(-3, 3, n); sy = rng.uniform(-3, 3, n)
sz_surface = np.exp(-(sx**2 + sy**2)/3) * np.cos(sx*1.2)
sz = sz_surface + rng.normal(0, 0.15, n)
ax.scatter(sx, sy, sz, c=C[3], s=30, alpha=0.95,
           edgecolor='white', linewidths=0.5, zorder=5, label='Samples')
# mark global max
yi, xi = np.unravel_index(np.argmax(Z), Z.shape)
ax.scatter([X[yi,xi]], [Y[yi,xi]], [Z[yi,xi]+0.05],
           c='gold', s=180, marker='*',
           edgecolor='black', linewidths=1, zorder=10,
           label=f'Max = {Z.max():.2f}')
ax.contour(X, Y, Z, zdir='z', offset=Z.min()-0.4,
           cmap='viridis', alpha=0.6)
ax.set_zlim(Z.min()-0.4, Z.max()+0.3)
ax.legend(loc='upper left', fontsize=7)
ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_zlabel('Z')
ax.set_title('(d) Surface + samples + critical pts',
             fontweight='bold', fontsize=10.5, loc='left')

plt.tight_layout()
plt.show()

```

```
#----------data------------
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  register 3d projection

x = np.linspace(-3, 3, 80); y = np.linspace(-3, 3, 80)
X, Y = np.meshgrid(x, y)
Z = (np.exp(-(X**2 + Y**2)/3) * np.cos(X*1.2)
     + 0.3*np.sin(Y*1.5)*np.exp(-(X**2 + Y**2)/8))

#-----------draw--------------
fig = plt.figure(figsize=(14, 6))

# (a) 3D surface
ax1 = fig.add_subplot(1, 2, 1, projection='3d')
surf = ax1.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none',
                        alpha=0.92, antialiased=True, rstride=2, cstride=2)
ax1.contour(X, Y, Z, zdir='z', offset=Z.min() - 0.2,
            cmap='viridis', alpha=0.7)
ax1.set_xlabel('X (mm)'); ax1.set_ylabel('Y (mm)'); ax1.set_zlabel('Stress (MPa)')
ax1.set_title('(a) 3D Stress Surface', loc='left', fontweight='bold', pad=10)
ax1.view_init(elev=28, azim=-55)
fig.colorbar(surf, ax=ax1, shrink=0.55, pad=0.1, label='σ (MPa)')

# (b) 2D contour
ax2 = fig.add_subplot(1, 2, 2)
cf = ax2.contourf(X, Y, Z, levels=18, cmap='viridis')
cs = ax2.contour(X, Y, Z, levels=10, colors='white', linewidths=0.6, alpha=0.85)
ax2.clabel(cs, inline=True, fontsize=8, fmt='%.2f')

# Mark extreme points
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

#### Field Plot

```
#----------Part One Code----------
#------draw-------
fig = plt.figure(figsize=FIGSIZE)
gs = GridSpec(1, 4, figure=fig, wspace=0.32)
fig.suptitle('Fig 10. Contour & Field Plots — simple to complex',
             fontsize=14, fontweight='bold', y=1.02)

X, Y = np.meshgrid(np.linspace(-3, 3, 80), np.linspace(-3, 3, 80))
Z = np.exp(-(X**2 + Y**2)/3) * np.cos(X*1.2) + 0.3*np.sin(Y*1.5)*np.exp(-(X**2+Y**2)/8)

# (a) basic contour
ax = fig.add_subplot(gs[0])
cs = ax.contour(X, Y, Z, levels=10, cmap='viridis')
ax.clabel(cs, inline=True, fontsize=7, fmt='%.2f')
ax.set_xlabel('X'); ax.set_ylabel('Y')
ax.set_aspect('equal')
panel(ax, 'a', 'Basic contour lines')

# (b) filled contour + overlay lines
ax = fig.add_subplot(gs[1])
cf = ax.contourf(X, Y, Z, levels=20, cmap='viridis')
ax.contour(X, Y, Z, levels=10, colors='white',
           linewidths=0.6, alpha=0.8)
fig.colorbar(cf, ax=ax, shrink=0.85, pad=0.02)
ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_aspect('equal')
panel(ax, 'b', 'Filled + line overlay')

# (c) 2D KDE from samples
ax = fig.add_subplot(gs[2])
n = 500
sx = np.concatenate([rng.normal(-1, 0.6, n//2), rng.normal(1.2, 0.5, n//2)])
sy = np.concatenate([rng.normal(-0.5, 0.7, n//2), rng.normal(1, 0.6, n//2)])
sns.kdeplot(x=sx, y=sy, ax=ax, cmap='RdPu', fill=True, levels=12, alpha=0.9)
ax.scatter(sx, sy, s=4, color='white', alpha=0.5,
           edgecolor='black', linewidths=0.2)
ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_aspect('equal')
panel(ax, 'c', '2D KDE + samples')

# (d) streamplot + magnitude colormap (vector field)
ax = fig.add_subplot(gs[3])
Y2, X2 = np.mgrid[-3:3:60j, -3:3:60j]
U = -1 - X2**2 + Y2; V = 1 + X2 - Y2**2
speed = np.sqrt(U**2 + V**2)
strm = ax.streamplot(X2, Y2, U, V, color=speed, cmap='plasma',
                     linewidth=1.2, density=1.5, arrowsize=1.2)
fig.colorbar(strm.lines, ax=ax, shrink=0.85, pad=0.02, label='|v|')
ax.set_xlabel('X'); ax.set_ylabel('Y'); ax.set_aspect('equal')
panel(ax, 'd', 'Vector field (streamplot)')

plt.show()

```

#### Joy Plot

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

#### ROC Curve / Confusion Matrix Plot

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

# (a) Confusion matrix
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
# Highlight diagonal with red boxes
for i in range(len(classes)):
    ax.add_patch(plt.Rectangle((i, i), 1, 1, fill=False,
                               edgecolor='#C73E1D', lw=2.2))

# (b) ROC curves
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

#### Error & Uncertainty Plot

```
#-----------Part One Code---------
#---draw----
fig = plt.figure(figsize=FIGSIZE)
gs = GridSpec(1, 4, figure=fig, wspace=0.34)
fig.suptitle('Fig 11. Error & Uncertainty — simple to complex',
             fontsize=14, fontweight='bold', y=1.02)

# (a) bar with error bars
ax = fig.add_subplot(gs[0])
cats = ['A','B','C','D','E']
vals = rng.uniform(40, 80, 5)
err = rng.uniform(3, 8, 5)
ax.bar(cats, vals, yerr=err, color=C[0], edgecolor='black',
       capsize=6, ecolor='black', linewidth=0.7, alpha=0.9,
       error_kw={'lw': 1.2, 'capthick': 1.2})
ax.set_ylabel('Value'); ax.set_xlabel('Category')
panel(ax, 'a', 'Bar + std error')

# (b) forest plot (effect sizes with CI)
ax = fig.add_subplot(gs[1])
studies = [f'Study {i+1}' for i in range(7)]
eff = rng.normal(0.3, 0.4, 7)
ci_lo = eff - rng.uniform(0.1, 0.4, 7)
ci_hi = eff + rng.uniform(0.1, 0.4, 7)
weights = rng.uniform(30, 200, 7)
y = np.arange(len(studies))
ax.errorbar(eff, y, xerr=[eff-ci_lo, ci_hi-eff], fmt='none',
            color='black', capsize=4, lw=1.2)
ax.scatter(eff, y, s=weights, color=C[0], edgecolor='black',
           linewidth=0.8, alpha=0.85, zorder=5)
ax.axvline(0, color='gray', ls='--', lw=0.8)
# pooled diamond
pooled = np.average(eff, weights=weights)
ax.scatter(pooled, -1, marker='D', s=200, color=C[3],
           edgecolor='black', linewidth=1, zorder=6)
ax.text(pooled, -1, 'Pooled', va='center', ha='center',
        fontsize=7, color='white', fontweight='bold')
ax.set_yticks(list(y) + [-1])
ax.set_yticklabels(studies + ['Pooled'])
ax.set_xlabel('Effect size')
ax.set_ylim(-1.8, len(studies))
panel(ax, 'b', 'Forest plot (meta-analysis)')

# (c) Bland-Altman
ax = fig.add_subplot(gs[2])
n = 100
m1 = rng.normal(50, 8, n)
m2 = m1 + rng.normal(0.5, 2, n)
means = (m1 + m2)/2; diffs = m1 - m2
md = diffs.mean(); sd = diffs.std()
ax.scatter(means, diffs, s=30, color=C[0], alpha=0.6,
           edgecolor='white', linewidths=0.4)
ax.axhline(md, color=C[3], lw=1.5, label=f'mean = {md:.2f}')
ax.axhline(md + 1.96*sd, color='gray', ls='--', lw=1,
           label=f'+1.96 SD = {md+1.96*sd:.2f}')
ax.axhline(md - 1.96*sd, color='gray', ls='--', lw=1,
           label=f'−1.96 SD = {md-1.96*sd:.2f}')
ax.fill_between(ax.get_xlim(), md+1.96*sd, md-1.96*sd, color='gray', alpha=0.05)
ax.set_xlabel('Mean of methods'); ax.set_ylabel('Difference')
ax.legend(frameon=True, framealpha=0.95, fontsize=7, loc='lower right')
ymin, ymax = diffs.min(), diffs.max()
ypad = (ymax - ymin) * 0.30
ax.set_ylim(ymin - ypad, ymax + ypad)
panel(ax, 'c', 'Bland–Altman agreement')

# (d) bootstrap distribution + CI band on regression
ax = fig.add_subplot(gs[3])
n = 60
x = np.linspace(0, 10, n)
y = 1.5*x + 2 + rng.normal(0, 2, n)
# bootstrap regression lines
n_boot = 200
xfit = np.linspace(0, 10, 50)
yfits = []
for _ in range(n_boot):
    idx = rng.integers(0, n, n)
    m, b = np.polyfit(x[idx], y[idx], 1)
    yfits.append(m*xfit + b)
yfits = np.array(yfits)
lo, hi = np.percentile(yfits, [2.5, 97.5], axis=0)
med = np.median(yfits, axis=0)
# plot some translucent bootstrap lines
for yf in yfits[::10]:
    ax.plot(xfit, yf, color=C[0], alpha=0.05, lw=0.8)
ax.fill_between(xfit, lo, hi, color=C[0], alpha=0.25, label='95% bootstrap CI')
ax.plot(xfit, med, color=C[3], lw=2, label='Median fit')
ax.scatter(x, y, s=28, color=C[0], alpha=0.7,
           edgecolor='white', linewidths=0.4, zorder=5)
ax.legend(frameon=False, loc='upper left', fontsize=8)
ax.set_xlabel('X'); ax.set_ylabel('Y')
panel(ax, 'd', 'Bootstrap regression CI')

plt.show()

```

#### Flow & Relationship Diagrams

```
#---------Part One Code--------
#------draw-----
fig = plt.figure(figsize=FIGSIZE)
gs = GridSpec(1, 4, figure=fig, wspace=0.30)
fig.suptitle('Fig 13. Flow & Relationship Diagrams',
             fontsize=14, fontweight='bold', y=1.02)

# (a) Sankey-like: 2-stage flow with rectangles + smooth curves
ax = fig.add_subplot(gs[0])
sources = ['S1', 'S2', 'S3']
targets = ['T1', 'T2']
flows = np.array([[0.10, 0.06],   # S1 -> T1, T2
                  [0.16, 0.12],   # S2 -> ...
                  [0.05, 0.11]])  # S3 -> ...

src_h = flows.sum(axis=1)         # source heights
tgt_h = flows.sum(axis=0)         # target heights
gap = 0.04
src_y_top = np.cumsum(np.concatenate([[0], src_h[:-1] + gap]))   # top of each block
tgt_y_top = np.cumsum(np.concatenate([[0], tgt_h[:-1] + gap]))
src_y_top = src_y_top[::-1]  # show top-down
# Recompute so sum aligns; simpler: place blocks from top
cur = 0
src_top = []
for h in src_h:
    src_top.append(cur); cur += h + gap
cur = 0
tgt_top = []
for h in tgt_h:
    tgt_top.append(cur); cur += h + gap

# Shift so vertical centers align
src_total = sum(src_h) + gap*(len(src_h)-1)
tgt_total = sum(tgt_h) + gap*(len(tgt_h)-1)
total = max(src_total, tgt_total)
src_top = [t + (total - src_total)/2 for t in src_top]
tgt_top = [t + (total - tgt_total)/2 for t in tgt_top]

# Draw source / target blocks
for i, (s, top, h) in enumerate(zip(sources, src_top, src_h)):
    ax.add_patch(Rectangle((0, top), 0.04, h, color=C[i], alpha=0.9))
    ax.text(-0.02, top + h/2, s, ha='right', va='center',
            fontsize=9, fontweight='bold')
for j, (t_, top, h) in enumerate(zip(targets, tgt_top, tgt_h)):
    ax.add_patch(Rectangle((0.96, top), 0.04, h, color=C[j+5], alpha=0.9))
    ax.text(1.02, top + h/2, t_, ha='left', va='center',
            fontsize=9, fontweight='bold')

# Sigmoid curves between blocks
src_used = [0]*len(sources); tgt_used = [0]*len(targets)
xs = np.linspace(0.04, 0.96, 80)
sig = (1 - np.cos(np.pi * (xs - 0.04)/0.92)) / 2  # 0..1 smoothly
for i in range(len(sources)):
    for j in range(len(targets)):
        f = flows[i, j]
        if f <= 0: continue
        s_top = src_top[i] + src_used[i]
        s_bot = s_top + f
        t_top = tgt_top[j] + tgt_used[j]
        t_bot = t_top + f
        ys_top = s_top + (t_top - s_top) * sig
        ys_bot = s_bot + (t_bot - s_bot) * sig
        ax.fill_between(xs, ys_top, ys_bot, color=C[i],
                        alpha=0.40, edgecolor='none')
        src_used[i] += f
        tgt_used[j] += f

ax.set_xlim(-0.10, 1.10); ax.set_ylim(total + 0.05, -0.05)  # invert y for top-down
ax.axis('off')
ax.set_title('(a) Sankey-style flow', loc='left',
             fontweight='bold', fontsize=10.5, pad=8)

# (b) chord-like (circular layout with arcs)
ax = fig.add_subplot(gs[1])
n_nodes = 6
angles = np.linspace(0, 2*np.pi, n_nodes, endpoint=False)
pos = np.array([[np.cos(a), np.sin(a)] for a in angles])
# outer arcs
for i, a in enumerate(angles):
    wedge = Wedge(center=(0,0), r=1.1, theta1=np.degrees(a)-25,
                  theta2=np.degrees(a)+25, width=0.08,
                  facecolor=C[i], edgecolor='white', linewidth=1)
    ax.add_patch(wedge)
    ax.text(1.25*np.cos(a), 1.25*np.sin(a), f'N{i+1}',
            ha='center', va='center', fontsize=9, fontweight='bold')
# connection arcs
pairs = [(0,2,0.7), (0,4,0.4), (1,3,0.8), (2,5,0.5), (3,5,0.3), (1,4,0.6)]
for i, j, w in pairs:
    # bezier through origin
    verts = [pos[i], (0, 0), pos[j]]
    from matplotlib.path import Path
    path = Path(verts, [Path.MOVETO, Path.CURVE3, Path.CURVE3])
    from matplotlib.patches import PathPatch
    ax.add_patch(PathPatch(path, facecolor='none', edgecolor=C[i],
                            linewidth=w*4, alpha=0.55))
ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal'); ax.axis('off')
ax.set_title('(b) Chord diagram', loc='left',
             fontweight='bold', fontsize=10.5, pad=8)

# (c) network graph with circular layout, weighted edges
ax = fig.add_subplot(gs[2])
n = 10
angles = np.linspace(0, 2*np.pi, n, endpoint=False)
pos = np.array([[np.cos(a), np.sin(a)] for a in angles])
edges = [(0,1,0.8),(0,3,0.5),(1,4,0.7),(2,5,0.6),
         (3,6,0.4),(4,7,0.9),(5,8,0.3),(6,9,0.7),
         (7,9,0.6),(2,8,0.5),(0,5,0.4),(1,6,0.5)]
for i, j, w in edges:
    ax.plot([pos[i,0], pos[j,0]], [pos[i,1], pos[j,1]],
            color='gray', alpha=w*0.8, lw=w*3, zorder=1)
sizes = rng.uniform(150, 600, n)
sc = ax.scatter(pos[:,0], pos[:,1], s=sizes, c=range(n),
                cmap='viridis', edgecolor='black', linewidth=1, zorder=3)
for i, (x, y) in enumerate(pos):
    ax.text(x, y, f'{i+1}', ha='center', va='center',
            fontsize=8, fontweight='bold', color='white', zorder=4)
ax.set_xlim(-1.5, 1.5); ax.set_ylim(-1.5, 1.5)
ax.set_aspect('equal'); ax.axis('off')
ax.set_title('(c) Network graph', loc='left',
             fontweight='bold', fontsize=10.5, pad=8)

# (d) arc diagram (linear nodes, arcs above)
ax = fig.add_subplot(gs[3])
n = 12
xs = np.arange(n)
edges = [(0,3),(0,5),(1,7),(2,4),(2,9),(3,6),(4,8),(5,10),(6,11),(7,9),(1,4)]
for i, j in edges:
    cx = (xs[i] + xs[j])/2; r = abs(xs[j] - xs[i])/2
    theta = np.linspace(0, np.pi, 60)
    ax.plot(cx + r*np.cos(theta), r*np.sin(theta),
            color=C[i % len(C)], lw=1.5, alpha=0.6)
sizes = rng.uniform(60, 200, n)
ax.scatter(xs, np.zeros(n), s=sizes, c=range(n), cmap='plasma',
           edgecolor='black', linewidth=0.8, zorder=5)
for i in range(n):
    ax.text(xs[i], -0.5, f'N{i+1}', ha='center', va='top',
            fontsize=7, fontweight='bold')
ax.set_xlim(-0.5, n-0.5); ax.set_ylim(-1.5, 7)
ax.axis('off')
ax.set_title('(d) Arc diagram', loc='left',
             fontweight='bold', fontsize=10.5, pad=8)

plt.show()

```

#### Regression Diagnostics

```
#-----------Part One Code------------
#--------draw--------
fig = plt.figure(figsize=FIGSIZE)
gs = GridSpec(1, 4, figure=fig, wspace=0.32)

n = 100
x = rng.uniform(0, 10, n)
y = 2*x + 3 + rng.normal(0, 1.5, n) + 0.05*x**2  # slight nonlinearity
coef = np.polyfit(x, y, 1)
yhat = np.polyval(coef, x); resid = y - yhat
standardized = resid / resid.std()

# (a) fit + CI
ax = fig.add_subplot(gs[0])
sns.regplot(x=x, y=y, ax=ax, color=C[0],
            scatter_kws={'s': 22, 'alpha': 0.6, 'edgecolor': 'white', 'linewidths': 0.4},
            line_kws={'color': C[3], 'lw': 2})
r, _ = stats.pearsonr(x, y)
ax.text(0.04, 0.96, f'y = {coef[0]:.2f}x + {coef[1]:.2f}\nr = {r:.3f}',
        transform=ax.transAxes, va='top', fontsize=8,
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='gray'))
ax.set_xlabel('X'); ax.set_ylabel('Y')
panel(ax, 'a', 'Regression fit + 95% CI')

# (b) residuals vs fitted
ax = fig.add_subplot(gs[1])
ax.scatter(yhat, resid, s=22, color=C[0], alpha=0.6,
           edgecolor='white', linewidths=0.4)
ax.axhline(0, color=C[3], lw=1.2)
# lowess-like smooth
order = np.argsort(yhat)
smooth = pd.Series(resid[order]).rolling(15, center=True).mean()
ax.plot(yhat[order], smooth, color='black', lw=1.5, alpha=0.8, label='Trend')
ax.set_xlabel('Fitted values'); ax.set_ylabel('Residuals')
ax.legend(frameon=False, fontsize=7)
panel(ax, 'b', 'Residuals vs fitted')

# (c) Q-Q plot
ax = fig.add_subplot(gs[2])
stats.probplot(standardized, dist='norm', plot=ax)
ax.get_lines()[0].set_color(C[0]); ax.get_lines()[0].set_marker('o'); ax.get_lines()[0].set_markersize(4)
ax.get_lines()[1].set_color(C[3]); ax.get_lines()[1].set_linewidth(1.5)
ax.set_xlabel('Theoretical quantiles'); ax.set_ylabel('Standardized residuals')
ax.set_title('')  # clear scipy default title
panel(ax, 'c', 'Normal Q-Q')

# (d) leverage / Cook's distance (visual proxy)
ax = fig.add_subplot(gs[3])
# leverage approx: h_ii from hat matrix for simple linear: 1/n + (x-mean)^2/Sxx
Sxx = np.sum((x - x.mean())**2)
h = 1/n + (x - x.mean())**2/Sxx
cook = (standardized**2 / 2) * (h / (1 - h))
sc = ax.scatter(h, standardized, s=cook*200 + 10, c=cook,
                cmap='Reds', alpha=0.75, edgecolor='black', linewidths=0.5)
ax.axhline(0, color='gray', lw=0.7, ls='--')
ax.axhline(2, color='gray', lw=0.7, ls='--')
ax.axhline(-2, color='gray', lw=0.7, ls='--')
fig.colorbar(sc, ax=ax, shrink=0.85, pad=0.02, label="Cook's D")
ax.set_xlabel('Leverage'); ax.set_ylabel('Standardized residuals')
panel(ax, 'd', "Leverage + Cook's distance")

plt.show()

```
