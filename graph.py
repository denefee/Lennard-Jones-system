import numpy as np
import matplotlib.pyplot as plt

x = np.array([])
for i in np.arange(200):
    x = np.append(x, (i))

ymec = np.array([])
f = open('mec.txt')
for line in f:
    ymec = np.append(ymec, np.log10(float(line)))
f.close()

ypot = np.array([])
f = open('pot.txt')
for line in f:
    ypot = np.append(ypot, np.log10(float(line)))
f.close()

ykin = np.array([])
f = open('kin.txt')
for line in f:
    ykin = np.append(ykin, np.log10(float(line)))
f.close()


plt.xlabel(r'Время работы программы, тиков', fontsize=14)
plt.ylabel(r'Механическая энергия', fontsize=14)
plt.title(r'График', fontsize=14)
plt.grid(True)
plt.errorbar(x, ymec, fmt='o', color='black', capsize=3)
plt.errorbar(x, ykin, fmt='o', color='red', capsize=3)
plt.errorbar(x, ypot, fmt='o', color='green', capsize=3)
#p = np.polyfit(x, y, 1, full=True, cov=False)
#print(p)
#p = p[0]
#yfit = np.polyval(p,x)
# plt.plot(x, yfit, color="firebrick")
plt.show()