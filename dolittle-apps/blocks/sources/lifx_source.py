from pyblocks.source import PollingSource
from lifxlan import *

class LifxSource(PollingSource):
    def __init__(self):
        super(LifxSource, self).__init__()
        self.mac_addr = self.params['mac_addr']
        self.ip_addr = self.params['ip_addr']

        lifxlan = LifxLAN()
        self.bulb = Light(self.mac_addr, service=1, port=56700, source_id=lifxlan.source_id, ip_addr=self.ip_addr)

        self.poll_rate_secs = 1
        self.start_polling() #must call start polling at end of polling source init function  

    def poll(self):
        state = {'name': self.bulb.get_label().replace('\x00', ''), 'mac_addr': self.mac_addr}
        state['ip_addr'] = self.ip_addr
        state['on'] = True if self.bulb.get_power() > 0 else False
        hue, saturation, brightness, kelvin = self.bulb.get_color()
        state['hue'] = hue
        state['saturation'] = saturation
        state['brightness'] = brightness
        state['kelvin'] = kelvin
        msg = state
        msg["type"] = "status"
        self.send(msg)
        return self.poll_rate_secs


if __name__ == "__main__":
    block = LifxSource()
    block.client.loop_forever()
