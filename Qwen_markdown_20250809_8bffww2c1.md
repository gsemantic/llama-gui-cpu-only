# 🧭 Навигатор проекта: Llama GUI

## 📂 Структура проекта
- `main.py` — 📌 Точка входа. Запускает логирование, модель и GUI.
- `model_handler.py` — 🔧 Логика модели: загрузка, генерация, история, сессии.
- `gui.py` — 🎨 Графический интерфейс: окно, кнопки, настройки, сохранение.
- `config.py` — ⚙️ Все настройки: пути, параметры модели, логирование.
- `__init__.py` — 📦 Пустой файл (помечает директорию как пакет Python).
- `requirements.txt` — 📦 Список зависимостей (llama-cpp-python и др.).
- `session_logs/` — 📁 Папка для сохранённых сессий и логов.
- `error.log` — 📄 Основной файл логов (настраивается в config.py).

## 🔍 Как находить ошибки по сообщению

Если в ошибке или логе есть:

- **`ImportError`, `cannot import`**  
  → Проверь импорты в любом файле. Возможна ошибка в пути или имени модуля.

- **`FileNotFoundError`, `модель не найдена`**  
  → Проблема в `model_handler.py` или `config.py`. Проверь путь к модели.

- **`llama_cpp`, `Llama`, `create_chat_completion`**  
  → Ошибка в `model_handler.py`. Модель не загружена или `llama-cpp-python` не установлен.

- **`generate_response`, `ответ`, `температура`**  
  → Логика генерации в `model_handler.py`. Проверь параметры и обработку.

- **`кнопка`, `настройки`, `сохранить`, `GUI`**  
  → Ищи в `gui.py`. Проблема с виджетами или обработчиками событий.

- **`логирование`, `error.log`, `INFO`, `DEBUG`**  
  → Настройки в `main.py` или `config.py`. Проверь `LOG_CONFIG`.

- **`session_logs`, `save_session`, `JSON`**  
  → Сохранение/загрузка сессий в `model_handler.py`.

- **`temperature`, `max_tokens`, `top_p`**  
  → Параметры в `config.py` или в `SettingsWindow` (в `gui.py`).

## 🧩 Примеры диагностики

### ❌ `FileNotFoundError: .../gguf/Llama-3.2-3B-Instruct-Q2_K.gguf`
→ Проверь `DEFAULT_MODEL_DIR` и `DEFAULT_MODEL` в `config.py`. Убедись, что файл существует.

### ❌ `ImportError: cannot import name 'Llama' from 'llama_cpp'`
→ Выполни: `pip install llama-cpp-python`. Если не помогло — переустанови с `--no-cache-dir`.

### ❌ `KeyError: 'temperature'`
→ В `config.py` в `DEFAULT_GENERATION_PARAMS` нет ключа `'temperature'`. Добавь его.

## 📦 Полезные команды
```bash
# Установка зависимости
pip install llama-cpp-python

# Запуск приложения
cd ~/project/llama_gui_project
python3 main.py

# Проверка наличия модели
ls -l /home/Alex/project/gguf/Llama-3.2-3B-Instruct-Q2_K.gguf

# Просмотр логов
tail -f error.log