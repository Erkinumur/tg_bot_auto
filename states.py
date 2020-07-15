from aiogram.dispatcher.filters.state import State, StatesGroup


class NewCar(StatesGroup):
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
    image = State()
