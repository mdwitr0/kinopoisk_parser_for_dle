from aiogram.utils.callback_data import CallbackData

# Создает шаблон callback для кнопок с результатом
movie_callback = CallbackData("movies_result", "item_name", "id_button")
