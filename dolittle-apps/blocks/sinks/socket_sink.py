from pyblocks.sink import Sink
import socket
import json

BUFFER_SIZE = 1024

class SocketSink(Sink):
    def __init__(self):
        super(SocketSink, self).__init__()
        self.dest = self.params['dest']
        self.port = self.params['port']

    def process(self, msg_json):
        print("sending...")
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect((self.dest, self.port))
        self.s.send(json.dumps(msg_json))
        self.s.close()
        print("done...")

if __name__ == "__main__":
    block = SocketSink()
    block.client.loop_forever()

