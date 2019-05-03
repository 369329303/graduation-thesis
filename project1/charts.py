import matplotlib.pyplot as plt

radius_a = list()
liv1_rmse_a, liv1_error_a = list(), list()
liv2_rmse_a, liv2_error_a = list(), list()
idw_rmse_a, idw_error_a = list(), list()
with open('report.txt', 'r') as f:
    for line in f:
        if line.startswith('----'):
            radius_a.append(float(line.split()[-2]))
        elif line.startswith('liv1'):
            liv1_rmse_a.append(float(line.split()[-2]))
            liv1_error_a.append(float(line.split()[-1]))
        elif line.startswith('liv2'):
            liv2_rmse_a.append(float(line.split()[-2]))
            liv2_error_a.append(float(line.split()[-1]))
        elif line.startswith('idw'):
            idw_rmse_a.append(float(line.split()[-2]))
            idw_error_a.append(float(line.split()[-1]))

plt.subplot(121)
plt.plot(radius_a, liv1_rmse_a, 'ro-', label='liv1')
plt.plot(radius_a, liv2_rmse_a, 'b^-', label='liv2')
plt.plot(radius_a, idw_rmse_a, 'ks-', label='idw')
plt.title('radius vs. RMSE')
plt.xlabel('radium/m')
plt.ylabel('RMSE/m')
plt.legend()

plt.subplot(122)
plt.plot(radius_a, liv1_error_a, 'ro-', label='liv1')
plt.plot(radius_a, liv2_error_a, 'b^-', label='liv2')
plt.plot(radius_a, idw_error_a, 'ks-', label='idw')
plt.title('radius vs. error rate')
plt.xlabel('radius/m')
plt.ylabel('error rate/%')
plt.legend()

plt.show()
