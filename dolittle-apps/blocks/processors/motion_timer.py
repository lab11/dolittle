from pyblocks.processor import Processor

class MotionTimer(Processor):
	def __init__(self):
		super(MotionTimer, self).__init__()

		self.duration_secs = self.params['duration_secs']
		self.counter_secs = 0
		self.last_seen_timestamp = None
		self.enabled = False

		self.start_msg = {"type": "motion_timer", "event": "timer_started", "timer_duration_secs": self.duration_secs}
		self.timeout_msg = {"type": "motion_timer", "event": "timer_expired", "timer_duration_secs": self.duration_secs}


	def process(self, msg_json):
		if msg_json["type"] == "motion":
			self.reset()
			self.enabled = True
			self.send(self.start_msg)
		elif msg_json["type"] == "timestamp_seconds":
			if self.enabled:
				if self.last_seen_timestamp == None:
					self.last_seen_timestamp = msg_json["timestamp"]
				else:
					elapsed_time_secs = msg_json["timestamp"] - self.last_seen_timestamp
					self.last_seen_timestamp = msg_json["timestamp"]
					self.counter_secs += elapsed_time_secs
					if self.counter_secs >= self.duration_secs:
						self.send(self.timeout_msg)
						self.enabled = False
						self.reset()

	def reset(self):
		self.counter_secs = 0
		self.last_seen_timestamp = None

if __name__ == "__main__":
    block = MotionTimer()
    block.client.loop_forever()
