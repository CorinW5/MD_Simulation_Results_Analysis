import numpy as np
import matplotlib.pyplot as plt
import os

def rdf_rd(s):
    if s[0] == '#': return []
    res = []
    temp_arr = s.split(" ")
    for i in temp_arr: res.append(float(i))
    return res


def rdf_read_data(file_path):
    x_list, y_list = [], []
    with open(file_path, 'r') as file:
        lines = file.readlines()
    for line in lines:
        temp = rdf_rd(line)
        if len(temp) == 2 or len(temp) == 0:
            x_list.clear()
            y_list.clear()
        else:
            x_list.append(temp[1])
            y_list.append(temp[2])
    return [x_list, y_list]

def rdf_plot_data(file_path, folder_path, file_name):
    res = rdf_read_data(file_path)
    x_list, y_list = res[0], res[1]
    x = np.array(x_list)
    y = np.array(y_list)
    plt.figure(figsize = (10, 6), dpi = 300)
    #plt.yscale('log')
    plt.axis([0, 2.5, 0.001, 10])
    plt.scatter(x, y, label = 'Data points', s = 1)
    plt.xlabel('Radius', fontsize = 20)
    plt.xticks(fontsize=15)
    plt.ylabel('RDF', fontsize = 20)
    plt.yticks(fontsize=15)
    plt.title(file_path[file_path.find("tmp") + 3:-4], fontsize = 20)
    plt.plot(x, y)
    plt.savefig(folder_path + "/Graphs/" + file_name[:-4] + '.png')
    #plt.show()

def analyze_rdf(folder_path):
    list_fp = []
    file_list = os.listdir(folder_path)
    for file in file_list:
        if file[-3:] == 'rdf':
            list_fp.append(file)
    for i in list_fp:
        rdf_plot_data(folder_path + "/" + i, folder_path, i)

def analyze_multiple_rdf():
    list_ys = []
    colors = ["#008000", "#FF0000", "#0000FF"]
    list_fp = ["Resources/MD data/n1_weak/200f/tmpFiller_Poly.rdf",
               "Resources/MD data/n1_repulsive/200f/tmpFiller_Poly.rdf", "Resources/MD data/n1_attractive/200f/tmpFiller_Poly.rdf"]
    labels = ["Weak interaction", "Strong repulsion", "Strong attraction"]
    for i, label, color in zip(list_fp, labels, colors):
        res = rdf_read_data(i)
        x_list, y_list = res[0], res[1]
        x = np.array(x_list)
        y = np.array(y_list)
        list_ys.append((y, label, color))
    plt.figure(figsize = (11, 6), dpi = 300)
    #plt.axis([0, 2.5, 0, 20])
    for y, label, color in list_ys:
        plt.scatter(x, y, s = 8, color = color)
        plt.plot(x, y, label=f'{label}', linewidth = 2, color = color)
    plt.xlabel('Radius', fontsize=20)
    plt.legend(fontsize = 20)
    plt.xticks(fontsize=15)
    plt.ylabel('RDF', fontsize=20)
    plt.yticks(fontsize=15)
    plt.title("RDF between Filler and Polymer at 200f", fontsize=20)
    # to be changed
    plt.savefig('Resources/MD data/RDF_200f.png')
    plt.show()

analyze_multiple_rdf()