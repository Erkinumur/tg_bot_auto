from loader import bot, storage
from config import admins

from logger import log_decorator


async def on_startup(dp):
    import middlewares
    middlewares.setup(dp)

    for admin in admins:
        await bot.send_message(admin, "Я запущен!")


async def on_shutdown(dp):
    await bot.close()
    await storage.close()


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)

