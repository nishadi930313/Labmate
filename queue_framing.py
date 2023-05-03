import cv2
import numpy as np
import matplotlib.pyplot as plt


def find_slop_intercept_values(img_shape, l1_bottom=0.15, l1_top=0.5, l2_bottom=0.8, l2_top=0.7): # l1_bottom is a point (l1_bottom*img_width,0) and l1_top is a point (l1_top*img_width,0) defining line 1
    height, width = img_shape[:2]

    # Convert the line points to pixel coordinates
    l1_x1, l1_y1 = int(l1_bottom*width), height
    l1_x2, l1_y2 = int(l1_top*width), 0
    l2_x1, l2_y1 = int(l2_bottom*width), height
    l2_x2, l2_y2 = int(l2_top*width), 0

    # Fit lines to the points using np.polyfit
    m1, c1 = np.polyfit([l1_x1, l1_x2], [l1_y1, l1_y2], 1)
    m2, c2 = np.polyfit([l2_x1, l2_x2], [l2_y1, l2_y2], 1)

    return m1, c1, m2, c2


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
            if m1 < 0:
                if m2<0:
                    mask = np.logical_and(
                        points[:, 1] > m1*points[:, 0] + c1,
                        points[:, 1] < m2*points[:, 0] + c2
                    )
                else:
                    mask = np.logical_and(
                        points[:, 1] > m1*points[:, 0] + c1,
                        points[:, 1] > m2*points[:, 0] + c2
                    )
            else:
                if m2<0:
                    mask = np.logical_and(
                        points[:, 1] < m1*points[:, 0] + c1,
                        points[:, 1] < m2*points[:, 0] + c2
                    )
                else:
                    mask = np.logical_and(
                        points[:, 1] < m1*points[:, 0] + c1,
                        points[:, 1] > m2*points[:, 0] + c2
                    )
            
            # Filter the points array based on the mask
            filtered_points = points[mask]

            instances.append(filtered_points)
        
    return instances
