from ...core.source import PollingSource
import time

class TimestampSecondsSource(PollingSource):
    def __init__(self):
        super(TimestampSecondsSource, self).__init__()
        self.start_polling()

    def poll(self):
        one_second = 1
        timestamp = int(time.time())
        msg = {"type": "timestamp_secs", "timestamp": timestamp}
        self.send(msg)
        return one_second
        

if __name__ == "__main__":
    block = TimestampSecondsSource()
    block.client.loop_forever()


    """
    from dolittle pkg root:
    python -m src.lib.sources.timestamp_seconds_source -name 'Timestamp in seconds' -out time/timestamps/seconds
    """