import sys
import math
import numpy as np
from scipy import spatial
from scipy.spatial import Delaunay
import matplotlib.pyplot as plt


def is_related(box, mbr):
    '''
    判断box和mbr是否有接触
    '''
    if box[0] >= mbr[1] or box[1] <= mbr[0] or \
       box[2] >= mbr[3] or box[3] <= mbr[2]:
        return False
    else:
        return True


def is_inMBR(p, MBR):
    '''
    判断点p是否位于MBR（最小外接矩形）内部
    '''
    if MBR[0] < p[0] < MBR[1] and \
       MBR[2] < p[1] < MBR[3]:
        return True
    else:
        return False


contents, extracted_contents = list(), list()
flag = True
with open(sys.argv[1], 'r') as f:
    for line in f:
        sline = line.split()
        contents.append([float(sline[0]), float(sline[1]), float(sline[2])])
        if flag:
            extracted_contents.append(contents[-1])
        flag = not flag  # 在 True 和 False 值之间切换

# extracted_contents = contents
extracted_contents_a = np.array(extracted_contents)
# 对筛选过的数据构造kd树
tree = spatial.KDTree(extracted_contents_a[:, 0:2])
# 未知点的x,y坐标
point_loc = [contents[3][0], contents[3][1]]
# 未知点的邻居数目
neighbors = 9
res = tree.query(point_loc, neighbors)
# 未知点的邻居的x,y,z坐标值
tri_a = extracted_contents_a[res[1]]
# 未知点的邻居所构建的Delaunay三角网
tri = Delaunay(tri_a[:, 0:2])
# plt.triplot(tri_a[:, 0], tri_a[:, 1])
# plt.plot(tri_a[:, 0], tri_a[:, 1], 'o')
# plt.plot(point_loc[0], point_loc[1], 'yo')
# plt.grid()
# plt.show()
# MBR: Minimum Bounding Rectangle 最小外接矩形
# width: 格网宽度
# 设置Delaunay三角网的MBR的上下左右界限
width = 5
MBR_left = tri.min_bound[0] // width * width
MBR_right = ((tri.max_bound[0] - 1) // width + 1) * width
MBR_down = tri.min_bound[1] // width * width
MBR_up = ((tri.max_bound[1] - 1) // width + 1) * width
MBR = [MBR_left, MBR_right, MBR_down, MBR_up]
# 给未知点添加假z值，以便和其邻居x,y,z坐标数据的统一处理
p = point_loc + [0]
# 判断未知点是否位于Delaunay三角网内部
if not is_inMBR(p, MBR):  # 否，不需要在进行下去，直接用最近邻点代替
    tree.query([p[0:2]], 1)
    sys.exit(0)

# 计算Delaunay三角网的MBR内格网数量
rows = int((MBR_up - MBR_down) // width)
cols = int((MBR_right - MBR_left) // width)
# 对每个小格网都建立一个set集合
set_group = [set() for i in range(rows * cols)]

# 如果Delaunay三角网中某个三角形与某个格网相关，
# 则将这个三角形添加为这个格网的相关三角形
for t in tri.simplices:
    tri_left = min(tri_a[t][:, 0]) // width * width
    tri_right = ((max(tri_a[t][:, 0]) - 1) // width + 1) * width
    tri_down = min(tri_a[t][:, 1]) // width * width
    tri_up = ((max(tri_a[t][:, 1]) - 1) // width + 1) * width
    for i in range(rows * cols):
        box_left = MBR_left + (i % cols) * width
        box_down = MBR_down + i // cols * width
        box = [box_left, box_left + width, box_down, box_down + width]
        mbr = [tri_left, tri_right, tri_down, tri_up]
        if is_related(box, mbr):
            set_group[i].update(t)

# 如果未知点位于Delaunay三角网的MBR内部，则计算未知点位于哪个小格网内
i = int((p[0] - MBR_left) // width + (p[1] - MBR_down) // width * cols)
print(i)
print(set_group[i])
# 获取未知点的相关邻居点
tri_new_a = tri_a[np.array(list(set_group[i]))]
# 利用未知点和其相关邻居点一起重新构建三角网
tri_new_a = np.append([p], tri_new_a, axis=0)
tri_new = Delaunay(tri_new_a[:, 0:2])
# 查找未知点的一阶自然邻近点
set_new = set()
for vertices in tri_new.simplices:
    if 0 in vertices:
        set_new.update(vertices)
set_new.remove(0)

for i in set_new:
    print(tri_new_a[i])
