import sys
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

fname = sys.argv[1]
data = list()
with open(fname, 'r') as f1:
    for line in f1:
        sline = line.split()
        data.append([float(sline[0]),
                     float(sline[1]),
                     float(sline[2])])
data = np.array(data)

fig = plt.figure()
ax = Axes3D(fig)
ax.scatter(data[:, 0], data[:, 1], data[:, 2], s=1)
plt.show()
