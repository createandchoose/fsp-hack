import paramiko
import psycopg2

# Параметры для подключения к серверу
ssh_host = '94.228.123.59'
ssh_port = 22
ssh_username = 'root'
ssh_password = 'p9xiwE5t@HPt^B'

# Параметры для подключения к базе данных PostgreSQL
db_host = 'localhost'
db_port = '5432'
db_name = 'test'
db_user = 'admin'
db_password = 'admin'

try:
    # Подключение к серверу через SSH
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh_client.connect(hostname=ssh_host, port=ssh_port, username=ssh_username, password=ssh_password)

    # Подключение к базе данных PostgreSQL
    conn = psycopg2.connect(host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_password)

    # Вывод результатов подключения к серверу и базе данных
    print("Успешное подключение к серверу через SSH и к базе данных PostgreSQL")

    # Здесь можно выполнять операции с базой данных

    # Закрытие соединений
    conn.close()
    ssh_client.close()

except Exception as e:
    print("Ошибка: ", e)
