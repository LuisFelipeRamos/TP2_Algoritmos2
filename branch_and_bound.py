import heapq
import time

import numpy as np
import numpy.typing as npt
import scipy.sparse.csgraph
from numba import njit

from instance_generator import generate_tsp_instance

NDArrayInt = npt.NDArray[np.int_]

def bound(path: NDArrayInt, graph: NDArrayInt) -> float:
    total: int = 0
    count = np.zeros(len(graph))
    for i in range(len(path) - 1):
        total += 2 * max(graph[path[i], path[i + 1]], graph[path[i + 1], path[i]])
        count[path[i]] += 1
        count[path[i + 1]] += 1
    for i in range(len(graph)):      
        if count[i] == 2:
            continue     
        elif count[i] == 1: # ta errado
            adjacencies = np.union1d(graph[i], graph[:, i])
            min1 = np.amin(adjacencies, where = adjacencies != 0, initial = adjacencies[-1])
            total += min1
            count[i] += 1
        elif count[i] == 0:
            adjacencies = np.union1d(graph[i], graph[:, i])
            min1 = np.amin(adjacencies, where = adjacencies != 0, initial = adjacencies[-1])
            min2 = np.amin(adjacencies, where = adjacencies > min1, initial = adjacencies[-1])
            total += min1 + min2
            count[i] += 2
    return total/2

def branch_and_bound_tsp(graph: NDArrayInt) -> NDArrayInt:
    #OBS: VAMOS ASSUMIR QUE 1 VEM SEMPRE ANTES DE 2
    #node[0] = estimaitva da subarvore, ex: 14
    #node[1] = custo total ate agora
    #node[2] = lista->caminho seguindo , ex: 0,2,4 ---> len(caminho) == number_of_nodes- 2 indica caminho encontrado
    #NOVE LEVEL = LEN(NODE[2])
    number_of_nodes: int = len(graph)
    root: tuple(int, int, list[int]) = (0, 0, [0])
    heap: heapq = [root]
    heapq.heapify(heap)
    best: npt.float_ = float("inf")
    solution: NDArrayInt = np.array([])
    while (len(heap) > 0):
        print(len(heap))
        node = heapq.heappop(heap)
        if len(node[2]) > number_of_nodes:
            if best > node[1]:
                best = node[1]
                solution = node[2]
        elif node[0] < best:
            if len(node[2]) < number_of_nodes:
                for k in range(1, number_of_nodes):
                    if k not in node[2] and bound(node[2] + [k], graph) < best:
                        heapq.heappush(heap, (bound(node[2] + [k], graph), node[1] + graph[node[2][-1]][k], node[2] + [k]))
                       
            elif bound(node[2] + [0], graph) < best:
                heapq.heappush(heap, (bound(node[2] + [0], graph), node[1] + graph[node[2][-1]][0], node[2] + [0]))
    return solution

#instancia_de_teste = np.array([[0,10,15,20], [0,0,35,25], [0,0,0,30], [0,0,0,0]])
#instancia_de_teste = np.array([[0, 3, 1, 5, 8], [0, 0, 6, 7, 9], [0, 0, 0, 4, 2], [0, 0, 0, 0, 3], [0, 0, 0, 0, 0]])
instance = generate_tsp_instance(5, 0, 10)

s = time.time()
path = branch_and_bound_tsp(instance)
e = time.time()
print(f"Tempo: {e-s}")
