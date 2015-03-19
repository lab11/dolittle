import paho.mqtt.client as mqtt
import thread
import time
from sys import argv, exit

class Block(object):
    def __init__(self):

    #def __init__(self, name = None, in_streams = None, out_stream = None, broker_port = 1883, broker_addr = 'localhost'):
    def __init__(self):
        # Defaults    
        self.name = None
        self.receive_buffer = []
        self.send_buffer = []
        self.in_streams = None
        self.out_stream = None
        self.broker_port = 1883
        self.broker_addr = 'localhost'

        # Get actual params
        self.configure_with_cmd_line_args()

        # MQTT connection
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.on_subscribe = self.on_subscribe
        self.client.on_message = self.receive
        self.client.connect(broker_addr)

        thread.start_new_thread(self.emit_loop, ())
        thread.start_new_thread(self.process_loop, ())

    def configure_with_cmd_line_args():
        try:
            for (i, arg) in enumerate(argv):
                if arg == '-name' or arg == '-n':
                    self.name = argv[i+1]
                elif arg == '-in' or arg == '-i':
                    in_streams = argv[i+1].split(':')
                    self.in_streams = in_streams
                elif arg == '-out' or arg == '-o':
                    out_stream = argv[i+1]
                    self.out_stream = out_stream
                elif arg == '-port' or arg == '-p':
                    port = int(argv[i+1])
                    self.broker_port = port
                elif arg == '-host' or arg == '-h':
                    self.broker_addr = argv[i+1]
                else:
                    print("Unknown argument: {0}".format(arg))
            if self.name == None:
                print("The -name or -n flag is required to name this block.")
                sys.exit()
        except:
            print("Problem with command-line argument format.")
            sys.exit()

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
    p = Processor()
    p.client.loop_forever()


