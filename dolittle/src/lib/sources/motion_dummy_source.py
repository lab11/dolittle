from ...core.source import PollingSource
import time

class MotionDummySource(PollingSource):
    def __init__(self):
        super(MotionDummySource, self).__init__()

        self.count = 0
        self.send_at = [5, 20]

        self.start_polling()

    def poll(self):
        one_second = 1
        if self.count in self.send_at:
            msg = {"type": "motion"}
            self.send(msg)
        self.count += 1
        return one_second        

if __name__ == "__main__":
    block = MotionDummySource()
    block.client.loop_forever()