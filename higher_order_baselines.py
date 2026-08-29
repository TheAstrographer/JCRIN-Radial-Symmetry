import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

psi = 0.1503378808
step = 7 * psi  # 1.0523651656
print(f"7ψ = {step:.10f}")

fig = plt.figure(figsize=(14, 12), facecolor='#0a0a12')
fig.suptitle('Higher-Order Baselines\nQuaternionic Order 12 • Octonionic Orders 10 • 15 • 30\n'
             f'Precise Step: 7ψ = {step:.10f} rad', 
             color='white', fontsize=14, fontweight='bold', y=0.98)

orders = [12, 10, 15, 30]
titles = [
    'Quaternionic Baseline — Order 12\nDense Mid-Shell Starred Polyhedra + 24-Cell Core',
    'Octonionic Baseline — Order 10\nMulti-Ring E₈ Precursor',
    'Octonionic Baseline — Order 15\nDenser Petrie Shells',
    'Octonionic Baseline — Order 30\nHigh-Density E₈ Root Shell Approximation'
]
positions = [221, 222, 223, 224]

for idx, (order, title, pos) in enumerate(zip(orders, titles, positions)):
    ax = fig.add_subplot(pos, projection='3d', facecolor='#0a0a12')
    
    # Generate points on a slightly flattened sphere / disk for visual density
    angles = np.array([(k * step) % (2 * np.pi) for k in range(order)])
    
    # Multiple radial shells for density effect
    if order == 12:
        # Starred polyhedra style: two radii + connections
        r_outer = 1.0
        r_inner = 0.55
        x = r_outer * np.cos(angles)
        y = r_outer * np.sin(angles)
        z = 0.12 * np.sin(3 * angles)  # mild wave
        ax.scatter(x, y, z, c='#FFD700', s=55, edgecolors='white', linewidths=0.4, zorder=5)
        
        # Inner core (24-cell hint)
x_in = r_inner * np.cos(angles)
        y_in = r_inner * np.sin(angles)
        z_in = 0.08 * np.cos(2 * angles)
        ax.scatter(x_in, y_in, z_in, c='#00E5FF', s=35, alpha=0.9)
        
        # Connect outer hexagon-like
        for i in range(order):
            j = (i + 1) % order
            ax.plot([x[i], x[j]], [y[i], y[j]], [z[i], z[j]], color='#FF6B6B', alpha=0.7, lw=1.1)
            # star connections every 2
            k = (i + 2) % order
            ax.plot([x[i], x[k]], [y[i], y[k]], [z[i], z[k]], color='#FFD700', alpha=0.5, lw=0.9)
            # to inner
            ax.plot([x[i], x_in[i]], [y[i], y_in[i]], [z[i], z_in[i]], color='#4ECDC4', alpha=0.4, lw=0.7)
            
    else:
        # Concentric ring densification for octonionic
        n_rings = 3 if order <= 15 else 5
        for r_idx, r in enumerate(np.linspace(0.35, 1.0, n_rings)):
            # Offset angles slightly per ring for spiral feel
            ang_off = angles + r_idx * 0.08
            x = r * np.cos(ang_off)
            y = r * np.sin(ang_off)
            z = 0.06 * (r_idx - n_rings/2) * np.ones_like(x)
            size = 28 if order < 30 else 12
            color = plt.cm.cool(0.3 + 0.5 * r)
            ax.scatter(x, y, z, c=[color], s=size, alpha=0.85, edgecolors='none')
        
        # Central core
        ax.scatter([0], [0], [0], c='gold', s=80, zorder=10)
        # Faint radial lines
        for ang in angles[::max(1, order//12)]:
            ax.plot([0, np.cos(ang)], [0, np.sin(ang)], [0, 0], color='white', alpha=0.08, lw=0.5)

    ax.set_xlim(-1.2, 1.2)
    ax.set_ylim(-1.2, 1.2)
    ax.set_zlim(-0.6, 0.6)
    ax.set_axis_off()
    ax.view_init(elev=28, azim=-60)
    
    # Title below each
    ax.text2D(0.5, -0.08, title, transform=ax.transAxes, ha='center', va='top',
              color='white', fontsize=9, wrap=True)

# Footer
plt.tight_layout(rect=[0, 0.06, 1, 0.95])
plt.savefig('/tmp/higher_order_baselines_7psi.png', dpi=160, bbox_inches='tight', facecolor='#0a0a12')
print("Saved: /tmp/higher_order_baselines_7psi.png")
