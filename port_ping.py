import socket
from contextlib import closing


def check_port(host, port):
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        if result == 0:
            return f'Port is open : code {result}'
        else:
            return f'Port is not open : code {result}'



