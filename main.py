import math
import numpy as np
import time

from particleclass import Particle

# глобальные переменные
N = int(8)  # количество частиц
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


def cell_gen(particles):
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
                        particles.append(Particle(n, c, v))
                        return 0
                    particles.append(Particle(n, c, v))
                    particle_is_even = False
                    n += 1
                else:
                    particles.append(Particle(n, c, -v))
                    if (n == N-1):
                        return 0
                    particle_is_even = True
                    n += 1


def null_axel(particles):
    # nullifies all accelerations
    for i in np.arange(N):
        particles[i].a = np.zeros(3)


def axel(part, part1):
    # calculates the forces of interaction between these particles
    # and changes their accelerations
    vect_r = Particle.vec_to_virtual_copy(part.c, part1.c)
    abs_r = np.linalg.norm(vect_r)
    ac = 24*(2*np.power(abs_r, -14) - np.power(abs_r, -8))*vect_r
    part.a -= ac
    part1.a += ac


def calc_axel(particles):
    # calculates the accelerations of all particles and changes them
    for i in np.arange(N-1):
        for j in np.arange(i+1, N):
            axel(particles[i], particles[j])


def first_move(particles):
    # moves all particles for the first time
    calc_axel(particles)
    for i in np.arange(N):
        Particle.first_move(particles[i])


def move(particles):
    # moves all particles
    for i in np.arange(N):
        Particle.move(particles[i])


def potentwo(part, part1):
    # calculates the potential energy of the interaction of two particles
    vect_r = Particle.vec_to_virtual_copy(part.c, part1.c)
    abs_r = np.linalg.norm(vect_r)
    u = 4*(np.power(abs_r, -12) - np.power(abs_r, -6))
    return u


def impulse(particles):
    # calculates the total momentum of the system
    summ = np.zeros(3)
    for i in np.arange(N):
        summ += particles[i].v
    impt.write(np.array2string(summ) + '\n')


def poten_eng(particles):
    # calculates the potential energy of the interaction of all particles
    pot = 0.0
    for i in np.arange(N-1):
        for j in np.arange(i+1, N):
            pot += potentwo(particles[i], particles[j])
    pott.write(str(pot) + '\n')
    return pot


def kinetic_eng(particles):
    # calculates the total kinetic energy of the system
    kin = 0.0
    for i in np.arange(N):
        kin += (np.linalg.norm(particles[i].v)**2)/2
    kint.write(str(kin) + '\n')
    return kin


def energy(particles):
    # calculates the total mechanical energy of the system
    pot = poten_eng(particles)
    kin = kinetic_eng(particles)
    summ = pot + kin
    mect.write(str(summ) + '\n')


def maxwell(particles):
    list = np.zeros(N)
    for i in np.arange(N):
        list[i] = np.linalg.norm(particles[i].v)
    list = np.sort(list)
    for i in np.arange(N):
        maxwt.write(str(list[i]) + '\n')


def average_way(particles):
    summ = 0.0
    for i in np.arange(N):
        summ += np.linalg.norm(particles[i].way)
    summ = summ/N
    wayt.write(str(summ) + '\n')


def timego(particles, tick):
    # starts the simulation
    print(0)
    first_move(particles)
    # impulse(particles)
    energy(particles)
    average_way(particles)
    null_axel(particles)
    for i in np.arange(1, tick):
        calc_axel(particles)
        move(particles)
        # impulse(particles) commented out because momentum is maintained
        energy(particles)
        average_way(particles)
        null_axel(particles)
        if i % (tick//10) == 0:
            print(i)
    maxwell(particles)


def main():
    t = int(100000)  # ticks
    start = time.time()  # точка отсчета времени
    particles = [] # particle spisok
    cell_gen(particles)  # генерация сеткой  
    timego(particles, t)
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
