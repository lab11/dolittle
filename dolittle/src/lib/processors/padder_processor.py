from ..core.pushmi_pullyu import Pushmi_Pullyu

class Padder(Pushmi_Pullyu):
	def __init__(self, broker_port, broker_addr, name, in_streams, out_stream):
		super(Padder, self).__init__(broker_port, broker_addr, name, in_streams, out_stream)

	def process(self, obj):
		new_obj = str(obj) + "000000"
		self.send(new_obj)

if __name__ == "__main__":
    block = Padder(1883, 'localhost', 'Padder_test', ['test_in'], 'test_out')
    block.client.loop_forever()
