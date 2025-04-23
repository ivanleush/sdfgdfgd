import telebot
from config import TOKEN
from handlers import menu_handlers
import logging

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    logging.info(f"Пользователь {message.from_user.id} запустил бота")  # Логируем запуск
    markup = menu_handlers.create_main_menu()
    bot.send_message(message.chat.id, "Добро пожаловать в викторину 'Итальянские животные'!", reply_markup=markup)