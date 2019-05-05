import sys
import math
import time
import numpy as np
from scipy import spatial


def distance(i, j):
    '''
    Return the distance of point i &  j.
    '''
    return math.sqrt(
        pow(contents[i][0] - contents[j][0], 2) +
        pow(contents[i][1] - contents[j][1], 2))


def within_range(tree, i, radius):
    '''
    Return all the points that lie in the circle of point i, with R=radius.
    '''
    in_range = list()
    res = tree.query_ball_point([contents[i][0], contents[i][1]], radius)
    for j in res:
        d = distance(i, 2 * j)
        z = extracted_contents[j][2]
        in_range.append([j, d, z])
    return in_range


def LIv1(i):
    '''
    Return predicated z value using linear interpolation version 1 method.
    '''
    previous = contents[i - 1]
    next_ = contents[i + 1] if i + 1 < len(contents) else previous
    return (previous[2] + next_[2]) / 2


def LIv2(i, radius):
    '''
    Return predicated z value of point i
    using linear interpolation version 2 method.
    '''
    in_range = within_range(tree, i, radius)
    sum_z = 0
    for record in in_range:
        sum_z += record[2]
    return sum_z / len(in_range) if len(in_range) != 0 else contents[i - 1][2]


def IDWv1(i, radius):
    '''
    Return predicated z value of point i
    using Inverse Distance Weighted method.
    '''
    in_range = within_range(tree, i, radius)
    m, n = 0, 0
    for i in range(len(in_range)):
        m += 1 / in_range[i][1]
        n += in_range[i][2] / in_range[i][1]
    return n / m if m != 0 else contents[i - 1][2]


def IDWv2(i, k=2):
    '''
    Return predicated z value of point i.
    First find k points that nearest point i.
    Then use IDW method to interpolate.
    '''
    res = NN(i, k)
    m, n = 0, 0
    for j in res:
        m += 1 / distance(i, 2 * j)
        n += contents[2 * j][2] / distance(i, 2 * j)
    return n / m if m != 0 else contents[i - 1][2]


def NN(i, k=1):
    '''
    Return (distance, index) if k == 1 else
           ([distance1, ...], [index1, ...])
    Nearest Neighbor for interpolation.
    '''
    res = tree.query([contents[i][0], contents[i][1]], k)
    return res[1]


# Help information
if len(sys.argv) != 3:
    print(f'Usage: {sys.argv[0]} <radius> <data.txt>')
    sys.exit(1)

radius = float(sys.argv[1])
contents, extracted_contents = list(), list()
flag = True
with open(sys.argv[2], 'r') as f:
    for line in f:
        sline = line.split()
        contents.append([float(sline[0]), float(sline[1]), float(sline[2])])
        if flag:
            extracted_contents.append(contents[-1])
        flag = not flag  # Switch between True and False

print(f'{"Method":<10}{"Time/s":>10}')

# Store the time used to create KD tree.
start = time.time()
extracted_contents_array = np.array(extracted_contents)
tree = spatial.KDTree(extracted_contents_array[:, 0:2])
t0 = time.time() - start

# LIv1 method
start = time.time()
with open('f1.txt', 'w') as f1:
    for i in range(len(contents)):
        if i % 2:
            cur = contents[i]
            z = LIv1(i)
            f1.write(f'{cur[0]}\t{cur[1]}\t{z}\n')
        else:
            f1.write('\t'.join(map(str, contents[i])) + '\n')
end = time.time()
print(f'{"LIv1":<10}{end-start:>10.2f}')

# LIv2 method
start = time.time()
with open('f2.txt', 'w') as f2:
    for i in range(len(contents)):
        if i % 2:
            cur = contents[i]
            z = LIv2(i, radius)
            f2.write(f'{cur[0]}\t{cur[1]}\t{z}\n')
        else:
            f2.write('\t'.join(map(str, contents[i])) + '\n')
end = time.time()
print(f'{"LIv2":<10}{end-start+t0:>10.2f}')

# IDWv1 method
start = time.time()
with open('f3.txt', 'w') as f3:
    for i in range(len(contents)):
        if i % 2:
            cur = contents[i]
            z = IDWv1(i, radius)
            f3.write(f'{cur[0]}\t{cur[1]}\t{z}\n')
        else:
            f3.write('\t'.join(map(str, contents[i])) + '\n')
end = time.time()
print(f'{"IDWv1":<10}{end-start+t0:>10.2f}')

# IDWv2 method
start = time.time()
with open('f4.txt', 'w') as f4:
    k = 3  # 3 neighbors
    for i in range(len(contents)):
        if i % 2:
            cur = contents[i]
            z = IDWv2(i, k)
            f4.write(f'{cur[0]}\t{cur[1]}\t{z}\n')
        else:
            f4.write('\t'.join(map(str, contents[i])) + '\n')
end = time.time()
print(f'{"IDWv2":<10}{end-start+t0:>10.2f}')

# NN method
start = time.time()
with open('f5.txt', 'w') as f5:
    for i in range(len(contents)):
        if i % 2:
            cur = contents[i]
            index = NN(i) * 2
            z = contents[index][2]
            f5.write(f'{cur[0]}\t{cur[1]}\t{z}\n')
        else:
            f5.write('\t'.join(map(str, contents[i])) + '\n')
end = time.time()
print(f'{"NN":<10}{end-start+t0:>10.2f}')
