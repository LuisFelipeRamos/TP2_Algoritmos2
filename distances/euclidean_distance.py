import math

# Calcula a distância euclidiana entre dois pontos bidimensionais utilizando a biblioteca math
def euclidean_distance(point_1: list[int], point_2: list[int]) -> float:
    return math.dist(point_1, point_2)
