import psycopg2

try:
    conn = psycopg2.connect(
        host="80.90.185.102",
        database="default_db",
        user="admin",
        password = "fsphack1"
    )
    
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()

    if db_version:
        print("Вход произошел. Версия PostgreSQL:", db_version)
    else:
        print("Нет входа")

    cursor.close()
    conn.close()

except psycopg2.Error as error:
    print("Ошибка при соединении с базой данных:", error)
    print("Нет входа")
