from datetime import datetime
from unittest.mock import mock_open, patch

import pandas as pd
import pytest

from src.utils import filter_by_dates, greeting, read_currencies_and_stocks_from_json


# ТЕСТ PASSED
@pytest.mark.parametrize(
    "date_, greet",
    [
        (datetime(2021, 12, 30, 19, 27, 7), "Добрый вечер"),
        (datetime(2021, 12, 30, 11, 27, 4), "Доброе утро"),
        (datetime(2021, 12, 30, 15, 27, 2), "Добрый день"),
        (datetime(2021, 12, 30, 3, 27, 1), "Доброй ночи"),
    ],
)
def test_greeting(date_: datetime, greet: str) -> None:
    """Тест проверяет корректность возвращаемого приветствия."""
    assert greeting(date_) == greet


from pandas import DataFrame

def test_filter_by_dates(
    source_dataframe: DataFrame,
    filtered_by_dates_df: DataFrame
) -> None:
    """Тест проверяет правильность выборки по диапазону дат."""
    start_date = datetime(2021, 10, 1, 0, 0, 0)
    current_date = datetime(2021, 10, 8, 8, 24, 0)
    expected = filtered_by_dates_df.to_dict(orient="records")
    assert filter_by_dates(source_dataframe, start_date, current_date) == expected

from unittest.mock import MagicMock

@patch(
    "builtins.open",
    new_callable=mock_open,
    read_data='{"currencies": ["USD", "EUR"], "stocks": ["AAPL", "AMZN", "GOOG", "MSFT", "TSLA"]}',
)
def test_read_currencies_and_stocks_from_json(mocked: MagicMock) -> None:
    """Тест на правильность возвращения кортежа из списка валют и акций."""
    assert read_currencies_and_stocks_from_json() == (["USD", "EUR"], ["AAPL", "AMZN", "GOOG", "MSFT", "TSLA"])


@patch("builtins.open", new_callable=mock_open, read_data="{}")
def test_read_currencies_and_stocks_from_json_empty(mocked: MagicMock) -> None:
    """Тест на пустой файл json."""
    assert read_currencies_and_stocks_from_json() == (None, None)
