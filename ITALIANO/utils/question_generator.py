import telebot
import random
from config import TOKEN
import logging

bot = telebot.TeleBot(TOKEN)

questions = [
    {
        "photo": "https://avatars.mds.yandex.net/i?id=2a000001965dce205f6bca1177d9bf156d9f-1371038-fast-images&n=13",  # Замените на URL своей фотографии
        "question": "Кто изображен на фотографии?",
        "options": ["Бомбардиро Крокдило", "Тралалео Тралала", "Трипи Тропи", "Бобрито Бандито"],
        "correct_answer": "Тралалео Тралала"
    },
    {
        "photo": "https://static.life.ru/ip/unsafe/rs:fit:1200:/q:95/sh:0.5/czM6Ly9saWZlLXN0YXRpYy9wdWJsaWNhdGlvbnMvMjAyNS80LzIxLzI3Nzc3OTEzMTc3MC43Njc5LndlYnA=",  # Замените на URL своей фотографии
        "question": "Что это означает?",
        "options": ["Крокодилдо", "Крокодил", "Бомбардиро Крокодило", "Бомбини Гусини"],
        "correct_answer": "Бомбардиро Крокодило"
    },
    # Добавьте больше вопросов и фотографий
]

current_question = None  # Переменная для хранения текущего вопроса

def get_new_question(chat_id):
    global current_question
    try:
        current_question = random.choice(questions)
        photo = current_question["photo"]
        question = current_question["question"]
        options = current_question["options"]
        correct_answer = current_question["correct_answer"]

        markup = telebot.types.InlineKeyboardMarkup(row_width=2)
        random.shuffle(options)  # перемешать
        buttons = [telebot.types.InlineKeyboardButton(text=option, callback_data=option) for option in options]
        markup.add(*buttons)
        bot.send_photo(chat_id, photo=photo, caption=question, reply_markup=markup)
    except Exception as e:
        logging.error(f"Ошибка при отправке вопроса пользователю: {e}")
        bot.send_message(chat_id, "Произошла ошибка при получении вопроса. Попробуйте позже.")