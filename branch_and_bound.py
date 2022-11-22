import heapq
import time

import numpy as np
import numpy.typing as npt
import scipy.sparse.csgraph
from numba import njit
import math

from instance_generator import generate_tsp_instance

NDArrayInt = npt.NDArray[np.int_]

def graph_bound(graph: NDArrayInt) -> tuple:

    total: int = 0

    # Criação de um array auxiliar para armazenar quais arestas foram checadas
    counted_edges: NDArrayInt = np.zeros((len(graph), 2))

    # preciso checar ainda o segundo min Posso ter edges minimas de vlaores erradas, nao considero isso
    for i in range(len(graph)): 

        min_edge_cost: int = np.amin(graph[i], initial=np.inf)
        min_edge_cost_adjacent_node, = np.where(graph[i] == min_edge_cost)
        second_min_edge_cost: int = np.amin(graph[i], where = graph[i] > min_edge_cost, initial=np.inf)
        second_min_edge_cost_adjacent_node, = np.where(graph[i] == second_min_edge_cost)
        total += min_edge_cost + second_min_edge_cost
        counted_edges[i][0] = min_edge_cost_adjacent_node[0]
        counted_edges[i][1] = second_min_edge_cost_adjacent_node[0]
    
    return total/2, counted_edges

def bound(path: NDArrayInt, graph: NDArrayInt, total: float, counted_edges: NDArrayInt) -> float:

    total: int = 2 * total

    for i in range(len(path) - 1):
        
        edge_already_counted_1: bool = counted_edges[path[i]][0] == path[i + 1] or counted_edges[path[i]][1] == path[i + 1]
        edge_already_counted_2: bool = counted_edges[path[i + 1]][0] == path[i] or counted_edges[path[i + 1]][1] == path[i]
        
        if not edge_already_counted_1:
            total -= graph[path[i]][int(counted_edges[path[i]][1])]
            total += graph[path[i]][path[i + 1]]
        
        if not edge_already_counted_2:
            total -= graph[path[i + 1]][int(counted_edges[path[i + 1]][1])]
            total += graph[path[i + 1]][path[i]]

    return total/2

def branch_and_bound_tsp(graph: NDArrayInt) -> NDArrayInt:
    #OBS: VAMOS ASSUMIR QUE 1 VEM SEMPRE ANTES DE 2
    #node[0] = estimaitva da subarvore, ex: 14
    #node[1] = custo total ate agora
    #node[2] = lista->caminho seguindo , ex: 0,2,4 ---> len(caminho) == number_of_nodes- 2 indica caminho encontrado
    #node[3] = 1 esta antes de 2(false por vacuidade, true cc)
    #NOVE LEVEL = LEN(NODE[2])
    
    graph_initial_bound, graph_initial_bound_counted_edges = graph_bound(graph)

    number_of_nodes: int = len(graph)
    root: tuple(np.int_, np.int_, NDArrayInt, bool) = graph_initial_bound, 0, [0], False
    heap: heapq = [root]
    heapq.heapify(heap)
    best: npt.float_ = float("inf")
    solution: NDArrayInt = np.array([])
    while (len(heap) > 0):
        print(len(heap))
        node = heapq.heappop(heap)
        #print([chr(x+65) for x in node[2]])
        #print(f"estimativa atual: {node[0]}")
        if len(node[2]) > number_of_nodes:
            if best > node[1]:
                best = node[1]
                solution = node[2]
        elif node[0] < best:
            if len(node[2]) < number_of_nodes:
                for k in range(1, number_of_nodes):
                    if not node[3] and k == 2:
                        continue
                    new_bound: np.float_ = bound(node[2] + [k], graph, graph_initial_bound, graph_initial_bound_counted_edges)
                    if k not in node[2] and new_bound < best:
                        heapq.heappush(heap, (new_bound, node[1] + graph[node[2][-1]][k], node[2] + [k], node[3] or k == 1)) 
                        
            new_bound: np.float_ = bound(node[2] + [0], graph, graph_initial_bound, graph_initial_bound_counted_edges)
            if new_bound < best and len(node[2]) == number_of_nodes:
                heapq.heappush(heap, (new_bound, node[1] + graph[node[2][-1]][0], node[2] + [0], True))
                
    return solution

instance = np.array([   [np.inf, 3, 1, 5, 8], 
                        [3, np.inf, 6, 7, 9], 
                        [1, 6, np.inf, 4, 2], 
                        [5, 7, 4, np.inf, 3], 
                        [8, 9, 2, 3, np.inf]])

instance = generate_tsp_instance(4, 0, 10)

s = time.time()
path = branch_and_bound_tsp(instance)
print([chr(x+65) for x in path])
e = time.time()
print(f"Tempo: {e-s}")

#todo
# otimizar bound
# arrumar heapq pra ordenar pelo parametro certo (primeiro estimativa e se empatar pelo index do no)
# otimizar