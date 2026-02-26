# Практическое занятие 25: Tkinter - паттерн MVC

## Цель занятия
Изучить паттерн Model-View-Controller (MVC) и его применение при создании приложений с графическим интерфейсом на Tkinter. Научиться разделять логику данных, представление и управление.

## Задачи
1. Освоить структуру MVC
2. Научиться создавать Model, View и Controller
3. Реализовать паттерн Observer для связи компонентов
4. Создать полноценное прилож архиение стектурой MVC

## Ход работы

### 1. Структура MVC

```python
# Model - данные и бизнес-логика
class TaskModel:
    def __init__(self):
        self.tasks = []
        self.observers = []
        
    def add_task(self, task):
        # ВАШ КОД ЗДЕСЬ
        pass
```

---

## 1. Теоретическая часть: Паттерн MVC

### Уровень 1 - Начальный

#### Задание 1.1: Разделение компонентов MVC

Создайте структуру MVC:

```python
class TaskModel:
    """
    Model - хранение данных
    """
    def __init__(self):
        self.tasks = []
        self.observers = []
        
    def add_task(self, task):
        # ВАШ КОД ЗДЕСЬ - добавьте задачу и уведомите наблюдателей
        pass
        
    def add_observer(self, observer):
        # ВАШ КОД ЗДЕСЬ - добавьте наблюдателя
        pass
        
    def notify_observers(self):
        # ВАШ КОД ЗДЕСЬ - уведомите всех наблюдателей
        pass

class TaskView:
    """
    View - отображение интерфейса
    """
    def __init__(self, root, controller):
        # ВАШ КОД ЗДЕСЬ - создайте интерфейс
        pass

class TaskController:
    """
    Controller - обработка событий
    """
    def __init__(self, model, view):
        # ВАШ КОД ЗДЕСЬ - свяжите model и view
        pass
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import tkinter as tk
from tkinter import ttk

class TaskModel:
    def __init__(self):
        self.tasks = []
        self.observers = []
    
    def add_task(self, task):
        self.tasks.append(task)
        self.notify_observers()
    
    def remove_task(self, index):
        task = self.tasks.pop(index)
        self.notify_observers()
        return task
    
    def get_tasks(self):
        return self.tasks.copy()
    
    def add_observer(self, observer):
        self.observers.append(observer)
    
    def notify_observers(self):
        for observer in self.observers:
            observer.update()

class TaskView:
    def __init__(self, root, controller):
        self.controller = controller
        self.frame = ttk.Frame(root, padding="10")
        
        self.listbox = tk.Listbox(self.frame)
        self.listbox.pack(pady=5)
        
        self.entry = ttk.Entry(self.frame)
        self.entry.pack(pady=5)
        
        ttk.Button(self.frame, text="Добавить", 
                  command=self.controller.add_task).pack(pady=5)
        
    def get_input(self):
        return self.entry.get()
    
    def clear_input(self):
        self.entry.delete(0, tk.END)
    
    def set_tasks(self, tasks):
        self.listbox.delete(0, tk.END)
        for task in tasks:
            self.listbox.insert(tk.END, task)

class TaskController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.model.add_observer(self)
    
    def add_task(self):
        task = self.view.get_input()
        if task:
            self.model.add_task(task)
            self.view.clear_input()
    
    def update(self):
        tasks = self.model.get_tasks()
        self.view.set_tasks(tasks)
```

</details>

### Уровень 2 - Средний

#### Задание 2.1: Приложение списка задач

Создайте To-Do приложение:

```python
class TodoApp:
    """
    Приложение списка задач
    """
    def __init__(self, root):
        # ВАШ КОД ЗДЕСЬ - создайте полное приложение с:
        # - Моделью задач
        # - Представлением с чекбоксами
        # - Контроллером для добавления/удаления
        pass
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import tkinter as tk
from tkinter import ttk

class TodoModel:
    def __init__(self):
        self.tasks = []
        self.observers = []
    
    def add(self, text):
        self.tasks.append({"text": text, "done": False})
        self.notify()
    
    def toggle(self, index):
        self.tasks[index]["done"] = not self.tasks[index]["done"]
        self.notify()
    
    def delete(self, index):
        self.tasks.pop(index)
        self.notify()
    
    def get_all(self):
        return self.tasks
    
    def add_observer(self, obs):
        self.observers.append(obs)
    
    def notify(self):
        for obs in self.observers:
            obs.refresh()

class TodoView:
    def __init__(self, root):
        self.root = root
        self.listbox = tk.Listbox(root)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.entry = tk.Entry(root)
        self.entry.pack(fill=tk.X, padx=10, pady=5)
        
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)
        
        self.add_btn = tk.Button(btn_frame, text="Добавить")
        self.del_btn = tk.Button(btn_frame, text="Удалить")
        self.add_btn.pack(side=tk.LEFT, padx=5)
        self.del_btn.pack(side=tk.LEFT, padx=5)

class TodoController:
    def __init__(self):
        self.model = TodoModel()
        self.view = TodoView(tk.Tk())
        
        self.view.add_btn.config(command=self.add)
        self.view.del_btn.config(command=self.delete)
        self.view.listbox.bind('<Double-Button-1>', self.toggle)
        
        self.model.add_observer(self)
        self.refresh()
        
        self.view.root.mainloop()
    
    def add(self):
        text = self.view.entry.get()
        if text:
            self.model.add(text)
            self.view.entry.delete(0, tk.END)
    
    def delete(self):
        selection = self.view.listbox.curselection()
        if selection:
            self.model.delete(selection[0])
    
    def toggle(self, event):
        selection = self.view.listbox.curselection()
        if selection:
            self.model.toggle(selection[0])
    
    def refresh(self):
        self.view.listbox.delete(0, tk.END)
        for task in self.model.get_all():
            text = f"[{'x' if task['done'] else ' '}] {task['text']}"
            self.view.listbox.insert(tk.END, text)

TodoController()
```

</details>

### Уровень 3 - Продвинутый

#### Задание 3.1: Полноценное MVC приложение

Создайте приложение с архитектурой MVC:

```python
# Реализуйте приложение "Контакты" с:
# - Модель: контакты с полями (имя, телефон, email)
# - View: таблица и форма редактирования
# - Controller: CRUD операции, валидация, поиск

class ContactModel:
    """
    Модель контактов
    """
    def __init__(self):
        # ВАШ КОД ЗДЕСЬ - реализуйте хранение контактов
        pass
        
class ContactView:
    """
    Представление контактов
    """
    def __init__(self, root):
        # ВАШ КОД ЗДЕСЬ - создайте таблицу и форму
        pass
        
class ContactController:
    """
    Контроллер контактов
    """
    def __init__(self):
        # ВАШ КОД ЗДЕСЬ - свяжите компоненты
        pass
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import tkinter as tk
from tkinter import ttk

class ContactModel:
    def __init__(self):
        self.contacts = []
        self.observers = []
    
    def add(self, name, phone, email):
        self.contacts.append({"name": name, "phone": phone, "email": email})
        self.notify()
    
    def update(self, index, name, phone, email):
        if 0 <= index < len(self.contacts):
            self.contacts[index] = {"name": name, "phone": phone, "email": email}
            self.notify()
    
    def delete(self, index):
        if 0 <= index < len(self.contacts):
            self.contacts.pop(index)
            self.notify()
    
    def get_all(self):
        return self.contacts
    
    def add_observer(self, obs):
        self.observers.append(obs)
    
    def notify(self):
        for obs in self.observers:
            obs.refresh()

class ContactView:
    def __init__(self, root):
        self.root = root
        self.root.title("Контакты")
        
        # Таблица
        self.tree = ttk.Treeview(root, columns=("name", "phone", "email"), show="headings")
        self.tree.heading("name", text="Имя")
        self.tree.heading("phone", text="Телефон")
        self.tree.heading("email", text="Email")
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Форма
        form = ttk.Frame(root, padding="10")
        form.pack(fill=tk.X)
        
        ttk.Label(form, text="Имя:").grid(row=0, column=0)
        self.name_entry = ttk.Entry(form)
        self.name_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(form, text="Телефон:").grid(row=0, column=2)
        self.phone_entry = ttk.Entry(form)
        self.phone_entry.grid(row=0, column=3, padx=5)
        
        ttk.Label(form, text="Email:").grid(row=0, column=4)
        self.email_entry = ttk.Entry(form)
        self.email_entry.grid(row=0, column=5, padx=5)
        
        # Кнопки
        btn_frame = ttk.Frame(root, padding="10")
        btn_frame.pack()
        
        self.add_btn = ttk.Button(btn_frame, text="Добавить")
        self.edit_btn = ttk.Button(btn_frame, text="Изменить")
        self.del_btn = ttk.Button(btn_frame, text="Удалить")
        
        self.add_btn.pack(side=tk.LEFT, padx=5)
        self.edit_btn.pack(side=tk.LEFT, padx=5)
        self.del_btn.pack(side=tk.LEFT, padx=5)

class ContactController:
    def __init__(self):
        self.model = ContactModel()
        self.view = ContactView(tk.Tk())
        
        self.view.add_btn.config(command=self.add)
        self.view.edit_btn.config(command=self.edit)
        self.view.del_btn.config(command=self.delete)
        
        self.model.add_observer(self)
        self.refresh()
        
        self.view.root.mainloop()
    
    def add(self):
        name = self.view.name_entry.get()
        phone = self.view.phone_entry.get()
        email = self.view.email_entry.get()
        if name:
            self.model.add(name, phone, email)
            self.clear_form()
    
    def edit(self):
        selection = self.view.tree.selection()
        if selection:
            index = self.view.tree.index(selection[0])
            name = self.view.name_entry.get()
            phone = self.view.phone_entry.get()
            email = self.view.email_entry.get()
            self.model.update(index, name, phone, email)
    
    def delete(self):
        selection = self.view.tree.selection()
        if selection:
            index = self.view.tree.index(selection[0])
            self.model.delete(index)
    
    def clear_form(self):
        self.view.name_entry.delete(0, tk.END)
        self.view.phone_entry.delete(0, tk.END)
        self.view.email_entry.delete(0, tk.END)
    
    def refresh(self):
        for item in self.view.tree.get_children():
            self.view.tree.delete(item)
        for contact in self.model.get_all():
            self.view.tree.insert("", tk.END, values=(contact["name"], contact["phone"], contact["email"]))

ContactController()
```

</details>

---

## Требования к отчету
- Исходный код всех компонентов
- UML диаграмма архитектуры
- Описание взаимодействия компонентов
- Тесты компонентов

## Критерии оценки
- Архитектура: 30%
- Функциональность: 30%
- Качество кода: 20%
- Документация: 20%
