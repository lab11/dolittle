import paho.mqtt.client as mqtt
import thread
import time

class Block(object):
    def __init__(self, broker_port, broker_addr, name, in_streams, out_stream):
        self.name = name
        self.receive_buffer = []
        self.send_buffer = []
        self.in_streams = in_streams
        self.out_stream = out_stream

        # MQTT connection
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.receive
        self.client.connect(broker_addr)

        thread.start_new_thread(self.emit_loop, ())
        thread.start_new_thread(self.process_loop, ())

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(self.name + ": connected " + str(client))
            for in_stream in self.in_streams:
                client.subscribe(in_stream, 2)
        else:
            print(str(rc))

    def on_publish(self, client, userdata, mid):
        print(self.name + ": published mid: "+str(mid))

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
        self.receive_buffer.append(msg.payload)

    def process_loop(self):
        while(True):
            if len(self.receive_buffer) > 0:
                msg = self.receive_buffer.pop(0)
                self.process(msg)
            time.sleep(1)

    def process(self, obj):
        self.send_buffer.append(obj)

    def emit_loop(self):
        while(True):
            if len(self.send_buffer) > 0:
                self.emit()
            self.client.loop()
            time.sleep(1)

    def emit(self):
        msg = self.send_buffer.pop(0)
        self.client.publish(self.out_stream, msg)
        print("published " + str(msg))

    def send(self, msg):
        self.send_buffer.append(msg)


if __name__ == "__main__":
    pp = Pushmi_Pullyu(1883, 'localhost', 'Dummy', ['test_in'], 'test_out')
    pp.client.loop_forever()


