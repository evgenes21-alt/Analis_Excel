import json
import logging
from datetime import datetime, timedelta
from functools import wraps
from pathlib import Path
from typing import Callable

import pandas as pd
from pandas import Series

from src.utils import filter_by_dates

BASE_DIR = str(Path(__file__).parent.parent)  # корневая папка проекта
results_path = BASE_DIR + "\\results\\"

reports_logs_path = BASE_DIR + r"\logs\reports.log"

# настраиваем параметры логирования
reports_logger = logging.getLogger("reports")
file_handler = logging.FileHandler(reports_logs_path, "w", encoding="UTF-8")
file_formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
reports_logger.addHandler(file_handler)
reports_logger.setLevel(logging.INFO)


def log_to_file(filename: str = "report_expences_by_category.json") -> Callable:
    """
    Декоратор, осуществляющий запись в файл результат работы функции
    По умолчанию имя файла 'reports.txt', однако пользователь может задать
    любое имя по своему желанию.
    """

    def wrapper(func) -> Callable:
        @wraps(func)
        def inner(*args, **kwargs) -> dict:
            # В args[2] поступает название категории
            result = {"Категория": args[2]}
            try:
                result["Траты за 3 месяца:"] = (
                    str(round(abs(func(*args, **kwargs).to_dict()["Сумма операции"]), 2)) + " руб."
                )
            except Exception as err:
                reports_logger.info("Что-то пошло не так при работе функции, ошибка: ", err)
                return {}
            try:
                with open(results_path + filename, "w", encoding="utf-8") as file:
                    file.write(json.dumps(result, ensure_ascii=False, indent=4))
                    reports_logger.info(f"Отчет успешно записан в файл {results_path + filename}")
            except FileNotFoundError as err:
                reports_logger.info("Что-то пошло не так, ошибка: ", err)
            return result

        return inner

    return wrapper


@log_to_file("category_expences.json")
def spending_by_category(transactions: pd.DataFrame, months: int, category: str, date_: str) -> Series:
    """
    Функция принимает данные транзакций, категорию и исходную дату.
    Возвращается датафрейм, содержащий траты по заданной категории
    за последние три месяца от переданной даты.
    """
    current_date = datetime.strptime(date_, "%d.%m.%Y %H:%M:%S")
    back_date = current_date - timedelta(days=months * 30)

    # фильтруем датасет по датам
    filtered_by_dates = filter_by_dates(transactions, back_date, current_date)
    df = pd.DataFrame(filtered_by_dates)

    # выбираем только заданные категории
    filtered_by_category = df.loc[(df["Категория"] == category) & (df["Статус"] == "OK")]

    # находим общую сумму платежей по этой категории
    expences_sum = filtered_by_category.agg({"Сумма операции": "sum"})
    filtered_by_category.to_excel(results_path + r"\categories_3_months.xlsx")
    reports_logger.info("Запись файла categories_3_months.xlsx успешна.")

    return expences_sum
