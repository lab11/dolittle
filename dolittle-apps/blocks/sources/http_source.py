from pyblocks.source import Source
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi, urlparse
import re
import thread
import json

class HTTPSource(Source):
    def __init__(self, *argsfghjhk):
        #super(HTTPSource, self).__init__()
        Source.__init__(self)
        self.hostname = self.params["host"]
        self.port = self.params["port"]

        HTTPRequestHandler.send = self.send

        self.server = HTTPServer((self.hostname, self.port), HTTPRequestHandler)
        #self.server = HTTPServer((self.hostname, self.port), HTTPSource)
        try:
            #in new thread
            thread.start_new_thread(self.server.serve_forever, ())
        except KeyboardInterrupt:
            self.server.server_close()

class HTTPRequestHandler(BaseHTTPRequestHandler):

    def __init__(self, *args):
        self.motion = {"type": "motion"}
        self.lights_on = {"type": "cmd", "cmd": "turn_on"}
        self.light_off = {"type": "cmd", "cmd": "turn_off"}
        self.chat_msg = {"type": "chat", "response": ""}
        BaseHTTPRequestHandler.__init__(self, *args)

    def do_POST(self):
        print("Got a POST!")
        content_type, pdict = cgi.parse_header(self.headers.getheader('content-type'))
        if content_type == 'application/json':
            if None != re.search('/ninjablocks/rf', self.path):
                    length = int(self.headers.getheader('content-length'))
                    data = urlparse.parse_qs(self.rfile.read(length), keep_blank_values=1).keys()[0]
                    data_json = json.loads(data)
                    print(data_json)
                    self.send(self.motion)
                    self.send_response(200)
                    self.end_headers()
            elif None != re.search('ubi', self.path):
                if None != re.search('/livingroom/ubi/turn_off_lights', self.path):
                    self.send(self.light_off)
                    self.send_response(200)
                    self.end_headers()
                elif None != re.search('/livingroom/ubi/turn_on_lights', self.path):
                    self.send(self.lights_on)
                    self.send_response(200)
                    self.end_headers()
                elif None != re.search('/livingroom/ubi/chat', self.path): 
                    print(self.path)
                    parts = urlparse.urlparse(self.path)
                    qs = urlparse.parse_qs(parts.query)
                    self.chat_msg["response"] = qs['say'][0] 
                    print(self.chat_msg)
                    self.send(self.chat_msg)
                    self.send_response(200)
                    self.end_headers()
                else:
                    self.send_response(403)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
        else:
            self.send_response(403)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()

    def do_GET(self):
        self.send_response(403)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

if __name__ == "__main__":
    block = HTTPSource()
    try:
        block.client.loop_forever()
    except KeyboardInterrupt:
        block.server.server_close()