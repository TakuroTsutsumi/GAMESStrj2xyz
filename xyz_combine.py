import sys
from tools_xyz_converter import convert_xyz2list, convert_list2xyz

# -------------------------------------------------------
# Command : python xyz_combine.py foward.xyz backward.xyz outxyz.xyz
# -------------------------------------------------------
fwd_xyz = sys.argv[1]
bwd_xyz = sys.argv[2]  # Already reversed in main.sh!!
out_xyz = sys.argv[3]

# Load xyz_path
l_atomname_f, l_xyz_f, l_comment_f = convert_xyz2list(fwd_xyz)
l_atomname_b, l_xyz_b, l_comment_b = convert_xyz2list(bwd_xyz)


# Reverse lists
l_atomname = l_atomname_b + l_atomname_f
l_xyz = l_xyz_b + l_xyz_f
l_comment = l_comment_b + l_comment_f

# Write reversed xyz_path
convert_list2xyz(l_atomname, l_xyz, l_comment, fname=out_xyz)
