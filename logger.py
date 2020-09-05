import logging


logger = logging.getLogger('tg_bot')


def log_decorator(func):
    async def wrapper(*args, **kwargs):
        logger.info(f'Вызов: {func.__name__}')
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.exception(f'Ошибка {e} в {func.__name__}:')
    return wrapper
