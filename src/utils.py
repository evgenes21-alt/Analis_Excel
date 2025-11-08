import json
import logging
from datetime import datetime
from json import JSONDecodeError
from pathlib import Path
from typing import Any

import pandas as pd

pd.options.mode.chained_assignment = None

BASE_DIR = str(Path(__file__).parent.parent)  # корневая папка проекта

utils_logs_path = BASE_DIR + r'\logs\utils.log'

# настраиваем параметры логирования
utils_logger = logging.getLogger("utils")
file_handler = logging.FileHandler(utils_logs_path, "w", encoding="UTF-8")
file_formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
utils_logger.addHandler(file_handler)
utils_logger.setLevel(logging.INFO)


def greeting(date_: datetime) -> str:
    """
    Функция принимает текущую дату со временем и возвращает приветствие
    в зависимости от времени суток.
    """
    hour = date_.hour
    message = "Доброе утро"
    if 12 <= hour < 18:
        message = "Добрый день"
    elif 18 <= hour <= 23:
        message = "Добрый вечер"
    elif 0 <= hour < 6:
        message = "Доброй ночи"

    return message


def get_cards_and_expences_only(dict_) -> tuple[list[Any], pd.DataFrame]:
    """
    Функция возвращает кортеж, состоящий из списка уникальных номеров карт
    и датафрейма, состоящий только из платежей (суммы транзакций отрицательные),
    и очищенный от отсутствующих номеров карт.
    """
    # собираем только те строки, в которых есть номера карт и сумма транзакции отрицательна,
    # что означает, что берем только платежи (расходы)
    cards = []
    expences_only = []
    for trans in dict_:
        try:
            if float(trans['Сумма операции']) < 0:
                if not trans['Номер карты'] in cards:
                    cards.append(trans['Номер карты'])
                expences_only.append(trans)
        except Exception:
            continue

    # Собираем список из уникальных номеров карт
    cards = sorted(cards)

    # датафрейм только по платежам, очищенный от отсутствующих номеров карт
    expences = pd.DataFrame(expences_only)

    return cards, expences


def filter_by_dates(transactions: pd.DataFrame, start_date: datetime, current_date: datetime) -> list[dict]:
    """
    Функция создает словарь от поступившего датафрейма
    и выделяет диапазон в пределах от start_date и current_date.
    Берутся только успешные транзакции (со статусом ОК).
    """
    # преобразовываем поле даты в формат даты pandas
    transactions['Дата операции'] = pd.to_datetime(transactions['Дата операции'], dayfirst=True)

    # фильтруем по диапазону дат
    filtered_by_dates_df = transactions[(transactions['Дата операции'].between(start_date, current_date))]

    # берем только успешные транзакции
    filtered_by_dates_OK = filtered_by_dates_df[filtered_by_dates_df['Статус'] == 'OK']

    # исключаем Nan поля в столбце "Номер карты"
    filtered_by_dates_OK_noNANs = filtered_by_dates_OK.dropna(subset=['Номер карты'])

    # возвращаем поле даты обратно в строковый формат (далее нам понадобится именно строковое представление)
    filtered_by_dates_OK_noNANs['Дата операции'] = filtered_by_dates_OK_noNANs['Дата операции'].dt.strftime(
        '%d.%m.%Y %H:%M:%S')

    # очищаем весь датафрейм от полей Nan, записываем туда нули. Иначе с тестами возникнут сложности
    filtered_by_dates_OK_noNANs = filtered_by_dates_OK_noNANs.fillna(0)

    # возвращаем датафрейм, преобразованный в список
    return filtered_by_dates_OK_noNANs.to_dict(orient="records")


def read_currencies_and_stocks_from_json() -> tuple[list[str], list[str]]:
    """
    Функция считывает список валют и акций, по которым требуется
    запросить цены и текущий курс.
    Возвращает два списка, отдельно по валютам и акциям.
    """

    currencies = []
    stocks = []

    try:
        with open(BASE_DIR + r'\user_settings.json') as u_sets:
            sets = json.load(u_sets)
            currencies = sets.get('user_currencies', 0)
            stocks = sets.get('user_stocks', 0)
            utils_logger.info("Чтение файла user_settings.json успешно")

    except JSONDecodeError:
        print("Ошибка чтения файла json")
        utils_logger.error("Ошибка чтения файла json")

    return currencies, stocks