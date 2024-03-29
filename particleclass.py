import numpy as np

dt = float(0.001) # тик
Leng = int(4) # длина коробки
half = Leng/2 # половина длины коробки

class Particle:
    """Particle class"""
    def __init__(self, c = np.zeros(3), v = np.zeros(3), a = np.zeros(3), lc = np.zeros(3), way = np.zeros(3)):
        self.c = c # coordinate
        self.v = v # velocity
        self.a = a # acceleration
        self.lc = lc # last coordinate
        self.way = way # the movement of a particle from the beginning of time
        
    def to_border(c):
        # returns the particle to the borders of the box
        for i in np.arange(3):
            while ((c[i] >= Leng)or(c[i] < 0)):
                c[i] %= Leng
             
    def vec_to_virtual_copy(partc, part1c):
        # returns a vector directed to a virtual copy of particle "part1"
        vect_r = part1c - partc
        for i in np.arange(3):
            if (vect_r[i] > half):
                vect_r[i] -= Leng
            if (vect_r[i] < -half):
                vect_r[i] += Leng
        return vect_r
       
    def first_move(self):
        # moves the particle for the first time 
        self.lc = np.zeros(3) + self.c
        delta_r = dt*(self.v) + 0.5*(self.a)*dt**2
        self.way += delta_r
        self.c += delta_r
        Particle.to_border(self.c)
        self.v += dt*(self.a)
    
    def move(self):
        # moves the particle using the Verlet scheme
        delta_r = Particle.vec_to_virtual_copy(self.lc, self.c) + self.a*dt**2
        self.lc = np.zeros(3) + self.c
        self.way += delta_r
        self.c += delta_r
        Particle.to_border(self.c)
        self.v += self.a*dt