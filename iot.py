from iotmanager import Manager
from flask_socketio import emit

device_types = [
    "rgb_light",
    "dimmed_light",
    "box_light"
]

# IoT Manager instance
device_manager = Manager(device_types)


@device_manager.event
def on_connect():
    return


@device_manager.event
def on_message():
    return


def get_data_by_role(role):
    data = device_manager.get_client_data()

    return data
