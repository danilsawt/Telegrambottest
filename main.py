import telebot
from telebot import types
import psycopg2 #подключение библиотеки для работы с PostgesSQL
from config import host,user,password,db_name
api_token = '5931451553:AAFxV9irXzz_lf0zhZYu6zWwyKSfGd3y1ZI'

bot = telebot.TeleBot(api_token)

# Глобальная переменная
name = None

# начальное меню на команду старт
@bot.message_handler(commands=['start'])
def start_message(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    bt1 = types.KeyboardButton('герои')
    bt2 = types.KeyboardButton('предметы')
    kb.add(bt1, bt2)
    bot.send_message(message.chat.id,
                     "Здравствуй,титан! В этом боте ты можешь узнать о некоторых героях доты и предметах,не стесняйся-используй кнопки снизу",
                     reply_markup=kb)


# обработчик в случае отправки фотографии в чат бота

@bot.message_handler(content_types=['photo'])
def photo_send(message):
    bot.send_message(message.chat.id, "Извините,мы пока не можем реагировать на фотографии, но в скором времени эта функции обязательно появится")


# обработчик в случае отправки голосового
@bot.message_handler(content_types=['voice'])
def audio_send(message):
    bot.send_message(message.chat.id, "Извините,мы пока не можем реагировать на аудиосообщения, но в скором времени эта функции обязательно появится")

# обработчик в случае отправки видео
@bot.message_handler(content_types=['video'])
def video_send(message):
    bot.send_message(message.chat.id, "Извините,мы пока не можем реагировать на видео, но в скором времени эта функции обязательно появится")

# Проверка работоспособности бд
@bot.message_handler(commands=['registration'])
def registr(message):
    conn = psycopg2.connect(host=host,
                            user=user,
                            password=password,
                            database=db_name)
    cur = conn.cursor()

    #Создание таблицы в бд,если она не существует
    cur.execute('CREATE TABLE IF NOT EXISTS "users" (id bigserial primary key, name VARCHAR(45), hero VARCHAR(45))')

    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, 'Давайка мы запишем с каким героем ты себя ассоциируешь. Для начала введи имя')
    bot.register_next_step_handler(message, user_name)


# Считывание логин нейма введенного пользователем
def user_name(message):
    global name
    name = message.text.strip()
    bot.send_message(message.chat.id, 'А теперь героя')
    bot.register_next_step_handler(message, hero_name)


# Считывание херонейма и занесение в бд
def hero_name(message):
    ar = types.InlineKeyboardMarkup()
    heroname = message.text.strip()
    conn = psycopg2.connect(host=host,
                            user=user,
                            password=password,
                            database=db_name)
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, hero) values ('%s','%s')" % (name, heroname))
    conn.commit()
    cur.close()
    conn.close()
    knopka = types.InlineKeyboardButton(text='Список пользователей', callback_data='knopka')
    ar.add(knopka)
    bot.send_message(message.chat.id, 'Ты добавлен в базу',reply_markup=ar)



# тестовый вариант инлайн блоков
'''
@bot.message_handler(commands=['start1'])
def start_message(message):
    switch = types.InlineKeyboardButton(text='Выберите атрибут', switch_inline_query='/start')
    kc = types.InlineKeyboardMarkup(row_width=2)
    bt1 = types.InlineKeyboardButton(text='Сларк', url="https://dota2.fandom.com/ru/wiki/Slark")
    bt2 = types.InlineKeyboardButton(text='Грим', url="https://dota2.fandom.com/ru/wiki/Grimstroke")
    kc.add(bt1, bt2)
    bot.send_message(message.chat.id, "Герои", reply_markup=kc)
'''


# Переписывание инлайн кнопок "Герои" и "предметы" на сопутсвующие им кнопки
@bot.message_handler()
def heroes(message):
    if message.text == 'герои':
        kf = types.InlineKeyboardMarkup(row_width=2)
        bt1 = types.InlineKeyboardButton(text='Ловкость', callback_data='bt1')
        bt2 = types.InlineKeyboardButton(text='Интелект', callback_data='bt2')
        kf.add(bt1, bt2)
        bot.send_message(message.chat.id, "Выбери атрибут", reply_markup=kf)
    elif message.text == 'предметы':
        kf = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton(text='Боковая лавка', callback_data='btn1')
        btn2 = types.InlineKeyboardButton(text='Фонтанная лавка', callback_data='btn2')
        kf.add(btn1, btn2)
        bot.send_message(message.chat.id, "Выбери лавку", reply_markup=kf)


# Проверка введенное пользователем команды и переписывание инлайн кнопок, а так же проверка на кнопку вывода пользователей из бд
@bot.callback_query_handler(func=lambda callback: callback.data)
def check_callback_data(callback):
    if callback.data == 'bt1':
        kf = types.InlineKeyboardMarkup(row_width=2)
        bt1 = types.InlineKeyboardButton(text='Сларк', url="https://dota2.fandom.com/ru/wiki/Slark")
        bt2 = types.InlineKeyboardButton(text='Войд', url="https://dota2.fandom.com/ru/wiki/Faceless_Void")
        kf.add(bt1, bt2)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text="Heroes agility",
                              reply_markup=kf)

    elif callback.data == 'bt2':
        kf = types.InlineKeyboardMarkup(row_width=2)
        bt1 = types.InlineKeyboardButton(text='Грим', url="https://dota2.fandom.com/ru/wiki/Grimstroke")
        bt2 = types.InlineKeyboardButton(text='Цм', url="https://dota2.fandom.com/ru/wiki/Crystal_Maiden")
        kf.add(bt1, bt2)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text="Heroes int",
                              reply_markup=kf)
    elif callback.data == 'btn1':
        kf = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton(text='Манго', url="https://dota2.fandom.com/ru/wiki/Enchanted_Mango")
        btn2 = types.InlineKeyboardButton(text='Танго', url="https://dota2.fandom.com/ru/wiki/Tango")
        kf.add(btn1, btn2)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text="Основная",
                              reply_markup=kf)
    elif callback.data == 'btn2':
        kf = types.InlineKeyboardMarkup(row_width=2)
        btn1 = types.InlineKeyboardButton(text='Корнкопия', url="https://dota2.fandom.com/ru/wiki/Cornucopia")
        btn2 = types.InlineKeyboardButton(text='Плита', url="https://dota2.fandom.com/ru/wiki/Platemail")
        kf.add(btn1, btn2)
        bot.edit_message_text(chat_id=callback.message.chat.id, message_id=callback.message.id, text="Боковая",
                              reply_markup=kf)
    elif callback.data == 'knopka':
        conn = psycopg2.connect(host=host,
                                user=user,
                                password=password,
                                database=db_name)
        cur = conn.cursor()

        cur.execute('SELECT * FROM users')
        users = cur.fetchall()  # Возвращение всех найденных записей

        per = ''
        # Перебор и вывод всех пользователей в бд
        for i in users:
            per += f'Имя пользователя: {i[1]} С каким героем себя ассоциирует: {i[2]} \n'

        cur.close()
        conn.close()
        bot.send_message(callback.message.chat.id, per)


bot.polling()
