from instance_generator import generate_tsp_instance
from branch_and_bound import branch_and_bound_tsp
from twice_around_the_tree import twice_around_the_tree
from christofides import christofides
import utils

import time
import argparse
import numpy as np
import numpy.typing as npt

NDArrayFloat = npt.NDArray[np.int_]
NDArrayInt = npt.NDArray[np.float_]

parser = argparse.ArgumentParser(description="Parâmetros de linha de comando para o trabalho prático de Algoritmos II.")
parser.add_argument("--dist", dest = "dist", type = str, help = "Tipo de distância utilizado no cálculo entre os pontos da instância gerada")
parser.add_argument("--size", dest = "size", type = int, help = "Tamanho da instância que deve ser gerada (potência de 2 utilizada)")
parser.add_argument("--alg", dest = "alg", type = str, help = "Qual algoritmo deve ser utilizado para o cálculo")

ARGUMENTS = parser.parse_args()

def calculate_tsp(graph: NDArrayFloat, alg: str):

    if alg == "branch-and-bound":
        start = time.time()
        path = branch_and_bound_tsp(graph)
        end = time.time()
    elif alg == "twice-around-the-tree":
        start = time.time()
        path = twice_around_the_tree(graph)
        end = time.time()
    elif alg == "christofides":
        start = time.time()
        path = christofides(graph)
        end = time.time()
    else:
        print("Não identificamos esse algoritmo :(")
        return

    cost = utils.get_path_cost(path, graph)
    
    return path, cost, end - start

def main():

    dist: str = ARGUMENTS.dist

    size: int = ARGUMENTS.size

    alg: str = ARGUMENTS.alg

    graph_euclidean, graph_manhattan = generate_tsp_instance(size)
    
    if dist == "euclidean":
        path, cost, time = calculate_tsp(graph_euclidean, alg)
    elif dist == "manhattan":
        path, cost, time = calculate_tsp(graph_manhattan, alg)
    else:
        print("Não conheço essa distância!")
    print(f"Algoritmo executado: {alg}")
    print()
    print(f"Tempo de execução: {round(time, 3)} segundos")
    print()
    minimized_path: str = "-".join(str(v) for v in path)
    if size > 4:
        first_half = " - ".join(str(v) for v in path[:9])
        second_half = " - ".join(str(v) for v in path[-8:])
        minimized_path = first_half + " ... " + second_half
        print(f"O ciclo hamiltoniano encontrado foi {minimized_path}")
    else:
        path = " - ".join(str(v) for v in path)
        print(f"O ciclo hamiltoniano encontrado foi {path}")
    print()
    print(f"O custo total de percorrer o ciclo foi de {round(cost, 2)}")
    print()

if __name__ == "__main__":
    main()
