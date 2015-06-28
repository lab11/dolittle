from master_control_board_block import MCBBlock
import socket
import thread


class MasterControlBoard(MCBBlock):
    def __init__(self):
        super(MasterControlBoard, self).__init__()
        self.name = socket.gethostname()

        # Default (local) MQTT broker settings
        self.broker_port = 1883
        self.broker_addr = 'localhost'

        # Zeroconf settings
        # Can this device be master of the universe?
        # True => will host Dolittle service on LAN if none found. False => will only run Dolittle locally.
        # Only select True if the host device has consistent uptime. 
        # ATM, if the LAN master goes down, all Dolittle comms on any device on the LAN will cease.
        self.can_be_master = True

        # State about the Dolittle system
        self.shell_commands = []
        self.apps = []
        self.streams = {}
        self.blocks = {}

        print("\nDOLITTLE: Starting Dolittle.\n")

        # start local block watchdog

        # connect to Dolittle messaging domain
        service_info = self.get_dolittle_service_info()
        if service_info != None: 
            self.broker_addr, self.broker_port = service_info
            print("DOLITTLE: Found Dolittle service on LAN at {}:{}".format(self.broker_addr, self.broker_port))
            self.is_master = False
            print("DOLITTLE: Joined local Dolittle messaging domain.")
        else:
            print("DOLITTLE: No existing Dolittle service found on LAN.") 
            #print("Should I provide the Dolittle service to the LAN, or just run locally?")
            if self.can_be_master == True:
                print("DOLITTLE: I am now master of the universe. Advertising service.")
                self.spawn_dolittle_service()
                self.is_master = True
        self.join_dolittle_service()
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

    def watchdog(self):
        for cmd in self.shell_commands:
            #if not in ps aux, then execute
            pass

if __name__ == "__main__":
    mcb = MasterControlBoard()
    name = mcb.name
    mcb.in_streams = ['dolittle/apps']
    mcb.out_streams = ['dolittle/status']
    print("WOO")
    print(mcb.broker_addr)
    try:
        mcb.client.loop_forever()
    except KeyboardInterrupt:
        if mcb.is_master:
            mcb.unregister_dolittle_service()