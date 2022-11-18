import heapq
import time

import numpy as np
import numpy.typing as npt
import scipy.sparse.csgraph
from numba import njit
import math

from instance_generator import generate_tsp_instance

NDArrayInt = npt.NDArray[np.int_]

def bound(path: NDArrayInt, graph: NDArrayInt) -> float:
    total: int = 0

    # Criação de um array auxiliar para armazenar quais arestas foram checadas
    counted_edges: NDArrayInt = np.zeros((len(graph), 2))

    for i in range(len(graph)): 

        min_edge_cost: int = int(np.amin(graph[i], initial=np.inf))
        min_edge_cost_adjacent_node, = np.where(graph[i] == min_edge_cost)
        second_min_edge_cost: int = int(np.amin(graph[i], where = graph[i] > min_edge_cost, initial=np.inf))
        second_min_edge_cost_adjacent_node, = np.where(graph[i] == second_min_edge_cost)
        total += min_edge_cost + second_min_edge_cost
        counted_edges[i][0] = min_edge_cost_adjacent_node
        counted_edges[i][1] = second_min_edge_cost_adjacent_node

    # problema auqi, no already counted, tenho q checar pra aresta indo e voltando
    for i in range(len(path) - 1):
        
        edge_already_counted_1: bool = counted_edges[path[i]][0] == path[i + 1] or counted_edges[path[i]][1] == path[i + 1]
        edge_already_counted_2: bool = counted_edges[path[i + 1]][0] == path[i] or counted_edges[path[i + 1]][1] == path[i]
        
        if not edge_already_counted_1:
            total -= graph[path[i]][int(counted_edges[path[i]][1])]
            counted_edges[path[i]][1] = path[i + 1]
            total += graph[path[i]][path[i + 1]]
        
        if not edge_already_counted_2:
            total -= graph[path[i + 1]][int(counted_edges[path[i + 1]][1])]
            counted_edges[path[i + 1]][1] = path[i]
            total += graph[path[i + 1]][path[i]]

    return math.ceil(total/2)

def branch_and_bound_tsp(graph: NDArrayInt) -> NDArrayInt:
    #OBS: VAMOS ASSUMIR QUE 1 VEM SEMPRE ANTES DE 2
    #node[0] = estimaitva da subarvore, ex: 14
    #node[1] = custo total ate agora
    #node[2] = lista->caminho seguindo , ex: 0,2,4 ---> len(caminho) == number_of_nodes- 2 indica caminho encontrado
    #NOVE LEVEL = LEN(NODE[2])
    number_of_nodes: int = len(graph)
    root: tuple(int, int, list[int]) = (bound([0], graph), 0, [0])
    heap: heapq = [root]
    heapq.heapify(heap)
    best: npt.float_ = float("inf")
    solution: NDArrayInt = np.array([])
    while (len(heap) > 0):
        node = heapq.heappop(heap)
        print([chr(x+65) for x in node[2]])
        print(f"estimativa atual: {node[0]}")
        if len(node[2]) > number_of_nodes:
            if best > node[1]:
                best = node[1]
                solution = node[2]
        elif node[0] < best:
            if len(node[2]) < number_of_nodes:
                for k in range(1, number_of_nodes):
                    if 1 not in node[2] and k == 2:
                        continue
                    if k not in node[2] and bound(node[2] + [k], graph) < best:
                        heapq.heappush(heap, (bound(node[2] + [k], graph), node[1] + graph[node[2][-1]][k], node[2] + [k]))      
            elif bound(node[2] + [0], graph) < best:
                heapq.heappush(heap, (bound(node[2] + [0], graph), node[1] + graph[node[2][-1]][0], node[2] + [0]))
    return solution

#instancia_de_teste = np.array([[0,10,15,20], [0,0,35,25], [0,0,0,30], [0,0,0,0]])
instance = np.array([   [np.inf, 3, 1, 5, 8], 
                        [3, np.inf, 6, 7, 9], 
                        [1, 6, np.inf, 4, 2], 
                        [5, 7, 4, np.inf, 3], 
                        [8, 9, 2, 3, np.inf]])
#instance = generate_tsp_instance(5, 0, 10)

s = time.time()
path = branch_and_bound_tsp(instance)
print([chr(x+65) for x in path])
e = time.time()
print(f"Tempo: {e-s}")

#todo
# aind ata errado o bound
# arrumar heapq pra ordenar pelo parametro certo
# testese mais testes
# otimizar