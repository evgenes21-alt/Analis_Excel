import json
from unittest.mock import patch

from src.services import search_phones


# TEST PASSED
@patch('src.services.pd.read_excel')
def test_search_phones(mocked_excel, source_dataframe, phones_found) -> None:
    mocked_excel.return_value = source_dataframe
    path_ = 'abc'
    description = 'Описание'
    pattern = r'\d{3} \d{3}-\d{2}-\d{2}'
    assert search_phones(path_, description, pattern) == json.dumps(phones_found, ensure_ascii=False, indent=4)