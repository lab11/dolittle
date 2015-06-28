from master_control_board_block import MCBBlock
from zeroconf import ServiceInfo, ServiceBrowser, Zeroconf

class MasterControlBoard(MCBBlock):
    def __init__(self):
        super(MasterControlBoard, self).__init__()
        self.name = 'localhost'
        self.broker_port = 1883
        self.broker_addr = 'localhost'
        self.can_be_master = True

        self.shell_commands = []
        self.apps = []
        self.streams = {}
        self.blocks = {}

        print("\nDOLITTLE: Starting Dolittle.\n")

        # start local block watchdog

        # set up multi-device messaging domain
        service_info = self.get_dolittle_service_info()
        if service_info != None: 
            self.broker_addr, self.broker_port = service_info
            print("DOLITTLE: Found Dolittle service on LAN at {}:{}".format(self.broker_addr, self.broker_port))
            self.join_dolittle_service()
        else:
            print("DOLITTLE: No existing Dolittle service found on LAN."
            print("Should I provide the Dolittle service to the LAN, or just run locally?")

            if self.can_be_master == True:
            print("DOLITTLE: I am now master of the universe. Advertising service.")f
            self.spawn_dolittle_service()

        self.send({"msg": "Hello"})


    def process(self, msg_json):
        mag = msg_json
        if msg["type"] == "control":
            app_name = msg["app"]["app_name"]
            if app_name not in self.apps:
                self.apps.append(app_name)
            
            blocks_in_progress = []

            blocks = msg["app"]["blocks"]
            for block in blocks:
                extension = block["code"].split(".")[-1]
                if extension == ".py":
                    program = "python"
                elif extension == ".js":
                    # will need to detect OS to get this right
                    program = "node"
                block["program"] = program
                blocks_in_progress.append(block)

            streams = msg["app"]["streams"]
            for stream in streams:
                if "add_publishers" in stream:
                    pass
                if "add_subscribers" in stream:
                    pass
                
            # for each block, assemble command, add to list (let watchdog deal)
            # send status
            
        elif msg["type"] == "request":
            if msg["request"] == "available_streams":
                pass
            elif msg["request"] == "stream_schema":
                pass
            elif msg["request"] == "available_devices":
                pass
            elif msg["request"] == "available_locations":
                pass

    def get_dolittle_service_info(self):
        service_info = None
        zeroconf = Zeroconf()
        name = "dolittle_mqtt._tcp.local."
        info = ServiceInfo("_mqtt._tcp.local.", "dolittle._mqtt._tcp.local.")
        exists = info.request(zeroconf, 1000)
        if exists:
            service_info = (info.server[:-1], info.port)
        zeroconf.close()
        return service_info

    def join_dolittle_service(self):
        self.start_messaging_interface()

    def spawn_dolittle_service(self):
        # register zeroconf dolittle service
        pass

    def watchdog(self):
        for cmd in self.shell_commands:
            #if not in ps aux, then execute
            pass

if __name__ == "__main__":
    mcb = MasterControlBoard()
    name = mcb.name
    mcb.in_streams = ['dolittle/apps']
    mcb.out_streams = ['dolittle/status']
    mcb.client.loop_forever()