from block import Block

class Pullyu(Block):

    def __init__(self, broker_port, broker_addr, name, in_streams, out_stream):
        super(Pullyu, self).__init__(broker_port, broker_addr, name, [], out_stream)

    def receive(*args):
        raise NotImplementedError