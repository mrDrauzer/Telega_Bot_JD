from telethon.sync import TelegramClient
from config import Config
from database.db import get_connection
import asyncio
import logging

logger = logging.getLogger(__name__)


async def parse_channels():
    conn = get_connection()
    cursor = conn.cursor()

    # Авторизация как пользователь (не как бот!)
    client = TelegramClient(
        'news_parser',
        Config.API_ID,
        Config.API_HASH,
        system_version="4.16.30-vxCustom"
    )

    try:
        await client.start(phone=Config.PHONE)  # Используем номер телефона

        for channel in Config.TELEGRAM_CHANNELS:
            try:
                async for message in client.iter_messages(channel, limit=50):
                    if not message.text:
                        continue

                    if any(kw.lower() in message.text.lower() for kw in Config.KEYWORDS):
                        url = f"https://t.me/{channel}/{message.id}"

                        # Проверяем по URL и заголовку
                        cursor.execute("""
                            SELECT 1 FROM news 
                            WHERE url = ? OR title = ?
                        """, (url, message.text[:200]))

                        if not cursor.fetchone():
                            cursor.execute(
                                "INSERT INTO news (title, url, source) VALUES (?, ?, ?)",
                                (message.text[:200], url, channel)
                            )
                            conn.commit()
                            logger.info(f"Новая новость: {message.text[:50]}...")
                            yield message.text, channel
                        else:
                            logger.debug(f"Дубликат пропущен: {url}")

            except Exception as e:
                logger.error(f"Ошибка в канале {channel}: {str(e)}")
                continue

    finally:
        await client.disconnect()
        conn.close()