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

`тест автогенерации`
→ Ищи в `config.py`.

`GUI — основное окно: выбор модели, ввод, история, кнопки (выбрать, настройки, очистить, сохранить)`
→ Ищи в `gui.py`.

`Кнопка — выбор модели → browse_model`
→ Ищи в `gui.py`.

`Кнопка — открыть настройки → open_settings`
→ Ищи в `gui.py`.

`Кнопка — очистить историю диалога → clear_history`
→ Ищи в `gui.py`.

`Кнопка — сохранить сессию → save_session`
→ Ищи в `gui.py`.

`Кнопка — отправить сообщение → send_message`
→ Ищи в `gui.py`.

`Выбор модели → через filedialog, путь из DEFAULT_MODEL_DIR`
→ Ищи в `gui.py`.

`Отправка сообщения → send_message, вызывает generate_response`
→ Ищи в `gui.py`.

`Добавление сообщения в историю → add_message_to_history`
→ Ищи в `gui.py`.

`Очистка истории → clear_history, вызывает model_handler.clear_history()`
→ Ищи в `gui.py`.

`Сохранение сессии → save_session, использует filedialog и model_handler.save_session()`
→ Ищи в `gui.py`.

`Открытие окна настроек → open_settings, создаёт SettingsWindow`
→ Ищи в `gui.py`.

`Применение настроек → apply_settings, передаёт параметры в model_handler`
→ Ищи в `gui.py`.

`Окно настроек → SettingsWindow: temperature, max_tokens, top_p`
→ Ищи в `gui.py`.

`Применить настройки → on_apply, вызывает callback`
→ Ищи в `gui.py`.

`Обработчик кнопки 'Применить' → on_apply, собирает параметры и вызывает callback`
→ Ищи в `gui.py`.

`Конфигурация — импорт путей, параметров модели, генерации из config.py`
→ Ищи в `model_handler.py`.

`ModelHandler — основной класс: загрузка модели, генерация, история, сессии`
→ Ищи в `model_handler.py`.

`Загрузка модели — при инициализации ModelHandler`
→ Ищи в `model_handler.py`.

`Загрузка модели → load_model, проверяет путь, использует Llama из llama_cpp`
→ Ищи в `model_handler.py`.

`Добавление в историю → add_to_history, ограничение по MAX_HISTORY_LENGTH`
→ Ищи в `model_handler.py`.

`Генерация ответа → generate_response, в потоке, использует create_chat_completion`
→ Ищи в `model_handler.py`.

`Очистка истории → clear_history, вызывается из GUI`
→ Ищи в `model_handler.py`.

`Сохранение сессии → save_session, JSON, в папку session_logs`
→ Ищи в `model_handler.py`.

`Загрузка сессии → load_session, восстанавливает модель, параметры, историю`
→ Ищи в `model_handler.py`.

`Обновление параметров → update_parameters, вызывается из GUI при изменении настроек`
→ Ищи в `model_handler.py`.

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