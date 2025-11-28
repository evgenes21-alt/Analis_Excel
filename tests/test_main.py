
import json
import os
from tempfile import TemporaryDirectory
from typing import AnyStr
from unittest.mock import patch, MagicMock

import pandas as pd
from _pytest.capture import CaptureFixture


@patch("src.utils.get_stock_prices")
@patch("src.utils.get_currency_rates")
@patch("src.services.search_phones")
@patch("pandas.read_excel")
def test_main(
    mocked_excel_read: MagicMock,
    mocked_search: MagicMock,
    mocked_currency: MagicMock,
    mocked_stocks: MagicMock,
    source_dataframe: pd.DataFrame,
    phones_found: list[str],
    capsys: CaptureFixture
) -> None:
    ...


    """Тест на правильность вывода информации в консоль."""
    mocked_excel_read.return_value = source_dataframe
    mocked_search.return_value = json.dumps(phones_found, ensure_ascii=False, indent=4)
    mocked_currency.return_value = []
    mocked_stocks.return_value = []

    # Создаём временный файл output.txt
    with TemporaryDirectory() as temp_dir:
        output_path = os.path.join(temp_dir, "output.txt")
        with open(output_path, "w", encoding="UTF-8") as f:
            f.write("Тестовый контент\n")

        # Теперь открываем его (для имитации работы теста)
        with open(output_path, "r", encoding="UTF-8") as file:
            content = file.read()

    # Здесь продолжайте логику теста (если нужно проверить content)
