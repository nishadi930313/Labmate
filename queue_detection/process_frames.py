"""
This script has to be run on server (EC2 port 400 for the moment) to:
- retrieve image sent by send_frames.py script connected to camera
- store image in S3
- run inference on it
- store inference result in RDS
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import shutil
import boto3
import pymysql
from datetime import datetime

# define the port to listen on
PORT = 4000

# configure S3 credentials
s3 = boto3.client('s3',aws_access_key_id='',aws_secret_access_key='') # see server.py script in ec2 for credentials
bucket_name = 'labmate'

# configure RDS
host = 'muc.cyzbfaoq6z0b.eu-north-1.rds.amazonaws.com'
user = '' # see server.py script in ec2 for credentials
database = 'example'
password = '' # see server.py script in ec2 for credentials
connection = pymysql.connect(host=host, user=user, password=password, database=database)
sql = "INSERT INTO Inferences (dt, numpeople) VALUES (%s, %s)"

class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # get the filename from the URL path
        filename = self.path[1:]
        # read the frame bytes from the request body
        content_length = int(self.headers.get('Content-Length'))
        frame_bytes = self.rfile.read(content_length)
        # save the frame bytes to a file
        temp_path = './img_tmp'
        os.makedirs(temp_path)
        with open(os.path.join(temp_path, filename), 'wb') as f:
            f.write(frame_bytes)
        # upload to s3
        s3.upload_file(os.path.join(temp_path,filename), bucket_name, filename)
        # run inference
        inference = 9 # need to call inference script here
        # store inference result in RDS
        try:
            cursor = connection.cursor()
            timestamp = datetime.now()
            cursor.execute(sql, (timestamp, inference))
            connection.commit()
        except pymysql.Error as e:
            print("Error occured when trying to store inference result into RDS: ", e)
        # delete temp file                                                    
        shutil.rmtree(temp_path)
        # send a response back to the client
        self.send_response(200)
        self.end_headers()
        # send a response back to the client
        self.send_response(200)
        self.end_headers()
# create an HTTP server object and start listening for incoming requests
httpd = HTTPServer(('0.0.0.0', PORT), RequestHandler)
print('Listening on port', PORT)
httpd.serve_forever()
