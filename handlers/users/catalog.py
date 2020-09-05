from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ContentType, InlineKeyboardMarkup

import states
from keyboards.default import menu
from keyboards.inline.add_car import choice_brand_markup
from keyboards.inline.callback_datas import ChoiceBrandCallback, ChoiceModelCallback, CarsListCallback, \
    CarDetailCallback
from keyboards.inline.catalog import cars_list_markup, choice_model_markup, car_detail_markup
from loader import dp
from models import DBCommands, Car

db = DBCommands()


async def show_car(message: Message, car: Car, markup=None):
    text = f'<b>{car.title}</b>\n' \
           f'<i>Марка:</i> {car.model.brand.name}\n' \
           f'<i>Модель:</i> {car.model.name}\n' \
           f'<i>Год:</i> {car.year}\n' \
           f'<i>Пробег:</i> {car.kilometerage}\n' \
           f'<i>Цвет:</i> {car.color}\n' \
           f'<i>Объем:</i> {car.volume}\n' \
           f'<i>Тип топлива:</i> {car.fuel_type}\n' \
           f'<i>Привод:</i> {car.wheel_drive}\n' \
           f'<i>КПП:</i> {car.gear_box}\n' \
           f'<i>Руль:</i> {car.wheel_position}\n' \
           f'<i>Описание:</i> {car.description}\n' \
           f'<b>Цена: {car.price}\n</b>'
    images = car.images
    media = None
    if images:
        media = types.MediaGroup()
        for image in images:
            media.attach_photo(image.file_id)
    await message.answer(text)
    if images:
        await message.answer_media_group(media)
    await message.delete()


@dp.message_handler(text='Каталог')
async def choice_brand(message: Message):
    markup = await choice_brand_markup()
    await message.answer('Выберите марку авто:', reply_markup=markup)


@dp.callback_query_handler(ChoiceBrandCallback.filter())
async def choice_model(call: CallbackQuery, callback_data: dict):
    brand_id = int(callback_data.get('pk'))
    markup = await choice_model_markup(brand_id)
    await call.message.edit_text(f'Вы выбрали: {callback_data.get("brand_name")}')
    await call.message.answer('Выберите модель:', reply_markup=markup)


@dp.callback_query_handler(CarsListCallback.filter())
async def show_cars_list(call: CallbackQuery, callback_data: dict):
    count = await db.count_cars_by_model(int(callback_data.get('model_pk')))
    if not count:
        await call.message.edit_text("Актуальные объявления "
                                     "по данной моделе остутствуют")
        await choice_brand(call.message)
    elif count <= 10:
        markup = await cars_list_markup(
            count,
            int(callback_data.get('brand_pk')),
            int(callback_data.get('model_pk')),
            one_page=True
        )
        await call.message.edit_text('Страница 1/1:')
    else:
        page = int(callback_data.get('page'))
        markup, last_page = await cars_list_markup(
            count,
            int(callback_data.get('brand_pk')),
            int(callback_data.get('model_pk')),
            page
        )
        await call.message.edit_text(f'Страница {page}/{last_page}\n'
                                     f'Для навигации используйте кнопки ниже:\n'
                                     f'⬅️ - предыдущая страница\n'
                                     f'➡️ - следующая страница\n',
                                     reply_markup=markup)


@dp.callback_query_handler(CarDetailCallback.filter())
async def car_detail(call: CallbackQuery, callback_data: dict):
    car = await db.get_car(int(callback_data.get('car_pk')))
    markup = await car_detail_markup(car.phone, callback_data)
    await show_car(call.message, car)
    await call.message.answer('Для получения номера телефона'
                              'нажмите "Контакт"\n'
                              'Чтобы вернутся назад нажмите "Назад"',
                              reply_markup=markup)


@dp.callback_query_handler(text='back_to_catalog')
async def back_to_catalog(call: CallbackQuery):
    await call.message.edit_text('Каталог')
    await choice_brand(call.message)


@dp.callback_query_handler(text_contains='car_contact')
async def send_contact(call: CallbackQuery):
    car_pk = call.data.split(':')[-1]
    car = await db.get_car(car_pk)
    phone = car.phone
    title = car.title
    await call.message.answer_contact(
        phone, title
    )