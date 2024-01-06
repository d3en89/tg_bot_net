import configparser


""" Здесь собираю все функции которые относятся к чтению данных из файла
    *в преспективе переделаю данную историю*
"""


def bot(arg) -> str:
    config = configparser.ConfigParser()
    config.read("config.ini")
    bot_token = config.get("Bot", f"{arg}")
    return bot_token


def watch_id(val) -> bool:
    i = []
    config = configparser.ConfigParser()
    config.read("config.ini")
    id_list = config.get("White_List","id")
    if str(val) in id_list.split(','):
        return True
    else:
        return False


def zabbix_data(arg) -> str:
    config = configparser.ConfigParser()
    config.read("config.ini")
    data = config.get("zabbix_connection", f"{arg}")
    return data


def read_dns_server() -> str:
    config = configparser.ConfigParser()
    config.read("config.ini")
    conf = config.get("dns", "server")
    return conf


def read_ip() -> str:
    config = configparser.ConfigParser()
    config.read('config.ini')
    conf = config.get('ping', 'ip')
    return conf


def read_dns_suffix() -> list:
    config = configparser.ConfigParser()
    config.read('config.ini')
    conf_suffix = [config.get('dns', 'domain_suffix_active'), config.get('dns', 'domain_suffix')]
    return conf_suffix