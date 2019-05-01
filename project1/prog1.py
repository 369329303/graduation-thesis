#!/usr/local/bin/python3
import sys
import math


# calculate the distance between contents[i] and contents[j]
def distance(contents, i, j):
    li = contents[i].split()
    lj = contents[j].split()
    return math.sqrt(
        pow(float(li[0]) - float(lj[0]), 2) +
        pow(float(li[1]) - float(lj[1]), 2))


def within_range(contents, i, limit):
    in_range = list()
    for j in range(0, len(contents), 2):
        if abs(float(contents[j].split()[0]) - float(contents[i].split()[0])) > limit \
           or abs(float(contents[j].split()[1]) - float(contents[i].split()[0])) > limit:
            continue
        if pow(float(contents[j].split()[0]), 2) + pow(float(contents[j].split()[1]), 2) \
           > pow(limit, 2) \
           or pow(float(contents[j].split()[1]), 2) + pow(float(contents[j].split()[2]), 2) \
           > pow(limit, 2):
            continue
        d = distance(contents, i, j)
        in_range.append([j, d, float(contents[j].split()[2])])
    return in_range


# calculate z value using idw method
def idw(contents, i, limit):
    in_range = within_range(contents, i, limit)
    m, n = 0, 0
    for i in range(len(in_range)):
        m += 1 / in_range[i][1]
        n += in_range[i][2] / in_range[i][1]
    return n / m if m != 0 else contents[i-1].split()[2]


# calculate z value using linear interpolation version 2 method
def liv2(contents, i, limit):
    n, z = 0, 0
    j = i - 1
    while True:
        if j >= 0 and distance(contents, i, j) <= limit:
            n += 1
            z += float(contents[j].split()[2])
            j -= 2
        else:
            break
    j = i + 1
    while True:
        if j <= len(contents) and distance(contents, i, j) <= limit:
            n += 1
            z += float(contents[j].split()[2])
            j += 2
        else:
            break
    return z / n


contents = list()
with open('sample.txt', 'r') as f:
    for line in f:
        contents.append(line)

limit = 15
with open('f3.txt', 'w') as f3:
    for i in range(len(contents)):
        if i % 2:
            cur = contents[i].split()
            z = idw(contents, i, limit)
            f3.write(f'{cur[0]}\t{cur[1]}\t{z}\n')
        else:
            f3.write(contents[i])

sys.exit(1)
# linear interpolation version 1 method
with open('f2.txt', 'w') as f2:
    for i in range(len(contents)):
        if i % 2:
            cur = contents[i].split()
            z = liv2(contents, i, limit)
            f2.write(f'{cur[0]}\t{cur[1]}\t{z}\n')
        else:
            f2.write(contents[i])

sys.exit(1)
# linear interpolation version 1 method
with open('f1.txt', 'w') as f1:
    for i in range(len(contents)):
        if i % 2:
            up = contents[i - 1].split()
            cur = contents[i].split()
            down = contents[i + 1].split()
            z = (float(up[2]) + float(down[2])) / 2
            f1.write(f'{cur[0]}\t{cur[1]}\t{z}\n')
            pass
        else:
            f1.write(contents[i])
