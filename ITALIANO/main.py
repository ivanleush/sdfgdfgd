import telebot
from config import TOKEN
from utils import database, question_generator
from handlers import menu_handlers, callback_handlers
import logging

# Инициализация логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Инициализация бота
bot = telebot.TeleBot(TOKEN)

# Инициализация базы данных
database.init_db()

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = menu_handlers.create_main_menu()  # Создаем главное меню
    bot.send_message(message.chat.id, "Привет! Это викторина по итальянским мемам.", reply_markup=markup)
    question_generator.get_new_question(message.chat.id) # Отправляем первый вопрос

menu_handlers.bot = bot

# Запуск бота
if __name__ == '__main__':
    logging.info("Bot starting...")
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.error(f"Ошибка при запуске бота: {e}")