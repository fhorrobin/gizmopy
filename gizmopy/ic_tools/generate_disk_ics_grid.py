"""
Generate disk ics on a grid, with uneven particle masses (better for MFV).
"""

from .write_ic_file import write_file
import numpy as np
from scipy.integrate import quad
from tqdm import trange
import matplotlib.pyplot as plt


# Conversion factor for e -> T in Msun, AU, yr
T_FAC = 4 * np.pi**2 * 4.444e-8 / 1.38e-23 * (2.35 * 1.674e-27)

def f(r, r_in, r_out, smooth):
    inner = np.exp((r_in - r) / smooth)
    outer = np.exp((r - r_out) / smooth)

    return 1 / (1 + inner) + 1 / (1 + outer) - 1


def sigma(r, r_in, r_out, h, alpha, sigma0):
    return f(r, r_in, r_out, h) * sigma0 * r**(alpha + 1)


def mass(sigma, r_min, r_max):
    mass, _ = quad(sigma, r_min, r_max)
    return 2 * np.pi * mass


def generate_grid_coordinates(r_max, r_min, z_max, Nxy, Nz, alpha, sigma0, h):
    grid = np.mgrid[-r_max:r_max:Nxy*1j, -r_max:r_max:Nxy*1j, -z_max:z_max:Nz*1j]

    x, y, z = [grid[i].ravel() for i in range(3)]

    R = np.sqrt(x**2 + y**2)
    mask = np.logical_and(R > r_min, R < r_max)

    x, y, z = x[mask], y[mask], z[mask]

    R = R[mask]
    mass = f(R, r_min, r_max, 2 * h) * 2 * np.pi * (r_max**2 - r_min**2) * sigma0 / (Nxy**2 * Nz) * R**(alpha) * np.exp(-z**2 / (R * h)**2)

    mask = mass > 1e-12
    x, y, z = x[mask], y[mask], z[mask]
    R = R[mask]
    mass = mass[mask]

    return x, y, z, mass, R


def generate_disk_ics_grid(N, r_in, r_out, alpha, sigma0, T0, h, gamma, G, Mstar, fname):
    q = -1.0
    z_max = r_out * h * 4

    Nxy = (N * 2 * r_out / z_max)**(1/3)
    Nz = N / Nxy**2

    x, y, z, mass, R = generate_grid_coordinates(r_out, r_in, z_max, Nxy, Nz, alpha, sigma0, h)

    pos = np.column_stack((x, y, z))

    # Velocities
    omega_k = np.sqrt(G * Mstar / R**2)
    omega = omega_k * np.sqrt((q + alpha) * h**2 + (1 + q) - q * R / np.sqrt(R**2 + z**2))

    vx = -omega * y
    vy = omega * x
    vz = np.zeros(len(vx))

    # Stack the velocities
    vel = np.column_stack((vx, vy, vz))

    T = T0 * R**(q)
    e = T * T_FAC / (gamma - 1)

    nump = len(x)

    npart = np.array([nump, 0, 0, 0, 0, 0])

    # Make dicts
    header_attributes = {
        "NumPart_ThisFile": npart,
        "NumPartt_Total": npart,
        "NumPart_Total_HighWord": 0.0,
        "MassTable": np.zeros(6)
    }

    p0 = {
        "Coordinates": pos,
        "Velocities": vel,
        "ParticleIDs": np.arange(1, nump+1),
        "Masses": mass,
        "InternalEnergy": e,
    }

    particle_groups = {0: p0}

    # Save to GIZMO format
    write_file(fname.strip(".hdf5"), header_attributes, particle_groups)


