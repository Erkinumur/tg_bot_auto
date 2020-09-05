from aiogram import filters, types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ContentType

import states
from handlers.users.catalog import show_car
from keyboards.default import menu
from keyboards.inline.add_car import choice_fuel_markup, choice_wheel_drive_markup, choice_gear_box_markup, \
    choice_wheel_position_markup
from keyboards.inline.callback_datas import MyCarsListCallback, MyCarDetailCallback, UpdateCarCallback, \
    ImageArrowsCallback
from keyboards.inline.my_advs import adv_list_markup, car_detail_markup, car_fields_markup, get_car_image_and_mrakup
from loader import dp, bot
from models import DBCommands

db = DBCommands()


@dp.message_handler(text='Мои объявления')
async def show_my_advs(message: Message):
    user = types.User.get_current()
    count = await db.count_cars_by_user(int(user.id))
    if not count:
        await message.answer("У Вас нет объявлений", reply_markup=menu)
    elif count <= 10:
        markup = await adv_list_markup(
            count,
            int(user.id),
            one_page=True
        )
        await message.answer('Страница 1/1:', reply_markup=markup)
    else:
        page = 1
        markup, last_page = await adv_list_markup(
            count,
            user.id,
            page
        )
        await message.answer(f'Страница {page}/{last_page}\n'
                             f'Для навигации используйте кнопки ниже:\n'
                             f'⬅️ - предыдущая страница\n'
                             f'➡️ - следующая страница\n',
                             reply_markup=markup)


@dp.callback_query_handler(MyCarsListCallback.filter())
async def call_show_my_advs(call: CallbackQuery, callback_data: int):
    user = types.User.get_current()
    count = await db.count_cars_by_user(int(user.id))
    if not count:
        await call.message.edit_text("У Вас нет объявлений", reply_markup=menu)
    elif count <= 10:
        markup = await adv_list_markup(
            count,
            int(user.id),
            one_page=True
        )
        await call.message.edit_text('Страница 1/1:')
    else:
        page = int(callback_data.get('page'))
        markup, last_page = await adv_list_markup(
            count,
            user.id,
            page
        )
        await call.message.edit_text(f'Страница {page}/{last_page}\n'
                                     f'Для навигации используйте кнопки ниже:\n'
                                     f'⬅️ - предыдущая страница\n'
                                     f'➡️ - следующая страница\n',
                                     reply_markup=markup)


@dp.callback_query_handler(MyCarDetailCallback.filter())
async def my_car_detail(call: CallbackQuery, callback_data: dict):
    user = types.User.get_current()
    car = await db.get_car(int(callback_data.get('car_pk')))
    markup = await car_detail_markup(int(callback_data.get('page')), car.id)
    await show_car(call.message, car)
    await call.message.answer('Чтобы вернутся назад нажмите "Назад"',
                              reply_markup=markup)


@dp.callback_query_handler(text_contains='delete_car')
async def delete_car(call: CallbackQuery):
    pk = int(call.data.split(':')[-1])
    car = await db.get_car(pk)
    await db.delete_obj(car)
    await call.answer('Объявление удалено!')
    await call.message.delete()
    await show_my_advs(call.message)


@dp.callback_query_handler(text_contains='car_update')
async def update_car(call: CallbackQuery = None, car=None, message=None,
                     page=None):
    if not car:
        data = call.data.split(':')
        pk = int(data[-1])
        car = await db.get_car(pk)
        page = int(data[1])
        markup = await car_fields_markup(car, page)
        await call.message.answer('Выберите что хотите изменить', reply_markup=markup)
        await call.message.delete()
    else:
        markup = await car_fields_markup(car, page)
        await message.answer('Выберите что хотите изменить', reply_markup=markup)
        await message.delete()


async def get_markup_car_fields(field):
    if field not in ['fuel_type', 'wheel_drive', 'gear_box', 'wheel_position']:
        return
    fields = {'fuel_type': choice_fuel_markup,
              'wheel_drive': choice_wheel_drive_markup,
              'gear_box': choice_gear_box_markup,
              'wheel_position': choice_wheel_position_markup}
    return fields.get(field)


@dp.callback_query_handler(ImageArrowsCallback.filter(), state=states.UpdateCar.update)
async def show_images(call: CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    img_idx = int(callback_data.get('img_idx', 0))
    car = data.get('car')
    page = data.get('page')
    images = data.get('images')
    image, markup = await get_car_image_and_mrakup(images, page, car.id, img_idx)
    await state.update_data(img_idx=img_idx)
    await call.message.delete()
    await call.message.answer_photo(
        image.file_id,
        caption='Для пролистывания используйте кнопки стрелок.\n'
                'Чтобы вернуться назад, удалить данное фото или '
                'добавить новое, используйте соответсвующие кнопки',
        reply_markup=markup)


@dp.callback_query_handler(text='back_to_car_update', state='*')
async def back_to_car_update(call: CallbackQuery, state: FSMContext,
                             message = None):
    data = await state.get_data()
    car = data.get('car')
    page = data.get('page')
    if not message:
        message = call.message
    await state.finish()
    await update_car(car=car, page=page, message=message)


@dp.callback_query_handler(UpdateCarCallback.filter(), state='*')
async def recieve_car_fields(call: CallbackQuery, callback_data: dict, state: FSMContext):
    field = callback_data.get('field')
    car = await db.get_car(int(callback_data.get('pk')))
    page = callback_data.get('page')
    await states.UpdateCar.update.set()
    await state.update_data(
        field=field,
        car=car,
        page=int(page)
    )
    if field == 'images':
        images = car.images
        if images:
            images = list(images)
            await state.update_data(images=images, img_idx=0)
        image, markup = await get_car_image_and_mrakup(images, page, car.id)
        if image:
            await call.message.answer_photo(
                image.file_id,
                caption='Для пролистывания используйте кнопки стрелок.\n'
                        'Чтобы вернуться назад, удалить данное фото или '
                        'добавить новое, используйте соответсвующие кнопки',
                reply_markup=markup)
        else:
            await call.message.answer("У данного объявления отсутсвуют фото.",
                                         reply_markup=markup)
        await call.message.delete()
        return
    markup = await get_markup_car_fields(field)
    await states.UpdateCar.text.set()
    if markup:
        await call.message.edit_text('Выберите новое значение (для отмены введите "/cancel"): ',
                                     reply_markup=markup)
    else:
        await state.update_data(call=call)
        await call.message.edit_text('Введите новое значение (для отмены введите "/cancel"):')


@dp.callback_query_handler(text='add_car_img', state=states.UpdateCar.update)
async def add_car_image(call: CallbackQuery, state: FSMContext):
    await states.UpdateCar.image.set()
    await state.update_data(call=call)
    await call.message.answer('Отправте изображение (как фото):')


@dp.message_handler(content_types=ContentType.PHOTO, state=states.UpdateCar.image)
async def save_car_image(message: Message, state: FSMContext):
    async with state.proxy() as data:
        file_id = message.photo[-1].file_id
        car = data.get('car')
        await db.add_new_img(file_id, car)
        data['images'] = list(car.images)
        call = data.pop('call')
        await call.answer('Фото добавлено!')
    await back_to_car_update({}, state, message)


@dp.callback_query_handler(text='delete_car_img', state=states.UpdateCar.update)
async def delete_car_image(call: CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        img_idx = data.get('img_idx')
        image = data.get('images').pop(img_idx)
        try:
            await db.delete_obj(image)
        except Exception as e:
            print('func delete car image, exception:\n', e )
            return
    await call.answer('Фото удалено!')
    await back_to_car_update({}, state, call.message)


@dp.callback_query_handler(state=states.UpdateCar.text)
async def update_car_field_callback(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    field = data.get('field')
    car = data.get('car')
    page = data.get('page')
    if field == 'fuel_type':
        car.fuel_type = call.data
    elif field == 'wheel_drive':
        car.wheel_drive = call.data
    elif field == 'gear_box':
        car.gear_box = call.data
    elif field == 'wheel_position':
        car.wheel_position = call.data
    await db.update_obj(car, [field])
    await state.finish()
    await call.answer('Поле обновлено')
    await update_car(car=car, message=call.message, page=page)


@dp.message_handler(state=states.UpdateCar.text)
async def update_car_field(message: Message, state: FSMContext):
    data = await state.get_data()
    field = data.get('field')
    car = data.get('car')
    page = data.get('page')
    call = data.pop('call')
    if field == 'title':
        car.title = message.text
    elif field == 'year':
        year = message.text
        if len(year) == 4:
            try:
                car.year = int(year)
            except ValueError:
                await message.answer('Не правильное значение,'
                                     'введите год в формате "2ххх"\n'
                                     'Для отмены введите "/cancel"')
                return
        else:
            await message.answer('Не правильное значение, '
                                 'введите год в формате "2ххх"\n'
                                 'Для отмены введите "/cancel"')
            return
    elif field == 'kilometerage':
        try:
            car.kilometerage = int(message.text)
        except ValueError:
            await message.answer('Не правильное значение, '
                                 'введите только цифры\n'
                                 'Для отмены введите "/cancel"')
            return
    elif field == 'volume':
        try:
            car.volume = float(message.text)
        except ValueError:
            await message.answer('Не правильное значение, '
                                 'введите объем цифрами (пример 2.390)\n'
                                 'Для отмены введите "/cancel"')
            return
    elif field == 'color':
        car.color = message.text
    elif field == 'description':
        car.description = message.text
    elif field == 'price':
        try:
            car.price = int(message.text)
        except ValueError:
            await message.answer('Не правильное значение, '
                                 'введите только цифры\n'
                                 'Для отмены введите "/cancel"')
            return
    elif field == 'phone':
        if not message.text.isdigit():
            await message.answer('Не правильное значение, '
                                 'Введите номер телефона '
                                 'в формате 996ХХХХХХ, только цифры\n'
                                 'Для отмены введите "/cancel"')
            return
        car.phone = message.text
    await db.update_obj(car, [field])
    await call.answer('Поле обновлено')
    await state.finish()
    await update_car(car=car, message=message, page=page)
