import paho.mqtt.client as mqtt
import thread
import time
from sys import argv, exit
import json

class Block(object):
    #def __init__(self, name = None, in_streams = None, out_streams = None, broker_port = 1883, broker_addr = 'localhost'):
    def __init__(self):
        # Defaults    
        self.name = None
        self.receive_buffer = []
        self.send_buffer = []
        self.in_streams = []
        self.out_streams = []
        self.broker_port = 1883
        self.broker_addr = 'localhost'
        self.params = "" #JSON blob

        # Get actual params from cmd line
        self.configure_with_cmd_line_args()

        # MQTT connection
        self.connected = False
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.receive
        self.client.connect(self.broker_addr)

        while(self.connected == False):
            self.client.loop()
            time.sleep(0.1)

        thread.start_new_thread(self.emit_loop, ())
        thread.start_new_thread(self.process_loop, ())

    def configure_with_cmd_line_args(self):
            program_file = argv.pop(0) # don't need
            while len(argv) > 0:
                arg = argv.pop(0)
                if arg == '-name' or arg == '-n':
                    self.name = argv.pop(0)
                elif arg == '-in' or arg == '-i':
                    in_streams = argv.pop(0).split(':')
                    self.in_streams = in_streams
                elif arg == '-out' or arg == '-o':
                    out_streams = argv.pop(0).split(':')
                    self.out_streams = out_streams
                elif arg == '-port' or arg == '-p':
                    port = int(argv.pop(0))
                    self.broker_port = port
                elif arg == '-host' or arg == '-h':
                    self.broker_addr = argv.pop(0)
                elif arg == '-params':
                    self.params = json.loads(argv.pop(0)) # convert string to JSON
                else:
                    print("Unknown argument: {0}".format(arg))
            if self.name == None:
                print("The -name or -n flag is required to name this block.")
                exit()
     #   except:
     #       print()
     #       print("Problem with command-line argument format.")
     #       exit()

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
        self.send_buffer.append(obj)

    def emit_loop(self):
        while(True):
            if len(self.send_buffer) > 0:
                self.emit()
            time.sleep(0.1)

    def emit(self):
        msg = self.send_buffer.pop(0)
        for out_stream in self.out_streams:
            self.client.publish(out_stream, msg)
        print("published " + str(msg))

    def send(self, msg):
        msg = self.validate(msg)
        self.send_buffer.append(msg)

    # this should validate JSON eventually
    # might push to library to define msgs
    def validate(self, msg):
        return json.dumps(msg)


if __name__ == "__main__":
    p = Processor()
    p.client.loop_forever()


