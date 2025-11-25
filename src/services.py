# import json
# import logging
# import re
# from pathlib import Path
#
# import pandas as pd
#
# pd.set_option("future.no_silent_downcasting", True)
#
# BASE_DIR = str(Path(__file__).parent.parent)  # корневая папка проекта
# views_logs_path = BASE_DIR + r"\logs\services.log"
# transactions_path = BASE_DIR + "\\data"
#
# # настраиваем параметры логирования
# services_logger = logging.getLogger("services")
# file_handler = logging.FileHandler(views_logs_path, "w", encoding="UTF-8")
# file_formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s: %(message)s")
# file_handler.setFormatter(file_formatter)
# services_logger.addHandler(file_handler)
# services_logger.setLevel(logging.INFO)
#
#
# def search_phones(transactions_path: str | Path, field_name: str, pattern: str) -> str:
#     """
#     Ищет телефонные номера в указанном поле Excel-файла.
#
#     :param transactions_path: путь к Excel-файлу (str или Path)
#     :param field_name: название столбца для поиска
#     :param pattern: регулярное выражение для поиска номеров
#     :return: JSON-строка с найденными номерами
#     """
#     # Преобразуем в Path, если передано как строка
#     file_path = Path(transactions_path)
#
#     if not file_path.exists():
#         raise FileNotFoundError(f"Файл не найден: {file_path}")
#
#     # Читаем Excel-файл
#     df = pd.read_excel(file_path, engine="openpyxl")
#
#     # Проверяем, есть ли нужный столбец
#     if field_name not in df.columns:
#         raise ValueError(f"Столбец '{field_name}' не найден в файле")
#
#     found_numbers = []
#     for value in df[field_name].dropna():
#         matches = re.findall(pattern, str(value))
#         for match in matches:
#             found_numbers.append(match)
#
#     return json.dumps({"found_phones": found_numbers}, ensure_ascii=False, indent=2)

import json
import logging
import re
from pathlib import Path

import pandas as pd

# Настройка pandas (подавление предупреждений о downcasting)
pd.set_option("future.no_silent_downcasting", True)

# Определение базовых путей
BASE_DIR = Path(__file__).parent.parent  # корневая папка проекта
VIEWS_LOGS_PATH = BASE_DIR / "logs" / "services.log"
TRANSACTIONS_PATH = BASE_DIR / "data"

# Настройка логирования
services_logger = logging.getLogger("services")
services_logger.setLevel(logging.INFO)

# Убедимся, что обработчик не дублируется при повторном импорте
if not services_logger.handlers:
    file_handler = logging.FileHandler(VIEWS_LOGS_PATH, mode="w", encoding="UTF-8")
    file_formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s: %(message)s")
    file_handler.setFormatter(file_formatter)
    services_logger.addHandler(file_handler)


def search_phones(transactions_path: str | Path, field_name: str, pattern: str) -> str:
    """
    Ищет телефонные номера в указанном поле Excel-файла.

    :param transactions_path: путь к Excel-файлу (str или Path)
    :param field_name: название столбца для поиска
    :param pattern: регулярное выражение для поиска номеров (например, r'\\d{3} \\d{3}-\\d{2}-\\d{2}')
    :return: JSON-строка с найденными номерами в формате {"found_phones": [...]}
    :raises FileNotFoundError: если файл не найден
    :raises ValueError: если указанный столбец отсутствует в файле
    """
    file_path = Path(transactions_path)

    # Проверка существования файла
    if not file_path.exists():
        services_logger.error("Файл не найден: %s", file_path)
        raise FileNotFoundError(f"Файл не найден: {file_path}")

    # Чтение Excel-файла
    try:
        df = pd.read_excel(file_path, engine="openpyxl")
    except Exception as e:
        services_logger.error("Ошибка при чтении Excel-файла %s: %s", file_path, e)
        raise

    # Проверка наличия столбца
    if field_name not in df.columns:
        services_logger.error("Столбец '%s' не найден в файле %s", field_name, file_path)
        raise ValueError(f"Столбец '{field_name}' не найден в файле")

    # Поиск номеров по шаблону
    found_numbers = []
    for value in df[field_name].dropna():
        matches = re.findall(pattern, str(value))
        found_numbers.extend(matches)

    # Логирование результата
    services_logger.info("Найдено номеров: %d", len(found_numbers))

    return json.dumps({"found_phones": found_numbers}, ensure_ascii=False, indent=2)
