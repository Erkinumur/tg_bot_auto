from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import CarsListCallback, CarDetailCallback, ChoiceBrandCallback
from models import DBCommands

db = DBCommands()


async def choice_model_markup(brand_pk):
    markup = InlineKeyboardMarkup()
    model_list = await db.get_models(brand_pk)
    for model in model_list:
        name = model.name
        pk = model.id
        markup.insert(InlineKeyboardButton(
            text=name,
            callback_data=CarsListCallback.new(
                brand_pk=brand_pk,
                model_pk=model.id,
                page=1
            )
        ))
    markup.row(InlineKeyboardButton(text='Назад', callback_data='back_to_catalog'))
    return markup


async def cars_list_markup(count, brand_pk, model_pk, page=1, one_page=None):
    last_page = 0
    brand = await db.get_brand(brand_pk)
    markup = InlineKeyboardMarkup()
    back_button = InlineKeyboardButton(
        'Вернуться',
        callback_data=ChoiceBrandCallback.new(
            brand_name=brand.name,
            pk=brand_pk
        )
    )
    cars_list = await db.get_cars_list(model_pk, page)
    for car in cars_list:
        markup.row(InlineKeyboardButton(
            car.title,
            callback_data=CarDetailCallback.new(
                car_pk=car.id,
                brand_pk=brand_pk,
                model_pk=model_pk,
                page=page
            )
        ))
    if one_page:
        markup.row(back_button)
        return markup

    if count / 10 == count // 10:
        last_page = count / 10
    else:
        last_page = count // 10 + 1
    if last_page == page:
        markup.row(InlineKeyboardButton(
            '⬅️',
            callback_data=CarsListCallback.new(
                brand_pk=brand_pk,
                model_pk=model_pk,
                page=page-1
            )),
            back_button
        )
    elif page == 1:
        markup.row(back_button,
                   InlineKeyboardButton(
                       '➡️',
                       callback_data=CarsListCallback.new(
                           brand_pk=brand_pk,
                           model_pk=model_pk,
                           page=2)
                   )
        )
    else:
        markup.row(
            InlineKeyboardButton(
                '⬅️',
                callback_data=CarsListCallback.new(
                    brand_pk=brand_pk,
                    model_pk=model_pk,
                    page=page - 1)
            ),
            back_button,
            InlineKeyboardButton(
                '➡️',
                callback_data=CarsListCallback.new(
                    brand_pk=brand_pk,
                    model_pk=model_pk,
                    page=page + 1)
            )
        )
    return markup, last_page


async def car_detail_markup(phone, data: dict):
    data.pop('@')
    car_pk = data.pop('car_pk')
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton(
        text='Контакт владельца',
        callback_data=f'car_contact:{car_pk}'))
    markup.row(InlineKeyboardButton(
        text='Назад',
        callback_data=CarsListCallback.new(**data)
    ))
    return markup
