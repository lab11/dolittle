from ..core.processor import Processor

class MasterControlBoard(Block):
	def __init__(self):
        super(Processor, self).__init__()

	def process(self, obj):
		new_obj = str(obj)
		# if msg_type == app:
			# for block in blocks, instantiate.
			# send status
		# if msg_type == status_request:
			# send status

if __name__ == "__main__":
	mcb = MasterControlBoard()
	name = mcb.name
	mcb.in_streams = [name + '/dolittle/apps']
	mcb.out_streams = [name + '/dolittle/status']
    mcb.client.loop_forever()