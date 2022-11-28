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

parser = argparse.ArgumentParser(description="nao sei oq por na descirçao")
parser.add_argument("--dist", dest = "dist", type = str, help = "Tipo de distância utilizado entre os pontos da instância gerada")
parser.add_argument("--size", dest = "size", type = int, help = "Tamanho da instância que deve ser gerada")
parser.add_argument("--alg", dest = "alg", type = str, help = "Qual algoritmos deve ser utilizado para o cálculo")

ARGUMENTS = parser.parse_args()

def calculate_tsp(dist: str, size: int, alg: str):

    df: pd.DataFrame = pd.DataFrame(columns = ["size", "time", "path", "cost"])

    

    for i in range(1000):

        graph: NDArrayFloat = generate_tsp_instance(size = size, max_coordinate = 2000, dist = dist)

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
        df = pd.concat([df, pd.Series({"size": size, "time": round(end - start, 4), "path": path, "cost": round(cost, 4)}).to_frame().T], ignore_index  = True)
    
    df.to_csv(f"data/{alg}.csv", index = False)

def arq():
    graph = np.zeros((29, 29))

    with open("teste.txt", "r") as file:
        lines = file.readlines()
    
    edge_values = []
    for line in lines:
        edge_values.append(line.split(' '))

    for i in range(len(edge_values)):
        for j in range(len(edge_values[i])):
            graph[i, j + i + 1] = int(edge_values[i][j])
            graph[j + i + 1, i] = int(edge_values[i][j])

    path_opt = [0,27,5,11,8,25,2,28,4,20,1,19,9,3,14,17,13,16,21,10,18,24,6,22,7,26,15,12,23,0]
    cost_opt = utils.get_path_cost(path_opt, graph)
    print(f"cost_opt: {cost_opt}")


def main():

    dist: str = ARGUMENTS.dist

    size: int = ARGUMENTS.size

    alg: str = ARGUMENTS.alg

    calculate_tsp(dist, size,alg)
    

if __name__ == "__main__":
    main()