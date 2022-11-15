import numpy as np
import numpy.typing as npt
from numba import njit
import scipy.sparse.csgraph
import heapq

NDArrayInt = npt.NDArray[np.int_]

import networkx as nx
instancia_de_teste = np.array([[0, 3, 5, 1, 8], [0, 0, 6, 7, 9], [0, 0, 0, 4, 2], [0, 0, 0, 0, 3], [0, 0, 0, 0, 0]])

def bound(nodes: NDArrayInt, graph: NDArrayInt):
    pass

#@njit(cache = True)
def branch_and_bound_tsp(graph: NDArrayInt) -> NDArrayInt:
    #OBS: VAMOS ASSUMIR QUE 1 VEM SEMPRE ANTES DE 2
    #node[0] = estimaitva da subarvore, ex: 14
    #node[1] = custo total ate agora
    #node[2] = lista->caminho seguindo , ex: 0,2,4 ---> len(caminho) == number_of_nodes- 2 indica caminho encontrado
    #NOVE LEVEL = LEN(NODE[2])
    number_of_nodes: int = len(graph)
    root: tuple(int, int, list[int]) = (0, 0, [0])
    heap: heapq = heapq.heapify([])
    best: npt.float_ = npt.inf
    solution: NDArrayInt = np.array([])
    while (len(heap) > 0):
        node = heap.heappop()
        if len(node[2]) == number_of_nodes - 2:
            if best > node[1]:
                best = node[1]
                solution = node[2]
        elif node[0] < best:
            if len(node[2]) < number_of_nodes:
                for k in range(1, number_of_nodes):
                    if k not in node[2] and bound(node[2] + [k]) < best:
                        heap.heappush((bound(node[2] + [k]), node[1] + graph[node[2][-1]][k]), node[2] + [k])
            elif bound(node[2] + [0]) < best:
                heap.heappush(bound(node[2] + [0]), node[1] + graph[node[2][-1]][0], node[2] + [0])

