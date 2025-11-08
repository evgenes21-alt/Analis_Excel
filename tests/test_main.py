import json
from unittest.mock import patch

from src.main import app_main
from tests.conftest import tests_path


# ТЕСТ PASSED
@patch('src.main.get_stock_prices')
@patch('src.main.get_currency_rates')
@patch('src.main.search_phones')
@patch('src.main.pd.read_excel')
def test_main(mocked_excel_read, mocked_search, mocked_currency, mocked_stocks, source_dataframe, phones_found,
              capsys) -> None:
    """ Тест на правильность вывода информации в консоль. """
    mocked_excel_read.return_value = source_dataframe
    mocked_search.return_value = json.dumps(phones_found, ensure_ascii=False, indent=4)
    mocked_currency.return_value = []
    mocked_stocks.return_value = []

    with open(tests_path + r'\output.txt', 'r', encoding='UTF-8') as file:
        output = file.read()
        app_main("08.10.2021 08:24:00", '')
        captured = capsys.readouterr()
        assert output == captured.out