from aiogram import Dispatcher
from app.bot.routers import start

def get_dispatcher() -> Dispatcher:
    dp = Dispatcher()
    # Регистрируем роутеры (порядок важен: сначала специфичные)
    dp.include_router(start.router)
    return dp