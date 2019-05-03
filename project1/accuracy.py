import sys
import math
import statistics
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

print(f'{"Method":<10}{"min/m":>10}{"max/m":>20}{"mean/m":>20}'
      f'{"rmse/m":>20.6}{"gross_error_rate/%":>20}')
methods = ["liv1", "liv2", 'idw']
for method, fn in zip(methods, sys.argv[2:]):
    diff = diff_list(sys.argv[1], fn)
    diff = np.array(diff)
    min_ = diff.min()
    max_ = diff.max()
    mean = diff.mean()
    rmse = math.sqrt(sum(diff**2) / diff.size)
    gross_error_rate = sum(abs(diff) > 3 * rmse) / diff.size
    print(f'{method:<10}{min_:>10.6}{max_:>20.6}{mean:>20.6}'
          f'{rmse:>20.6}{gross_error_rate*100:>20.6}')