import json
import geopy
from geopy.distance import geodesic
import math
from sys import maxsize
from itertools import permutations
import numpy as np
import matplotlib.pyplot as plt

# task 1
f = open('data/coords.json')
data = json.load(f)

for i in data['waypoints']:
    # print(i)
    # print(i['latitude'])
    '''
    for x in i:
        print(x)
    '''

# task 2
def find_distance(wp1, wp2):
    lat1 = list(wp1.values())[0] # latitude of waypoint 1
    long1 = list(wp1.values())[1] # longitude of waypoint 1
    alt1 = list(wp1.values())[2] # altitude of waypoint 1

    lat2 = list(wp2.values())[0]
    long2 = list(wp2.values())[1]
    alt2 = list(wp2.values())[2]

    dist_ll = geodesic((lat1, long1), (lat2, long2)).feet
    dist = math.sqrt(((abs(alt2 - alt1))**2)+(dist_ll**2))

    return dist

# testing find_distance based on the test case given in instructions.md
waypoint1 = data['waypoints'][0]
waypoint2 = data['waypoints'][1]

# print(find_distance(waypoint1, waypoint2)) 
# output: 1350.9321704989154 which is correct!

# print(len(data['waypoints']))

# task 3

dist_arr = [[0 for i in range(14)] for j in range(14)] # initializes a 2d array that is 14x14, where each element = 0

'''
for row in data['waypoints']:
    for col in data['waypoints']:
'''
for i in range(14):
    waypointi = data['waypoints'][i]
    for x in range(14):
        waypointx = data['waypoints'][x]
        dist_arr[i][x] = find_distance(waypointi,waypointx) # filling up the arr row by row

# checking test case again; should give the distance between waypoint 1 and 2, which should be 1350.9321704989154
# print(dist_arr[0][1])
# output: 1350.9321704989154 -- correct!

# for row in dist_arr:
#     print(row+'\n')
# print(np.matrix(dist_arr))
# this looks right???? seems like every [n,n] element is 0, which is at least definitely correct 
# (distances between waypoint n and waypoint n are always zero since they are at the same point)

# hamiltonian cycle: every node visited once, come back to the starting node
# minimize the total cost of this cycle; output the minimum weight hamiltonian cycle

# number of nodes -- 14 waypoints
n = 14 

# memoization for top-down recursion
# using a bitmask to represent which waypoints have been visited,
# a bitmask of 00000000000000 would mean all 14 waypoints have been visited.

memo = [[(-1, [])]*(1 << (n)) for _ in range(n)] # list of lists of -1s
# memoization is a way to speed up & optimize recursion programs
# by storing intermediate results to avoid repeated results

def get_min_dist(i,mask):

    if mask == ((1 << i)): 
    # implies all the bits but 1 have been visited
        return dist_arr[0][i], [0,i] # the distance from waypoint 0 to waypoint i bc all other waypoints have been visited
    
    if memo[i][mask][0] != -1: # min dist has been recorded
        return memo[i][mask]

    # this is just setting a max value that the total dist could be
    # from the dist_arr, I know that most distances are 3-4 digits, and there are 14 digits
    # assuming maximum, I just multiplied the largest 4 digit number by 14
    min_dist = 9999*14 
    shortest_route = [] # to store the path that is the shortest

    # we have to travel all nodes j in mask and end the path at ith node
    # so for every node j in mask, recursively calculate cost of travelling all nodes in mask
    # except i and then travel back from node j to node i taking the shortest path 
    # take the minimum of all possible j nodes
    for j in range(0, n):
        if (mask & (1 << j)) != 0 and j != i and j != 0:
            md, route = get_min_dist(j, mask & (~(1 << i))) 
            # this is where the mask is changing
            # making j i, so traversing from 0 to n now
            # flipping the ith node to 0 on the mask
            if min_dist > md+dist_arr[j][i]:
                min_dist = md+dist_arr[j][i]
                shortest_route = route + [i]
    
    memo[i][mask] = min_dist, shortest_route  # storing the minimum value + cities visited on this route

    return min_dist, shortest_route

'''
ans = 9999*14 
shortest_route = []

for i in range(0, n):
    # try to go from node 0 visiting all nodes in between to i
    # then return from i taking the shortest route to 0
    min_d, route = get_min_dist(i, (1 << (n))-1)
    if ans > min_d + dist_arr[i][0]:
        ans = min_d + dist_arr[i][0]
        shortest_route = route 

shortest_route.reverse() 
'''

min_d, route = get_min_dist(0, (1 << (n))-1)
route.reverse() # because we got the min dist by going from the end to the beginning, the route we got needs to be reversed
# doing memo[0][16383] will give you the min dist + route; node 0 is the endpoint, 16363 = binary list of 14 1s, implying all nodes have been visited
# print(memo[0][16383])
'''
for i in range(0,13):
    for x in range((1<<14)-1):
        if memo[i][x][0] != -1:
            print(memo[i][x])
            print("node: " + str(i))
            print("combo: " + str(x))
'''

print("The minimum distance to travel to all 14 waypoints = " + str(min_d))
# output: 13358.79556824653
print("The shortest route to take = " + str(route))
# output: [0, 13, 4, 5, 6, 7, 8, 9, 10, 11, 12, 3, 2, 1, 0]

# task 4

minLat = 90
minLong = 90

for i in data['flyZones']:
    for x in (i['boundaryPoints']):
        if minLat > (x['latitude']):
            minLat = (x['latitude'])
        if minLong > (x['longitude']):
            minLong = (x['longitude'])

# print(minLat, minLong)

def get_coords(waypoint, min_lat, min_long):

    wp_lat = list(waypoint.values())[0] # latitude of waypoint
    wp_long = list(waypoint.values())[1] # longitude of waypoint

    # x = math.dist(min_lat,wp_long)
    # y = math.dist(min_long,wp_lat)
    x = abs(min_lat - wp_long)
    y = abs(min_long - wp_lat)

    return x,y

xcoordsArr = []
ycoordsArr = []

for i in route:
    x,y = get_coords(data['waypoints'][i], minLat, minLong)
    xcoordsArr.append(x)
    ycoordsArr.append(y)

plt.plot(xcoordsArr,ycoordsArr)
plt.xlabel('dist btwn wp & min lat')
plt.ylabel('dist btwn wp & min long')
plt.grid('equal')
plt.show()

f.close()