import numpy as np
from numpy.typing import npt
from numba import njit
import scipy.sparse.csgraph
import heapq

NDArrayInt = npt.NDArray[np.int_]

@njit(cache = True)
def branch_and_bound_tsp(graph: NDArrayInt) -> NDArrayInt:
    heap = []
    pass