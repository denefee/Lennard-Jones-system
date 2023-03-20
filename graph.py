import numpy as np
import matplotlib.pyplot as plt

x = np.array([])
y = np.array([])

for i in np.arange(2, 101):
    x = np.append(x, i)

f = open('mechanic.txt')
for line in f:
    y = np.append(y, float(line))
f.close()


plt.xlabel(r'Механическая энергия', fontsize=14)
plt.ylabel(r'Время работы программы, тиков', fontsize=14)
plt.title(r'График', fontsize=14)
plt.grid(True)
plt.errorbar(x, y, xerr=0, yerr=0, fmt='.', color='black', capsize=3)
p = np.polyfit(x, y, 1, full=True, cov=False)
print(p)
p = p[0]
yfit = np.polyval(p,x)
plt.plot(x, yfit, color="firebrick")
plt.show()