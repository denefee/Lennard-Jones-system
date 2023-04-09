import math
import matplotlib as plt
import numpy as np
import time
import random
import os

# глобальные переменные
N = int(8) # количество частиц
Vmax = float(1.0)  # максимальная скорость частицы
d = float(0.001) # delta-окрестность
dt = float(0.001) # тик
Leng = int(10) # длина коробки
half = Leng/2 # половина длины коробки


# opens files with data 
impt = open('imp.txt', 'w')
kint = open('kin.txt', 'w')
pott = open('pot.txt', 'w')
mect = open('mec.txt', 'w')


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
        

def rand_gen_char(pars):
    # generates a particle with a unique coordinate
    n = 0
    c = np.random.uniform(0, Leng, (3))
    for i in np.arange(pars.size):
        a = pars[i]
        if (np.linalg.norm(c - a.c) <= d): # may work, but needs a test
            c = np.random.uniform(0, Leng, (3))
            i = -1
            continue
    v = np.random.uniform(-Vmax, Vmax, (3))
    n += 1
    print (n)
    return Particle(c, v)
  
  
def rand_gen(pars):
    # generates N particles with unique coordinates
    for i in np.arange(N):
        pars.append(rand_gen_char(pars))
        continue


def cell_gen(pars):
    # cell generation
    n = 0
    key = 0
    flag = True
    reb = math.ceil(np.cbrt(N))
    dl = Leng/reb  
    for i in np.arange(reb):
        x = dl/2 + i*dl
        if (flag == False):
            break
        for j in np.arange(reb):
            y = dl/2 + j*dl
            if (flag == False):
                break
            for k in np.arange(reb):
                z = dl/2 + k*dl
                n += 1
                c = np.array([x, y, z])
                if key == 0:
                    v = np.random.uniform(-Vmax, Vmax, (3))
                    key += 1
                else:
                    v = -v
                    key -= 1
                pars.append(Particle(c, v))
                if (n == N):
                    flag = False
                    break


def axel(part, part1):
    # calculates the forces of interaction between these particles and changes their accelerations
    vecr = Particle.vec_to_virtual_copy(part.c, part1.c)
    modr = np.linalg.norm(vecr)
    if (modr < d):
        modr = d
    ac = -24*(2*np.power(modr, -14) - np.power(modr, -8))*vecr
    part.a = part.a + ac
    part1.a = part1.a - ac
  
  
def calc_ax(pars):
    # calculates the accelerations of all particles and changes them
    for i in np.arange(N-1):
        for j in np.arange(i+1, N):
            axel(pars[i], pars[j])
        
        
def null_ax(pars):
    # nullifies all accelerations
    for i in np.arange(N):
        pars[i].a = np.array([0, 0, 0]) 
    
    
def first_move(pars):
    # moves all particles for the first time
    calc_ax(pars)
    for i in np.arange(N):
        Particle.first_move(pars[i])
    
    
def move(pars):
    # moves all particles
    for i in np.arange(N):
        Particle.move(pars[i])  

        
def potentwo(part, part1):
    # calculates the potential energy of the interaction of two particles
    vecr = Particle.vec_to_virtual_copy(part.c, part1.c)
    modr = np.linalg.norm(vecr)
    if (modr < d):
        modr = d
    u = 4*(np.power(modr, -12) - np.power(modr, -6))
    return u
    
    
def impulse(pars):
    # calculates the total momentum of the system
    summ = np.array([0.0, 0.0, 0.0])
    for i in np.arange(N):
        summ = summ + pars[i].v
    impt.write(np.array2string(summ) + '\n')
        
        
def poten_eng(pars):
    # calculates the potential energy of the interaction of all particles
    pot = 0
    for i in np.arange(N-1):
        for j in np.arange(i+1, N):
            pot = pot + potentwo(pars[i], pars[j])
    pott.write(str(pot) + '\n')
    return pot 
        
        
def kinetic_eng(pars):
    # calculates the total kinetic energy of the system
    kin = 0
    for i in np.arange(N):
        kin = kin + (np.linalg.norm(pars[i].v)**2)/2
    kint.write(str(kin) + '\n')
    return kin


def energy(pars):
    # calculates the total mechanical energy of the system
    pot = poten_eng(pars)
    kin = kinetic_eng(pars)
    summ = pot + kin
    mect.write(str(summ) + '\n')

    
def timego(pars, tick):
    # starts the simulation
    print(0)
    first_move(pars)
    impulse(pars)
    energy(pars)
    # Particle.display(pars[N//2])
    null_ax(pars)
    for i in np.arange(1, tick):
        calc_ax(pars)
        move(pars)
        # Particle.display(pars[N//2])
        impulse(pars)
        energy(pars)
        null_ax(pars)
        if i%(tick//10) == 0:
            print (i)


def main():  
    t = int(10000) # ticks
    start = time.time() # точка отсчета времени
    pars = []
    cell_gen(pars) # генерация сеткой
    # rand_gen(pars) # случайная генерация, возможно работает как надо
    #for i in np.arange(N): # выводит характеристики всех частиц
    #  Particle.display(pars[i])
    timego(pars, t)
    end = time.time() - start # собственно время работы программы
    print(end) # вывод времени


if __name__ == "__main__":
    main()
    
    
# close files with data 
impt.close()
kint.close()
mect.close()
pott.close()