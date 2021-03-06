from pyblocks.source import PollingSource
import socket
import json

BUFFER_SIZE = 1024  # Normally 1024, but we want fast response

class SocketSource(PollingSource):
    def __init__(self, *args):
        super(SocketSource, self).__init__()
        self.TCP_IP = self.params['host']
        self.TCP_PORT = self.params['port']
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind((self.TCP_IP, self.TCP_PORT))
        self.s.listen(1)

        self.start_polling()

    def poll(self):
        print("listening...")
        self.conn, addr = self.s.accept()
        print("accepted...")
        while 1:
            data = self.conn.recv(BUFFER_SIZE)
            if not data: break
            try:
                self.send(json.loads(data))
            except:
                print("Received non-JSON data from {}: {}".format(addr, data))
        self.conn.close()
        #self.s.close()
        return 0


if __name__ == "__main__":
    block = SocketSource()
    try:
        block.client.loop_forever()
    except KeyboardInterrupt:
        try:
            block.conn.close()
        except:
            pass
