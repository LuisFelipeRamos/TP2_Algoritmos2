import random
import math
import numpy as np
import cProfile
from numba import njit, vectorize, int64
import time

# Gera instância para testes de execução dos algoritmos para o Caixeiro Viajante
# Recebe um inteiro size. O número de vértices da instância gerada será 2**size
# Recebe os inteiros que dizem quais os limites inferior e superior dos pontos
# Os vértices são pontos no plano cartesiano. Os pesos entre os vértices será computado de duas formas diferentes:
# Distância euclidiana e distância Manhatan
@njit(cache=True)
def generate_instance(size: int, min_coordinate: int, max_coordinate: int) -> list[list[int]]:
    vertexes: list[list[int]] = np.random.randint(low = min_coordinate, high = max_coordinate, size = (int(math.pow(2, size)), 2))
    return vertexes
