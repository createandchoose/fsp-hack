import psycopg2
import telegram
from telegram.ext import *
import paramiko
import time

# Установка состояний для ConversationHandler
CHOOSING, METRIC, RECOVERY = range(3)

# Задаем токен бота и ID администратора
TOKEN = '6947924117:AAGFMG2m5LkvTa8s3xyhavT3nWLZBi7jccE'
ADMIN_CHAT_ID = '463407972'

# Параметры подключения к PostgreSQL базе данных
DB_HOST = '80.90.185.102'
DB_PORT = '5432'
DB_NAME = 'default_db'
DB_USER = 'admin'
DB_PASSWORD = 'fsphack1'

# Параметры SSH подключения к серверу
SSH_HOST = 'YOUR_SSH_HOST'
SSH_PORT = 'YOUR_SSH_PORT'
SSH_USER = 'YOUR_SSH_USER'
SSH_PASSWORD = 'YOUR_SSH_PASSWORD'

# Параметры для определения метрик
METRIC_QUERIES = {
    'longest_transaction': 'SELECT max(now() - xact_start) FROM pg_stat_activity;',
    'active_sessions': 'SELECT count(*) FROM pg_stat_activity WHERE state = \'active\';',
    # Добавьте другие метрики здесь
}

# Функция для отправки сообщений в Telegram
def send_message(update, context, message):
    context.bot.send_message(chat_id=update.message.chat_id, text=message)

# Команда /start начинает диалог с пользователем
def start(update, context):
    update.message.reply_text(
        "Привет! Я бот для отслеживания состояния баз данных PostgreSQL. "
        "Чтобы получить метрику, используйте команду /metrics. "
        "Для восстановления корректной работы базы используйте команду /recovery."
    )
    return CHOOSING

# Команда /metrics предоставляет доступ к метрикам базы данных
def metrics(update, context):
    keyboard = [['Продолжительность самой долгой транзакции', 'Количество активных сессий'],
                ['Количество сессий со значением LWLock в колонке wait_event', 'Объём свободного места на диске'],
                ['Загруженность процессора']]
    update.message.reply_text("Выберите метрику:", reply_markup=telegram.ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
    return METRIC

# Функция для получения метрики из базы данных PostgreSQL
def get_metric(metric_name):
    conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    cur = conn.cursor()
    cur.execute(METRIC_QUERIES[metric_name])
    result = cur.fetchone()[0]
    cur.close()
    conn.close()
    return result

# Команда /recovery восстанавливает корректную работу базы данных
def recovery(update, context):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=SSH_HOST, port=SSH_PORT, username=SSH_USER, password=SSH_PASSWORD)
    
    ssh.exec_command('pg_ctl restart -D /path/to/postgresql/data')
    ssh.close()
    
    send_message(update, context, "База данных восстановлена.")
    return ConversationHandler.END

# Функция обработки выбора метрики
def choose_metric(update, context):
    metric_name = update.message.text
    try:
        metric_value = get_metric(metric_name.lower())
        send_message(update, context, f"{metric_name}: {metric_value}")
    except Exception as e:
        send_message(update, context, f"Ошибка при получении метрики: {e}")
    return ConversationHandler.END

# Функция обработки неизвестных команд
def unknown(update, context):
    send_message(update, context, "Извините, я не понимаю эту команду.")

# Функция для проверки состояния базы данных каждые 15 секунд
def check_database(context: CallbackContext):
    try:
        # Проверка метрик и уведомление администратора при необходимости
        # Добавьте код для проверки метрик и уведомления администратора здесь
        pass
    except Exception as e:
        # Ошибка при проверке метрик, уведомление администратора
        send_message(context.job.context, f"Ошибка при проверке метрик: {e}")

# Основная функция бота
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Добавляем обработчики команд
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CHOOSING: [MessageHandler(Filters.regex('^Метрики$'), metrics)],
            METRIC: [MessageHandler(Filters.regex('^(Продолжительность самой долгой транзакции|Количество активных сессий|Количество сессий со значением LWLock в колонке wait_event|Объём свободного места на диске|Загруженность процессора)$'), choose_metric)],
            RECOVERY: [MessageHandler(Filters.regex('^Восстановить базу данных$'), recovery)]
        },
        fallbacks=[],
        map_to_parent={
            CHOOSING: CHOOSING,
            METRIC: CHOOSING,
            RECOVERY: CHOOSING
        }
    )
    dp.add_handler(conv_handler)
    dp.add_handler(MessageHandler(Filters.command, unknown))

    # Запускаем проверку состояния базы данных каждые 15 секунд
    job_queue = updater.job_queue
    job_queue.run_repeating(check_database, interval=15, first=0, context=updater)

    # Запускаем бота
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
