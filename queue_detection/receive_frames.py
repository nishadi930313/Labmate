from http.server import BaseHTTPRequestHandler, HTTPServer
import os

# define the port to listen on
PORT = 4000

# define the directory to save the frames to
SAVE_DIR = './images'

# define a custom request handler that saves the received frames to disk
class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # get the filename from the URL path
        filename = self.path[1:]

        # read the frame bytes from the request body
        content_length = int(self.headers.get('Content-Length'))
        frame_bytes = self.rfile.read(content_length)

        # save the frame bytes to a file
        with open(os.path.join(SAVE_DIR, filename), 'wb') as f:
            f.write(frame_bytes)

        # send a response back to the client
        self.send_response(200)
        self.end_headers()

# create an HTTP server object and start listening for incoming requests
httpd = HTTPServer(('0.0.0.0', PORT), RequestHandler)
print('Listening on port', PORT)
httpd.serve_forever()
