import json
import logging
import re
from pathlib import Path

import pandas as pd

pd.set_option('future.no_silent_downcasting', True)

BASE_DIR = str(Path(__file__).parent.parent)  # корневая папка проекта
views_logs_path = BASE_DIR + r'\logs\services.log'
transactions_path = BASE_DIR + '\\data'

# настраиваем параметры логирования
services_logger = logging.getLogger("services")
file_handler = logging.FileHandler(views_logs_path, "w", encoding="UTF-8")
file_formatter = logging.Formatter('%(asctime)s-%(name)s-%(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
services_logger.addHandler(file_handler)
services_logger.setLevel(logging.INFO)


def search_phones(transactions: str, field_to_search: str, regex: str) -> str:
    """
    Функция получает данные с транзакциями и возвращает датафрейм,
    в котором в поле, заданном параметром 'field_to_search' имеются записи
    с телефонными номерами, заданным в шаблоне 'regex'.
    """
    phones_json = ''
    try:
        trans = pd.read_excel(transactions_path + transactions)
        pattern = re.compile(regex)
        phones = trans[trans[field_to_search].str.contains(pattern)].fillna(0)

        # переводим датафрейм с найденными номерами телефонов
        # сначала в словарь, а затем в формат json
        phones_json = json.dumps(phones.to_dict(orient='records'), ensure_ascii=False, indent=4)
        services_logger.info("Успешная выборка, возвращен json с найденными номерами телефонов")
    except FileNotFoundError:
        services_logger.error("Ошибка открытия файла, возвращен пустой список")

    return phones_json