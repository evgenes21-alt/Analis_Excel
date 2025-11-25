
from pathlib import Path
from unittest.mock import MagicMock, patch
import pandas as pd
import pytest

# Импортируем тестируемую функцию
from src.services import search_phones


@pytest.fixture
def mock_dataframe() -> pd.DataFrame:
    """Тестовый DataFrame с полем 'Описание' и номерами телефонов."""
    return pd.DataFrame({
        "Описание": [
            "Звоните: 995 555-55-55",
            "Контакт: 981 333-44-55",
            "Нет номера",
            "Ещё один: 921 111-22-33"
        ]
    })

@patch("pathlib.Path.exists")
def test_search_phones_file_not_found(mock_exists: MagicMock) -> None:
    """Тест: файл не найден."""
    mock_exists.return_value = False

    with pytest.raises(FileNotFoundError) as exc_info:
        search_phones("data/nonexistent.xlsx", "Описание", r"\d{3} \d{3}-\d{2}-\d{2}")

    assert "Файл не найден" in str(exc_info.value)
