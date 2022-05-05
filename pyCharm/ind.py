#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
import jsonschema
from jsonschema import validate

schema = {
    "type" : "object",
    "properties" : {
        "price" : {"type" : "number"},
        "name" : {"type" : "string"},
        "shop" : {"type" : "string"}
    },
}


def get_goods():
    """
    Запросить данные о товаре.
    """

    name = input("Название товара: ")
    shop = input("Название магазина: ")
    price = float(input("Стоимость: "))

    # Создать словарь.
    return {
        'name': name,
        'shop': shop,
        'price': price,
    }


def display_goods(goods):
    """
    Отобразить список товаров.
    """
    # Проверить, что список товаров не пуст.
    if goods:
        # Заголовок таблицы.
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 8
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^8} |'.format(
                "№",
                "Название",
                "Магазин",
                "Цена"
            )
        )
        print(line)
        # Вывести данные о всех товарах.
        for idx, good in enumerate(goods, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>8} |'.format(
                    idx,
                    good.get('name', ''),
                    good.get('shop', ''),
                    good.get('price', 0)
                )
            )
        print(line)

    else:
        print("Список товаров пуст.")


def select_goods(goods, shop):
    """
    Выбрать товары магазина.
    """

    # Счетчик записей.
    count = 0

    # Сформировать список товаров.
    result = []

    for good in goods:
        if shop == good.get('shop', shop):
            count += 1
            result.append(good)

    # Проверка на отсутствие товаров или выбранного магазина.
    if count == 0:
        print("Такого магазина не существует либо нет товаров.")
    else:
        # Возвратить список выбранных товаров.
        return result


def save_goods(file_name, goods):
    """
    Сохранить все магазины в файл JSON.
    """
    # Открыть файл с заданным именем для записи.
    with open(file_name, "w", encoding="utf-8") as fout:
        # Выполнить сериализацию данных в формат JSON.
        # Для поддержки кирилицы установим ensure_ascii=False
        json.dump(goods, fout, ensure_ascii=False, indent=4)


def load_goods(file_name):
    """
    Загрузить все магазины из файла JSON.
    """
    # Открыть файл с заданным именем для чтения.
    with open(file_name, "r", encoding="utf-8") as fin:
        f = json.load(fin)
    err_count = 0
    print("...валидация...")
    for idx, item in enumerate(f):
        try:
            validate(item, schema)
            sys.stdout.write("Запись {}: OK\n".format(idx))
        except jsonschema.exceptions.ValidationError as ve:
            sys.stderr.write("Запись {}: ОШИБКА\n".format(idx))
            sys.stderr.write(str(ve) + "\n")
            err_count += 1
    if err_count > 0:
        print("JSON-файл не прошел валидацию.\nФайл не будет загружен.")
    else:
        print("JSON-файл успешно загружен")
        return f


def main():
    """
    Главная функция программы.
    """

    # Список товаров.
    goods = []

    # Организовать бесконечный цикл запроса команд.
    while True:
        # Запросить команду из терминала.
        command = input(">>> ").lower()

        # Выполнить действие в соответствие с командой.
        if command == 'exit':
            break

        elif command == 'add':
            # Запросить данные о товаре.
            good = get_goods()

            # Добавить словарь в список.
            goods.append(good)
            # Отсортировать список в случае необходимости.
            if len(goods) > 1:
                goods.sort(key=lambda item: item.get('name', ''))

        elif command == 'list':
            # Отобразить все товары.
            display_goods(goods)

        elif command.startswith('select '):
            # Разбить команду на части для выделения стажа.
            parts = command.split(' ', maxsplit=1)
            # Получить требуемые товары.
            shop = parts[1]

            # Выбрать товары ммагазина.
            selected = select_goods(goods, shop)
            # Отобразить выбранные товары.
            display_goods(selected)

        elif command.startswith("save "):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]

            # Сохранить данные в файл с заданным именем.
            save_goods(file_name, goods)

        elif command.startswith("load "):
            # Разбить команду на части для выделения имени файла.
            parts = command.split(maxsplit=1)
            # Получить имя файла.
            file_name = parts[1]

            # Сохранить данные в файл с заданным именем.
            goods = load_goods(file_name)

        elif command == 'help':
            # Вывести справку о работе с программой.
            print("Список команд:\n")
            print("add - добавить товар;")
            print("list - вывести список товаров;")
            print("select <имя магазина> - запросить товары магазина;")
            print("help - отобразить справку;")
            print("exit - завершить работу с программой.")
        else:
            print(f"Неизвестная команда {command}", file=sys.stderr)


if __name__ == '__main__':
    main()
