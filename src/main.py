
import logging
from pathlib import Path

from dotenv import load_dotenv

from src.views import app_main

BASE_DIR = Path(__file__).parent.parent
main_logs_path = BASE_DIR / "logs" / "main.log"

main_logger = logging.getLogger("main")
file_handler = logging.FileHandler(main_logs_path, "w", encoding="UTF-8")
file_formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s: %(message)s")
file_handler.setFormatter(file_formatter)
main_logger.addHandler(file_handler)
main_logger.setLevel(logging.INFO)

load_dotenv(BASE_DIR / ".env")
results_path = BASE_DIR / "results"


def main():
    app_main(current_date)


if __name__ == "__main__":
    current_date = "30.12.2021 11:27:01"
    main()