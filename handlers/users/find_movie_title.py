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
    Активирует состояние type_movie, и призывает пользователя к выбору типа
    :param message: Передает данные из предыдущего хендлера
    """
    text = 'Что будем искать? 🧐'
    await message.answer(text=text, reply_markup=type_choice)
    # Автивирует состояние type_movie
    await DataUpdate.type_movie.set()


@dp.callback_query_handler(state=DataUpdate.type_movie)
async def keyboards(call: CallbackQuery, state: FSMContext):
    """
    Призывает пользователя к вводу названия фильма
    :param call: Передает данные из предыдущего хендлера
    :param state: получает состояние предыдущего хендлера
    """
    # Записывает значение callback_data и нажатой внопки в состояние type_movie
    await state.update_data(type_movie=call.data)
    await DataUpdate.next()

    # Формирует ответ пользователю
    text = 'Введите название'
    await call.message.answer(text=text)
    # Автивирует состояние title
    await DataUpdate.title.set()


@dp.message_handler(state=DataUpdate.title)
async def find_movie(message: Message, state: FSMContext):
    """
    Показывает результат поиска по названию
    :param message: Передает данные из предыдущего хендлера
    :param state: получает состояние предыдущего хендлера
    """
    # Получает выбранный тип из type_movie
    type_movie = (await state.get_data())['type_movie']
    # Получает список фильмов которые соответствуют выбранному типу и введенному названию
    movie_data = FinderTitle(type_movie, message.text).get_list_movie()
    # Проверяет наличие ответа. Если ничего небыло найдено, то movie_data будет содержать None
    if movie_data:
        # Генерирует список кнопок из полученного ответа movie_data
        choice_movie_list = movie_list(movie_data)
        await message.answer(text='Вот, что я нашел:', reply_markup=choice_movie_list)
    else:
        # Выводится если ничего небыло найдено
        await message.answer(text='Ничего не найдено')
    # Активирует состояние title
    await DataUpdate.title.set()


@dp.callback_query_handler(movie_callback.filter(item_name="movie"), state=DataUpdate.title)
async def buying_apples(call: CallbackQuery, state: FSMContext, callback_data: dict):
    """
    Показывает результат поиска по ID, и выводит кнопки "Опубликовать" и "Добавить описание и опубликовать"
    :param call: Передает данные из предыдущего хендлера
    :param state: Передает состояние из предыдущего хендлера
    :param callback_data: Передает данные нажатой кнопки
    """
    # Получает id кинпоиска из нажатой кнопки
    idkp = callback_data['id_button']
    # Получает по id кинопоиска данные из API
    movie_data = FinderId(idkp, False).get_movie()
    # Записывает полученные данные в состояние json
    await state.update_data(json=movie_data)
    # Формирует ответ пользователю, если id не найден, то произойдет ошибка TypeError и пользовалю будет отправлено
    # сообщение 'По этому ID ничего не найдено'
    try:
        info = f'Фильм который вы искали: {movie_data["title"]} \r\nОписание: {movie_data["description"]} ' \
               f'\r\nТрейлер: {movie_data["trailer"]} \r\nПостер: {movie_data["poster"]}'
        await call.message.answer(text=info, reply_markup=run_choice)
    except TypeError:
        info = 'По этому ID ничего не найдено'
        await call.message.answer(text=info)
    # Автивирует состояние json
    await DataUpdate.json.set()
