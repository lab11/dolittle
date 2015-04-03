from pyblocks.processor import Processor

class AutoShutoff(Processor):
	def __init__(self):
		super(AutoShutoff, self).__init__()

		self.in_alert = False

		self.alert = {"type": "alert", "msg": "start_alert"}
		self.cancel_alert = {"type": "alert", "msg": "cancel_alert"}
		self.turn_on = {"type": "cmd", "cmd": "turn_on"}
		self.turn_off = {"type": "cmd", "cmd": "turn_off"}

	def process(self, msg_json):
		if msg_json["type"] == "motion_timer" and msg_json["event"] == "timer_expired":
			self.in_alert = True
			self.send(self.alert)

		elif msg_json["type"] == "motion_timer" and msg_json["event"] == "timer_started":
			if self.in_alert:
				self.in_alert = False
				self.send(self.cancel_alert)
			else:
				self.send(self.turn_on)

		elif msg_json["type"] == "alert_timer" and msg_json["event"] == "timer_expired":
			self.in_alert = False
			self.send(self.turn_off)

if __name__ == "__main__":
    block = AutoShutoff()
    block.client.loop_forever()