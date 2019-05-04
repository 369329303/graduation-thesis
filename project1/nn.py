def NN(i, k=1):
    '''
    Nearest Neighbor for interpolation.
    Return the index of nearest neighbor in the tree.
    return (distance, index) if k == 1 else
           ([distance1, ...], [index1, ...])
    '''
    res = tree.query([contents[i][0], contents[i][1]], k)
    return res[1]

contents, extracted_contents = list(), list()
flag = True
with open(sys.argv[2], 'r') as f:
    for line in f:
        sline = line.split()
        contents.append([float(sline[0]),
                         float(sline[1]),
                         float(sline[2])])
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
