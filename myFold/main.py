from test import tsp
import random
import copy

# drivers - number of drivers
# nodes   - number of locations
# times   - 1 index
# distance - 1 index 
# mx = float('inf') for 0th row and column
# nodeweights - item weight/volume
# deliveryManWeight - Bag weight
# n - number of drivers
# Final Total Cost :  8987.897068021997 h = 1.53
# Final Total Cost :  12012.661532082   h = 1.6


def solve(drivers, nodes, adjMtrxDist, adjMtrxTimes, nodeWeights, deliveryManWeight, n, p, maxNodesInCluster):
	graph = {}
	for i in range(nodes+1):
		graph[i] = {}
	
	mexVal = -1
	for i in range(1, nodes+1):
		for j in range(1, nodes+1):
			graph[i][j] = adjMtrxDist[i][j]
			mexVal = max(mexVal, adjMtrxDist[i][j])
			
	
	drivers = min(drivers, nodes)
	
	# if n == 5:
	startingPoints = random.sample(range(2, nodes+1), drivers)
	# startingPoints = [54, 81, 86, 79]
	
	
	points = []
	for i in range(2, nodes+1):
		if (i in startingPoints):
			continue
		points.append(i)

	if n == 0:
		random.shuffle(points)
		

	clustersGraphs = [{i: {}} for i in startingPoints]
	clusterWeightSum = [nodeWeights[i] for i in startingPoints]
	clustersNodes = [[i] for i in startingPoints]
	clusterValues = [0 for i in range(drivers)]
	clusterValuesSum = 0
	newPoints = []
<<<<<<< HEAD
	h =  (mexVal ** (1.53) / nodes)
	# print("H value is : ", h)
=======
	h =  2*mexVal*p
	print("H value is : ", h, p)
>>>>>>> 0d53c1843aaa581147461dac046aecb8d0179cb5
	
	for i in points:
		mx = float('inf')
		mxValue = float('inf')
		valueCoorToMx = 0
		idx = 0
		mxGraph = {}
		for l in range(max(1, 200//nodes)):
			for j in range(drivers):
				if (clusterWeightSum[j] + nodeWeights[i] > deliveryManWeight or len(clustersNodes[j]) > maxNodesInCluster): continue
				newGraph = copy.deepcopy(clustersGraphs[j])
				newGraph[i] = {}
				for n in clustersNodes[j]:
					newGraph[i][n] = adjMtrxDist[i][n]
					newGraph[n][i] = adjMtrxDist[n][i]
				
				[value, _] = tsp(newGraph)
				totVal = value - clusterValues[j] + clusterValuesSum
				# if (totVal < mx):
				if (value < mxValue):
					mx = totVal
					mxValue = value
					valueCoorToMx = value
					idx = j
					mxGraph = newGraph
				
		# please add nodes in cluster nodes
		# please update the value 
		# update cluster sum as well
		if (mxValue - clusterValues[idx] > h) :
			newPoints.append(i)
			continue
		if (mx == float('inf')): continue
		clusterValuesSum += (valueCoorToMx - clusterValues[idx])
		clusterValues[idx] = valueCoorToMx
		clustersNodes[idx].append(i)
		clustersGraphs[idx] = mxGraph
		clusterWeightSum[idx] += nodeWeights[i]
		# print("And the node i goes to :", clustersNodes[idx][0])

	# print(len(newPoints))

	nodesDone = 0 
	for i in clustersNodes:
		nodesDone += len(i)

	print("nodesDone = ", nodesDone)

	for i in newPoints:
		mx = float('inf')
		mxValue = float('inf')
		valueCoorToMx = 0
		idx = 0
		mxGraph = {}
		for l in range(max(1, 200//nodes)):
			for j in range(drivers):
				if (clusterWeightSum[j] + nodeWeights[i] > deliveryManWeight or len(clustersNodes[j]) > maxNodesInCluster): continue
				newGraph = copy.deepcopy(clustersGraphs[j])
				newGraph[i] = {}
				for n in clustersNodes[j]:
					newGraph[i][n] = adjMtrxDist[i][n]
					newGraph[n][i] = adjMtrxDist[n][i]
				
				[value, _] = tsp(newGraph)
				totVal = value - clusterValues[j] + clusterValuesSum
				# if (totVal < mx):
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

	# print("Total Cost == ", totalCost)
	# driver id, path
	ans = {}
	for i in range(drivers):
		tmp = tsp(clustersGraphs[i])
		path = tmp[1]
		menCost = tmp[0]
		for k in range(5):
			tmp = tsp(clustersGraphs[i])
			if(tmp[0] < menCost):
				path = tmp[1]
				menCost = tmp[0]
			# path = tmp[1]
		ans[i] = path
		# print("path before", path)
		assert(len(path) > 1)
		if (len(path) == 2): 
			assert(path[0] == path[1])
			ans[i] = [1] + path[0] + [1]
			# print("path after", path)
			continue
		
		mnDistDiff = float('inf')
		mnIdx = -1
		for j in range(len(path)-1):
			distDiff = -adjMtrxDist[path[j]][path[j+1]] + adjMtrxDist[path[j]][1] + adjMtrxDist[1][path[j+1]]
			if (distDiff < mnDistDiff):
				mnDistDiff = distDiff
				mnIdx = j
		assert(idx != -1)
		path = [1] + path[mnIdx+1:] + path[1:mnIdx+1] + [1]
		# print("path after", path)
		ans[i] = path
	# print("my length", len(ans))

	return ans, totalCost, nodesDone