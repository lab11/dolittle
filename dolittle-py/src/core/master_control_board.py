from ..core.processor import Processor

class MasterControlBoard(Block):
	def __init__(self):
        super(Processor, self).__init__()

	def process(self, obj):
		new_obj = str(obj)

if __name__ == "__main__":
	mcb = MasterControlBoard()
	name = mcb.name
	mcb.in_streams = ['{0}/mcb/in'.format(name)]
	mcb.out_stream = '{0}/mcb/status'.format(name)
    mcb.client.loop_forever()