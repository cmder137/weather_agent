import asyncio
import logging
from aiogram import Bot
from app.bot.dispatcher import get_dispatcher
from app.core.config import settings

# Настройка базового логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)


async def main():
    bot = Bot(token=settings.TELEGRAM_BOT_TOKEN)
    dp = get_dispatcher()

    logging.info("Starting bot...")
    try:
        # Запуск бота в режиме Long Polling
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())