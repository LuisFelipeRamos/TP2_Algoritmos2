# Calcula a distância Manhattan entre dois pontos bidimensionais
def manhattan_distance(point_1: list[int], point_2: list[int]) -> int:
    return abs(point_1[0] - point_2[0]) + abs(point_1[1] - point_2[1])
