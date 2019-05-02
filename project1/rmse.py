import sys
import math


if len(sys.argv) != 5:
    print(f'Usage: {sys.argv[0]} <data1.txt> <data2.txt> '
          f'<data3.txt> <data4.txt>')
    sys.exit(1)

# calculate RMSE of data1.txt and data2.txt
count = 0
sum_z12_square, sum_z13_square, sum_z14_square = 0, 0, 0
with open(sys.argv[1], 'r') as f1, \
     open(sys.argv[2], 'r') as f2, \
     open(sys.argv[3], 'r') as f3, \
     open(sys.argv[4], 'r') as f4:
    for line1, line2, line3, line4 in \
          zip(f1, f2, f3, f4):
        # Because even lines are the same,
        # we just deal with odd lines.
        if count % 2:
            z1 = float(line1.split()[2])
            z2 = float(line2.split()[2])
            z3 = float(line3.split()[2])
            z4 = float(line4.split()[2])
            sum_z12_square = pow(z2-z1, 2)
            sum_z13_square = pow(z3-z1, 2)
            sum_z14_square = pow(z4-z1, 2)
        count += 1
rmse12 = math.sqrt(sum_z12_square / count)
rmse13 = math.sqrt(sum_z13_square / count)
rmse14 = math.sqrt(sum_z14_square / count)
print(f'RMSE for {sys.argv[1]} and {sys.argv[2]} is:\t{rmse12:<.10}')
print(f'RMSE for {sys.argv[1]} and {sys.argv[3]} is:\t{rmse13:<.10}')
print(f'RMSE for {sys.argv[1]} and {sys.argv[4]} is:\t{rmse14:<.10}')
