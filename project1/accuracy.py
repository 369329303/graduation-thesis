import sys
import math
import numpy as np


def diff_list(file1, file2):
    '''return list of (z2-z1) for z1 in file1, z2 in file2.'''
    count = 0
    diff = list()
    with open(file1, 'r') as f1, \
            open(file2, 'r') as f2:
        for line1, line2 in zip(f1, f2):
            if count % 2:
                z1 = float(line1.split()[2])
                z2 = float(line2.split()[2])
                diff.append(z2 - z1)
            count += 1
    return diff


if len(sys.argv) < 3:
    print(f'Usage: {sys.argv[0]} <data1.txt> <data2.txt> ...')
    sys.exit(1)

tmpfile2 = open('tmpfile2.txt', 'w')
print(f'{"Method":<10}{"min/m":>10}{"max/m":>10}{"mean/m":>12}'
      f'{"rmse/m":>10}{"error/%":>10}')
tmpfile2.write(f'{"Method":<10}{"min/m":>10}{"max/m":>10}{"mean/m":>12}'
               f'{"rmse/m":>10}{"error/%":>10}\n')
methods = ["liv1", "liv2", 'idw', 'idwv2', 'nn']
for method, fn in zip(methods, sys.argv[2:]):
    diff = diff_list(sys.argv[1], fn)
    diff = np.array(diff)
    min_ = diff.min()
    max_ = diff.max()
    mean = diff.mean()
    rmse = math.sqrt(sum(diff**2) / diff.size)
    error = sum(abs(diff) > 3 * rmse) / diff.size * 100
    print(f'{method:<10}{min_:>10.2f}{max_:>10.2f}{mean:>12.6f}'
          f'{rmse:>10.2f}{error:>10.2f}')
    tmpfile2.write(f'{method:<10}{min_:>10.2f}{max_:>10.2f}{mean:>12.6f}'
                   f'{rmse:>10.2f}{error:>10.2f}\n')
