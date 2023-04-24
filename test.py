import numpy as np

f = np.array([1, 2, 3, 4, 5])
a = f[f>3] + 1

print(a)
print(f)