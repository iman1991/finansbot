import sqlite3


def boardText(raw):
    return "Кто получил: {}\nТип тразакции: #{}\nСумма: {}\nОт кого получил: {}\nДата: {}"\
        .format(raw[1], raw[2], raw[3], raw[4], raw[5])


def BDConn():
    conn = sqlite3.connect('my.sqlite')
    return conn, conn.cursor()

def BDClosse(conn, c):
    conn.commit()
    c.close()
    conn.close()