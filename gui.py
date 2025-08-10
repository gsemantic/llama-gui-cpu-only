# gui.py
import os
import json
import tkinter as tk
from tkinter import (
<<<<<<< HEAD
    ttk, filedialog, messagebox, StringVar, DoubleVar, IntVar
)
from model_handler import ModelHandler
from config import DEFAULT_MODEL_DIR
import tkinter.font as tkfont
import matplotlib.font_manager as fm
=======
    ttk, filedialog, messagebox, simpledialog
)
import tkinter.font as tkfont
from model_handler import ModelHandler
import config  # Для PARAM_INFO, PROFILES_DIR, DEFAULT_SYSTEM_PROMPT
>>>>>>> 70b1b38 (feat(gui): добавлены профили, системный промт, улучшено копирование и шрифт)


class LlamaGUI:
    """Графический интерфейс для Llama-модели"""
    def __init__(self, root, model_handler, logger):
        self.root = root
        self.model_handler = model_handler
        self.logger = logger
        self.root.title("Llama GUI")
        self.root.geometry("900x600")
        self.root.minsize(700, 500)

<<<<<<< HEAD
        # Текущий шрифт
        self.current_font = StringVar(value=self.model_handler.params.get('font', "Arial"))

        # Переменные для интерфейса
        self.model_path_var = tk.StringVar(value=self.model_handler.model_path)
        self.status_var = tk.StringVar(value="Готов")

        # Создаём виджеты и компонуем
=======
        self.model_path_var = tk.StringVar(value=self.model_handler.model_path)
        self.status_var = tk.StringVar(value="Готов")

>>>>>>> 70b1b38 (feat(gui): добавлены профили, системный промт, улучшено копирование и шрифт)
        self.create_widgets()
        self.setup_layout()
        self.apply_font()

    def create_widgets(self):
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(top_frame, text="Модель:").pack(side=tk.LEFT)
        ttk.Entry(top_frame, textvariable=self.model_path_var, width=50, state="readonly").pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Выбрать", command=self.browse_model).pack(side=tk.LEFT, padx=2)
        ttk.Button(top_frame, text="Настройки", command=self.open_settings).pack(side=tk.LEFT, padx=2)
        ttk.Button(top_frame, text="Очистить", command=self.clear_history).pack(side=tk.LEFT, padx=2)
        ttk.Button(top_frame, text="Сохранить", command=self.save_session).pack(side=tk.LEFT, padx=2)

        input_frame = ttk.Frame(self.root)
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(input_frame, text="Вы:").pack(anchor=tk.W)
        self.input_text = tk.Text(
            input_frame, height=4, wrap=tk.WORD,
            font=("TkFixedFont", 12)
        )
        self.input_text.pack(fill=tk.X, pady=2)
        ttk.Button(input_frame, text="Отправить", command=self.send_message).pack(anchor=tk.E, pady=2)

        history_frame = ttk.LabelFrame(self.root, text="Диалог")
        history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
<<<<<<< HEAD
        self.history_text = tk.Text(history_frame, wrap=tk.WORD, state=tk.DISABLED, height=15)
=======
        self.history_text = tk.Text(
            history_frame, wrap=tk.WORD, state=tk.DISABLED, height=15,
            font=("TkFixedFont", 12)
        )
>>>>>>> 70b1b38 (feat(gui): добавлены профили, системный промт, улучшено копирование и шрифт)
        scrollbar = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_text.yview)
        self.history_text.configure(yscrollcommand=scrollbar.set)
        self.history_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.history_text.bind("<Control-c>", lambda e: self.copy_selection())
        self.history_text.bind("<Button-3>", self.show_context_menu)

        status_bar = ttk.Frame(self.root)
        status_bar.pack(fill=tk.X, padx=10, pady=(0, 10))
        ttk.Label(status_bar, text="Статус:").pack(side=tk.LEFT)
        ttk.Label(status_bar, textvariable=self.status_var, foreground="blue").pack(side=tk.LEFT, padx=5)

        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Копировать", command=self.copy_selection)
        self.context_menu.add_command(label="Сохранить ответ как…", command=self.save_selected_response)

    def setup_layout(self):
        pass

<<<<<<< HEAD
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

=======
>>>>>>> 70b1b38 (feat(gui): добавлены профили, системный промт, улучшено копирование и шрифт)
    def browse_model(self):
        path = filedialog.askopenfilename(
            title="Выберите файл модели",
            initialdir=config.DEFAULT_MODEL_DIR,
            filetypes=[("Model files", "*.gguf *.bin"), ("All files", "*.*")]
        )
        if path:
            self.model_path_var.set(path)
            self.logger.info(f"Выбрана модель: {path}")

    def send_message(self):
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
        self.history_text.config(state=tk.NORMAL)
        self.history_text.insert(tk.END, f"{sender}: {message}\n")
<<<<<<< HEAD
=======
        self.history_text.tag_add(sender.lower(), "end-2l", "end-1l")
>>>>>>> 70b1b38 (feat(gui): добавлены профили, системный промт, улучшено копирование и шрифт)
        self.history_text.config(state=tk.DISABLED)
        self.history_text.see(tk.END)

    def clear_history(self):
        if messagebox.askyesno("Подтверждение", "Очистить историю диалога?"):
            self.model_handler.clear_history()
            self.history_text.config(state=tk.NORMAL)
            self.history_text.delete("1.0", tk.END)
            self.history_text.config(state=tk.DISABLED)
            self.logger.info("История диалога очищена в GUI")

    def save_session(self):
        filename = filedialog.asksaveasfilename(
            title="Сохранить сессию",
            initialdir="session_logs",
<<<<<<< HEAD
            initialfile=f"session_{self.root.winfo_name()}",
=======
            initialfile="session.json",
>>>>>>> 70b1b38 (feat(gui): добавлены профили, системный промт, улучшено копирование и шрифт)
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            defaultextension=".json"
        )
        if filename:
            self.model_handler.save_session(filename)
            messagebox.showinfo("Сохранение", "Сессия успешно сохранена!")

    def open_settings(self):
<<<<<<< HEAD
        """Открытие окна настроек"""
        SettingsWindow(self.root, self.model_handler, self.current_font.get(), self.apply_settings_and_font)

    def apply_settings_and_font(self, params, font_name):
        """Применение настроек и шрифта"""
=======
        SettingsWindow(self.root, self.model_handler, self.apply_settings)

    def apply_settings(self, params):
>>>>>>> 70b1b38 (feat(gui): добавлены профили, системный промт, улучшено копирование и шрифт)
        self.model_handler.update_parameters(**params)
        self.current_font.set(font_name)
        self.apply_font()
        self.logger.info(f"Настройки и шрифт обновлены: {params}, шрифт: {font_name}")

    def copy_selection(self):
        try:
            selected = self.history_text.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.root.clipboard_clear()
            self.root.clipboard_append(selected)
        except tk.TclError:
            pass

    def show_context_menu(self, event):
        try:
            index = self.history_text.index(f"@{event.x},{event.y}")
            tags = self.history_text.tag_names(index)
            if "assistant" in tags:
                self.context_menu.entryconfig("Сохранить ответ как…", state="normal")
            else:
                self.context_menu.entryconfig("Сохранить ответ как…", state="disabled")
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()

    def save_selected_response(self):
        try:
            full_text = self.history_text.get("1.0", tk.END)
            lines = [line.strip() for line in full_text.split('\n') if line.strip()]
            assistant_lines = [line for line in lines if line.startswith("Ассистент: ")]
            if not assistant_lines:
                messagebox.showwarning("Сохранение", "Нет ответа ассистента для сохранения.")
                return
            last_response = assistant_lines[-1]
            content = last_response[len("Ассистент: "):].strip()
            filename = filedialog.asksaveasfilename(
                title="Сохранить ответ",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("Markdown", "*.md"), ("All files", "*.*")]
            )
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("Сохранение", f"Ответ сохранён в:\n{filename}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить ответ:\n{str(e)}")


class SettingsWindow:
<<<<<<< HEAD
    """Окно настроек приложения"""
    def __init__(self, parent, model_handler, current_font, apply_callback):
        self.window = tk.Toplevel(parent)
        self.window.title("Настройки")
        self.window.geometry("600x650")
=======
    """Окно настроек с профилями, валидацией и подсказками"""
    def __init__(self, parent, model_handler, apply_callback):
        self.window = tk.Toplevel(parent)
        self.window.title("Настройки")
        self.window.geometry("600x550")
>>>>>>> 70b1b38 (feat(gui): добавлены профили, системный промт, улучшено копирование и шрифт)
        self.window.resizable(True, True)
        self.window.transient(parent)
        self.window.grab_set()

        self.model_handler = model_handler
        self.apply_callback = apply_callback
<<<<<<< HEAD
        self.current_font = current_font

        # Получаем системные шрифты
        try:
            font_names = sorted(set(f.name for f in fm.fontManager.ttflist))
        except:
            font_names = ["Arial", "DejaVu Sans", "Liberation Sans", "Times New Roman", "Courier New"]
        self.font_var = StringVar(value=current_font)
        self.font_list = font_names
=======
        self.params_entries = {}
        self.profile_var = tk.StringVar()
>>>>>>> 70b1b38 (feat(gui): добавлены профили, системный промт, улучшено копирование и шрифт)

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
        self.load_profiles()
        self.setup_layout()

    def create_widgets(self):
<<<<<<< HEAD
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
=======
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        basic_frame = ttk.Frame(notebook)
        notebook.add(basic_frame, text="Основные")

        ttk.Label(basic_frame, text="Системный промт:").grid(row=0, column=0, sticky=tk.W, pady=5, padx=5)
        self.system_prompt_text = tk.Text(basic_frame, height=4, width=50, wrap=tk.WORD)
        self.system_prompt_text.grid(row=0, column=1, columnspan=2, pady=5, padx=5)
        self.add_tooltip(self.system_prompt_text, config.PARAM_INFO['system_prompt']['description'])

        row = 1
        for param in ['temperature', 'max_tokens', 'top_p', 'frequency_penalty', 'presence_penalty', 'repeat_penalty']:
            info = config.PARAM_INFO[param]
            ttk.Label(basic_frame, text=info['label'] + ":").grid(row=row, column=0, sticky=tk.W, pady=2, padx=5)
            entry = ttk.Entry(basic_frame, width=10)
            entry.grid(row=row, column=1, pady=2, padx=5)
            self.params_entries[param] = entry
            self.add_tooltip(entry, info['description'])
            row += 1

        advanced_frame = ttk.Frame(notebook)
        notebook.add(advanced_frame, text="Дополнительно")

        row = 0
        for param in config.PARAM_INFO:
            if param in ['temperature', 'max_tokens', 'top_p', 'frequency_penalty', 'presence_penalty', 'repeat_penalty', 'system_prompt']:
                continue
            info = config.PARAM_INFO[param]
            ttk.Label(advanced_frame, text=info['label'] + ":").grid(row=row, column=0, sticky=tk.W, pady=2, padx=5)
            entry = ttk.Entry(advanced_frame, width=15)
            entry.grid(row=row, column=1, pady=2, padx=5)
            self.params_entries[param] = entry
            self.add_tooltip(entry, info['description'])
            row += 1

        profile_frame = ttk.LabelFrame(self.window, text="Профили")
        profile_frame.pack(fill=tk.X, padx=10, pady=5)
        ttk.Label(profile_frame, text="Профиль:").pack(side=tk.LEFT, padx=5)
        self.profile_combo = ttk.Combobox(profile_frame, textvariable=self.profile_var, state="readonly")
        self.profile_combo.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.profile_combo.bind("<<ComboboxSelected>>", self.load_profile)
        ttk.Button(profile_frame, text="Загрузить", command=self.load_profile).pack(side=tk.LEFT, padx=2)
        ttk.Button(profile_frame, text="Сохранить", command=self.save_profile).pack(side=tk.LEFT, padx=2)
        ttk.Button(profile_frame, text="Удалить", command=self.delete_profile).pack(side=tk.LEFT, padx=2)

        button_frame = ttk.Frame(self.window)
        button_frame.pack(pady=10)
>>>>>>> 70b1b38 (feat(gui): добавлены профили, системный промт, улучшено копирование и шрифт)
        ttk.Button(button_frame, text="Применить", command=self.on_apply).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Отмена", command=self.window.destroy).pack(side=tk.LEFT, padx=5)

<<<<<<< HEAD
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
=======
    def setup_layout(self):
        self.window.columnconfigure(0, weight=1)

    def add_tooltip(self, widget, text):
        def on_enter(e):
            widget.tooltip = tk.Toplevel(widget)
            widget.tooltip.wm_overrideredirect(True)
            x, y, _, _ = widget.bbox("insert")
            x += widget.winfo_rootx() + 25
            y += widget.winfo_rooty() + 25
            widget.tooltip.wm_geometry(f"+{x}+{y}")
            label = tk.Label(
                widget.tooltip, text=text, background="lightyellow",
                relief="solid", borderwidth=1, font=("Segoe UI", 9)
            )
            label.pack()
        def on_leave(e):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()
                del widget.tooltip
        widget.bind("<Enter>", on_enter)
        widget.bind("<Leave>", on_leave)

    def load_profiles(self):
        profiles = []
        if os.path.exists(config.PROFILES_DIR):
            profiles = [f[:-5] for f in os.listdir(config.PROFILES_DIR) if f.endswith(".json")]
        self.profile_combo['values'] = profiles

    def load_profile(self, event=None):
        name = self.profile_var.get()
        if not name:
            return
        path = os.path.join(config.PROFILES_DIR, f"{name}.json")
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            for param, entry in self.params_entries.items():
                value = data.get(param)
                if value is not None:
                    entry.delete(0, tk.END)
                    entry.insert(0, str(value))
            if 'system_prompt' in data:
                self.system_prompt_text.delete("1.0", tk.END)
                self.system_prompt_text.insert("1.0", data['system_prompt'])
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить профиль:\n{str(e)}")

    def save_profile(self):
        name = self.profile_var.get()
        if not name:
            name = simpledialog.askstring("Имя профиля", "Введите имя профиля:")
            if not name:
                return
            self.profile_var.set(name)
        path = os.path.join(config.PROFILES_DIR, f"{name}.json")
        data = {}
        for param, entry in self.params_entries.items():
            value = entry.get().strip()
            if not value:
                continue
            info = config.PARAM_INFO[param]
            try:
                if info['type'] == bool:
                    val = value.lower() in ('true', '1', 'yes', 'on')
                elif info['type'] == float:
                    val = float(value)
                    if info.get('min') is not None and val < info['min']:
                        raise ValueError()
                    if info.get('max') is not None and val > info['max']:
                        raise ValueError()
                elif info['type'] == int:
                    val = int(value)
                    if info.get('min') is not None and val < info['min']:
                        raise ValueError()
                    if info.get('max') is not None and val > info['max']:
                        raise ValueError()
                else:
                    val = value
                data[param] = val
            except Exception:
                messagebox.showerror("Ошибка", f"Неверное значение для '{info['label']}'")
                return
        system_prompt = self.system_prompt_text.get("1.0", tk.END).strip()
        data['system_prompt'] = system_prompt
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.load_profiles()
            messagebox.showinfo("Профиль", "Профиль сохранён!")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить профиль:\n{str(e)}")

    def delete_profile(self):
        name = self.profile_var.get()
        if not name:
            return
        if messagebox.askyesno("Удалить", f"Удалить профиль '{name}'?"):
            path = os.path.join(config.PROFILES_DIR, f"{name}.json")
            try:
                os.remove(path)
                self.profile_var.set("")
                self.load_profiles()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось удалить:\n{str(e)}")

    def on_apply(self):
        params = {}
        for param, entry in self.params_entries.items():
            value = entry.get().strip()
            if not value:
                continue
            info = config.PARAM_INFO[param]
            try:
                if info['type'] == bool:
                    val = value.lower() in ('true', '1', 'yes', 'on')
                elif info['type'] == float:
                    val = float(value)
                    if info.get('min') is not None and val < info['min']:
                        raise ValueError()
                    if info.get('max') is not None and val > info['max']:
                        raise ValueError()
                elif info['type'] == int:
                    val = int(value)
                    if info.get('min') is not None and val < info['min']:
                        raise ValueError()
                    if info.get('max') is not None and val > info['max']:
                        raise ValueError()
                else:
                    val = value
                params[param] = val
            except Exception:
                messagebox.showerror("Ошибка", f"Неверное значение для '{info['label']}'")
                return
        system_prompt = self.system_prompt_text.get("1.0", tk.END).strip()
        params['system_prompt'] = system_prompt
        self.apply_callback(params)
>>>>>>> 70b1b38 (feat(gui): добавлены профили, системный промт, улучшено копирование и шрифт)
        self.window.destroy()
