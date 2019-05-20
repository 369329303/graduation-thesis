import random


with open('new_source.txt', 'r') as f1, \
     open('new_source2.txt', 'w') as f2:
    for line in f1:
        if random.random() > 0.4:
            f2.write(line)
