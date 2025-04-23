import telebot
from config import TOKEN
from utils import database, question_generator  # Импортируем question_generator и database
import logging

bot = telebot.TeleBot(TOKEN)


# Обработчик нажатия inline-кнопок (ответа пользователя)
@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    user_id = call.from_user.id  # Получаем ID пользователя
    username = call.from_user.first_name if call.from_user.first_name else call.from_user.username  # Получаем username
    try:
        if call.data == question_generator.current_question["correct_answer"]:
            bot.send_message(call.message.chat.id, "Правильно! +1 балл")
            database.update_user_score(user_id, username, 1)  # Обновляем счет в БД, передаем username
        else:
            bot.send_message(call.message.chat.id,
                             f"Неправильно! Правильный ответ: {question_generator.current_question['correct_answer']} (-1 балл)")
            database.update_user_score(user_id, username, -1)  # Обновляем счет в БД, передаем username

        question_generator.get_new_question(call.message.chat.id)  # Отправляем следующий вопрос
    except Exception as e:
        logging.error(f"Ошибка при обработке ответа пользователя {user_id}: {e}")
        bot.send_message(call.message.chat.id, "Произошла ошибка при обработке ответа.")