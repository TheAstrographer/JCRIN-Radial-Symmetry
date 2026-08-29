import numpy as np
import matplotlib.pyplot as plt

psi = 0.1503378808
step = 7 * psi                  # 1.0523651656
ideal = np.pi / 3               # 1.0471975512
delta = step - ideal            # ≈ 0.0051676144
print(f"7ψ = {step:.10f}")
print(f"π/3 = {ideal:.10f}")
print(f"δ = {delta:.10f} rad")

fig, ax = plt.subplots(figsize=(10, 10))

#Unit circle
theta = np.linspace(0, 2*np.pi, 500)
ax.plot(np.cos(theta), np.sin(theta), 'k-', lw=1.5, label='Unit circle')

# Ideal π/3 residue classes (red)
ideal_angles = [k * ideal for k in range(6)]
for i, ang in enumerate(ideal_angles):
    x, y = np.cos(ang), np.sin(ang)
    ax.plot([0, x], [0, y], 'r--', alpha=0.5, lw=1.2)
    ax.scatter([x], [y], c='red', s=90, zorder=5, edgecolors='darkred')
    ax.text(1.12*x, 1.12*y, f'[ {i} ]\nπ/3', color='red', ha='center', va='center', fontsize=8)

# Practical 7ψ orbit (cyan)
prac_angles = [(k * step) % (2*np.pi) for k in range(6)]
for i, ang in enumerate(prac_angles):
    x, y = np.cos(ang), np.sin(ang)
    ax.plot([0, x], [0, y], color='cyan', alpha=0.8, lw=1.8)
    ax.scatter([x], [y], c='cyan', s=70, zorder=6, edgecolors='blue')
    # label only a few to avoid clutter
    if i in [0, 1, 2]:
        ax.text(1.22*x, 1.22*y, f'{i}×7ψ', color='blue', ha='center', va='center', fontsize=8)

# Highlight the residual δ at the first step (between 0 and first points)
# Arc showing δ
arc_theta = np.linspace(ideal, step, 30)
ax.plot(1.05*np.cos(arc_theta), 1.05*np.sin(arc_theta), color='magenta', lw=3, solid_capstyle='round')
ax.annotate('', xy=(np.cos(step)*1.05, np.sin(step)*1.05),
            xytext=(np.cos(ideal)*1.05, np.sin(ideal)*1.05),
            arrowprops=dict(arrowstyle='->', color='magenta', lw=2))
mid = (ideal + step)/2
ax.text(1.18*np.cos(mid), 1.18*np.sin(mid), r'$\delta\approx 0.00517$', 
        color='magenta', fontsize=11, fontweight='bold', ha='center')

# Hexagon outlines
ideal_x = [np.cos(a) for a in ideal_angles] + [np.cos(ideal_angles[0])]
ideal_y = [np.sin(a) for a in ideal_angles] + [np.sin(ideal_angles[0])]
ax.plot(ideal_x, ideal_y, 'r-', lw=1.5, alpha=0.6, label='Ideal π/3 hexagon')

prac_x = [np.cos(a) for a in prac_angles] + [np.cos(prac_angles[0])]
prac_y = [np.sin(a) for a in prac_angles] + [np.sin(prac_angles[0])]
ax.plot(prac_x, prac_y, color='cyan', lw=2.0, alpha=0.8, label='Practical 7ψ orbit')

# Star (every second of practical)
t1 = [prac_angles[0], prac_angles[2], prac_angles[4], prac_angles[0]]
t2 = [prac_angles[1], prac_angles[3], prac_angles[5], prac_angles[1]]
ax.plot([np.cos(a) for a in t1], [np.sin(a) for a in t1], color='gold', lw=2.2, label='Radial-fold star')
ax.plot([np.cos(a) for a in t2], [np.sin(a) for a in t2], color='gold', lw=2.2)

# Origin
ax.scatter([0], [0], c='black', s=40, zorder=10)

ax.set_xlim(-1.45, 1.45)
ax.set_ylim(-1.45, 1.45)
ax.set_aspect('equal')
ax.set_title('Circle Graph — Comoving Residual\n'
             r'$\delta = 7\psi - \pi/3 \approx 0.0051676$ rad' + '\n'
             'Practical 7ψ orbit (cyan) vs Ideal π/3 lattice (red)',
             fontsize=13, pad=12)
ax.legend(loc='upper left', fontsize=9, framealpha=0.92)
ax.grid(True, alpha=0.3)
ax.set_xlabel('cos φ')
ax.set_ylabel('sin φ')

# Info box
textstr = '\n'.join([
    r'$7\psi = 1.0523651656$',
    r'$\pi/3 \approx 1.0471975512$',
    r'$\delta \approx 0.0051676$ rad',
    r'($\approx 0.296^\circ$)',
    '',
    'The residual is the signature',
    'that the radial-fold is emergent',
    'and comoving with the continuous',
    'tan-arctan-τ family of the',
    'Cosmological Clock.'
])
props = dict(boxstyle='round', facecolor='lightyellow', alpha=0.9)
ax.text(0.98, 0.02, textstr, transform=ax.transAxes, fontsize=8,
        verticalalignment='bottom', horizontalalignment='right', bbox=props)

plt.tight_layout()
plt.savefig('/tmp/comoving_residual_circle_graph.png', dpi=160, bbox_inches='tight', facecolor='white')
print("Saved: /tmp/comoving_residual_circle_graph.png"
