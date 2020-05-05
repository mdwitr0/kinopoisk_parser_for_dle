from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Стандартные кнопки меню
menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Поиск по ID 🔎"),
            KeyboardButton(text="Поиск по названию 🔎")
        ],
    ],
    resize_keyboard=True
)
