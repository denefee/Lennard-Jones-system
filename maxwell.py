import numpy as np
import matplotlib.pyplot as plt

#x = np.array([])
#for i in np.arange(2000):
#   x = np.append(x, (i))

y = np.array([])
f = open('maxw.txt')
for line in f:
    y = np.append(y, (float(line)))
f.close()

#plt.xlabel(r'Время работы программы, тиков', fontsize=14)
#plt.ylabel(r'Механическая энергия', fontsize=14)
plt.title(r'Распределение проекции скоростей частиц на ось X', fontsize=14)
plt.hist(y, bins=10, edgecolor='black', density = True) 
#plt.grid(True)

plt.show()