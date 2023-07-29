import configparser

def bot(arg):
    config = configparser.ConfigParser()
    config.read("config.ini")
    bot = config.get("Bot", f"{arg}")
    return bot

def watch_id(val):
    i=[]
    config= configparser.ConfigParser()
    config.read("config.ini")
    ids= config.get("White_List","id")
    id_a = ids.split(",")
    for id in id_a:
        if str(id) == str(val):
            i.append(True)
        else:
            i.append(False)
    out = any(i)
    return out

def watch_mac(val):
    i = 0
    config= configparser.ConfigParser()
    config.read("config.ini")
    ids= config.get("MAC_address","mac")
    id_a = ids.split(",")
    for id in id_a:
        if str(id) == str(val):
            i.append(True)
        else:
            i.append(False)
    out = any(i)
    return out

def zabbix_data(arg):
    config = configparser.ConfigParser()
    config.read("config.ini")
    data = config.get("zabbix_connection", f"{arg}")
    return data

def read_dns_server():
    config = configparser.ConfigParser()
    config.read('config.ini')
    conf = config.get('dns', 'server')
    return conf
