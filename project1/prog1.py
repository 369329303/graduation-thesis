import sys
import math
import time


# difference between contents[i].split()[column] -
# contents[j].split()[column]
def diff(contents, i, j, column):
    return float(contents[i].split()[column]) - \
        float(contents[j].split()[column])


# calculate the distance between contents[i] and contents[j]
def distance(contents, i, j):
    return math.sqrt(
        pow(diff(contents, i, j, 0), 2) +
        pow(diff(contents, i, j, 1), 2))


# find all the points that lie in the radius of limit around point i
def within_range(contents, i, limit):
    in_range = list()
    for j in range(0, len(contents), 2):
        if abs(diff(contents, i, j, 0)) > limit \
           or abs(diff(contents, i, j, 1)) > limit:
            continue
        if pow(diff(contents, i, j, 0), 2) + \
           pow(diff(contents, i, j, 1), 2) > \
           pow(limit, 2):
            continue
        d = distance(contents, i, j)
        in_range.append([j, d, float(contents[j].split()[2])])
    return in_range


# calculate z value using linear interpolation version 1 method
def liv1(contents, i):
    previous = contents[i - 1].split()
    next_ = contents[i + 1].split() if i + 1 < len(contents) else previous
    return (float(previous[2]) + float(next_[2])) / 2


# calculate z value using linear interpolation version 2 method
def liv2(contents, i, limit):
    in_range = within_range(contents, i, limit)
    sum_z = 0
    for record in in_range:
        sum_z += record[2]
    return sum_z / len(in_range) if len(in_range) != 0 else contents[
        i - 1].split()[2]


# calculate z value using idw method
def idw(contents, i, limit):
    in_range = within_range(contents, i, limit)
    m, n = 0, 0
    for i in range(len(in_range)):
        m += 1 / in_range[i][1]
        n += in_range[i][2] / in_range[i][1]
    return n / m if m != 0 else contents[i - 1].split()[2]


if len(sys.argv) != 3:
    print(f'Usage: {sys.argv[0]} <limit> <data.txt>')
    sys.exit(1)

contents = list()
limit = float(sys.argv[1])
with open(sys.argv[2], 'r') as f:
    for line in f:
        contents.append(line)

start = time.time()
with open('f1.txt', 'w') as f1:
    for i in range(len(contents)):
        if i % 2:
            cur = contents[i].split()
            z = liv1(contents, i)
            f1.write(f'{cur[0]}\t{cur[1]}\t{z}\n')
        else:
            f1.write(contents[i])
end = time.time()
print(f'Time for liv1 method:\t{end-start:<20.10}s.')

start = time.time()
with open('f2.txt', 'w') as f2:
    for i in range(len(contents)):
        if i % 2:
            cur = contents[i].split()
            z = liv2(contents, i, limit)
            f2.write(f'{cur[0]}\t{cur[1]}\t{z}\n')
        else:
            f2.write(contents[i])
end = time.time()
print(f'Time for liv2 method:\t{end-start:<20.10}s.')

start = time.time()
with open('f3.txt', 'w') as f3:
    for i in range(len(contents)):
        if i % 2:
            cur = contents[i].split()
            z = idw(contents, i, limit)
            f3.write(f'{cur[0]}\t{cur[1]}\t{z}\n')
        else:
            f3.write(contents[i])
end = time.time()
print(f'Time for idw  method:\t{end-start:<20.10}s.')
