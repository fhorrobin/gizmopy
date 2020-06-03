from gizmopy.ic_tools import generate_disk_ics
from argparse import ArgumentParser


argparser = ArgumentParser(description='Generate Particle Disk Initial Conditions for GIZMO.')
argparser.add_argument("N", help="the number of particles")
argparser.add_argument("rin", help="inner radius of the disk (middle of smoothed boundary)")
argparser.add_argument("rout", help="outer radius of the disk (middle of smoothed boundary)")
argparser.add_argument("alpha", help="power law index for the disk")
argparser.add_argument("sigma0", help="surface density at r=1")
argparser.add_argument("T0", help="gas temperature at r=1")
argparser.add_argument("h", help="H/r scale factor")
argparser.add_argument("gamma", help="adiabatic index")
argparser.add_argument("-G", help="gravitational constant (code units, default: 1.0)", default=1.0)
argparser.add_argument("-Mstar", help="mass of the star (code units, default: 1.0)", default=1.0)
argparser.add_argument("--output_file", "-o", help="name of file to output (default: ic_disk.hdf5)", default="ic_disk")

results = argparser.parse_args()

N = int(float(results.N))
r_in = float(results.rin)
r_out = float(results.rout)
alpha = float(results.alpha)
sigma0 = float(results.sigma0)
T0 = float(results.T0)
h = float(results.h)
gamma = float(results.gamma)
G = float(results.G)
Mstar = float(results.Mstar)
fname = results.output_file

generate_disk_ics(N, r_in, r_out, alpha, sigma0, T0, h, gamma, G, Mstar, fname)
