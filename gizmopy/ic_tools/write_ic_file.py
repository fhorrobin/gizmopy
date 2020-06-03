"""
Module to generate the hdf5 input file for gizmo given the relevant physical
variables and configuration settings.
"""
import h5py
import numpy as np


def write_header(file_handle, attributes):
    """
    Write the dictionary of attributes for the header to the open file given
    the file handle.
    Parameters
    ----------
    file_handle: h5py.File
        h5py file handle open for writing.
    attributes: dict
        Dictionary of key:value pairs for gizmo header attributes.
    """
    # These values get overwritten by the run-time parameter file but values
    # need to be set in order for the code to run.
    default_value_attributes = {
        "Time": 0.0,
        "Redshift": 0.0,
        "BoxSize": 1.0,
        "NumFilesPerSnapshot": 1,
        "Omega0": 1.0,
        "OmegaLambda": 0.0,
        "HubbleParam": 1.0,
        "Flag_Sfr": 0,
        "Flag_Cooling": 0,
        "Flag_StellarAge": 0,
        "Flag_Metals": 0,
        "Flag_Feedback": 0,
        "Flag_DoublePrecision": 0,
        "Flag_IC_Info": 0
    }

    header_group = file_handle.create_group("Header")

    attributes_combined = {**attributes, **default_value_attributes}
    for key, value in attributes_combined.items():
        header_group.attrs[key] = value


def write_particle_group(file_handle, part_type, **kwargs):
    """
    Write the data for a particle group to the open hdf5 file given the file
    handle.
    Parameters
    ----------
    file_handle: h5py.File
        h5py file handle open for writing.
    part_type: int
        Particle type number.
    **kwargs
        Keyword arguments with keys dataset names and values as datasets.
    """
    particle_group = file_handle.create_group("PartType{}".format(part_type))

    for key, value in kwargs.items():
        particle_group.create_dataset(key, data=value)


def write_file(fname, header_attributes, particles):
    """
    Write the hdf5 file which can then be used as input for a gizmo simulation.
    Parameters
    ----------
    fname: str
        Name for the hdf5 file (without the extension).
    header_attributes: dict
        Dictionary of key: value pairs for gizmo header attributes.
    particles: dict
        Dictionary of particle id to particle datasets where the datasets are
        represented as dictionaries of dataset name: dataset.
    """
    with h5py.File("{}.hdf5".format(fname), "w") as f:
        write_header(f, header_attributes)

        for key, value in particles.items():
            write_particle_group(f, key, **value)
