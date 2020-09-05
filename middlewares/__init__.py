from aiogram import Dispatcher
from aiogram.contrib.middlewares import logging

from .throttling import ThrottlingMiddleware


def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(logging.LoggingMiddleware())
