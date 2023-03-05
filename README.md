# Triangulator

This program takes an integer as input, and then generates the corresponding amount of points to randomly place on a 2D plane. After that, it calculates the smallest triangle (by area) that can be formed using any of the three points placed in such a way.

## Handling errors:
- The errors might first occur during user input. If the user inputs anything other than an integer, they are prompted to re-enter the number. Similarly, if the user inputs an integer smaller than 3, they will also be prompted to re-enter the number, as no triangle will be able to be formed using less than 3 points
- My approach uses duality to convert points to lines and relies on their intersections to find the third point that would result in smallest possible area. Should the two former points have the exact same X-axis value, such lines would never intersect. To remedy that, either the entire grid could be rotated, or an effectively infinitessimal value (I chose 1e-10) could be added to one of them to guarantee an intersection

## Validation of triangles
- I considered a triangle to be valid if its area was greater than 0, which is what I checked for upon finding the new smallest area. Considering that the points I generated were floating-point numbers and not integers, the likelihood of two points having the exact same coordinates seemed slim, so I decided against checking for two different points (when producing the intersection) being the same, and masked the points used to produce it when seeking out the third

## Speeding the algorithm up
- The method I used reduced the complexity from O(n^3) to what seems to be O(n^2 log n) thanks to vectorisation
- From what I observed, I discarded my initial idea of finding triangles formed from tight clusters of points, as the smallest triangles consistently proved to be constructed from distant points that resembled a line
- Having that in mind, I'm not sure how speed could further be improved, save a more efficient sweep for the closest (in terms of Y-coordinate distance) point to the dual lines intersection
- At the risk (that in this case is essentially a guarantee) of sacrificing accuracy, the approach of finding the triangle with the smallest perimeter might deliver somewhat acceptable results, depending on one's needs. It could perhaps be done by creating a moving box, similar to a kernel in a convolutional neural network, that would move over the entire plane, at each step producing a list of coordinates for points within it
