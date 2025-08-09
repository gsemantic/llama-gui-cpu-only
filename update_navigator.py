# update_navigator.py
"""
Автоматически обновляет NAVIGATOR.md на основе комментариев # NAVIGATOR: в коде
"""

import os

# Шаблон начала файла
NAVIGATOR_HEADER = """# 🧭 Навигатор проекта: Llama GUI

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
"""

def extract_navigator_lines():
    """Извлекает строки с # NAVIGATOR: из ключевых файлов"""
    lines = []
    files_to_scan = ["config.py", "gui.py", "model_handler.py", "main.py"]
    
    for filename in files_to_scan:
        if not os.path.exists(filename):
            print(f"⚠️  Файл не найден: {filename}")
            continue
            
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                if "# NAVIGATOR:" in line:
                    # Извлекаем текст после метки
                    try:
                        text = line.split("# NAVIGATOR:", 1)[1].strip()
                        lines.append(f"`{text}`\n→ Ищи в `{filename}`.")
                    except:
                        continue
    return "\n\n".join(lines)

def main():
    try:
        content = NAVIGATOR_HEADER.strip() + "\n\n"
        content += extract_navigator_lines()
        
        with open("NAVIGATOR.md", "w", encoding="utf-8") as f:
            f.write(content)
        
        print("✅ NAVIGATOR.md успешно обновлён!")
        print("➡️  Теперь можно выполнить: git add NAVIGATOR.md && git commit -m 'docs: обновлён навигатор'")
        
    except Exception as e:
        print(f"❌ Ошибка при обновлении: {e}")

if __name__ == "__main__":
    main()
