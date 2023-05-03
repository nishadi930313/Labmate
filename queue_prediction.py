import os, sys, cv2
import matplotlib.pyplot as plt
import numpy as np
sys.path.append(os.getcwd()+'/models/faster_rcnn')
from models.faster_rcnn import inference
from queue_orientation import *
from queue_framing import *


def plot_image_with_points(image_path, points, saving_folder=None, line1=None, line2=None): # line = (m,c)
    image_name = image_path.split("/")[-1]
    # Load the image using cv2
    image = cv2.imread(image_path)
    # Convert the image from BGR to RGB format
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Convert the list of points to a numpy array and extract the x and y coordinates
    points = np.array(points)
    x_coords, y_coords = np.hsplit(points, 2)
    # Create a new figure and set its size
    fig, ax = plt.subplots(figsize=(8, 8))
    # Plot the image
    ax.imshow(image)
    # Plot the points as red circles with a radius of 5 pixels
    ax.scatter(x_coords, y_coords, s=5**2, c='r')
    # Plot the lines
    if line1 != None:
        x1 = 0
        y1 = m1 * x1 + c1
        x2 = img_shape[1]
        y2 = m1 * x2 + c1
        plt.plot([x1, x2], [y1, y2], color='blue')
    if line2 != None:
        x1 = 0
        y1 = m2 * x1 + c2
        x2 = img_shape[1]
        y2 = m2 * x2 + c2
        plt.plot([x1, x2], [y1, y2], color='blue')
    # Set the x and y limits to match the image dimensions
    ax.set_xlim(0, image.shape[1])
    ax.set_ylim(image.shape[0], 0)
    # Save image
    if saving_folder is not None:
        plt.savefig(saving_folder + "/" + image_name, image)
    # Show the plot
    plt.show()


# pick method to use to extract people queuing among all people deteted
methods = ["framing", "queue_orientation"]
method = methods[0]

# pick model for inferrence
models = ["faster_rcnn"]
model = models[0]

# indicate necessary paths
directory = os.getcwd() + "/models/faster_rcnn/images"
model_config_file = "COCO-Detection/faster_rcnn_R_50_C4_1x.yaml"
model_checkpoint = "COCO-Detection/faster_rcnn_R_50_C4_1x.yaml"

# make predictions
if model == "faster_rcnn":
    faster_rcnn = inference.FasterRCNN(directory, model_config_file, model_checkpoint)
    out = faster_rcnn.run_inference()
    img_shape = out[0]["instances"].image_size # take shape of first image of the dir by default
    #faster_rcnn.show_outputs(out)
    points = faster_rcnn.get_bounding_boxes_centers(out)

# extract people queuing
if method == "queue_orientation":
    # queue orientation with convex hull method
    people_in_queue = find_people_in_queue(points)
    people_in_queue = [p[0] for p in people_in_queue]
    number_people_per_image = [len(p) for p in people_in_queue]
    print(number_people_per_image)
elif method == "framing":
    m1, c1, m2, c2 = find_slop_intercept_values(img_shape) # l1_bottom, l1_top, l2_bottom, l2_top
    print(m1)
    print(m2)
    people_in_queue = find_points_between_lines(points, m1, c1, m2, c2)
    number_people_per_image = [len(p) for p in people_in_queue]
    print(number_people_per_image)

# plot (and save) results
i = 0
for im_name in os.listdir(directory):
    plot_image_with_points(directory + "/" + im_name, people_in_queue[i], line1=(m1,c1), line2=(m2,c2))
    i += 1




