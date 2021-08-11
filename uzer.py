def transfer(user_id):
    cards = read_file_key("cards.csv", "Пользователь", user_id)
    index = 1
    print("Какой картой вы хотите воспользоваться?\nВыбор Номер карточки Деньги")
    for number in enumerate(cards["Номер"]):
        print(index, number[1], cards["Деньги"][number[0]] + "$")
    number = check_int("Ваш выбор: ")
    receiver = input("Номер карты, на которую вы хотите перевести деньги: ")
    all_cards = read_file("cards.csv")
    if receiver in all_cards["Номер"]:
        money = check_int("Количество денег, которые вы хотите отправить: ")
        update_file("cards.csv", cards["Номер"][number-1], "Номер", int(cards["Деньги"][number - 1])-money, "Деньги")
        update_file("cards.csv", receiver, "Номер", int(all_cards["Деньги"][all_cards["Номер"].index(receiver)])+money,
                    "Деньги")
        record("history.csv", [cards["Номер"][number-1], user_id, "Отправлен перевод на "+str(money)+"$. Остаток: "
                               + str(int(cards["Деньги"][number - 1])-money)], ["Номер", "id", "История"])
        record("history.csv", [receiver, all_cards["Пользователь"][all_cards["Номер"].index(receiver)],
                               "Получен перевод на "+str(money)+"$. Остаток: "
                               + str(int(all_cards["Деньги"][all_cards["Номер"].index(receiver)])+money)],
                               ["Номер", "id", "История"])
    else:
        print("Нет такой карты")


def get_transfer(user_id):
    cards = read_file_key("cards.csv", "Пользователь", user_id)
    print("На какую карточку вы бы хотели получить перевод?\nВыбор Номер карточки Деньги")
    for number in enumerate(cards["Номер"]):
        print(number[0] + 1, number[1], cards["Деньги"][number[0]] + "$")
    number = check_int("Ваш выбор: ")  # cards["Статус"][number-1]
    money = check_int("Сколько? ")
    update_file("cards.csv", cards["Номер"][number - 1], "Номер", int(cards["Деньги"][number - 1]) + money, "Деньги")
    record("history.csv", [cards["Номер"][number - 1], user_id, "Был получен перевод на " + str(money) +
                           "\nОстаток на карте: " + str(int(cards["Деньги"][number - 1]) + money)],
           ["Номер карты", "id", "История"])


def block_cards(user_id):
    cards = read_file_key("cards.csv", "Пользователь", user_id)
    print("Какую карточку вы бы хотели заблокировать/разблокировать\nВыбор Номер карточки Деньги")
    for number in enumerate(cards["Номер"]):
        print(number[0] + 1, number[1], cards["Деньги"][number[0]] + "$")
    number = check_int("Ваш выбор: ")
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
    number = check_int("Ваш выбор: ")
    print(read_file_key("history.csv", "Номер", cards["Номер"][number - 1]))


def client_menu(user_id):
    while True:
        print(
            "Меню:\n1 - Перевести на карту\n2 - Платёж\n3 - (Раз)Блокировка карты" +
            "\n4 - Получить перевод\n5 - Выписка карты\n6 - Добавить карту\n7 - Вывести все карты\n8 - Выход")
        choice = int(input("Введите ваш выбор: "))
        if choice == 1:
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
            info = read_file_key("cards.csv", 'Пользователь', user_id)
            print(info)
        elif choice == 8:
            break


def check_history():
    users = read_file("registration.csv")
    for user in enumerate(users['id']):
        print(user[0] + 1, user[1], users["ФИО"][user[0]], users["Телефон"][user[0]])
    user = check_int("Ваш выбор: ")
    print(read_file_key("history.csv", 'id', users['id'][user - 1]))


def delete_user():
    user = input("Введите id пользователя, которого хотите удалить: ")
    users = read_file("registration.csv")
    print(users['id'])
    index = users['id'].index(user)
    for key in users.keys():
        users[key].pop(index)
    for index in range(len(users['id'])):
        row = []
        for val in users.values():
            row.append(val[index])
        record("registration.csv", row, list(users.keys()), 'w' if index == 0 else 'a')