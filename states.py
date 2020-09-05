from aiogram.dispatcher.filters.state import State, StatesGroup


class NewCar(StatesGroup):
    brand = State()
    model = State()
    year = State()
    kilometerage = State()
    color = State()
    volume = State()
    fuel_type = State()
    wheel_drive = State()
    gear_box = State()
    wheel_position = State()
    description = State()
    price = State()
    phone = State()
    image = State()
    confirm = State()


class UpdateCar(StatesGroup):
    update = State()
    text = State()
    image = State()