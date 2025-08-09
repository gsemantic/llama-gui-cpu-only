import sys
import logging
import tkinter as tk
from logging.handlers import RotatingFileHandler

# Абсолютные импорты (без точки)
from config import LOG_CONFIG
from model_handler import ModelHandler
from gui import LlamaGUI


def setup_logging():
    """Настройка системы логирования"""
    logger = logging.getLogger("llama_gui")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler = RotatingFileHandler(
        filename=LOG_CONFIG['log_file'],
        maxBytes=LOG_CONFIG['max_bytes'],
        backupCount=LOG_CONFIG['backup_count'],
        encoding=LOG_CONFIG['encoding']
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.INFO)
    logger.addHandler(console_handler)

    return logger


def main():
    logger = setup_logging()
    logger.info("=" * 50)
    logger.info("Запуск Llama GUI")
    logger.info(f"Python версия: {sys.version}")

    # Создание обработчика модели
    model_handler = ModelHandler(logger)

    # Создание GUI
    root = tk.Tk()
    app = LlamaGUI(root, model_handler, logger)

    # Запуск основного цикла
    root.mainloop()
    logger.info("Работа приложения завершена")


if __name__ == "__main__":
    main()
