import glob
import matplotlib.pyplot as plt
import csv
import os

x = []
y = []
z = []
output_path = './output'

for output_file in glob.glob(os.path.join(output_path, '*.txt')):
    with open(output_file,'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            if row[2] == '0' or row[2] == 'None':
                continue
            else:
                x.append(int(row[2]))
                y.append(int(row[1]))
                z.append(float(int(row[1])/int(row[2])))

    nb_update_fig = plt.figure()
    plt.semilogy(x,y,'x')
    plt.xlabel('Number of prefixes')
    plt.ylabel('Number of updates')
    plt.title('BGP updates in last two weeks')
    plt.legend()
    nb_update_fig.savefig(output_file.replace(".txt","")+'-nb-update.png')
    plt.close(nb_update_fig)

    update_ratio_fig = plt.figure()
    plt.loglog(x,z,'x')
    plt.xlabel('Number of prefixes')
    plt.ylabel('Update ratio')
    plt.title('BGP update ratio in last two weeks')
    plt.legend()
    update_ratio_fig.savefig(output_file.replace(".txt","")+'-update-ratio.png')
    plt.close(update_ratio_fig)

