import numpy as np
import matplotlib.pyplot as plt
import sys
import time

def produceIntersection(point1, point2):
    """Converts two points into their respective dual lines and returns the intersection of those lines"""
    if (point1[0] == point2[0]):
        """Either rotate the whole thing by a tiny amount or just add an (effectively?) infinitessimal amount to the x value of one of the points"""
        point1[0] += 0.0000000001
    leftX = point1[0] - point2[0]
    rightY = point2[1] - point1[1]
    rightY /= leftX

    return np.array((rightY, point1[0] * rightY + point1[1]))

def Herons(points):
    """Thanks to Heron of Alexandria, calculates area and perimeter of a triangle using the lengths of its sides"""
    dists = [np.linalg.norm(points[0] - points[1]), np.linalg.norm(points[1] - points[2]), np.linalg.norm(points[2] - points[0])]
    s = (np.sum(dists)) / 2
    area = np.sqrt(s * (s - dists[0]) * (s - dists[1]) * (s - dists[2]))
    return area, np.sum(dists)

def triangulate(points):
    linez = np.multiply(points, np.array((1, -1)))
    """Converts points into their respective dual lines"""

    """Return values to calculate"""
    minArea = sys.maxsize
    corlen = 0
    minindices = [0, 0, 0]

    for i in range(linez.shape[0] - 1):
        for j in range(i + 1, linez.shape[0]):
            result = produceIntersection(linez[i], linez[j])
            """Prepares intersection of two points"""

            """Calculates the y value of all dual lines"""
            assorted = np.add(np.multiply(linez, result[0]), linez[:, [1, 0]])[:, 0]

            minidx = 0
            tempmin = 0
            templen = 0

            """Finds the point with the smallest distance to intersection in question that is not the intersection itself"""
            minidx = np.ma.MaskedArray(np.abs(assorted - result[1]), np.abs(assorted - result[1]) == 0).argmin()
            tempmin, templen = Herons([points[i], points[j], points[minidx]])

            if (tempmin < minArea and tempmin > 0):
                minArea = tempmin
                corlen = templen
                minindices = [i, j, minidx]
    
    return minArea, corlen, minindices

def showresults(s, c, points, found):
    print(f"Smallest area: {s}, sum of lengths: {c}")
    print(f"Found: {points[found]}")

    plt.plot(points[:,0], points[:,1], 'o', alpha=0.8)
    plt.plot(points[found,0], points[found,1], 'o', color='red', alpha=0.8)

    t = plt.Polygon(points[found], color='red', alpha=0.2)
    plt.gca().add_patch(t)

    plt.show()

def main():
    """
    seed = input("Please enter a seed for the random number generator or leave empty for random seed: ")
    if (seed != ""):
        if (seed.isnumeric()):
            np.random.seed(int(seed))
        else:
            seedcalc = [ord(x) for x in seed]
            seedcalc = np.prod(seedcalc)
            np.random.seed(seedcalc)
    """
    iterations = 0
    while(True):
        userInput = input("Please enter the number of points to generate: ")
        if (userInput.isdigit()):
            if (int(userInput) > 2):
                iterations = int(userInput)
                break
        print("Please enter a valid number of points (at least 3) to generate.\n")

    points = (np.random.rand(iterations, 2) - 0.5) * 200

    starter = time.time()

    minArea, corlen, minindices = triangulate(points)

    ender = time.time()
    print(f"Executed in {ender - starter} seconds.")

    showresults(minArea, corlen, points, minindices)

if __name__ == "__main__":
    main()
    
"""
Answers to posited questions:

## Handling errors:
- The errors might first occur during user input. If the user inputs anything other than an integer, 
they are prompted to re-enter the number. Similarly, if the user inputs an integer smaller than 3, 
they will also be prompted to re-enter the number, as no triangle will be able to be formed using less than 3 points
- My approach uses duality to convert points to lines and relies on their intersections to find the third point 
that would result in smallest possible area. Should the two former points have the exact same X-axis value, 
such lines would never intersect. To remedy that, either the entire grid could be rotated, 
or an effectively infinitessimal value (I chose 1e-10) could be added to one of them to guarantee an intersection

## Validation of triangles
- I considered a triangle to be valid if its area was greater than 0, which is what I checked for upon finding the new smallest area.
Considering that the points I generated were floating-point numbers and not integers, the likelihood of two points having the exact same coordinates seemed slim, 
so I decided against checking for two different points (when producing the intersection) being the same, 
and masked the points used to produce it when seeking out the third

## Speeding the algorithm up
- The method I used reduced the complexity from O(n^3) to what seems to be O(n^2 log n) thanks to vectorisation
- From what I observed, I discarded my initial idea of finding triangles formed from tight clusters of points,
as the smallest triangles consistently proved to be constructed from distant points that resembled a line
- Having that in mind, I'm not sure how speed could further be improved, save a more efficient sweep for the closest(in terms of Y-coordinate distance)
point to the dual lines intersection
- At the risk (that in this case is essentially a guarantee) of sacrificing accuracy,
the approach of finding the triangle with the smallest perimeter might deliver somewhat acceptable results, depending on one's needs.
It could perhaps be done by creating a moving box, similar to a kernel in a convolutional neural network, that would move over the entire plane,
at each step producing a list of coordinates for points within it

"""
