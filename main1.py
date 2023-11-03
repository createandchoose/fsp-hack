import telebot
import psycopg2
import time

# Подключение к базе данных PostgreSQL
conn = psycopg2.connect(
    database="default_db",
    user="admin",
    password="fsphack1",
    host="80.90.185.102",
    port="5432"
)
cursor = conn.cursor()

# Токен вашего бота
bot_token = '6947924117:AAGFMG2m5LkvTa8s3xyhavT3nWLZBi7jccE'
bot = telebot.TeleBot(bot_token)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Я начну отправлять данные из столбца asd каждые 10 секунд в течение 60 секунд.")
    for _ in range(6):  # Отправляем данные каждые 10 секунд в течение 60 секунд
        cursor.execute("SELECT data FROM asd")
        rows = cursor.fetchall()
        for row in rows:
            bot.send_message(message.chat.id, f"Данные из столбца asd: {row[0]}")
            time.sleep(1)

# Обработчик команды /stop
@bot.message_handler(commands=['stop'])
def handle_stop(message):
    bot.send_message(message.chat.id, "Остановлено.")
    bot.stop_polling()

# Запуск бота
bot.polling()