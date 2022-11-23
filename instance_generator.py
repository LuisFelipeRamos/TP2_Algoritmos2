import random
import math
import numpy as np
from numpy.random import default_rng
import numpy.typing as npt

NDArrayInt = npt.NDArray[np.int_]
NDArrayFloat = npt.NDArray[np.float_]

# Calcula a distância euclidiana entre dois pontos bidimensionais
def euclidean_distance(point_1: list[int], point_2: list[int]) -> float:
    return math.dist(point_1, point_2)

# Calcula a distância Manhattan entre dois pontos bidimensionais
def manhattan_distance(point_1: list[int], point_2: list[int]) -> int:
    return abs(point_1[0] - point_2[0]) + abs(point_1[1] - point_2[1])

# Gera instância para testes de execução dos algoritmos para o Caixeiro Viajante
# Recebe um inteiro size. O número de vértices da instância gerada será 2**size
# Recebe os inteiros que dizem quais os limites inferior e superior dos pontos
# Os vértices são pontos no plano cartesiano. Os pesos entre os vértices será computado de duas formas diferentes:
# Distância euclidiana e distância Manhatan

def generate_tsp_instance(size: int, max_coordinate: int, dist: str = "euclidean") -> NDArrayInt:

    number_of_nodes: int = int(math.pow(2, size))
    graph: NDArrayInt = np.ones((number_of_nodes, number_of_nodes), dtype=float)*np.inf
    rng = default_rng() # gerar sem replacement
    # os pontos possuem coordenadas entre 0 e numeros de nos*4
    nodes_coordinates: NDArrayInt = rng.choice(number_of_nodes*4, size=(number_of_nodes, 2), replace=False)
    #potencial de melhora aqui
    if dist == "euclidean":
        for i in range(number_of_nodes):
            for j in range(i+1, number_of_nodes):
                distance: float = euclidean_distance(nodes_coordinates[i], nodes_coordinates[j])
                graph[i, j] = distance
                graph[j, i] = distance
    else:
        for i in range(number_of_nodes):
            for j in range(i+1, number_of_nodes):
                distance: float = manhattan_distance(nodes_coordinates[i], nodes_coordinates[j])
                graph[i, j] = distance
                graph[j, i] = distance
    return graph


""" import time
s = time.time()
i = generate_tsp_instance(10, 10)
e = time.time()
print(f"{e-s}") """