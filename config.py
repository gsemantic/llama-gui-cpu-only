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
    # Основные
    'temperature': 0.7,
    'max_tokens': 512,
    'top_p': 0.9,

    # Выборка
    'top_k': 40,
    'min_p': 0.05,
    'typical_p': 1.0,
    'frequency_penalty': 0.0,
    'presence_penalty': 0.0,
    'repeat_penalty': 1.1,
    'tfs_z': 1.0,
    'mirostat_mode': 0,
    'mirostat_tau': 5.0,
    'mirostat_eta': 0.1,

    # Управление контекстом
    'seed': -1,
    'num_ctx': 2048,
    'num_batch': 512,
    'num_keep': 0,
    'num_predict': -1,

    # Флаги
    'penalize_nl': False,
    'cache_prompt': True,
    'use_mmap': True,
    'use_mlock': False,
    'echo': False,
    'include_bos_token': True,
    'craft_assistant': False,
    'stream': True,

    # Остановка
    'stop': [],
    'grammar': '',
    'logit_bias': None,
    'response_format': None,
}

# Новый параметр: шрифт
DEFAULT_FONT = "Arial"  # Можно заменить на "DejaVu Sans", "Liberation Sans" и т.д.
