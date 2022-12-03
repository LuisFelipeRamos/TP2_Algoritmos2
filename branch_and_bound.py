from __future__ import annotations

import heapq
import numpy as np
import numpy.typing as npt

NDArrayInt = npt.NDArray[np.int_]
NDArrayFloat = npt.NDArray[np.float_]

# Classe auxiliar que representa cadanó na árvore de buscas
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

# Função auxiliar para calcular a estimativa do cmainho hamiltoniano mínimo do grafo sem contabilizar nenhuma aresta específica.
def graph_bound(graph: NDArrayInt) -> np.float_:
    total: int = 0
    counted_edges: NDArrayInt = np.zeros((len(graph), 3), dtype = np.int_)
    for i in range(len(graph)):
        a, b = np.partition(graph[i], 2)[1:3]
        counted_edges[i, 0] = np.where(graph[i] == a)[0][0]
        second_min_possible_indexes = np.where(graph[i] == b)[0]
        if second_min_possible_indexes[0] != counted_edges[i, 0]:
            counted_edges[i, 1] = second_min_possible_indexes[0] 
        else:
            counted_edges[i, 1] = second_min_possible_indexes[1]
        total += a + b
    return total/2, counted_edges

# Função de estimativa que atualiza a estimativa de custo dos caminhos hamiltonianos no grafo conforme são adicionadas arestas ao caminho.
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
