#!python3
# 自定义搜索策略，插值方法LI, IDW, LR
import sys
import time
import numpy as np
from scipy import spatial
from scipy.spatial import Delaunay
from sklearn.linear_model import LinearRegression


def is_inMBR(p, MBR):
    '''
    判断点p是否位于MBR（最小外接矩形）内部
    '''
    if MBR[0] < p[0] < MBR[1] and \
       MBR[2] < p[1] < MBR[3]:
        return True
    else:
        return False


def distance_square(pA, pB):
    '''
    计算点pA，pB的水平距离的平方
    '''
    return pow(pA[0] - pB[0], 2) + pow(pA[1] - pB[1], 2)


def fun(i):
    point_loc = [contents[i][0], contents[i][1], 0]
    # 判断未知点是否位于Delaunay三角网的最小外接矩形内部
    if not is_inMBR(point_loc, MBR):  # 否，不需要在判断，直接用相邻点代替
        return [contents[i-1]]

    # 如果未知点位于Delaunay三角网的MBR内部，则计算未知点位于哪个小格网内
    i = int((point_loc[1] - MBR_down) // width)
    j = int((point_loc[0] - MBR_left) // width)
    if len(set_groups[i][j]) == 0:  # 如果格网不与任何三角形有关系，则用相邻点代替
        return [contents[i-1]]

    # 获取未知点的相关邻居点
    neighbors_a = extracted_contents_a[np.array(list(set_groups[i][j]))]
    # 利用未知点和其相关邻居点一起构建新的三角网
    tri_inner_a = np.append([point_loc], neighbors_a, axis=0)
    tri_inner = Delaunay(tri_inner_a[:, 0:2])
    # 查找未知点的一阶自然邻近点在新构建的局部三角网中的索引值
    set_new = set()
    for vertices in tri_inner.simplices:
        if 0 in vertices:
            set_new.update(vertices)
    set_new.remove(0)  # 删除掉未知点自身
    # 根据索引值找到完整x,y,z坐标数据
    points = list()
    for k in set_new:
        points.append(tri_inner_a[k])
    return points  # 返回未知点的一阶自然邻近点的x,y,z坐标数据


def NN(i):
    '''
    NN: Nearest Neighbors
    使用最近邻法计算未知点的高程值
    '''
    point_loc = [contents[i][0], contents[i][1]]
    res = tree.query(point_loc)
    return extracted_contents_a[res[1]][2]


def LI(i):
    '''
    LI: Linear Interpolation
    使用线性插值法计算未知点的高程值
    '''
    points = fun(i)
    sum_z = 0
    for point in points:
        sum_z += point[2]
    return sum_z / len(points)


def IDW(i):
    '''
    IDW: Inverse Distance Weighted
    使用反距离加权法计算未知点的高程值
    '''
    points = fun(i)
    m, n = 0, 0
    unknown_point = contents[i]
    for point in points:
        n += 1 / distance_square(unknown_point, point) * point[2]
        m += 1 / distance_square(unknown_point, point)
    return n / m


def LR(i):
    '''
    LR: Linear Regression method.
    使用线性回归法计算未知点的高程值
    '''
    points = fun(i)
    points_a = np.array(points)
    # 建立线性回归模型
    model = LinearRegression()
    # 用模型拟合未知点的邻居数据
    model.fit(points_a[:, 0:2], points_a[:, 2])
    # 利用模型预测未知点的高程值
    pdt = model.predict([contents[i][0:2]])
    return pdt[0]


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
# 利用 extracted_contents_a 建立 Delaunay 三角网
tri = Delaunay(extracted_contents_a[:, 0:2])
# 设置内部格网宽度为5m
width = 5
# 计算MBR的上下左右界限
MBR_left = tri.min_bound[0] // width * width
MBR_right = ((tri.max_bound[0] - 1) // width + 1) * width
MBR_down = tri.min_bound[1] // width * width
MBR_up = ((tri.max_bound[1] - 1) // width + 1) * width
MBR = [MBR_left, MBR_right, MBR_down, MBR_up]
# 计算Delaunay三角网的MBR内格网数量
rows = int((MBR_up - MBR_down) // width)
cols = int((MBR_right - MBR_left) // width)
# 对每个小格网都建立一个set集合,行和列均增加一组,
# 防止下一步为格网添加相关三角形时数组越界的情况
set_groups = [[set() for j in range(cols + 1)] for i in range(rows + 1)]

# 如果Delaunay三角网内某个三角形与某个格网相关，
# 则将这个三角形添加为这个格网的相关三角形
for t in tri.simplices:
    tri_inner_left = min(extracted_contents_a[t][:, 0]) // width * width
    tri_inner_right = ((max(extracted_contents_a[t][:, 0]) - 1) // width + 1) * width
    tri_inner_down = min(extracted_contents_a[t][:, 1]) // width * width
    tri_inner_up = ((max(extracted_contents_a[t][:, 1]) - 1) // width + 1) * width
    C = int((tri_inner_down - MBR_down) // width)
    D = int((tri_inner_up - MBR_down) // width) + 1
    A = int((tri_inner_left - MBR_left) // width)
    B = int((tri_inner_right - MBR_left) // width) + 1
    for i in range(C, D):
        for j in range(A, B):
            set_groups[i][j].update(t)

for j in range(2, 5):
    start = time.time()
    with open('f' + str(j) + '.txt', 'w') as f:
        for i in range(len(contents)):
            if i % 2:
                cur = contents[i]
                if j == 2:
                    z = LI(i)
                    m_name = 'LI'
                elif j == 3:
                    z = IDW(i)
                    m_name = 'IDW'
                elif j == 4:
                    z = LR(i)
                    m_name = 'LR'
                f.write(f'{cur[0]}\t{cur[1]}\t{z}\n')
            else:
                f.write('\t'.join(map(str, contents[i])) + '\n')
    end = time.time()
    print(f'{m_name:<10}{end-start+t0:>10.2f}')
