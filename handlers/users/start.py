from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from keyboards.default import menu
from loader import dp
from models import DBCommands


db = DBCommands()


@dp.message_handler(CommandStart(), state='*')
async def bot_start(message: types.Message, state: FSMContext, command):
    user = types.User.get_current()
    await db.add_new_user(user.id)
    await state.finish()
    await message.answer(f'Привет, {message.from_user.full_name}!', reply_markup=menu)
