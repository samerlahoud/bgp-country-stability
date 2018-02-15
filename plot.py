import matplotlib.pyplot as plt
import csv

x = []
y = []
z = []

with open('bgp-stability-lb-1518687353.8155603.txt','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        if int(row[2]) != 0:
            x.append(int(row[2]))
            y.append(int(row[1]))
            z.append(float(int(row[1])/int(row[2])))

fig1 = plt.figure()
plt.semilogy(x,y,'x')
plt.xlabel('Number of prefixes')
plt.ylabel('Number of updates')
plt.title('BGP updates in last two weeks for Lebanese ASes')
plt.legend()
fig1.savefig('update-lb.png')

fig2 = plt.figure()
plt.semilogy(x,z,'x')
plt.xlabel('Number of prefixes')
plt.ylabel('Update ratio')
plt.title('BGP update ratio in last two weeks for Lebanese ASes')
plt.legend()
fig2.savefig('update-ratio-lb.png')


