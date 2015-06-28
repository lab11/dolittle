from pyblocks.sink import Sink
import aiml
import requests
import time

class ChatbotSink(Sink):
    def __init__(self):
        super(ChatbotSink, self).__init__()

        self.chatbot_path = self.params['chatbot_path']

        self.k = aiml.Kernel()
        try:
            self.k.loadBrain(self.chatbot_path + "/alice.brn")
        except:
            self.k.learn(self.chatbot_path + "/alice-startup.xml")
            self.k.respond("load aiml b")
            self.k.saveBrain(self.chatbot_path + "/alice.brn")

    def process(self, msg_json):
        msg = msg_json
        if msg["type"] == "chat":
            human_response = msg["response"]
            print(human_response)
            bot_response = self.k.respond(human_response)
            post_data = {'access_token': '03757c97-f5d8-4145-8030-d00453266cb4', 'say': bot_response}
            post_response = requests.get("https://portal.theubi.com/webapi/behaviour", params=post_data)
            print(bot_response)
            print(post_response.url)
            print(post_response)


if __name__ == "__main__":
    block = ChatbotSink()
    block.client.loop_forever()

