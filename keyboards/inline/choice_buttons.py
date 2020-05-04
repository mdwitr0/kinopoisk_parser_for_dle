from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

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
