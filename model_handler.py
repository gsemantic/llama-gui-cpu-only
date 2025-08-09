# model_handler.py
import os
import json
import logging
import threading
from datetime import datetime
from tkinter import messagebox  # Для ошибок в GUI

from config import (
    DEFAULT_MODEL_DIR,
    DEFAULT_MODEL,
    MAX_HISTORY_LENGTH,
    N_THREADS,
    N_CTX,
    DEFAULT_GENERATION_PARAMS
)

# Импортируем движок модели
try:
    from llama_cpp import Llama
except ImportError:
    raise ImportError(
        "Модуль llama_cpp не установлен. Выполни: pip install llama-cpp-python"
    )


class ModelHandler:
    """Класс для управления моделью и диалогами"""
    
    def __init__(self, logger):
        self.logger = logger
        self.history = []
        self.model = None
        self.model_name = ""
        self.model_path = os.path.join(DEFAULT_MODEL_DIR, DEFAULT_MODEL)
        
        # Параметры генерации
        self.temperature = DEFAULT_GENERATION_PARAMS['temperature']
        self.max_tokens = DEFAULT_GENERATION_PARAMS['max_tokens']
        self.top_p = DEFAULT_GENERATION_PARAMS['top_p']
        
        # Загружаем модель
        self.load_model()

    def load_model(self, model_path=None):
        """Загрузка модели из указанного пути"""
        path_to_load = model_path or self.model_path

        if not os.path.exists(path_to_load):
            error_msg = f"Файл модели не найден: {path_to_load}"
            self.logger.error(error_msg)
            messagebox.showerror("Ошибка модели", error_msg)
            return

        try:
            self.logger.info(f"Загрузка модели: {path_to_load}")
            self.model = Llama(
                model_path=path_to_load,
                n_ctx=N_CTX,
                n_threads=N_THREADS,
                n_gpu_layers=0,  # ← изменить на 1+, если есть GPU и llama-cpp-python с CUDA
                verbose=True,   # чтобы видеть прогресс загрузки
            )
            self.model_name = os.path.basename(path_to_load)
            self.logger.info(f"✅ Модель успешно загружена: {self.model_name}")
        except Exception as e:
            error_msg = f"Не удалось загрузить модель:\n{type(e).__name__}: {e}"
            self.logger.error(error_msg)
            messagebox.showerror("Ошибка загрузки", error_msg)

    def add_to_history(self, role, content):
        """Добавление сообщения в историю диалога"""
        if len(self.history) >= MAX_HISTORY_LENGTH:
            self.history.pop(0)
        self.history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        self.logger.debug(f"История ({role}): {content[:60]}...")

    def generate_response(self, prompt, callback):
        """Генерация ответа модели в отдельном потоке"""
        if self.model is None:
            callback("❌ Ошибка: модель не загружена.")
            return

        def worker():
            try:
                # Формируем контекст: system + история + текущий запрос
                # Используем простой формат, так как модель Instruct
                messages = [{"role": "system", "content": "Ты — полезный ассистент."}]
                messages.extend([
                    {"role": "user" if msg["role"] == "user" else "assistant", "content": msg["content"]}
                    for msg in self.history
                ])
                messages.append({"role": "user", "content": prompt})

                # Генерация через llama-cpp
                self.logger.info(f"Генерация ответа... (max_tokens={self.max_tokens})")
                output = self.model.create_chat_completion(
                    messages=messages,
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                    top_p=self.top_p,
                    stream=False  # можно включить stream, но сложнее обрабатывать
                )

                response = output["choices"][0]["message"]["content"].strip()

            except Exception as e:
                self.logger.error(f"Ошибка при генерации: {e}")
                response = f"❌ Ошибка генерации: {e}"

            # Добавляем в историю и возвращаем
            self.add_to_history("assistant", response)
            callback(response)

        thread = threading.Thread(target=worker, daemon=True)
        thread.start()

    def clear_history(self):
        """Очистка истории диалога"""
        self.history = []
        self.logger.info("История диалога очищена")

    def save_session(self, filename=None):
        """Сохранение сессии в JSON"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"session_{timestamp}.json"
        
        session_data = {
            "model_name": self.model_name,
            "model_path": self.model_path,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "top_p": self.top_p,
            "history": self.history
        }
        
        filepath = os.path.join("session_logs", filename)
        os.makedirs("session_logs", exist_ok=True)
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(session_data, f, ensure_ascii=False, indent=4)
            self.logger.info(f"Сессия сохранена: {filepath}")
        except Exception as e:
            self.logger.error(f"Ошибка при сохранении: {e}")
            messagebox.showerror("Ошибка", f"Не удалось сохранить сессию:\n{e}")

    def load_session(self, filename):
        """Загрузка сессии из файла"""
        filepath = os.path.join("session_logs", filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                session_data = json.load(f)
            
            self.model_name = session_data.get("model_name", "")
            self.model_path = session_data.get("model_path", self.model_path)
            self.temperature = session_data.get("temperature", self.temperature)
            self.max_tokens = session_data.get("max_tokens", self.max_tokens)
            self.top_p = session_data.get("top_p", self.top_p)
            self.history = session_data.get("history", [])
            
            self.logger.info(f"Сессия загружена: {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Ошибка при загрузке сессии: {e}")
            messagebox.showerror("Ошибка", f"Не удалось загрузить сессию:\n{e}")
            return False

    def update_parameters(self, **params):
        """Обновление параметров генерации"""
        if 'temperature' in params:
            self.temperature = params['temperature']
        if 'max_tokens' in params:
            self.max_tokens = params['max_tokens']
        if 'top_p' in params:
            self.top_p = params['top_p']
