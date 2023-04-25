import numpy as np

N = int(2) # количество частиц
Vmax = float(1.0)  # максимальная скорость частицы
d = float(0.0) # delta-окрестность
dt = float(0.001) # тик
Leng = int(10) # длина коробки
half = Leng/2 # половина длины коробки

class Particle:
    """Particle class"""
    def __init__(self, n, c, v, a = np.zeros(3), lc = np.zeros(3), way = np.zeros(3)):
        self.n = n # particle number
        self.c = c # coordinate
        self.v = v # velocity
        self.a = a # acceleration
        self.lc = lc # last coordinate
        self.way = way # the movement of a particle from the beginning of time

    def display(self):
        # displays information about the particle
        return print('Coordinate: ' + np.array2string(self.c) + 
        ', Velocity: ' + np.array2string(self.v) + 
        ', Acceleration: ' + np.array2string(self.a)) 
        
    def to_border(c):
        # returns the particle to the borders of the box
        for i in np.arange(3):
            while ((c[i] >= Leng)or(c[i] < 0)):
                c[i] %= Leng
                
    def vec_to_virtual_copy(partc, part1c):
        # returns a vector directed to a virtual copy of particle "part1"
        vecr = part1c - partc
        for i in np.arange(3):
            if (vecr[i] > half):
                vecr[i] -= Leng
            if (vecr[i] < -half):
                vecr[i] += Leng
        return vecr
        
    def first_move(self):
        # moves the particle for the first time 
        self.lc = self.c
        dradius = dt*(self.v) + 0.5*(self.a)*dt**2
        self.way = self.way + dradius
        self.c = self.c + dradius
        Particle.to_border(self.c)
        self.v += dt*(self.a)
     
    def move(self):
        # moves the particle using the Verlet scheme
        dradius = self.c - self.lc + self.a*dt**2
        self.lc = self.c
        self.way = self.way + dradius
        self.c = self.c + dradius
        Particle.to_border(self.c)
        self.v += self.a*dt