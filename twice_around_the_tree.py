
import time
import numpy as np
import numpy.typing as npt
import networkx as nx
import igraph as ig
import math
import cProfile
import matplotlib.pyplot as plt

from instance_generator import generate_tsp_instance

NDArrayInt = npt.NDArray[np.int_]
NDArrayFloat = npt.NDArray[np.float_]

instance = np.array([[np.inf, 3, 1, 5, 8], 
                    [3, np.inf, 6, 7, 9], 
                    [1, 6, np.inf, 4, 2], 
                    [5, 7, 4, np.inf, 3], 
                    [8, 9, 2, 3, np.inf]])

instance = generate_tsp_instance(9, 10)

def twice_around_the_tree(graph: NDArrayInt):

    graph = nx.from_numpy_matrix(graph)
    mst = nx.minimum_spanning_tree(graph)
    hamiltonian_cycle = list(nx.dfs_preorder_nodes(mst, source = 0))
    return hamiltonian_cycle + [0]

def twice_around_the_tree_ig(graph: NDArrayInt):

    graph = ig.Graph.Adjacency(graph, mode = "undirected")
    mst = ig.Graph.spanning_tree(graph, return_tree = True)
    hamiltonian_cycle = mst.dfs(vid = 0)
    return hamiltonian_cycle[0] + [0]

s = time.time()
path = twice_around_the_tree_ig(instance)
e = time.time()

print(f"Time: {e-s}")


time.sleep(1)

s = time.time()
path = twice_around_the_tree_ig(instance)
e = time.time()


""" print([chr(x+65) for x in path]) """
print(f"Time: {e-s}")