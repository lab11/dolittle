from ...core.source import PollingSource
from phue import Bridge
from time import sleep
import sys

class HueBulbSource(PollingSource):
    def __init__(self):
        super(HueBulbSource, self).__init__()
        self.bridge_addr = self.params['bridge_addr']
        self.bulb_name = str(self.params['bulb_name'])
        self.poll_rate_secs = self.params['poll_rate'] if 'poll_rate' in self.params else 2

        self.bridge = Bridge(self.bridge_addr)
        light_objects_dict = self.bridge.get_light_objects('name')
        try:
            self.bulb = light_objects_dict[self.bulb_name]
        except KeyError:
            print("Unknown bulb name. Here is the list of available bulbs at bridge " + self.bridge_addr + ":")
            print(light_objects_dict.keys())
        # self.bulb_id = self.bulb.light_id
        self.start_polling() #must call begin polling at end of polling source init function  

    def poll(self):
        state = {'bridge': self.bridge_addr, 'name': self.bulb_name}
        state['on'] = self.bulb.on
        state['hue'] = self.bulb.hue
        state['saturation'] = self.bulb.saturation
        state['brightness'] = self.bulb.brightness
        state['transitiontime'] = self.bulb.transitiontime
        state['colormode'] = self.bulb.colormode
        state['xy'] = self.bulb.xy
        state['alert'] = self.bulb.alert
        state['transitiontime'] = self.bulb.transitiontime
        try:
            state['colortemp'] = self.bulb.colortemp
        except KeyError:
            pass # lightstrips have no colortemp
        self.send(state)
        return self.poll_rate_secs



if __name__ == "__main__":
    block = HueBulbSource()
    block.client.loop_forever()

    """
    from dolittle pkg root:
    python -m src.lib.sources.hue_bulb_source -name 'Hue Bulb Dummy' -out livingroom/lights:hue/lights -params '{"bridge_addr": "10.0.0.225","bulb_name": "Fan front"}'
    """

