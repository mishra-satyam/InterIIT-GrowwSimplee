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

def solve(drivers, nodes, adjMtrxDist, adjMtrxTimes, nodeWeights, deliveryManWeight, n):
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
	startingPoints = random.sample(range(1, nodes+1), drivers)
	# startingPoints = [54, 81, 86, 79]
	
	
	points = []
	for i in range(1, nodes+1):
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
	h =  (mexVal ** (1.5) / nodes)
	print("H value is : ", h)
	
	for i in points:
		mx = float('inf')
		mxValue = float('inf')
		valueCoorToMx = 0
		idx = 0
		mxGraph = {}
		for l in range(5):
			for j in range(drivers):
				if (clusterWeightSum[j] + nodeWeights[i] > deliveryManWeight or len(clustersNodes[j]) > 20): continue
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

	print(nodesDone)

	for i in newPoints:
		mx = float('inf')
		mxValue = float('inf')
		valueCoorToMx = 0
		idx = 0
		mxGraph = {}
		for l in range(5):
			for j in range(drivers):
				if (clusterWeightSum[j] + nodeWeights[i] > deliveryManWeight or len(clustersNodes[j]) > 20): continue
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
	# print("my length", len(ans))

	return ans, totalCost