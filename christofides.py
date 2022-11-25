
import numpy as np
import numpy.typing as npt
import networkx as nx

NDArrayInt = npt.NDArray[np.int_]
NDArrayFloat = npt.NDArray[np.float_]

from instance_generator import generate_tsp_instance

NDArrayInt = npt.NDArray[np.int_]
NDArrayFloat = npt.NDArray[np.float_]

graph = np.array([[np.inf, 3, 1, 5, 8], 
                    [3, np.inf, 6, 7, 9], 
                    [1, 6, np.inf, 4, 2], 
                    [5, 7, 4, np.inf, 3], 
                    [8, 9, 2, 3, np.inf]])

#instance = generate_tsp_instance(10, 10)
import matplotlib.pyplot as plt
def christofides(graph: NDArrayInt, src: np.int_ = 0):
    graph = nx.from_numpy_matrix(graph)
    mst = nx.minimum_spanning_tree(graph)
    odd_degre_nodes: NDArrayInt = [] 
    for node in mst.nodes:
        if mst.degree[node] % 2 == 1:
            odd_degre_nodes.append(node)
    induced_subgraph = mst.subgraph(odd_degre_nodes)
    #calcular edmond blossom do grafo induzido
    #dfs
    #dale
    
christofides(graph)