import sys
import math
import time
import numpy as np
from scipy import spatial


def distance(i, j):
    '''
    Return the distance between contents[i] and contents[j]
    '''
    return math.sqrt(
        pow(contents[i][0] - contents[j][0], 2) +
        pow(contents[i][1] - contents[j][1], 2))


def new_z(indecies, i):
    '''
    Return the predicate z value of point i.
    '''
    m, n = 0, 0
    for j in indecies:
        m += 1 / distance(i, 2 * j)
        n += contents[2 * j][2] / distance(i, 2 * j)
    return n / m if m != 0 else contents[i - 1][2]


def NN(i, k=1):
    '''
    Nearest Neighbor for interpolation.
    Return the index of nearest neighbor in the tree.
    return (distance, index) if k == 1 else
           ([distance1, ...], [index1, ...])
    '''
    res = tree.query([contents[i][0], contents[i][1]], k)
    return res[1]


def NNTest(k):
    '''
    Test for k Nearest Neighbors.
    '''
    start = time.time()
    with open('NN-' + str(k) + '.txt', 'w') as f:
        for i in range(len(contents)):
            if i % 2:
                cur = contents[i]
                indecies = NN(i, k)
                if k == 1:
                    z = contents[indecies * 2][2]
                else:
                    z = new_z(indecies, i)
                f.write(f'{cur[0]}\t{cur[1]}\t{z}\n')
            else:
                f.write('\t'.join(map(str, contents[i])) + '\n')
    end = time.time()
    print(f'{"NN-"+str(k):<10}{end-start+t0:>10.2f}')


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
            flag = False
        else:
            flag = True
print(f'{"Method":<10}{"Time/s":>10}')

start = time.time()
extracted_contents_array = np.array(extracted_contents)
tree = spatial.KDTree(extracted_contents_array[:, 0:2])
t0 = time.time() - start

k_a = [i+1 for i in range(10)]
for k in k_a:
    NNTest(k)
