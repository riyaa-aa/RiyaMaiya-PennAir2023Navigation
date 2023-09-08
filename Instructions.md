![alt_text](logos/image1.png "image_tooltip")



# Software Navigation Challenge

Welcome to the 2023 Penn Aerial Robotics software challenge! The goal of this challenge is not only for the board to best assess your fit for the software team, but also for you to get a taste for the types of projects that you will be asked to tackle as a member of the team.

Take however long you want to work on the challenge. If you can’t complete the full challenge, don’t worry—it’s meant to be difficult. Remember we are looking for commitment and willingness to learn, not previous knowledge, so don’t get discouraged if you’re having trouble. We’ve provided resources below to help you and are looking for you to give this your best effort. **Submit however much you can complete.** Be prepared to talk about your code and to explain how you arrived at your solution.


# Submission

Please **submit a zip file** containing your code on the google form with your application by **11:59 p.m. Wednesday, September 14th**:

Please include your full name in the title of your zip file.

Please also include a README file in your submission with the following:



1. How far did you get with the challenge? How much time did it take?
2. Please provide a brief description of the way that you have organized your code.
    1. Be sure to also include total distance traveled and waypoint order from Task 3.
3. Please **provide instructions on how to run your code**.
4. Is there any other relevant information that would be helpful for us to know?


# Support

If you have clarification questions or are in need of any assistance, don’t hesitate to reach out! Especially if you have trouble during figuring out how to use GitHub. We want to challenge you with the coding challenge, not with the setup. Feel free to email [jsq@seas.upenn.edu](mailto:jsq@seas.upenn.edu) or [daveshv@seas.upenn.edu](mailto:daveshv@seas.upenn.edu).


# Resources

Feel free to use whatever outside resources you wish. In fact, we highly recommend that you do research into the subject of navigation and obstacle avoidance. A large part of being on this team is learning how to do research and figure things out. We strongly suggest using **Python** as that is the main coding language at PennAir. You can use whatever guides you find online, and whatever libraries you want. However, you must fully understand how your code works because you will be asked to explain it. Commenting your code is also good practice and can help us (and you) understand what you’re doing. You might find the following websites useful:

(Short tutorial on how to read JSON files with Python)

[https://www.programiz.com/python-programming/json](https://www.programiz.com/python-programming/json)

(Documentation for the GeoPy library)

[https://geopy.readthedocs.io/en/stable/](https://geopy.readthedocs.io/en/stable/)

(Tutorial on how to more efficiently solve the traveling salesman problem)

[https://www.geeksforgeeks.org/travelling-salesman-problem-set-1/](https://www.geeksforgeeks.org/travelling-salesman-problem-set-1/)

(Cool tool for real world flight planning eg. KJFK to KLAX)

[https://flightplandatabase.com/planner](https://flightplandatabase.com/planner)

(Contains the ICAO codes to fill in for the link above)

[https://en.wikipedia.org/wiki/List_of_airports_by_ICAO_code:_K#K_%E2%80%93_United_States](https://en.wikipedia.org/wiki/List_of_airports_by_ICAO_code:_K#K_%E2%80%93_United_States)

You should also feel free to reach out to [jsq@seas.upenn.edu](mailto:jsq@seas.upenn.edu) or [daveshv@seas.upenn.edu](mailto:daveshv@seas.upenn.edu) if you are stuck and need some assistance.


# The Challenge

Previously, at the AUVSI 2022 competition, one of our challenges was to identify and navigate through waypoints, around obstacles, and inside the boundaries. The task presented to you is a simplified version of the competition. 

**Please find the JSON file provided for this task under the “data” folder.**

The challenge is split into four parts, but **the fourth part is optional. You should attempt the problems in order, and only attempt part four if you want to visualize your work.**


## Part 1: Reading JSON File

Your first task is to read the JSON file presented above. You can either mount the folder to read the file or download the file, whichever you prefer. In the JSON file, you should read the waypoints data storing the latitude, longitude, and altitude. The other data is used for different missions in the AUVSI competition.


## Part 2: Calculate Lat/Long/Altitude Distances 

**Note: We would like you to install the geopy library for this part.** 

Now that you have the waypoint data, you need to create a function finding the distance between two waypoints. The input to the function should be two waypoints, with the result being the distance. The geopy python library is simplistic with the command **geodesic((lat, long), (lat, long)).feet**, finding distances between two latitude and longitudes. To add in the altitude element, square the difference between the first and second coordinate altitude. Add this value to the square of lat/long distance. Finally square root this value to get the desired outcome.

Ex: Between Waypoint 1 (38.1446916666667, -76.4279944444445, 200.0) and Waypoint 2  (38.1461944444444, -76.4237138888889, 300.0), your result should be 1350.9321704989145 feet.


## Part 3: Finding the Optimal Path

With the function above, create an array of distances between waypoints, which will result in an array of shape (14, 14). 

Then, starting from the first waypoint (38.1446916666667, -76.4279944444445, 200.0), find the order to visit each of the other waypoints and return to the start, in order to minimize the total distance traveled. Then print out the total distance you need to travel to visit each waypoint and travel back to the beginning, as well as the indices of all the waypoints, in the optimal order (with the first point having an index of 0, the second point being at index 1, etc).

Hint: This is a variation of the traveling salesman problem. To ensure that your code is efficient, try to use the more advanced dynamic programming solution to the problem, which you can find in the resources section.


## Part 4: Visualization

We will leave this part open ended. Your goal is to create a plot of the waypoints by either converting the latitude longitude coordinates to a flat x y grid. (Obviously there is curvature on Earth, but for the sake of simplicity we want you to plot this data on a linear basis). Then based on the minimum values of **flyZones** coordinates, which is the origin of the map. Set minLat and minLong as the minimum latitude and longitude for the flyZones. Note: These values do not have to be from the same coordinate.

From there, create a function for each waypoint, setting x equal to the distance between the waypoint and minLat with waypoint longitude. Similarly, set y equal to the distance between the waypoint and waypoint lat with minLong. With these points, use matplotlib or another library to map out the coordinates.
Include this image along with your code in your final ZIP submission.
