import paramiko
import psycopg2
from psycopg2 import sql

def ssh_connect(host, port, username, password):
    host = '94.228.123.59'
    port = 22
    username = 'root'
    password = 'p9xiwE5t@HPt^B'

if ssh_connect(host, port, username, password):
    print("Подключение успешно установлено!")
else:
    print("Не удалось установить подключение.")

def get_postgresql_version(host, port, username, password):
    cursor = None
    connection = None
    
    try:
        # Устанавливаем SSH-соединение
        ssh_connect(host, port, username, password)

        # Подключаемся к PostgreSQL на удаленном сервере
        connection = psycopg2.connect(
            dbname='test',
            user='admin',
            password='admin',
            host='127.0.0.1'  # Хост можно указать как localhost, если PostgreSQL на том же сервере, где и SSH-соединение
        )

        # Создаем курсор для выполнения SQL-запросов
        cursor = connection.cursor()

        # Выполняем запрос для получения версии PostgreSQL
        cursor.execute(sql.SQL("SELECT version()"))

        # Получаем результат запроса
        version = cursor.fetchone()[0]

        # Возвращаем версию PostgreSQL
        return version
    except Exception as e:
        print(f"Ошибка при получении версии PostgreSQL: {e}")
        return None
    finally:
        # Закрываем соединения
        if cursor:
            cursor.close()
        if connection:
            connection.close()

# Задаем параметры подключения к серверу
host = '94.228.123.59'
port = 22
username = 'root'
password = 'hicU?BnqfUAy64'

# Вызываем функцию для получения версии PostgreSQL
postgresql_version = get_postgresql_version(host, port, username, password)

if postgresql_version:
    print(f"Версия PostgreSQL на сервере: {postgresql_version}")
else:
    print("Не удалось получить версию PostgreSQL.")