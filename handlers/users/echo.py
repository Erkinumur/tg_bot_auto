from aiogram import types
from aiogram.types import ContentType

from loader import dp


@dp.message_handler()
async def bot_echo(message: types.Message):
    await message.answer(message.text)
