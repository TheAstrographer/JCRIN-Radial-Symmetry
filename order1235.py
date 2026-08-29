import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import hsv_to_rgb
from matplotlib.patches import Circle

fig = plt.figure(figsize=(13, 13))
ax = fig.add_subplot(111)
ax.set_aspect('equal')
ax.set_xlim(-1.6, 1.6)
ax.set_ylim(-1.6, 1.6)
ax.set_facecolor('#050510')
fig.patch.set_facecolor('#050510')

theta = np.linspace(0, 2*np.pi, 800)

# === Nested Hypercomplex Shells (Octonionic baseline rings) ===
shell_radii = [0.25, 0.45, 0.65, 0.85, 1.05]
shell_colors = ['#2255aa', '#3377cc', '#4499ee', '#66bbff', '#99ddff']
shell_labels = ['Order 1 core', 'Order 2', 'Order 3', 'Order 5', 'Outer E8-approx']
for r, col, lab in zip(shell_radii, shell_colors, shell_labels):
    ax.plot(r*np.cos(theta), r*np.sin(theta), color=col, lw=1.8, alpha=0.5)
    # Small Petrie-style dots on outer rings
    if r >= 0.65:
        n_dots = int(30 * r)
        for i in range(n_dots):
            ang = 2*np.pi * i / n_dots
            ax.scatter([r*np.cos(ang)], [r*np.sin(ang)], color=col, s=8, alpha=0.6)

# === Order-6 Starred Polyhedra (practical 7ψ orbit) ===
psi = 0.1503378808
step = 7 * psi
orbit = [(k * step) % (2*np.pi) for k in range(6)]
orbit_s = sorted(orbit)

# Hexagon
hx = [np.cos(a) for a in orbit_s] + [np.cos(orbit_s[0])]
hy = [np.sin(a) for a in orbit_s] + [np.sin(orbit_s[0])]
ax.plot(hx, hy, color='#ff3333', lw=2.2, alpha=0.9, zorder=4)

# Star
for start in [0, 1]:
    idx = [(start + 2*i) % 6 for i in range(4)]
    sx = [np.cos(orbit_s[i]) for i in idx]
    sy = [np.sin(orbit_s[i]) for i in idx]
    ax.plot(sx, sy, color='#ffaa00', lw=1.8, alpha=0.8, zorder=4)

# Radial spines
spine_colors = ['#00ffff', '#ff00ff', '#ffff00', '#00ff99', '#ff6600', '#aa88ff']
for ang, col in zip(orbit, spine_colors):
    ax.plot([0, np.cos(ang)], [0, np.sin(ang)], color=col, lw=1.5, alpha=0.85, zorder=3)
    ax.scatter([np.cos(ang)], [np.sin(ang)], color=col, s=70, zorder=5, edgecolors='white', linewidths=0.5)

# === Cosmo Clock Angles ===
cosmo = {
    r'$\psi$': 0.1503378808,
    r'$\alpha$': 0.193218843731,
    r'$\theta_{eff}$': 1.2140298,
    r'$\arctan(2\pi)$': 1.4129651365,
    r'$\Delta\phi$': 1.72113420759,
}
cosmo_colors = ['#4488ff', '#00ffcc', '#88ff00', '#ff44aa', '#ff2222']
for (lab, ang), col in zip(cosmo.items(), cosmo_colors):
    x, y = 1.15*np.cos(ang), 1.15*np.sin(ang)
    ax.plot([0, np.cos(ang)], [0, np.sin(ang)], color=col, lw=1.3, ls='--', alpha=0.7)
    ax.text(x, y, lab, color=col, fontsize=8, ha='center', va='center')

# === Maximal-Winding spiral projection (aerial) ===
t = np.linspace(0, 6.5*np.pi, 1200)
r_spiral = 0.15 + 0.9*(t / (6.5*np.pi))
xs = r_spiral * np.cos(t)
ys = r_spiral * np.sin(t)
for i in range(0, len(t)-1, 3):
    hue = (t[i] / (2*np.pi)) % 1.0
col = hsv_to_rgb([hue, 0.9, 0.95])
    ax.plot(xs[i:i+4], ys[i:i+4], color=col, lw=1.3, alpha=0.75)

# === Arcan(τ) Helix suggestion (compressed rings) ===
for r, alpha in [(0.55, 0.3), (0.75, 0.25)]:
    ax.plot(r*np.cos(theta), r*np.sin(theta), color='#ffcc00', lw=1.2, alpha=alpha, ls=':')

# Center
ax.scatter([0], [0], color='white', s=50, zorder=6)

# Title
ax.set_title('Octonionic Baseline Orders 1 • 2 • 3 • 5\n'
             'Aerial View — 360° Sphere Radians Representation\n'
             'Maximal-Winding (w=3.25) • Arcan(τ) Helix • Order-6 Starred Polyhedra\n'
             'Cosmo Clock Angles • Nested Hypercomplex Shells', 
             color='white', fontsize=12, pad=10, fontweight='bold')

# Legend box
textstr = (
    "Nested Shells: Orders 1-2-3-5 (Octonionic)\n"
    "Red + Gold: Order-6 Starred Polyhedra (7ψ orbit)\n"
    "HSV Spiral: Maximal-Winding w=3.25\n"
    "Dashed coloured rays: Cosmo Clock Angles\n"
    "Gold dotted: Arcan(τ) compression loci\n"
    "Practical orbit step = 7ψ ≈ 1.052365 rad"
)
props = dict(boxstyle='round', facecolor='#0a0a18', alpha=0.92, edgecolor='#555577')
ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=8.5,
        verticalalignment='top', color='white', bbox=props)

ax.set_xticks([])
ax.set_yticks([])
for spine in ax.spines.values():
    spine.set_visible(False)

plt.tight_layout()
plt.savefig('/tmp/octonionic_baseline_aerial_360.png', dpi=170, bbox_inches='tight', facecolor=fig.get_facecolor())
print("Saved: /tmp/octonionic_baseline_aerial_360
