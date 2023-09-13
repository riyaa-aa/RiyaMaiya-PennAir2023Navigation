import json
from geopy.distance import geodesic
import numpy as np
import matplotlib.pyplot as plt
from python_tsp.exact import solve_tsp_dynamic_programming

# TASK 1

f = open('data/coords.json')
data = json.load(f)

# TASK 2

def find_distance(wp1, wp2):
    lat1 = list(wp1.values())[0] # latitude of waypoint 1
    long1 = list(wp1.values())[1] # longitude of waypoint 1
    alt1 = list(wp1.values())[2] # altitude of waypoint 1

    lat2 = list(wp2.values())[0]
    long2 = list(wp2.values())[1]
    alt2 = list(wp2.values())[2]

    dist_ll = geodesic((lat1, long1), (lat2, long2)).feet
    dist = np.sqrt(((abs(alt2 - alt1))**2)+(dist_ll**2))

    return dist

# testing find_distance based on the test case given in instructions.md
waypoint1 = data['waypoints'][0]
waypoint2 = data['waypoints'][1]

# find_distance(waypoint1, waypoint2)
# output: 1350.9321704989154 which is correct!

# TASK 3

dist_arr = [[0 for i in range(14)] for j in range(14)] # initializes a 2d array that is 14x14, where each element = 0

for i in range(14):
    waypointi = data['waypoints'][i]
    for x in range(14):
        waypointx = data['waypoints'][x]
        dist_arr[i][x] = find_distance(waypointi,waypointx) # filling up the arr row by row

# checking test case again; should give the distance between waypoint 1 and 2, which should be 1350.9321704989154
# dist_arr[0][1]
# output: 1350.9321704989154 -- correct!
# also: dist_arr[i][x] where i == x is always 0, which is correct since distances between waypoint n and waypoint n are always zero since they are at the same point

# hamiltonian cycle: every node visited once, come back to the starting node
# minimize the total cost of this cycle; output the minimum weight hamiltonian cycle

# number of nodes -- 14 waypoints
n = 14 

# memoization for top-down recursion
# using a bitmask to represent which waypoints have been visited,
# a bitmask of 00000000000000 would mean all 14 waypoints have been visited.

memo = [[(-1, [])]*(1 << (n)) for _ in range(n)] # list of lists of -1s + empty lists to store route
# memoization is a way to speed up & optimize recursion programs
# by storing intermediate results to avoid repeated results

def get_min_dist(i,mask):

    if mask == ((1 << i)): 
    # implies all the bits but 1 (the endpoint) have been visited
        return dist_arr[0][i], [0,i] # the distance from waypoint 0 to waypoint i bc all other waypoints have been visited
    
    if memo[i][mask][0] != -1: # min dist has been recorded
        return memo[i][mask] # this is the dynamic programming part that prevents the algorithm from having to repeat calculations

    # this is just setting a max value that the total dist could be
    # from the dist_arr, I know that the distances are 3-4 digits, and there are 14 distances
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
            # flipping the ith node to 0 on the mask
            # saying that that node is now being visited
            if min_dist > md+dist_arr[j][i]:
                min_dist = md+dist_arr[j][i]
                shortest_route = route + [i]
    
    memo[i][mask] = min_dist, shortest_route  # storing the minimum value + cities visited on this route

    return min_dist, shortest_route

min_d, route = get_min_dist(0, (1 << (n))-1) # setting mask to be 14 1s; every node needs to be visited
route.reverse() # because we got the min dist by going from the end to the beginning, the route we got needs to be reversed
# memo[0][16383] will give you the min dist + route; node 0 is the endpoint, 16383 = binary list of 14 1s, meaning that the min dist value stored in memo[0][16383] takes into account every single node

print("The minimum distance to travel to all 14 waypoints = " + str(min_d))
# output: 13358.79556824653
print("The shortest route to take = " + str(route))
# output: [0, 13, 4, 5, 6, 7, 8, 9, 10, 11, 12, 3, 2, 1, 0]

# using a python library to check if my code outputs the correct answer
distance_matrix = np.array(dist_arr)
permutation, distance = solve_tsp_dynamic_programming(distance_matrix)
# permutation output: [0, 13, 4, 5, 6, 7, 8, 9, 10, 11, 12, 3, 2, 1]
# distance output: 13358.79556824653
# code is correct!

# TASK 4

minLat = 90
minLong = 90

for i in data['flyZones']:
    for x in (i['boundaryPoints']):
        if minLat > (x['latitude']):
            minLat = (x['latitude'])
        if minLong > (x['longitude']):
            minLong = (x['longitude'])

def get_coords(waypoint, min_lat, min_long):

    wp_lat = list(waypoint.values())[0] # latitude of waypoint
    wp_long = list(waypoint.values())[1] # longitude of waypoint

    x = abs(wp_long - min_long) # normalizing the waypoint longitude
    y = abs(wp_lat - min_lat) # normalizing the waypoint latitude

    return x,y

# to show direction that the plane is travelling in
def draw_arrows(xarr, yarr):
    x0 = xarr[i]
    x1 = xarr[i+1]
    y0 = yarr[i]
    y1 = yarr[i+1]
    xpos = (x0+x1)/2
    ypos = (y0+y1)/2
    xdir = x1-x0
    ydir = y1-y0
    return xpos, ypos, xdir, ydir

xcoordsArr = []
ycoordsArr = []

# getting array of points to plot
for i in route:
    x,y = get_coords(data['waypoints'][i], minLat, minLong)
    xcoordsArr.append(x)
    ycoordsArr.append(y)

plt.scatter(xcoordsArr,ycoordsArr) # plotting points
plt.plot(xcoordsArr,ycoordsArr) # plotting line to join points
plt.xlabel('longitude')
plt.ylabel('latitude')
plt.grid('equal')
plt.text(xcoordsArr[0]-4e-4,ycoordsArr[0]+4e-4, "start") # where you start; should be waypoint 0
plt.title('shortest route')
for i in range(len(xcoordsArr)-1):
    xpos, ypos, xdir, ydir = draw_arrows(xcoordsArr,ycoordsArr)
    plt.annotate("", xytext=(xpos,ypos),xy=(xpos+0.001*xdir,ypos+0.001*ydir), # putting arrows along the line; direction the plane moves in
    arrowprops=dict(arrowstyle="->", color='k'), size = 20) # styling the arrows
plt.show()

f.close()