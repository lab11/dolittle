from pyblocks.source import PollingSource
import urllib2

req = "https://api.ninja.is/rest/v0/device/1014BBBK6048_0_0_11/heartbeat?user_access_token=96926c846234d80b18ddc2d3c276162e2962da77"


class NinjablocksMotionSource(PollingSource):
    def __init__(self):
        super(NinjablocksMotionSource, self).__init__()

        self.ninjablocks_auth_file = self.params["ninjablocks_auth_file"]

        self.user_access_token = #crap with the file

        self.start_polling()

     def poll():
     	req = "https://api.ninja.is/rest/v0/device/{0}/heartbeat?user_access_token={1}".format(self.rf_device_id, self.user_access_token)
     	response = urllib2.urlopen(req).read()

     def get_rf_device_id():


if __name__ == "__main__":
    block = NinjablocksMotionSource()
    block.client.loop_forever()