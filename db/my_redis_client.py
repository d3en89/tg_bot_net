import redis


redis_base = redis.Redis(decode_responses=True)
"""  Модуль для создания и использования базы редис, 
    запоминает в память 5ть последних значений используемых с командами"""


def get_hash_command(id_user, use_command: str) -> None|list:
    data = redis_base.hget(name=id_user, key=use_command.lower())
    return None if data is None else data.split(',')


def add_hash_table(id_user, use_command: str, value):
    redis_base.hset(name=id_user, items=[f'{use_command}', f'{value}'])


def update_hash_table(id_user, use_command: str, value: str):
    data = redis_base.hget(name=id_user, key=use_command).split(',')
    data.append(value)
    redis_base.hset(id_user, use_command, ','.join(data[-5:]))


async def check_hash_table(id_user, use_command: str, value: str):
    """ Проверяем наличие введенного значения в списке
    :id_user -  id  пользователя телеграм
    :use_command - введеная команда
    :value -  значение которое следует за командой
    """
    data = redis_base.hget(name=id_user, key=use_command.lower())
    match data:
        case None:
            add_hash_table(id_user, use_command.lower(), value.lower())
        case values if value.lower() in data.split(','):
            pass
        case values if not value.lower() in data.split(','):
            update_hash_table(id_user, use_command.lower(), value.lower())
