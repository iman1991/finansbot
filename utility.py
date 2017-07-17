import sqlite3


def boardText(raw):
    desk = "От кого получил:"if raw[2] == "Кредит" else "На что потрачены:"
    return "Номер транзакции {0}\nКто получил: {1}\nТип тразакции: #{2}\nСумма: {3}\n{6} {4}\nДата: {5}"\
        .format(raw[0],raw[1], raw[2], raw[3], raw[4], raw[5], desk)


def BDConn():
    conn = sqlite3.connect('my.sqlite')
    return conn, conn.cursor()

def BDClosse(conn, c):
    conn.commit()
    c.close()
    conn.close()