# gui.py
import os
import tkinter as tk
from tkinter import (
    ttk, filedialog, messagebox, StringVar, DoubleVar, IntVar, DISABLED, NORMAL
)
# ✅ Убираем точки: .model_handler → model_handler
from model_handler import ModelHandler
from config import DEFAULT_MODEL_DIR


# NAVIGATOR: GUI — основное окно: выбор модели, ввод, история, кнопки (выбрать, настройки, очистить, сохранить)
class LlamaGUI:
    """Графический интерфейс для Llama-модели"""
    
    def __init__(self, root, model_handler, logger):
        self.root = root
        self.model_handler = model_handler
        self.logger = logger
        
        self.root.title("Llama GUI")
        self.root.geometry("900x600")
        self.root.minsize(700, 500)
        
        # Переменные для интерфейса
        self.model_path_var = tk.StringVar(value=self.model_handler.model_path)
        self.status_var = tk.StringVar(value="Готов")
        
        # Создаём виджеты и компонуем
        self.create_widgets()
        self.setup_layout()

    def create_widgets(self):
        """Создание элементов интерфейса"""
        # --- Верхняя панель ---
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(top_frame, text="Модель:").pack(side=tk.LEFT)
        ttk.Entry(top_frame, textvariable=self.model_path_var, width=50, state="readonly").pack(side=tk.LEFT, padx=5)
        
        # NAVIGATOR: Кнопка — выбор модели → browse_model
        ttk.Button(top_frame, text="Выбрать", command=self.browse_model).pack(side=tk.LEFT, padx=2)
        
        # NAVIGATOR: Кнопка — открыть настройки → open_settings
        ttk.Button(top_frame, text="Настройки", command=self.open_settings).pack(side=tk.LEFT, padx=2)
        
        # NAVIGATOR: Кнопка — очистить историю диалога → clear_history
        ttk.Button(top_frame, text="Очистить", command=self.clear_history).pack(side=tk.LEFT, padx=2)
        
        # NAVIGATOR: Кнопка — сохранить сессию → save_session
        ttk.Button(top_frame, text="Сохранить", command=self.save_session).pack(side=tk.LEFT, padx=2)

        # --- Поле ввода ---
        input_frame = ttk.Frame(self.root)
        input_frame.pack(fill=tk.X, padx=10, pady=5)

        ttk.Label(input_frame, text="Вы:").pack(anchor=tk.W)
        self.input_text = tk.Text(input_frame, height=4, wrap=tk.WORD)
        self.input_text.pack(fill=tk.X, pady=2)
        
        # NAVIGATOR: Кнопка — отправить сообщение → send_message
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
        """Расположение элементов в интерфейсе"""
        # Уже реализовано через pack в create_widgets
        pass

    # NAVIGATOR: Выбор модели → через filedialog, путь из DEFAULT_MODEL_DIR
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

    # NAVIGATOR: Отправка сообщения → send_message, вызывает generate_response
    def send_message(self):
        """Отправка сообщения и генерация ответа"""
        user_input = self.input_text.get("1.0", tk.END).strip()
        if not user_input:
            return

        # Очистка поля ввода
        self.input_text.delete("1.0", tk.END)

        # Добавляем сообщение пользователя
        self.add_message_to_history("Пользователь", user_input)

        # Показываем, что идёт обработка
        self.status_var.set("Генерация ответа...")
        self.root.update()

        # Генерируем ответ
        def on_response(response):
            self.add_message_to_history("Ассистент", response)
            self.status_var.set("Готов")
            self.root.update()

        self.model_handler.generate_response(user_input, on_response)

    # NAVIGATOR: Добавление сообщения в историю → add_message_to_history
    def add_message_to_history(self, sender, message):
        """Добавление сообщения в текстовое поле истории"""
        self.history_text.config(state=tk.NORMAL)
        self.history_text.insert(tk.END, f"{sender}: {message}\n\n")
        self.history_text.config(state=tk.DISABLED)
        self.history_text.see(tk.END)

    # NAVIGATOR: Очистка истории → clear_history, вызывает model_handler.clear_history()
    def clear_history(self):
        """Очистка истории диалога"""
        if messagebox.askyesno("Подтверждение", "Очистить историю диалога?"):
            self.model_handler.clear_history()
            self.history_text.config(state=tk.NORMAL)
            self.history_text.delete("1.0", tk.END)
            self.history_text.config(state=tk.DISABLED)
            self.logger.info("История диалога очищена в GUI")

    # NAVIGATOR: Сохранение сессии → save_session, использует filedialog и model_handler.save_session()
    def save_session(self):
        """Сохранение текущей сессии"""
        filename = filedialog.asksaveasfilename(
            title="Сохранить сессию",
            initialdir="session_logs",
            initialfile=f"session_{tk.Tk().winfo_toplevel().winfo_name()}",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            defaultextension=".json"
        )
        if filename:
            self.model_handler.save_session(filename)
            messagebox.showinfo("Сохранение", "Сессия успешно сохранена!")

    # NAVIGATOR: Открытие окна настроек → open_settings, создаёт SettingsWindow
    def open_settings(self):
        """Открытие окна настроек"""
        SettingsWindow(self.root, self.model_handler, [], self.apply_settings)

    # NAVIGATOR: Применение настроек → apply_settings, передаёт параметры в model_handler
    def apply_settings(self, params):
        """Применение изменённых настроек"""
        self.model_handler.update_parameters(**params)
        self.logger.info(f"Настройки обновлены: {params}")


# NAVIGATOR: Окно настроек → SettingsWindow: temperature, max_tokens, top_p
class SettingsWindow:
    """Окно настроек приложения"""
    
    def __init__(self, parent, model_handler, model_list, apply_callback):
        self.window = tk.Toplevel(parent)
        self.window.title("Настройки")
        self.window.geometry("400x300")
        self.window.resizable(False, False)
        self.window.transient(parent)
        self.window.grab_set()

        self.model_handler = model_handler
        self.apply_callback = apply_callback

        # Переменные
        self.temperature_var = DoubleVar(value=self.model_handler.temperature)
        self.max_tokens_var = IntVar(value=self.model_handler.max_tokens)
        self.top_p_var = DoubleVar(value=self.model_handler.top_p)

        self.create_widgets()
        self.setup_layout()

    def create_widgets(self):
        """Создание элементов интерфейса настроек"""
        frame = ttk.Frame(self.window)
        frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Temperature
        ttk.Label(frame, text="Temperature:").grid(row=0, column=0, sticky=tk.W, pady=5)
        temp_scale = ttk.Scale(frame, from_=0.1, to=2.0, variable=self.temperature_var, orient=tk.HORIZONTAL)
        temp_scale.grid(row=0, column=1, sticky=tk.EW, pady=5)
        ttk.Label(frame, textvariable=self.temperature_var).grid(row=0, column=2, padx=5)

        # Max Tokens
        ttk.Label(frame, text="Max Tokens:").grid(row=1, column=0, sticky=tk.W, pady=5)
        max_scale = ttk.Scale(frame, from_=64, to=4096, variable=self.max_tokens_var, orient=tk.HORIZONTAL)
        max_scale.grid(row=1, column=1, sticky=tk.EW, pady=5)
        ttk.Label(frame, textvariable=self.max_tokens_var).grid(row=1, column=2, padx=5)

        # Top_p
        ttk.Label(frame, text="Top_p:").grid(row=2, column=0, sticky=tk.W, pady=5)
        top_p_scale = ttk.Scale(frame, from_=0.1, to=1.0, variable=self.top_p_var, orient=tk.HORIZONTAL)
        top_p_scale.grid(row=2, column=1, sticky=tk.EW, pady=5)
        ttk.Label(frame, textvariable=self.top_p_var).grid(row=2, column=2, padx=5)

        # Кнопки
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=3, column=0, columnspan=3, pady=20)

        # NAVIGATOR: Применить настройки → on_apply, вызывает callback
        ttk.Button(button_frame, text="Применить", command=self.on_apply).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Отмена", command=self.window.destroy).pack(side=tk.LEFT)

    def setup_layout(self):
        """Расположение элементов в окне настроек"""
        self.window.columnconfigure(1, weight=1)

    # NAVIGATOR: Обработчик кнопки 'Применить' → on_apply, собирает параметры и вызывает callback
    def on_apply(self):
        """Обработчик кнопки 'Применить'"""
        params = {
            "temperature": self.temperature_var.get(),
            "max_tokens": self.max_tokens_var.get(),
            "top_p": self.top_p_var.get()
        }
        self.apply_callback(params)
        self.window.destroy()


