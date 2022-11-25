import numpy as np
import numpy.typing as npt
import networkx as nx

NDArrayInt = npt.NDArray[np.int_]
NDArrayFloat = npt.NDArray[np.float_]

def twice_around_the_tree(graph: NDArrayInt, src: np.int_ = 0):

    graph_nx = nx.from_numpy_array(graph)
    mst = nx.minimum_spanning_tree(graph_nx)
    hamiltonian_cycle = list(nx.dfs_preorder_nodes(mst, source = src))
    return hamiltonian_cycle + [src]
