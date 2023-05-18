import torch
from PIL import Image
from detector import Detector 
from pprint import pprint
from convex_hull import ConvexHull
import glob
import cv2
import os

def main():
    detectorModule = Detector()
    model = detectorModule.load_model("yolov5x", pretrained = True)

    images = glob.glob("models/yolov3/input_img/*.png")

    filename = 'models/yolov3/input_img/line.png'
    # Predict People
    for image_name in images:
        filename = image_name
        print(f"FILENAME : {filename}")
        
        people_predictions = detectorModule.predict_people(model, filename)
        q = detectorModule.predict_queue(people_predictions)
        
        image = cv2.imread(image_name)
        for i, p in enumerate(q):
            image = cv2.circle(image, (p[0],p[1]), radius=5, color=(0, 255, 0), thickness=5)
        basename = os.path.basename(filename)
        name, extension = os.path.splitext(basename)
        print("Number of people in line: " + str(len(q)))
        cv2.imwrite(f"models/yolov3/output_img/{name}_result.jpg", image)

if __name__ == "__main__":
    main()