from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ContentType

import states
from handlers.users.catalog import show_car
from keyboards.default import menu
from keyboards.inline.add_car import choice_brand_markup, choice_model_markup, \
    choice_fuel_markup, choice_wheel_drive_markup, choice_gear_box_markup, \
    choice_wheel_position_markup, confirm_markup
from keyboards.inline.callback_datas import ChoiceModelCallback, ChoiceBrandCallback
from loader import dp
from models import DBCommands

db = DBCommands()

not_valid_text = 'Введенны не правильные данные.\n' \
                 'Попробуйте еще раз\n'
cancel_text = '\nДля выхода введите "cancel"'


@dp.message_handler(text='Создать объявление')
async def choice_brand(message: Message):
    markup = await choice_brand_markup()
    await states.NewCar.brand.set()
    await message.answer('Выберите марку авто:', reply_markup=markup)


@dp.callback_query_handler(ChoiceBrandCallback.filter(), state=states.NewCar.brand)
async def choice_model(call: CallbackQuery, callback_data: dict, state: FSMContext):
    brand_id = int(callback_data.get('pk'))
    await states.NewCar.next()
    await state.update_data(brand=await db.get_brand(brand_id))

    markup = await choice_model_markup(brand_id)
    await call.message.edit_text(f'Вы выбрали: {callback_data.get("brand_name")}')
    await call.message.answer('Выберите модель:', reply_markup=markup)


@dp.callback_query_handler(ChoiceModelCallback.filter(), state=states.NewCar.model)
async def input_car_year(call: CallbackQuery, callback_data: dict, state: FSMContext):
    model_id = int(callback_data.get('pk'))
    await states.NewCar.next()
    text = 'Введите год выпуска авто (пример: 2000):' + cancel_text
    await state.update_data(model=await db.get_model(model_id), prev_text=text)
    await call.message.edit_text(f'Вы выбрали: {callback_data.get("model_name")}')
    await call.message.edit_text(text)


@dp.message_handler(state=states.NewCar.year)
async def input_kilometerage(message: Message, state: FSMContext):
    if not message.text.isdigit() or len(message.text) != 4:
        data = await state.get_data()
        await message.answer(not_valid_text + data.get('prev_text'))
        return
    await states.NewCar.next()
    text = 'Введите пробег авто:' + cancel_text
    await state.update_data(year=int(message.text), prev_text=text)
    await message.answer(text)


@dp.message_handler(state=states.NewCar.kilometerage)
async def input_color(message: Message, state: FSMContext):
    if not message.text.isdigit():
        data = await state.get_data()
        await message.answer(not_valid_text + data.get('prev_text'))
        return
    await states.NewCar.next()
    text = 'Введите цвет авто:' + cancel_text
    await state.update_data(kilometerage=int(message.text), prev_text=text)
    await message.answer(text)


@dp.message_handler(state=states.NewCar.color)
async def input_volume(message: Message, state: FSMContext):
    text = 'Введите объем двигателя (пример: 2.4):' + cancel_text
    await state.update_data(color=message.text, prev_text=text)
    await states.NewCar.next()
    await message.answer(text)


@dp.message_handler(state=states.NewCar.volume)
async def input_fuel_type(message: Message, state: FSMContext):
    try:
        float(message.text)
    except ValueError:
        data = await state.get_data()
        await message.answer(not_valid_text + data.get('prev_text'))
        return
    await state.update_data(volume=float(message.text))
    await states.NewCar.next()
    markup = choice_fuel_markup
    await message.answer('Выберите тип топлива:' + cancel_text, reply_markup=markup)


@dp.callback_query_handler(state=states.NewCar.fuel_type)
async def choice_wheel_drive(call: CallbackQuery, state: FSMContext):
    await state.update_data(fuel_type=call.data)
    await states.NewCar.next()
    markup = choice_wheel_drive_markup
    await call.message.edit_text(f'Вы выбрали: {call.data}')
    await call.message.answer('Выберите привод:' + cancel_text, reply_markup=markup)


@dp.callback_query_handler(state=states.NewCar.wheel_drive)
async def choice_gear_box(call: CallbackQuery, state: FSMContext):
    await state.update_data(wheel_drive=call.data)
    await states.NewCar.next()
    markup = choice_gear_box_markup
    await call.message.edit_text(f'Вы выбрали: {call.data}')
    await call.message.answer('Выберите тип КПП:' + cancel_text, reply_markup=markup)


@dp.callback_query_handler(state=states.NewCar.gear_box)
async def choice_wheel_position(call: CallbackQuery, state: FSMContext):
    await state.update_data(gear_box=call.data)
    await states.NewCar.next()
    markup = choice_wheel_position_markup
    await call.message.edit_text(f'Вы выбрали: {call.data}')
    await call.message.answer('Выберите расположение руля:' + cancel_text, reply_markup=markup)


@dp.callback_query_handler(state=states.NewCar.wheel_position)
async def input_description(call: CallbackQuery, state: FSMContext):
    await state.update_data(wheel_position=call.data)
    await states.NewCar.next()
    await call.message.edit_text(f'Вы выбрали: {call.data}')
    await call.message.answer('Введите дополнительное описание (одним сообщением):' + cancel_text)


@dp.message_handler(state=states.NewCar.description)
async def input_price(message: Message, state: FSMContext):
    text = 'Введите цену:' + cancel_text
    await state.update_data(description=message.text,
                            prev_text=text)
    await states.NewCar.next()
    await message.answer(text)


@dp.message_handler(state=states.NewCar.price)
async def input_img(message: Message, state: FSMContext):
    if not message.text.isdigit():
        data = await state.get_data()
        await message.answer(not_valid_text + data.get('prev_text'))
        return
    text = 'Введите номер телефона\n' \
           '(в формате 996ХХХХХХ, только цифры' + cancel_text
    await state.update_data(price=int(message.text),
                            prev_text=text)
    await states.NewCar.next()
    await message.answer(text)


@dp.message_handler(state=states.NewCar.phone)
async def input_img(message: Message, state: FSMContext):
    if not message.text.isdigit():
        data = await state.get_data()
        await message.answer(not_valid_text + data.get('prev_text'))
        return
    text = 'Отправте фото авто (по одному)\n' \
           'Если фото больше нет, нажмите кнопку ниже или напишите "готово"'
    markup = ReplyKeyboardMarkup(
                             keyboard=[[KeyboardButton('готово')]],
                             resize_keyboard=True,
                             one_time_keyboard=True
                         )
    await state.update_data(phone=message.text,
                            prev_text=text,
                            img_markup=markup,
                            images=[])
    await states.NewCar.next()
    await message.answer(text + cancel_text, reply_markup=markup)


@dp.message_handler(content_types=ContentType.PHOTO, state=states.NewCar.image)
async def reciev_img(message: Message, state: FSMContext):
    async with state.proxy() as data:
        data['images'].append(message.photo[-1].file_id)
        await message.answer(data.get('prev_text') + cancel_text,
                             reply_markup=data.get('img_markup'))


@dp.message_handler(text='готово', state=states.NewCar.image)
async def create_car(message: Message, state: FSMContext):
    user = types.User.get_current()
    await state.update_data(user_id=int(user.id))
    data = await state.get_data()
    car = await db.add_new_car(data)
    await state.update_data(car=car)
    await states.NewCar.next()
    markup = confirm_markup
    await show_car(message, car)
    await message.answer('Подтвердите создание объявления',
                         reply_markup=markup)


@dp.callback_query_handler(text_contains='confirm', state=states.NewCar.confirm)
async def confirm_create_car(call: CallbackQuery, state: FSMContext):
    await state.reset_state()
    await call.message('Объявление создано')
    await call.message.answer('Готово!', reply_markup=menu)
    await call.message.delete()


@dp.callback_query_handler(text_contains='delete', state=states.NewCar.confirm)
async def delete_create_car(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await db.delete_obj(data['car'])
    await state.reset_state()
    await call.answer('Отмена')
    await call.message.answer('Создание отменено', reply_markup=menu)
    await call.message.delete()


@dp.message_handler(text='cancel', state=states.NewCar)
async def cancel(message: Message, state: FSMContext):
    await state.reset_state()
    await message.answer('Отмена', reply_markup=menu)
    await message.delete()
