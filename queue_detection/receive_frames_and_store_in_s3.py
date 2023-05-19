from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import shutil
import boto3

# define the port to listen on
PORT = 4000
bucket_name = 'labmate'

# define a custom request handler that saves the received frames to disk
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
        # delete temp (ile                                                    )
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