from flask_socketio import Namespace, emit
from iot import device_manager


# namespace for controlling iot devices
class IoTControl(Namespace):
    # hen the client connects send them the client data
    def on_connect(self):
        data = device_manager.get_client_data()

        emit("client_data")

    def on_update_light(self, data):
        return

