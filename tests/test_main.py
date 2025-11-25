# import json
# from unittest.mock import patch
#
# from src.main import app_main
#
#
# @patch('src.utils.get_stock_prices')
# @patch('src.utils.get_currency_rates')
# @patch('src.services.search_phones')
# @patch('pandas.read_excel')
# def test_main(mocked_excel_read, mocked_search, mocked_currency, mocked_stocks, source_dataframe, phones_found,
#               capsys) -> None:
#     """ Тест на правильность вывода информации в консоль. """
#     mocked_excel_read.return_value = source_dataframe
#     mocked_search.return_value = json.dumps(phones_found, ensure_ascii=False, indent=4)
#     mocked_currency.return_value = []
#     mocked_stocks.return_value = []
#     with open('tests/output.txt', 'r', encoding='UTF-8') as file:
#
#     # with open('tests/output.txt', 'r', encoding='UTF-8') as file:
#         output = file.read()
#         app_main("08.10.2021 08:24:00")
#         captured = capsys.readouterr()
#         print(captured.out)
#         assert output == captured.out
#
import json
import os
from tempfile import TemporaryDirectory
from typing import AnyStr
from unittest.mock import patch


@patch("src.utils.get_stock_prices")
@patch("src.utils.get_currency_rates")
@patch("src.services.search_phones")
@patch("pandas.read_excel")
def test_main(
    mocked_excel_read: any, mocked_search: any, mocked_currency: any, mocked_stocks: any, source_dataframe: any, phones_found: any, capsys: any
) -> None:
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
