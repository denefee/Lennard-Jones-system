import math
import matplotlib as plt
import numpy as np
import time
import random
import os

# глобальные переменные
N = int(100) # количество частиц
Mass = int(1) # масса материи
# m = float(Mass/N) # масса одной частицы
Vmax = int(3)  # максимальная скорость частицы
d = float(0.0001) # delta-окрестность
dt = float(0.001) # тик
Leng = int(1) # длина коробки


class Particle:
    """Класс частиц"""
    def __init__(self, c, v, a = np.array([0, 0, 0]), lc = np.array([0, 0, 0])):
        self.c = c
        self.v = v
        self.a = a
        self.lc = lc

    def display(self):
        return print('Координаты: ' + np.array2string(self.c) + 
        ', Скорость: ' + np.array2string(self.v) + 
        ', Ускорение: ' + np.array2string(self.a))


def rand_gen_char(pars):
    # генерирует частицу с уникальной случайной координатой
    n = 0
    c = np.random.uniform(0, Leng, (3))
    for i in np.arange(pars.size):
        a = pars[i]
        if (np.linalg.norm(c - a.c) <= d): # возможно работает
            c = np.random.uniform(0, Leng, (3))
            i = -1
            continue
    v = np.random.uniform(-Vmax, Vmax, (3))
    n += 1
    print (n)
    return Particle(c, v)
  
  
def rand_gen(pars):
    # генерирует N частиц с уникальной рандомной координатой
    for i in np.arange(N):
        pars.append(rand_gen_char(pars))
        continue


def cell_gen(pars):
    # генерация сеткой
    n = 0
    flag = True
    reb = math.ceil(N**(1/3))
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
                v = np.random.uniform(-Vmax, Vmax, (3))
                print (n)
                pars.append(Particle(c, v))
                if (n == N):
                    flag = False
                    break


def axel(part, part1):
    # считает силы взаимодействия между данными частицами и меняет их ускорения
    half = Leng/2
    vecr = part1.c - part.c
    p1copy = np.copy(part1.c)
    for i in np.arange(3):
        if (vecr[i] > half):
            p1copy[i] = p1copy[i] - Leng
        if (vecr[i] < -half):
            p1copy[i] = p1copy[i] + Leng
    vecr = p1copy - part.c
    modr = np.linalg.norm(vecr)
    if (modr > d):
        ac = (24/(modr**8) - 48/(modr**14))*vecr
        part.a = part.a + ac
        part1.a = part1.a - ac
  
  
def calc_ax(pars):
    # вычисляет ускорения всех частиц
    for i in np.arange(N-1):
        for j in np.arange(i+1, N):
            axel(pars[i], pars[j])
        
        
def null_ax(pars):
    # обнуляет все ускорения
    for i in np.arange(N):
        pars[i].a = np.array([0, 0, 0]) 


def one_first_move(part):
    # двигает одну частицу в первый раз
    mem = np.copy(part.c)
    part.c = part.c + dt*(part.v) + 0.5*dt*dt*(part.a)
    part.v = part.v + dt*(part.a)
    part.lc = np.copy(mem)
    
    
def first_move(pars):
    # двигает все частицы в первый раз
    calc_ax(pars)
    for i in np.arange(N):
        one_first_move(pars[i])


def move_one(part):
    #двигает частицу используя схему Верле
    mem = np.copy(part.c)
    part.c = 2*part.c - part.lc + part.a*dt**2
    part.lc = np.copy(mem)
    part.v = part.v + part.a*dt
    
    
def move(pars):
    #двигает все частицы
    for i in np.arange(N):
        move_one(pars[i])  
        
        
def begin_impulse(pars):
    # считает начальный импульс
    summ = np.array([0.0, 0.0, 0.0])
    for i in np.arange(N):
        summ = summ + pars[i].v
    print('Суммарный начальный импульс: ' + np.array2string(summ))
    return summ
    
    
def impulse(pars, imp):
    # считает как изменился испульс по сранвению с началом
    summ = np.array([0.0, 0.0, 0.0])
    for i in np.arange(N):
        summ = summ + pars[i].v
    summ = summ - imp
    print('Изменение начального импульса: ' + np.array2string(summ))
        
        
def potentwo(part, part1):
    # считает потенциальную энергию взаимодействия двух частиц
    half = Leng/2
    vecr = part1.c - part.c
    p1copy = np.copy(part1.c)
    for i in np.arange(3):
        if (vecr[i] > half):
            p1copy[i] = p1copy[i] - Leng
        if (vecr[i] < -half):
            p1copy[i] = p1copy[i] + Leng
    vecr = p1copy - part.c
    modr = np.linalg.norm(vecr)
    if (modr > d):
        u = 4/(modr**12) - 4/(modr**6)
    else:
        u = 0
    return u
        
        
def calc_poten(pars):
    # вычисляет потенциальную энергию взаимодейсвтия всех частиц
    pot = 0
    for i in np.arange(N-1):
        for j in np.arange(i+1, N):
            pot = pot + potentwo(pars[i], pars[j])
    return pot
    
    
def begin_energy(pars):
    summ = 0
    for i in np.arange(N):
        summ = summ + (np.linalg.norm(pars[i].v)**2)/2
    summ = summ + calc_poten(pars)
    print('Суммарная энергия: ' + np.array2string(summ))
    return summ
    
    
def energy(pars, eng):
    summ = 0
    for i in np.arange(N):
        summ = summ + (np.linalg.norm(pars[i].v)**2)/2
    summ = summ + calc_poten(pars)
    print('Флуктуация энергии: ' + np.array2string(summ - eng))

    
def timego(pars, tick):
    # запускает счёт времени
    print(0)
    first_move(pars)
    imp = begin_impulse(pars)
    eng = begin_energy(pars)
    # Particle.display(pars[N//2])
    null_ax(pars)
    for i in np.arange(tick - 1):
        print(i + 1)
        calc_ax(pars)
        move(pars)
        # Particle.display(pars[N//2])
        null_ax(pars)
        impulse(pars, imp)
        energy(pars, eng)


def main():  
    t = int(100) # тики
    start = time.time() # точка отсчета времени
    pars = []
    cell_gen(pars) # генерация сеткой
    # Particle.display(pars[N-1])
    # rand_gen(pars) # случайная генерация, возможно работает как надо
    #for i in np.arange(N): # выводит характеристики всех частиц
    #  Particle.display(pars[i])
    timego(pars, t)
    end = time.time() - start # собственно время работы программы
    print(end) # вывод времени


if __name__ == "__main__":
    main()