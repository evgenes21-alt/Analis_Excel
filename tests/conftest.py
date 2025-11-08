from pathlib import Path

import pandas as pd
import pytest

tests_path = str(Path(__file__).parent)


@pytest.fixture
def source_dataframe():
    df = pd.read_excel(tests_path + r'\test_operations.xlsx')
    df['Сумма операции'] = df['Сумма операции'].astype(float)
    df['MCC'] = df['MCC'].astype(float)
    # df = df.fillna(0)

    return df


@pytest.fixture
def filtered_by_dates_df():
    df = pd.read_excel(tests_path + r'\expected_filtered_by_dates.xlsx')
    df['MCC'] = df['MCC'].astype(float)
    df['Сумма операции'] = df['Сумма операции'].astype(float)
    df['Сумма платежа'] = df['Сумма платежа'].astype(float)
    df['Сумма операции с округлением'] = df['Сумма операции с округлением'].astype(float)
    df = df.fillna(0)

    return df


@pytest.fixture
def stocks_list():
    return ["AAPL", "AMZN"]


@pytest.fixture
def stocks_to_get():
    return [
        {
            "stock": "AAPL",
            "price": 150.12
        },
        {
            "stock": "AMZN",
            "price": 3173.18
        },
    ]


@pytest.fixture
def currencies_list():
    return ["USD", "EUR"]


@pytest.fixture
def currencies_to_get():
    return [
        {
            "currency": "USD",
            "rate": 73.21
        },
        {
            "currency": "EUR",
            "rate": 87.08
        }
    ]


@pytest.fixture
def top_5_expences():
    return [
        {'amount': 146.0,
         'category': 'Супермаркеты',
         'date': '06.10.2021',
         'description': 'Колхоз'},
        {'amount': 146.0,
         'category': 'Супермаркеты',
         'date': '04.10.2021',
         'description': 'Колхоз'},
        {'amount': 99.0,
         'category': 'Фастфуд',
         'date': '04.10.2021',
         'description': "McDonald's"},
        {'amount': 99.0,
         'category': 'Фастфуд',
         'date': '03.10.2021',
         'description': "McDonald's"},
        {'amount': 99.0,
         'category': 'Фастфуд',
         'date': '03.10.2021',
         'description': "McDonald's"}
    ]


@pytest.fixture
def cards_spent():
    return [
        {
            "last_digits": "5684",
            "total_spent": 245.0,
            "cashback": 2.45
        },
        {
            "last_digits": "7197",
            "total_spent": 475.0,
            "cashback": 4.75
        },
    ]


@pytest.fixture
def phones_found():
    return [{'Дата операции': '18.11.2021 21:15:27', 'Дата платежа': '19.11.2021', 'Номер карты': 0, 'Статус': 'OK',
             'Сумма операции': -200.0, 'Валюта операции': 'RUB', 'Сумма платежа': -200.0, 'Валюта платежа': 'RUB',
             'Кэшбэк': 0.0, 'Категория': 'Мобильная связь', 'MCC': 0.0, 'Описание': 'Тинькофф Мобайл +7 995 555-55-55',
             'Бонусы (включая кэшбэк)': 2, 'Округление на инвесткопилку': 0, 'Сумма операции с округлением': 200.0},
            {'Дата операции': '29.09.2021 09:22:42', 'Дата платежа': '29.09.2021', 'Номер карты': 0, 'Статус': 'OK',
             'Сумма операции': -400.0, 'Валюта операции': 'RUB', 'Сумма платежа': -400.0, 'Валюта платежа': 'RUB',
             'Кэшбэк': 0.0, 'Категория': 'Мобильная связь', 'MCC': 0.0, 'Описание': 'Я МТС +7 921 111-22-33',
             'Бонусы (включая кэшбэк)': 4, 'Округление на инвесткопилку': 0, 'Сумма операции с округлением': 400.0},
            {'Дата операции': '07.10.2021 12:00:06', 'Дата платежа': '07.03.2021', 'Номер карты': 0,
             'Статус': 'OK', 'Сумма операции': -50.0, 'Валюта операции': 'RUB', 'Сумма платежа': -50.0,
             'Валюта платежа': 'RUB', 'Кэшбэк': 0.0, 'Категория': 'Мобильная связь', 'MCC': 0.0,
             'Описание': 'МТС Mobile +7 981 333-33-33', 'Бонусы (включая кэшбэк)': 0, 'Округление на инвесткопилку': 0,
             'Сумма операции с округлением': 50.0}]


@pytest.fixture
def expected_fastfood():
    df = pd.read_excel(tests_path + r'\expected_fastfood.xlsx').agg({'Сумма операции': 'sum'}).astype(float)
    return df


@pytest.fixture
def expected_supermarkets():
    df = pd.read_excel(tests_path + r'\expected_supermarkets.xlsx').agg({'Сумма операции': 'sum'}).astype(float)
    return df