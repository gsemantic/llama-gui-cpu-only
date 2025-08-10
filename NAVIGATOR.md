# 🧭 Навигатор проекта: Llama GUI

## 📂 Структура проекта
`main.py` — 📌 Точка входа. Запускает логирование, модель и GUI.
`model_handler.py` — 🔧 Логика модели: загрузка, генерация, история, сессии.
`gui.py` — 🎨 Графический интерфейс: окно, кнопки, настройки, сохранение.
`config.py` — ⚙️ Все настройки: пути, параметры модели, логирование.
`__init__.py` — 📦 Пустой файл (помечает директорию как пакет Python).
`requirements.txt` — 📦 Список зависимостей (llama-cpp-python и др.).
`session_logs/` — 📁 Папка для сохранённых сессий и логов.
`error.log` — 📄 Основной файл логов (настраивается в config.py).

## 🔍 Как находить ошибки по сообщению
Если в ошибке или логе есть:

`Пути — DEFAULT_MODEL_DIR, DEFAULT_MODEL, MAX_HISTORY_LENGTH, N_THREADS, N_CTX`
→ Ищи в `config.py`.

`Логирование — LOG_CONFIG: файл, размер, ротация, кодировка`
→ Ищи в `config.py`.

`Параметры генерации — DEFAULT_GENERATION_PARAMS: temperature, max_tokens, top_p`
→ Ищи в `config.py`.

`Импорты — config (логирование), model_handler, gui`
→ Ищи в `main.py`.

`Настройка логирования → setup_logging, использует RotatingFileHandler и console`
→ Ищи в `main.py`.

`Точка входа — main(), создаёт логгер, model_handler и GUI, запускает mainloop`
→ Ищи в `main.py`.

`Создание ModelHandler → передаётся в GUI`
→ Ищи в `main.py`.

`Создание GUI → LlamaGUI(root, model_handler, logger)`
→ Ищи в `main.py`.

`Запуск GUI — root.mainloop()`
→ Ищи в `main.py`.

`Запуск приложения — python main.py`
→ Ищи в `main.py`.