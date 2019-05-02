import sys
import math


def accuracy(file1, file2):
    '''
    calculate RMSE, min_, max_, mean_ values for file1 and file2
    - RMSE: 	Root Mean Square Error
    - min_: 	minimum value of (z2-z1)
    - max_: 	maximum value of (z2-z1)
    - mean_: 	mean value of (z2-z1)
    '''
    count, sum_z12, sum_z12_square = 0, 0, 0
    min_, max_, mean_ = math.inf, -math.inf, 0
    with open(file1, 'r') as f1, \
         open(file2, 'r') as f2:
        for line1, line2 in zip(f1, f2):
            if count % 2:
                z1 = float(line1.split()[2])
                z2 = float(line2.split()[2])
                sum_z12 += z2 - z1
                sum_z12_square += pow(z2 - z1, 2)
                if z2 - z1 < min_:
                    min_ = z2 - z1
                if z2 - z1 > max_:
                    max_ = z2 - z1
            count += 1
    mean_ = sum_z12 / count
    rmse = math.sqrt(sum_z12_square / count)
    return [rmse, min_, max_, mean_]


if len(sys.argv) < 3:
    print(f'Usage: {sys.argv[0]} <data1.txt> <data2.txt> ...')
    sys.exit(1)

print(f'{"Method":^10}{"RMSE":^20}{"min":^20}{"max":^20}{"mean":^20}')
methods = ["liv1", "liv2", 'idw']
for method, fn in zip(methods, sys.argv[2:]):
    [rmse, min_, max_, mean_] = accuracy(sys.argv[1], fn)
    print(f'{method:<10}{rmse:>20.6}{min_:>20.6}{max_:>20.6}{mean_:>20.6}')
