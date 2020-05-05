from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from api.kp_cloud_api import FinderTitle, FinderId
from keyboards.inline.callback_datas import movie_callback
from keyboards.inline.choice_buttons import type_choice, movie_list, run_choice
from state.state import DataUpdate
from loader import dp


@dp.message_handler(Text(equals=["Поиск по названию 🔎"]), state="*")
async def keyboards(message: Message):
    """
    Призывает пользователя к вводу выбору типа
    :param message: Передает данные из предыдущего хендлера
    """
    text = 'Что будем искать? 🧐'
    await message.answer(text=text, reply_markup=type_choice)
    await DataUpdate.type_movie.set()


@dp.callback_query_handler(state=DataUpdate.type_movie)
async def keyboards(call: CallbackQuery, state: FSMContext):
    """
    Призывает пользователя к вводу названия фильма
    :param call: Передает данные из предыдущего хендлера
    :param state: получает состояние предыдущего хендлера
    """
    await state.update_data(type=call.data)
    await DataUpdate.next()
    text = 'Введите название'
    await call.message.answer(text=text)
    await DataUpdate.title.set()


@dp.message_handler(state=DataUpdate.title)
async def find_movie(message: Message, state: FSMContext):
    """
    Показывает результат поиска по названию, и выводит список кнопок
    :param message: Передает данные из предыдущего хендлера
    :param state: получает состояние предыдущего хендлера
    """
    type_movie = (await state.get_data())['type']
    movie_data = FinderTitle(type_movie, message.text).get_list_movie()
    if movie_data:
        choice_movie_list = movie_list(movie_data)
        await message.answer(text='Вот, что я нашел:', reply_markup=choice_movie_list)
    else:
        await message.answer(text='Ничего не найдено')
    await DataUpdate.title.set()


@dp.callback_query_handler(movie_callback.filter(item_name="movie"), state=DataUpdate.title)
async def buying_apples(call: CallbackQuery, state: FSMContext, callback_data: dict):
    """
    Показывает результат поиска по ID, и выводит кнопки "Опубликовать" и "Добавить описание и опубликовать"
    :param call: Передает данные из предыдущего хендлера
    :param callback_data: Передает данные нажатой кнопки
    """
    await call.answer(cache_time=60)
    idkp = callback_data['id_button']
    movie_data = FinderId(idkp, False).get_movie()
    await state.update_data(json=movie_data)
    try:
        info = f'Фильм который вы искали: {movie_data["title"]} \r\nОписание: {movie_data["description"]} ' \
               f'\r\nТрейлер: {movie_data["trailer"]} \r\nПостер: {movie_data["poster"]}'
    except TypeError:
        info = 'По этому ID ничего не найдено'
    if not info == 'По этому ID ничего не найдено':
        await call.message.edit_text(text=info, reply_markup=run_choice)
    else:
        await call.message.edit_text(text=info)
    await DataUpdate.json.set()