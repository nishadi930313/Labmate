import cv2
import requests
import numpy as np
import time

# initialize the video capture object
cap = cv2.VideoCapture(0)

# set the IP address and port of the EC2 instance
ec2_ip = 'ec2-13-50-249-234.eu-north-1.compute.amazonaws.com'
ec2_port = '3000'

# loop to capture and send frames
while True:
    # read a frame from the video capture object
    ret, frame = cap.read()

    # encode the frame into JPEG format
    _, jpeg = cv2.imencode('.jpg', frame)

    # convert the JPEG-encoded frame to bytes
    img_bytes = jpeg.tobytes()

    # create a unique filename based on the current time
    filename = time.strftime('%Y%m%d-%H%M%S') + '.jpg'

    # send the frame to the EC2 instance
    url = 'http://{}:{}/{}'.format(ec2_ip, ec2_port, filename)
    response = requests.post(url, data=img_bytes)

    # wait for 0.1 seconds before capturing the next frame
    time.sleep(0.1)

    # break the loop if the 'q' key is pressed
    if cv2.waitKey(1) == ord('q'):
        break

# release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
