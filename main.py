from instance_generator import generate_tsp_instance
from branch_and_bound import branch_and_bound_tsp
from twice_around_the_tree import twice_around_the_tree
from christofides import christofides
import utils

import time
import argparse
import pandas as pd
import numpy as np
import numpy.typing as npt

NDArrayFloat = npt.NDArray[np.int_]
NDArrayInt = npt.NDArray[np.float_]

parser = argparse.ArgumentParser(description="nao sei oq por na descrição")
parser.add_argument("--dist", dest = "dist", type = str, help = "Tipo de distância utilizado entre os pontos da instância gerada")
parser.add_argument("--size", dest = "size", type = int, help = "Tamanho da instância que deve ser gerada")
parser.add_argument("--alg", dest = "alg", type = str, help = "Qual algoritmos deve ser utilizado para o cálculo")

ARGUMENTS = parser.parse_args()

# retorna caminho, custo do cmainho e tempo que demorou
def calculate_tsp(graph: NDArrayFloat, alg: str):

    if alg == "branch_and_bound":
        start = time.time()
        path = branch_and_bound_tsp(graph)
        end = time.time()
    elif alg == "twice_around_the_tree":
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

    g,_ = generate_tsp_instance(size, 5000)
    path = branch_and_bound_tsp(g)
    

if __name__ == "__main__":
    main()