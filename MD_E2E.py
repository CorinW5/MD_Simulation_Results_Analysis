import traceback
import math
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
import matplotlib.animation as animation

r = [3.7795993480640668e+01 - 2.0411775193606272e+00, 3.7795993480640668e+01 - 2.0411775193606272e+00, 3.7925523137323012e+01 - 1.2663108626814366e+00]

def find_avg(molecules):
    distances = find_distances(molecules)
    avg_distance = sum(distances.values()) / len(distances)
    return avg_distance


def find_distances(molecules):
    distances = defaultdict(list)
    for mol_id, atoms in molecules.items():
        if atoms:
            # the index of the atom is the data
            first_atom = atoms[0]
            last_atom = atoms[-1]
            x1 = float(first_atom[2][0])
            y1 = float(first_atom[2][1])
            z1 = float(first_atom[2][2])
            x2 = float(last_atom[2][0])
            y2 = float(last_atom[2][1])
            z2 = float(last_atom[2][2])
            x_dis = abs(x2 - x1)
            x_dis = min(x_dis, r[0] - x_dis)
            y_dis = abs(y2 - y1)
            y_dis = min(y_dis, r[1] - y_dis)
            z_dis = abs(z2 - z1)
            z_dis = min(z_dis, r[2] - z_dis)
            distances[mol_id] = math.sqrt(x_dis * x_dis + y_dis * y_dis + z_dis * z_dis)

    return distances


def update_hist(num, data):
    if num % 10 == 0: print("e2e now at step:" + str(num))
    plt.cla()
    plt.hist(data[num], bins=50)
    plt.axis([0, 20, 0, 30])
    plt.title(f'Timestep {num}')
    plt.xlabel('Distance')
    plt.ylabel('Frequency')


def animate_hist(distances_hist, folder_path):
    # each index of distances_hist is a frame
    list_mean, list_std = [], []
    for i in distances_hist:
        list_mean.append(np.mean(i))
        list_std.append(np.std(i, ddof = 1))

    y_mean = np.array(list_mean)
    y_std = np.array(list_std)
    x = np.arange(601)
    x *= 10000

    kernel_size = 5
    kernel = np.ones(kernel_size) / kernel_size

    # Apply convolution to smooth the y data
    y_mean_smooth = np.convolve(y_mean, kernel, mode='same')
    y_std_smooth = np.convolve(y_std, kernel, mode='same')
    x = x[5:-5]
    y_mean_smooth = y_mean_smooth[5:-5]
    y_std_smooth = y_std_smooth[5:-5]

    plt.figure(figsize=(10, 6), dpi=300)
    plt.axis([0, 6e6, 0, 10])
    plt.scatter(x, y_mean_smooth, label='Data points', s=1)
    plt.xlabel('Time steps')
    plt.ylabel('Mean E2E Distance')
    plt.plot(x, y_mean_smooth)
    plt.savefig(folder_path + '/Graphs/e2e_mean.png')
    plt.show()
    plt.close()
    plt.figure(figsize=(10, 6), dpi=300)
    plt.axis([0, 6e6, 0, 10])
    plt.scatter(x, y_std_smooth, label='Data points', s=1)
    plt.xlabel('Time steps')
    plt.ylabel('STD of E2E Distance')
    plt.plot(x, y_std_smooth)
    plt.savefig(folder_path + '/Graphs/e2e_std.png')
    plt.show()
    plt.close()


    save_path = folder_path + '/Graphs/E2E.gif'
    number_of_frames = len(distances_hist)
    fig2 = plt.figure()
    hist = plt.hist(distances_hist[0], bins=50)
    movie = animation.FuncAnimation(fig2, update_hist, number_of_frames, \
                                    fargs=(distances_hist,))
    movie.save(save_path, writer='pillow', fps=20)
    #plt.show()


def analyze_e2e(folder_path):
    file_path = folder_path + '/chains_after.lammpstrj'
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        for i in range(3):
            temp = lines[5 + i].split(" ")
            r[i] = float(temp[1]) - float(temp[0])
        print(r[0] * r[1] * r[2])

        molecules = defaultdict(list)

        reading = True
        not_first = False
        avg_distances = []
        distances_hist = []

        for line in lines:

            if ("ITEM:" in line and "TIMESTEP" in line):
                reading = False
                continue

            elif ("ITEM:" in line and "mol" in line and "type" in line):
                reading = True
                if (not_first):
                    # adding the average
                    avg_distances.append(find_avg(molecules))

                    # adding a frame to the histogram
                    dist_dict = find_distances(molecules)
                    distances_hist.append(list(dist_dict.values()))

                    molecules.clear()
                not_first = True
                continue
            elif (reading == False):
                continue

            else:
                parts = line.split()
                index = int(parts[0])
                mol_id = int(parts[1])
                atom_type = int(parts[2])
                coordinates = parts[3:]
                molecules[mol_id].append((index, atom_type, coordinates))

        # for the last distance
        avg_distances.append(find_avg(molecules))

        # creating the last frame for the histogram
        dist_dict = find_distances(molecules)
        distances_hist.append(list(dist_dict.values()))
        animate_hist(distances_hist, folder_path)

    except PermissionError as e:
        print(f"Permission error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()