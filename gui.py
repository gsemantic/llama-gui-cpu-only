# gui.py
import os
import tkinter as tk
from tkinter import (
    ttk, filedialog, messagebox, StringVar, DoubleVar, IntVar
)
from model_handler import ModelHandler
from config import DEFAULT_MODEL_DIR
import tkinter.font as tkfont
import matplotlib.font_manager as fm


class LlamaGUI:
    """Графический интерфейс для Llama-модели"""
    def __init__(self, root, model_handler, logger):
        self.root = root
        self.model_handler = model_handler
        self.logger = logger
        self.root.title("Llama GUI")
        self.root.geometry("900x600")
        self.root.minsize(700, 500)

        # Текущий шрифт
        self.current_font = StringVar(value=self.model_handler.params.get('font', "Arial"))

        # Переменные для интерфейса
        self.model_path_var = tk.StringVar(value=self.model_handler.model_path)
        self.status_var = tk.StringVar(value="Готов")

        # Создаём виджеты и компонуем
        self.create_widgets()
        self.setup_layout()
        self.apply_font()

    def create_widgets(self):
        """Создание элементов интерфейса"""
        # --- Верхняя панель ---
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(top_frame, text="Модель:").pack(side=tk.LEFT)
        ttk.Entry(top_frame, textvariable=self.model_path_var, width=50, state="readonly").pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Выбрать", command=self.browse_model).pack(side=tk.LEFT, padx=2)
        ttk.Button(top_frame, text="Настройки", command=self.open_settings).pack(side=tk.LEFT, padx=2)
        ttk.Button(top_frame, text="Очистить", command=self.clear_history).pack(side=tk.LEFT, padx=2)
        ttk.Button(top_frame, text="Сохранить", command=self.save_session).pack(side=tk.LEFT, padx=2)

        # --- Поле ввода ---
        input_frame = ttk.Frame(self.root)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(input_frame, text="Вы:").pack(anchor=tk.W)
        self.input_text = tk.Text(input_frame, height=4, wrap=tk.WORD)
        self.input_text.pack(fill=tk.X, pady=2)
        ttk.Button(input_frame, text="Отправить", command=self.send_message).pack(anchor=tk.E, pady=2)

        # --- История диалога ---
        history_frame = ttk.LabelFrame(self.root, text="Диалог")
        history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.history_text = tk.Text(history_frame, wrap=tk.WORD, state=tk.DISABLED, height=15)
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_text.yview)
        self.history_text.configure(yscrollcommand=scrollbar.set)
        self.history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # --- Статусная строка ---
        status_bar = ttk.Frame(self.root)
        status_bar.pack(fill=tk.X, padx=10, pady=(0, 10))
        ttk.Label(status_bar, text="Статус:").pack(side=tk.LEFT)
        ttk.Label(status_bar, textvariable=self.status_var, foreground="blue").pack(side=tk.LEFT, padx=5)

    def setup_layout(self):
        pass

    def apply_font(self):
        """Применяет выбранный шрифт ко всем текстовым виджетам"""
        font_name = self.current_font.get()
        try:
            font = tkfont.Font(family=font_name, size=10)
            self.input_text.configure(font=font)
            self.history_text.configure(font=font)
        except tk.TclError:
            self.logger.warning(f"Шрифт '{font_name}' не найден. Используется стандартный.")
            default_font = tkfont.Font(family="Arial", size=10)
            self.input_text.configure(font=default_font)
            self.history_text.configure(font=default_font)

    def browse_model(self):
        """Выбор файла модели"""
        path = filedialog.askopenfilename(
            title="Выберите файл модели",
            initialdir=DEFAULT_MODEL_DIR,
            filetypes=[("Model files", "*.gguf *.bin"), ("All files", "*.*")]
        )
        if path:
            self.model_path_var.set(path)
            self.logger.info(f"Выбрана модель: {path}")

    def send_message(self):
        """Отправка сообщения и генерация ответа"""
        user_input = self.input_text.get("1.0", tk.END).strip()
        if not user_input:
            return
        self.input_text.delete("1.0", tk.END)
        self.add_message_to_history("Пользователь", user_input)
        self.status_var.set("Генерация ответа...")
        self.root.update()

        def on_response(response):
            self.add_message_to_history("Ассистент", response)
            self.status_var.set("Готов")
            self.root.update()

        self.model_handler.generate_response(user_input, on_response)

    def add_message_to_history(self, sender, message):
        """Добавление сообщения в текстовое поле истории"""
        self.history_text.config(state=tk.NORMAL)
        self.history_text.insert(tk.END, f"{sender}: {message}\n")
        self.history_text.config(state=tk.DISABLED)
        self.history_text.see(tk.END)

    def clear_history(self):
        """Очистка истории диалога"""
        if messagebox.askyesno("Подтверждение", "Очистить историю диалога?"):
            self.model_handler.clear_history()
            self.history_text.config(state=tk.NORMAL)
            self.history_text.delete("1.0", tk.END)
            self.history_text.config(state=tk.DISABLED)
            self.logger.info("История диалога очищена в GUI")

    def save_session(self):
        """Сохранение текущей сессии"""
        filename = filedialog.asksaveasfilename(
            title="Сохранить сессию",
            initialdir="session_logs",
            initialfile=f"session_{self.root.winfo_name()}",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            defaultextension=".json"
        )
        if filename:
            self.model_handler.save_session(filename)
            messagebox.showinfo("Сохранение", "Сессия успешно сохранена!")

    def open_settings(self):
        """Открытие окна настроек"""
        SettingsWindow(self.root, self.model_handler, self.current_font.get(), self.apply_settings_and_font)

    def apply_settings_and_font(self, params, font_name):
        """Применение настроек и шрифта"""
        self.model_handler.update_parameters(**params)
        self.current_font.set(font_name)
        self.apply_font()
        self.logger.info(f"Настройки и шрифт обновлены: {params}, шрифт: {font_name}")


class SettingsWindow:
    """Окно настроек приложения"""
    def __init__(self, parent, model_handler, current_font, apply_callback):
        self.window = tk.Toplevel(parent)
        self.window.title("Настройки")
        self.window.geometry("600x650")
        self.window.resizable(True, True)
        self.window.transient(parent)
        self.window.grab_set()

        self.model_handler = model_handler
        self.apply_callback = apply_callback
        self.current_font = current_font

        # Получаем системные шрифты
        try:
            font_names = sorted(set(f.name for f in fm.fontManager.ttflist))
        except:
            font_names = ["Arial", "DejaVu Sans", "Liberation Sans", "Times New Roman", "Courier New"]
        self.font_var = StringVar(value=current_font)
        self.font_list = font_names

        # Подсказки
        self.tooltips = {
            'temperature': "Случайность ответа. Высокое значение — креативность, низкое — предсказуемость.",
            'max_tokens': "Максимальное количество токенов в ответе.",
            'top_p': "Вероятностный порог для выбора следующего токена (ядерная выборка).",
            'top_k': "Ограничивает выбор следующего токена до K наиболее вероятных.",
            'min_p': "Минимальная вероятность для включения токена (по отношению к лучшему).",
            'typical_p': "Фильтр, основанный на типичности вероятностей.",
            'frequency_penalty': "Штраф за повторение токенов (выше = меньше повторов).",
            'presence_penalty': "Штраф за появление уже использованных токенов.",
            'repeat_penalty': "Штраф за повторение (влияет на все токены).",
            'tfs_z': "Tail Free Sampling: фильтр, удаляющий хвосты распределения.",
            'mirostat_mode': "0=выкл, 1=Mirostat, 2=Mirostat 2.0 — саморегулируемая температура.",
            'mirostat_tau': "Целевое значение перплексии для Mirostat (обычно 5–10).",
            'mirostat_eta': "Скорость обучения Mirostat (обычно 0.1–0.3).",
            'seed': "Значение для воспроизводимости. -1 = случайное.",
            'num_ctx': "Размер контекстного окна (сколько токенов помнит модель).",
            'num_batch': "Размер батча при обработке запроса.",
            'num_keep': "Сколько первых токенов контекста сохранять при переполнении.",
            'num_predict': "Макс. токенов для генерации. -1 = до конца.",
            'penalize_nl': "Применять штраф к символам новой строки.",
            'cache_prompt': "Кэшировать промпт для ускорения последующих запросов.",
            'use_mmap': "Использовать отображение в память (экономит RAM).",
            'use_mlock': "Заблокировать модель в RAM (не выгружать в своп).",
            'grammar': "BNF-грамматика для структурированного вывода.",
            'logit_bias': "Словарь: {токен: смещение} для принудительного выбора.",
            'stop': "Строки, при появлении которых генерация останавливается.",
            'response_format': "Формат ответа (например, { 'type': 'json_object' }).",
            'echo': "Повторять входной промпт в ответе.",
            'include_bos_token': "Включать начальный токен (BOS).",
            'craft_assistant': "Режим ассистента (экспериментально).",
            'stream': "Потоковая генерация (постепенный вывод).",
        }

        # Все параметры
        self.params = {}
        for key, default in model_handler.params.items():
            if isinstance(default, bool):
                self.params[key] = IntVar(value=int(default))
            elif isinstance(default, int):
                self.params[key] = IntVar(value=default)
            elif isinstance(default, float):
                self.params[key] = DoubleVar(value=default)
            else:
                self.params[key] = StringVar(value=str(default) if default is not None else "")

        self.entries = {}
        self.create_widgets()
        self.setup_layout()

    def create_widgets(self):
        """Создание элементов интерфейса настроек"""
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        canvas = tk.Canvas(main_frame)
        scroll_frame = ttk.Frame(canvas)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

        def on_frame_configure(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        scroll_frame.bind("<Configure>", on_frame_configure)

        # --- Шрифт ---
        ttk.Label(scroll_frame, text="🔤 Шрифт", font=("Helvetica", 10, "bold")).grid(
            row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))

        ttk.Label(scroll_frame, text="Шрифт:").grid(row=1, column=0, sticky=tk.W, pady=2)
        font_combo = ttk.Combobox(scroll_frame, textvariable=self.font_var, values=self.font_list, width=30)
        font_combo.grid(row=1, column=1, sticky=tk.EW, padx=(5, 0), pady=2)
        font_combo.bind("<<ComboboxSelected>>", lambda e: self.preview_font())

        # Пример
        self.preview_label = ttk.Label(scroll_frame, text="Пример текста", font=("Arial", 10))
        self.preview_label.grid(row=2, column=1, sticky=tk.W, pady=2)

        row = 3

        # --- Основные ---
        ttk.Label(scroll_frame, text="🔧 Основные", font=("Helvetica", 10, "bold")).grid(
            row=row, column=0, columnspan=3, sticky=tk.W, pady=(15, 10))
        row += 1

        for key in ['temperature', 'max_tokens', 'top_p']:
            ttk.Label(scroll_frame, text=f"{key}:").grid(row=row, column=0, sticky=tk.W, pady=2)
            entry = ttk.Entry(scroll_frame, textvariable=self.params[key], width=40)
            entry.grid(row=row, column=1, sticky=tk.EW, padx=(5, 0), pady=2)
            self.entries[key] = entry
            self._add_tooltip(scroll_frame, row, key)
            row += 1

        # --- Дополнительные ---
        ttk.Label(scroll_frame, text="⚙️ Дополнительные", font=("Helvetica", 10, "bold")).grid(
            row=row, column=0, columnspan=3, sticky=tk.W, pady=(15, 10))
        row += 1

        for key in sorted(self.params.keys()):
            if key in ['temperature', 'max_tokens', 'top_p']:
                continue
            ttk.Label(scroll_frame, text=f"{key}:").grid(row=row, column=0, sticky=tk.W, pady=2)
            entry = ttk.Entry(scroll_frame, textvariable=self.params[key], width=40)
            entry.grid(row=row, column=1, sticky=tk.EW, padx=(5, 0), pady=2)
            self.entries[key] = entry
            self._add_tooltip(scroll_frame, row, key)
            row += 1

        # --- Кнопки ---
        button_frame = ttk.Frame(scroll_frame)
        button_frame.grid(row=row, column=0, columnspan=3, pady=20)
        ttk.Button(button_frame, text="Применить", command=self.on_apply).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Отмена", command=self.window.destroy).pack(side=tk.LEFT)

        scroll_frame.columnconfigure(1, weight=1)

    def _add_tooltip(self, parent, row, key):
        label = ttk.Label(parent, text="?", foreground="blue", cursor="hand2", font=("Arial", 8, "bold"))
        label.grid(row=row, column=2, padx=2)
        label.bind("<Enter>", lambda e, msg=self.tooltips.get(key, ""): self.show_tooltip(e.widget, msg))
        label.bind("<Leave>", lambda e: self.hide_tooltip())

    def show_tooltip(self, widget, text):
        x, y, _, _ = widget.bbox("insert")
        x += widget.winfo_rootx() + 25
        y += widget.winfo_rooty() + 25
        self.tooltip = tk.Toplevel(widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = ttk.Label(self.tooltip, text=text, background="lightyellow", relief="solid", borderwidth=1, wraplength=300)
        label.pack()

    def hide_tooltip(self):
        if hasattr(self, 'tooltip'):
            self.tooltip.destroy()

    def preview_font(self):
        font_name = self.font_var.get()
        try:
            self.preview_label.configure(font=(font_name, 10))
        except:
            pass

    def setup_layout(self):
        pass

    def on_apply(self):
        """Обработчик кнопки 'Применить'"""
        params = {}
        for key, var in self.params.items():
            try:
                if isinstance(var, StringVar):
                    value = var.get().strip()
                    if key == 'stop' and value:
                        value = [s.strip() for s in value.split(",") if s.strip()]
                    elif key in ['logit_bias', 'response_format'] and value:
                        try:
                            value = eval(value)
                        except:
                            value = {}
                    params[key] = value
                elif isinstance(var, IntVar):
                    val = var.get()
                    if key in ['penalize_nl', 'cache_prompt', 'use_mmap', 'use_mlock', 'echo', 'include_bos_token', 'craft_assistant', 'stream']:
                        params[key] = bool(val)
                    else:
                        params[key] = val
                else:
                    params[key] = var.get()
            except Exception:
                params[key] = self.model_handler.params.get(key)

        # Сохраняем шрифт
        params['font'] = self.font_var.get()

        self.apply_callback(params, self.font_var.get())
        self.window.destroy()
