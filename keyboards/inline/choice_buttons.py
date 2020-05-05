from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline.callback_datas import movie_callback

run_choice = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="📄 Добавить описание и опубликовать 📄", callback_data="add_text"),
    ],
    [
        InlineKeyboardButton(text="📺 Опубликовать на сайте 📺", callback_data="run_sender")
    ]
])

running = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="⏳ Публикую ⏳", callback_data="running"),
    ]
])


def url_movies(url):
    url_movie = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Опубликовано ✅", url=url)
        ]
    ])
    return url_movie


type_choice = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text="Фильм 👈", callback_data="movies"),
        InlineKeyboardButton(text="👉 Сериал", callback_data="tv-series"),
    ]
])


def movie_list(json):
    choice_movie_list = []
    for movie in json:
        button = [InlineKeyboardButton(
            text=f'{movie["title"]} {movie["year"]}',
            callback_data=movie_callback.new(item_name="movie", id_button=movie["id_kinopoisk"]))]
        choice_movie_list.append(button)

    return InlineKeyboardMarkup(inline_keyboard=choice_movie_list)