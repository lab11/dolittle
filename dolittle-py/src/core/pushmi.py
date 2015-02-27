from block import Block

class Pushmi(Block):

    def __init__(self, broker_port, broker_addr, name, in_streams, out_stream):
        super(Pushmi, self).__init__(broker_port, broker_addr, name, in_streams, None)

    def emit(self):
        raise NotImplementedError
