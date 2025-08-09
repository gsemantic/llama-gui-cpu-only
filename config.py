# config.py
import os

# NAVIGATOR: Пути — DEFAULT_MODEL_DIR, DEFAULT_MODEL, MAX_HISTORY_LENGTH, N_THREADS, N_CTX
DEFAULT_MODEL_DIR = "/home/Alex/project/gguf/"
DEFAULT_MODEL = "Llama-3.2-3B-Instruct-Q2_K.gguf"
MAX_HISTORY_LENGTH = 10
N_THREADS = 2
N_CTX = 2048

# NAVIGATOR: Логирование — LOG_CONFIG: файл, размер, ротация, кодировка
LOG_CONFIG = {
    'log_file': 'error.log',
    'max_bytes': 2 * 1024 * 1024,  # 2 MB
    'backup_count': 3,
    'encoding': 'utf-8'
}

# NAVIGATOR: Параметры генерации — DEFAULT_GENERATION_PARAMS: temperature, max_tokens, top_p
DEFAULT_GENERATION_PARAMS = {
    'temperature': 0.7,
    'max_tokens': 512,
    'top_p': 0.9
}
