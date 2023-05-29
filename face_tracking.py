import os
import time
import numpy as np
import torch
import cv2
import subprocess
import argparse
from PIL import Image, ImageDraw
from facenet_pytorch import MTCNN
from optical_flow import OpticalFlowTracker

parser = argparse.ArgumentParser(description='Face tracking using Optical Flow.')
parser.add_argument('--input', type=str, required=False, help='Path to the video file.', default = "videos/face-demographics-walking-and-pause.mp4")
parser.add_argument('--output', type=str, required=False, help='Path to the directory where output frames will be saved.', default = "tracked_face")

# Get length of video in seconds
def get_length(filename):
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT)
    return float(result.stdout)

# IOU (Intersection Over Union): Area of overlap/area of union threshold
def calculate_iou(box1, box2):
    # Calculate the (x, y)-coordinates of the intersection rectangle
    xi1 = max(box1[0], box2[0])
    yi1 = max(box1[1], box2[1])
    xi2 = min(box1[2], box2[2])
    yi2 = min(box1[3], box2[3])

    inter_area = max(0, xi2 - xi1 + 1) * max(0, yi2 - yi1 + 1)

    # Calculate the area of both rectangles
    box1_area = (box1[2] - box1[0] + 1) * (box1[3] - box1[1] + 1)
    box2_area = (box2[2] - box2[0] + 1) * (box2[3] - box2[1] + 1)

    # Calculate the intersection over union
    iou = inter_area / float(box1_area + box2_area - inter_area)
    return iou

def main():
    args = parser.parse_args()
    # Use GPU
    device = torch.device('cuda:1' if torch.cuda.is_available() else 'cpu')
    print('Running on device: {}'.format(device))
    # Load face detection model
    mtcnn = MTCNN(keep_all=True, device=device)

    video_dir = args.input
    video = cv2.VideoCapture(video_dir)

    frames = []
    trackers = []
    while video.isOpened():
        ret, frame = video.read()
        if not ret:
            break
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frames.append(Image.fromarray(frame))

    video.release()

    frames_dir = args.output
    os.makedirs(frames_dir, exist_ok=True)

    video_length = get_length(video_dir)
    num_frames = len(frames)
    fps = num_frames / video_length
    print("Video FPS: " + str(fps))

    frames_tracked = []
    track_face = True
    for i, frame in enumerate(frames):
        print('\rTracking frame: {}'.format(i + 1), end='')
                                                
        frame_draw = frame.copy()
        draw = ImageDraw.Draw(frame_draw)
        frame_np = np.array(frame)

        if track_face:
            # Detect faces
            boxes, _ = mtcnn.detect(frame)
            # if a face is detected
            if boxes is not None:
                # sort by y coordinate of the box (topmost face)
                boxes = sorted(boxes, key=lambda y: y[1])
                # Only track the topmost face
                box = boxes[0]
                tracker_exists = False
                for tracker in trackers:
                    iou = calculate_iou(box, tracker.bbox)
                    if iou > 0.5:
                        tracker_exists = True
                        break
                if not tracker_exists:
                    tracker = OpticalFlowTracker(box.tolist(), frame_np, time.time())
                    tracker.start_frame_idx = i
                    trackers.append(tracker)
                    track_face = False

        if trackers:  # If there is a tracker in the list
            tracker = trackers[0]
            tracker.end_frame_idx = i 
            print("\nTracking in process...")
            updated_bbox = tracker.update(frame_np)
            updated_bbox = updated_bbox.tolist()  # convert numpy array to list
            # Ensure that the coordinates are valid      
            print(updated_bbox)                                                                         
            if updated_bbox[0] < updated_bbox[2] and updated_bbox[1] < updated_bbox[3] and updated_bbox[0] > 0 and updated_bbox[0] > 0 and updated_bbox[1] > 0 and updated_bbox[2] > 0 and updated_bbox[3] > 0:
                draw.rectangle(updated_bbox, outline=(255, 0, 0), width=1)
            else:
                # If not valid, calculate wait time, remove tracker and restart face tracking
                tracking_duration = (tracker.end_frame_idx - tracker.start_frame_idx + 1) / fps
                print(f'Duration of tracking for person: {tracking_duration} seconds')
                trackers.remove(tracker)
                track_face = True

        # Add to frame list
        tracked_frame = frame_draw.resize((640, 360), Image.BILINEAR)
        frames_tracked.append(tracked_frame)
        # Save frame to file
        tracked_frame.save(os.path.join(frames_dir, f'frame_{i+1:04d}.png'))

    print('\nFinished')

if __name__ == "__main__":
    main()