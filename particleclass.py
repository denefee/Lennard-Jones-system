import numpy as np

N = int(512) # количество частиц
Vmax = float(1.0)  # максимальная скорость частицы
d = float(0.0) # delta-окрестность
dt = float(0.001) # тик
Leng = int(10) # длина коробки
half = Leng/2 # половина длины коробки

class Particle:
    """Particle class"""
    def __init__(self, c, v, a = np.array([0, 0, 0]), lc = np.array([0, 0, 0])):
        self.c = c # coordinate
        self.v = v # velocity
        self.a = a # acceleration
        self.lc = lc # last coordinate

    def display(self):
        # displays information about the particle
        return print('Coordinate: ' + np.array2string(self.c) + 
        ', Velocity: ' + np.array2string(self.v) + 
        ', Acceleration: ' + np.array2string(self.a))
        
    def to_border(c):
        # returns the particle to the borders of the box
        for i in np.arange(3):
            while ((c[i] >= Leng)or(c[i] < 0)):
                c[i] = c[i] % Leng  
                
    def vec_to_virtual_copy(partc, part1c):
        # returns a vector directed to a virtual copy of particle "part1"
        vecr = part1c - partc
        p1copy = np.copy(part1c)
        for i in np.arange(3):
            if (vecr[i] > half):
                p1copy[i] = p1copy[i] - Leng
            if (vecr[i] < -half):
                p1copy[i] = p1copy[i] + Leng
        vecr = p1copy - partc
        return vecr
        
    def first_move(self):
        # moves the particle for the first time 
        self.lc = np.copy(self.c)
        self.c = self.c + dt*(self.v) + 0.5*(self.a)*dt**2
        Particle.to_border(self.c)
        self.v = self.v + dt*(self.a)
        
    def move(self):
        # moves the particle using the Verlet scheme
        mem = np.copy(self.c)
        self.c = 2*self.c - self.lc + self.a*dt**2
        Particle.to_border(self.c)
        self.lc = mem
        self.v = self.v + self.a*dt