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
plt.title(r'График', fontsize=14)
plt.hist (y, bins=5, edgecolor='black') 
#plt.grid(True)
#plt.errorbar(x, y, fmt='o', color='black', capsize=3)
#p = np.polyfit(x, y, 1, full=True, cov=False)
#print(p)
#p = p[0]
#yfit = np.polyval(p,x)
# plt.plot(x, yfit, color="firebrick")
plt.show()