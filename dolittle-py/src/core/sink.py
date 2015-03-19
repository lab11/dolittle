from block import Block

class Sink(Block):

    def __init__(self):
        super(Sink, self).__init__()

        if self.in_streams == None:
        	print("Sinks must have at least one input stream.")
        	sys.exit()

    def emit(self):
        raise NotImplementedError
