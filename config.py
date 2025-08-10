# config.py
import os

# --- Пути ---
DEFAULT_MODEL_DIR = "/home/Alex/project/gguf/"
DEFAULT_MODEL = "Llama-3.2-3B-Instruct-Q2_K.gguf"
MAX_HISTORY_LENGTH = 10
N_THREADS = 2
N_CTX = 2048

# --- Логирование ---
LOG_CONFIG = {
    'log_file': 'error.log',
    'max_bytes': 2 * 1024 * 1024,  # 2 MB
    'backup_count': 3,
    'encoding': 'utf-8'
}

# --- Профили ---
PROFILES_DIR = "profiles"
os.makedirs(PROFILES_DIR, exist_ok=True)

# --- Системный промт ---
DEFAULT_SYSTEM_PROMPT = "Ты — полезный и вежливый ассистент."

# --- Параметры генерации ---
DEFAULT_GENERATION_PARAMS = {
    # Основные
    'temperature': 0.7,
    'max_tokens': 512,
    'top_p': 0.9,
<<<<<<< HEAD

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
=======
    'frequency_penalty': 0.0,
    'presence_penalty': 0.0,
    'repeat_penalty': 1.1,

    # Дополнительные
    'top_k': 40,
    'min_p': 0.05,
    'typical_p': 1.0,
    'tfs_z': 1.0,
    'mirostat': 0,
    'mirostat_lr': 0.1,
    'mirostat_tau': 5.0,
    'seed': -1,
    'n_ctx': 2048,
    'n_batch': 512,
    'n_predict': -1,
    'n_keep': 0,
    'n_discard': 0,
    'ignore_eos': False,
    'stream': True,
    'logit_bias': None,
    'grammar': '',
    'penalize_nl': True,
}

# --- Описание параметров (для подсказок и валидации) ---
PARAM_INFO = {
    'temperature': {
        'label': 'Temperature',
        'description': 'Контролирует случайность: чем выше, тем более случайный вывод (0.1–1.2 — консервативно, >1.5 — креативно)',
        'type': float,
        'min': 0.0,
        'max': 2.0,
        'default': 0.7
    },
    'max_tokens': {
        'label': 'Max Tokens',
        'description': 'Максимальное количество токенов в ответе',
        'type': int,
        'min': 64,
        'max': 8192,
        'default': 512
    },
    'top_p': {
        'label': 'Top P',
        'description': 'Сэмплирование по вероятности: модель выбирает из наименьшего набора токенов с совокупной вероятностью P',
        'type': float,
        'min': 0.0,
        'max': 1.0,
        'default': 0.9
    },
    'frequency_penalty': {
        'label': 'Frequency Penalty',
        'description': 'Штраф за повторение токенов (положительные значения уменьшают повторы)',
        'type': float,
        'min': -2.0,
        'max': 2.0,
        'default': 0.0
    },
    'presence_penalty': {
        'label': 'Presence Penalty',
        'description': 'Штраф за появление новых токенов (побуждает модель говорить о новом)',
        'type': float,
        'min': -2.0,
        'max': 2.0,
        'default': 0.0
    },
    'repeat_penalty': {
        'label': 'Repeat Penalty',
        'description': 'Штраф за повторение последовательностей (1.0 = нет штрафа, >1.0 = штраф)',
        'type': float,
        'min': 0.0,
        'max': 2.0,
        'default': 1.1
    },
    'top_k': {
        'label': 'Top K',
        'description': 'Ограничивает выбор следующего токена до K наиболее вероятных',
        'type': int,
        'min': 0,
        'max': 100,
        'default': 40
    },
    'min_p': {
        'label': 'Min P',
        'description': 'Минимальная вероятность для включения токена в выборку (0.05 = 5%)',
        'type': float,
        'min': 0.0,
        'max': 1.0,
        'default': 0.05
    },
    'typical_p': {
        'label': 'Typical P',
        'description': 'Альтернатива top_p, основана на типичности распределения',
        'type': float,
        'min': 0.0,
        'max': 1.0,
        'default': 1.0
    },
    'tfs_z': {
        'label': 'TFS Z',
        'description': 'Tail Free Sampling: фильтрация "хвостов" распределения',
        'type': float,
        'min': 0.0,
        'max': 10.0,
        'default': 1.0
    },
    'mirostat': {
        'label': 'Mirostat',
        'description': 'Алгоритм регулирования перплексии (0 = выкл, 1 = Mirostat, 2 = Mirostat 2.0)',
        'type': int,
        'min': 0,
        'max': 2,
        'default': 0
    },
    'mirostat_lr': {
        'label': 'Mirostat LR',
        'description': 'Скорость обучения Mirostat (чувствительность к перплексии)',
        'type': float,
        'min': 0.01,
        'max': 1.0,
        'default': 0.1
    },
    'mirostat_tau': {
        'label': 'Mirostat Tau',
        'description': 'Целевая перплексия для Mirostat (обычно 5–10)',
        'type': float,
        'min': 0.0,
        'max': 20.0,
        'default': 5.0
    },
    'seed': {
        'label': 'Seed',
        'description': 'Значение для воспроизводимости (–1 = случайный)',
        'type': int,
        'min': -1,
        'max': 2**31,
        'default': -1
    },
    'n_ctx': {
        'label': 'Context Size',
        'description': 'Размер контекстного окна (в токенах)',
        'type': int,
        'min': 512,
        'max': 32768,
        'default': 2048
    },
    'n_batch': {
        'label': 'Batch Size',
        'description': 'Количество токенов, обрабатываемых за раз',
        'type': int,
        'min': 1,
        'max': 2048,
        'default': 512
    },
    'n_predict': {
        'label': 'Predict Tokens',
        'description': 'Максимальное количество токенов для генерации (обычно совпадает с max_tokens)',
        'type': int,
        'min': -1,
        'max': 8192,
        'default': -1
    },
    'n_keep': {
        'label': 'Keep Tokens',
        'description': 'Сколько токенов из начала контекста сохранять (0 = автоматически)',
        'type': int,
        'min': 0,
        'max': 1000,
        'default': 0
    },
    'n_discard': {
        'label': 'Discard Tokens',
        'description': 'Сколько токенов отбрасывать при нехватке памяти (экспериментально)',
        'type': int,
        'min': 0,
        'max': 1000,
        'default': 0
    },
    'ignore_eos': {
        'label': 'Ignore EOS',
        'description': 'Игнорировать конец строки (продолжать генерацию после \n)',
        'type': bool,
        'default': False
    },
    'stream': {
        'label': 'Stream Output',
        'description': 'Потоковая генерация (рекомендуется)',
        'type': bool,
        'default': True
    },
    'logit_bias': {
        'label': 'Logit Bias',
        'description': 'Словарь: {token_id: bias}, например, {123: 1.5}',
        'type': 'dict',
        'default': None
    },
    'grammar': {
        'label': 'Grammar',
        'description': 'BNF-грамматика для структурированной генерации (экспериментально)',
        'type': str,
        'default': ''
    },
    'penalize_nl': {
        'label': 'Penalize Newline',
        'description': 'Штрафовать символ новой строки при генерации',
        'type': bool,
        'default': True
    },
    'system_prompt': {
    'label': 'System Prompt',
    'description': 'Системное сообщение, определяющее поведение модели',
    'type': str,
    'default': "Ты — полезный и вежливый ассистент."
}
}
>>>>>>> 70b1b38 (feat(gui): добавлены профили, системный промт, улучшено копирование и шрифт)
