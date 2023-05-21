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

v_x = y
N = len(v_x)

T = np.sum(v_x**2)
plt.hist(v_x, bins=N//5, density=True)

print(T/N)

plt.title(r'Распределение проекции скоростей частиц на ось X', fontsize=14)

plt.show()