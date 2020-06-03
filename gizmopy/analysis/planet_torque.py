"""
Compute the torque on a planet from the gas disk.
"""

import numpy as np


def compute_torque(r, m, t, ap, epsp, G=1.0, Mstar=1.0):
    omega = np.sqrt(G * Mstar / ap**3)

    rp = np.array([ap * np.cos(omega * t), ap * np.cos(omega * t), 0.0])

    g = compute_grav_accel_vector(r, rp, epsp)

    cross = np.cross(rp, g)
    return np.sum(G * m * cross[:,2])


def compute_grav_accel_vector(r, rp, epsp):
    r2 = np.sum((r - rp)**2)

    return (r - rp) / (r2 + epsp**2)**(3/2)
