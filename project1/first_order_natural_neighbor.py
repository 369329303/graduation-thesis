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

def first_order_natural_neighbor(contents, extracted_contents_a,
                                 tree, i, neighbors):
    '''
    返回点 i 的一阶自然近邻点的x,y,z坐标值
    '''
    # 未知点的x,y坐标
    point_loc = [contents[i][0], contents[i][1]]
    res = tree.query(point_loc, neighbors)
    # 未知点的邻居的x,y,z坐标值
    tri_a = extracted_contents_a[res[1]]
    # 未知点的邻居所构建的Delaunay三角网
    tri = Delaunay(tri_a[:, 0:2])

    # MBR: Minimum Bounding Rectangle 最小外接矩形
    # width: 格网宽度
    # 计算Delaunay三角网的MBR的上下左右界限
    width = 5
    MBR_left = tri.min_bound[0] // width * width
    MBR_right = ((tri.max_bound[0] - 1) // width + 1) * width
    MBR_down = tri.min_bound[1] // width * width
    MBR_up = ((tri.max_bound[1] - 1) // width + 1) * width
    MBR = [MBR_left, MBR_right, MBR_down, MBR_up]
    # 给未知点添加假z值，以便和其邻居数据格式统一，便于处理
    point_loc.append(0)
    # 判断未知点是否位于Delaunay三角网内部
    if not is_inMBR(point_loc, MBR):  # 否，不需要在判断，直接用最近邻点代替
        res = tree.query([point_loc[0:2]])
        return extracted_contents_a[res[1]]  # 返回最近邻点的x,y,z坐标数据

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
    i = int((point_loc[0] - MBR_left) // width +
            (point_loc[1] - MBR_down) // width * cols)
    # 如果格网不与任何三角形有关系，则用最近邻点代替
    if len(set_group[i]) == 0:
        res = tree.query([point_loc[0:2]])
        return extracted_contents_a[res[1]]  # 返回最近邻点的x,y,z坐标数据

    # 获取未知点的相关邻居点
    tri_new_a = tri_a[np.array(list(set_group[i]))]
    # 利用未知点和其相关邻居点一起重新构建三角网
    tri_new_a = np.append([point_loc], tri_new_a, axis=0)
    tri_new = Delaunay(tri_new_a[:, 0:2])
    # 查找未知点的一阶自然邻近点在新构建的三角网中的索引值
    set_new = set()
    for vertices in tri_new.simplices:
        if 0 in vertices:
            set_new.update(vertices)
    set_new.remove(0)  # 删除掉未知点自身
    # 根据索引值找到完整x,y,z坐标数据
    points = list()
    for i in set_new:
        points.append(tri_new_a[i])
    return points  # 返回未知点的一阶自然邻近点的x,y,z坐标数据
