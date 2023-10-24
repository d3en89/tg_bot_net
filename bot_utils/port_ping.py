import socket
from contextlib import closing
from subprocess import run, PIPE, STDOUT

def check_port(host, port) -> str:
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as sock:
        sock.settimeout(2)
        result = sock.connect_ex((host, port))
        if result == 0:
            return f"Port is open : code {result}"
        else:
            return f"Port is not open : code {result}"


def whois_ianna(host, key="") -> str:
    """ Получвем сведенья об IP или Домене с офф IANNA  через локальный whois
    :param host - IP или Домен
    :key key -  ключ для расширенного вывода информации"""

    if key == "i":
        whois = (run(["whois", "-I", "-H", f"{host}"], stdout=PIPE, stderr=STDOUT, text=True)).stdout
    else:
        whois = (run(["whois", "-H", f"{host}"], stdout=PIPE, stderr=STDOUT, text=True)).stdout
    return whois

