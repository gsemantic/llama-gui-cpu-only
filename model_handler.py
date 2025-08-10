# model_handler.py
import os
import json
import logging
import threading
from datetime import datetime
from tkinter import messagebox
from config import (
    DEFAULT_MODEL_DIR,
    DEFAULT_MODEL,
    MAX_HISTORY_LENGTH,
    N_THREADS,
    N_CTX,
    DEFAULT_GENERATION_PARAMS
)

try:
    from llama_cpp import Llama
except ImportError:
    raise ImportError("Модуль llama_cpp не установлен. Выполни: pip install llama-cpp-python")


class ModelHandler:
    """Класс для управления моделью и диалогами"""
    def __init__(self, logger):
        self.logger = logger
        self.history = []
        self.model = None
        self.model_name = ""
        self.model_path = os.path.join(DEFAULT_MODEL_DIR, DEFAULT_MODEL)
        # Храним все параметры в одном словаре
        self.params = DEFAULT_GENERATION_PARAMS.copy()
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
                n_ctx=self.params.get('num_ctx', N_CTX),
                n_threads=N_THREADS,
                n_gpu_layers=0,
                verbose=True,
                use_mmap=self.params.get('use_mmap', True),
                use_mlock=self.params.get('use_mlock', False),
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
                messages = [{"role": "system", "content": "Ты — полезный ассистент."}]
                messages.extend([
                    {"role": "user" if msg["role"] == "user" else "assistant", "content": msg["content"]}
                    for msg in self.history
                ])
                messages.append({"role": "user", "content": prompt})

                self.logger.info(f"Генерация ответа... (max_tokens={self.params['max_tokens']})")
                output = self.model.create_chat_completion(
                    messages=messages,
                    temperature=self.params['temperature'],
                    max_tokens=self.params['max_tokens'],
                    top_p=self.params['top_p'],
                    top_k=self.params.get('top_k', 40),
                    min_p=self.params.get('min_p', 0.05),
                    typical_p=self.params.get('typical_p', 1.0),
                    frequency_penalty=self.params.get('frequency_penalty', 0.0),
                    presence_penalty=self.params.get('presence_penalty', 0.0),
                    repeat_penalty=self.params.get('repeat_penalty', 1.1),
                    tfs_z=self.params.get('tfs_z', 1.0),
                    mirostat_mode=self.params.get('mirostat_mode', 0),
                    mirostat_tau=self.params.get('mirostat_tau', 5.0),
                    mirostat_eta=self.params.get('mirostat_eta', 0.1),
                    seed=self.params.get('seed', -1),
                    num_ctx=self.params.get('num_ctx', 2048),
                    num_batch=self.params.get('num_batch', 512),
                    num_keep=self.params.get('num_keep', 0),
                    num_predict=self.params.get('num_predict', -1),
                    penalize_nl=self.params.get('penalize_nl', False),
                    cache_prompt=self.params.get('cache_prompt', True),
                    echo=self.params.get('echo', False),
                    include_bos_token=self.params.get('include_bos_token', True),
                    grammar=self.params.get('grammar', ''),
                    logit_bias=self.params.get('logit_bias'),
                    stop=self.params.get('stop', []),
                    response_format=self.params.get('response_format'),
                    stream=self.params.get('stream', True),
                )
                response = output["choices"][0]["message"]["content"].strip()
            except Exception as e:
                self.logger.error(f"Ошибка при генерации: {e}")
                response = f"❌ Ошибка генерации: {e}"

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
            "params": self.params,
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
            saved_params = session_data.get("params", {})
            self.params.update(saved_params)
            self.history = session_data.get("history", [])
            self.logger.info(f"Сессия загружена: {filepath}")
            return True
        except Exception as e:
            self.logger.error(f"Ошибка при загрузке сессии: {e}")
            messagebox.showerror("Ошибка", f"Не удалось загрузить сессию:\n{e}")
            return False

    def update_parameters(self, **params):
        """Обновление параметров генерации"""
        valid_keys = set(DEFAULT_GENERATION_PARAMS.keys())
        for key, value in params.items():
            if key in valid_keys:
                self.params[key] = value
        self.logger.info(f"Параметры обновлены: {params}")
