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
# Recebe o inteiro que indica acoordenada máxima que os pontos podem ter, por padrão esse valor é 5000
# Os vértices são pontos no plano cartesiano. Os pesos entre os vértices será computado de duas formas diferentes:
# Distância euclidiana e distância Manhatan

def generate_tsp_instance(size: int, max_coordinate: int = 5000) -> NDArrayInt:

    number_of_nodes: int = int(math.pow(2, size))
    graph_euclidean: NDArrayFloat = np.zeros((number_of_nodes, number_of_nodes), dtype=float)
    graph_manhattan: NDArrayInt = np.zeros((number_of_nodes, number_of_nodes), dtype=float)
    rng = default_rng()
    nodes_coordinates: NDArrayInt = rng.choice(max_coordinate, size = ( number_of_nodes, 2), replace = False)
    for i in range(number_of_nodes):
        for j in range(i+1, number_of_nodes):
            distance: float = euclidean_distance(nodes_coordinates[i], nodes_coordinates[j])
            graph_euclidean[i, j] = distance
            graph_euclidean[j, i] = distance

    for i in range(number_of_nodes):
        for j in range(i+1, number_of_nodes):
            distance: float = manhattan_distance(nodes_coordinates[i], nodes_coordinates[j])
            graph_manhattan[i, j] = distance
            graph_manhattan[j, i] = distance
            
    return graph_euclidean, graph_manhattan
