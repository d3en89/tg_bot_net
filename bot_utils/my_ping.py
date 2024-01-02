from pythonping import ping


def func_ping(mes: list|str, fl :str) -> list|str:
    """
        Обычный пинг
    """
    try:
        if fl == "No state":
            ping_ip = ping(mes[1], count=5)
        if fl == "State":
            ping_ip = ping(mes, count=5)
    except IndexError:
        ping_ip = "Ошибка ввода адресса"
    except RuntimeError as e:
        e1 = e.args[0].split("\"")
        if e1[0] == "Cannot resolve address ":
            ping_ip = e1[0]

    return ping_ip