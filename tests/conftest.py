import zipfile
from pathlib import Path

import pandas as pd
import pytest

tests_path = Path(__file__).parent


@pytest.fixture
def source_dataframe():
    df = pd.read_excel(tests_path / "test_operations.xlsx")
    df["Сумма операции"] = df["Сумма операции"].astype(float)
    df["MCC"] = df["MCC"].astype(float)
    # df = df.fillna(0)

    return df


@pytest.fixture
def filtered_by_dates_df():
    df = pd.read_excel(tests_path / "expected_filtered_by_dates.xlsx")
    df["MCC"] = df["MCC"].astype(float)
    df["Сумма операции"] = df["Сумма операции"].astype(float)
    df["Сумма платежа"] = df["Сумма платежа"].astype(float)
    df["Сумма операции с округлением"] = df["Сумма операции с округлением"].astype(float)
    df = df.fillna(0)

    return df


@pytest.fixture
def stocks_list():
    return ["AAPL", "AMZN"]


@pytest.fixture
def stocks_to_get():
    return [
        {"stock": "AAPL", "price": 150.12},
        {"stock": "AMZN", "price": 3173.18},
    ]


@pytest.fixture
def currencies_list():
    return ["USD", "EUR"]


@pytest.fixture
def currencies_to_get():
    return [{"currency": "USD", "rate": 73.21}, {"currency": "EUR", "rate": 87.08}]


@pytest.fixture
def top_5_expences():
    return [
        {"amount": 146.0, "category": "Супермаркеты", "date": "06.10.2021", "description": "Колхоз"},
        {"amount": 146.0, "category": "Супермаркеты", "date": "04.10.2021", "description": "Колхоз"},
        {"amount": 99.0, "category": "Фастфуд", "date": "04.10.2021", "description": "McDonald's"},
        {"amount": 99.0, "category": "Фастфуд", "date": "03.10.2021", "description": "McDonald's"},
        {"amount": 99.0, "category": "Фастфуд", "date": "03.10.2021", "description": "McDonald's"},
    ]


@pytest.fixture
def cards_spent():
    return [
        {"last_digits": "5684", "total_spent": 245.0, "cashback": 2.45},
        {"last_digits": "7197", "total_spent": 475.0, "cashback": 4.75},
    ]


@pytest.fixture
def phones_found():
    return [
        "995 555-55-55",
        "995 555-55-55",
        "981 333-44-55",
        "981 333-33-33",
        "921 333-33-33",
        "921 111-22-33",
        "981 666-66-66",
        "921 111-22-33",
        "981 888-88-88",
        "981 976-14-20",
        "981 976-14-20",
        "981 976-14-20",
        "921 111-22-33",
        "985 111-11-11",
        "921 999-99-99",
        "911 198-78-58",
        "981 555-55-55",
        "981 976-14-20",
        "966 000-00-00",
        "911 000-09-09",
        "911 882-65-08",
        "962 717-08-52",
        "962 717-08-52",
        "981 127-94-00",
        "911 695-42-03",
    ]


@pytest.fixture
def expected_fastfood():
    df = pd.read_excel(tests_path / "expected_fastfood.xlsx").agg({"Сумма операции": "sum"}).astype(float)
    return df


@pytest.fixture
def expected_supermarkets():
    df = pd.read_excel(tests_path / "expected_supermarkets.xlsx").agg({"Сумма операции": "sum"}).astype(float)
    return df


" В conftest.py добавьте проверку (временно)"
import os

print("Текущий каталог:", os.getcwd())
print("Файл существует:", os.path.exists(tests_path / "test_operations.xlsx"))
