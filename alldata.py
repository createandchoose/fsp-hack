import psycopg2

# Параметры подключения к PostgreSQL базе данных
db_params = {
    "host": "80.90.185.102",
    "database": "default_db",
    "user": "admin",
    "password": "fsphack1"
}
# Подключение к базе данных
connection = psycopg2.connect(**db_params)

# Создание курсора для выполнения SQL-запросов
cursor = connection.cursor()

# SQL-запрос для получения списка всех баз данных
query = "SELECT datname FROM pg_database WHERE datistemplate = false;"

# Выполнение SQL-запроса
cursor.execute(query)

# Получение результатов запроса в виде списка
databases = cursor.fetchall()

# Вывод списка баз данных
print("Список всех баз данных:")
for db in databases:
    print(db[0])

# Закрытие курсора и соединения с базой данных
cursor.close()
connection.close()