from test import tsp
import random
# import numpy as np
import numpy 
import copy

# drivers (same)
# locations (new) ==> remaining nodes, order same --> { rider : array_locations }
# nodeWeights ==> (same) original node weights --> { node_id : weight }
# adjMztirxtime, distance ==> same --> {1 based }
# nodes ==> (same) (int)
# newNode ==> [null, null, nodeWeight] ==> []
"""
	distance ==> { node_id : float }
	1 3 5
	{ 1 : _, 3 : }
"""
# times ==> { node_id : float }
# points ==> []

# return 
# locations, cost, adjMatrixTime, adjMatri, nodeWeights, nodes

def pickup(drivers, locations, nodeWeights, adjMtrxDist, adjMtrxTimes, nodes, newNode, distances, times, points):
	
	deliveryManWeight = 100
	graph = {}
	for i in range(nodes+1):
		graph[i] = {}

	for i in range(1, nodes+1):
		for j in range(1, nodes+1):
			graph[i][j] = adjMtrxDist[i][j]

	nodes += 1
	
	allLocations = set()
	allLocations.add(nodes)
	for i in locations:
		for j in locations[i]:
			allLocations.add(j)

	distances1 = []

	for i in range(1, nodes + 1):
		if(i == nodes):
			distances1.append(0)
			continue
		if(i in allLocations):
			distances1.append(distances[i])
		else:
			distances1.append(10 ** 10)

	adjMtrxDist.append(list(distances1))


	for i in range(1, nodes + 1):
		if(i == nodes):
			adjMtrxDist[i].append(0)
			continue
		if i in allLocations:
			adjMtrxDist[i].append(distances[i])
		else:
			adjMtrxDist[i].append(10 ** 10)


	# adjMtrxDist.append([])
	# adjMtrxDist.append(list(distances.values()))
	# np.concatenate(adjMtrxDist, list(distances.values()))
	# distances1 = [10**10 for i in range(nodes + 1)]
	# for i in distances.keys():
	#     distances1[i] = distances[i]
	
	
	print("sixe of matrix++++", len(adjMtrxDist))
	# we have to append the distance1 array at mthe end of adjmtrxdist  dont know in numpy 
	# adjMtrxDist =  numpy.append(adjMtrxDist, numpy.array(list(distances1)))
	# adjMtrxDist.append(list(distances1))
	print("sixe of matrix++++", len(adjMtrxDist))

	# nodes += 1
	# points.append([nodes-1, newNode[0], newNode[1], newNode[2]])



	# for i in range(1, nodes+1):
	# 	# print(type(adjMtrxDist[i]))
	# 	adjMtrxDist[i].append(times[i])

	# allLocations = set()
	# allLocations.add(nodes)
	# for i in locations:
	#     for j in locations[i]:
	#         allLocations.add(j)
	# # print("len of distances ", len)
	# # print("shape ", adjMtrxDist.shape());
	# print("matrix ", adjMtrxDist);
	# for i in locations:
	#     for j in locations[i]:
	#         if j in allLocations:
	#             # adjMtrxDist[j] =  numpy.append(adjMtrxDist[j], distances1[j])
	#             adjMtrxDist[j].append(distances1[j])
	#         else:
	#             adjMtrxDist[j].append(10**10)
	#             # adjMtrxDist[j] =  numpy.append(adjMtrxDist[j], 10**10)

	print("sixe of matrix++++", len(adjMtrxDist[0]))
	print("sixe of matrix++++", len(adjMtrxDist))
	for i in range(1, nodes+1):
		for j in range(1, nodes+1):
			if i == j :
				adjMtrxDist[i][i] = 0
			if i not in allLocations:
				adjMtrxDist[i][j] = float('inf')
				adjMtrxDist[j][i] = float('inf')
			if j not in allLocations:
				adjMtrxDist[i][j] = float('inf')
				adjMtrxDist[j][i] = float('inf')

	# for i in range(1, nodes):
	# 	if i in allLocations:
	# 		adjMtrxDist[i].append()

	# nodes1 = nodes + 1
	points1 = [nodes]
	nodeWeights[nodes] = newNode[2]
	clustersGraphs = []
	clusterWeightSum = [0 for i in range(drivers)]
	clustersNodes = []
	clusterValues = [0 for i in range(drivers)]
	clusterValuesSum = 0

	for i in locations:
		newGraph = {}
		for j in locations[i]:
			newGraph[j] = {}
		for j in locations[i]:
			for k in locations[i]:
				if(j > k):
					continue
				newGraph[j][k] = adjMtrxDist[j][k]
				newGraph[k][j] = adjMtrxDist[k][j]


		clustersGraphs.append(newGraph)

	for i in range(len(clustersGraphs)):
		clusterValues[i], _ = tsp(clustersGraphs[i])

	for i in locations:
		clustersNodes.append(locations[i])
		for j in locations[i]:
			clusterWeightSum[i] += nodeWeights[j]

	for i in points1:
		mx = float('inf')
		mxValue = float('inf')
		valueCoorToMx = 0
		idx = 0
		mxGraph = {}
		for l in range(100):
			for j in range(drivers):
				if len(clustersNodes[j]) > 25 : continue
				newGraph = copy.deepcopy(clustersGraphs[j])
				newGraph[i] = {}
				for n in clustersNodes[j]:
					newGraph[i][n] = adjMtrxDist[i][n]
					newGraph[n][i] = adjMtrxDist[n][i]
				
				[value, _] = tsp(newGraph)
				totVal = value - clusterValues[j] + clusterValuesSum
				# if (totVal < mx):
				# print(value, j)
				if (value < mxValue):
					mx = totVal
					mxValue = value
					valueCoorToMx = value
					idx = j
					mxGraph = newGraph

		
			
		# please add nodes in cluster nodes
		# please update the value 
		# update cluster sum as well
		if (mx == float('inf')): continue
		# print("added ", i , "to cluster : ", idx)
		# print()
		clusterValuesSum += (valueCoorToMx - clusterValues[idx])
		clusterValues[idx] = valueCoorToMx
		clustersNodes[idx].append(i)
		clustersGraphs[idx] = mxGraph
		clusterWeightSum[idx] += nodeWeights[i]
		# print("And the node i goes to :", clustersNodes[idx][0])

	totalCost = 0
	for i in range(drivers):
		x, _ = tsp(clustersGraphs[i])
		totalCost += x

	# totalCost = 0
	# for i in range(drivers):
	# 	x, _ = tsp(clustersGraphs[i])
	# 	totalCost += x
	ans = {}
	for i in range(drivers):
		tmp = tsp(clustersGraphs[i])
		path = tmp[1]
		ans[i] = path

	# print(clustersNodes[0])
	print("Total Cost == ", totalCost)
	# print(ans)
	# print(points)

	return ans,totalCost, adjMtrxDist, adjMtrxTimes, nodeWeights, nodes, points