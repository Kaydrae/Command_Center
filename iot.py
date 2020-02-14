from iotmanager import Manager, Client
from flask_socketio import emit
import logging


# declare the list of device types
device_types = [
    "rgb_light",
    "dimmed_light"
]

# IoT Manager instance
device_manager = Manager(device_types, host="0.0.0.0", heartbeat_rate=15, logging_level=logging.DEBUG)


@device_manager.event
def on_connect(client: Client):
    # socket_io.emit("new-client", client.return_data(), namespace="/iot-control")
    return


@device_manager.event
def on_message(client, message):
    return


def get_data_by_role(role):
    data = device_manager.get_client_data()

    return data
