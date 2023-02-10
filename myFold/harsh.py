# import markov_clustering as mc
from matplotlib import pyplot as plt
import numpy as np
# import networkx as nx
from matplotlib import pyplot as plt
from main import solve
from pickup import pickup
import copy
from func_rudr import *
from markov_rudr import *
from rudr import *


f = open("2000_30.in", "r")

n = int(f.readline())
m = int(f.readline())

print("solving part done")
# let hub be location 1
adjMtrxDist = [[0 for i in range(m+1)] for j in range(m+1)]
node_travel_time = [[0 for i in range(m+1)] for j in range(m+1)]
node_travel_distance = [[0 for i in range(m+1)] for j in range(m+1)]
# print(len(adjMtrxDist))

def distance(x1, y1, x2, y2):
	return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

points = []

deliveryManWeight = 100
nodeWeights = {}
for i in range(m):
	arr = list(map(float,f.readline().split()))
	arr.append(1)
	arr[3] = 1
	points.append(arr)
	nodeWeights[arr[0]] = arr[-1]

pos = dict()
pos[0] = (0,0)
for i in range(m):
	pos[points[i][0]] = (points[i][1], points[i][2])
	for j in range(i+1, m):
		adjMtrxDist[int(points[i][0])][int(points[j][0])] =  distance(points[i][1], points[i][2], points[j][1], points[j][2])
		adjMtrxDist[int(points[j][0])][int(points[i][0])] =  distance(points[i][1], points[i][2], points[j][1], points[j][2])

print(points[0])

for i in range(m):
    for j in range(i+1, m):
        node_travel_time[int(points[i][0])][int(points[j][0])] = distance(
            points[i][1], points[i][2], points[j][1], points[j][2])
        node_travel_time[int(points[j][0])][int(points[i][0])] = distance(
            points[i][1], points[i][2], points[j][1], points[j][2])

# for i in range(m):
#     for j in range(i+1, m):
#         node_travel_distance[int(points[i][0])][int(
#             points[j][0])] = 1 / distance(points[i][1], points[i][2], points[j][1], points[j][2])
#         node_travel_distance[int(points[j][0])][int(
#             points[i][0])] = 1 / distance(points[i][1], points[i][2], points[j][1], points[j][2])



# network = nx.from_numpy_array(np.matrix(adjMtrxDist))

# then get the adjacency matrix (in sparse form)
# matrix = nx.to_scipy_sparse_array(network)

# result = mc.run_mcl(matrix,inflation=10)
# result = mc.run_mcl(matrix)           # run MCL with default parameters
# clusters = mc.get_clusters(result)    # get clusters

# print(len(clusters))
# print(clusters)

# mc.draw_graph(matrix, clusters, pos=pos, node_size=50, with_labels=False, edge_color="grey")


fig, ax = plt.subplots(figsize = (10,10))
fig.suptitle("Points")

# n - number of drivers
# m - number of locations
# adjMtrxDist - (m + 1)* ( m +1 ) matrix - distance matrix 10000
# location 1 is the hub

"""
	0      1     2 3 4
0   INF  INF   INF
1   INF  INF   30 70
2   INF  30
3   INF  65
4

"""

# return a map -> (location, drivers)
# map of driver to path

def find_path_cost(path):
    if len(path) == 0:
        return 0
    temp_path = copy.deepcopy(path)
    temp_path += [temp_path[0]]
    path_sum = 0
    for i in range(len(temp_path)-1):
        path_sum += node_travel_time[temp_path[i]][temp_path[i+1]]
    return path_sum


def find_loc(n, m, node_travel_distance, node_travel_time, node_weights, deliveryManWeight, positions):
	clusters = markov_clusters(node_travel_distance, positions, False)


	print(clusters)

	# starting_points = random.sample(range(1, m+1), n)
	# locations, _ = find_path_for_all_drivers(n, m, node_travel_time, node_weights, deliveryManWeight, starting_points, 20)
	clusters = clusters[1:]
	for i in range(len(clusters)):
		clusters[i] = list(clusters[i])


	best_cost = infinity
	best_locations = {}
	for i in range(1):
		print("Current iteration -", i)
		locations, cost = find_travel_clusters(n, m, node_travel_time, copy.deepcopy(
			clusters), node_weights, deliveryManWeight)

		all_path_sum = 0
		for loc in locations.values():
			all_path_sum += find_path_cost(loc)

		cost = max(cost, all_path_sum)

		if cost < best_cost:
			best_locations = locations
			best_cost = cost
	for d in best_locations:
		idx = -1
		if (1 in best_locations[d]):
			idx = best_locations[d].index(1)
			best_locations[d] = best_locations[d][idx:] + best_locations[d][:idx] + [1]
		else :
			mnVal = float('inf')
			mnIdx = -1
			for i in range(len(best_locations[d])-1):
				x = best_locations[d][i]
				y = best_locations[d][i+1]
				val = -1 * node_travel_distance[x][y] + node_travel_distance[x][1] + node_travel_distance[1][y]
				if (val< mnVal):
					mnVal = val
					mnIdx = i
			assert(mnIdx != -1)
			best_locations[d] = [1] + best_locations[d][mnIdx+1:] + best_locations[d][:mnIdx+1] + [1]

	# print("B", best_locations)
	return best_locations, best_cost

for i in range(1, len(adjMtrxDist)):
	for j in range(1, len(adjMtrxDist[i])):
		if adjMtrxDist[i][j] != 0:
			node_travel_distance[i][j] = 1 / adjMtrxDist[i][j]

print("N", node_travel_distance)
# for i in range(m):
#     for j in range(i+1, m):
#         node_travel_distance[int(points[i][0])][int(
#             points[j][0])] = 1 / adjMtrxDist[int(points[i][0])][int(points[j][0])]
#         node_travel_distance[int(points[j][0])][int(
#             points[i][0])] = 1 / adjMtrxDist[int(points[j][0])][int(points[i][0])]

r_locations, r_cost = find_loc(
	n, m, node_travel_distance, node_travel_time, nodeWeights, deliveryManWeight, pos)

# maxNodesInCluster = 20
# p = 1

# low = 0
# high = 1
# while (high - low >= 0.001):
# 	mid = (low + high)/2
# 	men = float('inf')
# 	for i in range(1):
# 		print('calling solve')
# 		temp, temp1, doneNodes = solve(n, m, adjMtrxDist, {}, nodeWeights, deliveryManWeight, i%10, mid, int(1.75*maxNodesInCluster-1))
# 		print(temp1)
# 		if(temp1 < men):
# 			totalCost = temp1
# 			men = temp1
# 			locations = temp

# 	mxPossibleIncludedNodes = min(n * int(1.75*maxNodesInCluster), m)
# 	print(mxPossibleIncludedNodes, doneNodes, int(1.75*(maxNodesInCluster-1)))
# 	assert(mxPossibleIncludedNodes >= doneNodes)
# 	if (mxPossibleIncludedNodes > doneNodes):
# 		low = mid
# 	else:
# 		high = mid


# p = mid
# men = float('inf')
# for i in range(10):
# 	temp, temp1, doneNodes = solve(n, m, adjMtrxDist, {}, nodeWeights, deliveryManWeight, i%10, p, maxNodesInCluster-1)
# 	print(temp1)
# 	if(temp1 < men):
# 		totalCost = temp1
# 		men = temp1
# 		locations = temp

if (r_cost < infinity):
	totalCost = r_cost
	locations = r_locations

print("Final Total Cost : ", totalCost)

print("locations", locations)
print("loc lengths")
for x in locations:
	print(len(locations[x]))
print("loc lengths ends")


# for i in locations:
# 	locations[i] = locations[i][5:]
# print(locations)

newPoint = [1100, 1100, 1]
# points.append([])
distances = {}
for i in points:
	distances[i[0]] = distance(i[1], i[2], newPoint[0], newPoint[1])

distances[m+1] = 0

# -----------------

oriLocations = copy.deepcopy(locations)
print("oriLocations", oriLocations)
# locations, totalCost, adjMtrxDist, adjMtrxTimes, nodeWeights, m, points = pickup(n, locations, nodeWeights, adjMtrxDist, {}, m, newPoint, distances, {}, points)
men = totalCost

ix = -1
for i in oriLocations:
	print("i: ", i, len(oriLocations[i]), len(locations[i]))
	if(len(oriLocations[i])+1 != len(locations[i])) :
		ix = i
		continue
	locations[i] = oriLocations[i]
assert(ix != -1)

idx = -1
mnVal = float('inf')
for i in range(len(oriLocations[ix])-1):
	x = oriLocations[ix][i]
	y = oriLocations[ix][i+1]
	val = -adjMtrxDist[x][y] + adjMtrxDist[x][m] + adjMtrxDist[m][y]
	if (val < mnVal):
		mnVal = val
		idx = i

assert(idx != -1)
locations[ix] = oriLocations[ix][:idx+1] + [m] + oriLocations[ix][idx+1:]

# ------------------------

print("locations", locations)

X = []
Y = []
X1 = []
Y1 = []

for i in range(n):
	X.append([])
	Y.append([])

# print(points)
# exit()

for p in range(1, m+1):
   X1.append(points[p-1][1])
   Y1.append(points[p-1][2])

for i in range(n):
	for p in locations[i]:
		X[i].append(points[p-1][1])
		Y[i].append(points[p-1][2])

# print(locations)
# ax.scatter(X1, Y1, color = 'black')
colors = ['blue', 'red', 'yellow', 'green', 'purple']
for i in range (n):
	ax.scatter(X[i], Y[i])

# print(X)
# print(len(X))
# print(Y)
# print(len(Y))
# plt.show()
print(locations.keys())
for i in locations.keys():
	# ax.arrow(i)
	print("here")
	tmp = locations[i]
	for j in range(1, len(tmp)):
		plt.arrow(points[tmp[j-1]-1][1], points[tmp[j-1]-1][2], points[tmp[j]-1][1] - points[tmp[j-1]-1][1], points[tmp[j]-1][2] - points[tmp[j-1]-1][2])
	print(i)
	plt.scatter(X[i], Y[i])

plt.scatter(points[0][1], points[0][2], color = 'black')
plt.show()

