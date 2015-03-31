from pyblocks.source import Source
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi, urlparse
import re
import thread
import json

class HTTPSource(Source):
    def __init__(self):
        super(HTTPSource, self).__init__()
        self.hostname = self.params["host"]
        self.port = self.params["port"]
        self.server = HTTPServer((self.hostname, self.port), HTTPRequestHandler)
        try:
            #in new thread
            thread.start_new_thread(self.server.serve_forever, ())
        except KeyboardInterrupt:
            self.server.server_close()

class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        print("Got a POST!")
        if None != re.search('/ninjablocks/rf', self.path):
            content_type, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if content_type == 'application/json':
                length = int(self.headers.getheader('content-length'))
                data = urlparse.parse_qs(self.rfile.read(length), keep_blank_values=1).keys()[0]
                data_json = json.loads(data)
                self.send(data_json)
                self.send_response(200)
                self.end_headers()
            else:
                self.send_response(403)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
        elif None != re.search('/ubi/*', self.path):
            pass


    def do_GET(self):
        self.send_response(403)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()


if __name__ == "__main__":
    block = HTTPSource()
    block.client.loop_forever()