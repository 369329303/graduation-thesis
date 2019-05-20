import sys
import math
import numpy as np


def diff_s(file1, file2):
    '''
    Return [(z2-z1), ...] for z1 in file1, z2 in file2.
    '''
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


# 帮助信息
if len(sys.argv) < 3:
    print(f'Usage: {sys.argv[0]} <data1.txt> <data2.txt> ...')
    sys.exit(1)

files = sys.argv[2:]

print(f'{"Method":<10}{"min/m":>10}'
      f'{"max/m":>10}{"mean/m":>12}'
      f'{"rmse/m":>10}{"error/%":>10}')

methods = ['NN', 'LI', 'IDW', 'LR']
for method, fn in zip(methods, files):
    diff_a = np.array(diff_s(sys.argv[1], fn))
    min_ = diff_a.min()
    max_ = diff_a.max()
    mean = diff_a.mean()
    rmse = diff_a.std()
    error = sum(abs(diff_a) > 3 * rmse) / diff_a.size * 100
    print(f'{method:<10}{min_:>10.2f}'
          f'{max_:>10.2f}{mean:>12.6f}'
          f'{rmse:>10.2f}{error:>10.2f}')
