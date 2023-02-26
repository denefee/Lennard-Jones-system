import math
import matplotlib as plt
import numpy as np
import time
import random
import os

# глобальные переменные
N = int(1000) # количество частиц
Mass = int(1) # масса материи
# m = float(Mass/N) # масса одной частицы
Vmax = int(1)  # максимальная скорость частицы
# d = float(0.01) # delta-окрестность
dt = float(0.001) # тик
Leng = int(10) # длина коробки


class Particle:
  """Класс частиц"""
  def __init__(self, c, v, a = np.array([0, 0, 0])):
    self.c = c
    self.v = v
    self.a = a
    self.lc = c

  def display(self):
    return print('Координаты: ' + np.array2string(self.c) + 
    ', Скорость: ' + np.array2string(self.v) + 
    ', Ускорение: ' + np.array2string(self.a))


def rand_gen_char(pars):
  # генерирует частицу с уникальной случайной координатой
  n = 0
  c = np.random.uniform(0, Leng, (1, 3))
  for i in np.arange(pars.size):
    a = pars[i]
    if np.all((c >= a.c - d)and(c <= a.c + d)): # не работает, реализовать через длину вектора
      c = np.random.uniform(0, Leng, (1, 3))
      i = -1
      continue
  v = np.random.uniform(-Vmax, Vmax, (1, 3))
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
  dl = Leng / (reb - 1)
  for i in np.arange(reb):
    x = i*dl
    if (flag == False):
      break
    for j in np.arange(reb):
      y = j*dl
      if (flag == False):
        break
      for k in np.arange(reb):
        z = k*dl
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
  vecr = part1.c - part.c
  modr = np.linalg.norm(vecr)
  ac = (24/(modr**8) - 48/(modr**14))*vecr
  part.a = part.a + ac
  part1.a = part1.a - ac
  
  
def calc_ax(pars):
  # вычисляет ускорения всех частиц
  for i in np.arange(N-1):
    for j in np.arange(i+1, N):
      axel(pars[i], pars[j])
      

def first_move_one(part):
  # двигает частицу в первый раз
  part.c = part.c + part.v*dt + 0.5*(dt**2)*part.a


def first_move(pars):
  # двигает все частицы в первый раз
  for i in np.arange(N):
    first_move_one(pars[i])


def move_one(part):
  #двигает частицу используя схему Верле
  mem = part.c
  part.c = 2*part.c - part.lc + (dt**2)*part.a
  part.lc = mem
  part.v += part.a*dt
    
    
def move(pars):
  #двигает все частицы
  for i in np.arange(N):
    move_one(pars[i])
   
    
def timego(pars, tick):
  first_move(pars)
  for i in np.arange(tick - 1):
    print(i)
    calc_ax(pars)
    move(pars)
    Particle.display(pars[N//2])


def main():  
  zeit = int(100)
  start = time.time() # точка отсчета времени
  pars = []
  cell_gen(pars) # генерация сеткой
  Particle.display(pars[N//2])
  # rand_gen(pars) # случайная генерация, пока не работает
  #for i in np.arange(N): # выводит характеристики всех частиц
  #  Particle.display(pars[i])
  timego(pars, zeit)
  end = time.time() - start # собственно время работы программы
  print(end) # вывод времени


if __name__ == "__main__":
  main()