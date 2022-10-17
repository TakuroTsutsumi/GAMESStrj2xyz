import argparse
from tools_xyz_converter import convert_xyz2list, convert_list2xyz, thin_xyz

# -------------------------------------------------------
# Command : python xyz_cut.py data.xyz -o outdata.xyz -s 10 -l 100
# -------------------------------------------------------

# Reference : https://qiita.com/kzkadc/items/e4fc7bc9c003de1eb6d0
parser = argparse.ArgumentParser()
parser.add_argument("xyzpath")
parser.add_argument("-o", "--outdata")
parser.add_argument("-s", "--step")
# parser.add_argument("-l", "--length")
args = parser.parse_args()

xyz_ = args.xyzpath
outxyz_ = args.outdata
step_ = int(args.step)
# length_ = int(args.length)

# Cut xyz data
l_atomname, l_xyz, l_comment = thin_xyz(xyz_, steps=step_)
# l_atomname, l_xyz, l_comment = thin_xyz(xyz_, steps=step_, length=length_)

# Write reversed xyz_path
convert_list2xyz(l_atomname, l_xyz, l_comment, fname=outxyz_)

