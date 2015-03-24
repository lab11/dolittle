from block import Block

class Processor(Block):
    
    def __init__(self):
        super(Processor, self).__init__()
        
        abort = False
        if self.in_streams == None:
        	print("Processors must have at least one input stream.")
        	abort = True
        if self.out_stream == None:
        	print("Processors must have an output stream.")
        	abort = True
        if abort == True:
        	sys.exit()

    def process(self, obj):
        raise NotImplementedError