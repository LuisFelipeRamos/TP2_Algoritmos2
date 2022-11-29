from __future__ import annotations

import heapq
import time
import numpy as np
import numpy.typing as npt
import networkx as nx
import math
import cProfile

from instance_generator import generate_tsp_instance

NDArrayInt = npt.NDArray[np.int_]
NDArrayFloat = npt.NDArray[np.float_]

class Node:

    def __init__(self, bound: np.float_, cost: np.float_, path: NDArrayInt, counted_edges: NDArrayInt, graph_size: np.int_):
        self.bound: np.float_ = bound
        self.cost: np.float_ = cost
        self.path: NDArrayInt = path
        self.level: np.int_ = len(path)
        self.counted_edges: NDArrayInt = counted_edges
        self.visited: NDArrayInt = np.zeros(graph_size)
        self.visited[path] = 1
        self.oneIsVisited: bool = self.visited[1]
    
    def __lt__(self, other: Node) -> bool:
        if self.bound != other.bound:
            return self.bound < other.bound
        return self.cost < other.cost

def graph_bound(graph: NDArrayInt) -> np.float_:
    total: int = 0
    counted_edges: NDArrayInt = np.zeros((len(graph), 3), dtype = np.int_)
    for i in range(len(graph)):
        #pega dois menors elementos (pula 0 na primeira)
        a, b = np.partition(graph[i], 2)[1:3]

        # menor aresta em i,0. Segunda menor, se igual a menor é outr no se nao pega novo no
        counted_edges[i, 0] = np.where(graph[i] == a)[0][0]
        second_min_possible_indexes = np.where(graph[i] == b)[0]
        if second_min_possible_indexes[0] != counted_edges[i, 0]:
            counted_edges[i, 1] = second_min_possible_indexes[0] 
        else:
            counted_edges[i, 1] = second_min_possible_indexes[1]
        total += a + b

    return total/2, counted_edges

# devo conseguir fzr isso em tempo constante
def bound(prev_bound: np.float_, prev_node: np.int_, new_node: np.int_, counted_edges: NDArrayInt, graph: NDArrayFloat) -> np.float_:

    total: np.float_ = prev_bound * 2
    new_edge_value: np.float_ = graph[prev_node, new_node]
    total += new_edge_value * 2


    if counted_edges[prev_node, 0] == new_node:
        total -= new_edge_value
  
    elif counted_edges[prev_node, 1] == new_node:
        total -= new_edge_value
    
    else:
        if counted_edges[prev_node, 2] == 0:
            total -= graph[prev_node, counted_edges[prev_node, 1]]
        else:
            total -= graph[prev_node, counted_edges[prev_node, 0]]


    if counted_edges[new_node, 0] == prev_node:
        total -= new_edge_value
 
    elif counted_edges[new_node, 1] == prev_node:
        total -= new_edge_value
        counted_edges[new_node, 2] = 1
  
    else:
        total -= graph[new_node, counted_edges[new_node, 1]]
        counted_edges[new_node, 2] = 1


    return total/2, counted_edges

def branch_and_bound_tsp(graph: NDArrayFloat) -> NDArrayInt:
    
    graph_initial_bound, counted_edges = graph_bound(graph)

    number_of_nodes: np.int_ = len(graph)
    root: Node = Node(graph_initial_bound, 0, [0], counted_edges, len(graph))
    heap: heapq = [root]
    heapq.heapify(heap)
    best: npt.float_ = float("inf")
    solution: NDArrayInt = np.array([])
    while (len(heap) > 0):
        node = heapq.heappop(heap)
        counted_edges: NDArrayInt = node.counted_edges
        if node.level > number_of_nodes:
            if best > node.cost:
                best = node.cost
                solution = node.path
        elif node.bound < best:
            if node.level < number_of_nodes:
                for k in range(1, number_of_nodes):
                    if not node.oneIsVisited and k == 2:
                        continue
                    if node.path[-1] != k:
                        new_bound, new_counted_edges = bound(node.bound, node.path[-1], k, counted_edges, graph)
                        if not node.visited[k] and new_bound < best:
                            heapq.heappush(heap, Node(new_bound, node.cost + graph[node.path[-1]][k], np.append(node.path, k), new_counted_edges, len(graph))) 
            if node.path[-1] != 0:
                new_bound, new_counted_edges = bound(node.bound, node.path[-1], 0, counted_edges, graph)
                if new_bound < best and node.level == number_of_nodes:
                    heapq.heappush(heap, Node(new_bound, node.cost + graph[node.path[-1]][0], np.append(node.path, 0), new_counted_edges, len(graph)))
                    
    return solution

import utils
def teste():
    """ graph = np.array([   [0, 3, 1, 5, 8], 
                        [3,0, 6, 7, 9], 
                        [1, 6, 0, 4, 2], 
                        [5, 7, 4, 0, 3], 
                        [8, 9, 2, 3, 0]])
 """
    #graph = generate_tsp_instance(3, 5000)[0]
    
    graph = np.asarray([[ 0         , 5.88232947 , 5.42147581  ,3.34819354 ,10.96685917  ,8.25804456, 7.31221581  ,0.72027772, 11.70822361 , 7.9310655  ,25.7208573  , 5.29499764, 5.07079875  ,5.30050941  ,6.6912256   ,1.41209065],
        [ 5.88232947 , 0.       , 1.29189783 , 4.48742688, 16.75590045 ,14.10396044,
        13.09061114 , 6.06684432, 17.13061879 ,13.19734822, 31.55360043 ,11.07476411,
        10.89295185 ,11.17157106 ,12.51380438  ,6.59334513],
        [ 5.42147581 , 1.29189783 , 0    ,     4.83011387, 16.38825189 ,13.46836664,
        12.39611633  ,5.74943475 ,16.23383196 ,12.28515364, 30.85694897 ,10.40212478,
        10.25714385 ,10.59834893 ,12.11217982 ,5.88367232],
        [ 3.34819354 , 4.48742688 , 4.83011387 , 0   ,      12.88350884 ,11.00703866,
        10.2403955  , 2.96141858 ,14.87485462 ,11.20325845 ,28.33057183 , 8.29000603,
        7.99656176 , 8.04767047 , 8.83362327 , 4.72055082],
        [10.96685917 ,16.75590045 ,16.38825189, 12.88350884 , 0 ,         4.40101125,
        5.56852763 ,10.69259557 , 7.8826455 ,  8.08926449 ,15.96316071,  6.77998525,
        6.70410322  ,6.1382245 ,  4.28117974, 10.76730235],
        [ 8.25804456 ,14.10396044 ,13.46836664 ,11.00703866 , 4.40101125 , 0,
        1.25936492 , 8.25009697 , 4.79760357 , 3.71102412 ,17.46282909 , 3.07761271,
        3.21460729 , 2.98041943 , 2.97015151 , 7.58662639],
        [ 7.31221581 ,13.09061114 ,12.39611633, 10.2403955  , 5.56852763 , 1.25936492,
        0       , 7.3850457  , 4.89654981  ,2.75065447, 18.46883862  ,2.02061872,
        2.25621364  ,2.25204352 , 3.17001577 , 6.51813624],
        [ 0.72027772 , 6.06684432  ,5.74943475  ,2.96141858 ,10.69259557 , 8.25009697,
        7.3850457  , 0   ,      11.93145842 , 8.24224484 ,25.69038925 , 5.39431182,
        5.12884002 , 5.27000949 , 6.44789113 , 2.03960781],
        [11.70822361 ,17.13061879, 16.23383196, 14.87485462,  7.8826455,   4.79760357,
        4.89654981 ,11.93145842 , 0     ,     3.95045567, 15.2085042  , 6.63162876,
        6.96770407 , 7.11922046 , 7.75860812 ,10.62584114],
        [ 7.9310655 , 13.19734822 ,12.28515364 ,11.20325845 , 8.08926449,  3.71102412,
        2.75065447  ,8.24224484 , 3.95045567 , 0.     ,    18.95615204 , 3.40828403,
        3.79610327 , 4.2296572  , 5.82024914 , 6.75693718],
        [25.7208573 , 31.55360043, 30.85694897 ,28.33057183 ,15.96316071 ,17.46282909,
        18.46883862 ,25.69038925, 15.2085042 , 18.95615204 , 0      ,  20.47993408,
        20.66394202, 20.43010768 ,19.5389099 ,24.9862222 ],
        [ 5.29499764 ,11.07476411 ,10.40212478 , 8.29000603 , 6.77998525  ,3.07761271,
        2.02061872  ,5.39431182 , 6.63162876 , 3.40828403 ,20.47993408  ,0,
        0.38832976  ,0.96083297 , 3.08812241  ,4.51851746],
        [ 5.07079875 ,10.89295185 ,10.25714385 , 7.99656176  ,6.70410322 , 3.21460729,
        2.25621364  ,5.12884002 , 6.96770407 , 3.79610327 ,20.66394202 , 0.38832976,
        0       ,   0.66483081 , 2.85245508 , 4.38043377],
        [ 5.30050941 ,11.17157106 ,10.59834893 , 8.04767047 , 6.1382245 ,  2.98041943,
        2.25204352 , 5.27000949 , 7.11922046 , 4.2296572 , 20.43010768 , 0.96083297,
        0.66483081  ,0     ,     2.19155196 , 4.76388497],
        [ 6.6912256  ,12.51380438, 12.11217982 , 8.83362327 , 4.28117974 , 2.97015151,
        3.17001577 , 6.44789113 , 7.75860812 , 5.82024914 ,19.5389099 ,  3.08812241,
        2.85245508 , 2.19155196 , 0        ,  6.51417685],
        [ 1.41209065,  6.59334513 , 5.88367232  ,4.72055082 ,10.76730235  ,7.58662639,
        6.51813624 , 2.03960781 ,10.62584114 , 6.75693718, 24.9862222,   4.51851746,
        4.38043377 , 4.76388497 , 6.51417685  ,0       ]])
    

    s = time.time()
    path = branch_and_bound_tsp(graph)
    print([chr(x+65) for x in path])
    e = time.time()
    print(f"time: {e-s}")

teste()