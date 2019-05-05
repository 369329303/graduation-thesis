import matplotlib.pyplot as plt

neighbors_a = list()
rmse_a = list()
error_a = list()

with open('report2.txt', 'r') as f:
    for line in f:
        if line.startswith('NN'):
            sline = line.split()
            neighbors_a.append(float(sline[0][3:]))
            rmse_a.append(float(sline[-2]))
            error_a.append(float(sline[-1]))

params = {
    'axes.titlesize': 30,
    'axes.labelsize': 20,
    'lines.linewidth': 1,
    'lines.markersize': 10,
    'xtick.labelsize': 16,
    'ytick.labelsize': 16,
    'legend.fontsize': 16
}
plt.rcParams.update(params)

plt.subplot(121)
plt.plot(neighbors_a, rmse_a, 'k^-', label='RMSE')
plt.title('RMSE vs. neighbors')
plt.xlabel('neighbors/count')
plt.ylabel('RMSE/m')
plt.legend()

plt.subplot(122)
plt.plot(neighbors_a, error_a, 'rv-', label='Error Rate')
plt.title('Error Rate vs. neighbors')
plt.xlabel('neighbors/count')
plt.ylabel('Error Rate/%')
plt.legend()

plt.show()
