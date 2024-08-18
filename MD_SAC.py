import numpy as np
import matplotlib.pyplot as plt

def take_average(result_data):
    x_list, y_list = [], []
    for read in result_data:
        x_list.append(read[0])
        y_list.append(read[1])

    x = np.array(x_list)
    y = np.array(y_list)

    # Define the kernel size for convolution
    kernel_1_size = 5
    kernel_1 = np.ones(kernel_1_size) / kernel_1_size
    kernel_2_size = 15
    kernel_2 = np.ones(kernel_2_size) / kernel_2_size
    kernel_3_size = 50
    kernel_3 = np.ones(kernel_3_size) / kernel_3_size

    # Apply convolution to smooth the y data
    y_smooth = y_list[:10]
    for i in np.convolve(y, kernel_1, mode='same')[10:100]:
        y_smooth.append(i)
    for i in np.convolve(y, kernel_2, mode='same')[100:200]:
        y_smooth.append(i)
    for i in np.convolve(y, kernel_3, mode='same')[200:]:
        y_smooth.append(i)
    return x, np.array(y_smooth)


def integration(result_data):
    res = 0.0
    for i in range(4000 - 1):
        res += (result_data[i + 1][0] - result_data[i][0]) * 0.5 * (result_data[i + 1][1] + result_data[i][1])
    return res

def analyze(data_file):
    N = 4000
    M = 10  # times of dump
    temperature = 0.8
    volume = 35445.234
    result_data = []

    class Autocre:
        def __init__(self):
            self.stress = np.zeros(N)
            self.time = np.zeros(N, dtype=int)

    def read_data(file):
        data = []
        with open(file, 'r') as f:
            for line in f:
                data.append(line.strip())
        return data

    press = np.zeros((N, 3))
    gt = Autocre()

    result_file = "Resources/MD data/" + data_file[18:-4] + "_res.txt"
    aveGt_file = "Resources/MD data/" + data_file[18:-4] + "_ave.txt"

    pre = volume / (3 * temperature)
    data = read_data(data_file)
    data_iter = iter(data)
    next(data_iter)  # Skip first three lines
    next(data_iter)
    next(data_iter)

    for k in range(M + 1):
        dump, dump2 = map(int, next(data_iter).split())
        for j in range(N):
            parts = next(data_iter).split()
            i, gt.time[j], dump = map(int, parts[:3])
            press[j] = list(map(float, parts[3:]))
            gt.stress[j] = np.sum(press[j]) * pre

    with open(result_file, 'w') as result:
        sum_stress = 0
        with open(aveGt_file, 'w') as aveGt:
            for j in range(N):
                result.write(f"{gt.time[j]} {gt.stress[j]}\n")
                result_data.append([gt.time[j] * 0.005, gt.stress[j]])
                sum_stress += gt.stress[j]
                if (j + 1) % 10 == 0:
                    aveGt.write(f"{gt.time[j - 5]} {sum_stress / 10}\n")
                    sum_stress = 0

    resx, resy = take_average(result_data)
    data_after_convolution = []
    for i, j in zip(resx, resy):
        data_after_convolution.append([i, j])
    return resx, resy, integration(result_data)

def analyze_multiple_sac():
    list_ys = []
    # to be changed
    list_fp = ["Resources/MD data/n1_weak/0f/Sauto.dat", "Resources/MD data/n1_attractive/50f/Sauto.dat", "Resources/MD data/n1_attractive/100f/Sauto.dat", "Resources/MD data/n1_attractive/150f/Sauto.dat", "Resources/MD data/n1_attractive/200f/Sauto.dat"]
    # to be changed
    labels = ["  0f, viscosity = ", " 50f, viscosity = ", "100f, viscosity = ", "150f, viscosity = ", "200f, viscosity = "]
    for i, label in zip(list_fp, labels):
        x, y, eta = analyze(i)
        eta = '%.4f' % eta
        list_ys.append((y, label + str(eta)))
    plt.figure(figsize=(6, 8), dpi=300)
    plt.xlim((0.25, 1000))
    plt.ylim((-1, 7))
    plt.plot([0, 6e6], [0, 0], c='black', linestyle='--', linewidth=1)
    plt.xscale('log')
    for y, label in list_ys:
        plt.scatter(x, y, s=0.5)
        plt.plot(x, y, label=f'{label[:4]}', linewidth = 1)
    plt.legend(fontsize = 15)
    plt.title("SAF for Strong Attraction", fontsize = 16)
    plt.ylabel("G(t)", fontsize = 14)
    plt.yticks(fontsize = 10)
    plt.xticks(fontsize=10)
    plt.xlabel("Time", fontsize = 14)
    # to be changed
    plt.savefig('Resources/MD data/n1_attractive/sac.png')
    plt.show()

def analyze_multiple_sac():
    list_ys = []
    # to be changed
    list_fp = ["Resources/MD data/n1_weak/0f/Sauto.dat", "Resources/MD data/n1_attractive/50f/Sauto.dat", "Resources/MD data/n1_attractive/100f/Sauto.dat", "Resources/MD data/n1_attractive/150f/Sauto.dat", "Resources/MD data/n1_attractive/200f/Sauto.dat"]
    # to be changed
    labels = ["  0f, viscosity = ", " 50f, viscosity = ", "100f, viscosity = ", "150f, viscosity = ", "200f, viscosity = "]
    for i, label in zip(list_fp, labels):
        x, y, eta = analyze(i)
        eta = '%.4f' % eta
        list_ys.append((y, label + str(eta)))
    plt.figure(figsize=(6, 8), dpi=300)
    plt.xlim((0.25, 1000))
    plt.ylim((-1, 7))
    plt.plot([0, 6e6], [0, 0], c='black', linestyle='--', linewidth=1)
    plt.xscale('log')
    for y, label in list_ys:
        plt.scatter(x, y, s=0.5)
        plt.plot(x, y, label=f'{label[:4]}', linewidth = 1)
    plt.legend(fontsize = 15)
    plt.title("SAF for Strong Attraction", fontsize = 16)
    plt.ylabel("G(t)", fontsize = 14)
    plt.yticks(fontsize = 10)
    plt.xticks(fontsize=10)
    plt.xlabel("Time", fontsize = 14)
    # to be changed
    plt.savefig('Resources/MD data/n1_attractive/sac.png')
    plt.show()




def analyze_sac(folder_path):
    fp = folder_path + '/Sauto.dat'
    x, y, eta = analyze(fp)
    eta = '%.4f' % eta
    plt.figure(figsize=(5, 6), dpi=300)
    plt.xlim((0.25, 1000))
    plt.ylim((-0.5, 3))
    plt.plot([0, 6e6], [0, 0], c='black', linestyle='--', linewidth=0.5)
    plt.xscale('log')
    plt.plot(x, y, linewidth = 0.5)
    plt.scatter(x, y, s=0.5)
    plt.savefig(folder_path + '/Graphs/sac.png')
    plt.show()

analyze_multiple_sac()