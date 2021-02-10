import socketio
ready = False

class MyCustomNamespace(socketio.ClientNamespace):
    def on_connect(self):
        print('connected')
        global ready
        ready = True

    def on_disconnect(self):
        print('disconnected!')

    def on_my_response(self, data):
        print("recv: {}".format(data))

sio = socketio.Client(logger=True, engineio_logger=True)
sio.register_namespace(MyCustomNamespace('/test'))
sio.connect('http://jikding.net', socketio_path='api/socket.io')

while not ready:
    sio.sleep(1)

sio.emit('turn_off', {'data': 'trun off OK!'}, namespace='/test')
print('fin')

sio.disconnect()
