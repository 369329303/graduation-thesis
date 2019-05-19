import sys
import time
import numpy as np
from scipy import spatial
from sklearn.linear_model import LinearRegression
from first_order_natural_neighbor import first_order_natural_neighbor


def distance_square(pA, pB):
    '''
    计算点A，B的水平距离的平方
    '''
    return pow(pA[0] - pB[0], 2) + pow(pA[1] - pB[1], 2)


def LI(i):
    '''
    LI: Linear Interpolation
    使用线性插值法计算未知点的高程值
    '''
    points = first_order_natural_neighbor(contents, extracted_contents_a, tree,
                                          i, neighbors)
    sum_z = 0
    for point in points:
        sum_z += point[2]
    return sum_z / len(points)


def IDW(i):
    '''
    IDW: Inverse Distance Weighted
    使用反距离加权法计算未知点的高程值
    '''
    points = first_order_natural_neighbor(contents, extracted_contents_a, tree,
                                          i, neighbors)
    m, n = 0, 0
    unknown_point = contents[i]
    for point in points:
        n += 1 / distance_square(unknown_point, point) * point[2]
        m += 1 / distance_square(unknown_point, point)
    return n / m


def NN(i):
    '''
    NN: Nearest Neighbors
    使用最近邻法计算未知点的高程值
    '''
    point_loc = [contents[i][0], contents[i][1]]
    res = tree.query(point_loc)
    return extracted_contents_a[res[1]][2]


def LR(i):
    '''
    LR: Linear Regression method.
    使用线性回归法计算未知点的高程值
    '''
    points = first_order_natural_neighbor(contents, extracted_contents_a, tree,
                                          i, neighbors)
    # 建立线性回归模型
    model = LinearRegression()
    points_a = np.array(points)
    # 用模型拟合未知点的邻居数据
    model.fit(points_a[:, 0:2], points_a[:, 2])
    # 利用模型预测未知点的高程值
    pdt = model.predict([contents[i][0:2]])
    return pdt[0]


# 帮助信息
if len(sys.argv) != 2:
    print(f'Usage: {sys.argv[0]} <data.txt>')
    sys.exit(1)

# contents 中存放着原始精度数据
# extracted_contents 中存放着精度降低一半的数据
contents, extracted_contents = list(), list()
flag = True
with open(sys.argv[1], 'r') as f:
    for line in f:
        sline = line.split()
        contents.append([float(sline[0]), float(sline[1]), float(sline[2])])
        if flag:
            extracted_contents.append(contents[-1])
        flag = not flag  # 在 True 和 False 之间切换

print(f'{"Method":<10}{"Time/s":>10}')

# 存储用于建立KD树的时间。KD树是根据 extracted_contents_a 建立的。
start = time.time()
extracted_contents_a = np.array(extracted_contents)
tree = spatial.KDTree(extracted_contents_a[:, 0:2])
t0 = time.time() - start
# 查找一阶自然邻近点时，未知点邻居的数目
neighbors = 8

for j in range(1, 5):
    start = time.time()
    with open('f' + str(j) + '.txt', 'w') as f:
        for i in range(len(contents)):
            if i % 2:
                cur = contents[i]
                if j == 1:
                    z = LI(i)
                elif j == 2:
                    z = IDW(i)
                elif j == 3:
                    z = NN(i)
                else:
                    z = LR(i)
                f.write(f'{cur[0]}\t{cur[1]}\t{z}\n')
            else:
                f.write('\t'.join(map(str, contents[i])) + '\n')
    end = time.time()
    print(f'{j:<10}{end-start+t0:>10.2f}')
