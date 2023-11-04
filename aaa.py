import psycopg2
import telegram
from telegram.ext import Updater, CommandHandler, JobQueue
from telegram.ext import MessageHandler, Filters
from telegram.ext import CallbackContext
import logging
import os

# Устанавливаем уровень логирования (DEBUG, INFO, WARNING, ERROR, CRITICAL)
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Токен вашего Telegram бота
TELEGRAM_BOT_TOKEN = "6947924117:AAGFMG2m5LkvTa8s3xyhavT3nWLZBi7jccE"

# Данные для подключения к PostgreSQL базе данных
DB_HOST = "80.90.185.102"
DB_PORT = '5432'
DB_NAME = "default_db"
DB_USER = "admin"
DB_PASSWORD = "fsphack1"


# Устанавливаем интервал проверки базы данных (в секундах)
CHECK_INTERVAL = 15

# Функция для проверки состояния базы данных PostgreSQL
def check_database_status():
    try:
        conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        cur = conn.cursor()
        # Здесь можно добавить SQL-запросы для проверки состояния базы данных
        # Например: cur.execute("SELECT COUNT(*) FROM your_table;")
        # Проверьте результаты запросов и определите, что считать проблемой
        cur.execute("SELECT 1;")
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        logger.error(f"Ошибка при проверке базы данных: {e}")
        return False

# Функция, которая будет выполняться при команде /start
def start(update, context):
    update.message.reply_text("Привет! Я бот для отслеживания состояния баз данных PostgreSQL.")

# Функция для отправки уведомлений администратору
def send_notification(context: CallbackContext):
    chat_id = context.job.context
    if not check_database_status():
        context.bot.send_message(chat_id=chat_id, text="Проблемы с базой данных PostgreSQL!")

# Главная функция для запуска бота
def main():
    # Создаем объекты для взаимодействия с Telegram API и PostgreSQL
    updater = Updater(token=TELEGRAM_BOT_TOKEN)
    dispatcher = updater.dispatcher
    job_queue = JobQueue()

    # Добавляем команды для бота
    dispatcher.add_handler(CommandHandler("start", start))

    # Устанавливаем задачу для периодической проверки базы данных
    job_queue.run_repeating(send_notification, interval=CHECK_INTERVAL, first=0, context=dispatcher.chat_id)

    # Запускаем бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
