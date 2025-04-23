import os
from dotenv import load_dotenv

load_dotenv()  # Загружаем переменные окружения из .env файла

TOKEN = os.environ.get("BOT_TOKEN")  # Получаем токен из переменной окружения
DB_HOST = os.environ.get("DB_HOST") or "localhost"  # Хост БД
DB_USER = os.environ.get("DB_USER")  # Имя пользователя БД
DB_PASSWORD = os.environ.get("DB_PASSWORD")  # Пароль БД
DB_NAME = os.environ.get("DB_NAME")  # Имя базы данных

# Если не указаны переменные окружения, используем значения по умолчанию
if not TOKEN:
    print("Ошибка: Не указан токен бота в переменных окружения!")
    exit()