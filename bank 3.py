import csv
import os
import random


def read_file_key(path, key, value):
    with open(path, 'r', encoding='utf-8') as f:
        f_reader = csv.DictReader(f, delimiter=';')
        content = {key: [] for key in f_reader.fieldnames}
        for line in f_reader:
            if line[key] == value:
                for k, v in line.items():
                    content[k].append(v)
        return content


def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        f_reader = csv.DictReader(f, delimiter=';')
        content = {key: [] for key in f_reader.fieldnames}
        for line in f_reader:
            for key, value in line.items():
                content[key].append(value)
        return content


def update_file(path, line, key, update, key_update):  # line - значение, по которому искать
    content = read_file(path)
    for value in enumerate(content[key]):
        if value[1] == line:
            content[key_update][value[0]] = update
    with open(path, 'w', encoding='utf-8') as f:
        f_writer = csv.writer(f, delimiter=";")
        f_writer.writerow(content.keys())
        cont_val = content.values()
        row = []
        for value in enumerate(content[key]):
            for val in list(cont_val):
                row.append(val[value[0]])
            f_writer.writerow(row)


def record(path, data, header):
    with open(path, mode='a', encoding='utf-8') as f:
        f_writer = csv.writer(f,
                              delimiter=";")  # использую ; как делимитер, так как возможно позже мы будем добавлять туда списки, а списки используют запятую, как разделитель
        if os.stat(path).st_size == 0:  # на случай, если у нас пустой файл, запишем в него название столбиков
            f_writer.writerow(header)
        f_writer.writerow(data)


def registration():
    print("Добрый день, вас приветствует Альфа-банк, введите, пожалуйста необходимые данные для регистрации")
    fio = input("Введите, пожалуйста ФИО: ")
    while True:
        phone = input("Введите, пожалуйста ваш телефон: ")
        if phone[:4] == "+375":
            if phone[1:].isdigit():
                if len(phone) == 13:
                    break
        print("Введите номер ещё раз")
    while True:
        mail = input("Введите имейл: ")
        if '@' in mail:
            if '.' in mail[mail.index("@"):]:
                break
        print("Введите имейл ещё раз")
    login = input("Введите логин: ")
    password = input("Введите пароль: ")
    record("registration.csv", [random.randint(1000, 9999), fio, phone, mail, login, password],
           ["id", "ФИО", "Телефон", "Почта", "Логин", "Пароль"])
    return fio


def enter():
    while True:
        try:
            login = input("Введите логин: ")
            password = input("Введите пароль: ")
            with open("registration.csv", 'r', encoding='utf-8') as f:
                f_reader = csv.DictReader(f, delimiter=";")
                for line in f_reader:
                    if line["Логин"] == login and line["Пароль"] == password:
                        print(f'Добро пожаловать, {line["ФИО"]}')
                        return line["id"]
        except FileNotFoundError:
            print("Нет записей ещё ни об одном пользователе, зарегестрируйте кого-нибудь.")
            return False


def add_cart(userid):
    number = input("Введите номер карты: ")
    cvv = random.randint(100, 999)
    record("cards.csv", [number, userid, cvv, 0, "Разблокирована"],
           ["Номер", "Пользователь", "CVV", "Деньги", "Статус"])
    record("history.csv", [number, userid, "Карточка была создана"], ["Номер", "id", "История"])


def transfer(user_id):
    cards = read_file_key("cards.csv", "Пользователь", user_id)
    index = 1
    print("Какой картой вы хотите воспользоваться?\nВыбор Номер карточки Деньги")
    for number in enumerate(cards["Номер"]):
        print(index, number[1], cards["Деньги"][number[0]] + "$")
    number = int(input("Ваш выбор: "))
    reciever = int(input("Номер карты, на которую вы хотите перевести деньги: "))
    money = int(input("Количество денег, которые вы хотите отправить: "))
    update_file("cards.csv", reciever["Номер"][number - 1], "Номер", int(reciever["Деньги"][number - 1]) + money, "Деньги")
    record("history.csv", [reciever["Номер"][number - 1], user_id, "Произведен перевод на " + str(money) +
                           "\nОстаток на карте: " + str(int(reciever["Деньги"][number - 1]) + money)],
           ["Номер карты", "id", "История"])


def get_transfer(user_id):
    cards = read_file_key("cards.csv", "Пользователь", user_id)
    print("На какую карточку вы бы хотели получить перевод?\nВыбор Номер карточки Деньги")
    for number in enumerate(cards["Номер"]):
        print(number[0] + 1, number[1], cards["Деньги"][number[0]] + "$")
    number = int(input("Ваш выбор: "))
    money = int(input("Сколько? "))
    update_file("cards.csv", cards["Номер"][number - 1], "Номер", int(cards["Деньги"][number - 1]) + money, "Деньги")
    record("history.csv", [cards["Номер"][number - 1], user_id, "Был получен перевод на " + str(money) +
                           "\nОстаток на карте: " + str(int(cards["Деньги"][number - 1]) + money)],
           ["Номер карты", "id", "История"])


def block_cards(user_id):
    cards = read_file_key("cards.csv", "Пользователь", user_id)
    print("Какую карточку вы бы хотели заблокировать/разблокировать\nВыбор Номер карточки Деньги")
    for number in enumerate(cards["Номер"]):
        print(number[0] + 1, number[1], cards["Деньги"][number[0]] + "$")
    number = int(input("Ваш выбор: "))
    update_file("cards.csv", cards["Номер"][number - 1], "Номер", "Заблокирована"
                if cards["Статус"][number - 1] == "Разблокирована" else "Разблокирована",
                "Статус"
                )
    record("history.csv", [cards["Номер"][number - 1], user_id, "Карта была заблокирована"
           if cards["Статус"][number - 1] == "Разблокирована" else "Карта была разблокирована"],
           ["Номер карты", "id", "История"])


def history(user_id):
    cards = read_file_key("cards.csv", "Пользователь", user_id)
    print("Историю какой карточки вы бы хотели посмотреть?\nВыбор Номер карточки Деньги")
    for number in enumerate(cards["Номер"]):
        print(number[0] + 1, number[1], cards["Деньги"][number[0]] + "$")
    number = int(input("Ваш выбор: "))
    print(read_file_key("history.csv", "Номер карты", cards["Номер"][number - 1]))


def client_menu(user_id):
    while True:
        print(
            "Меню:\n1 - Перевести на карту/счёт\n2 - Платёж\n3 - (Раз)Блокировка карты" +
            "\n4 - Получить перевод\n5 - Выписка карты\n6 - Добавить карту\n7 - Вывести все карты\n8 - Выход")
        choice = int(input("Введите ваш выбор"))
        if choice == 1:
            question = input("Вы хотите перевести на карту или на счёт? [1(карта), 2(счёт)]")
            if int(question) == 1:
                transfer(user_id)
        elif choice == 2:
            pass
        elif choice == 3:
            block_cards(user_id)
        elif choice == 4:
            get_transfer(user_id)
        elif choice == 5:
            history(user_id)
        elif choice == 6:
            add_cart(user_id)
        elif choice == 7:
            info = read_file("cards.csv")
            print(info)
        elif choice == 8:
            break


def check_history():
    users = read_file("registration.csv")
    for user in enumerate(users['id']):
        print(user[0]+1, user[1], users["ФИО"][user[0]], users["Телефон"][user[0]])
    user = int(input("Ваш выбор: "))
    print(read_file_key("history.csv", 'id', users['id'][user-1]))


def delete_user():
    users = read_file("registration.csv")
    for user in enumerate(users['id']):



def admin_menu():
    print(
        "Меню:\n1 - Добавить пользователя\n2 - Посмотреть историю пользователей\n3 - Удалить пользователя\n4 - Выход")
    choice = input("Ваш выбор: ")
    if choice == "1":
        registration()
    if choice == "2":
        check_history()
    if choice == "3":

while True:
    command = input("1- Вход, 2- Регистрация: ")
    if command == "1":
        user_id = enter()
        if user_id:
            if user_id == "3863":
                admin_menu()
            else:
                client_menu(user_id)
    elif command == "2":
        fio = registration()
        print("Пользователь, " + fio + " успешно зарегистрирован")
