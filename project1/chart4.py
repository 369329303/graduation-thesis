#!python3
# 图表显示
import matplotlib.pyplot as plt

time_, min_ = dict(), dict()
time_2, min_2 = dict(), dict()
time_3, min_3 = dict(), dict()

with open('report.txt', 'r') as f:
    for line in f:
        if not line[0].isalpha():
            continue
        sline = line.split()
        if sline[0] == 'LI':
            time_['LI'] = float(sline[1])
            min_['LI'] = float(sline[2])
        elif sline[0] == 'IDW':
            time_['IDW'] = float(sline[1])
            min_['IDW'] = float(sline[2])
        elif sline[0] == 'LR':
            time_['LR'] = float(sline[1])
            min_['LR'] = float(sline[2])

        elif sline[0] == 'LI2':
            time_2['LI'] = float(sline[1])
            min_2['LI'] = float(sline[2])
        elif sline[0] == 'IDW2':
            time_2['IDW'] = float(sline[1])
            min_2['IDW'] = float(sline[2])
        elif sline[0] == 'LR2':
            time_2['LR'] = float(sline[1])
            min_2['LR'] = float(sline[2])

        elif sline[0] == 'LI3':
            time_3['LI'] = float(sline[1])
            min_3['LI'] = float(sline[2])
        elif sline[0] == 'IDW3':
            time_3['IDW'] = float(sline[1])
            min_3['IDW'] = float(sline[2])
        elif sline[0] == 'LR3':
            time_3['LR'] = float(sline[1])
            min_3['LR'] = float(sline[2])


# Parameters for setting figure
params = {
    'axes.titlesize': 30,
    'axes.labelsize': 20,
    'lines.linewidth': 2,
    'lines.markersize': 10,
    'xtick.labelsize': 20,
    'ytick.labelsize': 20,
    'legend.fontsize': 20
}
plt.rcParams.update(params)

plt.subplot(121)
names = list(time_3.keys())
values = list(time_3.values())
plt.plot(names, values, '-s', label='Fixed radius')

names = list(time_2.keys())
values = list(time_2.values())
plt.plot(names, values, '-^', label='Fixed points')

names = list(time_.keys())
values = list(time_.values())
plt.plot(names, values, '-o', label='Adaptive method')

plt.legend()
plt.title('Time')
plt.xlabel('Methods')
plt.ylabel('Time/s')


plt.subplot(122)
names = list(min_3.keys())
values = list(min_3.values())
plt.plot(names, values, '-s', label='Fixed radius')

names = list(min_2.keys())
values = list(min_2.values())
plt.plot(names, values, '-^', label='Fixed points')

names = list(min_.keys())
values = list(min_.values())
plt.plot(names, values, '-o', label='Adaptive method')


plt.legend()
plt.title('Min')
plt.xlabel('Methods')
plt.ylabel('min/m')
plt.show()
