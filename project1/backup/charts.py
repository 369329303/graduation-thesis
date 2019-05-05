import matplotlib.pyplot as plt

radius_a = list()
LIv1_rmse_a, LIv1_error_a = list(), list()
LIv2_rmse_a, LIv2_error_a = list(), list()
IDWv1_rmse_a, IDWv1_error_a = list(), list()
IDWv2_rmse_a, IDWv2_error_a = list(), list()
NN_rmse_a, NN_error_a = list(), list()
with open('report.txt', 'r') as f:
    for line in f:
        if line.startswith('----'):
            radius_a.append(float(line.split()[-2]))
        elif line.startswith('LIv1'):
            LIv1_rmse_a.append(float(line.split()[-2]))
            LIv1_error_a.append(float(line.split()[-1]))
        elif line.startswith('LIv2'):
            LIv2_rmse_a.append(float(line.split()[-2]))
            LIv2_error_a.append(float(line.split()[-1]))
        elif line.startswith('IDWv1'):
            IDWv1_rmse_a.append(float(line.split()[-2]))
            IDWv1_error_a.append(float(line.split()[-1]))
        elif line.startswith('IDWv2'):
            IDWv2_rmse_a.append(float(line.split()[-2]))
            IDWv2_error_a.append(float(line.split()[-1]))
        elif line.startswith('NN'):
            NN_rmse_a.append(float(line.split()[-2]))
            NN_error_a.append(float(line.split()[-1]))

# Parameters for setting figure            
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
plt.plot(radius_a, LIv1_rmse_a, 'ko-', label='LIv1')
plt.plot(radius_a, LIv2_rmse_a, 'b^-', label='LIv2')
plt.plot(radius_a, IDWv1_rmse_a, 'rv-', label='IDWv1')
plt.plot(radius_a, IDWv2_rmse_a, 'g>-', label='IDWv2')
plt.plot(radius_a, NN_rmse_a, 'ys-', label='NN')
plt.title('Radius vs. RMSE')
plt.xlabel('Radius/m')
plt.ylabel('RMSE/m')
plt.legend()

plt.subplot(122)
plt.plot(radius_a, LIv1_error_a, 'ko-', label='LIv1')
plt.plot(radius_a, LIv2_error_a, 'b^-', label='LIv2', markersize=10)
plt.plot(radius_a, IDWv1_error_a, 'rv-', label='IDWv1', markersize=10)
plt.plot(radius_a, IDWv2_error_a, 'g>-', label='IDWv2', markersize=10)
plt.plot(radius_a, NN_error_a, 'ys-', label='NN')
plt.title('Radius vs. Error Rate')
plt.xlabel('Radius/m')
plt.ylabel('Error Rate/%')
plt.legend()

plt.show()
