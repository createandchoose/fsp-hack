import telebot
import psycopg2
import matplotlib.pyplot as plt
import io
import datetime
from telebot import types
# Замените значения переменных на свои параметры баз данных PostgreSQL

DB_PORT = '5432'
DB_HOST = "80.90.185.102"
DB_NAME = "default_db"
DB_USER = "admin"
DB_PASSWORD = "fsphack1"

# Токен вашего Telegram бота
TELEGRAM_TOKEN = "6947924117:AAGFMG2m5LkvTa8s3xyhavT3nWLZBi7jccE"

# Инициализация бота
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Функция для проверки соединения с базой данных
def check_database_connection():
    try:
        conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        cur = conn.cursor()
        cur.execute('SELECT 1')  # Простой запрос для проверки соединения
        cur.close()
        conn.close()
        return True
    except psycopg2.Error as e:
        print(f'Ошибка соединения с базой данных: {e}')
        return False

# Функция для создания и отправки графика в формате png
def send_plot(chat_id, data):
    plt.figure(figsize=(8, 6))
    dates = [item['date'] for item in data]
    values = [item['value'] for item in data]
    plt.plot(dates, values, marker='o')
    plt.xlabel('Дата и время')
    plt.ylabel('Значение')
    plt.title('График состояния базы данных')
    plt.xticks(rotation=45)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    bot.send_photo(chat_id, photo=buf)

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Начать")
    markup.add(btn1)
    bot.send_message(message.from_user.id, "Привет давай начнем", reply_markup=markup)
    # bot.send_message(message.chat.id, 'Привет! Я бот для мониторинга состояния баз данных PostgreSQL.')

# Функция для проверки состояния баз данных и отправки уведомлений
def check_database_status():
    while True:
        if not check_database_connection():
            # Если соединение с базой данных утеряно, отправляем уведомление
            bot.send_message(admin_chat_id, '⚠️ Проблемы с соединением к базе данных!')
            print("⚠️ Проблемы с соединением к базе данных!")
            # Создаем и отправляем график состояния базы данных
            data = [{'date': str(datetime.datetime.now()), 'value': 0}]  # Замените это на данные графика
            send_plot(admin_chat_id, data)
            # Здесь можно добавить дополнительные действия для восстановления
        else:
            # Если соединение с базой данных в порядке, отправляем уведомление об этом
            bot.send_message(admin_chat_id, '✅ Соединение с базой данных в норме.')
            print("✅ Соединение с базой данных в норме.")
        # Периодичность проверки состояния базы данных (в секундах)
        time.sleep(15)  # Например, каждую минуту

# Замените admin_chat_id на ID чата администратора
admin_chat_id = '463407972'

# Запускаем функцию проверки состояния баз данных в отдельном потоке
import threading
import time
check_thread = threading.Thread(target=check_database_status)
check_thread.start()

# Запуск бота
bot.polling(none_stop=True)
