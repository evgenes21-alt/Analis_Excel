import json
import logging
import os
from pathlib import Path

import requests

from src.utils import get_cards_and_expences_only

BASE_DIR = str(Path(__file__).parent.parent)  # корневая папка проекта
views_logs_path = BASE_DIR + r'\logs\views.log'
results_path = BASE_DIR + '\\results'

# настраиваем параметры логирования
views_logger = logging.getLogger("views")
file_handler = logging.FileHandler(views_logs_path, "w", encoding="UTF-8")
file_formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
views_logger.addHandler(file_handler)
views_logger.setLevel(logging.INFO)


def cards_total_spent(dict_: list) -> list[dict]:
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

    # собираем общую сумму расходов по каждой карте
    total_expences = []
    for card in cards_df:
        total_expences.append(card.agg({'Сумма операции': 'sum'}).to_dict())

    # формируем список словарей, где ключами являются номер карты, общая сумма расходов, кэшбэк
    cards_expences = []
    for card_number, expence in zip(cards, total_expences):
        exp_sum = round(abs(expence['Сумма операции']), 2)
        cashback = round(abs(expence['Сумма операции']) / 100, 2)
        cards_expences.append({'last_digits': card_number[-4:], 'total_spent': exp_sum,
                               'cashback': cashback})

    # Временный тестовый блок для проверки правильности работы функции.
    # Выводит результат работы функции в отдельный json файл в папке logs текущего проекта
    with open(results_path + r'\json_out.json', 'w', encoding='utf-8') as test_file:
        json.dump(cards_expences, test_file, indent=4)
        views_logger.info("файл json_out.json создан успешно")

    return cards_expences


def get_top_transactions(dict_: list) -> list[dict]:
    """
    Функция возвращает список словарей из 5 транзакций, по которым самая большая сумма платежей.
    """
    # нам нужен только второй элемент [1] возвращенного кортежа (только датафрейм)
    expences = get_cards_and_expences_only(dict_)[1]

    # сортируем стоимости транзакций в порядке убывания
    sorted_by_amount = expences.sort_values(by='Сумма операции', ascending=True)

    # выводим в файл для проверки правильности сортировки (опционально)
    # sorted_by_amount.to_excel(results_path + r'\sorted_by_amount.xlsx')

    # выбираем первые 5 транзакций после сортировки по убыванию
    top_5_expences = sorted_by_amount.iloc[:5]

    # выводим в файл для проверки правильности выборки (опционально)
    # top_5_expences.to_excel(results_path + r'\top_5_expences.xlsx')

    # организуем список из топ 5 транзакций с дополнительными требуемыми полями
    top_5_list = []
    for index, transaction in top_5_expences.iterrows():
        tr_date = transaction['Дата операции'][:10]  # берем только дату, время не требуется по тз
        tr_amount = abs(transaction['Сумма операции'])  # по модулю числа
        tr_category = transaction['Категория']
        tr_descr = transaction['Описание']
        top_5_list.append(
            {
                "date": tr_date,
                "amount": tr_amount,
                "category": tr_category,
                "description": tr_descr
            }
        )

    with open(results_path + r'\top_5_json.json', 'w', encoding='UTF-8') as test_file:
        json.dump(top_5_list, test_file, ensure_ascii=False, indent=4)
        views_logger.info("файл top_5_json.json создан успешно")

    return top_5_list


def get_currency_rates(curr_list: list[str]) -> list[dict]:
    """
    Функция получает список валют и возвращает их текущий курс.
    """
    API_KEY = os.getenv("API_KEY")
    response_list = []
    convert_to = 'RUB'
    amount = 1
    for currency in curr_list:
        url = 'https://api.apilayer.com/exchangerates_data/convert'
        response = requests.get(
            f'{url}?to={convert_to}&from={currency}&amount={amount}&apikey={API_KEY}')
        if response.status_code == 200:
            # запрос успешный, можно распарсить ответ
            response_list.append(
                {
                    "currency": currency,
                    "rate": round(response.json()['info']['rate'], 2)
                })
        else:
            print("\nЧто-то пошло не так с запросом на конвертацию валюты.")
            views_logger.error("Что-то пошло не так с запросом на конвертацию валюты.")
            response_list.append(
                {
                    "currency": currency,
                    "rate": "N/A"
                })

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

    # тут будем собирать цены на акции
    stocks_price = []
    for stock in stock_list:
        url = f'http://api.marketstack.com/v1/eod?access_key={API_KEY_STOCK}&symbols={stock}'
        response = requests.get(url)
        if response.status_code == 200:
            # запрос успешный, можно распарсить ответ
            stocks_price.append(
                {
                    "stock": stock,
                    "price": response.json()['data'][0]['close']
                })
        else:
            print('\nЧто-то пошло не так с запросом на получение цен акций.')
            return []

    return stocks_price