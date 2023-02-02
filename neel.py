# INPUT FORMAT
# number of drivers
# number of nodes
# weight of each drivers box
# nodename, x coordinate, y coordinate, delivery box weight





from main import solve
from matplotlib import pyplot as plt


n = int(input())
m = int(input())

print("solving part done")
# let hub be location 1
times = [[10000 for i in range(m+1)] for j in range(m+1)]
# print(len(times))

# for i in range(m):
#     for j in range(i+1, m):
#         arr = list(map(int, input().split()))
#         # print(arr)
#         times[arr[0]][arr[1]] = arr[2]
def distance(x1, y1, x2, y2):
    return ((x1 - x2) ** 2 + (y1-y2) ** 2) ** 0.5

points = []

deliveryManWeight = int(input())
# deliveryManWeight = 100
nodeWeights = {}
for i in range(m):
    arr = list(map(float,input().split()))
    # arr.append(1)
    points.append(arr)
    nodeWeights[arr[0]] = arr[-1]

for i in range(m):
    for j in range(i+1, m):
        # print(points[i][0], points[j][0], distance(points[i][1], points[i][2], points[j][1], points[j][2]))
        times[int(points[i][0])][int(points[j][0])] = distance(points[i][1], points[i][2], points[j][1], points[j][2])
        times[int(points[j][0])][int(points[i][0])] = distance(points[i][1], points[i][2], points[j][1], points[j][2])


# print(times[2])
# exit()

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
locations = solve(n, m, times, nodeWeights, deliveryManWeight)

# locations = {18: 1, 1: 1, 5: 1, 10: 1, 14: 1, 19: 1, 23: 1, 27: 1, 31: 1, 36: 1, 40: 1, 44: 1, 48: 1, 52: 1, 56: 1, 60: 1, 64: 1, 68: 1, 72: 1, 77: 1, 81: 1, 85: 1, 73: 2, 2: 2, 6: 2, 11: 2, 15: 2, 20: 2, 24: 2, 28: 2, 32: 2, 37: 2, 41: 2, 45: 2, 49: 2, 53: 2, 57: 2, 61: 2, 65: 2, 69: 2, 74: 2, 78: 2, 82: 2, 86: 2, 9: 3, 3: 3, 7: 3, 12: 3, 16: 3, 21: 3, 25: 3, 29: 3, 34: 3, 38: 3, 42: 3, 46: 3, 50: 3, 54: 3, 58: 3, 62: 3, 66: 3, 70: 3, 75: 3, 79: 3, 83: 3, 87: 3, 33: 4, 4: 4, 8: 4, 13: 4, 17: 4, 22: 4, 26: 4, 30: 4, 35: 4, 39: 4, 43: 4, 47: 4, 51: 4, 55: 4, 59: 4, 63: 4, 67: 4, 71: 4, 76: 4, 80: 4, 84: 4}

X = []
Y = []

for i in range(n):
    X.append([])
    Y.append([])

print(locations)
for i in range(n):
    for p in locations[i]:
       X[i].append(points[p-1][1])
       Y[i].append(points[p-1][2])
       

colors = ['blue', 'red', 'yellow', 'green', 'purple']
for i in range (n):
    ax.scatter(X[i], Y[i], color = colors[i])

plt.show()