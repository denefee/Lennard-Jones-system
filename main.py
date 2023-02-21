import math
import matplotlib as plt
import numpy as np
import time
import random
import os

# глобальные переменные
N = int(1000) # количество частиц
Mass = int(1) # масса материи
m = float(Mass/N) # масса одной частицы
Vmax = int(1)  # максимальная скорость частицы
d = float(0.01) # delta-окрестность
dt = float(0.001) # тик
eps = int(1) # потенциальная яма
sig = int(1) # расстояние, на котором энергия взаимодействия обнуляется
Leng = 100*sig # длина коробки


class Particle:
  """Класс частиц"""
  def __init__(self, c, v, a = np.array([0, 0, 0])):
    self.c = c
    self.v = v
    self.a = a
 
  def pot_calc(self):
    U = 4*eps()
    return 0

  def force(self):
    return 0

  def movement(self):
    return 0

  def potential(self):
    return 0

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
        v = np.random.uniform(-Vmax, Vmax, (1, 3))
        print (n)
        pars.append(Particle(c, v))
        if (n == N):
          flag = False
          break



def pot():
  Ux = 0
  Uy = 0
  Uz = 0

  U = np.array(Ux, Uy, Uz)
  return U


def main():
  start = time.time() # точка отсчета времени
  pars = []
  cell_gen(pars) # генерация сеткой
  # rand_gen(pars) # случайная генерация, пока не работает
  for i in np.arange(N): # выводит характеристики всех частиц
    Particle.display(pars[i])
  end = time.time() - start # собственно время работы программы
  print(end) # вывод времени


if __name__ == "__main__":
  main()

# test