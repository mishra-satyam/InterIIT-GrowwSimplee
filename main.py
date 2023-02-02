from test import tsp
import random
import copy

def solve(drivers, nodes, adjMtrx, nodeWeights, deliveryManWeight):
	graph = {}
	for i in range(nodes+1):
		graph[i] = {}
	
	for i in range(1, nodes+1):
		for j in range(1, nodes+1):
			graph[i][j] = adjMtrx[i][j]
			
	
	drivers = min(drivers, nodes)
	
	startingPoints = random.sample(range(1, nodes+1), drivers)
	# startingPoints = [54, 81, 86, 79]
	
	
	points = []
	for i in range(1, nodes+1):
		if (i in startingPoints):
			continue
		points.append(i)
	
	clustersGraphs = [{i: {}} for i in startingPoints]
	clusterWeightSum = [nodeWeights[i] for i in startingPoints]
	clustersNodes = [[i] for i in startingPoints]
	clusterValues = [0 for i in range(drivers)]
	clusterValuesSum = 0
	
	for i in points:
		mx = float('inf')
		valueCoorToMx = 0
		idx = 0
		mxGraph = {}
		for j in range(drivers):
			if (clusterWeightSum[j] + nodeWeights[i] > deliveryManWeight): continue
			newGraph = copy.deepcopy(clustersGraphs[j])
			newGraph[i] = {}
			for n in clustersNodes[j]:
				newGraph[i][n] = adjMtrx[i][n]
				newGraph[n][i] = adjMtrx[n][i]
			
			[value, _] = tsp(newGraph)
			totVal = value - clusterValues[j] + clusterValuesSum
			if (totVal < mx):
			# if (value > clusterValues[j]):
				mx = totVal
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
		print("And the node i goes to :", clustersNodes[idx][0])
	
	# driver id, path
	ans = {}
	for i in range(drivers):
		tmp = tsp(clustersGraphs[i])
		path = tmp[1]
		ans[i] = path
	print("my length", len(ans))
	return ans