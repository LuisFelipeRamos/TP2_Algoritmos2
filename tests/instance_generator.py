import random
import math
import numpy as np
import cProfile

# Gera instância para testes de execução dos algoritmos para o Caixeiro Viajante
# Recebe um inteiro size. O número de vértices da instância gerada será 2**size
# Os vértices são pontos no plano cartesiano. Os pesos entre os vértices será computado de duas formas diferentes:
# Distância euclidiana e distância Manhatan
def generate_instance(size: int, min_coordinate: int, max_coordinate: int) -> list:
    vertexes: list[list[int]] = np.random.randint(low = min_coordinate, high = max_coordinate, size = (int(math.pow(2, size)), 2))
    
generate_instance(4,0,10)
#cProfile.runctx("g(x, y, z)", {"x": 4, "y": 0, "z": 10, "g": generate_instance}, {})