import torch
# import some common libraries
import numpy as np
import os, json, cv2, random, sys
#p=os.getcwd()
#print(p+"/models/faster_rcnn")
#os.chdir(p+"/models/faster_rcnn")
# Setup detectron2 logger
import detectron2
from detectron2.utils.logger import setup_logger
setup_logger()
#from google.colab.patches import cv2_imshow
import matplotlib.pyplot as plt
from cv2_plt_imshow import cv2_plt_imshow as cv2_imshow, plt_format
# import some common detectron2 utilities
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog, DatasetCatalog
from detectron2.structures import Boxes
#os.chdir(p)


directory = os.getcwd() + "/models/faster_rcnn/images"
model_config_file = "COCO-Detection/faster_rcnn_R_50_C4_1x.yaml"
model_checkpoint = "COCO-Detection/faster_rcnn_R_50_C4_1x.yaml"


def load_images(directory):
    im_list = []  
    for im_name in os.listdir(directory):
        im = cv2.imread(directory+"/"+im_name)
        im_list.append(im)
        #cv2_imshow(im)
        #plt.show()
    return im_list


## Function for detecting and segmenting only 1 class i.e cups
def onlykeep_person_class(outputs,im):
    cls = outputs['instances'].pred_classes
    scores = outputs["instances"].scores
    boxes = outputs['instances'].pred_boxes

    # index to keep whose class == 0
    indx_to_keep = (cls == 0).nonzero().flatten().tolist()
    
    # only keeping index  corresponding arrays
    cls1 = torch.tensor(np.take(cls.cpu().numpy(), indx_to_keep))
    scores1 = torch.tensor(np.take(scores.cpu().numpy(), indx_to_keep))
    boxes1 = Boxes(torch.tensor(np.take(boxes.tensor.cpu().numpy(), indx_to_keep, axis=0)))
  
    # create new instance obj and set its fields
    obj = detectron2.structures.Instances(image_size=(im.shape[0], im.shape[1]))
    obj.set('pred_classes', cls1)
    obj.set('scores', scores1)
    obj.set('pred_boxes',boxes1)
    return {'instances':obj}


def show_outputs(cfg, outputs):
    i=0
    for output in outputs:
        v = Visualizer(im_list[i][:, :, ::-1], MetadataCatalog.get(cfg.DATASETS.TRAIN[0]), scale=1.2)
        out = v.draw_instance_predictions(output["instances"].to("cpu"))
        cv2_imshow(out.get_image()[:, :, ::-1])
        plt.show()
        i+=1



im_list = load_images(directory)

cfg = get_cfg()
# add project-specific config (e.g., TensorMask) here if you're not running a model in detectron2's core library
cfg.merge_from_file(model_zoo.get_config_file(model_config_file))
cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5  # set threshold for this model
# Find a model from detectron2's model zoo
cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(model_checkpoint)
predictor = DefaultPredictor(cfg)

outputs = []
for im in im_list:
    outputs.append(predictor(im))

modified_outputs = []
for i in range(len(outputs)):
    modified_outputs.append(onlykeep_person_class(outputs[i],im_list[i]))

show_outputs(cfg, modified_outputs)

