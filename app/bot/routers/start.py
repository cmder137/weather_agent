import logging
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

logger = logging.getLogger(__name__)
router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    logger.info(f"User {message.from_user.id} triggered /start")
    await message.answer(
        "Привет! Я AI-агент погоды. 🌤️\n"
        "Отправь мне название города или поделись геолокацией, "
        "и я расскажу о погоде, используя нейросеть."
    )

@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer(
        "Доступные команды:\n"
        "/start - Запустить бота\n"
        "/help - Справка\n\n"
        "Или просто напиши название города, например: <b>Москва</b>",
        parse_mode="HTML"
    )