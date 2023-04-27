import matplotlib.pyplot as plt
import numpy as np
import cv2
import math
from bisect import bisect_left


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, slope, intercept):
        self.slope = slope
        self.intercept = intercept

    def value(self, x):
        return self.slope * x + self.intercept


def intersection(l1, l2):
    x = (l2.intercept - l1.intercept) / (l1.slope - l2.slope)
    y = l1.slope * x + l1.intercept
    return Point(x, y)


def perpendicular_distance(line, point):
    numerator = abs(line.slope * point.x - point.y + line.intercept)
    denominator = math.sqrt(line.slope ** 2 + 1)
    return numerator / denominator


def convex_hull_trick(points):
    points.sort(key=lambda p: p.x)
    lines = []
    hull = []
    for point in points:
        line = Line(point.y / point.x, point.y - point.x * point.y / point.x)
        if len(lines) > 0:
            i = bisect_left([intersection(lines[h], lines[h + 1])
                            for h in hull[:-1]], point.x)
            line = lines[hull[i]] if i < len(hull) else lines[hull[-1]]
            while len(hull) > 1 and intersection(lines[hull[-2]], lines[hull[-1]]).x < point.x:
                hull.pop()
                line = lines[hull[-1]]
            if len(hull) > 0 and lines[hull[-1]].slope == line.slope:
                hull.pop()
        lines.append(line)
        hull.append(len(lines) - 1)
    return lines


def solve(points):
    lines = convex_hull_trick(points)
    min_distance = float('inf')
    min_line = None
    for line in lines:
        print(line.slope)
        distance = sum(perpendicular_distance(line, point) for point in points)
        if distance < min_distance:
            min_distance = distance
            min_line = line
    return min_line



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

