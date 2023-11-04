import psycopg2
from telebot import types

# Параметры подключения к PostgreSQL базе данных
db_params = {
    "host": "ваш_хост",
    "database": "ваша_база_данных",
    "user": "ваш_пользователь",
    "password": "ваш_пароль"
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

# Закрытие курсора и соединения с базой данных
cursor.close()
connection.close()

# Обработчик callback-запросов
@bot.callback_query_handler(func=lambda callback: callback.data.startswith('bk') and logged_in)
def bk_handler(call):
    global to_switch
    if call.data == 'bk_mm':
        markup = types.InlineKeyboardMarkup()

        # Добавление каждой базы данных в отдельную кнопку
        for db in databases:
            db_name = db[0]
            btn = types.InlineKeyboardButton(db_name, callback_data=f'db_{db_name}')
            markup.add(btn)

        # Кнопка "Назад"
        back_btn = types.InlineKeyboardButton('<< Назад', callback_data='main_menu')
        markup.add(back_btn)

        # Отправка сообщения с клавиатурой
        bot.send_message(call.message.chat.id, 'Выберите базу данных:', reply_markup=markup)