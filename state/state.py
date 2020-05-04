from aiogram.dispatcher.filters.state import StatesGroup, State


class PageUpdate(StatesGroup):
    title = State()
    idkp = State()
    json = State()
    description = State()
