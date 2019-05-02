import sys
import numpy as np
import matplotlib.pyplot as plt


fname = sys.argv[1]
data = list()
with open(fname, 'r') as f1:
    for line in f1:
        sline = line.split()
        data.append([float(sline[0]),
                     float(sline[1]),
                     float(sline[2])])
data = np.array(data)
plt.scatter(data[:, 0], data[:, 1], s=1,)
plt.title(f'Scatter plot for {fname}')
plt.xlabel('x (m)')
plt.ylabel('y (m)')
plt.show()
