#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Практическое занятие 26: Tkinter - многопоточность
Решение задач по многопоточности в приложениях Tkinter

Автор: AI Assistant
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import queue
import random
import socket
import urllib.request
import urllib.error
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime


# ==============================================================================
# ЗАДАЧА 1: Проблемы однопоточного интерфейса
# ==============================================================================

class BlockingAppDemo:
    """Демонстрация блокирующей операции в одном потоке"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Задача 1: Блокирующая операция")
        self.root.geometry("400x200")
        
        self.create_ui()
    
    def create_ui(self):
        """Создание UI"""
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        self.status_label = ttk.Label(frame, text="Готов", font=("Arial", 12))
        self.status_label.pack(pady=10)
        
        ttk.Button(
            frame, 
            text="Блокирующая операция (заморозит интерфейс)",
            command=self.blocking_operation
        ).pack(pady=10)
        
        ttk.Button(
            frame, 
            text="Операция в потоке (не заморозит)",
            command=self.non_blocking_operation
        ).pack(pady=10)
    
    def blocking_operation(self):
        """Блокирующая операция - замораживает интерфейс"""
        self.status_label.config(text="Выполняется...")
        self.root.update()
        
        # Имитация долгой операции
        for i in range(10):
            time.sleep(0.5)
            self.status_label.config(text=f"Обработано {i+1}/10")
            self.root.update()
        
        self.status_label.config(text="Готово!")
        messagebox.showinfo("Готово", "Операция завершена")
    
    def non_blocking_operation(self):
        """Неблокирующая операция в отдельном потоке"""
        self.status_label.config(text="Запущен поток...")
        
        def worker():
            for i in range(10):
                time.sleep(0.5)
                # Обновление интерфейса через after
                self.root.after(0, lambda i=i: self.status_label.config(
                    text=f"Обработано {i+1}/10"
                ))
            
            self.root.after(0, lambda: self.status_label.config(text="Готово!"))
            self.root.after(0, lambda: messagebox.showinfo("Готово", "Операция завершена"))
        
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()


# ==============================================================================
# ЗАДАЧА 2: Загрузка данных в потоке
# ==============================================================================

class BackgroundLoaderDemo:
    """Демонстрация загрузки данных в фоновом режиме"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Задача 2: Фоновая загрузка")
        self.root.geometry("500x400")
        
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Готов")
        self.result_var = tk.StringVar()
        self.cancelled = False
        
        self.create_ui()
    
    def create_ui(self):
        """Создание UI"""
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        ttk.Label(
            frame, 
            text="Загрузка данных в фоновом режиме",
            font=("Arial", 12, "bold")
        ).pack(pady=10)
        
        # Прогресс
        self.progress = ttk.Progressbar(
            frame, 
            variable=self.progress_var,
            maximum=100,
            mode='determinate'
        )
        self.progress.pack(fill=tk.X, pady=10)
        
        # Статус
        self.status_label = ttk.Label(frame, textvariable=self.status_var)
        self.status_label.pack(pady=5)
        
        # Результат
        result_frame = ttk.LabelFrame(frame, text="Результат", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.result_text = tk.Text(result_frame, height=8, state=tk.DISABLED)
        self.result_text.pack(fill=tk.BOTH, expand=True)
        
        # Кнопки
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)
        
        self.start_btn = ttk.Button(
            btn_frame, 
            text="Начать загрузку", 
            command=self.start_loading
        )
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame, 
            text="Отмена", 
            command=self.cancel_loading
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame, 
            text="Очистить", 
            command=self.clear_results
        ).pack(side=tk.LEFT, padx=5)
    
    def start_loading(self):
        """Начать загрузку в отдельном потоке"""
        self.cancelled = False
        self.progress_var.set(0)
        self.start_btn.config(state=tk.DISABLED)
        
        def worker():
            items = [
                "Пользователи", "Заказы", "Товары", 
                "Категории", "Отзывы", "Сессии",
                "Настройки", "Логи", "Кэш", "Отчеты"
            ]
            
            total = len(items)
            
            for i, item in enumerate(items):
                if self.cancelled:
                    self.root.after(0, self.on_cancelled)
                    return
                
                # Имитация загрузки
                self.root.after(0, lambda p=0, s=f"Загрузка {item}...": 
                              self.update_progress(p, s))
                
                time.sleep(random.uniform(0.3, 0.8))
                
                progress = (i + 1) / total * 100
                self.root.after(0, lambda p=progress, s=f"Загружено: {item}":
                              self.update_progress(p, s))
                
                self.root.after(0, lambda item=item: self.append_result(f"✓ {item}"))
            
            self.root.after(0, self.on_complete)
        
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
    
    def update_progress(self, value, status):
        """Обновить прогресс"""
        self.progress_var.set(value)
        self.status_var.set(status)
    
    def append_result(self, text):
        """Добавить результат"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.insert(tk.END, text + "\n")
        self.result_text.see(tk.END)
        self.result_text.config(state=tk.DISABLED)
    
    def cancel_loading(self):
        """Отменить загрузку"""
        self.cancelled = True
        self.status_var.set("Отменено...")
    
    def on_complete(self):
        """Обработка завершения"""
        self.start_btn.config(state=tk.NORMAL)
        self.status_var.set("Загрузка завершена!")
        messagebox.showinfo("Готово", "Все данные загружены")
    
    def on_cancelled(self):
        """Обработка отмены"""
        self.start_btn.config(state=tk.NORMAL)
        self.status_var.set("Отменено")
    
    def clear_results(self):
        """Очистить результаты"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        self.result_text.config(state=tk.DISABLED)
        self.progress_var.set(0)
        self.status_var.set("Готов")


# ==============================================================================
# ЗАДАЧА 3: Таймеры и периодические задачи
# ==============================================================================

class TimerApp:
    """Приложение с таймерами"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Задача 3: Таймеры")
        self.root.geometry("450x500")
        
        self.stopwatch_running = False
        self.countdown_running = False
        self.stopwatch_start_time = None
        self.countdown_time = 0
        
        self.create_ui()
    
    def create_ui(self):
        """Создание UI"""
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Вкладка секундомера
        self.stopwatch_frame = ttk.Frame(notebook, padding=20)
        notebook.add(self.stopwatch_frame, text="Секундомер")
        self.create_stopwatch_tab()
        
        # Вкладка таймера обратного отсчета
        self.countdown_frame = ttk.Frame(notebook, padding=20)
        notebook.add(self.countdown_frame, text="Таймер")
        self.create_countdown_tab()
    
    def create_stopwatch_tab(self):
        """Вкладка секундомера"""
        ttk.Label(
            self.stopwatch_frame, 
            text="Секундомер",
            font=("Arial", 18, "bold")
        ).pack(pady=20)
        
        self.stopwatch_display = ttk.Label(
            self.stopwatch_frame, 
            text="00:00:00.00",
            font=("Courier", 32)
        )
        self.stopwatch_display.pack(pady=20)
        
        btn_frame = ttk.Frame(self.stopwatch_frame)
        btn_frame.pack(pady=20)
        
        self.stopwatch_start_btn = ttk.Button(
            btn_frame, 
            text="Старт", 
            command=self.start_stopwatch,
            width=10
        )
        self.stopwatch_start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stopwatch_stop_btn = ttk.Button(
            btn_frame, 
            text="Стоп", 
            command=self.stop_stopwatch,
            state=tk.DISABLED,
            width=10
        )
        self.stopwatch_stop_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame, 
            text="Сброс", 
            command=self.reset_stopwatch,
            width=10
        ).pack(side=tk.LEFT, padx=5)
        
        # Список кругов
        self.laps_text = tk.Text(self.stopwatch_frame, height=10)
        self.laps_text.pack(fill=tk.BOTH, expand=True, pady=10)
        
        ttk.Button(
            self.stopwatch_frame, 
            text="Круг", 
            command=self.add_lap
        ).pack()
    
    def start_stopwatch(self):
        """Запустить секундомер"""
        self.stopwatch_running = True
        self.stopwatch_start_time = time.time()
        
        self.stopwatch_start_btn.config(state=tk.DISABLED)
        self.stopwatch_stop_btn.config(state=tk.NORMAL)
        
        self.update_stopwatch()
    
    def stop_stopwatch(self):
        """Остановить секундомер"""
        self.stopwatch_running = False
        
        self.stopwatch_start_btn.config(state=tk.NORMAL)
        self.stopwatch_stop_btn.config(state=tk.DISABLED)
    
    def reset_stopwatch(self):
        """Сбросить секундомер"""
        self.stopwatch_running = False
        self.stopwatch_display.config(text="00:00:00.00")
        self.laps_text.delete("1.0", tk.END)
        
        self.stopwatch_start_btn.config(state=tk.NORMAL)
        self.stopwatch_stop_btn.config(state=tk.DISABLED)
    
    def update_stopwatch(self):
        """Обновить отображение секундомера"""
        if self.stopwatch_running:
            elapsed = time.time() - self.stopwatch_start_time
            self.stopwatch_display.config(text=self.format_time(elapsed))
            self.root.after(10, self.update_stopwatch)
    
    def add_lap(self):
        """Добавить круг"""
        if self.stopwatch_running:
            elapsed = time.time() - self.stopwatch_start_time
            self.laps_text.insert(tk.END, f"Круг {self.laps_text.index('end').split('.')[0]}: {self.format_time(elapsed)}\n")
            self.laps_text.see(tk.END)
    
    def create_countdown_tab(self):
        """Вкладка таймера обратного отсчета"""
        ttk.Label(
            self.countdown_frame, 
            text="Таймер обратного отсчета",
            font=("Arial", 18, "bold")
        ).pack(pady=20)
        
        # Ввод времени
        input_frame = ttk.Frame(self.countdown_frame)
        input_frame.pack(pady=10)
        
        ttk.Label(input_frame, text="Часы:").grid(row=0, column=0)
        self.hours_var = tk.IntVar(value=0)
        ttk.Spinbox(input_frame, from_=0, to=23, width=5, textvariable=self.hours_var).grid(row=0, column=1, padx=5)
        
        ttk.Label(input_frame, text="Минуты:").grid(row=0, column=2)
        self.minutes_var = tk.IntVar(value=5)
        ttk.Spinbox(input_frame, from_=0, to=59, width=5, textvariable=self.minutes_var).grid(row=0, column=3, padx=5)
        
        ttk.Label(input_frame, text="Секунды:").grid(row=0, column=4)
        self.seconds_var = tk.IntVar(value=0)
        ttk.Spinbox(input_frame, from_=0, to=59, width=5, textvariable=self.seconds_var).grid(row=0, column=5, padx=5)
        
        self.countdown_display = ttk.Label(
            self.countdown_frame, 
            text="05:00:00",
            font=("Courier", 36)
        )
        self.countdown_display.pack(pady=20)
        
        btn_frame = ttk.Frame(self.countdown_frame)
        btn_frame.pack(pady=10)
        
        self.countdown_start_btn = ttk.Button(
            btn_frame, 
            text="Старт", 
            command=self.start_countdown,
            width=10
        )
        self.countdown_start_btn.pack(side=tk.LEFT, padx=5)
        
        self.countdown_stop_btn = ttk.Button(
            btn_frame, 
            text="Стоп", 
            command=self.stop_countdown,
            state=tk.DISABLED,
            width=10
        )
        self.countdown_stop_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame, 
            text="Сброс", 
            command=self.reset_countdown,
            width=10
        ).pack(side=tk.LEFT, padx=5)
    
    def start_countdown(self):
        """Запустить таймер"""
        self.countdown_time = (
            self.hours_var.get() * 3600 + 
            self.minutes_var.get() * 60 + 
            self.seconds_var.get()
        )
        
        if self.countdown_time > 0:
            self.countdown_running = True
            
            self.countdown_start_btn.config(state=tk.DISABLED)
            self.countdown_stop_btn.config(state=tk.NORMAL)
            
            self.update_countdown()
    
    def stop_countdown(self):
        """Остановить таймер"""
        self.countdown_running = False
        
        self.countdown_start_btn.config(state=tk.NORMAL)
        self.countdown_stop_btn.config(state=tk.DISABLED)
    
    def reset_countdown(self):
        """Сбросить таймер"""
        self.countdown_running = False
        self.countdown_time = 0
        self.countdown_display.config(text="00:00:00")
        
        self.countdown_start_btn.config(state=tk.NORMAL)
        self.countdown_stop_btn.config(state=tk.DISABLED)
    
    def update_countdown(self):
        """Обновить отображение таймера"""
        if self.countdown_running and self.countdown_time > 0:
            self.countdown_time -= 1
            
            hours = self.countdown_time // 3600
            minutes = (self.countdown_time % 3600) // 60
            seconds = self.countdown_time % 60
            
            self.countdown_display.config(
                text=f"{hours:02d}:{minutes:02d}:{seconds:02d}"
            )
            
            self.root.after(1000, self.update_countdown)
        
        elif self.countdown_time == 0 and self.countdown_running:
            self.countdown_running = False
            messagebox.showinfo("Таймер", "Время вышло!")
            self.reset_countdown()
    
    def format_time(self, seconds):
        """Форматировать время"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        centisecs = int((seconds - int(seconds)) * 100)
        
        return f"{hours:02d}:{minutes:02d}:{secs:02d}.{centisecs:02d}"


# ==============================================================================
# ЗАДАЧА 4: Сетевые операции
# ==============================================================================

class NetworkApp:
    """Приложение для сетевых операций"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Задача 4: Сетевые операции")
        self.root.geometry("600x500")
        
        self.create_ui()
    
    def create_ui(self):
        """Создание UI"""
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        ttk.Label(
            frame, 
            text="Сетевые операции",
            font=("Arial", 14, "bold")
        ).pack(pady=10)
        
        # URL для загрузки
        url_frame = ttk.Frame(frame)
        url_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(url_frame, text="URL:").pack(side=tk.LEFT)
        self.url_entry = ttk.Entry(url_frame)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.url_entry.insert(0, "https://example.com")
        
        # Прогресс загрузки
        self.progress = ttk.Progressbar(frame, mode='indeterminate')
        self.progress.pack(fill=tk.X, pady=10)
        
        # Статус
        self.status_var = tk.StringVar(value="Готов")
        ttk.Label(frame, textvariable=self.status_var).pack(pady=5)
        
        # Кнопки
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(
            btn_frame, 
            text="Загрузить страницу", 
            command=self.download_page
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame, 
            text="Проверить соединение", 
            command=self.check_connection
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame, 
            text="Сканировать порты", 
            command=self.scan_ports
        ).pack(side=tk.LEFT, padx=5)
        
        # Результат
        result_frame = ttk.LabelFrame(frame, text="Результат", padding=10)
        result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.result_text = tk.Text(result_frame, state=tk.DISABLED)
        self.result_text.pack(fill=tk.BOTH, expand=True)
    
    def download_page(self):
        """Загрузить веб-страницу"""
        url = self.url_entry.get().strip()
        
        if not url:
            messagebox.showerror("Ошибка", "Введите URL")
            return
        
        self.progress.start()
        self.status_var.set("Загрузка...")
        
        def worker():
            try:
                # Добавить протокол, если нет
                if not url.startswith(('http://', 'https://')):
                    url = 'https://' + url
                
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=10) as response:
                    content = response.read().decode('utf-8', errors='ignore')
                    
                    self.root.after(0, lambda: self.show_result(
                        f"Загружено: {len(content)} байт\n\n"
                        f"Первые 500 символов:\n{content[:500]}"
                    ))
                    
            except urllib.error.URLError as e:
                self.root.after(0, lambda e=e: self.show_error(f"Ошибка: {e}"))
            except Exception as e:
                self.root.after(0, lambda e=e: self.show_error(f"Ошибка: {e}"))
            finally:
                self.root.after(0, self.progress.stop)
                self.root.after(0, lambda: self.status_var.set("Готов"))
        
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
    
    def check_connection(self):
        """Проверить соединение"""
        self.status_var.set("Проверка соединения...")
        
        def worker():
            try:
                socket.create_connection(("8.8.8.8", 53), timeout=3)
                self.root.after(0, lambda: self.show_result("✓ Соединение с интернетом активно"))
            except OSError:
                self.root.after(0, lambda: self.show_error("✗ Нет соединения с интернетом"))
            
            self.root.after(0, lambda: self.status_var.set("Готов"))
        
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
    
    def scan_ports(self):
        """Сканировать порты"""
        self.status_var.set("Сканирование портов...")
        
        def worker():
            ports = [21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995, 3306, 5432, 8080]
            results = []
            
            for port in ports:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex(('example.com', port))
                    sock.close()
                    
                    if result == 0:
                        results.append(f"Порт {port}: ОТКРЫТ")
                except (socket.error, OSError) as e:
                    # Игнорируем ошибки сокетов - это ожидаемо при сканировании
                    pass
            
            if results:
                self.root.after(0, lambda: self.show_result("Открытые порты:\n" + "\n".join(results)))
            else:
                self.root.after(0, lambda: self.show_result("Ни одного стандартного порта не найдено"))
            
            self.root.after(0, lambda: self.status_var.set("Готов"))
        
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
    
    def show_result(self, text):
        """Показать результат"""
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", text)
        self.result_text.config(state=tk.DISABLED)
    
    def show_error(self, text):
        """Показать ошибку"""
        self.show_result(text)
        messagebox.showerror("Ошибка", text)


# ==============================================================================
# ЗАДАЧА 5: Паттерны многопоточности
# ==============================================================================

class ThreadPoolDemo:
    """Демонстрация паттернов многопоточности"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Задача 5: Паттерны многопоточности")
        self.root.geometry("600x500")
        
        self.executor = ThreadPoolExecutor(max_workers=3)
        self.task_queue = queue.Queue()
        self.running = True
        
        self.create_ui()
        self.start_queue_processor()
    
    def create_ui(self):
        """Создание UI"""
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # ThreadPoolExecutor
        self.pool_frame = ttk.Frame(notebook, padding=20)
        notebook.add(self.pool_frame, text="ThreadPool")
        self.create_threadpool_tab()
        
        # Producer-Consumer
        self.pc_frame = ttk.Frame(notebook, padding=20)
        notebook.add(self.pc_frame, text="Producer-Consumer")
        self.create_producer_consumer_tab()
        
        # Active Object
        self.ao_frame = ttk.Frame(notebook, padding=20)
        notebook.add(self.ao_frame, text="Active Object")
        self.create_active_object_tab()
    
    def create_threadpool_tab(self):
        """Вкладка ThreadPool"""
        ttk.Label(
            self.pool_frame, 
            text="ThreadPoolExecutor",
            font=("Arial", 14, "bold")
        ).pack(pady=10)
        
        ttk.Label(
            self.pool_frame,
            text="Выполнение задач в пуле потоков (макс. 3 потока)"
        ).pack()
        
        self.pool_progress = ttk.Progressbar(self.pool_frame, mode='determinate', maximum=100)
        self.pool_progress.pack(fill=tk.X, pady=10)
        
        self.pool_status = ttk.Label(self.pool_frame, text="Готов")
        self.pool_status.pack(pady=5)
        
        btn_frame = ttk.Frame(self.pool_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(
            btn_frame, 
            text="Запустить задачи", 
            command=self.run_pool_tasks
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame, 
            text="Очистить", 
            command=self.clear_pool
        ).pack(side=tk.LEFT, padx=5)
        
        self.pool_log = tk.Text(self.pool_frame, height=15)
        self.pool_log.pack(fill=tk.BOTH, expand=True, pady=10)
    
    def run_pool_tasks(self):
        """Запустить задачи в пуле"""
        def task(n):
            for i in range(10):
                time.sleep(0.2)
                progress = (i + 1) * 10
                self.root.after(0, lambda p=progress, t=n: self.update_pool_progress(p, t))
            
            return f"Задача {n} завершена"
        
        for i in range(5):
            future = self.executor.submit(task, i + 1)
            future.add_done_callback(lambda f: self.log_pool(f.result()))
    
    def update_pool_progress(self, progress, task_num):
        """Обновить прогресс"""
        self.pool_progress['value'] = progress
        self.pool_status.config(text=f"Выполняется задача {task_num}: {progress}%")
    
    def log_pool(self, message):
        """Логировать сообщение"""
        self.pool_log.insert(tk.END, message + "\n")
        self.pool_log.see(tk.END)
    
    def clear_pool(self):
        """Очистить лог"""
        self.pool_log.delete("1.0", tk.END)
        self.pool_progress['value'] = 0
        self.pool_status.config(text="Готов")
    
    def create_producer_consumer_tab(self):
        """Вкладка Producer-Consumer"""
        ttk.Label(
            self.pc_frame, 
            text="Producer-Consumer паттерн",
            font=("Arial", 14, "bold")
        ).pack(pady=10)
        
        ttk.Label(
            self.pc_frame,
            text="Производители добавляют данные, потребители их обрабатывают"
        ).pack()
        
        self.pc_queue_label = ttk.Label(self.pc_frame, text="Очередь: 0")
        self.pc_queue_label.pack(pady=5)
        
        btn_frame = ttk.Frame(self.pc_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(
            btn_frame, 
            text="Добавить данные (Producer)", 
            command=self.add_to_queue
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame, 
            text="Остановить", 
            command=self.stop_queue_processor
        ).pack(side=tk.LEFT, padx=5)
        
        self.pc_log = tk.Text(self.pc_frame, height=18)
        self.pc_log.pack(fill=tk.BOTH, expand=True, pady=10)
    
    def start_queue_processor(self):
        """Запустить обработчик очереди"""
        self.running = True
        
        def consumer():
            while self.running:
                try:
                    item = self.task_queue.get(timeout=0.5)
                    time.sleep(1)  # Обработка
                    self.root.after(0, lambda i=item: self.log_queue(f"Обработано: {i}"))
                    self.task_queue.task_done()
                    self.root.after(0, self.update_queue_count)
                except queue.Empty:
                    pass
        
        thread = threading.Thread(target=consumer, daemon=True)
        thread.start()
    
    def add_to_queue(self):
        """Добавить элемент в очередь"""
        item = f"Данные-{random.randint(1000, 9999)}"
        self.task_queue.put(item)
        self.log_queue(f"Добавлено: {item}")
        self.update_queue_count()
    
    def update_queue_count(self):
        """Обновить счетчик очереди"""
        count = self.task_queue.qsize()
        self.pc_queue_label.config(text=f"Очередь: {count}")
    
    def log_queue(self, message):
        """Логировать сообщение"""
        self.pc_log.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} - {message}\n")
        self.pc_log.see(tk.END)
    
    def stop_queue_processor(self):
        """Остановить обработчик"""
        self.running = False
    
    def create_active_object_tab(self):
        """Вкладка Active Object"""
        ttk.Label(
            self.ao_frame, 
            text="Active Object паттерн",
            font=("Arial", 14, "bold")
        ).pack(pady=10)
        
        ttk.Label(
            self.ao_frame,
            text="Асинхронное выполнение методов через очередь"
        ).pack()
        
        self.ao_status = ttk.Label(self.ao_frame, text="Статус: Ожидание")
        self.ao_status.pack(pady=5)
        
        btn_frame = ttk.Frame(self.ao_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(
            btn_frame, 
            text="Асинхронная операция 1", 
            command=lambda: self.async_operation("Операция 1")
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame, 
            text="Асинхронная операция 2", 
            command=lambda: self.async_operation("Операция 2")
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame, 
            text="Асинхронная операция 3", 
            command=lambda: self.async_operation("Операция 3")
        ).pack(side=tk.LEFT, padx=5)
        
        self.ao_log = tk.Text(self.ao_frame, height=18)
        self.ao_log.pack(fill=tk.BOTH, expand=True, pady=10)
    
    def async_operation(self, name):
        """Асинхронная операция"""
        self.ao_status.config(text=f"Запущена: {name}")
        
        def worker():
            time.sleep(random.uniform(1, 3))
            self.root.after(0, lambda n=name: self.log_ao(f"Завершена: {n}"))
            self.root.after(0, lambda: self.ao_status.config(text="Статус: Ожидание"))
        
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
    
    def log_ao(self, message):
        """Логировать сообщение"""
        self.ao_log.insert(tk.END, f"{datetime.now().strftime('%H:%M:%S')} - {message}\n")
        self.ao_log.see(tk.END)
    
    def on_close(self):
        """Закрытие"""
        self.running = False
        self.executor.shutdown(wait=False)
        self.root.destroy()


# ==============================================================================
# ГЛАВНОЕ МЕНЮ ПРИЛОЖЕНИЯ
# ==============================================================================

class MainApp:
    """Главное приложение с выбором задач"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Практическое занятие 26: Tkinter - многопоточность")
        self.root.geometry("500x400")
        
        self.create_main_menu()
    
    def create_main_menu(self):
        """Создание главного меню"""
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title = ttk.Label(
            main_frame, 
            text="Выберите задачу:",
            font=("Arial", 16, "bold")
        )
        title.pack(pady=(0, 20))
        
        tasks = [
            ("Задача 1: Блокирующие операции", self.open_task1),
            ("Задача 2: Фоновая загрузка", self.open_task2),
            ("Задача 3: Таймеры", self.open_task3),
            ("Задача 4: Сетевые операции", self.open_task4),
            ("Задача 5: Паттерны многопоточности", self.open_task5),
        ]
        
        for text, command in tasks:
            btn = ttk.Button(main_frame, text=text, width=35, command=command)
            btn.pack(pady=5)
        
        ttk.Button(main_frame, text="Выход", command=self.root.quit).pack(pady=20)
    
    def open_task1(self):
        """Открыть задачу 1"""
        window = tk.Toplevel(self.root)
        BlockingAppDemo(window)
    
    def open_task2(self):
        """Открыть задачу 2"""
        window = tk.Toplevel(self.root)
        BackgroundLoaderDemo(window)
    
    def open_task3(self):
        """Открыть задачу 3"""
        window = tk.Toplevel(self.root)
        TimerApp(window)
    
    def open_task4(self):
        """Открыть задачу 4"""
        window = tk.Toplevel(self.root)
        NetworkApp(window)
    
    def open_task5(self):
        """Открыть задачу 5"""
        window = tk.Toplevel(self.root)
        app = ThreadPoolDemo(window)
        window.protocol("WM_DELETE_WINDOW", app.on_close)


def main():
    """Точка входа"""
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
