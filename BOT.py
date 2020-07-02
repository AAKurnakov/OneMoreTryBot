import sys
import telebot
import xlrd
import mysql.connector
import random
from mysql.connector import errorcode
from telebot import types

bot = telebot.TeleBot('1014151094:AAEyzNbrwI_8OezqOD2eN7L1r5Cwde1sU7A')

try:
    db = mysql.connector.connect(
      host="127.0.0.1",
      user="root",
      passwd="pass",
      port="3306",
      database="rvg_db"
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
        sys.exit()
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
        sys.exit()
    else:
        print(err)
        sys.exit()

cursor = db.cursor()


excel_data_file = xlrd.open_workbook('./Diety.xlsx')
sheet = excel_data_file.sheet_by_index(0)

a = ''
ros = ''
ves = ''
sex = ''
voz = ''
kal = ''
aim = ''
diet = ''
name = ''

item1 = types.KeyboardButton(text="Начать")
item2 = types.KeyboardButton(text="М")
item3 = types.KeyboardButton(text='Ж')
item4 = types.KeyboardButton(text="Похудеть")
item5 = types.KeyboardButton(text='Поддерживать')
item6 = types.KeyboardButton(text='Набрать')
item7 = types.KeyboardButton(text='Мне не нравится рацион')
item8 = types.KeyboardButton(text='Спасибо, мне нравится')

key_mal = types.InlineKeyboardButton(text='Малая', callback_data='1')
key_sr = types.InlineKeyboardButton(text='Средняя', callback_data='2')
key_wis = types.InlineKeyboardButton(text='Высокая', callback_data='3')

keyboard = types.InlineKeyboardMarkup()
keyboard1 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboard2 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboard3 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
keyboard4 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

keyboard.add(key_mal)
keyboard.add(key_sr)
keyboard.add(key_wis)
keyboard1.add(item1)
keyboard2.add(item2, item3)
keyboard3.add(item4, item5, item6)
keyboard4.add(item7, item8)

user_data = {}


class User:
    def __init__(self, first_name):
        self.first_name = first_name
        self.ros = ros
        self.voz = voz
        self.sex = sex
        self.aim = aim
        self.ves = ves


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start" or "Привет" or "Ку":
        bot.send_message(message.from_user.id, 'Привет, я - бот-диетолог. Я могу помочь тебе достигнуть поставленных '
                                               'целей и преобразиться. Если ты готов, напиши Начать, если нет - '
                                               'увидимся в следующий раз, ведь никогда не поздно передумать :)',
                         reply_markup=keyboard1)
        bot.register_next_step_handler(message, start)


def start(message):
    if message.text == 'Начать':
        bot.send_message(message.from_user.id, 'Введите имя')
        bot.register_next_step_handler(message, get_name)
    elif message.text == "Хочу стать сутулым задротом":
        bot.send_message(message.from_user.id, "Мое уважение, тогда не смею более тратить ни секунды твоей жизни, "
                                               "тебе сюда: https://t.me/iamgodfitness")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Рост и вес вводятся цифрами, пол вводится 1 буквой (М или Ж), "
                                               "активность выбирается из предложенных вариантов. Давай достигнем "
                                               "твоей цели вместе. Введите свое имя для начала")
        bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.from_user.id, "Напишите /help")
        bot.register_next_step_handler(message, get_name)


def get_name(message):
    global name
    name = ''
    while name == '':
        try:
            name = message.text
            user_id = message.from_user.id
            user_data[user_id] = User(message.text)
        except (TypeError, ValueError):
            bot.register_next_step_handler(message, get_name)
        else:
            bot.send_message(message.from_user.id, 'Введите рост')
            bot.register_next_step_handler(message, get_ros)


def get_ros(message):
    global ros
    ros = ''
    while ros == '':
        try:
            ros = int(message.text)
            user_id = message.from_user.id
            user = user_data[user_id]
            user.ros = ros
        except (TypeError, ValueError):
            bot.send_message(message.from_user.id, 'Введите рост цифрами, пожалуйста')
            ros = 'a'
            bot.register_next_step_handler(message, get_ros)
        else:
            bot.send_message(message.from_user.id, 'Введите возраст')
            bot.register_next_step_handler(message, get_voz)


def get_voz(message):
    global voz
    voz = ''
    while voz == '':
        try:
            voz = int(message.text)
            user_id = message.from_user.id
            user = user_data[user_id]
            user.voz = voz
        except (TypeError, ValueError):
            bot.send_message(message.from_user.id, 'Введите возраст цифрами, пожалуйста')
            voz = 'a'
            bot.register_next_step_handler(message, get_voz)
        else:
            bot.send_message(message.from_user.id, 'Введите Ваш пол (М или Ж)', reply_markup=keyboard2)
            bot.register_next_step_handler(message, get_sex)


def get_sex(message):
    global sex
    sex = ''
    while sex == '':
        try:
            sex = str(message.text)
            user_id = message.from_user.id
            user = user_data[user_id]
            user.sex = sex
        except (TypeError, ValueError):
            bot.send_message(message.from_user.id, 'Введите Ваш пол 1 буквой, пожалуйста')
            sex = '1'
            bot.register_next_step_handler(message, get_sex)
        else:
            bot.send_message(message.from_user.id, 'Выберите Вашу цель по изменению веса', reply_markup=keyboard3)
            bot.register_next_step_handler(message, get_aim)


def get_aim(message):
    global aim
    while aim == '':
        try:
            aim = str(message.text)
            user_id = message.from_user.id
            user = user_data[user_id]
            user.aim = aim
        except (TypeError, ValueError):
            bot.send_message(message.from_user.id, 'Выберите Вашу цель с помощью предложенной клавиатуры, пожалуйста')
            aim = '1'
            bot.register_next_step_handler(message, get_aim)
        else:
            bot.send_message(message.from_user.id, 'Введите вес')
            bot.register_next_step_handler(message, get_ves)


def get_ves(message):
    global ves
    ves = ''
    while ves == '':
        try:
            ves = int(message.text)
            user_id = message.from_user.id
            user = user_data[user_id]
            user.ves = ves
            sql = "INSERT INTO users (first_name, ros, voz, sex, aim, ves, user_id) \
                                              VALUES (%s, %s, %s, %s, %s, %s, %s)"
            val = (user.first_name, user.ros, user.voz, user.sex, user.aim, user.ves, user_id)
            cursor.execute(sql, val)
            db.commit()
        except Exception:
            bot.send_message(message.from_user.id, 'Вы уже зарегистрированы, выберите '
                                                   'активность', reply_markup=keyboard)
            ves = int(message.text)
        else:
            ves = int(message.text)
            bot.send_message(message.from_user.id, 'Выберите активность:', reply_markup=keyboard)


def get_diet(message):
    if message.text == 'Мне не нравится рацион' or '':
        bot.send_message(message.from_user.id, 'Понял, сейчас исправлю. Выберите, пожалуйста, активность заново',
                         reply_markup=keyboard)
    elif message.text == 'Спасибо, мне нравится':
        bot.send_message(message.from_user.id, 'Спасибо, что воспользовались моей помощью. Удачи в похудении :)')


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global kal, diet,  a
    if sex == 'М':
        if call.data == '1':
            a = '1'
            if aim == "Похудеть":
                kal = round(((88.36 + (13.4 * int(ves)) + (4.8 * int(ros)) - (5.7 * int(voz))) * 0.85), 2)
                bot.send_message(call.message.chat.id, 'Ваша норма калорий для похудения = ' + str(kal))
            elif aim == 'Поддерживать':
                kal = round((88.36 + (13.4 * int(ves)) + (4.8 * int(ros)) - (5.7 * int(voz))), 2)
                bot.send_message(call.message.chat.id, 'Ваша норма калорий = ' + str(kal))
            elif aim == 'Набрать':
                kal = round(((88.36 + (13.4 * int(ves)) + (4.8 * int(ros)) - (5.7 * int(voz))) * 1.2), 2)
                bot.send_message(call.message.chat.id, 'Ваша норма калорий для набора = ' + str(kal))
            if 0 < kal <= 750:
                diet = str(sheet.row(random.randint(1, 10))[0]).replace('text:', '')\
                    .replace("'", "").replace(" . ", "\n")
            elif 750 < kal <= 1250:
                diet = str(sheet.row(random.randint(1, 10))[1]).replace('text:', '')\
                    .replace("'", "").replace(" . ", "\n")
            elif 1250 < kal <= 1750:
                diet = str(sheet.row(random.randint(1, 10))[2]).replace('text:', '')\
                    .replace("'", "").replace(" . ", "\n")
            elif 1750 < kal <= 2250:
                diet = str(sheet.row(random.randint(1, 10))[3]).replace('text:', '')\
                    .replace("'", "").replace(" . ", "\n")
            elif 2250 < kal <= 2750:
                diet = str(sheet.row(random.randint(1, 10))[4]).replace('text:', '')\
                    .replace("'", "").replace(" . ", "\n")
            elif 2750 < kal <= 3250:
                diet = str(sheet.row(random.randint(1, 10))[5]).replace('text:', '')\
                    .replace("'", "").replace(" . ", "\n")
            elif 3250 < kal <= 3750:
                diet = str(sheet.row(random.randint(1, 10))[6]).replace('text:', '')\
                    .replace("'", "").replace(" . ", "\n")
            bot.send_message(call.message.chat.id, 'Ваш рацион на день:\n' + diet, reply_markup=keyboard4)
            bot.register_next_step_handler(call.message, get_diet)
        elif call.data == '2':
            a = '2'
            if aim == "Похудеть":
                kal = round((((88.36 + (13.4 * int(ves)) + (4.8 * int(ros)) - (5.7 * int(voz))) * 1.2) * 0.85), 2)
                bot.send_message(call.message.chat.id, 'Ваша норма калорий для похудения = ' + str(kal))
            elif aim == 'Поддерживать':
                kal = round(((88.36 + (13.4 * int(ves)) + (4.8 * int(ros)) - (5.7 * int(voz))) * 1.2), 2)
                bot.send_message(call.message.chat.id, 'Ваша норма калорий = ' + str(kal))
            elif aim == 'Набрать':
                kal = round((((88.36 + (13.4 * int(ves)) + (4.8 * int(ros)) - (5.7 * int(voz))) * 1.2) * 1.2), 2)
                bot.send_message(call.message.chat.id, 'Ваша норма калорий для набора = ' + str(kal))
            if 0 < kal <= 750:
                diet = str(sheet.row(random.randint(1, 10))[0]).replace('text:', '') \
                    .replace("'", "").replace(" . ", "\n")
            elif 750 < kal <= 1250:
                diet = str(sheet.row(random.randint(1, 10))[1]).replace('text:', '') \
                    .replace("'", "").replace(" . ", "\n")
            elif 1250 < kal <= 1750:
                diet = str(sheet.row(random.randint(1, 10))[2]).replace('text:', '') \
                    .replace("'", "").replace(" . ", "\n")
            elif 1750 < kal <= 2250:
                diet = str(sheet.row(random.randint(1, 10))[3]).replace('text:', '') \
                    .replace("'", "").replace(" . ", "\n")
            elif 2250 < kal <= 2750:
                diet = str(sheet.row(random.randint(1, 10))[4]).replace('text:', '') \
                    .replace("'", "").replace(" . ", "\n")
            elif 2750 < kal <= 3250:
                diet = str(sheet.row(random.randint(1, 10))[5]).replace('text:', '') \
                    .replace("'", "").replace(" . ", "\n")
            elif 3250 < kal <= 3750:
                diet = str(sheet.row(random.randint(1, 10))[6]).replace('text:', '') \
                    .replace("'", "").replace(" . ", "\n")
            bot.send_message(call.message.chat.id, 'Ваш рацион на день:\n' + diet, reply_markup=keyboard4)
            bot.register_next_step_handler(call.message, get_diet)
        elif call.data == '3':
            a = '3'
            if aim == "Похудеть":
                kal = round((((88.36 + (13.4 * int(ves)) + (4.8 * int(ros)) - (5.7 * int(voz))) * 1.55) * 0.85), 2)
                bot.send_message(call.message.chat.id, 'Ваша норма калорий для похудения = ' + str(kal))
            elif aim == 'Поддерживать':
                kal = round(((88.36 + (13.4 * int(ves)) + (4.8 * int(ros)) - (5.7 * int(voz))) * 1.55), 2)
                bot.send_message(call.message.chat.id, 'Ваша норма калорий = ' + str(kal))
            elif aim == 'Набрать':
                kal = round((((88.36 + (13.4 * int(ves)) + (4.8 * int(ros)) - (5.7 * int(voz))) * 1.55) * 1.2), 2)
                bot.send_message(call.message.chat.id, 'Ваша норма калорий для набора = ' + str(kal))
            if 0 < kal <= 750:
                diet = str(sheet.row(random.randint(1, 10))[0]).replace('text:', '') \
                    .replace("'", "").replace(" . ", "\n")
            elif 750 < kal <= 1250:
                diet = str(sheet.row(random.randint(1, 10))[1]).replace('text:', '') \
                    .replace("'", "").replace(" . ", "\n")
            elif 1250 < kal <= 1750:
                diet = str(sheet.row(random.randint(1, 10))[2]).replace('text:', '') \
                    .replace("'", "").replace(" . ", "\n")
            elif 1750 < kal <= 2250:
                diet = str(sheet.row(random.randint(1, 10))[3]).replace('text:', '') \
                    .replace("'", "").replace(" . ", "\n")
            elif 2250 < kal <= 2750:
                diet = str(sheet.row(random.randint(1, 10))[4]).replace('text:', '') \
                    .replace("'", "").replace(" . ", "\n")
            elif 2750 < kal <= 3250:
                diet = str(sheet.row(random.randint(1, 10))[5]).replace('text:', '') \
                    .replace("'", "").replace(" . ", "\n")
            elif 3250 < kal <= 3750:
                diet = str(sheet.row(random.randint(1, 10))[6]).replace('text:', '') \
                    .replace("'", "").replace(" . ", "\n")
            bot.send_message(call.message.chat.id, 'Ваш рацион на день:\n' + diet, reply_markup=keyboard4)
            bot.register_next_step_handler(call.message, get_diet)
    elif sex == 'Ж':
        if call.data == '1':
            a = '1'
            if aim == "Похудеть":
                kal = round(((447.6 + (9.2 * int(ves)) + (3.1 * int(ros)) - (4.3 * int(voz))) * 0.85), 2)
                bot.send_message(call.message.chat.id, 'Ваша норма калорий для похудения = ' + str(kal))
            elif aim == 'Поддерживать':
                kal = round((447.6 + (9.2 * int(ves)) + (3.1 * int(ros)) - (4.3 * int(voz))), 2)
                bot.send_message(call.message.chat.id, 'Ваша норма калорий = ' + str(kal))
            elif aim == 'Набрать':
                kal = round(((447.6 + (9.2 * int(ves)) + (3.1 * int(ros)) - (4.3 * int(voz))) * 1.2), 2)
                bot.send_message(call.message.chat.id, 'Ваша норма калорий для набора = ' + str(kal))
            if 0 < kal <= 750:
                diet = str(sheet.row(random.randint(1, 10))[0]).replace('text:', '') \
                    .replace("'", "").replace(" . ", "\n")
            elif 750 < kal <= 1250:
                diet = str(sheet.row(random.randint(1, 10))[1]).replace('text:', '') \
                    .replace("'", "").replace(" . ", "\n")
            elif 1250 < kal <= 1750:
                diet = str(sheet.row(random.randint(1, 10))[2]).replace('text:', '') \
                    .replace("'", "").replace(" . ", "\n")
            elif 1750 < kal <= 2250:
                diet = str(sheet.row(random.randint(1, 10))[3]).replace('text:', '') \
                    .replace("'", "").replace(" . ", "\n")
            elif 2250 < kal <= 2750:
                diet = str(sheet.row(random.randint(1, 10))[4]).replace('text:', '') \
                    .replace("'", "").replace(" . ", "\n")
            elif 2750 < kal <= 3250:
                diet = str(sheet.row(random.randint(1, 10))[5]).replace('text:', '') \
                    .replace("'", "").replace(" . ", "\n")
            elif 3250 < kal <= 3750:
                diet = str(sheet.row(random.randint(1, 10))[6]).replace('text:', '') \
                    .replace("'", "").replace(" . ", "\n")
            bot.send_message(call.message.chat.id, 'Ваш рацион на день:\n' + diet, reply_markup=keyboard4)
            bot.register_next_step_handler(call.message, get_diet)
        elif call.data == '2':
            a = '2'
            if aim == "Похудеть":
                kal = round((((447.6 + (9.2 * int(ves)) + (3.1 * int(ros)) - (4.3 * int(voz))) * 1.2) * 0.85), 2)
                bot.send_message(call.message.chat.id, 'Ваша норма калорий для похудения = ' + str(kal))
            elif aim == 'Поддерживать':
                kal = round(((447.6 + (9.2 * int(ves)) + (3.1 * int(ros)) - (4.3 * int(voz))) * 1.2), 2)
                bot.send_message(call.message.chat.id, 'Ваша норма калорий = ' + str(kal))
            elif aim == 'Набрать':
                kal = round((((447.6 + (9.2 * int(ves)) + (3.1 * int(ros)) - (4.3 * int(voz))) * 1.2) * 1.2), 2)
                bot.send_message(call.message.chat.id, 'Ваша норма калорий для набора = ' + str(kal))
            if 0 < kal <= 750:
                diet = str(sheet.row(random.randint(1, 10))[0]).replace('text:', '') \
                    .replace("'", "").replace(" . ", "\n")
            elif 750 < kal <= 1250:
                diet = str(sheet.row(random.randint(1, 10))[1]).replace('text:', '') \
                    .replace("'", "").replace(" . ", "\n")
            elif 1250 < kal <= 1750:
                diet = str(sheet.row(random.randint(1, 10))[2]).replace('text:', '') \
                    .replace("'", "").replace(" . ", "\n")
            elif 1750 < kal <= 2250:
                diet = str(sheet.row(random.randint(1, 10))[3]).replace('text:', '') \
                    .replace("'", "").replace(" . ", "\n")
            elif 2250 < kal <= 2750:
                diet = str(sheet.row(random.randint(1, 10))[4]).replace('text:', '') \
                    .replace("'", "").replace(" . ", "\n")
            elif 2750 < kal <= 3250:
                diet = str(sheet.row(random.randint(1, 10))[5]).replace('text:', '') \
                    .replace("'", "").replace(" . ", "\n")
            elif 3250 < kal <= 3750:
                diet = str(sheet.row(random.randint(1, 10))[6]).replace('text:', '') \
                    .replace("'", "").replace(" . ", "\n")
            bot.send_message(call.message.chat.id, 'Ваш рацион на день:\n' + diet, reply_markup=keyboard4)
            bot.register_next_step_handler(call.message, get_diet)
        elif call.data == '3':
            a = '3'
            if aim == "Похудеть":
                kal = round((((447.6 + (9.2 * int(ves)) + (3.1 * int(ros)) - (4.3 * int(voz))) * 1.55) * 0.85), 2)
                bot.send_message(call.message.chat.id, 'Ваша норма калорий для похудения = ' + str(kal))
            elif aim == 'Поддерживать':
                kal = round(((447.6 + (9.2 * int(ves)) + (3.1 * int(ros)) - (4.3 * int(voz))) * 1.55), 2)
                bot.send_message(call.message.chat.id, 'Ваша норма калорий = ' + str(kal))
            elif aim == 'Набрать':
                kal = round((((447.6 + (9.2 * int(ves)) + (3.1 * int(ros)) - (4.3 * int(voz))) * 1.55) * 1.2), 2)
                bot.send_message(call.message.chat.id, 'Ваша норма калорий для набора = ' + str(kal))
            if 0 < kal <= 750:
                diet = str(sheet.row(random.randint(1, 10))[0]).replace('text:', '') \
                    .replace("'", "").replace(" . ", "\n")
            elif 750 < kal <= 1250:
                diet = str(sheet.row(random.randint(1, 10))[1]).replace('text:', '') \
                    .replace("'", "").replace(" . ", "\n")
            elif 1250 < kal <= 1750:
                diet = str(sheet.row(random.randint(1, 10))[2]).replace('text:', '') \
                    .replace("'", "").replace(" . ", "\n")
            elif 1750 < kal <= 2250:
                diet = str(sheet.row(random.randint(1, 10))[3]).replace('text:', '') \
                    .replace("'", "").replace(" . ", "\n")
            elif 2250 < kal <= 2750:
                diet = str(sheet.row(random.randint(1, 10))[4]).replace('text:', '') \
                    .replace("'", "").replace(" . ", "\n")
            elif 2750 < kal <= 3250:
                diet = str(sheet.row(random.randint(1, 10))[5]).replace('text:', '') \
                    .replace("'", "").replace(" . ", "\n")
            elif 3250 < kal <= 3750:
                diet = str(sheet.row(random.randint(1, 10))[6]).replace('text:', '') \
                    .replace("'", "").replace(" . ", "\n")
            bot.send_message(call.message.chat.id, 'Ваш рацион на день:\n' + diet, reply_markup=keyboard4)
            bot.register_next_step_handler(call.message, get_diet)


bot.polling(none_stop=True, interval=0)
