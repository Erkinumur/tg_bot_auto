from aiogram import filters
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards.default import menu
from loader import dp
from models import DBCommands

db = DBCommands()


@dp.message_handler(filters.Text(['Меню', 'меню', 'menu', 'Menu']), state='*')
async def main_menu(message: Message, state: FSMContext):
    markup = menu
    await state.finish()
    await message.answer('Главное меню', reply_markup=markup)


@dp.callback_query_handler(text='main_menu', state='*')
async def call_main_menu(call: CallbackQuery, state):
    await main_menu(call.message, state)
