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
    counted_edges: NDArrayInt = np.zeros((len(graph), 2), dtype = np.int_)
    for i in range(len(graph)):
        a, b = np.partition(graph[i], 1)[0:2]
        counted_edges[i, 0] = np.where(graph[i] == a)[0][0]
        counted_edges[i, 1] = np.where(graph[i] == b)[0][0]
        total += a + b
    return total/2, counted_edges

def bound_old(prev_bound: np.float_, prev_node: np.int_, new_node: np.int_, graph: NDArrayFloat) -> np.float_:

    total: np.float_ = prev_bound * 2
    total += graph[prev_node, new_node] * 2

    a, b = np.partition(graph[prev_node], 1)[0:2]
    if graph[prev_node, new_node] == a:
        total -= a
    else:
        total -= b
    
    a, b = np.partition(graph[new_node], 1)[0:2]
    if graph[prev_node, new_node] == a:
        total -= a
    else:
        total -= b
    return total/2

# devo conseguir fzr isso em tempo constante
def bound(prev_bound: np.float_, prev_node: np.int_, new_node: np.int_, counted_edges: NDArrayInt, graph: NDArrayFloat) -> np.float_:

    total: np.float_ = prev_bound * 2
    new_edge_value: np.float_ = graph[prev_node, new_node]
    total += new_edge_value * 2

    if counted_edges[prev_node, 0] == new_node or counted_edges[prev_node, 1] == new_node:
        total -= new_edge_value * 2
    else:
        if prev_node == 0:
            total -= graph[prev_node, counted_edges[prev_node, 1]]
            total -= graph[new_node, counted_edges[new_node, 1]]
            counted_edges[prev_node, 1] = new_node
            counted_edges[new_node, 1] = prev_node
        elif new_node == 0:
            total -= graph[prev_node, counted_edges[prev_node, 0]]
            total -= graph[new_node, counted_edges[new_node, 0]]
            counted_edges[prev_node, 0] = new_node
            counted_edges[new_node, 0] = prev_node
        else:
            total -= graph[prev_node, counted_edges[prev_node, 0]]
            total -= graph[new_node, counted_edges[new_node, 1]]
            counted_edges[prev_node, 0] = new_node
            counted_edges[new_node, 1] = prev_node

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
        print([chr(x+65) for x in node.path])
        print(node.bound)
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


def teste():
    instance = np.array([   [np.inf, 3, 1, 5, 8], 
                            [3, np.inf, 6, 7, 9], 
                            [1, 6, np.inf, 4, 2], 
                            [5, 7, 4, np.inf, 3], 
                            [8, 9, 2, 3, np.inf]])

    #instance = generate_tsp_instance(3, 10)

    path = branch_and_bound_tsp(instance)
    print([chr(x+65) for x in path])
    return path
#cProfile.run("teste()")


