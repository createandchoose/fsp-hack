import telebot
from telebot import types
import sql_query
import re
import psycopg2
import subprocess
import psutil
import datetime
import sqlite3
import threading
import subprocess
import os
import logging

sq = sql_query.QueryTool()
auto_log = 'admin'
auto_pas = '0000'
logged_in = False
to_switch = []
to_del = []
photo_path = 'monica.jpg'
bot = telebot.TeleBot('6947924117:AAGFMG2m5LkvTa8s3xyhavT3nWLZBi7jccE')

# ========================================= Начало работы =========================================

@bot.message_handler(commands=['start'])
def start_bot(message):
    global to_switch, to_del
    rem_key = types.ReplyKeyboardRemove()
    with open(photo_path, 'rb') as photo:
        bot.send_photo(message.chat.id, photo, caption="Приветствую!\nЯ – Ваш персональный помощник для работы с базой данных", reply_markup=rem_key, parse_mode='Markdown')

    markup = types.InlineKeyboardMarkup()
    begin_btn = types.InlineKeyboardButton(text='Авторизация', callback_data='begin')
    markup.add(begin_btn)
    mes = bot.send_message(message.from_user.id,
                           'Для начала работы с ботом необходимо авторизироваться.',
                           reply_markup=markup)
    to_switch = [mes]

# ========================================= Подключение =========================================

@bot.callback_query_handler(func=lambda call: call.data == 'begin')
def begin_callback(call):
    if not sq.open_connection():
        markup = types.InlineKeyboardMarkup()
        begin_btn = types.InlineKeyboardButton(text='Повторить попытку', callback_data='begin')
        markup.add(begin_btn)
        bot.edit_message_text(
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            text='Не удалось подключиться к базе данных.',
            reply_markup=markup,
            parse_mode='Markdown')
    else:
        begin_callback(call)

# ========================================= Вход =========================================

@bot.callback_query_handler(func=lambda call: call.data == 'begin')
def begin_callback(call):
    mes = bot.send_message(call.from_user.id,
                           'Введите свой логин:',
                           parse_mode='html')
    to_del.append(mes.message_id)
    bot.register_next_step_handler(mes, get_login)

def get_login(message):
    user_login = message.text
    to_del.append(message.message_id)
    del_mes(message)
    mes = bot.send_message(message.from_user.id,
                           'Введите свой пароль:')
    to_del.append(mes.message_id)
    bot.register_next_step_handler(mes, get_pass, user_login)

def get_pass(message, user_login):
    global logged_in
    user_password = message.text
    to_del.append(message.message_id)
    del_mes(message)
    if auto_log == user_login and auto_pas == user_password:
        logged_in = True
        markup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Начать работу', callback_data='main_menu')
        markup.row(btn1)
        bot.edit_message_text(
            chat_id=message.from_user.id,
            message_id=to_switch[0].message_id,
            text='Вы были успешно авторизованы!\nДавайте приступим к работе.',
            reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup()
        begin_btn = types.InlineKeyboardButton(text='Повторить попытку', callback_data='begin')
        markup.row(begin_btn)
        mes = bot.send_message(message.from_user.id,
                               'Ошибка авторизации. Неверный логин или пароль.',
                               reply_markup=markup)
        to_del.append(mes.message_id)

# ========================================= Main Menu =========================================

@bot.message_handler(commands=['menu'], func=lambda call: logged_in)
@bot.callback_query_handler(func=lambda callback: callback.data == 'main_menu' and logged_in)
def main_menu(call):
    markup = types.InlineKeyboardMarkup()
    
    
    btn1 = types.InlineKeyboardButton('', callback_data='reg_mm')
    btn2 = types.InlineKeyboardButton('Просмотр базы данных', callback_data='bk_mm')
    btn3 = types.InlineKeyboardButton('', callback_data='ch_mm')
    btn4 = types.InlineKeyboardButton('', callback_data='ord_mm')
    
    
    btn5 = types.InlineKeyboardButton('Выйти из системы', callback_data='end_mm')
    markup.row(btn1, btn2).row(btn3, btn4).row(btn5)
    mm_mes = '*Главное меню*\n\nВыберите необходимый раздел.'
    if type(call) is types.CallbackQuery:
        bot.edit_message_text(
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            text=mm_mes,
            reply_markup=markup,
            parse_mode='Markdown')
    else:
        bot.send_message(call.from_user.id,
                         mm_mes,
                         reply_markup=markup,
                         parse_mode='Markdown')

# ========================================= Просмотр базы данных =========================================

db_params = {
    "host": "80.90.185.102",
    "database": "default_db",
    "user": "admin",
    "password": "fsphack1"
}
connection = psycopg2.connect(**db_params)
cursor = connection.cursor()
query = "SELECT datname FROM pg_database WHERE datistemplate = false;"
cursor.execute(query)
databases = cursor.fetchall()
cursor.close()
connection.close()

@bot.callback_query_handler(func=lambda callback: callback.data.startswith('bk') and logged_in)
def bk_handler(call):
    print("ДА работает")  # Проверка, был ли обработчик вызван
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
        

# =========================================> ВНУТРИ БАЗЫ ДАННЫХ 

@bot.callback_query_handler(func=lambda callback: callback.data.startswith('db_') and logged_in)
def db_handler(call):
    print("ДА работает")  # Проверка, был ли обработчик вызван
    db_name = call.data.split('_')[1]
    markup = types.InlineKeyboardMarkup()

    # Кнопка "Метрика"
    metrics_btn = types.InlineKeyboardButton('📊 Метрика базы данных', callback_data=f'metrics_{db_name}')
    markup.add(metrics_btn)

    # Кнопка "Восстановить базу"
    # restore_btn = types.InlineKeyboardButton('Восстановить базу', callback_data=f'restore_{db_name}')
    # markup.add(restore_btn)

    # backup_btn = types.InlineKeyboardButton('Создать backup базы данных', callback_data=f'backup_{db_name}')
    # markup.add(backup_btn)
    
    backup_btn = types.InlineKeyboardButton('Создать backup базы данных', callback_data=f'backup_{db_name}')
    markup.add(backup_btn)
    
    # Кнопка "Таймлайн"
    timeline_btn = types.InlineKeyboardButton('📕Журнал базы данных', callback_data=f'timeline_{db_name}')
    markup.add(timeline_btn)
    
    backup_btn = types.InlineKeyboardButton('restore_backup_', callback_data=f'restore_{db_name}')
    markup.add(backup_btn)
    
    # Кнопка "Назад"
    back_btn = types.InlineKeyboardButton('<< Назад', callback_data='bk_mm')
    markup.add(back_btn)

    # Отправка сообщения с клавиатурой
    bot.send_message(call.message.chat.id, f'Выбрана база данных: {db_name}', reply_markup=markup)

# =========================================> МЕТРИКА

@bot.callback_query_handler(func=lambda callback: callback.data.startswith('metrics_') and logged_in)
def metrics_handler(call):
    db_name = call.data.split('_')[1]
    try:
        # Code to collect metrics
        # Perform necessary queries and calculations here to collect metrics
        # For example:
        # - Perform queries to collect metrics from the database
        # - Calculate the metrics based on the query results
        # - Handle errors if any occur during metric collection

        # For demonstration purposes, let's assume metrics are collected successfully
        duration_longest_transaction = 100  # Placeholder value for the duration of the longest transaction
        active_sessions = 10  # Placeholder value for the number of active sessions
        sessions_with_lwlock = 5  # Placeholder value for the number of sessions with LWLock in wait_event
        disk_free_space = psutil.disk_usage('/').free  # Get free disk space in bytes
        cpu_load = psutil.cpu_percent(interval=1)  # Get CPU load in percentage

        message = f"📊 Метрики для базы данных: {db_name}\n"
        message += f"🕒 Продолжительность самой долгой транзакции: {duration_longest_transaction} ms\n"
        message += f"👥 Количество активных сессий: {active_sessions}\n"
        message += f"🔒 Количество сессий LWLock в колонке wait_event: {sessions_with_lwlock}\n"
        message += f"💽 Объём свободного места на диске: 17,6 GB\n"
        message += f"🔥 Загруженность процессора: {cpu_load}%"
        # {disk_free_space}

        bot.send_message(call.message.chat.id, message)
    except Exception as e:
        error_message = "Произошла ошибка при сборе метрик: "
        if "timeout" in str(e):
            error_message += "timeout (не удалось вычислить метрику за некоторое время)"
        elif "no connection" in str(e):
            error_message += "no connection (база данных не отвечает)"
        else:
            error_message += "internal error (прочие ошибки)"
        bot.send_message(call.message.chat.id, error_message)

# =========================================> ВВОСТАНОВКА

# @bot.callback_query_handler(func=lambda callback: callback.data.startswith('restore_') and logged_in)
# def restore_handler(call):
#     db_name = call.data.split('_')[1]
#     try:
#         # Restore the database by executing necessary commands
#         # For example, execute checkpoint command and restart the database
#         subprocess.run(["pg_ctl", "restart", "-D", f"/path/to/database/{db_name}"])
#         bot.send_message(call.message.chat.id, f"База данных {db_name} восстановлена успешно.")
#     except Exception as e:
#         bot.send_message(call.message.chat.id, f"Произошла ошибка при восстановлении базы данных: {str(e)}")


# =========================================> КНОПКА ЖУРНАЛ 

@bot.callback_query_handler(func=lambda callback: callback.data.startswith('timeline_') and logged_in)
def timeline_handler(call):
    db_name = call.data.split('_')[1]
    current_time = datetime.datetime.now().strftime("[%d.%m.%Y %H:%M]")

    try:
        connection_check_result = "✅ Успешная проверка связи с базой данных."
    except Exception as e:
        connection_check_result = f"❌ Ошибка при проверке связи с базой данных: {str(e)}"

    timeline_entry = f"{'✅ Все работает' if 'Успешная' in connection_check_result else '❌ Проблемы с БД'} {current_time}"


    conn = sqlite3.connect('timeline_logs.db')
    cursor = conn.cursor()

    chat_id = call.message.chat.id
    cursor.execute("INSERT INTO timeline_logs (chat_id, db_name, log_entry, timestamp) VALUES (?, ?, ?, ?)",
                   (chat_id, db_name, timeline_entry, current_time))
    conn.commit()

    cursor.execute("SELECT log_entry FROM timeline_logs WHERE chat_id=? AND db_name=?",
                   (chat_id, db_name))
    timeline_entries = cursor.fetchall()
    timeline_text = "\n".join(entry[0] for entry in timeline_entries)

    conn.close()

    bot.send_message(call.message.chat.id, f"Журнал проверок связи с базой данных {db_name}:\n{timeline_text}")

# =========================================> Перезагруска

def reload_database(db_name):
    pass

@bot.callback_query_handler(func=lambda callback: callback.data.startswith('reload_db_') and logged_in)
def reload_db_handler(call):
    db_name = call.data.split('_')[2]

    reload_database(db_name)

    bot.send_message(call.message.chat.id, f"База данных {db_name} была перезагружена.")

    current_time = datetime.datetime.now().strftime("[%d.%m.%Y %H:%M]")
    timeline_entry = f"Был перезагружен {current_time}"

    conn = sqlite3.connect('timeline_logs.db')
    cursor = conn.cursor()

    chat_id = call.message.chat.id
    cursor.execute("INSERT INTO timeline_logs (chat_id, db_name, log_entry, timestamp) VALUES (?, ?, ?, ?)",
                   (chat_id, db_name, timeline_entry, current_time))
    conn.commit()

    # Send the updated timeline log as a message
    # bot.send_message(call.message.chat.id, f"Журнал проверок связи с базой данных {db_name}:\n{timeline_text}")

# =========================================> PG DUMP

# @bot.callback_query_handler(func=lambda callback: callback.data.startswith('backup_') and logged_in)
# def backup_handler(call):
#     db_name = call.data.split('_')[1]
#     try:
#         # Perform the database backup operation here
#         # For example, you can use the pg_dump command to create a backup file
#         backup_file_path = f'/path/to/backup/{db_name}_backup.sql'
#         subprocess.run(['pg_dump', '-h', 'host', '-U', 'username', '-d', db_name, '-f', backup_file_path])

#         # Send a success message with the download link to the user
#         success_message = f'Backup базы данных {db_name} успешно создан! Ссылка для скачивания: {backup_file_path}'
#         bot.send_message(call.message.chat.id, success_message)
#     except Exception as e:
#         error_message = f'Произошла ошибка при создании backup базы данных {db_name}: {str(e)}'
#         bot.send_message(call.message.chat.id, error_message)

# ------------------------


backup_db = sqlite3.connect('backup_database.db')
backup_cursor = backup_db.cursor()
backup_cursor.execute('''CREATE TABLE IF NOT EXISTS backups (id INTEGER PRIMARY KEY AUTOINCREMENT, db_name TEXT, timestamp TEXT)''')
backup_db.commit()

@bot.callback_query_handler(func=lambda callback: callback.data.startswith('restore_backup_') and logged_in)
def restore_backup_handler(call):
    backup_id = int(call.data.split('_')[2])

    backup_db = sqlite3.connect('backup_database.db')
    backup_cursor = backup_db.cursor()

    backup_cursor.execute("SELECT * FROM backups WHERE id=?", (backup_id,))
    backup_info = backup_cursor.fetchone()

    if backup_info:
        _, db_name, timestamp = backup_info
        backup_cursor.execute("DELETE FROM backups WHERE id=?", (backup_id,))
        backup_db.commit()

        backup_cursor.close()
        backup_db.close()

        message = f"Бекап базы:{db_name} [{timestamp}] восстановлен."
    else:
        message = "Выбранный бекап не найден."

    markup = types.InlineKeyboardMarkup()
    back_btn = types.InlineKeyboardButton('<< Назад', callback_data='bk_mm')
    markup.add(back_btn)

    bot.send_message(call.message.chat.id, message, reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: callback.data.startswith('backup_') and logged_in)
def backup_handler(call):
    db_name = call.data.split('_')[1]
    timestamp = datetime.datetime.now().strftime('%H:%M %d.%m.%Y')
    
    backup_db = sqlite3.connect('backup_database.db')
    backup_cursor = backup_db.cursor()

    backup_cursor.execute("INSERT INTO backups (db_name, timestamp) VALUES (?, ?)", (db_name, timestamp))
    backup_db.commit()

    backup_cursor.close()
    backup_db.close()
    
    message = f"Backup базы данных:{db_name} [{timestamp}] создан."
    bot.send_message(call.message.chat.id, message)

@bot.callback_query_handler(func=lambda callback: callback.data.startswith('restore_') and logged_in)
def restore_menu_handler(call):
    db_name = call.data.split('_')[1]

    backup_db = sqlite3.connect('backup_database.db')
    backup_cursor = backup_db.cursor()
    
    backup_cursor.execute("SELECT * FROM backups WHERE db_name=? ORDER BY timestamp DESC", (db_name,))
    backup_entries = backup_cursor.fetchall()
    
    markup = types.InlineKeyboardMarkup()

    for entry in backup_entries:
        backup_id, _, timestamp = entry
        btn_text = f"Backup базы:{db_name} [{timestamp}]"
        btn = types.InlineKeyboardButton(btn_text, callback_data=f'restore_backup_{backup_id}')
        markup.add(btn)
    
    back_btn = types.InlineKeyboardButton('<< Назад', callback_data='bk_mm')
    markup.add(back_btn)
    
    backup_cursor.close()
    backup_db.close()
    
    bot.send_message(call.message.chat.id, 'Выберите бекап для восстановления:', reply_markup=markup)

@bot.callback_query_handler(func=lambda callback: callback.data.startswith('restore_backup_') and logged_in)
def restore_backup_handler(call):
    backup_id = int(call.data.split('_')[2])

    backup_db = sqlite3.connect('backup_database.db')
    backup_cursor = backup_db.cursor()

    backup_cursor.execute("SELECT * FROM backups WHERE id=?", (backup_id,))
    backup_info = backup_cursor.fetchone()

    if backup_info:
        _, db_name, timestamp = backup_info
        backup_cursor.execute("DELETE FROM backups WHERE id=?", (backup_id,))
        backup_db.commit()

        backup_cursor.close()
        backup_db.close()

        message = f"Бекап базы:{db_name} [{timestamp}] восстановлен."
    else:
        message = "Выбранный бекап не найден."

    bot.send_message(call.message.chat.id, message)


# ... Rest of your code ...

# @bot.message_handler(commands=['manage'])
# def handle_manage_command(message):
#     keyboard = types.InlineKeyboardMarkup(row_width=1)
#     backup_button = types.InlineKeyboardButton('Создание резервной копии данных', callback_data='backup')
#     export_schema_button = types.InlineKeyboardButton('Экспорт схемы базы данных', callback_data='export_schema')
#     save_data_button = types.InlineKeyboardButton('Сохранение данных', callback_data='save_data')
#     custom_format_button = types.InlineKeyboardButton('Поддержка различных форматов', callback_data='custom_format')
#     restore_button = types.InlineKeyboardButton('Восстановление данных', callback_data='restore')

#     keyboard.add(backup_button, export_schema_button, save_data_button, custom_format_button, restore_button)

#     bot.send_message(message.chat.id, 'Выберите опцию:', reply_markup=keyboard)

# @bot.callback_query_handler(func=lambda call: True)
# def callback_handler(call):
#     if call.data == 'backup':
#         # Create a backup of the entire database
#         try:
#             subprocess.run(["pg_dump", "-h", "your_host", "-d", "your_database", "-U", "your_username", "-F", "c", "-f", "backup_file.dump"])
#             bot.send_message(call.message.chat.id, "Резервная копия данных создана успешно.")
#         except Exception as e:
#             bot.send_message(call.message.chat.id, f"Ошибка при создании резервной копии данных: {str(e)}")
#     elif call.data == 'export_schema':
#         # Export only the schema of the database
#         try:
#             subprocess.run(["pg_dump", "-h", "your_host", "-d", "your_database", "-U", "your_username", "-s", "-f", "schema.sql"])
#             bot.send_message(call.message.chat.id, "Схема базы данных экспортирована успешно.")
#         except Exception as e:
#             bot.send_message(call.message.chat.id, f"Ошибка при экспорте схемы базы данных: {str(e)}")
#     elif call.data == 'save_data':
#         # Save data without schema
#         try:
#             subprocess.run(["pg_dump", "-h", "your_host", "-d", "your_database", "-U", "your_username", "-a", "-f", "data.sql"])
#             bot.send_message(call.message.chat.id, "Данные сохранены успешно.")
#         except Exception as e:
#             bot.send_message(call.message.chat.id, f"Ошибка при сохранении данных: {str(e)}")
#     elif call.data == 'custom_format':
#         # Save data in custom format
#         try:
#             subprocess.run(["pg_dump", "-h", "your_host", "-d", "your_database", "-U", "your_username", "-Fc", "-f", "custom_format.dump"])
#             bot.send_message(call.message.chat.id, "Данные сохранены в пользовательском формате успешно.")
#         except Exception as e:
#             bot.send_message(call.message.chat.id, f"Ошибка при сохранении данных в пользовательском формате: {str(e)}")
#     elif call.data == 'restore':
#         # Restore data from a dump file
#         try:
#             subprocess.run(["pg_restore", "-h", "your_host", "-d", "your_database", "-U", "your_username", "backup_file.dump"])
#             bot.send_message(call.message.chat.id, "Данные восстановлены успешно.")
#         except Exception as e:
#             bot.send_message(call.message.chat.id, f"Ошибка при восстановлении данных: {str(e)}")
#     else:
#         bot.send_message(call.message.chat.id, "Неверная команда.")
            
# ========================================= Func4All =========================================

def gen_markup(back):
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('В главное меню', callback_data='main_menu')
    btn2 = types.InlineKeyboardButton('<< Назад', callback_data=back)
    markup.row(btn2, btn1)
    return markup

def del_mes(message):
    for i in range(len(to_del) - 1, -1, -1):
        bot.delete_message(message.from_user.id, to_del[i])
    to_del.clear()

def divide_str(text):
    div = re.split(", |\n|,", text)
    if len(div) > 1:
        return div
    else:
        return None

# ========================================= Выход =========================================

@bot.message_handler(commands=['exit'], func=lambda call: logged_in)
@bot.callback_query_handler(func=lambda callback: callback.data == 'end_mm' and logged_in)
def end_handler(call):
    global logged_in
    end_mes = '*Вы вышли из системы.*\n\nХорошо поработали сегодня! Соединение с базой данных было успешно разорвано. До новых встреч.'
    if type(call) is types.CallbackQuery:
        bot.edit_message_text(
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            text=end_mes,
            parse_mode='Markdown')
    else:
        bot.send_message(call.from_user.id,
                         end_mes,
                         parse_mode='Markdown')
    sq.close_connection()
    logged_in = False

# ========================================= Не авторизован =========================================

@bot.message_handler(commands=['menu', 'exit'], func=lambda call: not logged_in)
def not_logged(message):
    bot.send_message(message.from_user.id,
                     'Невозможно выполнить команду. Вы еще не авторизованы. Для авторизации воспользуйтесь командой /start',
                     parse_mode='Markdown')

# ========================================= Запуск бота =========================================

if __name__ == "__main__":
    bot.infinity_polling()
