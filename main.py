import telebot
from telebot import types
import sql_query
import re
import psycopg2

import subprocess
import psutil


sq = sql_query.QueryTool()

auto_log = 'admin'
auto_pas = '0000'
logged_in = False
to_switch = []
to_del = []

bot = telebot.TeleBot('6947924117:AAGFMG2m5LkvTa8s3xyhavT3nWLZBi7jccE')

# ========================================= Начало работы =========================================

@bot.message_handler(commands=['start'])
def start_bot(message):
    global to_switch, to_del
    rem_key = types.ReplyKeyboardRemove()
    bot.send_message(message.from_user.id,
                     "Приветствую!\nЯ – Ваш персональный помощник для работы с базой данных",
                     reply_markup=rem_key,
                     parse_mode='Markdown')
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
    print("Callback handler called!")  # Проверка, был ли обработчик вызван
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
    print("Callback handler called!")  # Проверка, был ли обработчик вызван
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
    print("Callback handler called!")  # Проверка, был ли обработчик вызван
    db_name = call.data.split('_')[1]
    markup = types.InlineKeyboardMarkup()

    # Кнопка "Метрика"
    metrics_btn = types.InlineKeyboardButton('📊 Метрика', callback_data=f'metrics_{db_name}')
    markup.add(metrics_btn)

    # Кнопка "Восстановить базу"
    restore_btn = types.InlineKeyboardButton('Восстановить базу', callback_data=f'restore_{db_name}')
    markup.add(restore_btn)

    # Кнопка "Таймлайн"
    timeline_btn = types.InlineKeyboardButton('Таймлайн', callback_data=f'timeline_{db_name}')
    markup.add(timeline_btn)

    # Кнопка "Назад"
    back_btn = types.InlineKeyboardButton('<< Назад', callback_data='bk_mm')
    markup.add(back_btn)

    # Отправка сообщения с клавиатурой
    bot.send_message(call.message.chat.id, f'Выбрана база данных: {db_name}', reply_markup=markup)

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
        message += f"💽 Объём свободного места на диске: {disk_free_space} bytes\n"
        message += f"🔥 Загруженность процессора: {cpu_load}%"

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

@bot.callback_query_handler(func=lambda callback: callback.data.startswith('restore_') and logged_in)
def restore_handler(call):
    db_name = call.data.split('_')[1]
    try:
        # Restore the database by executing necessary commands
        # For example, execute checkpoint command and restart the database
        subprocess.run(["pg_ctl", "restart", "-D", f"/path/to/database/{db_name}"])
        bot.send_message(call.message.chat.id, f"База данных {db_name} восстановлена успешно.")
    except Exception as e:
        bot.send_message(call.message.chat.id, f"Произошла ошибка при восстановлении базы данных: {str(e)}")

@bot.callback_query_handler(func=lambda callback: callback.data.startswith('timeline_') and logged_in)
def timeline_handler(call):
    db_name = call.data.split('_')[1]
    try:
        # Code to provide additional information about timeline
        # Fetch and provide the required timeline information
        # For example, fetch historical metrics data, analyze changes, and provide the information
        timeline_info = "Дополнительная информация о таймлайне будет предоставлена позже."
        bot.send_message(call.message.chat.id, timeline_info)
    except Exception as e:
        bot.send_message(call.message.chat.id, f"Произошла ошибка при получении информации о таймлайне: {str(e)}")


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

# ========================================= End =========================================

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

# ========================================= Not logged =========================================

@bot.message_handler(commands=['menu', 'exit'], func=lambda call: not logged_in)
def not_logged(message):
    bot.send_message(message.from_user.id,
                     'Невозможно выполнить команду. Вы еще не авторизованы. Для авторизации воспользуйтесь командой /start',
                     parse_mode='Markdown')

# ========================================= Start up bot =========================================

if __name__ == "__main__":
    bot.infinity_polling()
