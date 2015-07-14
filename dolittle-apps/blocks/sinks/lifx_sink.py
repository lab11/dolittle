from pyblocks.sink import Sink
from lifxlan import *

class LifxSink(Sink):
    def __init__(self):
        super(LifxSink, self).__init__()
        self.mac_addr = self.params['mac_addr']
        self.ip_addr = self.params['ip_addr']

        lifxlan = LifxLAN()
        self.bulb = Light(self.mac_addr, service=1, port=56700, source_id=lifxlan.source_id, ip_addr=self.ip_addr)

        self.in_alert = False
        self.stack = {}

    def process(self, msg_json):
        msg = msg_json
        if msg["type"] == "alert" and msg["msg"] == "start_alert":
            self.in_alert = True
            self.display_alert()
        elif msg["type"] == "alert" and msg["msg"] == "cancel_alert":
            self.in_alert = False
            self.restore_stack()
        elif msg["type"] == "cmd" and msg["cmd"] == "turn_off":
            if self.in_alert:
                self.restore_stack()
            self.in_alert = False
            self.turn_off()
        elif msg["type"] == "cmd" and msg["cmd"] == "turn_on":
            if self.in_alert:
                self.in_alert = False
                self.restore_stack()
            else:
                self.in_alert = False
                self.turn_on()

    def display_alert(self):
        self.save_stack()
        self.bulb.set_color([0.6308, 0.3537])
        self.bulb.set_power("on")


    def save_stack(self):
        self.stack["power"] = self.bulb.get_power()
        self.stack['color'] = self.bulb.get_color()

    def restore_stack(self):
        self.bulb.set_color(self.stack["color"])
        self.bulb.set_power(self.stack["power"])

    def turn_on(self):
        self.bulb.set_power("on")

    def turn_off(self):
        self.bulb.set_power("off")


if __name__ == "__main__":
    block = LifxSink()
    block.client.loop_forever()

