from block import Block
import thread
from time import sleep

class Source(Block):

    def __init__(self):
        super(Source, self).__init__()

        if len(self.out_streams) == 0:
            print("Sources must have an output stream.")
            sys.exit()

    # Sources only send to msg broker, they don't receive from it.
    # Receive is not - and shouldn't be - defined for a source.
    # If you need to send and receive from MQTT msg queues, then you want a processor.
    def receive(*args):
        raise NotImplementedError


# Important! All PollingSource classes must call self.begin_polling() at the end of their inits to begin polling.
class PollingSource(Source):

    def __init__(self):
        super(PollingSource, self).__init__()
        self.initialized = False
        thread.start_new_thread(self.polling_loop, ())

    def start_polling(self):
        self.initialized = True

    def polling_loop(self):
        while(True):
            if self.initialized:
                poll_interval = self.poll()
                if poll_interval == None:
                    poll_interval = 1
                sleep(poll_interval)

    def poll(self):
        raise NotImplementedError