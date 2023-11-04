import telebot
import psycopg2
import psutil

# Замените значения переменных ниже на свои данные
TELEGRAM_BOT_TOKEN = '6947924117:AAGFMG2m5LkvTa8s3xyhavT3nWLZBi7jccE'
POSTGRES_DB_HOST = '80.90.185.102'
POSTGRES_DB_NAME = 'default_db'
POSTGRES_DB_USER = 'admin'
POSTGRES_DB_PASSWORD = 'fsphack1'

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)

@bot.message_handler(commands=['metrics'])
def send_metrics(message):
    try:
        connection = psycopg2.connect(
            host=POSTGRES_DB_HOST,
            database=POSTGRES_DB_NAME,
            user=POSTGRES_DB_USER,
            password=POSTGRES_DB_PASSWORD
        )
        cursor = connection.cursor()
        cursor.execute("SELECT max(now() - pg_stat_activity.query_start) FROM pg_stat_activity;")
        longest_transaction_duration = cursor.fetchone()[0]

        cursor.execute("SELECT count(*) FROM pg_stat_activity;")
        active_sessions_count = cursor.fetchone()[0]

        cursor.execute("SELECT count(*) FROM pg_stat_activity WHERE wait_event IS NOT NULL;")
        sessions_with_lwlock_count = cursor.fetchone()[0]
        
        disk_free_space_gb = disk_free_space / (1024 ** 3)
        cpu_load = psutil.cpu_percent(interval=1)

        metrics_message = f"Продолжительность самой долгой транзакции: {longest_transaction_duration_ms} ms\n" \
                                f"Количество активных сессий: {active_sessions_count}\n" \
                                f"Количество сессий со значением LWLock в колонке wait_event: {sessions_with_lwlock_count}\n" \
                                f"Объём свободного места на диске: {disk_free_space_gb:.2f} GB\n" \
                                f"Загруженность процессора: {cpu_load}%"
        bot.send_message(message.chat.id, metrics_message)

        cursor.close()
        connection.close()

    except psycopg2.Error as e:
        bot.send_message(message.chat.id, f"Ошибка при работе с базой данных: {e}")
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {e}")

bot.polling()