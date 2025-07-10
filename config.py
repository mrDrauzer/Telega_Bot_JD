from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    PHONE = os.getenv("PHONE")  # Теперь PHONE есть в Config
    API_ID = int(os.getenv("API_ID"))
    API_HASH = os.getenv("API_HASH")
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    CHANNEL_ID = int(os.getenv("CHANNEL_ID"))

    KEYWORDS = ['ВСМ', 'Груз', 'РЖД', 'Логистика', 'Перевозки', 'Транспорт']

    TELEGRAM_CHANNELS = [
        '@rollingstock', '@Vgudok', '@gudokru',
        '@rzd_partner_news', '@today1520', '@telerzd'
    ]

    NEWS_SITES = {
        'Коммерсантъ': 'https://www.kommersant.ru/search?q=',
        'РБК': 'https://www.rbc.ru/search/?query=',
        'ТАСС': 'https://tass.ru/search?text='
    }

# Проверка
print("Config.PHONE:", Config.PHONE)
print("Config.API_ID:", Config.API_ID)