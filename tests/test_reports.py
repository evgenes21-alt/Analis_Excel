
import pandas as pd
from pandas import DataFrame, Series
from src.reports import spending_by_category

def test_spending_by_category(
    source_dataframe: DataFrame

) -> None:
    """
    Тест на выборку из датафрейма, правильно подсчитывающий сумму расходов
    по заданной категории за заданный период.
    Тестируется сама оригинальная функция без декоратора (метод __wrapped__)
    """
    date_input = "18.11.2021 21:15:27"
    expected_reports = {"Категория": "Фастфуд", "Траты за 3 месяца:": "463.0 руб."}


    assert spending_by_category(source_dataframe, 3, "Фастфуд", date_input) == expected_reports

def test_log_to_file(
    filtered_by_dates_df: DataFrame
) -> None:
    """Тест декоратора на правильный вывод файла."""
    expected_reports = {"Категория": "Фастфуд", "Траты за 3 месяца:": "353.0 руб."}
    date_input = "18.11.2021 21:15:27"
    result = spending_by_category(filtered_by_dates_df, 3, "Фастфуд", date_input)

    assert result == expected_reports
