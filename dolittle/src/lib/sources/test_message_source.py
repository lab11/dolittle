from ...core.source import PollingSource
from time import sleep

class TestMessageSource(PollingSource):
    def __init__(self):
        super(TestMessageSource, self).__init__()

        self.test_message = self.params["message"]
        self.delay_secs = 0
        if "delay_secs" in self.params:
            self.delay_secs = self.params["delay_secs"]

        self.counter = 0
        self.begin_polling()

    def poll(self):
        if self.counter == self.delay_secs:
            self.send(self.test_message)
        self.counter += 1
        sleep(1)
        #return 1

if __name__ == "__main__":
    block = TestMessageSource()
    block.client.loop_forever()