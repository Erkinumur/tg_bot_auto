from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.callback_datas import MyCarDetailCallback, MyCarsListCallback, UpdateCarCallback, \
    ImageArrowsCallback, ImageCallback
from models import DBCommands

db = DBCommands()


async def adv_list_markup(count, user_id, page=1, one_page=None):
    last_page = 0
    markup = InlineKeyboardMarkup()
    menu_button = InlineKeyboardButton(
        'Главное меню',
        callback_data='main_menu'
    )
    cars = await db.get_cars_by_user(user_id, page)
    for car in cars:
        markup.row(InlineKeyboardButton(
            car.title,
            callback_data=MyCarDetailCallback.new(
                car_pk=car.id,
                page=page
            )
        ))
    if one_page:
        markup.row(menu_button)
        return markup

    if count / 10 == count // 10:
        last_page = count / 10
    else:
        last_page = count // 10 + 1
    if last_page == page:
        markup.row(InlineKeyboardButton(
            '⬅️',
            callback_data=MyCarsListCallback.new(
                page=page-1
            )),
            menu_button
        )
    elif page == 1:
        markup.row(menu_button,
                   InlineKeyboardButton(
                       '➡️',
                       callback_data=MyCarsListCallback.new(
                           page=2)
                   )
        )
    else:
        markup.row(
            InlineKeyboardButton(
                '⬅️',
                callback_data=MyCarsListCallback.new(
                    page=page - 1)
            ),
            menu_button,
            InlineKeyboardButton(
                '➡️',
                callback_data=MyCarsListCallback.new(
                    page=page + 1)
            )
        )
    return markup, last_page


async def car_detail_markup(page, pk):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton(
            text='Изменить',
            callback_data=f'car_update:{page}:{pk}'
        ),
        InlineKeyboardButton(
            text='Удалить',
            callback_data=f'delete_car:{pk}'
        )
    )
    markup.row(InlineKeyboardButton(
        text='Назад',
        callback_data=MyCarsListCallback.new(page)
    ))
    markup.row(InlineKeyboardButton(
        text='Главное меню',
        callback_data='main_menu'
    ))
    return markup


async def car_fields_markup(car, page):
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton(
        text=f'Заголовок: {car.title}',
        callback_data=UpdateCarCallback.new(
            'title', car.id, page
        )
    ))
    markup.row(InlineKeyboardButton(
        text=f'Год: {car.year}',
        callback_data=UpdateCarCallback.new(
            'year', car.id, page
        )
    ))
    markup.row(InlineKeyboardButton(
        text=f'Пробег (км): {car.kilometerage}',
        callback_data=UpdateCarCallback.new(
            'kilometerage', car.id, page
        )
    ))
    markup.row(InlineKeyboardButton(
        text=f'Цвет: {car.color}',
        callback_data=UpdateCarCallback.new(
            'color', car.id, page
        )
    ))
    markup.row(InlineKeyboardButton(
        text=f'Объем: {car.volume}',
        callback_data=UpdateCarCallback.new(
            'volume', car.id, page
        )
    ))
    markup.row(InlineKeyboardButton(
        text=f'Тип топлива: {car.fuel_type}',
        callback_data=UpdateCarCallback.new(
            'fuel_type', car.id, page
        )
    ))
    markup.row(InlineKeyboardButton(
        text=f'Привод: {car.wheel_drive}',
        callback_data=UpdateCarCallback.new(
            'wheel_drive', car.id, page
        )
    ))
    markup.row(InlineKeyboardButton(
        text=f'КПП: {car.gear_box}',
        callback_data=UpdateCarCallback.new(
            'gear_box', car.id, page
        )
    ))
    markup.row(InlineKeyboardButton(
        text=f'Руль: {car.wheel_position}',
        callback_data=UpdateCarCallback.new(
            'wheel_position', car.id, page
        )
    ))
    markup.row(InlineKeyboardButton(
        text=f'Доп. описание',
        callback_data=UpdateCarCallback.new(
            'description', car.id, page
        )
    ))
    markup.row(InlineKeyboardButton(
        text=f'Цена: {car.price}',
        callback_data=UpdateCarCallback.new(
            'price', car.id, page
        )
    ))
    markup.row(InlineKeyboardButton(
        text=f'Телефон: {car.phone}',
        callback_data=UpdateCarCallback.new(
            'phone', car.id, page
        )
    ))
    markup.row(InlineKeyboardButton(
        text=f'Фотографии',
        callback_data=UpdateCarCallback.new(
            'images', car.id, page
        )
    ))
    markup.row(InlineKeyboardButton(
        text='Назад',
        callback_data=MyCarDetailCallback.new(
            car.id, page
        )
    ))

    return markup


async def get_car_image_and_mrakup(images, page, car_pk, img_idx=0):
    image = None
    markup = InlineKeyboardMarkup()
    if images:
        if img_idx:
            markup.insert(InlineKeyboardButton(
                text='⬅️',
                callback_data=ImageArrowsCallback.new(
                    img_idx-1,
                )
            ))
        markup.insert(InlineKeyboardButton(
            text='Назад',
            callback_data=f'back_to_car_update'
        ))
        if img_idx < len(images) - 1:
            markup.insert(InlineKeyboardButton(
                text='➡️',
                callback_data=ImageArrowsCallback.new(
                    img_idx + 1,
                )
            ))
        image = images[img_idx]
        markup.row(
            InlineKeyboardButton(
                'Удалить',
                callback_data='delete_car_img')
        )
    else:
        markup.insert(InlineKeyboardButton(
            text='Назад',
            callback_data=f'back_to_car_update'
        ))
    markup.row(InlineKeyboardButton(
        text="Добавить фото",
        callback_data='add_car_img'
    ))
    return image, markup
