import telebot
import psycopg2
from psycopg2 import OperationalError
import time
from telebot import types

# Подключение к данным PostgreSQL🔥
DB_HOST = "80.90.185.102"
DB_NAME = "default_db"
DB_USER = "admin"
DB_PASSWORD = "fsphack1"

# Токен вашего Telegram бота
TELEGRAM_BOT_TOKEN = "6947924117:AAGFMG2m5LkvTa8s3xyhavT3nWLZBi7jccE"

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
    bot.send_message(message.chat.id, message.from_user.id, "Привет! Я бот, который следит за состоянием баз данных PostgreSQL.")
    if check_database_connection():
        bot.send_message(message.chat.id, "База данных PostgreSQL работает нормально.")
        print("База данных PostgreSQL работает нормально.")
    else:
        bot.send_message(message.chat.id, "Проблемы с базой данных PostgreSQL! Пожалуйста, проверьте ее состояние.")
        print("FFFF")

def check_database_status():
    if check_database_connection():
        print("База данных PostgreSQL работает нормально.")
        bot.send_message(6947924117, "База данных PostgreSQL работает нормально.")
    else:
        print("Проблемы с базой данных PostgreSQL! Пожалуйста, проверьте ее состояние.")
        bot.send_message(6947924117, "Проблемы с базой данных PostgreSQL! Пожалуйста, проверьте ее состояние.")

# Периодическая проверка состояния баз данных каждые 10 минут
while True:
    check_database_status()
    time.sleep(15)  # Ждать 10 минут (600 секунд)