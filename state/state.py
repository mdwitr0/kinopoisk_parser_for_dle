from aiogram.dispatcher.filters.state import StatesGroup, State


class PageUpdate(StatesGroup):
    index = State()
    page = State()
    idkp = State()
    json = State()
    description = State()
