from pyblocks.sink import Sink
from phue import Bridge, PhueRegistrationException
import sys
import random
import socket
from time import sleep

class HueBulbSink(Sink):
    def __init__(self):
        super(HueBulbSink, self).__init__()

        self.bridge_addr = self.params['bridge_addr']
        self.bulb_name = str(self.params['bulb_name'])
        try:
            scene_file = str(self.params['scene_file'])
        except KeyError:
            scene_file = None

        success = False
        while not success:
            try:
                self.bridge = Bridge(self.bridge_addr)
                light_objects_dict = self.bridge.get_light_objects('name')
                try:
                    self.bulb = light_objects_dict[self.bulb_name]
                except KeyError:
                    print("Unknown bulb name. Here is the list of available bulbs at bridge " + self.bridge_addr + ":")
                    print(light_objects_dict.keys())
                    sys.exit()

                self.bulb_scenes = None
                if scene_file != None:
                    with open(scene_file) as sf:
                        all_scenes = json.load(sf)
                        self.bulb_scenes =  all_scenes[self.bulb_name.lower().replace(' ', '_')]
                success = True
            except socket.error:
                sleep(random.random())
            except PhueRegistrationException:
                print(str(self.name) + ": The link button has not been pressed in the last 30 seconds. Trying again in 10 seconds.")
                sleep(10)
        print(str(self.name) + ": Connected to Hue bulb.")

        self.in_alert = False
        self.stack = {}

    def process(self, msg_json):
        msg = msg_json
        if "alert" in msg["type"] and msg["msg"] == "start_alert":
            self.in_alert = True
            self.display_alert()
        elif "alert" in msg["type"] and msg["msg"] == "cancel_alert":
            self.in_alert = False
            self.restore_stack()
        elif "cmd" in msg["type"] and msg["cmd"] == "turn_off":
            if self.in_alert:
                self.restore_stack()
            self.in_alert = False
            self.turn_off()
        elif "cmd" in msg["type"] and msg["cmd"] == "turn_on":
            if self.in_alert:
                self.in_alert = False
                self.restore_stack()
            else:
                self.in_alert = False
                self.turn_on()

    def display_alert(self):
        success = False
        while not success:
            try:
                self.save_stack()
                self.bulb.xy = [0.6308, 0.3537] 
                self.bulb.brightness = 100
                success = True
            except socket.error:
                sleep(random.random())

    def save_stack(self):
        success = False
        while not success:
            try:
                self.stack["xy"] = self.bulb.xy
                self.stack["brightness"] = self.bulb.brightness
                success = True
            except socket.error:
                sleep(random.random())

    def restore_stack(self):
        success = False
        while not success:
            try:
                self.bulb.xy = self.stack["xy"]
                self.brightness = self.stack["brightness"]
                success = True
            except socket.error:
                sleep(random.random())

    def turn_on(self):
        success = False
        while not success:
            try:
                if self.bulb_scenes == None:
                    self.bulb.on = True
                    self.bulb.xy = [0.4609, 0.4108]
                    self.brightness = 254
                    #scene = self.bulb_scenes["daylight"]
                    success = True
            except socket.error:
                sleep(random.random())

    def turn_off(self):
        success = False
        while not success:
            try:
                self.bulb.on = False
                success = True
            except socket.error:
                sleep(random.random())


if __name__ == "__main__":
    block = HueBulbSink()
    block.client.loop_forever()

    """
    from dolittle pkg root:
    python -m src.lib.sinks.hue_bulb_sink -name 'Hue Bulb Dummy' -in livingroom/lights/cmds:hue/lights/cmds -params '{"bridge_addr": "10.0.0.225","bulb_name": "Fan front"}'
    """

