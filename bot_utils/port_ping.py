import asyncio
import socket
from contextlib import closing


def func_check_port(mes: list, fl: str) -> str:
    """
        Функция для проверки подключения к порту(открыт порт или нет)
    """

    def check_port(host, port) -> str:
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:

            sock.settimeout(2)
            result = sock.connect_ex((host, port))
            if result == 0:
                return f'Port is open : code {result}'
            else:
                return f'Port is not open : code {result}'

    try:
        if fl == "No state":
            port_ping = check_port(mes[1], int(mes[2]))
        if fl == "State":
            port_ping = check_port(mes[0], int(mes[1]))
        return port_ping
    except IndexError:
        return "Введите корректные данные"
