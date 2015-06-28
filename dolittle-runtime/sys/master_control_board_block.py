import paho.mqtt.client as mqtt
import thread
import time
import re
from sys import argv, exit
import json
from pattern.en import singularize, pluralize
from copy import copy

class MCBBlock(object):
    #def __init__(self, name = None, in_streams = None, out_streams = None, broker_port = 1883, broker_addr = 'localhost'):
    def __init__(self):
        # Defaults    
        self.receive_buffer = []
        self.send_buffer = []
        self.in_streams = []
        self.out_streams = []
        self.params = "" #JSON blob

        # MQTT connection
        self.connected = False
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.receive

    def start_messaging_interface(self):
        self.client.connect(self.broker_addr)
        while(self.connected == False):
            self.client.loop()
            time.sleep(0.1)

        thread.start_new_thread(self.emit_loop, ())
        thread.start_new_thread(self.process_loop, ())

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            print(self.name + ": connected " + str(client))
            for in_stream in self.in_streams:
                client.subscribe(in_stream, 2)
        else:
            print(str(rc))

    def on_publish(self, client, userdata, mid):
        #print(self.name + ": published mid: "+str(mid))
        pass

    def on_subscribe(self, client, userdata, mid, granted_qos):
        #print("Subscribed: "+str(mid)+" "+str(granted_qos))
        pass

    def on_log(self, client, userdata, level, buf):
        #print(string)
        pass

    ############# DOLITTLE ################

    #def receive(self, client, userdata, msg):
    def receive(self, *args):
        #on message, add to queue safely
        client, userdata, msg = args
        # not sure if this is the right place for this, since
        # source/sink/processors have different semantic requirements for subscriptions
        """if msg.payload.title == 'subscribe':
            pass
        elif msg.payload.title == 'unsubscribe':
            pass
        else:
            self.receive_buffer.append(msg.payload)"""
        msg_str = str(msg.payload)
        msg_json = json.loads(msg_str)
        self.receive_buffer.append(msg_json)


    def process_loop(self):
        while(True):
            if len(self.receive_buffer) > 0:
                msg = self.receive_buffer.pop(0)
                self.process(msg)
            time.sleep(0.1)

    def process(self, obj):
        raise NotImplementedError

    def emit_loop(self):
        while(True):
            if len(self.send_buffer) > 0:
                self.emit()
            time.sleep(0.1)

    def emit(self):
        msg = self.send_buffer.pop(0)
        msg_json = json.loads(msg)
        msg_type = msg_json["type"] if "type" in msg else None
        at_least_one_match = False
        for out_stream in self.out_streams:
            if self.matches_end(msg_type, out_stream):
                at_least_one_match = True
                final_msg = copy(msg_json)
                final_msg["stream"] = out_stream
                self.client.publish(out_stream, json.dumps(final_msg))
                print("published " + str(final_msg))
        if at_least_one_match == False:
            #then send to all
            for out_stream in self.out_streams:
                final_msg = copy(msg_json)
                final_msg["stream"] = out_stream
                self.client.publish(out_stream, json.dumps(final_msg))
                print("published " + str(final_msg))


    def matches_end(self, msg_type, stream_name):
        if msg_type != None:
            topic_path = msg_type.split("/")
            front_matter = topic_path[:-1]
            last_word = topic_path[-1]
            singular = singularize(last_word)
            plural = pluralize(singular)
            msg_type_singular = "/".join(front_matter + [singular])
            msg_type_plural = "/".join(front_matter + [plural])
            patterns = [msg_type_plural + "$", msg_type_singular + "$"]
        else:
            patterns = [".*"]
        is_match = False
        for pattern in patterns:
            if None != re.search(pattern, stream_name):
                is_match = True
        return is_match

    def send(self, msg):
        msg = self.validate(msg)
        self.send_buffer.append(msg)

    # this should validate JSON eventually
    # might push to library to define msgs
    def validate(self, msg):
        if type(msg) == type(""):
            string_msg = msg
        else:
            string_msg = json.dumps(msg)
        return string_msg


