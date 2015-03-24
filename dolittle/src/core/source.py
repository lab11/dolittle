from block import Block

class Source(Block):

    def __init__(self):
        super(Source, self).__init__()

        if self.out_stream == None:
        	print("Sources must have an output stream.")
        	sys.exit()

    def receive(*args):
        raise NotImplementedError