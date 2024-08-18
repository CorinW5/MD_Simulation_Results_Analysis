import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
import os


def read_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    data = []
    for line in lines:
        if line[0] == '#': continue
        if float(line) < 0.0000001: continue
        data.append(float(line))
    return data


def choose_best_fit_region(x, y):
    size = len(x)
    trial_list = [100000, 400000]
    best_fit_start, r_sq = 100000, 0
    while trial_list[1] < size - 50000:
        slope, intercept, r_value, p_value, std_err = st.linregress(x[trial_list[0]:trial_list[1]], y[trial_list[0]:trial_list[1]])
        if r_sq < r_value ** 2:
            best_fit_start, r_sq = trial_list[0], r_value ** 2
        for i in range(2):
            trial_list[i] += 5000
    return x[best_fit_start:best_fit_start + 200000], y[best_fit_start:best_fit_start + 200000]

def linear_regression(file_path, folder_path, file_name):
    y = read_data(file_path)
    x = np.arange(1, len(y) + 1)
    x *= 10


    x_mid = x[int(len(x) / 3):int(len(x) * 2 / 3)]
    y_mid = y[int(len(y) / 3):int(len(y) * 2 / 3)]
    b1, b0 = np.polyfit(x_mid, y_mid, 1)

    # Create regression line
    y_reg = b0 + b1 * x_mid

    plt.figure(figsize=(10, 6), dpi=300)
    #plt.xscale('log')
    #plt.yscale('log')

    plt.scatter(x, y, s=5)
    plt.plot(x_mid, y_reg, color='red', label='Regression line')

    plt.xlabel('Time steps')
    plt.ylabel('MSD value')
    plt.title(file_path[18:-4])

    # Add text "viscosity: b1"
    plt.text(0.02, 0.90, f'viscosity: {b1:.3e}', transform=plt.gca().transAxes, fontsize=10,
             verticalalignment='top', bbox=dict(boxstyle='round,pad=0.5', alpha=0.5))

    plt.legend()
    plt.savefig(folder_path + "/Graphs/" + file_name[:-4] + '.png')
    plt.show()


def analyze_msd(folder_path):
    list_fp = []
    file_list = os.listdir(folder_path)
    for file in file_list:
        if file[:3] == 'msd':
            list_fp.append(file)
    for i in list_fp:
        linear_regression(folder_path + "/" + i, folder_path, i)