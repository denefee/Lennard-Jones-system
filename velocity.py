import numpy as np

y = np.array([])
f = open('maxw.txt')
for line in f:
    y = np.append(y, abs((float(line))))
f.close()

v_x = y
N = len(v_x)

V = np.sum(v_x)*np.sqrt(3)/N

print(V)
