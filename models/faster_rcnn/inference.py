import torch
import numpy as np
import os, json, cv2, random, sys
import matplotlib.pyplot as plt

import detectron2
from detectron2.utils.logger import setup_logger
from detectron2 import model_zoo
from detectron2.engine import DefaultPredictor
from detectron2.config import get_cfg
from detectron2.utils.visualizer import Visualizer
from detectron2.data import MetadataCatalog
from detectron2.structures import Boxes
from cv2_plt_imshow import cv2_plt_imshow as cv2_imshow, plt_format

setup_logger() 


class FasterRCNN:

    def __init__(self, directory, model_config_file, model_checkpoint):
        self.directory = directory
        self.model_config_file = model_config_file
        self.model_checkpoint = model_checkpoint

        self.cfg = get_cfg()
        self.cfg.merge_from_file(model_zoo.get_config_file(self.model_config_file))
        self.cfg.MODEL.ROI_HEADS.SCORE_THRESH_TEST = 0.5
        self.cfg.MODEL.WEIGHTS = model_zoo.get_checkpoint_url(self.model_checkpoint)
        self.predictor = DefaultPredictor(self.cfg)

    def load_images(self):
        im_list = []  
        for im_name in os.listdir(self.directory):
            im = cv2.imread(self.directory + "/" + im_name)
            im_list.append(im)
        #cv2_imshow(im)
        #plt.show()
        return im_list

    def onlykeep_person_class(self, outputs, im):
        cls = outputs['instances'].pred_classes
        scores = outputs["instances"].scores
        boxes = outputs['instances'].pred_boxes

        indx_to_keep = (cls == 0).nonzero().flatten().tolist()

        cls1 = torch.tensor(np.take(cls.cpu().numpy(), indx_to_keep))
        scores1 = torch.tensor(np.take(scores.cpu().numpy(), indx_to_keep))
        boxes1 = Boxes(torch.tensor(np.take(boxes.tensor.cpu().numpy(), indx_to_keep, axis=0)))

        obj = detectron2.structures.Instances(image_size=(im.shape[0], im.shape[1]))
        obj.set('pred_classes', cls1)
        obj.set('scores', scores1)
        obj.set('pred_boxes',boxes1)
        return {'instances':obj}

    def show_outputs(self, outputs, im_list):
        i = 0
        for output in outputs:
            v = Visualizer(im_list[i][:, :, ::-1], MetadataCatalog.get(self.cfg.DATASETS.TRAIN[0]), scale=1.2)
            out = v.draw_instance_predictions(output["instances"].to("cpu"))
            cv2_imshow(out.get_image()[:, :, ::-1])
            plt.show()
            i += 1

    def run_inference(self):
        im_list = self.load_images()

        outputs = []
        for im in im_list:
            outputs.append(self.predictor(im))

        modified_outputs = []
        for i in range(len(outputs)):
            modified_outputs.append(self.onlykeep_person_class(outputs[i], im_list[i]))

        return modified_outputs

    def get_bounding_boxes_centers(self, modified_outputs):
        centered_outputs = []
        for output in modified_outputs:
            centered_outputs.append([])
            boxes_centers = output["instances"].pred_boxes.get_centers()
            for x, y in boxes_centers:
                centered_outputs[-1].append((x.item(),y.item()))
        return centered_outputs


