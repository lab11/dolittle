from ...core.source import Source
import IPy
import json
import sys
try:
    import socketIO_client as sioc
except ImportError:
    print('Could not import the socket.io client library.')
    print('sudo pip install socketIO-client')
    sys.exit(1)

class GATDSource(Source, sioc.BaseNamespace):
    def __init__(self):
        super(GATDSource, self).__init__()

        socketio_host = self.params['socketio_host']
        socketio_port = self.params['socketio_port']
        socketio_namespace = self.params['socketio_namespace']
        query = self.params['query']

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
        stream_namespace = socketIO.define(stream_receiver,
            '/{}'.format(socketio_namespace))
        socketIO.wait()


if __name__ == "__main__":
    block = GATDSource()
    block.client.loop_forever()

    """
    from dolittle pkg root:
    python -m src.lib.sources.gatd_source -name 'GATD Dummy' -out gatd/test:gatd/ted -params '{"socketio_host": "gatd.eecs.umich.edu","socketio_port": 8082,"socketio_namespace": "stream","query": {"profile_id": "nMR0xcWInF"}}'
    """

