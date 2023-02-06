import markov_clustering as mc
from matplotlib import pyplot as plt
import numpy as np
import networkx as nx
from matplotlib import pyplot as plt
from main import solve
from pickup import pickup
import copy


f = open("exOut.in", "r")

n = int(f.readline())
m = int(f.readline())

print("solving part done")
# let hub be location 1
times = [[0 for i in range(m+1)] for j in range(m+1)]
# print(len(times))

def distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

points = []

deliveryManWeight = 100
nodeWeights = {}
for i in range(m):
    arr = list(map(float,f.readline().split()))
    arr.append(1)
    points.append(arr)
    nodeWeights[arr[0]] = arr[-1]

pos = dict()
pos[0] = (0,0)
for i in range(m):
    pos[points[i][0]] = (points[i][1], points[i][2])
    for j in range(i+1, m):
        times[int(points[i][0])][int(points[j][0])] =  distance(points[i][1], points[i][2], points[j][1], points[j][2])
        times[int(points[j][0])][int(points[i][0])] =  distance(points[i][1], points[i][2], points[j][1], points[j][2])



network = nx.from_numpy_array(np.matrix(times))

# then get the adjacency matrix (in sparse form)
matrix = nx.to_scipy_sparse_array(network)

result = mc.run_mcl(matrix,inflation=10)
# result = mc.run_mcl(matrix)           # run MCL with default parameters
clusters = mc.get_clusters(result)    # get clusters

# print(len(clusters))
print(clusters)

# mc.draw_graph(matrix, clusters, pos=pos, node_size=50, with_labels=False, edge_color="grey")


fig, ax = plt.subplots(figsize = (10,10))
fig.suptitle("Points")

# n - number of drivers
# m - number of locations
# times - (m + 1)* ( m +1 ) matrix - distance matrix 10000
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
locations, totalCost = solve(n, m, times, {},nodeWeights, deliveryManWeight, 0)
men = totalCost

for i in range(20):
    temp, temp1 = solve(n, m, times, {},nodeWeights, deliveryManWeight, i%10)
    print(temp1)
    if(temp1 < men):
        totalCost = temp1
        men = temp1
        locations = temp

print("Final Total Cost : ", totalCost)

print(locations)
for i in locations:
    locations[i] = locations[i][5:]
# print(locations)

newPoint = [11, 11, 1]
# points.append([])
distances = {}
for i in points:
    distances[i[0]] = distance(i[1], i[2], newPoint[0], newPoint[1])

distances[m+1] = 0

oriLocations = copy.deepcopy(locations)
print(oriLocations)
locations, totalCost, times, nodeWeights, m, points = pickup(n, locations, nodeWeights, times, {}, m, newPoint, distances, points)
men = totalCost

# ix = -1
# for i in oriLocations:
#     if(len(oriLocations[i]) != len(locations[i])) : 
#         ix = i 
    
#     locations[i] = oriLocations[i]

print(locations)

X = []
Y = []

for i in range(n):
    X.append([])
    Y.append([])

# print(points)
# exit()
for i in range(n):
    for p in locations[i]:

       X[i].append(points[p-1][1])
       Y[i].append(points[p-1][2])
       

# print(locations)
colors = ['blue', 'red', 'yellow', 'green', 'purple']
for i in range (n):
    ax.scatter(X[i], Y[i], color = colors[i])

plt.show()