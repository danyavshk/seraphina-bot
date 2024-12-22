import os
import asyncio
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from app.handlers import router


class TelegramBot:
    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
        )
        self.logger = logging.getLogger(__name__)
        
        load_dotenv()
        self.bot = Bot(token=os.getenv('TG_TOKEN'))
        self.dispatcher = Dispatcher()

    def setup_handlers(self):
        self.dispatcher.include_router(router)
        self.logger.info("Обработчики маршрутов зарегистрированы.")

    async def start(self):
        self.setup_handlers()
        try:
            self.logger.info("Бот запущен и готов к работе.")
            await self.dispatcher.start_polling(self.bot)
        except asyncio.CancelledError:
            self.logger.warning("Операция была отменена.")
        except Exception as e:
            self.logger.error(f"Произошла ошибка: {e}")
        finally:
            await self.shutdown()

    async def shutdown(self):
        self.logger.info("Завершение работы бота...")
        await self.bot.session.close()
        self.logger.info("Сессия бота закрыта. Бот успешно остановлен.")


if __name__ == '__main__':
    bot_instance = TelegramBot()
    try:
        asyncio.run(bot_instance.start())
    except KeyboardInterrupt:
        logging.warning("Бот выключен пользователем.")
