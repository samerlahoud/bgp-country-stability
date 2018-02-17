#!/root/anaconda3/bin/python
import glob
import matplotlib.pyplot as plt
import numpy as np
import csv
import os
import re
from datetime import datetime

merge_nb_updates = []
merge_update_ratio = []
country_codes = []
output_path = './output/'
figure_path = './figures/'

for output_file in sorted(glob.glob(os.path.join(output_path, '*.txt'))):
    nb_prefixes = []
    nb_updates = []
    update_ratio = []
    country_code = re.split('-',output_file)[2]

    timestamp = '-'.join(re.split(r'[-.]',output_file)[4:7])
    with open(output_file,'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            if row[2] == '0' or row[2] == 'None':
                continue
            else:
                nb_prefixes.append(int(row[2]))
                nb_updates.append(int(row[1]))
                update_ratio.append(float(int(row[1])/int(row[2])))
        country_codes.append(country_code)
        merge_nb_updates.append(np.log10(nb_updates))
        merge_update_ratio.append(np.log10(update_ratio))

        update_ratio_fig = plt.figure()
        plt.loglog(nb_prefixes,update_ratio,'x')
        plt.xlabel('Number of prefixes')
        plt.ylabel('Number of updates per prefix')
        update_ratio_fig.savefig(figure_path+'nb-updates-'+country_code+'-'+timestamp+'.png')
        plt.close(update_ratio_fig)

fig, ax = plt.subplots()
ax.violinplot(merge_nb_updates, showmedians=True)
ax.grid(True)
plt.ylabel('log10(Number of updates)')
xtickNames = plt.setp(ax, xticklabels=np.repeat(country_codes, 2))
plt.setp(ax, xticks=[y+1 for y in range(len(merge_nb_updates))],
         xticklabels=country_codes)
fig.savefig(figure_path+'nb-updates-menog-'+timestamp+'.png')
plt.close(fig)

fig, ax = plt.subplots()
ax.violinplot(merge_update_ratio, showmedians=True)
ax.grid(True)
plt.ylabel('log10(Number of updates per prefix)')
xtickNames = plt.setp(ax, xticklabels=np.repeat(country_codes, 2))
plt.setp(ax, xticks=[y+1 for y in range(len(merge_update_ratio))],
         xticklabels=country_codes)
fig.savefig(figure_path+'update-ratio-menog-'+timestamp+'.png')
plt.close(fig)

#    nb_update_fig = plt.figure()
#    plt.semilogy(x,y,'x')
#    plt.xlabel('Number of prefixes')
#    plt.ylabel('Number of updates')
#    plt.title('BGP updates in last two weeks')
#    plt.legend()
#    nb_update_fig.savefig('nb-updates'+output_file.replace(".txt","")+'.png')
#    plt.close(nb_update_fig)

#    update_ratio_fig = plt.figure()
#    plt.loglog(x,z,'x')
#    plt.xlabel('Number of prefixes')
#    plt.ylabel('Update ratio')
#    plt.title('BGP update ratio in last two weeks')
#    plt.legend()
#    update_ratio_fig.savefig(output_file.replace(".txt","")+'-update-ratio.png')
#    plt.close(update_ratio_fig)

