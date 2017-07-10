from telebot import types

userKeys = types.ReplyKeyboardMarkup()
userKeys.row('Получил деньги', 'Потратил деньги')
userKeys.row('Посмотреть свою статистику')

statisticsMenu = types.ReplyKeyboardMarkup()
statisticsMenu.row("Статистика полученных средств", "Статистика потраченных средств")
statisticsMenu.row("Показать всю статистику", "Статистика по работникам")
statisticsMenu.row('Получил деньги', 'Потратил деньги')

adminMenu = types.ReplyKeyboardMarkup()
adminMenu.row('Добавить администратора')
adminMenu.row('Удалить администратора')
adminMenu.row('Добавить пользователя')
adminMenu.row('Удалить пользователя')
adminMenu.row('Назад')

main_menu = types.ReplyKeyboardMarkup()
main_menu.row("Управление")
main_menu.row("Работа")

kassKeys = types.ReplyKeyboardMarkup()
kassKeys.add('Расчетный счет', 'Наличные Хасай', 'Наличиные Магомед', 'Касса в Сбербанке')
