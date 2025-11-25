import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Any, List

import pandas as pd
import requests

pd.options.mode.chained_assignment = None

BASE_DIR = Path(__file__).parent.parent  # корневая папка проекта

utils_logs_path = BASE_DIR / "logs/utils.log"  # raw string

# настраиваем параметры логирования
utils_logger = logging.getLogger("utils")
file_handler = logging.FileHandler(utils_logs_path, "w", encoding="UTF-8")
file_formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
utils_logger.addHandler(file_handler)
utils_logger.setLevel(logging.INFO)

results_path = BASE_DIR / "results"

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


def get_cards_and_expences_only(dict_: dict) -> tuple[list[Any], pd.DataFrame]:
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
            if float(trans["Сумма операции"]) < 0:
                if not trans["Номер карты"] in cards:
                    cards.append(trans["Номер карты"])
                expences_only.append(trans)
        except Exception:
            continue

    # Собираем список из уникальных номеров карт
    cards = sorted(cards)

    # датафрейм только по платежам, очищенный от отсутствующих номеров карт
    expences = pd.DataFrame(expences_only)

    return cards, expences


def filter_by_dates(transactions: pd.DataFrame, start_date: datetime, current_date: datetime) -> List:
    """
    Функция создает словарь от поступившего датафрейма
    и выделяет диапазон в пределах от start_date и current_date.
    Берутся только успешные транзакции (со статусом ОК).
    """
    # преобразовываем поле даты в формат даты pandas
    transactions["Дата операции"] = pd.to_datetime(transactions["Дата операции"], dayfirst=True)

    # фильтруем по диапазону дат
    filtered_by_dates_df = transactions[(transactions["Дата операции"].between(start_date, current_date))]

    # берем только успешные транзакции
    filtered_by_dates_OK = filtered_by_dates_df[filtered_by_dates_df["Статус"] == "OK"]

    # исключаем Nan поля в столбце "Номер карты"
    filtered_by_dates_OK_noNANs = filtered_by_dates_OK.dropna(subset=["Номер карты"])

    # возвращаем поле даты обратно в строковый формат (далее нам понадобится именно строковое представление)
    filtered_by_dates_OK_noNANs["Дата операции"] = filtered_by_dates_OK_noNANs["Дата операции"].dt.strftime(
        "%d.%m.%Y %H:%M:%S"
    )

    # очищаем весь датафрейм от полей Nan, записываем туда нули. Иначе с тестами возникнут сложности
    filtered_by_dates_OK_noNANs = filtered_by_dates_OK_noNANs.fillna(0)

    # возвращаем датафрейм, преобразованный в список
    return filtered_by_dates_OK_noNANs.to_dict(orient="records")


def read_currencies_and_stocks_from_json() -> tuple:
    file_path = BASE_DIR / "user_settings.json"

    try:
        with open(file_path, "r", encoding="utf-8") as u_sets:
            data = json.load(u_sets)
        print(data)
        return data.get("currencies"), data.get("stocks")
    except FileNotFoundError:
        print(f"Ошибка: файл {file_path} не найден.")
        print("Создайте файл user_settings.json в корне проекта с содержимым:")
        print('{"currencies": ["USD", "EUR"], "stocks": ["AAPL", "MSFT"]}')
        raise
    except json.JSONDecodeError as e:
        print(f"Ошибка в формате JSON: {e}")
        raise


def cards_total_spent(dict_: dict) -> list[dict]:
    """
    Функция получает отфильтрованный словарь по датам
    и возвращает список из словарей для всех карт, общую сумму расходов по каждой карте
    за заданный период, а также сумму кэшбека
    """

    #  уникальные номера карт и датафрейм только по платежам, очищенный от отсутствующих номеров карт
    cards, expences = get_cards_and_expences_only(dict_)
    # print(get_cards_and_expences_only(dict_))

    # собираем список транзакций, отдельно по каждой карте
    cards_df = []
    for card_ in cards:
        cards_df.append(expences.loc[expences["Номер карты"] == card_])

    total_expences = []
    for card in cards_df:
        total_expences.append(card.agg({"Сумма операции": "sum"}).to_dict())

    cards_expences = []
    for card_number, expence in zip(cards, total_expences):
        exp_sum = round(abs(expence["Сумма операции"]), 2)
        cashback = round(abs(expence["Сумма операции"]) / 100, 2)
        cards_expences.append({"last_digits": card_number[-4:], "total_spent": exp_sum, "cashback": cashback})

    with open(results_path / "json_out.json", "w", encoding="utf-8") as test_file:
        json.dump(cards_expences, test_file, indent=4)
        utils_logger.info("файл json_out.json создан успешно")

    return cards_expences


def get_top_transactions(dict_: dict) -> list[dict]:
    """
    Функция возвращает список словарей из 5 транзакций, по которым самая большая сумма платежей.
    """
    expences = get_cards_and_expences_only(dict_)[1]
    sorted_by_amount = expences.sort_values(by="Сумма операции", ascending=True)
    top_5_expences = sorted_by_amount.iloc[:5]
    top_5_list = []
    for index, transaction in top_5_expences.iterrows():
        tr_date = transaction["Дата операции"][:10]
        tr_amount = abs(transaction["Сумма операции"])
        tr_category = transaction["Категория"]
        tr_descr = transaction["Описание"]
        top_5_list.append({"date": tr_date, "amount": tr_amount, "category": tr_category, "description": tr_descr})

    with open(results_path / "top_5_json.json", "w", encoding="UTF-8") as test_file:
        json.dump(top_5_list, test_file, ensure_ascii=False, indent=4)
        utils_logger.info("файл top_5_json.json создан успешно")

    return top_5_list


def get_currency_rates(curr_list: list[str]) -> list[dict]:
    """
    Функция получает список валют и возвращает их текущий курс.
    """
    API_KEY = os.getenv("API_KEY")
    response_list = []
    convert_to = "RUB"
    amount = 1
    for currency in curr_list:
        url = "https://api.apilayer.com/exchangerates_data/convert"
        response = requests.get(f"{url}?to={convert_to}&from={currency}&amount={amount}&apikey={API_KEY}")
        if response.status_code == 200:
            # запрос успешный, можно распарсить ответ
            response_list.append({"currency": currency, "rate": round(response.json()["info"]["rate"], 2)})
        else:
            print("\nЧто-то пошло не так с запросом на конвертацию валюты.")
            utils_logger.error("Что-то пошло не так с запросом на конвертацию валюты.")
            response_list.append({"currency": currency, "rate": "N/A"})

    return response_list


def get_stock_prices(stock_list: list[str]) -> list[dict]:
    """
    Функция получает список акций и возвращает их стоимость.
    Используется API: http://api.marketstack.com/v1/eod?access_key={API_KEY_STOCK}&symbols={stock}.
    Ответ возвращается в формате JSON.
    В качестве стоимости акции берется ее стоимость на момент закрытия предыдущего дня (параметр 'close').
    Чтобы получить актуальную цену акции на момент запроса, необходимо иметь платную подписку.
    К сожалению, такой возможности нет. Надеюсь на понимание.
    """
    API_KEY_STOCK = os.getenv("API_KEY_STOCK")

    stocks_price = []
    for stock in stock_list:
        url = f"http://api.marketstack.com/v1/eod?access_key={API_KEY_STOCK}&symbols={stock}"
        response = requests.get(url)
        if response.status_code == 200:
            stocks_price.append({"stock": stock, "price": response.json()["data"][0]["close"]})
        else:
            print("\nЧто-то пошло не так с запросом на получение цен акций.")
            return []

    return stocks_price