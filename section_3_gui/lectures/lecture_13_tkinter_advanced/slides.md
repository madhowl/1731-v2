# Лекция 13: Tkinter - продвинутый уровень

## Продвинутые виджеты, MVC/MVP паттерны, многопоточность

### План лекции:
1. Продвинутые виджеты Tkinter
2. Архитектурные паттерны в GUI-приложениях
3. Многопоточность в Tkinter
4. Пользовательские виджеты
5. Работа с изображениями
6. Практические примеры

---

## 1. Продвинутые виджеты Tkinter

### Canvas и его возможности

Canvas - это мощный виджет для рисования графики, текста и других элементов. Он позволяет создавать интерактивные графические интерфейсы.

```python
import tkinter as tk
from tkinter import ttk

class CanvasDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Canvas Demo")
        self.root.geometry("800x600")
        
        # Создание Canvas
        self.canvas = tk.Canvas(root, width=780, height=500, bg="white", relief="sunken", bd=2)
        self.canvas.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Добавление инструментов рисования
        self.setup_tools()
        
        # Рисование начальных фигур
        self.draw_initial_shapes()
    
    def setup_tools(self):
        # Панель инструментов
        toolbar = tk.Frame(self.root)
        toolbar.pack(fill="x", padx=10)
        
        tk.Button(toolbar, text="Очистить", command=self.clear_canvas).pack(side="left", padx=5)
        tk.Button(toolbar, text="Рисовать круг", command=self.draw_circle).pack(side="left", padx=5)
        tk.Button(toolbar, text="Рисовать прямоугольник", command=self.draw_rectangle).pack(side="left", padx=5)
        tk.Button(toolbar, text="Рисовать линию", command=self.draw_line).pack(side="left", padx=5)
        
        # Выбор цвета
        tk.Label(toolbar, text="Цвет:").pack(side="left", padx=(20, 5))
        self.color_var = tk.StringVar(value="black")
        color_options = ["black", "red", "blue", "green", "yellow", "purple"]
        color_menu = tk.OptionMenu(toolbar, self.color_var, *color_options)
        color_menu.pack(side="left", padx=5)
        
        # Размер кисти
        tk.Label(toolbar, text="Размер:").pack(side="left", padx=(20, 5))
        self.brush_size = tk.Scale(toolbar, from_=1, to=20, orient="horizontal", length=100)
        self.brush_size.set(5)
        self.brush_size.pack(side="left", padx=5)
    
    def draw_initial_shapes(self):
        # Рисование различных фигур на Canvas
        # Прямоугольник
        self.canvas.create_rectangle(50, 50, 150, 100, fill="lightblue", outline="navy", width=2)
        
        # Овал
        self.canvas.create_oval(200, 50, 300, 150, fill="lightgreen", outline="darkgreen", width=2)
        
        # Многоугольник
        self.canvas.create_polygon(350, 50, 400, 100, 350, 150, fill="pink", outline="magenta", width=2)
        
        # Линия
        self.canvas.create_line(50, 200, 150, 250, fill="red", width=3)
        
        # Текст
        self.canvas.create_text(400, 200, text="Текст на Canvas", font=("Arial", 16), fill="purple")
        
        # Дуга
        self.canvas.create_arc(500, 50, 600, 150, start=0, extent=180, fill="yellow", outline="orange", style="pieslice")
    
    def clear_canvas(self):
        """Очистка холста"""
        self.canvas.delete("all")
    
    def draw_circle(self):
        """Рисование круга"""
        color = self.color_var.get()
        size = self.brush_size.get()
        import random
        x = random.randint(50, 700)
        y = random.randint(50, 400)
        self.canvas.create_oval(x, y, x+size*4, y+size*4, 
                               fill=color, outline=color, width=size)
    
    def draw_rectangle(self):
        """Рисование прямоугольника"""
        color = self.color_var.get()
        size = self.brush_size.get()
        import random
        x = random.randint(50, 700)
        y = random.randint(50, 400)
        self.canvas.create_rectangle(x, y, x+size*6, y+size*4, 
                                    fill="", outline=color, width=size)
    
    def draw_line(self):
        """Рисование линии"""
        color = self.color_var.get()
        size = self.brush_size.get()
        import random
        x1 = random.randint(50, 700)
        y1 = random.randint(50, 400)
        x2 = random.randint(50, 700)
        y2 = random.randint(50, 400)
        self.canvas.create_line(x1, y1, x2, y2, 
                               fill=color, width=size)

root = tk.Tk()
app = CanvasDemo(root)
root.mainloop()
```

### Treeview (таблицы и иерархические данные)

```python
class TreeviewDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Treeview Demo")
        self.root.geometry("800x600")
        
        # Создание Treeview
        columns = ("Имя", "Возраст", "Город", "Должность")
        self.tree = ttk.Treeview(root, columns=columns, show="tree headings")
        
        # Настройка заголовков
        self.tree.heading("#0", text="ID")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Добавление данных
        parent1 = self.tree.insert("", tk.END, text="Отдел 1", values=("", "", "", ""))
        parent2 = self.tree.insert("", tk.END, text="Отдел 2", values=("", "", "", ""))
        
        # Добавление дочерних элементов
        self.tree.insert(parent1, tk.END, text="Сотрудник 1", values=("Иван Иванов", "30", "Москва", "Программист"))
        self.tree.insert(parent1, tk.END, text="Сотрудник 2", values=("Мария Петрова", "25", "СПб", "Дизайнер"))
        self.tree.insert(parent2, tk.END, text="Сотрудник 3", values=("Алексей Сидоров", "35", "Новосибирск", "Менеджер"))
        
        # Добавление прокрутки
        tree_scrollbar = ttk.Scrollbar(root, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 5), pady=5)

# root = tk.Tk()
# app = TreeviewDemo(root)
# root.mainloop()
```

---

## 2. Архитектурные паттерны в GUI-приложениях

### Паттерн MVC (Model-View-Controller)

```python
class User:
    """Модель данных пользователя"""
    def __init__(self, name, email, age):
        self.name = name
        self.email = email
        self.age = age

class UserModel:
    """Модель для управления пользователями"""
    def __init__(self):
        self.users = []
        self._observers = []
    
    def add_user(self, user):
        self.users.append(user)
        self._notify_observers()
    
    def get_users(self):
        return self.users.copy()
    
    def attach_observer(self, observer):
        self._observers.append(observer)
    
    def _notify_observers(self):
        for observer in self._observers:
            observer.update_users_list(self.users)

class UserView:
    """Представление для отображения пользователей"""
    def __init__(self, root, controller):
        self.controller = controller
        self.frame = ttk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Таблица для отображения пользователей
        columns = ("Имя", "Email", "Возраст")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Прокрутка
        tree_scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Форма для добавления
        self.create_input_form()
    
    def create_input_form(self):
        input_frame = ttk.LabelFrame(self.frame, text="Добавить пользователя")
        input_frame.pack(fill=tk.X, pady=10)
        
        # Поля ввода
        fields = ["Имя", "Email", "Возраст"]
        self.entries = {}
        
        for i, field in enumerate(fields):
            ttk.Label(input_frame, text=field).grid(row=0, column=i*2, sticky="w", padx=(5, 5), pady=5)
            entry = ttk.Entry(input_frame, width=20)
            entry.grid(row=0, column=i*2+1, padx=(0, 15), pady=5)
            self.entries[field.lower()] = entry
        
        # Кнопка добавления
        add_btn = ttk.Button(input_frame, text="Добавить", command=self.add_user)
        add_btn.grid(row=0, column=6, padx=5, pady=5)
    
    def add_user(self):
        """Обработка добавления пользователя"""
        try:
            name = self.entries["имя"].get()
            email = self.entries["email"].get()
            age_str = self.entries["возраст"].get()
            
            if not name or not email or not age_str:
                raise ValueError("Все поля обязательны для заполнения")
            
            age = int(age_str)
            user = User(name, email, age)
            
            self.controller.add_user(user)
            
            # Очистка полей
            for entry in self.entries.values():
                entry.delete(0, tk.END)
        except ValueError as e:
            from tkinter import messagebox
            messagebox.showerror("Ошибка", str(e))
    
    def update_users_list(self, users):
        """Обновление списка пользователей"""
        # Очистка текущего списка
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Добавление новых данных
        for user in users:
            self.tree.insert("", tk.END, values=(user.name, user.email, user.age))

class UserController:
    """Контроллер для управления взаимодействием"""
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.model.attach_observer(self.view)
    
    def add_user(self, user):
        """Добавление пользователя через контроллер"""
        self.model.add_user(user)

class MVCPatternDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("MVC Pattern Demo")
        self.root.geometry("700x500")
        
        # Создание компонентов MVC
        model = UserModel()
        view = UserView(self.root, None)  # Временно None, контроллер создадим позже
        controller = UserController(model, view)
        
        # Назначение контроллера во view
        view.controller = controller
        
        # Инициализация данных
        view.update_users_list(model.get_users())

# root = tk.Tk()
# app = MVCPatternDemo(root)
# root.mainloop()
```

### Паттерн MVP (Model-View-Presenter)

MVP - это архитектурный паттерн, который отделяет логику представления от логики пользовательского интерфейса.

```python
from abc import ABC, abstractmethod

class IUserView(ABC):
    """Интерфейс представления для MVP"""
    
    @abstractmethod
    def display_users(self, users):
        pass
    
    @abstractmethod
    def get_user_data(self):
        pass
    
    @abstractmethod
    def show_message(self, message):
        pass

class UserPresenter:
    """Презентер для MVP паттерна"""
    
    def __init__(self, model, view):
        self.model = model
        self.view = view
    
    def load_users(self):
        """Загрузка и отображение пользователей"""
        users = self.model.get_users()
        self.view.display_users(users)
    
    def add_user(self):
        """Добавление пользователя"""
        try:
            user_data = self.view.get_user_data()
            user = User(user_data['name'], user_data['email'], user_data['age'])
            self.model.add_user(user)
            self.load_users()  # Обновляем отображение
            self.view.show_message("Пользователь успешно добавлен")
        except ValueError as e:
            self.view.show_message(f"Ошибка: {str(e)}")

class MVPUserView(IUserView):
    """Реализация интерфейса IUserView"""
    
    def __init__(self, root):
        self.root = root
        self.presenter = None  # Будет установлен позже
        
        # Создание интерфейса
        self.frame = ttk.Frame(root)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Таблица пользователей
        columns = ("Имя", "Email", "Возраст")
        self.tree = ttk.Treeview(self.frame, columns=columns, show="headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Прокрутка
        tree_scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Форма ввода
        self.create_input_form()
    
    def create_input_form(self):
        input_frame = ttk.LabelFrame(self.frame, text="Добавить пользователя")
        input_frame.pack(fill=tk.X, pady=10)
        
        fields = ["Имя", "Email", "Возраст"]
        self.entries = {}
        
        for i, field in enumerate(fields):
            ttk.Label(input_frame, text=field).grid(row=0, column=i*2, sticky="w", padx=(5, 5), pady=5)
            entry = ttk.Entry(input_frame, width=20)
            entry.grid(row=0, column=i*2+1, padx=(0, 15), pady=5)
            self.entries[field.lower()] = entry
        
        add_btn = ttk.Button(input_frame, text="Добавить", command=self.add_user)
        add_btn.grid(row=0, column=6, padx=5, pady=5)
    
    def display_users(self, users):
        # Очистка текущего списка
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Добавление новых данных
        for user in users:
            self.tree.insert("", tk.END, values=(user.name, user.email, user.age))
    
    def get_user_data(self):
        data = {}
        for field, entry in self.entries.items():
            data[field] = entry.get()
        
        # Проверка данных
        if not data['name'] or not data['email'] or not data['age']:
            raise ValueError("Все поля обязательны для заполнения")
        
        try:
            data['age'] = int(data['age'])
        except ValueError:
            raise ValueError("Возраст должен быть числом")
        
        return data
    
    def show_message(self, message):
        from tkinter import messagebox
        messagebox.showinfo("Информация", message)
    
    def add_user(self):
        if self.presenter:
            self.presenter.add_user()

class MVPPatternDemo:
    """Демонстрация MVP паттерна"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("MVP Pattern Demo")
        self.root.geometry("700x500")
        
        # Создание компонентов MVP
        model = UserModel()
        view = MVPUserView(self.root)
        presenter = UserPresenter(model, view)
        
        # Назначение презентера в представление
        view.presenter = presenter
        
        # Загрузка начальных данных
        presenter.load_users()

# root = tk.Tk()
# app = MVPPatternDemo(root)
# root.mainloop()
```

---

## 3. Многопоточность в Tkinter

### Проблемы GUI и многопоточности

При работе с GUI-приложениями важно помнить, что все изменения интерфейса должны происходить в основном потоке (GUI-потоке). Работа с многопоточностью требует специальных подходов.

```python
import threading
import time
from tkinter import messagebox

class ThreadingDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Многопоточность в Tkinter")
        self.root.geometry("700x500")
        
        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Текстовая область для вывода
        self.output_text = tk.Text(main_frame, height=15, width=70)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.output_text.yview)
        self.output_text.configure(yscrollcommand=scrollbar.set)
        
        self.output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Кнопки управления
        button_frame = ttk.Frame(root)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Запустить задачу в потоке", 
                  command=self.start_background_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Очистить вывод", 
                  command=lambda: self.output_text.delete(1.0, tk.END)).pack(side=tk.LEFT, padx=5)
        
        # Прогресс бар
        self.progress = ttk.Progressbar(root, mode="indeterminate")
        self.progress.pack(fill=tk.X, padx=10, pady=5)
    
    def start_background_task(self):
        """Запуск задачи в фоновом потоке"""
        # Запуск потока
        thread = threading.Thread(target=self.background_task, daemon=True)
        thread.start()
    
    def background_task(self):
        """Фоновая задача"""
        # Начало задачи в отдельном потоке
        self.update_output("Начало фоновой задачи...\n")
        
        for i in range(10):
            time.sleep(0.5)  # Имитация работы
            self.update_output(f"Шаг {i+1} фоновой задачи\n")
        
        self.update_output("Фоновая задача завершена!\n")
    
    def update_output(self, text):
        """Обновление текстовой области (должно выполняться в GUI-потоке)"""
        # Используем after для выполнения в GUI-потоке
        self.root.after(0, lambda: self.output_text.insert(tk.END, text))
        self.root.after(0, lambda: self.output_text.see(tk.END))  # Прокрутка к концу

# root = tk.Tk()
# app = ThreadingDemo(root)
# root.mainloop()
```

### Использование concurrent.futures

```python
from concurrent.futures import ThreadPoolExecutor
import requests  # Для примера сетевых запросов

class ConcurrentDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Concurrent.futures в Tkinter")
        self.root.geometry("800x600")
        
        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Поле ввода URL
        url_frame = ttk.Frame(main_frame)
        url_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(url_frame, text="URL:").pack(side=tk.LEFT)
        self.url_entry = ttk.Entry(url_frame, width=50)
        self.url_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.url_entry.insert(0, "https://httpbin.org/delay/1")  # Пример URL для тестирования
        
        # Кнопки
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Выполнить один запрос", 
                  command=self.single_request).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Выполнить несколько запросов", 
                  command=self.multiple_requests).pack(side=tk.LEFT, padx=5)
        
        # Текстовая область для вывода
        self.result_text = tk.Text(main_frame, height=20, width=80)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Прогресс бар
        self.progress = ttk.Progressbar(root, mode="determinate")
        self.progress.pack(fill=tk.X, padx=10, pady=5)
    
    def single_request(self):
        """Выполнение одного сетевого запроса в потоке"""
        url = self.url_entry.get()
        if not url:
            messagebox.showerror("Ошибка", "Введите URL")
            return
        
        # Выполнение запроса в отдельном потоке
        thread = threading.Thread(target=self._perform_single_request, args=(url,))
        thread.start()
    
    def _perform_single_request(self, url):
        """Выполнение одного запроса"""
        try:
            self.root.after(0, lambda: self.result_text.insert(tk.END, f"Запрос к {url}...\n"))
            
            response = requests.get(url, timeout=10)
            
            self.root.after(0, lambda: self.result_text.insert(
                tk.END, f"Ответ от {url}: статус {response.status_code}, длина {len(response.content)} байт\n"))
        except Exception as e:
            self.root.after(0, lambda: self.result_text.insert(tk.END, f"Ошибка запроса к {url}: {str(e)}\n"))
    
    def multiple_requests(self):
        """Выполнение нескольких сетевых запросов с использованием ThreadPoolExecutor"""
        urls = [
            "https://httpbin.org/delay/1",
            "https://httpbin.org/delay/2", 
            "https://httpbin.org/delay/1",
            "https://httpbin.org/status/200"
        ]
        
        # Выполнение запросов в пуле потоков
        thread = threading.Thread(target=self._perform_multiple_requests, args=(urls,))
        thread.start()
    
    def _perform_multiple_requests(self, urls):
        """Выполнение нескольких запросов"""
        self.root.after(0, lambda: self.progress.config(value=0, maximum=len(urls)))
        
        with ThreadPoolExecutor(max_workers=3) as executor:
            # Выполняем запросы асинхронно
            futures = [executor.submit(requests.get, url, {"timeout": 10}) for url in urls]
            
            for i, future in enumerate(futures):
                try:
                    response = future.result()  # Блокирует до завершения задачи
                    self.root.after(0, lambda r=response, u=urls[i]: 
                                   self.result_text.insert(
                                       tk.END, 
                                       f"Ответ от {u}: статус {r.status_code}, длина {len(r.content)} байт\n"))
                except Exception as e:
                    self.root.after(0, lambda err=str(e), u=urls[i]: 
                                   self.result_text.insert(tk.END, f"Ошибка запроса к {u}: {err}\n"))
                
                # Обновляем прогресс
                self.root.after(0, lambda val=i+1: self.progress.step())
        
        self.root.after(0, lambda: self.result_text.insert(tk.END, "Все запросы завершены\n"))

# root = tk.Tk()
# app = ConcurrentDemo(root)
# root.mainloop()
```

---

## 4. Пользовательские виджеты

### Создание составного виджета

```python
class CustomInputWidget:
    """Пользовательский виджет ввода с меткой и полем"""
    
    def __init__(self, parent, label_text="Поле:", initial_value=""):
        self.frame = ttk.Frame(parent)
        
        # Метка
        self.label = ttk.Label(self.frame, text=label_text)
        self.label.pack(side=tk.LEFT, padx=(0, 5))
        
        # Поле ввода
        self.entry = ttk.Entry(self.frame)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.insert(0, initial_value)
        
        # Кнопка очистки
        self.clear_btn = ttk.Button(self.frame, text="×", width=3, 
                                   command=self.clear, state="disabled")
        self.clear_btn.pack(side=tk.LEFT, padx=(5, 0))
        
        # Отслеживание изменений
        self.entry.bind("<KeyRelease>", self.on_entry_change)
        self.entry.bind("<FocusIn>", self.on_focus_in)
        self.entry.bind("<FocusOut>", self.on_focus_out)
    
    def on_entry_change(self, event):
        """Обработка изменения текста"""
        if self.entry.get():
            self.clear_btn.config(state="normal")
        else:
            self.clear_btn.config(state="disabled")
    
    def on_focus_in(self, event):
        """Обработка получения фокуса"""
        self.label.config(foreground="blue")
    
    def on_focus_out(self, event):
        """Обработка потери фокуса"""
        self.label.config(foreground="black")
    
    def clear(self):
        """Очистка поля ввода"""
        self.entry.delete(0, tk.END)
        self.clear_btn.config(state="disabled")
    
    def get(self):
        """Получение значения из поля ввода"""
        return self.entry.get()
    
    def set(self, value):
        """Установка значения в поле ввода"""
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)
    
    def pack(self, **kwargs):
        """Упаковка виджета"""
        self.frame.pack(**kwargs)

class CustomButton:
    """Пользовательская кнопка с дополнительными возможностями"""
    
    def __init__(self, parent, text, command=None, default=False):
        self.frame = ttk.Frame(parent)
        
        # Кнопка
        self.button = ttk.Button(self.frame, text=text, command=self._on_click)
        self.button.pack(side=tk.LEFT)
        
        # Индикатор загрузки
        self.loading_indicator = ttk.Label(self.frame, text="⏳", visible=False)
        
        # Сохранение оригинальной команды
        self.command = command
        self.default = default
        
        # Привязка клавиши Enter к кнопке по умолчанию
        if self.default:
            self.frame.bind("<Return>", lambda e: self._on_click())
    
    def _on_click(self):
        """Обработка нажатия кнопки"""
        if self.command:
            # Показываем индикатор загрузки
            self.loading_indicator.pack(side=tk.LEFT, padx=(5, 0))
            self.button.config(state="disabled")
            
            # Выполняем команду
            try:
                result = self.command()
                return result
            finally:
                # Скрываем индикатор загрузки
                self.loading_indicator.pack_forget()
                self.button.config(state="normal")
    
    def pack(self, **kwargs):
        """Упаковка виджета"""
        self.frame.pack(**kwargs)

class CustomWidgetDemo:
    """Демонстрация пользовательских виджетов"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Пользовательские виджеты")
        self.root.geometry("700x500")
        
        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Заголовок
        title = ttk.Label(main_frame, text="Пользовательские виджеты", font=("Arial", 16, "bold"))
        title.pack(pady=10)
        
        # Использование пользовательского виджета ввода
        name_widget = CustomInputWidget(main_frame, "Имя:", "Иван Иванов")
        name_widget.pack(fill=tk.X, pady=5)
        
        email_widget = CustomInputWidget(main_frame, "Email:", "ivan@example.com")
        email_widget.pack(fill=tk.X, pady=5)
        
        age_widget = CustomInputWidget(main_frame, "Возраст:", "30")
        age_widget.pack(fill=tk.X, pady=5)
        
        # Использование пользовательской кнопки
        def submit_action():
            name = name_widget.get()
            email = email_widget.get()
            age = age_widget.get()
            messagebox.showinfo("Данные", f"Имя: {name}\nEmail: {email}\nВозраст: {age}")
        
        submit_btn = CustomButton(main_frame, "Отправить", submit_action, default=True)
        submit_btn.pack(pady=20)
        
        # Кнопка для получения значений
        def show_values():
            values = {
                "Имя": name_widget.get(),
                "Email": email_widget.get(),
                "Возраст": age_widget.get()
            }
            messagebox.showinfo("Значения", f"Текущие значения:\n{values}")
        
        show_btn = CustomButton(main_frame, "Показать значения", show_values)
        show_btn.pack(pady=5)

# root = tk.Tk()
# app = CustomWidgetDemo(root)
# root.mainloop()
```

---

## 5. Работа с изображениями

### Использование PhotoImage

```python
class ImageHandlingDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Работа с изображениями")
        self.root.geometry("800x600")
        
        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Заголовок
        title = ttk.Label(main_frame, text="Демонстрация работы с изображениями", 
                         font=("Arial", 14, "bold"))
        title.pack(pady=10)
        
        # Canvas для отображения изображений
        self.canvas = tk.Canvas(main_frame, bg="lightgray", width=600, height=400)
        self.canvas.pack(pady=10)
        
        # Попытка загрузить и отобразить изображение
        self.load_and_display_image()
        
        # Кнопки управления
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Загрузить изображение", 
                  command=self.select_and_load_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Очистить", 
                  command=lambda: self.canvas.delete("all")).pack(side=tk.LEFT, padx=5)
    
    def load_and_display_image(self):
        """Загрузка и отображение изображения"""
        try:
            # В реальном приложении здесь будет загрузка реального изображения
            # Для демонстрации создадим простую графику
            self.canvas.create_text(300, 200, 
                                   text="Здесь будет отображено изображение", 
                                   font=("Arial", 16), fill="navy")
            
            # Добавим простую графику для визуализации
            self.canvas.create_rectangle(100, 100, 200, 150, fill="red", outline="black")
            self.canvas.create_oval(250, 100, 350, 150, fill="green", outline="black")
            self.canvas.create_polygon(400, 100, 450, 150, 350, 150, fill="blue", outline="black")
        except Exception as e:
            print(f"Ошибка при отображении изображения: {e}")
    
    def select_and_load_image(self):
        """Выбор и загрузка изображения из файла"""
        from tkinter import filedialog
        
        file_path = filedialog.askopenfilename(
            title="Выберите изображение",
            filetypes=[
                ("Изображения", "*.png *.jpg *.jpeg *.gif *.bmp"),
                ("PNG файлы", "*.png"),
                ("JPG файлы", "*.jpg"),
                ("Все файлы", "*.*")
            ]
        )
        
        if file_path:
            try:
                # Загрузка изображения
                from PIL import Image, ImageTk  # pip install Pillow
                
                image = Image.open(file_path)
                image.thumbnail((600, 400))  # Масштабирование до размера Canvas
                photo = ImageTk.PhotoImage(image)
                
                # Сохраняем ссылку на изображение, чтобы оно не было удалено сборщиком мусора
                self.image_reference = photo
                
                # Отображение изображения
                self.canvas.delete("all")  # Очистка Canvas
                self.canvas.create_image(300, 200, image=photo)  # Центрирование изображения
                
            except ImportError:
                messagebox.showerror("Ошибка", "Для работы с изображениями установите Pillow:\npip install Pillow")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить изображение:\n{str(e)}")

# root = tk.Tk()
# app = ImageHandlingDemo(root)
# root.mainloop()
```

---

## 6. Практические примеры

### Пример 1: Калькулятор

```python
class Calculator:
    """Простой калькулятор с GUI"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор")
        self.root.geometry("400x500")
        
        self.current = "0"
        self.previous = ""
        self.operator = ""
        self.reset_next_input = False
        
        self.create_display()
        self.create_buttons()
    
    def create_display(self):
        """Создание дисплея калькулятора"""
        display_frame = ttk.Frame(self.root)
        display_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.display_var = tk.StringVar(value=self.current)
        display = ttk.Entry(display_frame, textvariable=self.display_var, 
                          font=("Arial", 20), justify="right", state="readonly")
        display.pack(fill=tk.X)
    
    def create_buttons(self):
        """Создание кнопок калькулятора"""
        buttons_frame = ttk.Frame(self.root)
        buttons_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Определение кнопок
        buttons = [
            ("C", 1, 0), ("±", 1, 1), ("%", 1, 2), ("÷", 1, 3),
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("×", 2, 3),
            ("4", 3, 0), ("5", 3, 1), ("6", 3, 2), ("-", 3, 3),
            ("1", 4, 0), ("2", 4, 1), ("3", 4, 2), ("+", 4, 3),
            ("0", 5, 0), (".", 5, 2), ("=", 5, 3)
        ]
        
        for (text, row, col) in buttons:
            if text == "0":
                # Кнопка 0 занимает 2 колонки
                btn = ttk.Button(
                    buttons_frame, 
                    text=text, 
                    command=lambda t=text: self.button_click(t)
                )
                btn.grid(row=row, column=col, columnspan=2, sticky="nsew", padx=2, pady=2)
            elif text == ".":
                btn = ttk.Button(
                    buttons_frame, 
                    text=text, 
                    command=lambda t=text: self.button_click(t)
                )
                btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
            elif text == "=":
                btn = ttk.Button(
                    buttons_frame, 
                    text=text, 
                    command=lambda t=text: self.button_click(t),
                    style="Accent.TButton"
                )
                btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
            else:
                btn = ttk.Button(
                    buttons_frame, 
                    text=text, 
                    command=lambda t=text: self.button_click(t)
                )
                btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
        
        # Настройка растягивания сетки
        for i in range(6):
            buttons_frame.rowconfigure(i, weight=1)
        for j in range(4):
            buttons_frame.columnconfigure(j, weight=1)
    
    def button_click(self, value):
        """Обработка нажатия кнопки"""
        if value.isdigit() or value == ".":
            self.input_number(value)
        elif value in "+-×÷":
            self.input_operator(value)
        elif value == "=":
            self.calculate()
        elif value == "C":
            self.clear()
        elif value == "±":
            self.change_sign()
        elif value == "%":
            self.percentage()
    
    def input_number(self, number):
        """Ввод числа"""
        if self.reset_next_input:
            self.current = "0"
            self.reset_next_input = False
        
        if self.current == "0" and number != ".":
            self.current = number
        elif number == "." and "." not in self.current:
            self.current += number
        elif number != ".":
            self.current += number
        
            "Title.TLabel",
            font=("Arial", 16, "bold"),
            foreground="purple"
        )
        
        # Стиль для рамок
        self.style.configure(
            "Custom.TFrame",
            background="lightgray",
            relief="raised",
            borderwidth=2
        )
    
    def create_styled_widgets(self):
        # Создание отдельной вкладки для пользовательских стилей
        styled_frame = ttk.LabelFrame(self.root, text="Пользовательские стили", padding=20)
        styled_frame.pack(fill="x", padx=10, pady=10)
        
        # Использование пользовательских стилей
        title = ttk.Label(styled_frame, text="Стилизованные виджеты", style="Title.TLabel")
        title.pack(pady=10)
        
        # Кнопки с разными стилями
        button_frame = ttk.Frame(styled_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Обычная кнопка", style="Custom.TButton").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Опасное действие", style="Danger.TButton").pack(side="left", padx=5)
        ttk.Button(button_frame, text="Успешное действие", style="Success.TButton").pack(side="left", padx=5)
        
        # Стилизованные флажки
        check_frame = ttk.LabelFrame(styled_frame, text="Флажки", padding=10)
        check_frame.pack(fill="x", pady=10)
        
        # Создание пользовательского стиля для флажков
        self.style.configure("Custom.TCheckbutton", font=("Arial", 12))
        
        ttk.Checkbutton(check_frame, text="Опция 1").pack(anchor="w", pady=2)
        ttk.Checkbutton(check_frame, text="Опция 2").pack(anchor="w", pady=2)
        ttk.Checkbutton(check_frame, text="Опция 3").pack(anchor="w", pady=2)
        
        # Прогресс бары с разными стилями
        progress_frame = ttk.LabelFrame(styled_frame, text="Прогресс бары", padding=10)
        progress_frame.pack(fill="x", pady=10)
        
        # Определение нового элемента стиля для прогресс бара
        self.style.element_create("custom.trough", "from", "clam")
        self.style.layout("Custom.Horizontal.TProgressbar",
            [('custom.trough', {'children':
                [('Horizontal.pbar', {'side': 'left', 'sticky': 'ns'})],
            'sticky': 'nswe'})])
        self.style.configure("Custom.Horizontal.TProgressbar", thickness=20)
        
        ttk.Progressbar(progress_frame, mode="determinate", value=75).pack(fill="x", pady=5)
        ttk.Progressbar(progress_frame, mode="indeterminate").pack(fill="x", pady=5)
        progress = ttk.Progressbar(progress_frame, mode="determinate", length=300)
        progress.pack(pady=5)
        progress.start(10)
    
    def change_theme(self, theme_name):
        """Изменение темы приложения"""
        try:
            self.style.theme_use(theme_name)
            # Обновляем все виджеты
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Widget):
                    widget.update()
        except tk.TclError:
            print(f"Тема {theme_name} не найдена")

root = tk.Tk()
app = StylingAndThemes(root)
root.mainloop()
```

---

## 6. Практические примеры

### Пример 1: Калькулятор с продвинутыми возможностями

```python
import tkinter as tk
from tkinter import ttk, messagebox
import math

class AdvancedCalculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Продвинутый калькулятор")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        
        # Переменные состояния
        self.current = "0"
        self.previous = ""
        self.operator = ""
        self.total = 0
        self.memory = 0
        
        self.create_widgets()
        self.setup_bindings()
    
    def create_widgets(self):
        # Дисплей
        display_frame = tk.Frame(self.root, bg="black")
        display_frame.pack(fill="x", padx=5, pady=5)
        
        self.display_var = tk.StringVar(value="0")
        display = tk.Label(
            display_frame,
            textvariable=self.display_var,
            anchor="e",
            bg="black",
            fg="white",
            font=("Digital-7", 24),
            padx=10,
            pady=10
        )
        display.pack(fill="x")
        
        # Кнопки памяти
        memory_frame = tk.Frame(self.root)
        memory_frame.pack(fill="x", padx=5, pady=2)
        
        tk.Button(memory_frame, text="MC", command=self.memory_clear, width=5).pack(side="left", padx=2)
        tk.Button(memory_frame, text="MR", command=self.memory_recall, width=5).pack(side="left", padx=2)
        tk.Button(memory_frame, text="M+", command=self.memory_add, width=5).pack(side="left", padx=2)
        tk.Button(memory_frame, text="M-", command=self.memory_subtract, width=5).pack(side="left", padx=2)
        tk.Button(memory_frame, text="MS", command=self.memory_store, width=5).pack(side="left", padx=2)
        
        # Кнопки функций
        functions_frame = tk.Frame(self.root)
        functions_frame.pack(fill="x", padx=5, pady=2)
        
        functions = [
            ("√", self.sqrt), ("x²", self.square), ("xʸ", lambda: self.set_op("**")),
            ("1/x", self.reciprocal), ("±", self.change_sign), ("C", self.clear),
            ("CE", self.clear_entry), ("⌫", self.backspace), ("%", self.percent)
        ]
        
        for i, (text, command) in enumerate(functions):
            col = i % 3
            row = i // 3
            btn = tk.Button(functions_frame, text=text, command=command, height=2)
            btn.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
            functions_frame.grid_columnconfigure(col, weight=1)
        
        # Основная панель кнопок
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Кнопки операций
        ops_frame = tk.Frame(main_frame)
        ops_frame.grid(row=0, column=1, sticky="nsew")
        
        operations = ["÷", "×", "-", "+"]
        for i, op in enumerate(operations):
            btn = tk.Button(ops_frame, text=op, command=lambda o=op: self.set_op(o), height=2)
            btn.pack(fill="x", pady=1)
        
        # Основная сетка кнопок
        buttons_frame = tk.Frame(main_frame)
        buttons_frame.grid(row=0, column=0, sticky="nsew")
        
        # Цифры и основные кнопки
        buttons = [
            ("7", lambda: self.add_digit("7")), ("8", lambda: self.add_digit("8")), ("9", lambda: self.add_digit("9")), ("", None),
            ("4", lambda: self.add_digit("4")), ("5", lambda: self.add_digit("5")), ("6", lambda: self.add_digit("6")), ("", None),
            ("1", lambda: self.add_digit("1")), ("2", lambda: self.add_digit("2")), ("3", lambda: self.add_digit("3")), ("", None),
            ("0", lambda: self.add_digit("0")), (".", self.add_decimal), ("=", self.calculate)
        ]
        
        for i, (text, command) in enumerate(buttons):
            if text:  # Пропускаем пустые кнопки
                row = i // 3
                col = i % 3
                btn = tk.Button(buttons_frame, text=text, command=command, height=2)
                btn.grid(row=row, column=col, sticky="nsew", padx=1, pady=1)
        
        # Настройка растягивания сетки
        for i in range(4):
            main_frame.grid_rowconfigure(i, weight=1)
            main_frame.grid_columnconfigure(i, weight=1)
        for i in range(3):
            buttons_frame.grid_rowconfigure(i, weight=1)
            buttons_frame.grid_columnconfigure(i, weight=1)
    
    def setup_bindings(self):
        # Привязка клавиш калькулятора
        self.root.bind("<Key>", self.key_press)
    
    def key_press(self, event):
        """Обработка нажатий клавиш"""
        key = event.char
        
        if key.isdigit():
            self.add_digit(key)
        elif key in "+-*/.":
            if key == "*":
                self.set_op("×")
            elif key == "/":
                self.set_op("÷")
            else:
                self.set_op(key)
        elif key == "\r":  # Enter
            self.calculate()
        elif key == "\x08":  # Backspace
            self.backspace()
        elif key.lower() == "c":
            self.clear()
    
    def add_digit(self, digit):
        """Добавление цифры"""
        if self.current == "0":
            self.current = digit
        else:
            self.current += digit
        self.display_var.set(self.current)
    
    def add_decimal(self):
        """Добавление десятичной точки"""
        if "." not in self.current:
            self.current += "."
        self.display_var.set(self.current)
    
    def set_op(self, op):
        """Установка операции"""
        if self.operator and self.previous:
            self.calculate()
        
        self.previous = self.current
        self.operator = op
        self.current = "0"
    
    def calculate(self):
        """Выполнение вычисления"""
        try:
            if self.operator == "+":
                self.total = float(self.previous) + float(self.current)
            elif self.operator == "-":
                self.total = float(self.previous) - float(self.current)
            elif self.operator == "×":
                self.total = float(self.previous) * float(self.current)
            elif self.operator == "÷":
                if float(self.current) == 0:
                    raise ZeroDivisionError("Деление на ноль")
                self.total = float(self.previous) / float(self.current)
            elif self.operator == "**":
                self.total = float(self.previous) ** float(self.current)
            
            self.current = str(self.total)
            self.display_var.set(self.current)
            self.operator = ""
            self.previous = ""
        except ZeroDivisionError:
            messagebox.showerror("Ошибка", "Деление на ноль невозможно!")
            self.clear()
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка вычисления: {str(e)}")
            self.clear()
    
    def sqrt(self):
        """Квадратный корень"""
        try:
            result = math.sqrt(float(self.current))
            self.current = str(result)
            self.display_var.set(self.current)
        except ValueError:
            messagebox.showerror("Ошибка", "Невозможно вычислить корень из отрицательного числа")
    
    def square(self):
        """Квадрат числа"""
        result = float(self.current) ** 2
        self.current = str(result)
        self.display_var.set(self.current)
    
    def reciprocal(self):
        """Обратное число (1/x)"""
        try:
            result = 1 / float(self.current)
            self.current = str(result)
            self.display_var.set(self.current)
        except ZeroDivisionError:
            messagebox.showerror("Ошибка", "Деление на ноль невозможно")
    
    def percent(self):
        """Процент"""
        result = float(self.current) / 100
        self.current = str(result)
        self.display_var.set(self.current)
    
    def change_sign(self):
        """Изменение знака"""
        if self.current.startswith("-"):
            self.current = self.current[1:]
        else:
            self.current = "-" + self.current
        self.display_var.set(self.current)
    
    def clear(self):
        """Очистка всего"""
        self.current = "0"
        self.previous = ""
        self.operator = ""
        self.total = 0
        self.display_var.set(self.current)
    
    def clear_entry(self):
        """Очистка текущего ввода"""
        self.current = "0"
        self.display_var.set(self.current)
    
    def backspace(self):
        """Удаление последнего символа"""
        if len(self.current) > 1:
            self.current = self.current[:-1]
        else:
            self.current = "0"
        self.display_var.set(self.current)
    
    # Функции памяти
    def memory_clear(self):
        self.memory = 0
    
    def memory_recall(self):
        self.current = str(self.memory)
        self.display_var.set(self.current)
    
    def memory_add(self):
        self.memory += float(self.current)
    
    def memory_subtract(self):
        self.memory -= float(self.current)
    
    def memory_store(self):
        self.memory = float(self.current)
    
    def run(self):
        self.root.mainloop()

# Запуск калькулятора
if __name__ == "__main__":
    calc = AdvancedCalculator()
    calc.run()
```

### Пример 2: Многооконное приложение

```python
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
import os

class MultiWindowApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Многооконное приложение")
        self.root.geometry("800x600")
        
        # Данные приложения
        self.app_data = {
            "settings": {
                "theme": "default",
                "language": "ru",
                "auto_save": True
            },
            "documents": [],
            "current_doc_index": -1
        }
        
        self.setup_main_window()
    
    def setup_main_window(self):
        # Меню
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Файл
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Новый", command=self.new_document, accelerator="Ctrl+N")
        file_menu.add_command(label="Открыть", command=self.open_document, accelerator="Ctrl+O")
        file_menu.add_command(label="Сохранить", command=self.save_document, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Настройки", command=self.open_settings)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.exit_app)
        
        # Вид
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Вид", menu=view_menu)
        view_menu.add_command(label="Открыть проводник", command=self.open_explorer)
        view_menu.add_command(label="Открыть консоль", command=self.open_console)
        
        # Создание панели инструментов
        toolbar = tk.Frame(self.root, bg="lightgray", height=40)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        tk.Button(toolbar, text="Новый", command=self.new_document).pack(side=tk.LEFT, padx=2, pady=5)
        tk.Button(toolbar, text="Открыть", command=self.open_document).pack(side=tk.LEFT, padx=2, pady=5)
        tk.Button(toolbar, text="Сохранить", command=self.save_document).pack(side=tk.LEFT, padx=2, pady=5)
        
        # Основная рабочая область
        self.work_area = tk.Frame(self.root)
        self.work_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Создание начального интерфейса
        self.show_welcome_screen()
        
        # Привязка горячих клавиш
        self.root.bind('<Control-n>', lambda e: self.new_document())
        self.root.bind('<Control-o>', lambda e: self.open_document())
        self.root.bind('<Control-s>', lambda e: self.save_document())
    
    def show_welcome_screen(self):
        """Показ приветственного экрана"""
        for widget in self.work_area.winfo_children():
            widget.destroy()
        
        welcome_frame = tk.Frame(self.work_area)
        welcome_frame.pack(expand=True)
        
        tk.Label(welcome_frame, text="Добро пожаловать!", font=("Arial", 24)).pack(pady=20)
        tk.Label(welcome_frame, text="Выберите действие:", font=("Arial", 14)).pack(pady=10)
        
        button_frame = tk.Frame(welcome_frame)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Создать документ", command=self.new_document, width=20).pack(pady=5)
        tk.Button(button_frame, text="Открыть документ", command=self.open_document, width=20).pack(pady=5)
        tk.Button(button_frame, text="Настройки", command=self.open_settings, width=20).pack(pady=5)
    
    def new_document(self):
        """Создание нового документа"""
        # Создаем новое окно для документа
        doc_window = tk.Toplevel(self.root)
        doc_window.title("Новый документ")
        doc_window.geometry("700x500")
        
        # Текстовая область
        text_frame = tk.Frame(doc_window)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        text_area = tk.Text(text_frame, wrap=tk.WORD)
        scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_area.yview)
        text_area.configure(yscrollcommand=scrollbar.set)
        
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Добавляем документ в список
        doc_info = {
            "window": doc_window,
            "text_area": text_area,
            "path": None,
            "modified": False
        }
        self.app_data["documents"].append(doc_info)
        self.app_data["current_doc_index"] = len(self.app_data["documents"]) - 1
        
        # Привязка события изменения текста
        text_area.bind("<<Modified>>", lambda e: self.on_doc_modified(doc_info))
        
        # Кнопки управления документом
        button_frame = tk.Frame(doc_window)
        button_frame.pack(fill=tk.X, pady=5)
        
        tk.Button(button_frame, text="Сохранить", command=lambda: self.save_specific_document(doc_info)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Закрыть", command=lambda: self.close_document(doc_info)).pack(side=tk.LEFT, padx=5)
    
    def open_document(self):
        """Открытие документа"""
        file_path = filedialog.askopenfilename(
            title="Открыть документ",
            filetypes=[("Текстовые файлы", "*.txt"), ("Python файлы", "*.py"), ("Все файлы", "*.*")]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                # Создаем окно для открытого документа
                doc_window = tk.Toplevel(self.root)
                doc_window.title(f"Документ - {os.path.basename(file_path)}")
                doc_window.geometry("700x500")
                
                # Текстовая область
                text_frame = tk.Frame(doc_window)
                text_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
                
                text_area = tk.Text(text_frame, wrap=tk.WORD)
                scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_area.yview)
                text_area.configure(yscrollcommand=scrollbar.set)
                
                text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                
                # Вставляем содержимое файла
                text_area.insert("1.0", content)
                text_area.edit_modified(False)  # Сбрасываем флаг изменения
                
                # Добавляем документ в список
                doc_info = {
                    "window": doc_window,
                    "text_area": text_area,
                    "path": file_path,
                    "modified": False
                }
                self.app_data["documents"].append(doc_info)
                self.app_data["current_doc_index"] = len(self.app_data["documents"]) - 1
                
                # Привязка события изменения текста
                text_area.bind("<<Modified>>", lambda e: self.on_doc_modified(doc_info))
                
                # Кнопки управления документом
                button_frame = tk.Frame(doc_window)
                button_frame.pack(fill=tk.X, pady=5)
                
                tk.Button(button_frame, text="Сохранить", command=lambda: self.save_specific_document(doc_info)).pack(side=tk.LEFT, padx=5)
                tk.Button(button_frame, text="Сохранить как", command=lambda: self.save_as_document(doc_info)).pack(side=tk.LEFT, padx=5)
                tk.Button(button_frame, text="Закрыть", command=lambda: self.close_document(doc_info)).pack(side=tk.LEFT, padx=5)
                
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось открыть файл:\n{str(e)}")
    
    def save_document(self):
        """Сохранение текущего документа"""
        if self.app_data["current_doc_index"] >= 0:
            current_doc = self.app_data["documents"][self.app_data["current_doc_index"]]
            self.save_specific_document(current_doc)
    
    def save_specific_document(self, doc_info):
        """Сохранение конкретного документа"""
        if doc_info["path"]:
            # Сохраняем в существующий файл
            try:
                content = doc_info["text_area"].get("1.0", tk.END + "-1c")  # -1c удаляет последний символ новой строки
                with open(doc_info["path"], 'w', encoding='utf-8') as file:
                    file.write(content)
                
                doc_info["modified"] = False
                doc_info["text_area"].edit_modified(False)
                messagebox.showinfo("Сохранение", "Документ успешно сохранен!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")
        else:
            # Предлагаем выбрать место для сохранения
            self.save_as_document(doc_info)
    
    def save_as_document(self, doc_info):
        """Сохранение документа с выбором пути"""
        file_path = filedialog.asksaveasfilename(
            title="Сохранить документ как",
            defaultextension=".txt",
            filetypes=[("Текстовые файлы", "*.txt"), ("Python файлы", "*.py"), ("Все файлы", "*.*")]
        )
        
        if file_path:
            try:
                content = doc_info["text_area"].get("1.0", tk.END + "-1c")
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                
                doc_info["path"] = file_path
                doc_info["modified"] = False
                doc_info["text_area"].edit_modified(False)
                
                # Обновляем заголовок окна
                doc_info["window"].title(f"Документ - {os.path.basename(file_path)}")
                
                messagebox.showinfo("Сохранение", "Документ успешно сохранен!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")
    
    def on_doc_modified(self, doc_info):
        """Обработка изменения документа"""
        if doc_info["text_area"].edit_modified():
            doc_info["modified"] = True
            # Добавляем * к заголовку окна
            if not doc_info["window"].title().endswith("*"):
                doc_info["window"].title(doc_info["window"].title() + " *")
    
    def close_document(self, doc_info):
        """Закрытие документа"""
        if doc_info["modified"]:
            result = messagebox.askyesnocancel("Сохранить изменения", "Сохранить изменения перед закрытием?")
            if result:
                self.save_specific_document(doc_info)
                if doc_info["modified"]:  # Если все еще несохраненные изменения
                    return  # Пользователь отменил сохранение
            elif result is None:
                return  # Отмена закрытия
        
        # Удаляем документ из списка
        self.app_data["documents"].remove(doc_info)
        doc_info["window"].destroy()
    
    def open_settings(self):
        """Открытие окна настроек"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Настройки")
        settings_window.geometry("400x300")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Создание вкладок для разных настроек
        notebook = ttk.Notebook(settings_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Вкладка общих настроек
        general_frame = ttk.Frame(notebook)
        notebook.add(general_frame, text="Общие")
        
        tk.Label(general_frame, text="Тема интерфейса:").pack(anchor="w", padx=10, pady=5)
        theme_var = tk.StringVar(value=self.app_data["settings"]["theme"])
        theme_combo = ttk.Combobox(general_frame, textvariable=theme_var, 
                                  values=["default", "clam", "alt", "classic"])
        theme_combo.pack(padx=10, pady=5)
        
        tk.Label(general_frame, text="Язык:").pack(anchor="w", padx=10, pady=(10, 5))
        lang_var = tk.StringVar(value=self.app_data["settings"]["language"])
        lang_combo = ttk.Combobox(general_frame, textvariable=lang_var, 
                                 values=["ru", "en", "de"])
        lang_combo.pack(padx=10, pady=5)
        
        auto_save_var = tk.BooleanVar(value=self.app_data["settings"]["auto_save"])
        auto_save_check = ttk.Checkbutton(general_frame, text="Автосохранение", 
                                         variable=auto_save_var)
        auto_save_check.pack(anchor="w", padx=10, pady=10)
        
        # Кнопки OK и Cancel
        button_frame = tk.Frame(settings_window)
        button_frame.pack(fill=tk.X, pady=10)
        
        def save_settings():
            self.app_data["settings"]["theme"] = theme_var.get()
            self.app_data["settings"]["language"] = lang_var.get()
            self.app_data["settings"]["auto_save"] = auto_save_var.get()
            settings_window.destroy()
        
        tk.Button(button_frame, text="OK", command=save_settings, width=10).pack(side=tk.RIGHT, padx=5)
        tk.Button(button_frame, text="Отмена", command=settings_window.destroy, width=10).pack(side=tk.RIGHT, padx=5)
    
    def open_explorer(self):
        """Открытие окна проводника"""
        explorer_window = tk.Toplevel(self.root)
        explorer_window.title("Проводник")
        explorer_window.geometry("500x400")
        
        # Создаем Treeview для отображения файловой системы
        tree = ttk.Treeview(explorer_window)
        tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Добавляем корневые диски (для Windows)
        import platform
        if platform.system() == "Windows":
            import string
            drives = [d + ":/" for d in string.ascii_uppercase 
                     if os.path.exists(d + ":")]
        else:
            drives = ["/"]
        
        for drive in drives:
            tree.insert("", "end", drive, text=drive, values=(drive,))
    
    def open_console(self):
        """Открытие окна консоли"""
        console_window = tk.Toplevel(self.root)
        console_window.title("Консоль")
        console_window.geometry("700x300")
        
        # Текстовая область для вывода
        output_frame = tk.Frame(console_window)
        output_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        output_text = tk.Text(output_frame, wrap=tk.WORD, state=tk.DISABLED)
        scrollbar = tk.Scrollbar(output_frame, orient=tk.VERTICAL, command=output_text.yview)
        output_text.configure(yscrollcommand=scrollbar.set)
        
        output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Поле ввода команды
        input_frame = tk.Frame(console_window)
        input_frame.pack(fill=tk.X, pady=5)
        
        tk.Label(input_frame, text="Команда:").pack(anchor="w", padx=5)
        
        command_var = tk.StringVar()
        command_entry = tk.Entry(input_frame, textvariable=command_var)
        command_entry.pack(fill=tk.X, padx=5, pady=5)
        
        def execute_command():
            command = command_var.get()
            if command:
                # Добавляем команду к выводу
                output_text.config(state=tk.NORMAL)
                output_text.insert(tk.END, f"> {command}\n")
                
                try:
                    # Выполняем команду
                    result = eval(command) if command.strip() else ""
                    output_text.insert(tk.END, f"{result}\n")
                except Exception as e:
                    output_text.insert(tk.END, f"Ошибка: {str(e)}\n")
                
                output_text.config(state=tk.DISABLED)
                output_text.see(tk.END)
                command_var.set("")  # Очищаем поле ввода
        
        command_entry.bind("<Return>", lambda e: execute_command())
        tk.Button(input_frame, text="Выполнить", command=execute_command).pack(pady=5)
    
    def exit_app(self):
        """Выход из приложения"""
        # Проверяем несохраненные документы
        unsaved_docs = [doc for doc in self.app_data["documents"] if doc["modified"]]
        
        if unsaved_docs:
            result = messagebox.askyesnocancel("Несохраненные изменения", 
                                            f"Есть {len(unsaved_docs)} несохраненных документов. Сохранить перед выходом?")
            if result:
                for doc in unsaved_docs:
                    self.save_specific_document(doc)
                    if doc["modified"]:  # Если пользователь отменил сохранение
                        return  # Отменяем выход
            elif result is None:
                return  # Отмена выхода
        
        self.root.quit()
    
    def run(self):
        self.root.mainloop()

# Запуск приложения
if __name__ == "__main__":
    app = MultiWindowApp()
    app.run()
```

---

## Заключение

Tkinter предоставляет мощный инструментарий для создания графических интерфейсов в Python. В этой лекции мы рассмотрели продвинутые аспекты:
1. Создание сложных виджетов и компоновок
2. Работа с событиями и привязками
3. Использование стилей и тем
4. Практические примеры приложений

Tkinter особенно полезен для создания настольных приложений, инструментов автоматизации и служебных программ, где не требуется очень современный внешний вид.

## Контрольные вопросы:
1. Какие виджеты Tkinter подходят для отображения иерархических данных?
2. Как создать пользовательский виджет в Tkinter?
3. Какие существуют способы размещения элементов в Tkinter?
4. Как обрабатывать события в Tkinter?
5. Как применять стили к виджетам Tkinter?
