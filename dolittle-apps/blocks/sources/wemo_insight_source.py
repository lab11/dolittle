from pyblocks.source import PollingSource
import socket

class WemoInsightSource(PollingSource):
    def __init__(self):
        super(WemoInsightSource, self).__init__()

        self.ip_addr = str(self.params['ip_addr'])
        self.device_name = str(self.params['device_name']) if 'device_name' in self.params else "Unknown"
        self.poll_rate_secs = self.params['poll_rate'] if 'poll_rate' in self.params else 2

        self.lowest_port = 49152
        self.highest_port = 49158

        self.header = """POST /upnp/control/{command_type}1 HTTP/1.1
SOAPACTION: "urn:Belkin:service:{command_type}:1#{command}"
Content-Length: {length}
Content-Type: text/xml; charset="utf-8"
HOST: {ipaddr}:{port}
User-Agent: CyberGarage-HTTP/1.0"""

        self.get_body = """<?xml version="1.0" encoding="utf-8"?>
<s:Envelope xmlns:s="http://schemas.xmlsoap.org/soap/envelope/" \
s:encodingStyle="http://schemas.xmlsoap.org/soap/encoding/">
 <s:Body>
  <u:{command} xmlns:u="urn:Belkin:service:{command_type}:1">
  </u:{command}>
 </s:Body>
</s:Envelope>
"""
        self.start_polling()

    def poll(self):
        status = self.get_insight_status()
        print(status)
        self.send(status)
        return self.poll_rate_secs

    def get_insight_status(self):
        tag = 'InsightParams'
        start_tag = '<' + tag + '>'
        end_tag = '</' + tag + '>'
        response = self.get_state('insight', 'GetInsightParams')
        start_index = response.index(start_tag) + len(start_tag)
        end_index = response.index(end_tag)
        status = self.process_insight_status_string(response[start_index:end_index])
        status['ip_addr'] = self.ip_addr
        status['port'] = self.current_port
        status['device_name'] = self.device_name
        status['device_type'] = 'Wemo Insight'
        return status
        #return response

    # 'GetInsightParams' returns something like:
    # 1|1427230660|4702|25528|82406|1209600|39|40880|15620649|54450534.000000|8000
    # 1. State (0 = off, 1 = on)
    # 2. Unix timestamp of last time it changed state (If on, when it was turned on. If off, last time it was on.)
    # 3. Seconds it has been on for since being turned on (0 if off)
    # 4. Seconds it has been on today
    # 5. Number of seconds it has been on over the past two weeks. Used for the Wemo app's average time on per day calculation.
    # 6. Constant between different insights: 1209600. This is two weeks in seconds. Used for the Wemo app's average time on per day calculation.
    # 7. Average power (W)
    # 8. InstantPower (mW)
    # 9. Energy used today in mW-minutes
    # 10. Energy used over the last two weeks in mW-minutes
    # 11. Unknown, constant between different insights: 8000
    def process_insight_status_string(self, status_str):
        status_str = str(status_str)
        status = {}
        fields = status_str.split('|')
        status['is_on'] = (int(fields[0]) == 1)
        status['last_transition_timestamp'] = fields[1]
        status['on_for_secs'] = fields[2]
        status['on_today_for_secs'] = fields[3]
        status['on_over_time_window_for_secs'] = fields[4]
        status['time_window_secs'] = fields[5]
        status['average_power_watts'] = fields[6]
        status['instant_power_watts'] = float(fields[7])/1000
        status['energy_used_today_watthour'] = (float(fields[8])/1000)/60 #FINISH
        status['energy_used_over_time_window_watthour'] = (float(fields[9])/1000)/60
        return status

    def get_state (self, cmd_type, cmd):
        response = ''
        for port in range(self.lowest_port, self.highest_port):
            wemo_socket, success = self.connect(port)
            if success:
                self.current_port = port
                soap_body = self.get_body.format(command_type=cmd_type, command=cmd)
                soap_header = self.header.format(command_type=cmd_type, command=cmd,
                    length=len(soap_body),
                    ipaddr=self.ip_addr,
                    port=self.current_port)
                soap_header = soap_header.replace('\n', '\r\n')
                soap = soap_header + '\r\n\r\n' + soap_body
                wemo_socket.send(soap.encode())
                while True:
                    data = wemo_socket.recv(1024)
                    response += data.decode()
                    if '</s:Envelope>' in response:
                        break
                wemo_socket.close()
        return response

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
    block = WemoInsightSource()
    block.client.loop_forever()

    """
    from dolittle pkg root:
    python -m src.lib.sources.wemo_insight_source -name 'Wemo Dummy' -out livingroom/lights:livingroom/wemo:wemo -params '{"ip_addr": "10.0.0.17", "device_name": "Flea"}'
    """
    # 17 (Flea), 145 (Bee), 229 (Caterpillar)

    # host send 2 insight basicevent GetBinaryState, SetBinaryState
    # host send 2 insight insight GetInsightParams -- GetPower, GetTodayKWH, GetTodayONTime, GetONFor return None