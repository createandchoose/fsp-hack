import psycopg2
import logging
import time
from telegram import Bot
from telegram.ext import Updater, CommandHandler

conn = psycopg2.connect(
    dbname="default_db",
    user="admin",
    password="fsphack1",
    host="80.90.185.102",
    port="5432"
)


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

def send_messages(context):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM asd")
    rows = cursor.fetchall()
    for row in rows:
        user_id = row[0]  
        message = "Состояние базы данных: {}".format(row[1]) 
        bot = context.job.context
        bot.send_message(chat_id=user_id, text=message)

def start(update, context):
    update.message.reply_text('Бот запущен и будет отправлять вам сообщения каждые 15 секунд.')

bot_token = '6947924117:AAGFMG2m5LkvTa8s3xyhavT3nWLZBi7jccE'
updater = Updater(token=bot_token, use_context=True)

updater.dispatcher.add_handler(CommandHandler('start', start))

updater.start_polling()

job_queue = updater.job_queue
job_queue.run_repeating(send_messages, interval=15, context=updater.bot)

updater.idle()
