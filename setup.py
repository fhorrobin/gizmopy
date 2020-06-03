import setuptools

with open("README.rst", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="gizmopy",
    version="0.0.1",
    author="Fergus Horrobin",
    author_email="horrobin@astro.utoronto.ca",
    description="Tools for working with GIZMO ICs and snapshots",
    long_description=long_description,
    url="https://github.com/fhorrobin/gizmopy",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    scripts=["./scripts/gizmoplot", "./scripts/makedisk"]
)
