import asyncio
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from models import DBCommands
from .callback_datas import choice_brand_callback, choice_model_callback

db = DBCommands()


async def choice_brand_markup():
    markup = InlineKeyboardMarkup()
    brands = await db.get_all_brands()
    for brand in brands:
        name = brand.name
        pk = brand.id
        markup.insert(InlineKeyboardButton(
            text=name,
            callback_data=choice_brand_callback.new(
                brand_name=name, pk=pk)
        ))
    return markup


async def choice_model_markup(brand_pk):
    markup = InlineKeyboardMarkup()
    model_list = await db.get_models(brand_pk)
    for model in model_list:
        name = model.name
        pk = model.id
        markup.insert(InlineKeyboardButton(
            text=name,
            callback_data=choice_model_callback.new(
                model_name=name, pk=pk)
        ))
    return markup


petrol = InlineKeyboardButton(text='Бензин', callback_data='Бензин')
gas = InlineKeyboardButton(text='Газ', callback_data='Газ')
petrol_gas = InlineKeyboardButton(text='Бензин/Газ', callback_data='Бензин/Газ')
hybrid = InlineKeyboardButton(text='Гибрид', callback_data='Гибрид')
electro = InlineKeyboardButton(text='Электромобиль', callback_data='Электромобиль')

choice_fuel_markup = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [petrol, gas, hybrid],
        [petrol_gas, electro]
    ]
)

choice_wheel_drive_markup = InlineKeyboardMarkup(
    inline_keyboard=
    [[
        InlineKeyboardButton(text='Передний', callback_data='Передний'),
        InlineKeyboardButton(text='Задний', callback_data='Задний'),
        InlineKeyboardButton(text='Полный', callback_data='Полный'),
    ]]
)

choice_gear_box_markup = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [InlineKeyboardButton(text='Автомат', callback_data='Автомат'),
         InlineKeyboardButton(text='Вариатор', callback_data='Вариатор')],
        [InlineKeyboardButton(text='Механическая', callback_data='Механическая')]
    ]
)

choice_wheel_position_markup = InlineKeyboardMarkup(
    inline_keyboard=
        [[InlineKeyboardButton(text='Левый', callback_data='Левый'),
         InlineKeyboardButton(text='Правый', callback_data='Правый')]]
)
