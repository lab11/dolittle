from block import Block

class Processor(Block):
    
    def __init__(self):
        super(Processor, self).__init__()
        
        abort = False
        if len(self.in_streams) == 0:
        	print("Processors must have at least one input stream.")
        	abort = True
        if len(self.out_streams) == 0:
        	print("Processors must have an output stream.")
        	abort = True
        if abort == True:
        	sys.exit()

    def process(self, msg_json):
        raise NotImplementedError