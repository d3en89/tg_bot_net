import subprocess
from os import devnull

FNULL = open(devnull, 'w')


def test_speed():
    """ Функция измерения скорости интернета, измеряет скорость интернета там где установлен tg-bot
    :return:
    """
    try:
        subprocess.check_call(["ping", "-c 1", "8.8.8.8"],
                              stdout=FNULL,
                              stderr=subprocess.STDOUT)
        val = "ok"
    except subprocess.CalledProcessError:
        val = "bad"

    start_script = subprocess.Popen('/bin/speedtest --secure', shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE, encoding='utf-8')

    match val:
        case "ok":
            res = ""
            for line in start_script.stderr:
                if 'ERROR' in line:
                    res += "" + line.strip()
            for line in start_script.stdout:
                if 'Download' in line or 'Upload' in line:
                    res += "" + line.strip()
            return res.strip().replace("Upload", " Upload")
        case "bad":
            return 'Not connection'
