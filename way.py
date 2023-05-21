import numpy as np
import matplotlib.pyplot as plt

y = np.array([])
f = open('way.txt')
for line in f:
    y = np.append(y, (float(line)))
f.close()

x = np.linspace(1, len(y)+1, num=len(y))

plt.xlabel(r'Время работы программы, тиков', fontsize=14)
plt.ylabel(r'Среднее квадратичное перемещение частиц, у.е.$^2$', fontsize=14)
plt.title(r'График зависимости перемещения частиц от времени', fontsize=14)
plt.grid(True)
plt.errorbar(x, y, fmt='o', color='black', capsize=3, label=r'Среднее перемещение частиц')
plt.legend(loc='best', fontsize=12)

p = np.polyfit(x, y, 1, full=True, cov=False)
print(p)
p = p[0]
yfit = np.polyval(p,x)
plt.plot(x, yfit, color="firebrick")
plt.show()