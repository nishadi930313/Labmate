import matplotlib.pyplot as plt
import numpy as np
import cv2
import math


def find_people_in_queue(bounding_boxes, threshold=2):
# bounding_boxes is an array of arrays, each array containing multiple (x,y) points representing the center of each bounding boxe  

# threshold: Another approach is to use a statistical method, such as calculating the mean and standard deviation of the distances between the convex hull line and the mid-points of the bounding boxes, and then setting the threshold as a multiple of the standard deviation (e.g. 2 or 3 times the standard deviation).
        
    #bounding_boxes = bounding_boxes[:1] # just to reduce nb of instance for testing

    instances = []

    for instance in bounding_boxes:

        if len(instance) == 0: # no people in the image
            instances.append([[],[],[],[]])

        else:

            # Define the input points
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

            pts_inside_hull = []
            pts_outside_hull = []
            for point in points:
                distance = abs(m*point[0] - point[1] + c) / math.sqrt(m**2 + 1)
                if distance <= threshold:
                    pts_inside_hull.append(point)
                else:
                    pts_outside_hull.append(point)

            instances.append([pts_inside_hull, pts_outside_hull, hull_points, line_points])
                
    return instances
        

def plot(pts_inside_hull, pts_outside_hull, hull_points, line_points):
    # Plot the input points, convex hull, and the line that minimizes the perpendicular distance (plot people in the line)
    for p in pts_inside_hull:
        plt.plot(p[0], p[1], 'o', color='green')
    for p in pts_outside_hull:
        plt.plot(p[0], p[1], 'o', color='red')
    plt.plot(*zip(*hull_points), 'r-')
    plt.plot(*zip(*line_points), 'k-')
    plt.show()