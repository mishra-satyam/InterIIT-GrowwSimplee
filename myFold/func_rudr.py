from networkx.algorithms.core import k_truss
from test import tsp
from rudr import *


def find_path_for_all_drivers(drivers, nodes, adjMtrx, nodeWeights, deliveryManWeight, startingPoints, cap):
	# print(adjMtrx)
	# print(startingPoints)

	graph = {}
	for i in range(nodes+1):
		graph[i] = {}

	for i in range(1, nodes+1):
		for j in range(1, nodes+1):
			graph[i][j] = adjMtrx[i][j]

	drivers = min(drivers, nodes)

	# startingPoints = random.sample(range(1, nodes+1), drivers)
	# startingPoints = [54, 81, 86, 79]

	points = []
	for i in range(1, nodes+1):
		if (i in startingPoints):
			continue
		points.append(i)

	# print("Points", points)

	clustersGraphs = [{i: {}} for i in startingPoints]
	clusterWeightSum = [nodeWeights[i] for i in startingPoints]
	clustersNodes = [[i] for i in startingPoints]
	clusterValues = [0 for i in range(drivers)]
	clusterValuesSum = 0

	for i in points:
		mx = infinity
		valueCoorToMx = infinity
		idx = 0
		mxGraph = {}
		for j in range(drivers):
			if clusterWeightSum[j] + nodeWeights[i] > deliveryManWeight or len(clustersNodes[j]) > cap:
				clusterWeightSum[j] += nodeWeights[i]
				continue
			newGraph = copy.deepcopy(clustersGraphs[j])
			newGraph[i] = {}
			for k in clustersNodes[j]:
				newGraph[i][k] = adjMtrx[i][k]
				newGraph[k][i] = adjMtrx[k][i]

			# print(newGraph)
			[value, _] = tsp(newGraph)
			totVal = value - clusterValues[j] + clusterValuesSum
			# if (totVal < mx):
			if (value < valueCoorToMx):
				mx = totVal
				valueCoorToMx = value
				idx = j
				mxGraph = newGraph

		# please add nodes in cluster nodes
		# please update the value
		# update cluster sum as well
		if (mx == infinity):
			continue
		clusterValuesSum += (valueCoorToMx - clusterValues[idx])
		clusterValues[idx] = valueCoorToMx
		clustersNodes[idx].append(i)
		clustersGraphs[idx] = mxGraph
		clusterWeightSum[idx] += nodeWeights[i]
		# print("And the node i goes to :", clustersNodes[idx][0])

	# driver id, path
	ans = {}
	for i in range(drivers):
		tmp = tsp(clustersGraphs[i])
		path = tmp[1]
		ans[i] = path
	# print("my length", len(ans))
	return ans, clusterWeightSum, clusterValuesSum


glob_cluster_assigned_to_driver = {}
glob_driver_completed = []
glob_driver_path = []
glob_all_cluster_cost = 0

# TODO - Make this better


def compare_clusters(next_cluster, curr_cluster, node_travel_time):
    time_for_farthest_nodes = 100000
    for node1 in next_cluster:
        for node2 in curr_cluster:
            time_for_farthest_nodes = min(
            	time_for_farthest_nodes, node_travel_time[node2][node1])

    return time_for_farthest_nodes


def find_path(clusters, prev_cluster, nodes, cap, node_travel_time, node_weights, delivery_man_weight, switch, driver_idx):

    global glob_driver_path
    global glob_driver_completed
    global glob_cluster_assigned_to_driver
    global glob_all_cluster_cost

    # pdb.set_trace()

    assert(glob_driver_completed[driver_idx] == 0)

    if switch:
        glob_cluster_assigned_to_driver[driver_idx] = prev_cluster
        return []

    closest_cluster = []
    closest_cluster_distance = infinity
    cluster_idx = -1
    idx = -1
    all_empty = 0

    if len(prev_cluster) == 0:
        while len(closest_cluster) == 0:
            closest_cluster = copy.deepcopy(random.sample(clusters, 1)[0])
            cluster_idx = clusters.index(closest_cluster)
    else:
        for cluster in clusters:
            idx += 1
            if cluster == []:
                all_empty += 1
                continue
            cluster_max_distance = compare_clusters(
            	cluster, prev_cluster, node_travel_time)
            if cluster_max_distance < closest_cluster_distance:
                closest_cluster = copy.deepcopy(cluster)
                closest_cluster_distance = cluster_max_distance
                cluster_idx = idx

    # print("Closest cluster", closest_cluster)

    if all_empty == len(clusters):
        return []

    starting_point = random.choice(closest_cluster)
    closest_point_distance = infinity
    for j in prev_cluster:
        for i in closest_cluster:
            if node_travel_time[j][i] < closest_point_distance:
                closest_point_distance = node_travel_time[j][i]
                starting_point = i

    # pdb.set_trace()

    # print(prev_cluster, closest_cluster)
    cluster_node_travel_time = [
    	[infinity for i in range(nodes+1)] for j in range(nodes+1)]
    for i in closest_cluster:
        for j in closest_cluster:
            cluster_node_travel_time[i][j] = node_travel_time[i][j]

    path_list, weight_list, cluster_cost = find_path_for_all_drivers(
    	1, nodes, cluster_node_travel_time, node_weights, delivery_man_weight, [starting_point], cap)
    path_len_covered = len(path_list[0]) - 1
    weight_covered = weight_list[0]

    glob_all_cluster_cost += cluster_cost

    for i in path_list[0][:-1]:
        clusters[cluster_idx].remove(i)

    path = []
    if path_len_covered >= cap or weight_covered >= delivery_man_weight:
        path = path_list[0][:-1]
        glob_driver_completed[driver_idx] = 1
    else:
        # print("Closest -", closest_cluster)
        path = path_list[0][:-1] + find_path(clusters, closest_cluster, nodes, cap - path_len_covered,
                                             node_travel_time, node_weights, delivery_man_weight - weight_covered, switch+1, driver_idx)

    return path


def find_travel_clusters(drivers, nodes, node_travel_time, clusters, node_weights, delivery_man_weight):

    global glob_driver_path
    global glob_driver_completed
    global glob_cluster_assigned_to_driver
    global glob_all_cluster_cost

    driver_idx, cluster_idx = 0, 0

    is_cluster_visited = [0 for i in range(len(clusters))]
    driver_clusters = {}
    # print("Drivers", drivers)

    driver_cap = [20 for i in range(drivers)]
    glob_driver_completed = [0 for i in range(drivers)]
    glob_driver_path = [[] for i in range(drivers)]
    glob_all_cluster_cost = 0
    for i in range(drivers):
        glob_cluster_assigned_to_driver[i] = []

    while True:
        all_completed = 0
        # print("Glob_driver_path for ", driver_idx, glob_driver_path)
        while driver_idx < drivers:

            if glob_driver_completed[driver_idx]:
                driver_clusters[driver_idx] = glob_driver_path[driver_idx]
                all_completed += 1
                driver_idx += 1
                continue
            # print("clusters", clusters)
            # print("nodes", nodes)
            # print("tot_cap", tot_cap)
            driver_next_path = find_path(clusters, glob_cluster_assigned_to_driver[driver_idx], nodes, driver_cap[
                                         driver_idx], node_travel_time, node_weights, delivery_man_weight, 0, driver_idx)
            glob_driver_path[driver_idx] += driver_next_path
            driver_cap[driver_idx] -= len(driver_next_path)
            # driver_clusters[driver_idx] = curr_driver_cluster

            driver_idx += 1

        driver_idx = 0
        if all_completed == drivers:
            break

    return driver_clusters, glob_all_cluster_cost
