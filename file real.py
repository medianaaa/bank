import csv
import os

def read_file_key(path, key, value):  # функция для нахождения в файле с записей с каким-то определённым ключом
    # path - путь к файлу, key - ключ, по которому буду искать, value - значение этого ключа
    try:  # блок try еобходим, чтобы нам не выбило исключение, когда мы будем читать файл, на случай, если его нет
        with open(path, 'r', encoding='utf-8') as f:  # открываю файлик конструкцией with, чтобы потом он сам автоматически закрылся
            f_reader = csv.DictReader(f, delimiter=';')  # создаю объект типа DictReader, позволяет нам работать с данными в файлике, почти как со словарём
            content = {key: [] for key in f_reader.fieldnames}  # генератор словаря .fieldnames - ключи в DictReader
            for line in f_reader:  # перебор каждой строки с ключами в DictReader
                if line[key] == value:  # проверка на то, подходит ли нам эта строчка
                    for k, v in line.items():  # запись всех значений из нужных строк в словарь, который будем выводить
                        content[k].append(v)
        return content  # возвращаем наш словарик
    except FileNotFoundError:  # обработка ошибки
        print("Сделайте записи, пока читать нечего")
        return False


def read_file(path):  # та же реализация, что и в прошлой функции
    with open(path, 'r', encoding='utf-8') as f:
        f_reader = csv.DictReader(f, delimiter=';')
        content = {key: [] for key in f_reader.fieldnames}
        for line in f_reader:
            for key, value in line.items():
                content[key].append(value)
        return content


def update_file(path, line, key, update, key_update):  # функция для обновления данных в файле
    # path - путь к файлу, line - значение ключа, по которому надо найти строчку, которую будем обновлять
    # key - ключ для нахождения строчки, которую мы будем обновлять, update - новое значение, key_update - ключ,
    # в котором надо изменить значение
    content = read_file(path)   # получаю данные из файла в виде словаря {"id": [1,2,3], "ФИО": ["Артур", "Алеся"] и т.д.
    for value in enumerate(content[key]):  # пробегаюсь по всем значениям ключа key
        if value[1] == line:  # нахожу нужный
            content[key_update][value[0]] = update  # обновляю данные
    with open(path, 'w', encoding='utf-8') as f:  # открываю файлик для записи
        f_writer = csv.writer(f, delimiter=";")  # создаю объект типа writer для записи в файл
        f_writer.writerow(content.keys())  # записываю в файл шапку
        cont_val = content.values()  # необязательная строчка, можно потом и убрать и просто использовать content.values
        row = []  # объявление списка
        for value in enumerate(content[key]):  # строка для того, что пробежаться по всем значениям в списках значений
            # можно заменить на for value in range(len(content[key]))
            row.clear()  # очищаю список для того, чтобы записать туда следующие данные
            for val in list(cont_val):  # затем цикл для каждого списка, который содержит у нас значения ключи
                # обратите внимание просто на то, в каком формате приходят данные и станет легче
                row.append(val[value[0]])   # соответственно, добавляю в выводящий список значения
            f_writer.writerow(row)  # записывваю список в файлик


def record(path, data, header, mode='a'):
    with open(path, mode=mode, encoding='utf-8') as f:
        f_writer = csv.writer(f,
                              delimiter=";")  # использую ; как делимитер, так как возможно позже мы будем добавлять туда списки, а списки используют запятую, как разделитель
        if os.stat(path).st_size == 0:  # на случай, если у нас пустой файл, запишем в него название столбиков
            f_writer.writerow(header)
        f_writer.writerow(data)