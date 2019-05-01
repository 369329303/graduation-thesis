#!/usr/local/bin/python3

import sys
import math


if len(sys.argv) != 1:
    print(f'Usage: {sys.argv[0]} <data1.txt> <data2.txt>')
    sys.exit(1)

count, sum_z_square = 0, 0
with open(sys.argv[1], 'r') as f1, \
     open(sys.argv[2], 'r') as f2:
    for line1, line2 in zip(f1, f2):
        if count % 2:
            z1 = line1.split()[2]
            z2 = line2.split()[2]
            sum_z_square = pow(float(z1)-float(z2), 2)
        count += 1
rmse = math.sqrt(sum_z_square / (count//2))
print(f'RMSE for {sys.argv[1]} and {sys.argv[2]} is:\t{rmse}')
