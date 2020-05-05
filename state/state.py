from aiogram.dispatcher.filters.state import StatesGroup, State


class DataUpdate(StatesGroup):
    title = State()
    idkp = State()
    type_movie = State()
    json = State()
    description = State()
