from gizmopy.snapshot_io import load_from_snapshot
from Meshoid import Meshoid
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors


def plot_surface_density(snum, rmin, rmax, sdir=".", res=800, clip_inner=True):
    fields = load_fields(snum, sdir)
    pos = fields["Coordinates"]
    mass = fields["Masses"]
    hsml = fields["SmoothingLength"]

    box_size = 2 * rmax

    if clip_inner:
        radius_cut = np.sum(pos*pos, axis=1) > rmin**2

        pos = pos[radius_cut]
        mass = mass[radius_cut]
        hsml = hsml[radius_cut]

    M = Meshoid(pos, mass, hsml)

    X = Y = np.linspace(-rmax, rmax, res)
    X, Y = np.meshgrid(X, Y)

    fig, ax = plt.subplots(figsize=(6, 6))

    # In cgs (from Msun / AU^2)
    sigma_gas = M.SurfaceDensity(M.m, center=np.array([0,0,0]), size=box_size, res=res) * 8.88e6

    p = ax.pcolormesh(X, Y, sigma_gas, norm=colors.LogNorm(), cmap='plasma')
    ax.set_aspect('equal')

    fig.colorbar(p,label=r"$\Sigma_{gas}$ $(\rm g\,cm^{-2})$")
    ax.set_xlabel("X (AU)")
    ax.set_ylabel("Y (AU)")
    plt.show()


def load_fields(snum, sdir):
    pdata = {}

    for field in "Masses", "Coordinates", "SmoothingLength":
        pdata[field] = load_from_snapshot(field, 0, sdir, snum)

    return pdata
