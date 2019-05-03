import sys
import math
import time
import numpy as np
from scipy import spatial


# calculate the distance between contents[i] and contents[j]
def distance(i, j):
    return math.sqrt(pow(contents[i][0]-contents[j][0], 2) +
                     pow(contents[i][1]-contents[j][1], 2))


# find all the points that lie in the radius of limit around point i
def within_range(tree, i, radius):
    in_range = list()
    res = tree.query_ball_point(
        [contents[i][0], contents[i][1]], radius)
    for j in res:
        d = distance(i, 2*j)
        z = extracted_contents[j][2]
        in_range.append([j, d, z])
    return in_range


# calculate z value using linear interpolation version 1 method
def liv1(i):
    previous = contents[i - 1]
    next_ = contents[i + 1] if i + 1 < len(contents) else previous
    return (previous[2] + next_[2]) / 2


# calculate z value using linear interpolation version 2 method
def liv2(i, radius):
    in_range = within_range(tree, i, radius)
    sum_z = 0
    for record in in_range:
        sum_z += record[2]
    return sum_z / len(in_range) \
        if len(in_range) != 0 \
        else contents[i - 1][2]


# calculate z value using idw method
def idw(i, radius):
    in_range = within_range(tree, i, radius)
    m, n = 0, 0
    for i in range(len(in_range)):
        m += 1 / in_range[i][1]
        n += in_range[i][2] / in_range[i][1]
    return n / m if m != 0 else contents[i - 1][2]


if len(sys.argv) != 3:
    print(f'Usage: {sys.argv[0]} <radius> <data.txt>')
    sys.exit(1)

tmpfile1 = open('tmpfile1.txt', 'w')
radius = float(sys.argv[1])
contents, extracted_contents = list(), list()
flag = True
with open(sys.argv[2], 'r') as f:
    for line in f:
        sline = line.split()
        contents.append([float(sline[0]),
                         float(sline[1]),
                         float(sline[2])])
        if flag:
            extracted_contents.append(contents[-1])
            flag = False
        else:
            flag = True
print(f'{"Method":<10}{"Used-Time/s":>20}')
tmpfile1.write(f'{"Method":<10}{"Used-Time/s":>20}\n')

start = time.time()
with open('f1.txt', 'w') as f1:
    for i in range(len(contents)):
        if i % 2:
            cur = contents[i]
            z = liv1(i)
            f1.write(f'{cur[0]}\t{cur[1]}\t{z}\n')
        else:
            f1.write('\t'.join(map(str, contents[i])) + '\n')
end = time.time()
print(f'{"liv1":<10}{end-start:>20.2f}')
tmpfile1.write(f'{"liv1":<10}{end-start:>20.2f}\n')

start = time.time()
with open('f2.txt', 'w') as f2:
    extracted_contents_array = np.array(extracted_contents)
    tree = spatial.KDTree(extracted_contents_array[:, 0:2])
    for i in range(len(contents)):
        if i % 2:
            cur = contents[i]
            z = liv2(i, radius)
            f2.write(f'{cur[0]}\t{cur[1]}\t{z}\n')
        else:
            f2.write('\t'.join(map(str, contents[i])) + '\n')
end = time.time()
print(f'{"liv2":<10}{end-start:>20.2f}')
tmpfile1.write(f'{"liv2":<10}{end-start:>20.2f}\n')

start = time.time()
with open('f3.txt', 'w') as f3:
    extracted_contents_array = np.array(extracted_contents)
    tree = spatial.KDTree(extracted_contents_array[:, 0:2])
    for i in range(len(contents)):
        if i % 2:
            cur = contents[i]
            z = idw(i, radius)
            f3.write(f'{cur[0]}\t{cur[1]}\t{z}\n')
        else:
            f3.write('\t'.join(map(str, contents[i])) + '\n')
end = time.time()
print(f'{"idw":<10}{end-start:>20.2f}')
tmpfile1.write(f'{"idw":<10}{end-start:>20.2f}\n')
tmpfile1.close()
