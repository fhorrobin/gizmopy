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


def sample_coordinates(r, sigma_r, box_size):
    for i in trange(len(r)):
        rn = box_size * np.random.random()
        choose = np.random.random()

        while sigma_r(rn) < choose:
            rn = box_size * np.random.random()
            choose = np.random.random()

        r[i] = rn


def generate_disk_ics(N, r_in, r_out, alpha, sigma0, T0, h, gamma, G, Mstar, fname):
    q = -1.0 # Initial temperature gradient T ~ r^(-q)

    r = np.linspace(0.1, 5, 1000)

    # Particle mass
    md = mass(lambda r: sigma(r, r_in, r_out, h, alpha, sigma0), r_in * 0.75, r_out * 1.25)
    mp = md / N

    # Sample the radial coordinates
    r = np.zeros(N)
    sample_coordinates(r, lambda r: sigma(r, r_in, r_out, h, alpha, sigma0) * 2 * np.pi / md, r_out * 1.25)

    # Angular coordinate
    theta = 2 * np.pi * np.random.random(N)

    # Conver to cartesian
    x = r * np.cos(theta)
    y = r * np.sin(theta)

    # Gaussian with SD H
    H = h * r
    z = np.random.randn(N) * H

    # Stack the positions
    pos = np.column_stack((x, y, z))

    # Velocities
    omega_k = np.sqrt(G * Mstar / r**2)
    omega = omega_k * np.sqrt((q + alpha) * h**2 + (1 + q) - q * r / np.sqrt(r**2 + z**2))

    vx = -omega * y
    vy = omega * x
    vz = np.zeros(N)

    # Stack the velocities
    vel = np.column_stack((vx, vy, vz))

    T = T0 * r**(q)
    e = T * T_FAC / (gamma - 1)

    npart = np.array([N, 0, 0, 0, 0, 0])

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
        "ParticleIDs": np.arange(1, N+1),
        "Masses": np.ones(N) * mp,
        "InternalEnergy": e,
    }

    particle_groups = {0: p0}

    # Save to GIZMO format
    write_file(fname.strip(".hdf5"), header_attributes, particle_groups)
