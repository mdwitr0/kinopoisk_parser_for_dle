from aiogram.dispatcher.filters.state import StatesGroup, State


# Временное хранилище состояний
class DataUpdate(StatesGroup):
    title = State()
    idkp = State()
    type_movie = State()
    json = State()
    description = State()
