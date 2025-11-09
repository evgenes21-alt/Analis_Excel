# import json
# import logging
# from datetime import datetime
# from pathlib import Path
#
# import pandas as pd
# from dotenv import load_dotenv
#
# from src.reports import spending_by_category
# from src.services import search_phones
# from src.utils import filter_by_dates, greeting, read_currencies_and_stocks_from_json
# from src.views import cards_total_spent, get_currency_rates, get_stock_prices, get_top_transactions
#
# BASE_DIR = Path(__file__).parent.parent  # НЕ преобразуем в str!
# transactions_path = BASE_DIR / "data"
# results_path = BASE_DIR / "results"
# main_logs_path = BASE_DIR / "logs" / "main.log"
#
#
#
#
# # BASE_DIR = str(Path(__file__).parent.parent)  # корневая папка проекта
# # transactions_path = BASE_DIR + '\\data'
# # results_path = BASE_DIR + '\\results'
# # main_logs_path = BASE_DIR + r'\logs\main.log'
#
# # настраиваем параметры логирования
# main_logger = logging.getLogger("main")
# file_handler = logging.FileHandler(main_logs_path, "w", encoding="UTF-8")
# file_formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s: %(message)s')
# file_handler.setFormatter(file_formatter)
# main_logger.addHandler(file_handler)
# main_logger.setLevel(logging.INFO)
#
# # загружаем ключи
# #load_dotenv(BASE_DIR + '\\.env')
# load_dotenv(BASE_DIR / ".env")
#
#
# def app_main(current_date_str: str, transaction_file: str, file_path=None) -> None:
#     """
#     Основная функция, объединяющая все модули приложения.
#     Переменные stock_prices и currency_rates на 80 и 81 строчке
#     были введены временно в качестве заглушек, чтобы не тратить
#     драгоценный лимит на запрос по API)).
#     """
#
#     # BASE_DIR = str(Path(__file__).parent.parent)  # корневая папка проекта
#     # transactions_path = BASE_DIR + '\\data'
#     # results_path = BASE_DIR + '\\results'
#     transaction_file = "operations.xlsx" # правильно
#     # НЕ надо: r'\operations.xlsx'
#     # print("=== ДИАГНОСТИКА ПУТЕЙ ===")
#     # print(f"__file__: {__file__}")
#     # print(f"BASE_DIR: {BASE_DIR}")
#     # print(f"transactions_path: {transactions_path}")
#     # print(f"transaction_file: {transaction_file}")
#     # print(f"file_path: {file_path}")
#     # print(f"Файл существует: {file_path.exists()}")
#     # print("=========================")
#
#     file_path = transactions_path / transaction_file
#     if not file_path.exists():
#         main_logger.error(f"Файл не найден: {file_path}")
#         raise FileNotFoundError(f"Файл не найден: {file_path}")
#
#     print(f"Проверяем существование: {file_path}")
#     print(f"Файл существует: {file_path.exists()}")
#     if not file_path.exists():
#         print(f"Директория {file_path.parent} существует: {file_path.parent.exists()}")
#         print(f"Содержимое директории {file_path.parent}:")
#         for item in file_path.parent.iterdir():
#             print(f"  {item.name}")
#
#     print("\nЧитаю excel файл с транзакциями, может занять некоторое время...")
#
#     try:
#         # пытаемся открыть и сохранить датафрейм из эксель файла
#         transactions = pd.read_excel(transactions_path + transaction_file)  # оригинал
#         main_logger.info(f"Успешное чтение файла {transactions_path + transaction_file}")
#
#         # -------------------- Веб-страница --------------------
#         # ------------------ Страница "Главная" ----------------
#
#         # конвертируем даты в datetime формат
#         # и определяем первый день месяца
#         current_date = datetime.strptime(current_date_str, '%d.%m.%Y %H:%M:%S')
#         start_date_main = current_date.replace(day=1, hour=0, minute=0, second=0)
#
#         print("\nСтраница 'Главная'")
#         print(f"Начало отчетного периода: {start_date_main}")
#         print(f"Конец отчетного периода: {current_date}")
#
#         # Фильтруем диапазон по начальной и текущей дате
#         # с учетом статуса (ОК)
#         filtered_by_dates = filter_by_dates(transactions, start_date_main, current_date)
#
#         # Формируем приветствие в зависимости от времени суток
#         greeting_message = greeting(current_date)
#
#         # получаем список словарей, где ключами являются номер карты, общая сумма расходов, кэшбэк
#         cards_total_expences = cards_total_spent(filtered_by_dates)
#
#         # Получаем топ 5 транзакций с наибольшей суммой платежа
#         top_transactions = get_top_transactions(filtered_by_dates)
#
#         currencies, stocks = read_currencies_and_stocks_from_json()
#         currency_rates = get_currency_rates(currencies)  # функция рабочая, временно отключена
#         stock_prices = get_stock_prices(stocks)  # функция рабочая, временно отключена
#         # stock_prices = []  # временная заглушка, потом нужно ее удалить и раскомментировать верхнюю строчку
#         # currency_rates = []  # временная заглушка, потом нужно ее удалить и раскомментировать верхнюю строчку
#
#         # Формируем словарь перед конвертацией в json согласно формату, представленному в тз
#         main_page = {
#             "greeting": greeting_message,
#             "cards": cards_total_expences,
#             "top_transactions": top_transactions,
#             "currency_rates": currency_rates,
#             "stock_prices": stock_prices
#         }
#
#         # Готовый json ответ для главной страницы сайта
#         main_page_json = json.dumps(main_page, ensure_ascii=False, indent=4)
#         print('\nJSON ответ для главной страницы:')
#         print(main_page_json)
#
#         with open(results_path + r'\main_page.json', 'w', encoding='UTF-8') as file_json:
#             file_json.write(main_page_json)
#             main_logger.info("файл main_page.json создан успешно")
#
#         # -------------------- Сервисы --------------------
#         # ----------- Поиск по телефонным номерам ---------
#
#         field_to_search = 'Описание'
#         regex_template = r'\d{3} \d{3}-\d{2}-\d{2}'
#         found_phones = search_phones(transaction_file, field_to_search, regex_template)
#
#         with open(results_path + r'\services.json', 'w', encoding='UTF-8') as file:
#             file.write(found_phones)
#             main_logger.info("файл services.json создан успешно")
#
#         print("\nВывожу список транзакций, в которых в описании имеется телефонный номер\n")
#         print(found_phones)
#
#         # -------------------- Отчеты --------------------
#         # -------------- Траты по категориям -------------
#
#         category_name = 'Супермаркеты'
#         months = 3
#         spent_by_categories = spending_by_category(transactions, months, category_name, current_date_str)
#         print("\nТраты по категориям:")
#         print(spent_by_categories)
#
#     except FileNotFoundError:
#         print(f"Ошибка чтения файла {transactions_path + transaction_file}")
#         main_logger.error(f"Ошибка чтения файла {transactions_path + transaction_file}")
#
#
# # Запуск программы, точка входа
# if __name__ == '__main__':
#     # Фиксируем определенную дату для передачи в функцию
#     current_date = "30.12.2021 11:27:01"
#
#     # источник данных
#     transaction_file = r'\operations.xlsx'
#
#     app_main(current_date, transaction_file)
import json
import logging
from datetime import datetime
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

from src.reports import spending_by_category
from src.services import search_phones
from src.utils import filter_by_dates, greeting, read_currencies_and_stocks_from_json
from src.views import cards_total_spent, get_currency_rates, get_stock_prices, get_top_transactions

BASE_DIR = Path(__file__).parent.parent
transactions_path = BASE_DIR / "data"
results_path = BASE_DIR / "results"
main_logs_path = BASE_DIR / "logs" / "main.log"

main_logger = logging.getLogger("main")
file_handler = logging.FileHandler(main_logs_path, "w", encoding="UTF-8")
file_formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
main_logger.addHandler(file_handler)
main_logger.setLevel(logging.INFO)

load_dotenv(BASE_DIR / ".env")


def app_main(current_date_str: str, transaction_file: str) -> None:
    file_path = transactions_path / transaction_file

    print(f"Проверяем существование: {file_path}")
    print(f"Файл существует: {file_path.exists()}")

    if not file_path.exists():
        print(f"Директория {file_path.parent} существует: {file_path.parent.exists()}")
        print(f"Содержимое директории {file_path.parent}:")
        for item in file_path.parent.iterdir():
            print(f"  {item.name}")
        main_logger.error(f"Файл не найден: {file_path}")
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    print("\nЧитаю excel файл с транзакциями, может занять некоторое время...")

    try:
        transactions = pd.read_excel(file_path)
       # transactions = pd.read_excel(file_path, engine='openpyxl')
        main_logger.info(f"Успешное чтение файла {file_path}")

        current_date = datetime.strptime(current_date_str, '%d.%m.%Y %H:%M:%S')
        start_date_main = current_date.replace(day=1, hour=0, minute=0, second=0)

        print("\nСтраница 'Главная'")
        print(f"Начало отчетного периода: {start_date_main}")
        print(f"Конец отчетного периода: {current_date}")

        filtered_by_dates = filter_by_dates(transactions, start_date_main, current_date)
        greeting_message = greeting(current_date)
        cards_total_expences = cards_total_spent(filtered_by_dates)
        top_transactions = get_top_transactions(filtered_by_dates)

        currencies, stocks = read_currencies_and_stocks_from_json()
        currency_rates = get_currency_rates(currencies)
        stock_prices = get_stock_prices(stocks)

        main_page = {
            "greeting": greeting_message,
            "cards": cards_total_expences,
            "top_transactions": top_transactions,
            "currency_rates": currency_rates,
            "stock_prices": stock_prices
        }

        main_page_json = json.dumps(main_page, ensure_ascii=False, indent=4)
        print('\nJSON ответ для главной страницы:')
        print(main_page_json)

        with open(results_path / "main_page.json", 'w', encoding='UTF-8') as file_json:
            file_json.write(main_page_json)
            main_logger.info("файл main_page.json создан успешно")

        field_to_search = 'Описание'
        regex_template = r'\d{3} \d{3}-\d{2}-\d{2}'
        found_phones = search_phones(str(file_path), field_to_search, regex_template)

        with open(results_path / "services.json", 'w', encoding='UTF-8') as file:
            file.write(found_phones)
            main_logger.info("файл services.json создан успешно")

        print("\nВывожу список транзакций, в которых в описании имеется телефонный номер\n")
        print(found_phones)

        category_name = 'Супермаркеты'
        months = 3
        spent_by_categories = spending_by_category(transactions, months, category_name, current_date_str)
        print("\nТраты по категориям:")
        print(spent_by_categories)

    except Exception as e:
        main_logger.error(f"Ошибка при обработке файла: {e}")
        raise


if __name__ == '__main__':
    current_date = "30.12.2021 11:27:01"
    transaction_file = "operations.xlsx"  # Убрали обратный слеш!
    app_main(current_date, transaction_file)
