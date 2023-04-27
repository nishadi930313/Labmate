import os, sys
import matplotlib.pyplot as plt
sys.path.append(os.getcwd()+'/models/faster_rcnn')
from models.faster_rcnn import inference
from queue_orientation import *


directory = os.getcwd() + "/models/faster_rcnn/images"
model_config_file = "COCO-Detection/faster_rcnn_R_50_C4_1x.yaml"
model_checkpoint = "COCO-Detection/faster_rcnn_R_50_C4_1x.yaml"

faster_rcnn = inference.FasterRCNN(directory, model_config_file, model_checkpoint)
out = faster_rcnn.run_inference()
#faster_rcnn.show_outputs(out)

points = faster_rcnn.get_bounding_boxes_centers(out)

find_people_in_queue(points)