import cv2
import numpy as np

def load_yolo_model():
    net = cv2.dnn.readNet("yolov3.weight", "models/yolov3/yolov3.cfg")
    with open("models/yolov3/coco.names", "r") as f:
        classes = [line.strip() for line in f.readlines()]
    return net, classes

def get_output_layers(net):
    layer_names = net.getLayerNames()
    output_layers_indices = net.getUnconnectedOutLayers().flatten()
    output_layers = [layer_names[i - 1] for i in output_layers_indices]
    return output_layers


def detect_humans(image, net, classes):
    img = cv2.imread(image)
    height, width, _ = img.shape
    blob = cv2.dnn.blobFromImage(img, 1/255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    outs = net.forward(get_output_layers(net))

    human_count = 0
    class_ids = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.5 and classes[class_id] == 'person':
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
                human_count += 1

    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    human_count = 0
    for i in indices.flatten():
        human_count += 1
        box = boxes[i]
        x, y, w, h = box[0], box[1], box[2], box[3]
        label = str(classes[class_ids[i]])
        color = (0, 255, 0)
        cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
        cv2.putText(img, label, (x, y + 30), cv2.FONT_HERSHEY_PLAIN, 1, color, 2)

    cv2.imwrite("models/yolov3/output_image.jpg", img)
    return human_count

def main(image_path):
    net, classes = load_yolo_model()
    human_count = detect_humans(image_path, net, classes)
    print(f"Number of humans detected: {human_count}")

if __name__ == "__main__":
    input_image = "models/yolov3/line.png"
    main(input_image)
