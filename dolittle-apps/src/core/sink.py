from block import Block

class Sink(Block):

    def __init__(self):
        super(Sink, self).__init__()

        if len(self.in_streams) == 0:
        	print("Sinks must have at least one input stream.")
        	sys.exit()

    def process(self, msg_json):
    	raise NotImplementedError

    def emit(self):
        raise NotImplementedError
