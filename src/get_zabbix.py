from pyzabbix import ZabbixAPI


def zabbix_get(server, user, password, response=False):
    zabbix = ZabbixAPI(url=f'{server}', user=f'{user}', password=f'{password}')
    result1 = zabbix.host.get(monitored_hosts=1)
    hosts = {}
    count = 0

    for host_list in result1:
        hosts[host_list.get("host")] = count
        count += 1
    try:
        status = result1[hosts[f'{response}']]['available']
        if status == "1":
            status = "ONLINE"
        else:
            status = "Агент не доступен"
    except KeyError:
        status = "Некорректное имя сервера"

    zabbix.user.logout()
    return status
