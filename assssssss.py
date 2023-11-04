import telebot
import psycopg2
from psycopg2 import OperationalError
import time
from telebot import types

# Подключение к данных PostgreSQL🔥
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

@bot.message_handler(commands=['metrics'])
def send_metrics(message):
    try:
        # Подключение к базе данных PostgreSQL
        connection = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = connection.cursor()

        # Запросы к базе данных для получения метрик
        cursor.execute("SELECT max(now() - pg_stat_activity.query_start) FROM pg_stat_activity;")
        longest_transaction_duration = cursor.fetchone()[0]

        cursor.execute("SELECT count(*) FROM pg_stat_activity;")
        active_sessions_count = cursor.fetchone()[0]

        cursor.execute("SELECT count(*) FROM pg_stat_activity WHERE wait_event IS NOT NULL;")
        sessions_with_lwlock_count = cursor.fetchone()[0]

        # Получение метрик системы
        disk_free_space_gb = disk_free_space / (1024 ** 3)
        cpu_load = psutil.cpu_percent(interval=1)

        # Отправка сообщения с метриками в Telegram
        metrics_message = f"Продолжительность самой долгой транзакции: {longest_transaction_duration_ms} ms\n" \
                                f"Количество активных сессий: {active_sessions_count}\n" \
                                f"Количество сессий со значением LWLock в колонке wait_event: {sessions_with_lwlock_count}\n" \
                                f"Объём свободного места на диске: {disk_free_space_gb:.2f} GB\n" \
                                f"Загруженность процессора: {cpu_load}%"
        bot.send_message(message.chat.id, metrics_message)

        # Закрытие соединения с базой данных
        cursor.close()
        connection.close()

    except psycopg2.Error as e:
        # Обработка ошибок при работе с базой данных
        bot.send_message(message.chat.id, f"Ошибка при работе с базой данных: {e}")
    except Exception as e:
        # Обработка других ошибок
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}")


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, message.from_user.id, "Привет! Я бот, который следит за состоянием баз данных PostgreSQL.")
    

def check_database_status():
    message = bot.send_message
    if check_database_connection():
        print("База данных PostgreSQL работает нормально.")
        bot.send_message(463407972, "База данных PostgreSQL работает нормально.")
    else:
        print("Проблемы с базой данных PostgreSQL! Пожалуйста, проверьте ее состояние.")
        bot.send_message(463407972, "Проблемы с базой данных PostgreSQL! Пожалуйста, проверьте ее состояние.")

# Периодическая проверка состояния баз данных каждые 10 минут
while True:
    check_database_status()
    time.sleep(15)