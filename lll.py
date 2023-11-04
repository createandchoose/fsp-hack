import psycopg2
import logging
import time
from telegram import Bot
from telegram.ext import Updater, CommandHandler

# Устанавливаем соединение с базой данных PostgreSQL
conn = psycopg2.connect(
    dbname="default_db",
    user="admin",
    password="fsphack1",
    host="80.90.185.102",
    port="5432"
)


# Настраиваем логирование
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Функция для отправки сообщений пользователям
def send_messages(context):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM asd")
    rows = cursor.fetchall()
    for row in rows:
        user_id = row[0]  # предположим, что user_id находится в первом столбце таблицы
        message = "Состояние базы данных: {}".format(row[1])  # предположим, что состояние находится во втором столбце таблицы
        bot = context.job.context
        bot.send_message(chat_id=user_id, text=message)

# Обработчик команды /start
def start(update, context):
    update.message.reply_text('Бот запущен и будет отправлять вам сообщения каждые 15 секунд.')

# Создаем бота и передаем ему токен
bot_token = '6947924117:AAGFMG2m5LkvTa8s3xyhavT3nWLZBi7jccE'
updater = Updater(token=bot_token, use_context=True)

# Регистрируем обработчики команд
updater.dispatcher.add_handler(CommandHandler('start', start))

# Запускаем бота
updater.start_polling()

# Планируем выполнение функции send_messages каждые 15 секунд
job_queue = updater.job_queue
job_queue.run_repeating(send_messages, interval=15, context=updater.bot)

# Бот будет работать до принудительной остановки
updater.idle()
