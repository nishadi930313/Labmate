import matplotlib.pyplot as plt
import numpy as np
import cv2
import math


def find_people_in_queue(bounding_boxes):
# bounding_boxes is an array of arrays, each array containing multiple (x,y) points representing the center of each bounding boxe  

    bounding_boxes = bounding_boxes[0] # just to reduce nb of instance for testing

    for instance in bounding_boxes:
        # Define the input points
        #points = np.array([(1, 2.5), (3.5, 4), (5, 5), (7, 8), (0.1, 7), (9, 8)], np.float32)
        points = np.array(instance, np.float32)

        # Compute the convex hull
        hull = cv2.convexHull(points)

        # Extract the x and y coordinates of the points on the convex hull
        hull_points = []
        for i in range(len(hull)):
            hull_points.append((hull[i][0][0], hull[i][0][1]))

        # Find the line that minimizes the perpendicular distance of the points on the hull
        x_coords, y_coords = zip(*hull_points)
        A = np.vstack([x_coords, np.ones(len(x_coords))]).T
        m, c = np.linalg.lstsq(A, y_coords, rcond=None)[0]
        line_points = [(min(x_coords), m*min(x_coords) + c),
                    (max(x_coords), m*max(x_coords) + c)]

        # Plot the input points, convex hull, and the line that minimizes the perpendicular distance (plot people in the line)
        threshold = 2 # Another approach is to use a statistical method, such as calculating the mean and standard deviation of the distances between the convex hull line and the mid-points of the bounding boxes, and then setting the threshold as a multiple of the standard deviation (e.g. 2 or 3 times the standard deviation).
        for point in points:
            distance = abs(m*point[0] - point[1] + c) / math.sqrt(m**2 + 1)
            if distance <= threshold:
                plt.plot(point[0], point[1], 'o', color='green')
            else:
                plt.plot(point[0], point[1], 'o', color='red')
        plt.plot(*zip(*hull_points), 'r-')
        plt.plot(*zip(*line_points), 'k-')
        plt.show()

