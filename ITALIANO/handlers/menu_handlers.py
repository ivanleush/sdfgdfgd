# handlers/menu_handlers.py
import telebot
from config import TOKEN
from utils import database, question_generator
import logging

bot = telebot.TeleBot(TOKEN)

def get_user_profile(message):
    user_id = message.from_user.id
    # Получаем имя пользователя:
    if message.from_user.first_name:
        username = message.from_user.first_name
        if message.from_user.last_name:
            username += " " + message.from_user.last_name  # Добавляем фамилию, если есть
    elif message.from_user.username:
        username = message.from_user.username
    else:
        username = "Не указано"  # Если нет ни имени, ни username

    try:
        score = database.get_user_score(user_id)
        profile_text = f"Имя: {username}\nID: {user_id}\nБаллы: {score}"
        bot.send_message(message.chat.id, profile_text)
    except Exception as e:
        logging.error(f"Ошибка при получении профиля пользователя {user_id}: {e}")
        bot.send_message(message.chat.id, "Произошла ошибка при получении профиля.")


# Функция для получения рейтинга (ТОП-10)
def get_rating(message):
    try:
        top_users = database.get_top_users()  # Получаем ТОП-10 пользователей из БД
        logging.info(f"top_users received: {top_users}") # Добавили логирование
        rating_text = "Топ 10 пользователей:\n"
        for i, user in enumerate(top_users):
            username = user['username']
            score = user['score']
            rating_text += f"{i+1}. {username}: {score}\n"
        bot.send_message(message.chat.id, rating_text)
    except Exception as e:
        logging.error(f"Ошибка при получении рейтинга: {e}")
        bot.send_message(message.chat.id, "Произошла ошибка при получении рейтинга.")


# Обработчик текстовых сообщений (для обработки нажатий кнопок меню)
@bot.message_handler(func=lambda message: True)
def handle_menu(message):
    if message.text == "Мой профиль":
        get_user_profile(message)
    elif message.text == "Рейтинг":
        get_rating(message)
    elif message.text == "Начало":
        question_generator.get_new_question(message.chat.id)


def create_main_menu():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = telebot.types.KeyboardButton("Мой профиль")
    item2 = telebot.types.KeyboardButton("Рейтинг")
    item3 = telebot.types.KeyboardButton("Начало")
    markup.add(item1, item2, item3)
    return markup