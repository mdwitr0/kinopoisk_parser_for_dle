from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext
from keyboards.inline.choice_buttons import url_movies, running
from state.state import DataUpdate
from browser.send_movie import SendMovie
from loader import dp


@dp.callback_query_handler(text_contains="run_sender", state=DataUpdate.json)
async def run_sender(call: CallbackQuery, state: FSMContext):
    """
    Запускает поститинг на сайте
    после публикации изменяет сообщение и прикладывает ссылку на опубликованный фильм
    :param call: Передает данные из предыдущего хендлера
    :param state: получает состояние предыдущего хендлера
    :return:
    """
    movie = await state.get_data()
    run = SendMovie(movie['json'], None).run_sender()
    await call.message.edit_reply_markup(reply_markup=running)
    await call.message.edit_reply_markup(reply_markup=url_movies(run))
    await DataUpdate.idkp.set()
