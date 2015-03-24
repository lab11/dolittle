from ..core.pullyu import Pullyu
import IPy
import json
import sys
try:
    import socketIO_client as sioc
except ImportError:
    print('Could not import the socket.io client library.')
    print('sudo pip install socketIO-client')
    sys.exit(1)

class GATD_Pullyu(Pullyu, sioc.BaseNamespace):
    def __init__(self, broker_port, broker_addr, name, in_streams, out_stream, config):
        super(GATD_Pullyu, self).__init__(broker_port, broker_addr, name, in_streams, out_stream)

        socketio_host = config['socketio_host']
        socketio_port = config['socketio_port']
        socketio_namespace = config['socketio_namespace']
        query = config['query']

        class stream_receiver(sioc.BaseNamespace):
            self.buffer = []

            def on_reconnect (self):
                if 'time' in query:
                    del query['time']
                stream_namespace.emit('query', query)

            def on_connect (self):
                stream_namespace.emit('query', query)

            def on_data (self, *args):
                pkt = args[0]
                self.buffer.append(str(pkt))

        stream_receiver.buffer = self.receive_buffer
        socketIO = sioc.SocketIO(socketio_host, socketio_port)
        print('Before')
        stream_namespace = socketIO.define(stream_receiver,
            '/{}'.format(socketio_namespace))
        print('After')
        socketIO.wait()

if __name__ == "__main__":
    gatd_config = { 
        'socketio_host': 'gatd.eecs.umich.edu',
        'socketio_port': 8082,
        'socketio_namespace': 'stream',
        'query': {'profile_id': 'nMR0xcWInF'}
    }
    block = GATD_Pullyu(1883, 'localhost', 'GATD_Pullyu_test', [], 'test_out', gatd_config)
    block.client.loop_forever()
