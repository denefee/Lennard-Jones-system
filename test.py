import numpy as np
coord = open('coord.txt', 'w')

a = np.array([1.0, 2.0, 3.0])
b = np.array([4.0, 5.0, 6.0])


for i in np.arange(3):
    coord.write(str(a[i]) + ' ')
coord.write('\n')
for i in np.arange(3):
    coord.write(str(b[i]) + ' ')
coord.write('\n')

coord.close()