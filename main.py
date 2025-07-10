import asyncio
import os
from telethon import TelegramClient, events
from telegram import Bot
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

api_id = int(os.getenv('API_ID'))
api_hash = os.getenv('API_HASH')
BOT_TOKEN = os.getenv('BOT_TOKEN')
TARGET_CHANNEL = int(os.getenv('TARGET_CHANNEL'))  # Числовой ID канала
PHONE = os.getenv('PHONE')

bot = Bot(token=BOT_TOKEN)

def load_channels(filename):
    with open(filename, encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Укажи правильный путь к файлам со списками каналов!
priority_channels = load_channels('database/channels_priority.txt')
secondary_channels = load_channels('database/channels_secondary.txt')
all_channels = priority_channels + secondary_channels

def post_to_channel(text, source):
    msg = f"🚂 Новость из {source}:\n\n{text}\n\n#транспорт #жд"
    bot.send_message(chat_id=TARGET_CHANNEL, text=msg, disable_web_page_preview=True)

async def main():
    async with TelegramClient('main', api_id, api_hash) as client:
        @client.on(events.NewMessage(chats=all_channels))
        async def handler(event):
            # Публикуем только текстовые сообщения (можно доработать для медиа)
            if event.text:
                post_to_channel(event.text, event.chat.username or event.chat.title)
        print('Бот слушает все каналы из списков...')
        await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
