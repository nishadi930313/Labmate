import cv2
import numpy as np
import matplotlib.pyplot as plt

# this function returns returns the points that are contained between 2 lines on an image
def find_points_between_lines(instances_points, m1=2, c1=-2000, m2=-4, c2=4000): # m1,c1 are the slope-intercept of the first line
    
    instances = []

    for points in instances_points:

        if len(points) == 0: # no people in the image
            instances.append([])

        else:
        
            # Convert the points array to a numpy array
            points = np.array(points)
            
            # Create a mask for points between the two lines
            mask = np.logical_and(
                points[:, 1] >= m1*points[:, 0] + c1,
                points[:, 1] <= m2*points[:, 0] + c2
            )
            
            # Filter the points array based on the mask
            filtered_points = points[mask]

            instances.append(filtered_points)
        
    return instances
