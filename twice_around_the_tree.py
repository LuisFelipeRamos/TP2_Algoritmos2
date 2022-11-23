
import time
import numpy as np
import numpy.typing as npt
import networkx as nx
import igraph as ig
import math
import cProfile

from instance_generator import generate_tsp_instance

NDArrayInt = npt.NDArray[np.int_]
NDArrayFloat = npt.NDArray[np.float_]

instance = np.array([[np.inf, 3, 1, 5, 8], 
                    [3, np.inf, 6, 7, 9], 
                    [1, 6, np.inf, 4, 2], 
                    [5, 7, 4, np.inf, 3], 
                    [8, 9, 2, 3, np.inf]])

#instance = generate_tsp_instance(10, 10)

def twice_around_the_tree(graph: NDArrayInt):

    graph = nx.from_numpy_matrix(graph)
    mst = nx.minimum_spanning_tree(graph)
    hamiltonian_cycle = list(nx.dfs_preorder_nodes(mst, source = 0))
    return hamiltonian_cycle + [0]

