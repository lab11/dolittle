from pyblocks.sink import Sink
import socket

class WemoInsightSink(Sink):
    def __init__(self):
        super(WemoInsightSink, self).__init__()

        self.ip_addr = str(self.params['ip_addr'])
        self.device_name = str(self.params['device_name']) if 'device_name' in self.params else "Unknown"

        self.lowest_port = 49152
        self.highest_port = 49158

        self.header = """POST /upnp/control/{command_type}1 HTTP/1.1
SOAPACTION: "urn:Belkin:service:{command_type}:1#{command}"
Content-Length: {length}
Content-Type: text/xml; charset="utf-8"
HOST: {ipaddr}:{port}
User-Agent: CyberGarage-HTTP/1.0"""

        self.set_body = """<?xml version="1.0" encoding="utf-8"?>
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" \
s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
 <s:Body>
  <u:SetBinaryState xmlns:u="urn:Belkin:service:basicevent:1">
   <BinaryState>{binstate}</BinaryState>
  </u:SetBinaryState>
 </s:Body>
</s:Envelope>
"""

    def process(self, msg_json):
        msg = msg_json
        if "cmd" in msg["type"]:
            if msg["cmd"].lower() in ["turn_off", "turn off"]:
                self.turn_off()
            elif msg["cmd"].lower() in ["turn_on", "turn on"]:
                self.turn_on()

    def turn_on(self):
        self.set_state('SetBinaryState', '1')

    def turn_off(self):
        self.set_state('SetBinaryState', '0')

    # change to set body, also get port logic
    def set_state(self, cmd, state):
        for port in range(self.lowest_port, self.highest_port):
            wemo_socket, success = self.connect(port)
            if success:
                self.current_port = port
                soap_body = self.set_body.format(binstate=state)
                soap_header = self.header.format(command_type="basicevent",
                    command=cmd,
                    length=len(soap_body),
                    ipaddr=self.ip_addr,
                    port=self.current_port)
                soap_header = soap_header.replace('\n', '\r\n')
                soap = soap_header + '\r\n\r\n' + soap_body
                wemo_socket.send(soap.encode())
                wemo_socket.close()

    def connect (self, port):
        connection_attempts = 0
        max_connection_attempts = 2
        connected = False
        wemo_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        while connection_attempts < max_connection_attempts:
            try:
                wemo_socket.connect((self.ip_addr, port))
                connected = True
                break
            except OSError:
                connection_attempts += 1
            except socket.timeout:
                connection_attempts += 1
            except socket.error:
                break
        return wemo_socket, connected

if __name__ == "__main__":
    block = WemoInsightSink()
    block.client.loop_forever()