# Практическое занятие 26: Tkinter - многопоточность

## Цель занятия
Изучить принципы многопоточности в приложениях Tkinter, научиться выполнять длительные операции в отдельных потоках без блокировки интерфейса, освоить синхронизацию потоков.

## Задачи
1. Понять проблемы однопоточного интерфейса
2. Освоить threading в Python
3. Научиться обновлять GUI из рабочего потока
4. Реализовать прогресс-бар и отмену операций

## Ход работы

### 1. Основы threading

```python
import threading
import time

def long_task(callback):
    """
    Длительная задача
    
    Args:
        callback: Функция для обновления прогресса
    """
    # ВАШ КОД ЗДЕСЬ - выполните длительную операцию
    # Вызывайте callback для обновления GUI
    pass
```

---

## 1. Теоретическая часть: Многопоточность в Tkinter

### Уровень 1 - Начальный

#### Задание 1.1: Проблемы однопоточного интерфейса

Демонстрация проблем:

```python
class BlockingDemo:
    """
    Демонстрация блокирующей операции
    """
    def __init__(self, root):
        self.root = root
        
        # ВАШ КОД ЗДЕСЬ - создайте кнопку с блокирующей операцией
        # Покажите, что интерфейс зависает
        pass
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import tkinter as tk
from tkinter import ttk
import time

root = tk.Tk()
root.title("Блокирующая операция")

label = ttk.Label(root, text="Нажмите кнопку")
label.pack(pady=20)

def blocking_operation():
    time.sleep(5)  # Блокировка на 5 секунд
    label.config(text="Готово!")

def on_click():
    label.config(text="Работаю...")
    blocking_operation()

btn = ttk.Button(root, text="Запустить", command=on_click)
btn.pack(pady=20)

root.mainloop()
```

</details>

### Уровень 2 - Средний

#### Задание 2.1: Загрузка данных в потоке

Реализуйте асинхронную загрузку:

```python
import threading

class AsyncLoader:
    """
    Асинхронная загрузка данных
    """
    def __init__(self, root):
        self.root = root
        
        # ВАШ КОД ЗДЕСЬ - создайте:
        # Progressbar
        # Кнопку запуска
        # Кнопку отмены
        pass
        
    def run_in_thread(self):
        """
        Запускает задачу в отдельном потоке
        """
        # ВАШ КОД ЗДЕСЬ - используйте threading.Thread
        # Обновляйте GUI через root.after()
        pass
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import tkinter as tk
from tkinter import ttk
import threading
import time

class AsyncLoader:
    def __init__(self, root):
        self.root = root
        self.running = False
        
        self.label = ttk.Label(root, text="Готов")
        self.label.pack(pady=10)
        
        self.progress = ttk.Progressbar(root, mode='determinate', length=300)
        self.progress.pack(pady=10)
        
        btn_frame = ttk.Frame(root)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Старт", command=self.start).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Стоп", command=self.stop).pack(side=tk.LEFT, padx=5)
    
    def start(self):
        self.running = True
        self.progress['value'] = 0
        thread = threading.Thread(target=self.long_task)
        thread.start()
    
    def stop(self):
        self.running = False
    
    def long_task(self):
        for i in range(100):
            if not self.running:
                break
            time.sleep(0.05)
            self.root.after(0, self.update_progress, i + 1)
        self.root.after(0, self.task_done)
    
    def update_progress(self, value):
        self.progress['value'] = value
        self.label.config(text=f"Загрузка: {value}%")
    
    def task_done(self):
        self.label.config(text="Готово!")

root = tk.Tk()
app = AsyncLoader(root)
root.mainloop()
```

</details>

### Уровень 3 - Продвинутый

#### Задание 3.1: Паттерны многопоточности

Реализуйте сложные паттерны:

```python
from queue import Queue
import threading

class TaskQueue:
    """
    Потокобезопасная очередь задач
    """
    def __init__(self):
        self.queue = Queue()
        # ВАШ КОД ЗДЕСЬ - реализуйте:
        # ThreadPoolExecutor
        # Producer-Consumer
        pass
        
class DownloadManager:
    """
    Менеджер загрузок
    """
    def __init__(self, root):
        # ВАШ КОД ЗДЕСЬ - создайте менеджер загрузок
        pass
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import tkinter as tk
from tkinter import ttk
from queue import Queue
import threading
import time

class DownloadManager:
    def __init__(self, root):
        self.root = root
        self.queue = Queue()
        self.downloads = []
        
        self.create_ui()
        self.worker_thread()
    
    def create_ui(self):
        self.listbox = tk.Listbox(self.root)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Добавить загрузку", 
                  command=self.add_download).pack(side=tk.LEFT, padx=5)
    
    def add_download(self):
        url = f"Файл {len(self.downloads) + 1}"
        self.downloads.append({"url": url, "progress": 0})
        self.queue.put(len(self.downloads) - 1)
        self.listbox.insert(tk.END, f"{url}: 0%")
    
    def worker_thread(self):
        def worker():
            while True:
                index = self.queue.get()
                if index is None:
                    break
                self.download_file(index)
                self.queue.task_done()
        
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
    
    def download_file(self, index):
        for progress in range(101):
            time.sleep(0.05)
            self.root.after(0, self.update_progress, index, progress)
    
    def update_progress(self, index, progress):
        self.listbox.delete(index)
        self.listbox.insert(index, f"Файл {index + 1}: {progress}%")

root = tk.Tk()
app = DownloadManager(root)
root.mainloop()
```

</details>

---

## Важные замечания
- Никогда не обновляйте GUI напрямую из рабочего потока
- Используйте root.after() для обновления интерфейса
- Применяйте блокировки для общих данных
- Обрабатывайте исключения в потоках

## Требования к отчету
- Исходный код всех приложений
- Описание архитектуры потоков
- Диаграмма взаимодействия

## Критерии оценки
- Функциональность: 35%
- Многопоточность: 30%
- Безопасность: 20%
- Документация: 15%
