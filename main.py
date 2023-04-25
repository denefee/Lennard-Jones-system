import math
import numpy as np
import time

from particleclass import Particle

# глобальные переменные
N = int(2)  # количество частиц
Vmax = float(1.0)  # максимальная скорость частицы
dt = float(0.001)  # тик
Leng = int(10)  # длина коробки
half = Leng/2  # половина длины коробки


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
    particle_is_even = True
    edge = math.ceil(np.cbrt(N))
    dl = Leng/edge
    dl_half = dl/2
    for i in np.arange(edge):
        for j in np.arange(edge):
            for k in np.arange(edge):
                c = dl_half + np.array([i, j, k])*dl
                if particle_is_even:
                    v = np.random.uniform(-Vmax, Vmax, (3))
                    if (n == N-1):
                        v = np.zeros(3)
                        pars.append(Particle(n, c, v))
                        return 0
                    pars.append(Particle(n, c, v))
                    particle_is_even = False
                    n += 1
                else:
                    v = -v
                    pars.append(Particle(n, c, v))
                    if (n == N-1):
                        return 0
                    particle_is_even = True
                    n += 1


def axel(part, part1):
    # calculates the forces of interaction between these particles
    # and changes their accelerations
    vecr = Particle.vec_to_virtual_copy(part.c, part1.c)
    modr = np.linalg.norm(vecr)
    ac = 24*(2*np.power(modr, -14) - np.power(modr, -8))*vecr
    part.a -= ac
    part1.a += ac


def calc_axel(pars):
    # calculates the accelerations of all particles and changes them
    for i in np.arange(N-1):
        for j in np.arange(i+1, N):
            axel(pars[i], pars[j])


def null_axel(pars):
    # nullifies all accelerations
    for i in np.arange(N):
        pars[i].a = np.zeros(3)


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
    u = 4*(np.power(modr, -12) - np.power(modr, -6))
    return u


def impulse(pars):
    # calculates the total momentum of the system
    summ = np.zeros(3)
    for i in np.arange(N):
        summ += pars[i].v
    impt.write(np.array2string(summ) + '\n')


def poten_eng(pars):
    # calculates the potential energy of the interaction of all particles
    pot = 0.0
    for i in np.arange(N-1):
        for j in np.arange(i+1, N):
            pot += potentwo(pars[i], pars[j])
    pott.write(str(pot) + '\n')
    return pot


def kinetic_eng(pars):
    # calculates the total kinetic energy of the system
    kin = 0.0
    for i in np.arange(N):
        kin += (np.linalg.norm(pars[i].v)**2)/2
    kint.write(str(kin) + '\n')
    return kin


def energy(pars):
    # calculates the total mechanical energy of the system
    pot = poten_eng(pars)
    kin = kinetic_eng(pars)
    summ = pot + kin
    mect.write(str(summ) + '\n')


def maxwell(pars):
    list = np.zeros(N)
    for i in np.arange(N):
        list[i] = np.linalg.norm(pars[i].v)
    list = np.sort(list)
    for i in np.arange(N):
        maxwt.write(str(list[i]) + '\n')


def average_way(pars):
    summ = 0.0
    for i in np.arange(N):
        summ += np.linalg.norm(pars[i].way)
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
        if i % (tick//10) == 0:
            print(i)
    maxwell(pars)


def main():
    t = int(100)  # ticks
    start = time.time()  # точка отсчета времени
    pars = []
    cell_gen(pars)  # генерация сеткой  
    # for i in np.arange(N): # выводит характеристики всех частиц
    #    Particle.display(pars[i])
    timego(pars, t)
    end = time.time() - start  # собственно время работы программы
    print(end)  # вывод времени


if __name__ == "__main__":
    main()


# close files with data
impt.close()
kint.close()
mect.close()
pott.close()
maxwt.close()
wayt.close()
