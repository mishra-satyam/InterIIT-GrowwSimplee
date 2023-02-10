from rudr import *

# Compute Markov Clusters


def markov_clusters(node_travel_distance, positions, draw=False):
    print("Called Markov algorithm")
    network = nx.from_numpy_array(np.matrix(node_travel_distance))
    print(node_travel_distance)
    print(network)

    # then get the adjacency matrix (in sparse form)
    matrix = nx.to_scipy_sparse_array(network)
    min_modularity_cluster_set = []
    min_modularity = -1

    # perform clustering using different inflation values from 1.5 and 2.5
    # for each clustering run, calculate the modularity
    for inflation in [i / 10 for i in range(11, 12)]:
        result = mc.run_mcl(matrix, inflation=inflation)
        clusters = mc.get_clusters(result)
        Q = mc.modularity(matrix=result, clusters=clusters)
        if Q > min_modularity:
            min_modularity_cluster_set = clusters
            min_modularity = Q

    print(min_modularity_cluster_set)
    if draw:
        print(min_modularity_cluster_set)
        mc.draw_graph(matrix, min_modularity_cluster_set, pos=positions,
                      node_size=50, with_labels=False, edge_color="grey")

    return min_modularity_cluster_set
