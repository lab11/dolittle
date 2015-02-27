from block import Block

class Pushmi_Pullyu(Block):
    
    def __init__(self, broker_port, broker_addr, name, in_streams, out_stream):
        super(Pushmi_Pullyu, self).__init__(broker_port, broker_addr, name, in_streams, out_stream)

    def process(self, obj):
        raise NotImplementedError