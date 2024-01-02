import subprocess
import time
from os import devnull
import asyncio

FNULL = open(devnull, "w")

def check_speedtest() -> str:
    """ Функция измерения скорости интернета, измеряет скорость интернета там где установлен tg-bot
    :return:
    """
 try:
        subprocess.check_call(["ping", "-c 1", "ya.ru"],
                              stdout=FNULL,
                              stderr=subprocess.STDOUT)
        val = "ok"
    except subprocess.CalledProcessError:
        val = "bad"

    start_script = await asyncio.create_subprocess_exec('/bin/speedtest', "--secure", stderr=asyncio.subprocess.PIPE, stdout=asyncio.subprocess.PIPE)

    st_out = await start_script.stdout.read()
    line_out = st_out.decode('utf-8').split("\n")
    st_err = await start_script.stderr.readline()
    line_err = st_err.decode('utf-8').rstrip().split("\n")

    await start_script.wait()

    match val:
        case "ok":
            res = ""
            for line in line_err:
                if 'ERROR' in line:
                    res += "" + line.strip()
            for line in line_out:
                if 'Download:' in line or 'Upload:' in line:
                    res += "" + line.strip().rstrip().lstrip()
            return res.strip().replace("Upload", " Upload")
        case "bad":
            return 'Not connection'