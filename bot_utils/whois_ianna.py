from subprocess import run, STDOUT, PIPE


def get_whois_ianna(host, key="") -> str:
    """ Получвем сведенья об IP или Домене с офф IANNA  через локальный whois
    :param host - IP или Домен
    :param key -  i  ключ для расширенного вывода информации
    """

    if key == "i":
        whois = (run(["whois", "-I", "-H", f"{host}"], stdout=PIPE, stderr=STDOUT, text=True)).stdout
    else:
        whois = (run(["whois", "-H", f"{host}"], stdout=PIPE, stderr=STDOUT, text=True)).stdout

    return whois
