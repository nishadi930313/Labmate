import numpy as np 
import cv2
import time 

# Optical Flow Tracker 
class OpticalFlowTracker:
    def __init__(self, bbox, frame, start_time, smooth_window=5):
        self.bbox = bbox  # initial bounding box
        self.track_points = np.array([[[bbox[0] + (bbox[2] - bbox[0]) / 2, bbox[1] + (bbox[3] - bbox[1]) / 2]]], np.float32)  # center point of bounding box
        self.old_frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.start_time = start_time
        self.end_time = None
        self.lk_params = dict(winSize=(15, 15),
                              maxLevel=2,
                              criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))
        self.width = bbox[2] - bbox[0]  # width of the bounding box
        self.height = bbox[3] - bbox[1]  # height of the bounding box
        # Initialize a list to store the past few bounding boxes for smoothing
        self.past_bboxes = [self.bbox]
        self.smooth_window = smooth_window
        self.start_frame_idx = None 
        self.end_frame_idx = None

    def update(self, frame):
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        new_points, status, error = cv2.calcOpticalFlowPyrLK(self.old_frame_gray, frame_gray, self.track_points, None, **self.lk_params)
        self.old_frame_gray = frame_gray.copy()
        self.track_points = new_points
        self.bbox = [new_points[0,0,0] - self.width / 2, new_points[0,0,1] - self.height / 2, new_points[0,0,0] + self.width / 2, new_points[0,0,1] + self.height / 2]

        # Add the new bounding box to the list of past bounding boxes
        self.past_bboxes.append(self.bbox)
        # If we have more past bounding boxes than the smoothing window size, remove the oldest
        if len(self.past_bboxes) > self.smooth_window:
            self.past_bboxes.pop(0)

        # Calculate the average bounding box coordinates over the past few frames for smoothing
        smoothed_bbox = np.mean(self.past_bboxes, axis=0)
        return smoothed_bbox

    def calculate_wait_time(self):
        if self.end_time is not None:
            return self.end_time - self.start_time
        else:
            self.end_time = time.time()
            return self.end_time - self.start_time