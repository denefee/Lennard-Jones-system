import numpy as np
Vmax = 1

r = np.array([0, 1.41, 1.41])
r = np.linalg.norm(r)
r = 0.01
u = 4/(r**12) - 4/(r**6)

print(u)