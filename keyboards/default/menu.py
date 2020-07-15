from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Создать объявление')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)