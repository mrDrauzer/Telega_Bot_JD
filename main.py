from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import Config
from database.db import init_db
from parsers.telegram_parser import parse_channels
from datetime import datetime
import asyncio
import logging
from dotenv import load_dotenv
import os

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Инициализация бота с HTML-разметкой по умолчанию
bot = Bot(
    token=Config.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())
scheduler = AsyncIOScheduler()


async def check_channel_access():
    """Проверка доступности канала и прав бота"""
    try:
        chat = await bot.get_chat(Config.CHANNEL_ID)
        logger.info(f"✅ Канал найден: {chat.title}")
        logger.info(f"ID: {chat.id}")
        logger.info(f"Тип: {chat.type}")

        me = await bot.get_me()
        member = await bot.get_chat_member(chat.id, me.id)
        if member.status == "administrator":
            logger.info("✅ Бот является администратором")
        else:
            logger.error("❌ Бот НЕ администратор!")
            raise Exception("Bot is not an admin in the channel")

    except Exception as e:
        logger.critical(f"❌ Критическая ошибка доступа к каналу: {repr(e)}")
        raise


async def post_to_channel(text: str, source: str):
    """Отправка сообщения в канал"""
    try:
        logger.info(f"Попытка отправить сообщение в канал {Config.CHANNEL_ID}")
        await bot.send_message(
            chat_id=Config.CHANNEL_ID,
            text=f"🚂 Новость из {source}:\n\n{text}\n\n#транспорт #жд",
            disable_web_page_preview=True
        )
        logger.info("Сообщение успешно отправлено")
    except Exception as e:
        logger.error(f"Ошибка отправки: {str(e)}")
        raise


async def scheduled_parse():
    """Планируемый парсинг"""
    logger.info("Запуск scheduled_parse")
    try:
        async for text, source in parse_channels():
            logger.info(f"Найдена новость: {text[:50]}...")
            await post_to_channel(text, source)
    except Exception as e:
        logger.error(f"Ошибка в scheduled_parse: {str(e)}")


@dp.message(Command("test"))
async def test_message(message: types.Message):
    """Тестовая команда для проверки работы"""
    try:
        test_text = (
            "⚠️ Тестовое сообщение от бота\n"
            f"ID канала: {Config.CHANNEL_ID}\n"
            f"Время: {datetime.now()}"
        )

        await bot.send_message(
            chat_id=Config.CHANNEL_ID,
            text=test_text,
            disable_web_page_preview=True
        )
        await message.answer("✅ Тест успешен! Сообщение отправлено в канал")
    except Exception as e:
        error_msg = (
            f"❌ Ошибка: {str(e)}\n\n"
            "Проверьте:\n"
            "1. Бот добавлен как админ в канал?\n"
            "2. CHANNEL_ID корректный?\n"
            f"3. Текущий ID: {Config.CHANNEL_ID}"
        )
        await message.answer(error_msg)
        logger.error(f"Ошибка в test_message: {str(e)}")


@dp.message(Command("parse"))
async def manual_parse(message: types.Message):
    """Ручной запуск парсинга"""
    await message.answer("⏳ Начинаю парсинг...")
    try:
        await scheduled_parse()
        await message.answer("✅ Парсинг завершён")
    except Exception as e:
        await message.answer(f"❌ Ошибка при парсинге: {str(e)}")
        logger.error(f"Ошибка в manual_parse: {str(e)}")


async def on_startup():
    """Действия при запуске бота"""
    logger.info("Запуск on_startup")
    try:
        await check_channel_access()  # Проверка доступа к каналу
        init_db()
        scheduler.add_job(scheduled_parse, 'interval', minutes=1)
        scheduler.start()
        logger.info("Планировщик запущен")
    except Exception as e:
        logger.critical(f"Ошибка при запуске: {str(e)}")
        raise


async def main():
    """Основная функция запуска"""
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, on_startup=on_startup)


if __name__ == '__main__':
    logger.info("Запуск бота")
    try:
        asyncio.run(main())
    except Exception as e:
        logger.critical(f"Критическая ошибка: {str(e)}")