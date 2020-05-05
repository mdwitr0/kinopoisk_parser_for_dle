from aiogram.dispatcher.filters import Text
from aiogram.types import Message
from aiogram.dispatcher import FSMContext

from api.kp_cloud_api import FinderId
from keyboards.inline.choice_buttons import run_choice
from state.state import DataUpdate
from loader import dp


@dp.message_handler(Text(equals=["Поиск по ID 🔎"]), state="*")
async def keyboards(message: Message):
    """
    Призывает пользователя к вводу id кинопоиска
    :param message: Передает данные из предыдущего хендлера
    """
    text = 'Введите ID кинопоиска'
    await message.answer(text=text)
    await DataUpdate.idkp.set()


@dp.message_handler(state=DataUpdate.idkp)
async def find_movie(message: Message, state: FSMContext):
    """
    Показывает результат поиска по ID, и выводит кнопки "Опубликовать" и "Добавить описание и опубликовать"
    :param message: Передает данные из предыдущего хендлера
    :param state: получает состояние предыдущего хендлера
    """
    movie_data = FinderId(message.text, False).get_movie()
    await state.update_data(json=movie_data)
    try:
        info = f'Фильм который вы искали: {movie_data["title"]} \r\nОписание: {movie_data["description"]} ' \
               f'\r\nТрейлер: {movie_data["trailer"]} \r\nПостер: {movie_data["poster"]}'
    except TypeError:
        info = 'По этому ID ничего не найдено'
    if not info == 'По этому ID ничего не найдено':
        await message.answer(text=info, reply_markup=run_choice)
    else:
        await message.answer(text=info)
    await DataUpdate.json.set()
