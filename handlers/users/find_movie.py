import logging

from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from keyboards.inline.choice_buttons import run_choice, url_movies, running
from keyboards.default import menu
from state.state import PageUpdate
from api.kp_cloud_api import FinderId
from browser.send_movie import SendMovie
from loader import dp, bot


@dp.message_handler(Command("start"), state="*")
async def start(message: Message):
    await message.answer("Выберите действие", reply_markup=menu)


@dp.message_handler(Text(equals=["Поиск по ID 🔎"]), state="*")
async def keyboards(message: Message, state: FSMContext):
    """
    Призывает пользователя к вводу id кинопоиска
    :param message: получает id
    :param state: вызывает состояние json
    :return:
    """
    text = 'Введите ID кинопоиска'
    await message.answer(text=text)
    await PageUpdate.json.set()


@dp.message_handler(state=PageUpdate.json)
async def find_movie(message: Message, state: FSMContext):
    """
    Показывает результат поиска по ID, и выводит кнопки "Опубликовать" и "Добавить описание и опубликовать"
    :param message: Получает сообщение с ID
    :param state: Сохраняет полученные данные о фильме в состояние json
    :return:
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
    await PageUpdate.json.set()


@dp.callback_query_handler(text_contains="add_text", state="*")
async def run_sender(call: CallbackQuery, state: FSMContext):
    """
    Получает новое описание для фильма
    :param call: Ожидает описание фильма
    :param state: записывает описание в состояние text
    :return:
    """
    text = 'Введите новое описание фильма'
    await state.update_data(description=call.message.text)
    await call.message.edit_text(text=text)
    await PageUpdate.description.set()


@dp.message_handler(state=PageUpdate.description)
async def run_sender(message: Message, state: FSMContext):
    """
    Показывает результат поиска по ID, и выводит кнопки "Опубликовать" и "Добавить описание и опубликовать"
    :param message: Получает сообщение с ID
    :param state: Сохраняет полученные данные о фильме в состояние json
    :return:
    """
    movie = await state.get_data()
    await state.update_data(description=message.text)
    await PageUpdate.description.set()
    await PageUpdate.next()
    movie = await state.get_data()
    movie_data = movie['json']
    info = f'Фильм который вы искали: {movie_data["title"]} \r\nОписание: {movie["description"]} ' \
           f'\r\nТрейлер: {movie_data["trailer"]} \r\nПостер: {movie_data["poster"]}'
    send_message = await message.answer(text=info, reply_markup=running)
    await send_message.edit_reply_markup(
        reply_markup=url_movies(SendMovie(movie['json'], movie['description']).run_sender()))
    await PageUpdate.json.set()


@dp.callback_query_handler(text_contains="run_sender", state=PageUpdate.json)
async def run_sender(call: CallbackQuery, state: FSMContext):
    """
    Запускает поститинг на сайте
    после публикации изменяет сообщение и прикладывает ссылку на опубликованный фильм
    :param call: получет последнее отправленное сообщение
    :param state: Получает состояние json
    :return:
    """
    movie = await state.get_data()
    run = SendMovie(movie['json'], None).run_sender()
    await call.message.edit_reply_markup(reply_markup=running)
    await call.message.edit_reply_markup(reply_markup=url_movies(run))
    await PageUpdate.idkp.set()
