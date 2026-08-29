import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Constants
psi = 0.1503378808
step = 7 * psi  # 1.0523651656
alpha = 0.193218843731
theta_eff = 1.2140298
arctan_2pi = 1.4129651365
delta_phi = 1.72113420759
theta_max = 6.5 * np.pi
w = 3.25

fig = plt.figure(figsize=(12, 11))
ax = fig.add_subplot(111, projection='3d')

# Unit sphere wireframe
u = np.linspace(0, 2*np.pi, 60)
v = np.linspace(0, np.pi, 30)
x_s = np.outer(np.cos(u), np.sin(v))
y_s = np.outer(np.sin(u), np.sin(v))
z_s = np.outer(np.ones(np.size(u)), np.cos(v))
ax.plot_surface(x_s, y_s, z_s, color='lightblue', alpha=0.12, edgecolor='none')

# Equator
eq_theta = np.linspace(0, 2*np.pi, 200)
ax.plot(np.cos(eq_theta), np.sin(eq_theta), 0, color='blue', linewidth=2.5, label='Equator (360°)')

# Diameters (Length / Width / Height = 2)
ax.plot([-1, 1], [0, 0], [0, 0], color='red', linewidth=2.5, label='Diameter = 2 (Length/Width)')
ax.plot([0, 0], [-1, 1], [0, 0], color='orange', linewidth=2.0)
ax.plot([0, 0], [0, 0], [-1, 1], color='purple', linewidth=2.0, label='Diameter = 2 (Height)')

# Practical six-fold orbit (Order-6) on equator
orbit_angles = [(k * step) % (2 * np.pi) for k in range(6)]
for i, ang in enumerate(orbit_angles):
    x, y = np.cos(ang), np.sin(ang)
    ax.scatter([x], [y], [0], color='red', s=80, zorder=10)
    ax.plot([0, x], [0, y], [0, 0], color='red', alpha=0.6, linewidth=1.2)

# Hexagon + star on equator
hex_x = [np.cos(a) for a in orbit_angles] + [np.cos(orbit_angles[0])]
hex_y = [np.sin(a) for a in orbit_angles] + [np.sin(orbit_angles[0])]
ax.plot(hex_x, hex_y, [0]*7, color='red', linewidth=2.0)

# Interlocking triangles (star)
t1 = [orbit_angles[0], orbit_angles[2], orbit_angles[4], orbit_angles[0]]
t2 = [orbit_angles[1], orbit_angles[3], orbit_angles[5], orbit_angles[1]]
ax.plot([np.cos(a) for a in t1], [np.sin(a) for a in t1], [0]*4, color='gold', linewidth=2.2)
ax.plot([np.cos(a) for a in t2], [np.sin(a) for a in t2], [0]*4, color='gold', linewidth=2.2)

# Cosmo Clock / Terminal rays (great-circle arcs approximated on sphere surface near equator + lifted)
rays = {
    'ψ': psi,
    'α': alpha,
    'θ_eff': theta_eff,
    'arctan(2π)': arctan_2pi,
    'Δφ_torque': delta_phi,
    '-arctan(2π)': (2*np.pi - arctan_2pi)
}
ray_colors = ['cyan', 'deepskyblue', 'lime', 'magenta', 'orange', 'violet']
for (name, ang), col in zip(rays.items(), ray_colors):
    # Ray on equator
    ax.plot([0, np.cos(ang)], [0, np.sin(ang)], [0, 0], color=col, linewidth=1.8, alpha=0.9)
    # Slightly lifted arc for visibility
    elev = np.linspace(0, 0.35, 20)
    ax.plot(np.cos(ang)*np.cos(elev), np.sin(ang)*np.cos(elev), np.sin(elev), color=col, linewidth=1.5, alpha=0.7)

# Maximal-winding spiral (on sphere surface, decreasing radius in z for visibility)
t = np.linspace(0, 1, 800)
theta = theta_max * t
r = 0.95 * (1 - 0.15*t)  # slight inward for depth
z_spiral = 0.55 * np.sin(2*np.pi * 1.5 * t) * (1-t*0.3)  # mild vertical modulation
x_spiral = r * np.cos(theta)
y_spiral = r * np.sin(theta)
# HSV-like coloring via segments
for i in range(0, len(t)-1, 8):
    ax.plot(x_spiral[i:i+9], y_spiral[i:i+9], z_spiral[i:i+9],
            color=plt.cm.hsv(theta[i]/(2*np.pi) % 1), linewidth=1.8, alpha=0.85)

# Nested shells (concentric circles in xy at different radii, slight z offset)
shell_radii = [0.35, 0.55, 0.75, 0.92]
shell_colors = ['gold', 'orange', 'coral', 'crimson']
for r_s, col in zip(shell_radii, shell_colors):
    ax.plot(r_s*np.cos(eq_theta), r_s*np.sin(eq_theta), 0.02*np.sin(3*eq_theta),
            color=col, linewidth=1.3, alpha=0.7)

# Labels
ax.text(1.15, 0, 0, 'X\n(Length)', color='red', fontsize=9)
ax.text(0, 1.15, 0, 'Y\n(Width)', color='orange', fontsize=9)
ax.text(0, 0, 1.15, 'Z\n(Height)', color='purple', fontsize=9)

ax.set_xlim(-1.3, 1.3)
ax.set_ylim(-1.3, 1.3)
ax.set_zlim(-1.3, 1.3)
ax.set_xlabel('X (Length/Width)')
ax.set_ylabel('Y (Width)')
ax.set_zlabel('Z (Height)')
ax.set_title('360° Sphere Radians Representation\n'
             'Unit Sphere • Maximal-Winding (w=3.25) • Order-6 Starred Polyhedra\n'
             'Cosmo Clock Angles • Nested Hypercomplex Shells • Practical 7ψ Orbit\n'
             'Diameter = 2 in every direction', fontsize=12, pad=12)

# Legend (manual)
from matplotlib.lines import Line2D
legend_elements = [
    Line2D([0], [0], color='blue', lw=2, label='Equator (full 360°)'),
    Line2D([0], [0], color='red', lw=2, label='Diameters = 2'),
    Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=8, label='Order-6 classes (7ψ orbit)'),
    Line2D([0], [0], color='gold', lw=2, label='Starred Polyhedra (mid-shell)'),
    Line2D([0], [0], color='magenta', lw=2, label='Cosmo Clock / Terminal rays'),
    Line2D([0], [0], color='orange', lw=1.5, label='Nested shells (24-cell → E₈)'),
]
ax.legend(handles=legend_elements, loc='upper left', fontsize=8, framealpha=0.9)

ax.view_init(elev=22, azim=-55)
plt.tight_layout()
plt.savefig('/tmp/360_sphere_radians_complete.png', dpi=160, bbox_inches='tight', facecolor='white')
print("Saved: /tmp/360_sphere_radians_complete.png")
print(f"7ψ step = {step:.10f}")
print(f"Orbit angles: {[round(a,6) for a in orbit_angles]}")
