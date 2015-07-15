from pyblocks.processor import Processor

class GhostingApp(Processor):
	def __init__(self):
		super(GhostingApp, self).__init__()

		# for sending to other house
		self.out_off = {"type": "out", "room": "", "cmd": "turn_off"}
		self.out_on = {"type": "out", "room": "", "cmd": "turn_on"}

		last_cmds = {}
		last_state = {}

	def process(self, msg_json):
		msg = msg_json
		if msg['stream'] == 'ghosting/in':
			room = msg['room']
			cmd = msg['cmd']
			control_msg = {"type": room+"/lights/cmds", "cmd": cmd}
			last_cmds['room'] = cmd
			self.send(control_msg)

		elif "/lights/status" in msg['stream']:
			room = msg['stream'].split('/')[0]
			device_name = msg["name"]
			current_power_state = msg["on"]
			if device_name not in last_state:
				last_state[device_name] = current_power_state
			if current_power_state != last_state[device_name]:
				if room in last_cmds:
					if last_cmds[room] == "turn_on" and current_power_state == off:
						state_change = True
						last_state[device_name] = current_power_state
					elif last_cmds[room] == "turn_off" and current_power_state == on:
						state_change = True
						last_state[device_name] = current_power_state
				else:
					state_change = True
					last_state[device_name] = current_power_state
			if state_change:
				ghost_msg = self.out_on if current_power_state == True else self.out_off
				ghost_msg['room'] = room
				self.send(ghost_msg)

if __name__ == "__main__":
    block = GhostingApp()
    block.client.loop_forever()