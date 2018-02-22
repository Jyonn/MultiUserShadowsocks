import json
import socket

from Base.common import deprint

client = socket.socket(socket.AF_UNIX, socket.SOCK_DGRAM)
client.bind('../Config/shadowsocks-client.sock')
client.connect('../Config/shadowsocks-manager.sock')


def add_port(port, password):
    data = {
        'add': {
            'server_port': port,
            'password': password,
        },
    }
    data_str = json.dumps(data)
    deprint(data_str)
    client.send(data_str)
    print(client.recv(1506))


def remove_port(port):
    data = {
        'remove': {
            'server_port': port,
        },
    }
    data_str = json.dumps(data)
    deprint(data_str)
    client.send(data_str)
    print(client.recv(1506))
