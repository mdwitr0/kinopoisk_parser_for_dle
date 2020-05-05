from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from keyboards.default import menu
from loader import dp


@dp.message_handler(Command("start"), state="*")
async def start(message: Message):
    """
    Отправлет пользователю кнопки
    """
    await message.answer("Выберите действие", reply_markup=menu)
