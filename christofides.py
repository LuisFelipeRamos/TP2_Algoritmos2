
import numpy as np
import numpy.typing as npt
import networkx as nx

NDArrayInt = npt.NDArray[np.int_]
NDArrayFloat = npt.NDArray[np.float_]

def christofides(graph: NDArrayInt, src: np.int_ = 0):
    graph_nx = nx.from_numpy_matrix(graph)
    mst = nx.minimum_spanning_tree(graph_nx)
    odd_degre_nodes: NDArrayInt = [] 
    for node in mst.nodes:
        if mst.degree[node] % 2 == 1:
            odd_degre_nodes.append(node)
    induced_subgraph = graph_nx.subgraph(odd_degre_nodes)
    min_weight_perfect_matching = nx.min_weight_matching(induced_subgraph, maxcardinality = True)

    #multigrafo criado de duas formas, checar qual melhor
    eulerian_multigraph = nx.MultiGraph(mst)
    
    #eulerian_multigraph = nxMultiGraph()
    #eulerian_multigraph.add_edges_from(mst.edges)
    
    eulerian_multigraph.add_edges_from(min_weight_perfect_matching)

    eulerian_circuit = list(nx.eulerian_circuit(eulerian_multigraph))
    hamiltonian_cycle = []
    for u, _ in eulerian_circuit:
        if u in hamiltonian_cycle:
            continue
        hamiltonian_cycle.append(u)

    return hamiltonian_cycle + [src]
