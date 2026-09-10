import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# -------------------------------------------------
# Quaternion utilities
# -------------------------------------------------
def quaternion_multiply(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2
    return np.array([
        w1*w2 - x1*x2 - y1*y2 - z1*z2,
        w1*x2 + x1*w2 + y1*z2 - z1*y2,
        w1*y2 - x1*z2 + y1*w2 + z1*x2,
        w1*z2 + x1*y2 - y1*x2 + z1*w2
    ])

def rotate_vector_by_quaternion(v, q):
    """Rotate 3-vector v by unit quaternion q"""
    q_conj = np.array([q[0], -q[1], -q[2], -q[3]])
    v_quat = np.array([0, v[0], v[1], v[2]])
    return quaternion_multiply(quaternion_multiply(q, v_quat), q_conj)[1:]

# -------------------------------------------------
# Parameters
# -------------------------------------------------
theta = np.arctan(2 * np.pi)
phi   = np.arctan(np.pi)
psi   = theta - phi
cos_psi = np.cos(psi)

# Several temperature values
taus = np.array([2*np.pi, np.pi, np.pi/2, 1.0, 0.5])

# Base attention directions on the sphere (query-key pairs simplified to directions)
np.random.seed(42)
n_dirs = 60
raw_dirs = np.random.randn(n_dirs, 3)
raw_dirs /= np.linalg.norm(raw_dirs, axis=1, keepdims=True)

fig = plt.figure(figsize=(14, 5))

for idx, tau in enumerate(taus):
    ax = fig.add_subplot(1, 5, idx+1, projection='3d')
    
    # Quaternion that encodes temperature + thinnest-triangle phase
    # We use a pure rotation quaternion whose angle is modulated by τ and locked by Ψ
    angle = (tau / (2*np.pi)) * psi          # residual angular freedom scaled by normalized τ
    axis = np.array([0, 0, 1])               # rotation about z for clarity
    q = np.array([
        np.cos(angle/2),
        axis[0]*np.sin(angle/2),
        axis[1]*np.sin(angle/2),
        axis[2]*np.sin(angle/2)
    ])
    
    # Rotate all directions by the temperature quaternion
    rotated = np.array([rotate_vector_by_quaternion(v, q) for v in raw_dirs])
    
    # Attention intensity: higher when closer to the thinnest-triangle sector
    # (simplified scalar field)
    intensity = np.exp(-np.abs(rotated[:, 2] - np.cos((theta+phi)/2))**2 / 0.3)
    intensity = (intensity - intensity.min()) / (intensity.max() - intensity.min() + 1e-8)
    
# Plot
    sc = ax.scatter(rotated[:,0], rotated[:,1], rotated[:,2],
                    c=intensity, cmap='magma', s=25, alpha=0.85)
    
    # Draw unit sphere wireframe (light)
    u = np.linspace(0, 2*np.pi, 30)
    v = np.linspace(0, np.pi, 20)
    x_s = np.outer(np.cos(u), np.sin(v))
    y_s = np.outer(np.sin(u), np.sin(v))
    z_s = np.outer(np.ones_like(u), np.cos(v))
    ax.plot_wireframe(x_s, y_s, z_s, color='gray', alpha=0.15, linewidth=0.3)
    
    ax.set_xlim(-1.1, 1.1)
    ax.set_ylim(-1.1, 1.1)
    ax.set_zlim(-1.1, 1.1)
    ax.set_title(f'τ = {tau:.2f}', fontsize=10)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.view_init(elev=22, azim=35)

fig.suptitle('Quaternion τ-Temperature Attention Maps on $S^2$\n'
             r'(rotation angle locked by Thinnest-Triangle $\Psi\approx 8.61^\circ$)',
             fontsize=13, y=1.02)

plt.tight_layout()
plt.savefig('/home/workdir/quaternion_tau_attention.png', dpi=150, bbox_inches='tight')
print("Quaternion τ-attention maps saved.")
