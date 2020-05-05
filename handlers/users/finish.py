from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from keyboards.inline.choice_buttons import url_movies, running
from state.state import DataUpdate
from browser.send_movie import SendMovie
from loader import dp


@dp.callback_query_handler(text_contains="run_sender", state=DataUpdate.json)
async def run_sender(call: CallbackQuery, state: FSMContext):
    """
    Хендлер наследует состояние json. И публикует фильм только по данным полученным из API
    после публикации изменяет сообщение и прикладывает ссылку на опубликованный фильм
    :param call: Передает данные из предыдущего хендлера
    :param state: получает состояние предыдущего хендлера
    :return:
    """
    # Получает все состояния
    movie = await state.get_data()
    # Готовит данные для публикации
    run = SendMovie(movie['json'], None).run_sender()
    # Показывает начало процесса публикации
    await call.message.edit_reply_markup(reply_markup=running)
    # Запускает постинг на сайте
    await call.message.edit_reply_markup(reply_markup=url_movies(run))
