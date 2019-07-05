#!python3
# 图表显示
import matplotlib.pyplot as plt

max_, mean_ = dict(), dict()
max_2, mean_2 = dict(), dict()
max_3, mean_3 = dict(), dict()

with open('report.txt', 'r') as f:
    for line in f:
        if not line[0].isalpha():
            continue
        sline = line.split()
        if sline[0] == 'LI':
            max_['LI'] = float(sline[3])
            mean_['LI'] = float(sline[4])
        elif sline[0] == 'IDW':
            max_['IDW'] = float(sline[3])
            mean_['IDW'] = float(sline[4])
        elif sline[0] == 'LR':
            max_['LR'] = float(sline[3])
            mean_['LR'] = float(sline[4])

        elif sline[0] == 'LI2':
            max_2['LI'] = float(sline[3])
            mean_2['LI'] = float(sline[4])
        elif sline[0] == 'IDW2':
            max_2['IDW'] = float(sline[3])
            mean_2['IDW'] = float(sline[4])
        elif sline[0] == 'LR2':
            max_2['LR'] = float(sline[3])
            mean_2['LR'] = float(sline[4])

        elif sline[0] == 'LI3':
            max_3['LI'] = float(sline[3])
            mean_3['LI'] = float(sline[4])
        elif sline[0] == 'IDW3':
            max_3['IDW'] = float(sline[3])
            mean_3['IDW'] = float(sline[4])
        elif sline[0] == 'LR3':
            max_3['LR'] = float(sline[3])
            mean_3['LR'] = float(sline[4])


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
names = list(max_3.keys())
values = list(max_3.values())
plt.plot(names, values, '-s', label='Fixed radius')

names = list(max_2.keys())
values = list(max_2.values())
plt.plot(names, values, '-^', label='Fixed points')

names = list(max_.keys())
values = list(max_.values())
plt.plot(names, values, '-o', label='Adaptive method')

plt.legend()
plt.title('Max')
plt.xlabel('Methods')
plt.ylabel('Max/m')


plt.subplot(122)
names = list(mean_3.keys())
values = list(mean_3.values())
plt.plot(names, values, '-s', label='Fixed radius')

names = list(mean_2.keys())
values = list(mean_2.values())
plt.plot(names, values, '-^', label='Fixed points')

names = list(mean_.keys())
values = list(mean_.values())
plt.plot(names, values, '-o', label='Adaptive method')


plt.axhline(0, color='black', lw=2)

plt.legend()
plt.title('Mean')
plt.xlabel('Methods')
plt.ylabel('Mean/m')
plt.show()
