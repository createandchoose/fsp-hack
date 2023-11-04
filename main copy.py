import telebot
from telebot import types
import sql_query
import re
import psycopg2

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
    
    
    btn5 = types.InlineKeyboardButton('Завершить работу', callback_data='end_mm')
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
        

def get_table_count(db_name):
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()
    query = f"SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_catalog = '{db_name}';"
    cursor.execute(query)
    count = cursor.fetchone()[0]
    cursor.close()
    connection.close()
    return count

@bot.callback_query_handler(func=lambda callback: callback.data.startswith('db_') and logged_in)
def db_handler(call):
    print("Database handler calleыыыыыыыыыыыыыыыd!")
    db_name = call.data.split('_')[1]
    table_count = get_table_count(db_name)
    bot.send_message(call.message.chat.id, f'Количество таблиц в базе данных {db_name}: {table_count}')


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
    end_mes = '*Завершение работы.*\n\nХорошо поработали сегодня! Соединение с базой данных было успешно разорвано. До новых встреч.'
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
