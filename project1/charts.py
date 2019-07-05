#!python3
# 图表显示
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

rmse, error = dict(), dict()
rmse2, error2 = dict(), dict()
rmse3, error3 = dict(), dict()

with open('report.txt', 'r') as f:
    for line in f:
        if not line[0].isalpha():
            continue
        sline = line.split()
        if sline[0] == 'LI':
            rmse['LI'] = float(sline[-2])
            error['LI'] = float(sline[-1])
        elif sline[0] == 'IDW':
            rmse['IDW'] = float(sline[-2])
            error['IDW'] = float(sline[-1])
        elif sline[0] == 'LR':
            rmse['LR'] = float(sline[-2])
            error['LR'] = float(sline[-1])

        elif sline[0] == 'LI2':
            rmse2['LI'] = float(sline[-2])
            error2['LI'] = float(sline[-1])
        elif sline[0] == 'IDW2':
            rmse2['IDW'] = float(sline[-2])
            error2['IDW'] = float(sline[-1])
        elif sline[0] == 'LR2':
            rmse2['LR'] = float(sline[-2])
            error2['LR'] = float(sline[-1])

        elif sline[0] == 'LI3':
            rmse3['LI'] = float(sline[-2])
            error3['LI'] = float(sline[-1])
        elif sline[0] == 'IDW3':
            rmse3['IDW'] = float(sline[-2])
            error3['IDW'] = float(sline[-1])
        elif sline[0] == 'LR3':
            rmse3['LR'] = float(sline[-2])
            error3['LR'] = float(sline[-1])


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
names = list(rmse3.keys())
values = list(rmse3.values())
plt.plot(names, values, '-s', label='Fixed radius')

names = list(rmse2.keys())
values = list(rmse2.values())
plt.plot(names, values, '-^', label='Fixed points')

names = list(rmse.keys())
values = list(rmse.values())
plt.plot(names, values, '-o', label='Adaptive method')

plt.legend()
plt.title('均方根误差')
plt.xlabel('Methods')
plt.ylabel('RMSE/m')


plt.subplot(122)
names = list(error3.keys())
values = list(error3.values())
plt.plot(names, values, '-s', label='Fixed radius')

names = list(error2.keys())
values = list(error2.values())
plt.plot(names, values, '-^', label='Fixed points')

names = list(error.keys())
values = list(error.values())
plt.plot(names, values, '-o', label='Adaptive method')


plt.legend()
plt.title('Gross Error Rate')
plt.xlabel('Methods')
plt.ylabel('Gross Error Rate/%')
plt.show()
