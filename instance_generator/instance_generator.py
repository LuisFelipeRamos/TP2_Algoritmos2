import random
import math
import numpy as np
import cProfile
from numba import njit, vectorize, int64
import time
from itertools import combinations
import numpy.typing as npt

NDArrayInt = npt.NDArray[np.int_]
NDArrayFloat = npt.NDArray[np.float_]

# Calcula a distância euclidiana entre dois pontos bidimensionais
def euclidean_distance(point_1: list[int], point_2: list[int]) -> float:
    return math.dist(point_1, point_2)

# Calcula a distância Manhattan entre dois pontos bidimensionais
def manhattan_distance(point_1: list[int], point_2: list[int], distance_measure: str = "euclidean") -> int:
    return abs(point_1[0] - point_2[0]) + abs(point_1[1] - point_2[1])

# Gera instância para testes de execução dos algoritmos para o Caixeiro Viajante
# Recebe um inteiro size. O número de vértices da instância gerada será 2**size
# Recebe os inteiros que dizem quais os limites inferior e superior dos pontos
# Os vértices são pontos no plano cartesiano. Os pesos entre os vértices será computado de duas formas diferentes:
# Distância euclidiana e distância Manhatan

def generate_tsp_instance(size: int, min_coordinate: int, max_coordinate: int, ) -> NDArrayInt:

    number_of_vertexes: int = int(math.pow(2, size))
    graph: NDArrayInt = np.zeros((number_of_vertexes, number_of_vertexes), dtype=float)
    vertexes_coordinates: NDArrayInt = np.random.randint(low = min_coordinate, high = max_coordinate, size = (int(math.pow(2, size)), 2))
    edges: NDArrayInt = list(combinations(np.arange(number_of_vertexes), 2))
    #potencial de melhora aqui
    for edge in edges:
        graph[edge[0], edge[1]] = euclidean_distance(vertexes_coordinates[edge[0]], vertexes_coordinates[edge[1]])

    return graph
