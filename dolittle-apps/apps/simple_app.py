import paho.mqtt.client as mqtt
import json
from sys import argv, exit

class SimpleApp(object):
    def __init__(self):
        self.name = "SimpleApp"
        self.broker_port = 1883
        self.broker_addr = 'localhost'
        self.app_json = None
        self.get_app_json()
        self.msg = json.dumps({"type": "control", "app": self.app_json})

        # MQTT connection
        self.connected = False
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.connect(self.broker_addr)

    def get_app_json(self):
        if len(argv) > 1:
            json_file = argv[1]
            with open(json_file) as data_file:    
                self.app_json = json.load(data_file)
            self.name = self.app_json["app_name"]
        else:
            print("Please provide json file containing app specification.")
            exit()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            print(self.name + ": connected " + str(client))
            self.client.publish("dolittle/apps", self.msg)
        else:
            print(str(rc))

    def on_publish(self, client, userdata, mid):
        print(self.name + ": sent app to MCB")
        exit()
        
if __name__=="__main__":
    app = SimpleApp()
    app.client.loop_forever()