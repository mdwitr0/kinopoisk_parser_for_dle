from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.callback_datas import movie_callback

# Кнопки для выбора способа публикации на сайте
run_choice = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="📄 Добавить описание и опубликовать 📄", callback_data="add_text"),
    ],
    [
        InlineKeyboardButton(text="📺 Опубликовать на сайте 📺", callback_data="run_sender")
    ]
])

# Отображает начало публикации
running = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="⏳ Публикую ⏳", callback_data="running"),
    ]
])


# Создает кнопку с ссылкой на опупликованный фильм
def url_movies(url):
    url_movie = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Опубликовано ✅", url=url)
        ]
    ])
    return url_movie


# Кнопки выбора типа данных
type_choice = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Фильм 👈", callback_data="movies"),
        InlineKeyboardButton(text="👉 Сериал", callback_data="tv-series"),
    ]
])


def movie_list(json):
    """
    Генератор кнопок.
    :param json: массив с данными о фильмах
    :return: Набор кнопок с названием фильма и его года с присвоенным значением callback_data к  movie_callback
    и уникальным id_button которому присвается id кинопоиска
    """
    choice_movie_list = []
    for movie in json:
        # Получает каждый элемент и парсит его данные, присваивая кнопке
        button = [InlineKeyboardButton(
            text=f'{movie["title"]} {movie["year"]}',
            callback_data=movie_callback.new(item_name="movie", id_button=movie["id_kinopoisk"]))]
        # Добавляет полученную кнопку в список choice_movie_list
        choice_movie_list.append(button)

    return InlineKeyboardMarkup(inline_keyboard=choice_movie_list)
