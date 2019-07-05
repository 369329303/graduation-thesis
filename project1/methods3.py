#!python3
# 半径固定的搜索策略，插值方法LI, IDW, LR

import sys
import math
import time
import numpy as np
from scipy import spatial
from sklearn.linear_model import LinearRegression


def distance(i, j):
    '''
    返回点i, j的水平距离
    '''
    return math.sqrt(pow(contents[i][0]-contents[j][0], 2) +
                     pow(contents[i][1]-contents[j][1], 2))


def within_range(i):
    '''
    返回所有点i周围一定范围内的点
    '''
    in_range = list()
    res = tree.query_ball_point([contents[i][0], contents[i][1]],
                                radius)
    for j in res:
        d = distance(i, 2*j)
        z = extracted_contents[j][2]
        in_range.append([j, d, z])
    return in_range


def LI(i):
    '''
    使用线性插值法计算未知点高程值
    '''
    in_range = within_range(i)
    if len(in_range) == 0:
        return contents[i-1][2]
    sum_z = 0
    for item in in_range:
        sum_z += item[2]
    return sum_z / len(in_range)


def IDW(i):
    '''
    使用反距离加权法计算未知点高程值
    '''
    in_range = within_range(i)
    if len(in_range) == 0:
        return contents[i-1][2]
    m, n = 0, 0
    for [j, d, z] in in_range:
        n += 1 / d ** 2 * z
        m += 1 / d ** 2
    return n / m


def LR(i):
    '''
    Linear Regression.
    使用线性回归法计算未知点的高程值
    '''
    in_range = within_range(i)
    if len(in_range) == 0:
        return contents[i-1][2]
    points = list()
    for [j, d, z] in in_range:
        points.append(extracted_contents[j])
    model = LinearRegression()
    points_a = np.array(points)
    model.fit(points_a[:, 0:2], points_a[:, 2])
    pdt = model.predict([contents[i][0:2]])
    return pdt[0]


# 帮助信息
if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} <data.txt>')
    sys.exit(1)

contents, extracted_contents = list(), list()
flag = True
with open(sys.argv[1], 'r') as f:
    for line in f:
        sline = line.split()
        contents.append([float(sline[0]), float(sline[1]), float(sline[2])])
        if flag:
            extracted_contents.append(contents[-1])
        flag = not flag  # Switch between True and False

print(f'{"Method":<10}{"Time/s":>10}')

# 存储用于建立KD树的时间，KD树是用extracted_contents_a建立的
start = time.time()
extracted_contents_a = np.array(extracted_contents)
tree = spatial.KDTree(extracted_contents_a[:, 0:2])
t0 = time.time() - start

# 半径固定
radius = 50
for j in range(8, 11):
    start = time.time()
    with open('f' + str(j) + '.txt', 'w') as f:
        for i in range(len(contents)):
            if i % 2:
                cur = contents[i]
                if j == 8:
                    z = LI(i)
                    m_name = 'LI'
                elif j == 9:
                    z = IDW(i)
                    m_name = 'IDW'
                else:
                    z = LR(i)
                    m_name = 'LR'
                f.write(f'{cur[0]}\t{cur[1]}\t{z}\n')
            else:
                f.write('\t'.join(map(str, contents[i])) + '\n')
    end = time.time()
    print(f'{m_name:<10}{end-start+t0:>10.2f}')
