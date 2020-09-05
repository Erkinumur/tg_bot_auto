from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Каталог'),
            KeyboardButton(text='Создать объявление')
        ],
        [
            KeyboardButton(text='Мои объявления')
        ]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)