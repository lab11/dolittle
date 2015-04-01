from ..core.processor import Processor

class MasterControlBoard(Block):
	def __init__(self):
        super(Processor, self).__init__()

	def process(self, msg_json):
		mag = msg_json
		if msg["type"] == "control":
			# for block in blocks, instantiate.
			# send status
			blocks = msg["blocks"]
			
		elif msg["type"] == "request":
			if msg["request"] == "available_streams":
				pass
			elif msg["request"] == "stream_schema":
				pass
			elif msg["request"] == "available_devices":
				pass
			elif msg["request"] == "available_locations":
				pass

if __name__ == "__main__":
	mcb = MasterControlBoard()
	name = mcb.name
	mcb.in_streams = [name + '/dolittle/apps']
	mcb.out_streams = [name + '/dolittle/status']
    mcb.client.loop_forever()