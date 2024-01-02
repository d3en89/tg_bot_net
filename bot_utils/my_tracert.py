import subprocess
import asyncio


async def check_tracert(host, hop=3) -> str:
    """ Проверяем трасировку до указанного хоста
    :param host -  ip  или dns  имя
    :param hop -  указываем кол-во прыжков по умолчанию 3
    """
    app = await asyncio.create_subprocess_exec("traceroute", f"{host}", f"-m {hop}",
                                               stderr=asyncio.subprocess.PIPE,
                                               stdout=asyncio.subprocess.PIPE)

    st_out = await app.stdout.read()
    line_out = st_out.decode("utf-8").split("\n")
    st_err = await app.stderr.readline()
    line_err = st_err.decode("utf-8").rstrip().split("\n")

    await app.wait()

    if line_err[0] != "":
        return "\n".join(line_err)
    if line_out != "":
        return "\n".join(line_out)
