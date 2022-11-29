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

def get_data(alg: str):

    df: pd.DataFrame = pd.DataFrame(columns = ["size", "dist", "time", "path", "cost"])
    for size in range(4, 11):
        for i in range(50):
            graph_euclidean, graph_manhattan = generate_tsp_instance(size, 5000)
            path_euclidean, cost_euclidean, time_euclidean = calculate_tsp(graph_euclidean, alg)
            path_manhattan, cost_manhattan, time_manhattan = calculate_tsp(graph_manhattan, alg)
            df = pd.concat([df, pd.Series({"size": size, "dist": "euclidean", "time": round(time_euclidean, 4), "path": path_euclidean, "cost": round(cost_euclidean, 4)}).to_frame().T], ignore_index  = True)
            df = pd.concat([df, pd.Series({"size": size, "dist": "manhattan", "time": round(time_manhattan, 4), "path": path_manhattan, "cost": round(cost_manhattan, 4)}).to_frame().T], ignore_index  = True)

    df.to_csv(f"data/{alg}.csv", index = False)

def main():

    dist: str = ARGUMENTS.dist

    size: int = ARGUMENTS.size

    alg: str = ARGUMENTS.alg

    get_data(alg)
    

if __name__ == "__main__":
    main()