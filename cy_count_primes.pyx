import math
import matplotlib as plt
import numpy as np
import os
import cython as cy
import cythonbuilder

    
def count_primes(limit:int) -> int:
  """ Vanilla python that returns the number of primes between 0 and [limit] """
  count:int = 0
  for candidate_int in range(limit):
    if (candidate_int > 1):
      for factor in range(2, candidate_int):
        if candidate_int % factor == 0:
          break
      else:
        count += 1
  return count


def main():
    print(count_primes(10000))

if __name__ == "__main__":
    main()