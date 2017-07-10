import telebot
from telebot import types
import sqlite3
import datetime
import buttons
import config
import utility

bot = telebot.TeleBot(token=config.token)




@bot.message_handler(commands = ['start'])
def main_admin_desk(message):
    if message.chat.id == 27390261:
        bot.send_message(message.chat.id, "Выберите действие", reply_markup=buttons.main_menu)
        conn, c = utility.BDConn()
        c.execute('SELECT * FROM users')
        s = ""
        for raw in c.fetchall():
            s = "%sID=%s, имя %s статус %s \n" % (s, raw[0], raw[1], raw[2])
        if s != "":
            bot.send_message(message.chat.id, s, reply_markup=buttons.adminMenu)
        utility.BDClosse(conn, c)
    else:
        main_desk(message)


@bot.message_handler(regexp="Получил деньги")
def receivedMoney(message):
    msg = bot.send_message(message.chat.id, "Сколько получили?")
    bot.register_next_step_handler(msg, db_take1)


@bot.message_handler(regexp="Потратил деньги")
def receivedMoney(message):
    msg = bot.send_message(message.chat.id, "Сколько потратил?")
    bot.register_next_step_handler(msg, db_give)


@bot.message_handler(regexp="Посмотреть свою статистику")
def myStatistic(message):
    bot.send_message(message.chat.id, "Вот ваша статистика: ")
    conn , c = utility.BDConn()
    c.execute("SELECT * FROM trans WHERE id = %s and num = 1 " % message.chat.id )
    bot.send_message(message.chat.id, "----Получено----")

    for row in c:
        bot.send_message(message.chat.id, "Кто получил: " + str(row[1]) + "\nТип тразакции: #" + str(row[2]) + "\nСумма: " + str(row[3]) + "\nОписание товара: " + str(row[4]) + "\nДата: " + str(row[5]))
    c.execute("SELECT * FROM trans WHERE id = %s and num = 0 " % message.chat.id )

    bot.send_message(message.chat.id, "----Потрачено----")
    for row in c:
        bot.send_message(message.chat.id, "Кто получил: " + str(row[1]) + "\nТип тразакции: #" + str(row[2]) + "\nСумма: " + str(row[3]) + "\nОт кого получил: " + str(row[4]) + "\nДата: " + str(row[5]))

    utility.BDClosse(conn, c)

@bot.message_handler(regexp="Статистика полученных средств")
def statOfDebitAll(message):
    conn = sqlite3.connect('my.sqlite')

    bot.send_message(message.from_user.id, "OK")
    conn , c = utility.BDConn()
    c.execute("SELECT id FROM users WHERE admin = 1 and id = ? ", (message.from_user.id,))
    print(c.fetchone())
    c.execute('SELECT * FROM trans WHERE num = 0 ')
    for row in c:
        bot.send_message(message.chat.id, utility.boardText(row))
    utility.BDClosse(conn, c)


@bot.message_handler(regexp="Статистика потраченных средств")
def statOfCreditAll(message):
    bot.send_message(message.chat.id, "Отлично, вот таблица: ")
    conn , c = utility.BDConn()
    if message.chat.id == message.chat.id:
        c.execute('SELECT * FROM trans WHERE num = 1 ')
        for row in c:
            bot.send_message(message.chat.id, utility.boardText(row))
    utility.BDClosse(conn, c)


@bot.message_handler(regexp="Показать всю статистику")
def statAll(message):
    bot.send_message(message.chat.id, "Отлично, вот таблица: ")
    conn , c = utility.BDConn()
    if message.chat.id == message.chat.id:
        c.execute('SELECT * FROM trans WHERE num = 1 ')
        bot.send_message(message.chat.id, "----Получено----")
        for row in c:
            bot.send_message(message.chat.id, utility.boardText(row))
        c.execute('SELECT * FROM trans WHERE num = 0 ')
        bot.send_message(message.chat.id, "----Потрачено----")
        for row in c:
            bot.send_message(message.chat.id, utility.boardText(row))
    utility.BDClosse(conn, c)

@bot.message_handler(regexp="Статистика по работникам")
def specific_employee(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=0.5, resize_keyboard=True)
    conn , c = utility.BDConn()
    c.execute('SELECT * FROM users')
    for row in c:
        keyboard.add(row[1])
    msg = bot.send_message(message.chat.id, "Выберите работника: ", reply_markup=keyboard)
    utility.BDClosse(conn, c)
    bot.register_next_step_handler(msg, output)


def main_desk(message):

    conn, c = utility.BDConn()
    resc = 0
    c.execute("SELECT id FROM users WHERE admin = 1 and id = :id ", ({"id": str(message.from_user.id)}))
    for row in c:
        print(row)
        bot.send_message(message.chat.id, "Выберите действие", reply_markup=buttons.statisticsMenu)
        conn.commit()
        resc = 1
    if resc == 1:
        return
    c.execute("SELECT id FROM users WHERE admin = 0 and id = ? ", (message.from_user.id,))
    for row in c:
        print(row)
        resc = 2
        cash_messages(message)
    if resc == 0:
        bot.send_message(message.from_user.id, "Вы не зарегистрированы в систем\n"
                                               "Подождите пока вас добавят")
        bot.send_message(27390261, "Тут чувак стучится во его данные ")
        bot.send_message(27390261, "{}".format(message.from_user))
    utility.BDClosse(conn, c)


@bot.message_handler(regexp="Добавить пользователя")
def decor(message):
    msg = bot.send_message(message.chat.id, "Укажите id пользователя, которого надо добавить")
    bot.register_next_step_handler(msg, add_user_1)

@bot.message_handler(regexp="Добавить администратора")
def decor(message):
    msg = bot.send_message(message.chat.id, "Укажите id администратора, которого надо добавить")
    bot.register_next_step_handler(msg, add_admin)


@bot.message_handler(regexp="Удалить администратора")
def decor(message):
    msg = bot.send_message(message.chat.id, "Укажите его id, которого надо удалить")
    bot.register_next_step_handler(msg, delete_admin)


@bot.message_handler(regexp="Удалить пользователя")
def decor(message):
    msg = bot.send_message(message.chat.id, "Укажите id пользователя, которого надо удалить")
    bot.register_next_step_handler(msg, delete_user)


def add_admin(message):
    conn, c = utility.BDConn()
    c.execute('UPDATE users SET admin = 1 where id = %s ' % message.text)
    utility.BDClosse(conn, c)
    bot.send_message(int(message.text), "Теперь вы администратор", reply_markup=buttons.statisticsMenu)
    bot.send_message(27390261, "администратор добавлен")


def delete_admin(message):
    conn, c = utility.BDConn()
    c.execute('UPDATE users SET admin = 0 where id = %s ' % message.text)
    utility.BDClosse(conn, c)


def add_user_1(message):
    global namik
    namik = message.text
    conn, c = utility.BDConn()
    c.execute("INSERT INTO users(id) VALUES('%s')" % message.text )
    utility.BDClosse(conn, c)
    msg = bot.send_message(message.chat.id, "Укажите имя пользователя")
    bot.register_next_step_handler(msg, add_user_all)


def add_user_all(message):
    conn, c = utility.BDConn()
    c.execute("UPDATE users SET name = ?, admin = '0' WHERE id = ?", (message.text, namik))
    utility.BDClosse(conn, c)
    bot.send_message(int(namik), "Вы добавлены в систему отчета", reply_markup=buttons.userKeys)
    bot.send_message(27390261, "Пользователь добавлен")


def delete_user(message):
    conn, c = utility.BDConn()
    c.execute('DELETE FROM users WHERE id = ' + message.text + '')
    utility.BDClosse(conn, c)


def cash_messages(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add('Получил деньги', 'Потратил деньги', 'Посмотреть свою статистику')
    bot.send_message(message.chat.id, "Ввидите команду", reply_markup=keyboard)


def output(message):
    conn, c = utility.BDConn()
    c.execute('SELECT * FROM trans WHERE uin = ? and num = ?', (message.text, '1'))
    bot.send_message(message.chat.id, "---Потрачено---")
    for row in c:
        bot.send_message(message.chat.id, utility.boardText(row))
    bot.send_message(message.chat.id, "---Получено---")
    c.execute('SELECT * FROM trans WHERE uin = ? and num = ?', (message.text, '0'))
    for row in c:
        bot.send_message(message.chat.id, utility.boardText(row))
    utility.BDClosse(conn, c)


def db_take1(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add('База Домалогика', 'База Производство', 'От Клиента')
    global cash_count_take
    cash_count_take = message.text
    msg = bot.send_message(message.chat.id, "От кого вы получили средства?", reply_markup=keyboard)
    bot.register_next_step_handler(msg, db_take2)


def db_take2(message):
    if message.text == 'База Домалогика':
        msg = bot.send_message(message.chat.id, "Выберите способ получения средств", reply_markup=buttons.kassKeys)
        bot.register_next_step_handler(msg, domalogika)

    if message.text == 'База Производство':
        msg = bot.send_message(message.chat.id, "Выберите способ получения средств", reply_markup=buttons.kassKeys)
        bot.register_next_step_handler(msg, factory)

    if message.text == 'От Клиента':
        msg = bot.send_message(message.chat.id, "Введите имя клиента")
        bot.register_next_step_handler(msg, client)



def factory(message):
    tday = datetime.date.today()
    tdelta = datetime.timedelta()
    conn, c = utility.BDConn()
    if message.text == 'Расчетный счет':
        c.execute("INSERT INTO trans(id, uin, trans, sum, description, time, num) VALUES(?,?,?,?,?,?,?)", (
            message.chat.id, message.chat.first_name, "Кредит", cash_count_take, "База Производство, "+ str(message.text), tday - tdelta, "1"))
        bot.send_message(message.chat.id, "Отлично данные о получении " + cash_count_take + " р. были отправлены  в базу данных")

    if message.text == 'Наличные Хасай':
        c.execute("INSERT INTO trans(id, uin, trans, sum, description, time, num) VALUES(?,?,?,?,?,?,?)", (
            message.chat.id, message.chat.first_name, "Кредит", cash_count_take,"База Производство, " + str(message.text), tday - tdelta, "1"))
        bot.send_message(message.chat.id,"Отлично данные о получении " + cash_count_take + " р. были отправлены  в базу данных")

    if message.text == 'Наличиные Магомед':
        c.execute("INSERT INTO trans(id, uin, trans, sum, description, time, num) VALUES(?,?,?,?,?,?,?)", (
            message.chat.id, message.chat.first_name, "Кредит", cash_count_take,"База Производство, " + str(message.text), tday - tdelta, "1"))
        bot.send_message(message.chat.id,"Отлично данные о получении " + cash_count_take + " р. были отправлены  в базу данных")

    if message.text == 'Касса в Сбербанке':
        c.execute("INSERT INTO trans(id, uin, trans, sum, description, time, num) VALUES(?,?,?,?,?,?,?)", (
            message.chat.id, message.chat.first_name, "Кредит", cash_count_take,"База Производство, " + str(message.text), tday - tdelta, "1"))
        bot.send_message(message.chat.id,"Отлично данные о получении " + cash_count_take + " р. были отправлены  в базу данных")
    utility.BDClosse(conn, c)



def domalogika(message):
    tday = datetime.date.today()
    tdelta = datetime.timedelta()
    conn, c = utility.BDConn()

    if message.text == 'Расчетный счет':
        c.execute("INSERT INTO trans(id, uin, trans, sum, description, time, num) VALUES(?,?,?,?,?,?,?)", (
            message.chat.id, message.chat.first_name, "Кредит", cash_count_take, "База Домалогика, "+ str(message.text), tday - tdelta, "1"))
        bot.send_message(message.chat.id, "Отлично данные о получении " + cash_count_take + " р. были отправлены  в базу данных")

    if message.text == 'Наличные Хасай':
        c.execute("INSERT INTO trans(id, uin, trans, sum, description, time, num) VALUES(?,?,?,?,?,?,?)", (
            message.chat.id, message.chat.first_name, "Кредит", cash_count_take,"База Домалогика, " + str(message.text), tday - tdelta, "1"))
        bot.send_message(message.chat.id,"Отлично данные о получении " + cash_count_take + " р. были отправлены  в базу данных")

    if message.text == 'Наличиные Магомед':
        c.execute("INSERT INTO trans(id, uin, trans, sum, description, time, num) VALUES(?,?,?,?,?,?,?)", (
            message.chat.id, message.chat.first_name, "Кредит", cash_count_take,"База Домалогика, " + str(message.text), tday - tdelta, "1"))
        bot.send_message(message.chat.id,"Отлично данные о получении " + cash_count_take + " р. были отправлены  в базу данных")

    if message.text == 'Касса в Сбербанке':
        c.execute("INSERT INTO trans(id, uin, trans, sum, description, time, num) VALUES(?,?,?,?,?,?,?)", (
            message.chat.id, message.chat.first_name, "Кредит", cash_count_take,"База Домалогика, " + str(message.text), tday - tdelta, "1"))
        bot.send_message(message.chat.id,"Отлично данные о получении " + cash_count_take + " р. были отправлены  в базу данных")
    utility.BDClosse(conn, c)



def client(message):
    tday = datetime.date.today()
    tdelta = datetime.timedelta()
    conn, c = utility.BDConn()

    take_client = message.text
    bot.send_message(message.chat.id,"Отлично, данные о получении " + cash_count_take + " р. были отправлены в базу данных")
    c.execute("INSERT INTO trans(id, uin, trans, sum, description, time, num) VALUES(?,?,?,?,?,?,?)",
              (message.chat.id, message.chat.first_name, "Кредит", cash_count_take, take_client, tday - tdelta, "1"))
    utility.BDClosse(conn, c)


def db_give(message):
    global cash_count_give
    cash_count_give = message.text
    msg = bot.send_message(message.chat.id, "На что потратили средства?")
    bot.register_next_step_handler(msg, db_give2)


def db_give2(message):
    tday = datetime.date.today()
    tdelta = datetime.timedelta()
    bot.send_message(message.chat.id, "Отлично, данные о рaстрате " + cash_count_give + " р. были отправены в базу данных")
    conn, c = utility.BDConn()
    c.execute("INSERT INTO trans(id, uin, trans, sum, description, time, num) VALUES(?,?,?,?,?,?,?)",
              (message.chat.id, message.chat.first_name, "Дебет", cash_count_give, message.text, tday-tdelta, "0"))
    utility.BDClosse(conn, c)

if __name__ == '__main__':
    bot.polling(none_stop=True)
