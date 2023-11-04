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

# Подключение к серверу через SSH
ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh_client.connect(hostname=ssh_host, port=ssh_port, username=ssh_username, password=ssh_password)

if ssh_client.connect(hostname=ssh_host, port=ssh_port, username=ssh_username, password=ssh_password):
    print("Подключение успешно установлено!")
else:
    print("Не удалось установить подключение.")

# Подключение к базе данных PostgreSQL
conn = psycopg2.connect(host=db_host, port=db_port, dbname=db_name, user=db_user, password=db_password)
cur = conn.cursor()

# Ваш SQL-запрос
sql_query = "SELECT * FROM test;"

# Выполнение запроса
cur.execute(sql_query)

# Получение результатов запроса
results = cur.fetchall()

# Вывод результатов
print("Результаты запроса к базе данных:")
for row in results:
    print(row)

# Закрытие соединений
cur.close()
conn.close()
ssh_client.close()
