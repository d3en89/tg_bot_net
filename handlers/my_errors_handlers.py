import logging
from aiogram import types
from aiogram.utils import exceptions

from aiogram.dispatcher import Dispatcher
from typing import NoReturn

from aiogram.utils.exceptions import MessageError


async def error_handler(update: types.Update, exception: exceptions.TelegramAPIError):
    """ Здесь создаём обработчик событий
    : структура if isinstance(exception, сравниваем с необходимым событием)
    :  действие если необходимо
    : return True
    """

    if isinstance(exception, MessageError):
        await update.message.reply('Message text is empty')
        return True

    if isinstance(exception, PermissionError):
        match str(exception):
            case '[Errno 1] Operation not permitted':
                await update.message.reply('Ошибка доступа')
                return True
            case 'Для вашего ID использование бота запрещено':
                await update.message.reply('Для вашего ID использование бота запрещено')
                return True

    ### Исключения которые еще не обработаны.
    logging.exception(f'Update: {update}, n\
                        Exeption: {exception}')


def register_error_handler(dp: Dispatcher) -> NoReturn:
    dp.register_errors_handler(error_handler)
