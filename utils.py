import numpy as np
import numpy.typing as npt

NDArrayInt = npt.NDArray[np.int_]
NDArrayFloat = npt.NDArray[np.float_]

# Função auxiliar utilizada para calcular o custo de um determinado caminho em um determinado grafo.
def get_path_cost(path: NDArrayInt, graph: NDArrayFloat) -> np.float_:
    cost: np.float_ = 0
    for i in range(len(path) - 1):
        cost += graph[path[i], path[i + 1]]
    return cost
