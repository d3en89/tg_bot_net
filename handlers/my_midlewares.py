from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from bot import dp
from read_config import watch_id


class CheckAccess(BaseMiddleware):
    """ Класс для проверки разрешения на использование бота
    """
    def __init__(self):
        BaseMiddleware.__init__(self)

    async def on_pre_process_message(self, message: types.Message, data: dict):
        if message.text == '/id':
            return data
        elif watch_id(message.from_user.id):
            return data
        else:
           raise PermissionError('Для вашего ID использование бота запрещено')
