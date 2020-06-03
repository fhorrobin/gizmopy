from argparse import ArgumentParser
from gizmopy.quickplots import plot_surface_density


argparser = ArgumentParser(description='Quickplot of a GIZMO Snapshot.')
argparser.add_argument("snap", help="the snapshot number")
argparser.add_argument("r_min", help="minimum boundary for particle position")
argparser.add_argument("r_max", help="maximum boundary for particle position")
argparser.add_argument("--dir", help="subdirectory for the snapshot (default: .)", default=".")
argparser.add_argument("--res", help="resolution for the mesh (default: 800)", default=800)
#argparser.add_argument("--field", help="name of the field to plot (default: Density, options: Density, Velocity, Vortensity)", default="Density")

results = argparser.parse_args()

plot_surface_density(int(results.snap), float(results.r_min), float(results.r_max), results.dir, int(results.res))
