import sys
from tools_xyz_converter import convert_xyz2list, convert_list2xyz

# -------------------------------------------------------
# Command : python xyz_reverse.py data.xyz outdata.xyz
# -------------------------------------------------------
xyz_ = sys.argv[1]
outxyz_ = sys.argv[2]

# Load xyz_path
l_atomname, l_xyz, l_comment = convert_xyz2list(xyz_)

# Reverse lists
l_atomname = list(reversed(l_atomname))
l_xyz = list(reversed(l_xyz))
l_comment = list(reversed(l_comment))

# Write reversed xyz_path
convert_list2xyz(l_atomname, l_xyz, l_comment, fname=outxyz_)
