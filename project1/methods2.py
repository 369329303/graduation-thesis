import sys
import math
import time
import numpy as np
from scipy import spatial
from sklearn.linear_model import LinearRegression


def LI(i):
    '''
    使用线性插值法计算未知点高程值
    '''
    res = tree.query([contents[i][0], contents[i][1]], k)
    sum_z = 0
    for j in res[1]:
        sum_z += extracted_contents_a[j][2]
    return sum_z / len(res[1])


def IDW(i):
    '''
    使用反距离加权法计算未知点高程值
    '''
    res = tree.query([contents[i][0], contents[i][1]], k)
    m, n = 0, 0
    for d, j in zip(res[0], res[1]):
        n += 1 / d ** 2 * extracted_contents[j][2]
        m += 1 / d ** 2
    return n / m


def LR(i):
    '''
    Return predicated z value of point i.
    Local Linear Regression method.
    '''
    res = tree.query([contents[i][0], contents[i][1]], k)
    points = list()
    for j in res[1]:
        points.append(extracted_contents[j])
    model = LinearRegression()
    points = np.array(points)
    model.fit(points[:, 0:2], points[:, 2])
    pdt = model.predict([contents[i][0:2]])
    return pdt[0]


# Help information
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

# Store the time used to create KD tree which based on extracted_contents_array
start = time.time()
extracted_contents_a = np.array(extracted_contents)
tree = spatial.KDTree(extracted_contents_a[:, 0:2])
t0 = time.time() - start

# 查找一阶自然邻近点时，未知点邻居的数目
k = 8
for j in range(5, 8):
    start = time.time()
    with open('f' + str(j) + '.txt', 'w') as f:
        for i in range(len(contents)):
            if i % 2:
                cur = contents[i]
                if j == 5:
                    z = LI(i)
                    m_name = 'LI'
                elif j == 6:
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
