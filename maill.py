import telebot 
from telebot import types
import psycopg2
from psycopg2 import OperationalError

# Подключение к данным PostgreSQL
DB_HOST = "80.90.185.102"
DB_NAME = "default_db"
DB_USER = "admin"
DB_PASSWORD = "fsphack1"

# Токен вашего Telegram бота
TELEGRAM_BOT_TOKEN = "6271062024:AAFbIlidnd_V_CRbAAHFHplQT5qigmeqyPs"

# Инициализация бота
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

# Функция для проверки состояния базы данных
def check_database_connection():
    try:
        connection = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        connection.close()
        return True
    except OperationalError:
        return False

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который следит за состоянием баз данных PostgreSQL.")

# Обработчик команды /status
@bot.message_handler(commands=['status'])
def handle_status(message):
    if check_database_connection():
        bot.send_message(message.chat.id, "База данных PostgreSQL работает нормально.")
    else:
        bot.send_message(message.chat.id, "Проблемы с базой данных PostgreSQL! Пожалуйста, проверьте ее состояние.")


# Запуск бота
bot.polling()