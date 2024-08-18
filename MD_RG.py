import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def rg_rd(s):
    if s[0] == '#': return []
    res = []
    temp_arr = s.split(" ")
    for i in temp_arr: res.append(float(i))
    return res


def update_hist(num, data):
    if num % 10 == 0: print("Rg now at step:" + str(num))
    plt.cla()
    plt.hist(data[num], bins=50)
    plt.axis([0, 5, 0, 30])
    plt.title("Rg over time at 0 filler", fontsize=14)
    plt.xlabel('Distance', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)

def analyze_rg(folder_path):
    file_path = folder_path + '/gmol_A.txt'
    with open(file_path, 'r') as file:
        lines = file.readlines()
    data, chunk = [], []
    cnt = -1
    for line in lines:
        temp = rg_rd(line)
        if len(temp) == 0: continue
        cnt += 1
        if cnt % 301 == 0:
            data.append([])
            for i in chunk:
                data[-1].append(i)
            chunk.clear()
            continue
        chunk.append(temp[1])
    data = data[1:]
    list_mean, list_std = [], []
    for i in data:
        list_mean.append(np.mean(i))
        list_std.append(np.std(i, ddof=1))

    y_mean = np.array(list_mean)
    y_mean = y_mean[5:-5]
    y_std = np.array(list_std)
    y_std = y_std[5:-5]
    x = np.arange(1, 600)
    x *= 10000
    x = x[5:-5]
    plt.figure(figsize=(10, 6), dpi=300)
    plt.axis([0, 6e6, 0, 5])
    plt.scatter(x, y_mean, label='Data points', s=1)
    plt.xlabel('Time steps')
    plt.ylabel('Mean Rg')
    plt.plot(x, y_mean)
    plt.savefig(folder_path + '/Graphs/Rg_mean.png')
    plt.show()
    plt.close()
    plt.figure(figsize=(10, 6), dpi=300)
    plt.axis([0, 6e6, 0, 5])
    plt.scatter(x, y_std, label='Data points', s=1)
    plt.xlabel('Time steps')
    plt.ylabel('STD of Rg')
    plt.plot(x, y_std)
    plt.savefig(folder_path + '/Graphs/Rg_std.png')
    plt.show()
    plt.close()



    save_path = folder_path + "/Graphs/Rg.gif"
    number_of_frames = len(data)
    fig2 = plt.figure()
    movie = animation.FuncAnimation(fig2, update_hist, number_of_frames, \
                                       fargs=(data,))
    movie.save(save_path, writer='pillow', fps=50)


def analyze_multiple_rg():
    list_y_mean, list_y_std = [], []
    # to be changed
    list_fp = ["Resources/MD data/n1_attractive/50f/gmol_A.txt", "Resources/MD data/n1_attractive/100f/gmol_A.txt", "Resources/MD data/n1_attractive/150f/gmol_A.txt", "Resources/MD data/n1_attractive/200f/gmol_A.txt"]
    # to be changed
    labels = ["50f: ", "100f: ", '150f: ', '200f: ']
    # to be changed
    save_path = "Resources/MD data/n1_attractive"

    for i, label in zip(list_fp, labels):
        with open(i, 'r') as file:
            lines = file.readlines()
        data, chunk = [], []
        cnt = -1
        for line in lines:
            temp = rg_rd(line)
            if len(temp) == 0: continue
            cnt += 1
            if cnt % 301 == 0:
                data.append([])
                for i in chunk:
                    data[-1].append(i)
                chunk.clear()
                continue
            chunk.append(temp[1])
        data = data[1:]
        list_mean, list_std = [], []
        for i in data:
            list_mean.append(np.mean(i))
            list_std.append(np.std(i, ddof=1))
        y_mean = np.array(list_mean)
        y_mean = y_mean[5:-5]
        y_std = np.array(list_std)
        y_std = y_std[5:-5]
        list_y_mean.append((y_mean, label))
        list_y_std.append((y_std, label))

    x = np.arange(1, 600)
    x *= 10000
    x = x[5:-5]
    plt.figure(figsize=(5, 6), dpi=300)
    plt.axis([0, 6e6, 0, 5])
    plt.xlabel('Time steps')
    plt.ylabel('Mean Rg')
    for y, label in list_y_mean:
        plt.scatter(x, y, s=1)
        temp_mean = np.mean(y)
        plt.plot(x, y, label=f'{label + str(temp_mean)}', linewidth=1)
        print(temp_mean)
    plt.legend()
    plt.savefig(save_path + "/mean Rg.png")
    #plt.show()
    plt.close()

    plt.figure(figsize=(5, 6), dpi=300)
    plt.axis([0, 6e6, 0, 5])
    plt.xlabel('Time steps')
    plt.ylabel('STD of Rg')
    for y, label in list_y_std:
        plt.scatter(x, y, s=1)
        temp_mean = y[-1]
        plt.plot(x, y, label=f'{label + str(temp_mean)}', linewidth=1)
        print(temp_mean)
    plt.legend()
    plt.savefig(save_path + "/std of Rg.png")
    plt.show()
    plt.close()