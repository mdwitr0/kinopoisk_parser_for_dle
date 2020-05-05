from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext
from keyboards.inline.choice_buttons import url_movies, running
from state.state import DataUpdate
from browser.send_movie import SendMovie
from loader import dp


@dp.callback_query_handler(text_contains="add_text", state="*")
async def run_sender(call: CallbackQuery, state: FSMContext):
    """
    Вызывает состояние description и отправляет сообщение пользователю с просьбой прислать описание
    :param call: Передает данные из предыдущего хендлера
    :param state: получает состояние предыдущего
    :return:
    """
    text = 'Введите новое описание фильма'
    await state.update_data(description=call.message.text)
    await call.message.edit_text(text=text)
    await DataUpdate.description.set()


@dp.message_handler(state=DataUpdate.description)
async def run_sender(message: Message, state: FSMContext):
    """
    Показывает результат поиска по ID, и выводит кнопки "Опубликовать" и "Добавить описание и опубликовать"
    Так же получает состояние из предыдущего хендлера и записывает в него описание.
    :param message: Получает сообщение с ID
    :param state: получает состояние предыдущего хендлера
    :return:
    """
    # Запись описания в состояние description
    await state.update_data(description=message.text)
    await DataUpdate.description.set()
    await DataUpdate.next()
    # Получает все состояния которые были записаны
    movie = await state.get_data()
    # Получаем из состояния данные о фильме
    movie_data = movie['json']
    # Парсим полученные данны и готовоим текст для отправки
    info = f'Фильм который вы искали: {movie_data["title"]} \r\nОписание: {movie["description"]} ' \
           f'\r\nТрейлер: {movie_data["trailer"]} \r\nПостер: {movie_data["poster"]}'
    # Отправляем сообщение и запускаем процесс публикации фильма на сайте
    send_message = await message.answer(text=info, reply_markup=running)
    await send_message.edit_reply_markup(
        reply_markup=url_movies(SendMovie(movie['json'], movie['description']).run_sender()))
