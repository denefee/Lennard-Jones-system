import math
import numpy as np
import time

from particleclass import Particle

# глобальные переменные
N = int(216) # количество частиц
Vmax = float(1.0)  # максимальная скорость частицы
d = float(0.0) # delta-окрестность
dt = float(0.001) # тик
Leng = int(10) # длина коробки
half = Leng/2 # половина длины коробки


# opens files with data 
impt = open('imp.txt', 'w')
kint = open('kin.txt', 'w')
pott = open('pot.txt', 'w')
mect = open('mec.txt', 'w')
maxwt = open('maxw.txt', 'w')
wayt = open('way.txt', 'w')
        

def cell_gen(pars):
    # cell generation
    n = 0
    is_even_particle = True
    is_full = False
    edge = math.ceil(np.cbrt(N))
    dl = Leng/edge 
    dl_half = dl/2
    need_zero = False
    if (N%2 == 1):
        need_zero = True
    for i in np.arange(edge):
        if is_full:
            break
        x = dl_half + i*dl
        for j in np.arange(edge):
            if is_full:
                break
            y = dl_half + j*dl
            for k in np.arange(edge):
                z = dl_half + k*dl
                n += 1
                c = np.array([x, y, z])
                if is_even_particle:
                    v = np.random.uniform(-Vmax, Vmax, (3))
                    is_even_particle = False
                else:
                    v = -v
                    is_even_particle = True
                
                if ((n == N)and(need_zero)):
                    v = np.array([0.0, 0.0, 0.0])
                pars.append(Particle(c, v))
                if (n == N):
                    is_full = True
                    break
                
                
def axel(part, part1):
    # calculates the forces of interaction between these particles and changes their accelerations
    vecr = Particle.vec_to_virtual_copy(part.c, part1.c)
    modr = np.linalg.norm(vecr)
    if (modr < d):
        modr = d
    ac = 24*(2*np.power(modr, -14) - np.power(modr, -8))*vecr
    part.a = part.a - ac
    part1.a = part1.a + ac
  
  
def calc_axel(pars):
    # calculates the accelerations of all particles and changes them
    for i in np.arange(N-1):
        for j in np.arange(i+1, N):
            axel(pars[i], pars[j])
        
        
def null_axel(pars):
    # nullifies all accelerations
    for i in np.arange(N):
        pars[i].a = np.array([0, 0, 0]) 
    
    
def first_move(pars):
    # moves all particles for the first time
    calc_axel(pars)
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
    
    
def maxwell(pars):
    list = np.array([])
    for i in np.arange(N):
        velocity = np.linalg.norm(pars[i].v)
        list = np.append(list, velocity)
    list = np.sort(list)
    for i in np.arange(N):
        maxwt.write(str(list[i]) + '\n')
        
        
def average_way(pars):
    summ = 0
    for i in np.arange(N):
        summ = summ + np.linalg.norm(pars[i].way)
    summ = summ/N
    wayt.write(str(summ) + '\n')
    

def timego(pars, tick):
    # starts the simulation
    print(0)
    first_move(pars)
    impulse(pars)
    energy(pars)
    average_way(pars)
    # Particle.display(pars[N//2])
    null_axel(pars)
    for i in np.arange(1, tick):
        calc_axel(pars)
        move(pars)
        # Particle.display(pars[N//2])
        impulse(pars)
        energy(pars)
        average_way(pars)
        null_axel(pars)
        if i%(tick//10) == 0:
            print (i)
    maxwell(pars)


def main():  
    t = int(1000) # ticks
    start = time.time() # точка отсчета времени
    pars = []
    cell_gen(pars) # генерация сеткой
    # rand_gen(pars) # случайная генерация, возможно работает как надо
    #for i in np.arange(N): # выводит характеристики всех частиц
    #    Particle.display(pars[i])
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
maxwt.close()
wayt.close()