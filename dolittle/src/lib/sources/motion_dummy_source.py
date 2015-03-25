from ...core.source import PollingSource
import time

class MotionDummySource(PollingSource):
    def __init__(self):
        super(MotionDummySource, self).__init__()

        self.count = 0
        self.send_at = [5, 20]

        self.begin_polling()

    def poll(self):
        if self.count in self.send_at:
            msg = {"type": "motion"}
            self.send(msg)
        self.count += 1
        time.sleep(1)
        

if __name__ == "__main__":
    block = MotionDummySource()
    block.client.loop_forever()