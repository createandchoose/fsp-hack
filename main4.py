import telebot
import psycopg2
import subprocess
import time

# Токен вашего бота в Telegram
TOKEN = '6947924117:AAGFMG2m5LkvTa8s3xyhavT3nWLZBi7jccE'

# Параметры подключения к PostgreSQL базе данных
DB_PORT = '5432'
DB_HOST = "80.90.185.102"
DB_NAME = "default_db"
DB_USER = "admin"
DB_PASSWORD = "fsphack1"


# Идентификатор администратора (пользователя, которому будут отправляться уведомления)
admin_user_id = '463407972'
bot = telebot.TeleBot(TOKEN)

def check_postgresql_metrics():
    try:
        connection = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
        cursor = connection.cursor()

        # Пример SQL запроса для получения количества активных сессий
        cursor.execute("SELECT COUNT(*) FROM pg_stat_activity WHERE state = 'active';")
        active_sessions = cursor.fetchone()[0]

        # Пример SQL запроса для получения продолжительности самой долгой транзакции
        cursor.execute("SELECT max(now() - pg_stat_activity.query_start) FROM pg_stat_activity;")
        longest_transaction_duration = cursor.fetchone()[0]

        # Здесь можно добавить другие SQL запросы для получения метрик из базы данных

        connection.close()

        return active_sessions, longest_transaction_duration
    except psycopg2.Error as e:
        raise Exception("Ошибка PostgreSQL: " + str(e))
    except Exception as e:
        raise Exception("Ошибка: " + str(e))

def send_notification(message):
    bot.send_message(admin_user_id, message)

def main_loop():
    while True:
        try:
            active_sessions, longest_transaction_duration = check_postgresql_metrics()
            bot.send_message(admin_user_id, '✅ Соединение с базой данных в норме.',)
            print(f"Aктивных сессий: {active_sessions}, самая долгая транзакция: {longest_transaction_duration}")

            # Условие для определения проблемы (например, если активных сессий больше 10)
            if active_sessions > 10:
                message = f"Проблема с PostgreSQL базой данных! Активных сессий: {active_sessions}, " \
                          f"самая долгая транзакция: {longest_transaction_duration}"
                send_notification(message)

                # Здесь можно добавить дополнительные действия для восстановления корректной работы базы данных
                # Например, вызвать команду checkpoint и перезапустить базу данных:
                # subprocess.run(["pg_ctl", "-D", "/path/to/your/postgres/data", "checkpoint"])
                # subprocess.run(["pg_ctl", "-D", "/path/to/your/postgres/data", "restart"])

        except Exception as e:
            print("Возникла ошибка:", e)
            bot.send_message(admin_user_id, '⚠️ Проблемы с соединением к базе данных!',)

        # Проверка каждые 15 секунд
        time.sleep(15)

if __name__ == "__main__":
    # Запускаем основной цикл
    main_loop()