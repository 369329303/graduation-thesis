import sys
import numpy as np
from scipy import spatial


def is_normal(i, k=9):
    point_loc = [contents[i][0], contents[i][1]]
    res = tree.query(point_loc, k)
    z_l = list()
    for i in res[1]:
        z_l.append(contents[i][2])
    z_a = np.array(z_l)
    z_std = np.std(z_a)
    z_median = np.median(z_a)
    if abs(contents[i][2] - z_median) > 3 * z_std:
        return False
    else:
        return True


contents = list()
with open(sys.argv[1], 'r') as f:
    for line in f:
        sline = line.split()
        contents.append([float(sline[0]), float(sline[1]), float(sline[2])])

contents_a = np.array(contents)
tree = spatial.KDTree(contents_a[:, 0:2])

with open('new_source.txt', 'w') as new_source:
    for i in range(len(contents)):
        if is_normal(i):
            new_source.write('\t'.join(map(str, contents[i])) + '\n')
