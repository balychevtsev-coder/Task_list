# config.py
# Файл конфигурации бота

import os
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

# Токен бота (получите у @BotFather в Telegram)
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

# Путь к базе данных
DATABASE_PATH = 'tasks.db'

