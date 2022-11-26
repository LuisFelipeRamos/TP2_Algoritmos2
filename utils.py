import numpy as np
import numpy.typing as npt
import networkx as nx

NDArrayInt = npt.NDArray[np.int_]
NDArrayFloat = npt.NDArray[np.float_]

def get_path_cost(path: NDArrayInt, graph: NDArrayFloat) -> np.float_:
    cost: np.float_ = 0
    for i in range(len(path) - 1):
        cost += graph[path[i], path[i + 1]]
    return cost
