from ...core.source import PollingSource
import time

class TimestampSecondsSource(PollingSource):
    def __init__(self):
        super(TimestampSecondsSource, self).__init__()
        self.begin_polling()

    def poll(self):
        timestamp = int(time.time())
        msg = {"type": "timestamp_secs", "timestamp": timestamp}
        self.send(msg)
        time.sleep(1)
        

if __name__ == "__main__":
    block = TimestampSecondsSource()
    block.client.loop_forever()


    """
    from dolittle pkg root:
    python -m src.lib.sources.timestamp_seconds_source -name 'Timestamp in seconds' -out time/timestamps/seconds
    """