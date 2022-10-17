"""
This contains useful functions related to handling xyz data.
"""
import itertools
import copy
from pathlib import Path

import numpy as np
import pandas as pd
from typing import List


def readline_strip(fname):
    list_line = []
    with open(fname) as file:
        line = file.readline()
        while line:
            tlist_line = line.strip()
            list_line.append(tlist_line)
            line = file.readline()
    return list_line


def convert_xyz2list(xyz_path):
    """
    Convert a xyz-format file into lists of atomic name, xyz, and comment line

    Parameters
    ----------
    xyz_path : str
        A file path

    Returns
    -------
    list_atname : List[List[str]]
        A list of atomic names for each molecule.
        [ ["O", "H", "H"], ["O", "H", "H"], ... ]
    list_xyz : List[List[List[float]]]
        A list of coordinates for each molecule.
        [[[0.00, 0.00,-0.06], [-0.00, 0.75, 0.52], [-0.00,-0.75, 0.52]],
         [[0.00, 0.00,-0.06], [-0.00, 0.80, 0.60], [-0.00,-0.80, 0.60]],
         [[                       ... ... ...                        ]] ]
    list_comment : List[str]
        A list of comment lines for each molecule.
        [ "H2O-0 Energy: 0.00 eV", "H2O-1 Energy: 0.40 eV",  ... ... ... ]
    """
    list_line = readline_strip(xyz_path)
    list_comment, list_xyz, list_atname = [], [], []
    tlist_xyz, tlist_atname = [], []
    natoms = int(list_line[0])

    for i, iline in enumerate(list_line):
        if iline == "":
            break
        if i % (natoms + 2) == 1:  # Comment line
            list_comment.append(iline)
        elif i % (natoms + 2) >= 2:  # Coordinate
            tiline = iline.split()
            tlist_xyz.append(list(map(float, tiline[1:])))
            tlist_atname.append(tiline[0])
        # Save template lists
        if i % (natoms + 2) == (natoms + 1):
            list_atname.append(tlist_atname)
            list_xyz.append(tlist_xyz)
            tlist_atname, tlist_xyz = [], []

    return list_atname, list_xyz, list_comment


def convert_list2xyz(list_atname, list_xyz, list_comment, fname="save_coordinate.xyz", *, open_type="w"):
    """
    Generate a xyz-format file from lists of atomic name, xyz, and comment line

    Parameters
    ----------
    list_atname : List[List[str]]
        A list of atomic names for each molecule.
        [ ["O", "H", "H"], ["O", "H", "H"], ... ]
    list_xyz : List[List[List[float]]]
        A list of coordinates for each molecule.
        [[[0.00, 0.00,-0.06], [-0.00, 0.75, 0.52], [-0.00,-0.75, 0.52]],
         [[0.00, 0.00,-0.06], [-0.00, 0.80, 0.60], [-0.00,-0.80, 0.60]],
         [[                       ... ... ...                        ]] ]
    list_comment : List[str]
        A list of comment lines for each molecule.
        [ "H2O-0 Energy: 0.00 eV", "H2O-1 Energy: 0.40 eV",  ... ... ... ]
    fname : str, default : "save_coordinate.xyz"
        A file name of output
    open_type : str, default : "w"
        The keyword is assigned as 'with open(fname, open_type)'.
    """
    natoms = len(list_atname[0])
    with open(fname, open_type) as f:
        for icomment, iatname, ixyz in zip(list_comment, list_atname, list_xyz):
            f.write("%s\n" % str(natoms))
            f.write("%s\n" % icomment)
            for i, xyz in enumerate(ixyz):
                f.write("%3s %18.12f %18.12f %18.12f\n" % (iatname[i], xyz[0], xyz[1], xyz[2]))
    return


def thin_xyz(fname, *, steps=1, length=None, addFinalXYZ=True):
    """
    Thin xyz-format files

    Parameters
    ----------
    fname : str
        Path of the xyz-format file.
    steps : int, default 1
        Number of steps to thin out the xyz-format file.
    length : int, default None
        Length of the xyz-format file after thinning.
        This option will be preferred even if the steps argument is specified.
    addFinalXYZ : bool, default True
        If True, in any case the final structure will be listed in the thinned out xyz file.

    Returns
    ----------
    new_list_atname : list
    new_list_xyz :  list
    new_list_comment : list

    """
    # Convert xyz-format to list
    list_atname, list_xyz, list_comment = convert_xyz2list(str(Path(fname)))

    # --------------------------------------------------------------------------
    # Define a per_steps and an output file name
    # --------------------------------------------------------------------------
    if length is None:
        per_steps = steps
    else:
        per_steps = len(list_xyz) // length

    nlength = len(list_xyz)
    # --------------------------------------------------------------------------
    # Cut xyz coordinate for each per_steps
    # --------------------------------------------------------------------------
    out_fname = "%s_per%03d.xyz" % (Path(fname).stem, per_steps)
    new_list_atname = [list_atname[i] for i in range(0, nlength, per_steps)]
    new_list_xyz = [list_xyz[i] for i in range(0, nlength, per_steps)]
    new_list_comment = [list_comment[i] for i in range(0, nlength, per_steps)]
    
    # Check the final coordinate
    if addFinalXYZ:
        if new_list_xyz[-1] != list_xyz[-1]:  # old condition: if (nlength - 1) % per_steps != 0:
            new_list_atname.append(list_atname[-1])
            new_list_xyz.append(list_xyz[-1])
            new_list_comment.append(list_comment[-1])

    return new_list_atname, new_list_xyz, new_list_comment
