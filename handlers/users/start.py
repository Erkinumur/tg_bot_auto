from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default import menu
from loader import dp
from models import DBCommands


db = DBCommands()


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    user = types.User.get_current()
    await db.add_new_user(user.id)
    await message.answer(f'Привет, {message.from_user.full_name}!', reply_markup=menu)
