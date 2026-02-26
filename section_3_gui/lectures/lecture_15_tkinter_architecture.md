# Лекция 15: Tkinter - архитектура GUI-приложений

## MVC/MVP паттерны в GUI-приложениях, организация кода

### План лекции:
1. Паттерны архитектуры GUI-приложений
2. MVC (Model-View-Controller)
3. MVP (Model-View-Presenter)
4. MVVM (Model-View-ViewModel)
5. Организация кода в GUI-приложениях
6. Практические примеры

---

## 1. Паттерны архитектуры GUI-приложений

### Введение в архитектурные паттерны

При создании графических интерфейсов важно правильно организовать структуру приложения. Архитектурные паттерны помогают разделить ответственность между различными компонентами приложения, что упрощает разработку, тестирование и поддержку кода.

### Зачем использовать архитектурные паттерны:
- **Разделение ответственности**: Каждая часть приложения отвечает за свою функцию
- **Тестируемость**: Логика может быть протестирована отдельно от интерфейса
- **Поддерживаемость**: Изменения в одной части не затрагивают другие
- **Повторное использование**: Компоненты могут использоваться в других частях приложения
- **Масштабируемость**: Приложение может расти без усложнения структуры

---

## 2. Паттерн MVC (Model-View-Controller)

### Основные компоненты MVC:

1. **Model (Модель)**: Отвечает за данные и бизнес-логику
2. **View (Представление)**: Отвечает за отображение данных
3. **Controller (Контроллер)**: Обрабатывает пользовательский ввод и координирует взаимодействие между Model и View

```python
import tkinter as tk
from tkinter import ttk
from typing import List, Dict, Any

class UserModel:
    """
    Модель данных пользователя
    """
    def __init__(self):
        self._users: List[Dict[str, Any]] = []
        self._observers = []
    
    def add_user(self, name: str, email: str, age: int):
        """Добавление пользователя"""
        user = {
            "id": len(self._users) + 1,
            "name": name,
            "email": email,
            "age": age
        }
        self._users.append(user)
        self._notify_observers()
    
    def get_users(self) -> List[Dict[str, Any]]:
        """Получение всех пользователей"""
        return self._users.copy()
    
    def get_user_by_id(self, user_id: int) -> Dict[str, Any]:
        """Получение пользователя по ID"""
        for user in self._users:
            if user["id"] == user_id:
                return user
        return None
    
    def attach_observer(self, observer):
        """Добавление наблюдателя"""
        self._observers.append(observer)
    
    def detach_observer(self, observer):
        """Удаление наблюдателя"""
        self._observers.remove(observer)
    
    def _notify_observers(self):
        """Уведомление наблюдателей об изменении"""
        for observer in self._observers:
            observer.update_users_list()

class UserView:
    """
    Представление пользовательского интерфейса
    """
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        
        self.setup_ui()
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="Управление пользователями", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Форма ввода
        input_frame = ttk.LabelFrame(main_frame, text="Добавить пользователя", padding="10")
        input_frame.pack(fill=tk.X, pady=10)
        
        # Поля ввода
        fields = ["Имя", "Email", "Возраст"]
        self.entries = {}
        
        for i, field in enumerate(fields):
            ttk.Label(input_frame, text=f"{field}:").grid(row=0, column=i*2, sticky="w", padx=(0, 5))
            entry = ttk.Entry(input_frame, width=20)
            entry.grid(row=0, column=i*2+1, padx=(0, 15))
            self.entries[field.lower()] = entry
        
        # Кнопка добавления
        add_btn = ttk.Button(input_frame, text="Добавить", 
                            command=self.controller.add_user_from_view)
        add_btn.grid(row=0, column=6, padx=(0, 10))
        
        # Кнопка очистки
        clear_btn = ttk.Button(input_frame, text="Очистить", 
                              command=self.controller.clear_users)
        clear_btn.grid(row=0, column=7)
        
        # Таблица пользователей
        table_frame = ttk.LabelFrame(main_frame, text="Список пользователей", padding="10")
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Создание таблицы
        columns = ("ID", "Имя", "Email", "Возраст")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="tree headings")
        
        # Настройка заголовков
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Прокрутка
        tree_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def update_users_list(self):
        """Обновление списка пользователей в интерфейсе"""
        # Очистка текущего списка
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Добавление обновленных данных
        users = self.controller.model.get_users()
        for user in users:
            self.tree.insert("", tk.END, values=(
                user["id"], 
                user["name"], 
                user["email"], 
                user["age"]
            ))
    
    def get_input_values(self) -> Dict[str, str]:
        """Получение значений из полей ввода"""
        values = {}
        for field, entry in self.entries.items():
            values[field] = entry.get()
        return values
    
    def clear_input_fields(self):
        """Очистка полей ввода"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)

class UserController:
    """
    Контроллер приложения
    """
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        # Регистрация наблюдателя
        self.model.attach_observer(self.view)
    
    def add_user_from_view(self):
        """Добавление пользователя из представления"""
        values = self.view.get_input_values()
        
        try:
            name = values["name"].strip()
            email = values["email"].strip()
            age = int(values["age"]) if values["age"] else 0
            
            if not name or not email:
                raise ValueError("Имя и email обязательны")
            
            self.model.add_user(name, email, age)
            self.view.clear_input_fields()
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
    
    def clear_users(self):
        """Очистка пользователей"""
        # В реальном приложении модель должна иметь метод очистки
        pass

class MVCApplication:
    """
    Основное приложение с архитектурой MVC
    """
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Приложение с архитектурой MVC")
        self.root.geometry("800x600")
        
        # Создание компонентов MVC
        self.model = UserModel()
        self.view = UserView(self.root, None)  # Временно None, пока контроллер не создан
        self.controller = UserController(self.model, self.view)
        
        # Назначение контроллера в представление
        self.view.controller = self.controller
    
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()

# Пример использования
if __name__ == "__main__":
    app = MVCApplication()
    app.run()
```

---

## 3. Паттерн MVP (Model-View-Presenter)

### Основные компоненты MVP:

1. **Model (Модель)**: Отвечает за данные и бизнес-логику
2. **View (Представление)**: Простой интерфейс, который ничего не знает о модели
3. **Presenter (Презентер)**: Мост между View и Model, содержит всю логику представления

```python
import tkinter as tk
from tkinter import ttk

class UserPresenter:
    """
    Презентер в архитектуре MVP
    """
    def __init__(self, model, view):
        self.model = model
        self.view = view
        
        # Подключение презентера к модели
        self.model.attach_observer(self)
    
    def on_add_user_click(self):
        """Обработка нажатия кнопки добавления пользователя"""
        try:
            values = self.view.get_input_values()
            
            name = values["name"].strip()
            email = values["email"].strip()
            age = int(values["age"]) if values["age"] else 0
            
            if not name or not email:
                raise ValueError("Имя и email обязательны")
            
            self.model.add_user(name, email, age)
            self.view.clear_input_fields()
        except ValueError as e:
            self.view.show_error(f"Ошибка валидации: {e}")
    
    def on_clear_click(self):
        """Обработка нажатия кнопки очистки"""
        self.model.clear_all()
    
    def update_view(self):
        """Обновление представления при изменении модели"""
        users = self.model.get_users()
        self.view.refresh_user_list(users)
    
    def get_user_count(self):
        """Получение количества пользователей"""
        return len(self.model.get_users())

class MVPView:
    """
    Представление в архитектуре MVP
    """
    def __init__(self, root):
        self.root = root
        self.presenter = None  # Будет установлен позже
        
        self.setup_ui()
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="Управление пользователями (MVP)", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Статусная строка
        self.status_label = ttk.Label(main_frame, text="Пользователей: 0", relief="sunken")
        self.status_label.pack(fill=tk.X, pady=(0, 10))
        
        # Форма ввода
        input_frame = ttk.LabelFrame(main_frame, text="Добавить пользователя", padding="10")
        input_frame.pack(fill=tk.X, pady=5)
        
        # Поля ввода
        fields = ["Имя", "Email", "Возраст"]
        self.entries = {}
        
        for i, field in enumerate(fields):
            ttk.Label(input_frame, text=f"{field}:").grid(row=0, column=i*2, sticky="w", padx=(0, 5))
            entry = ttk.Entry(input_frame, width=20)
            entry.grid(row=0, column=i*2+1, padx=(0, 15))
            self.entries[field.lower()] = entry
        
        # Кнопки
        ttk.Button(input_frame, text="Добавить", 
                  command=self.on_add_user_click).grid(row=0, column=6, padx=(0, 10))
        ttk.Button(input_frame, text="Очистить", 
                  command=self.on_clear_click).grid(row=0, column=7)
        
        # Таблица
        table_frame = ttk.LabelFrame(main_frame, text="Список пользователей", padding="10")
        table_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        columns = ("ID", "Имя", "Email", "Возраст")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="tree headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        tree_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def on_add_user_click(self):
        """Обработка нажатия кнопки добавления"""
        if self.presenter:
            self.presenter.on_add_user_click()
    
    def on_clear_click(self):
        """Обработка нажатия кнопки очистки"""
        if self.presenter:
            self.presenter.on_clear_click()
    
    def get_input_values(self):
        """Получение значений из полей ввода"""
        values = {}
        for field, entry in self.entries.items():
            values[field] = entry.get()
        return values
    
    def clear_input_fields(self):
        """Очистка полей ввода"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
    
    def refresh_user_list(self, users):
        """Обновление списка пользователей"""
        # Очистка текущего списка
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Добавление новых данных
        for user in users:
            self.tree.insert("", tk.END, values=(
                user["id"],
                user["name"],
                user["email"],
                user["age"]
            ))
        
        # Обновление статуса
        self.status_label.config(text=f"Пользователей: {len(users)}")
    
    def show_error(self, message):
        """Показ сообщения об ошибке"""
        from tkinter import messagebox
        messagebox.showerror("Ошибка", message)

class MVPApplication:
    """
    Приложение с архитектурой MVP
    """
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Приложение с архитектурой MVP")
        self.root.geometry("800x600")
        
        # Создание компонентов
        self.model = UserModel()
        self.view = MVPView(self.root)
        self.presenter = UserPresenter(self.model, self.view)
        
        # Назначение презентера в представление
        self.view.presenter = self.presenter
        
        # Инициализация начальных данных
        self.presenter.update_view()
    
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()
```

---

## 4. Паттерн MVVM (Model-View-ViewModel)

MVVM менее распространен в Tkinter, но может быть реализован с использованием наблюдаемых свойств:

```python
class ObservableValue:
    """
    Наблюдаемое значение для MVVM
    """
    def __init__(self, value):
        self._value = value
        self._observers = []
    
    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, new_value):
        old_value = self._value
        self._value = new_value
        self._notify_observers(old_value, new_value)
    
    def add_observer(self, callback):
        """Добавление наблюдателя"""
        self._observers.append(callback)
    
    def remove_observer(self, callback):
        """Удаление наблюдателя"""
        self._observers.remove(callback)
    
    def _notify_observers(self, old_value, new_value):
        """Уведомление наблюдателей"""
        for observer in self._observers:
            observer(old_value, new_value)

class UserViewModel:
    """
    ViewModel для управления пользователями
    """
    def __init__(self, model):
        self.model = model
        self.user_count = ObservableValue(0)
        
        # Подключение к модели
        self.model.attach_observer(self)
    
    def update(self):
        """Обновление ViewModel при изменении модели"""
        count = len(self.model.get_users())
        self.user_count.value = count
    
    def add_user(self, name, email, age):
        """Добавление пользователя через ViewModel"""
        self.model.add_user(name, email, age)
    
    def get_users(self):
        """Получение пользователей через ViewModel"""
        return self.model.get_users()

class MVVMView:
    """
    Представление в архитектуре MVVM
    """
    def __init__(self, root, view_model):
        self.root = root
        self.vm = view_model
        
        # Подключение к наблюдаемым значениям
        self.vm.user_count.add_observer(self.on_user_count_change)
        
        self.setup_ui()
    
    def setup_ui(self):
        """Настройка интерфейса"""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="Управление пользователями (MVVM)", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Статус с наблюдаемым значением
        self.status_label = ttk.Label(main_frame, text="Пользователей: 0", relief="sunken")
        self.status_label.pack(fill=tk.X, pady=(0, 10))
        
        # Остальная часть интерфейса...
    
    def on_user_count_change(self, old_value, new_value):
        """Обработка изменения количества пользователей"""
        self.status_label.config(text=f"Пользователей: {new_value}")

# Пример использования MVVM
def mvvm_example():
    root = tk.Tk()
    root.title("Пример MVVM")
    root.geometry("400x300")
    
    model = UserModel()
    vm = UserViewModel(model)
    view = MVVMView(root, vm)
    
    root.mainloop()
```

---

## 5. Организация кода в GUI-приложениях

### Структура проекта с MVC

```
my_gui_app/
├── main.py
├── models/
│   ├── __init__.py
│   ├── user_model.py
│   └── data_models.py
├── views/
│   ├── __init__.py
│   ├── user_view.py
│   └── main_window.py
├── controllers/
│   ├── __init__.py
│   ├── user_controller.py
│   └── app_controller.py
├── utils/
│   ├── __init__.py
│   └── helpers.py
└── resources/
    ├── icons/
    └── styles/
```

### Пример организации кода в модулях

```python
# models/user_model.py
from typing import List, Dict, Any
from dataclasses import dataclass

@dataclass
class User:
    id: int
    name: str
    email: str
    age: int

class UserManagementModel:
    """
    Модель управления пользователями
    """
    def __init__(self):
        self.users: List[User] = []
        self.next_id = 1
        self._observers = []
    
    def add_user(self, name: str, email: str, age: int) -> User:
        """Добавление пользователя"""
        user = User(
            id=self.next_id,
            name=name,
            email=email,
            age=age
        )
        self.users.append(user)
        self.next_id += 1
        self._notify_observers()
        return user
    
    def get_users(self) -> List[User]:
        """Получение всех пользователей"""
        return self.users.copy()
    
    def remove_user(self, user_id: int) -> bool:
        """Удаление пользователя по ID"""
        for i, user in enumerate(self.users):
            if user.id == user_id:
                del self.users[i]
                self._notify_observers()
                return True
        return False
    
    def attach_observer(self, observer):
        """Добавление наблюдателя"""
        self._observers.append(observer)
    
    def _notify_observers(self):
        """Уведомление наблюдателей"""
        for observer in self._observers:
            observer()
```

```python
# views/user_view.py
import tkinter as tk
from tkinter import ttk
from typing import Callable

class UserManagementView:
    """
    Представление для управления пользователями
    """
    def __init__(self, parent, on_add_callback: Callable, on_remove_callback: Callable):
        self.parent = parent
        self.on_add_callback = on_add_callback
        self.on_remove_callback = on_remove_callback
        
        self.setup_ui()
    
    def setup_ui(self):
        """Настройка пользовательского интерфейса"""
        # Создание элементов интерфейса
        self.create_input_form()
        self.create_user_table()
    
    def create_input_form(self):
        """Создание формы ввода"""
        input_frame = ttk.LabelFrame(self.parent, text="Добавить пользователя", padding="10")
        input_frame.pack(fill=tk.X, pady=5)
        
        # Поля ввода
        fields = ["Имя", "Email", "Возраст"]
        self.entries = {}
        
        for i, field in enumerate(fields):
            ttk.Label(input_frame, text=f"{field}:").grid(row=0, column=i*2, sticky="w", padx=(0, 5))
            entry = ttk.Entry(input_frame, width=20)
            entry.grid(row=0, column=i*2+1, padx=(0, 15))
            self.entries[field.lower()] = entry
        
        # Кнопка добавления
        ttk.Button(input_frame, text="Добавить", 
                  command=self.on_add_click).grid(row=0, column=6)
    
    def create_user_table(self):
        """Создание таблицы пользователей"""
        table_frame = ttk.LabelFrame(self.parent, text="Список пользователей", padding="10")
        table_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        columns = ("ID", "Имя", "Email", "Возраст", "Действия")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="tree headings")
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100 if col != "Действия" else 80)
        
        tree_scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Добавление кнопки удаления в таблицу
        self.tree.bind("<Double-1>", self.on_double_click)
    
    def on_add_click(self):
        """Обработка нажатия кнопки добавления"""
        values = self.get_input_values()
        self.on_add_callback(values)
        self.clear_input_fields()
    
    def on_double_click(self, event):
        """Обработка двойного клика для удаления"""
        item = self.tree.selection()[0]
        user_id = int(self.tree.item(item, "values")[0])
        self.on_remove_callback(user_id)
    
    def get_input_values(self):
        """Получение значений из полей ввода"""
        values = {}
        for field, entry in self.entries.items():
            values[field] = entry.get()
        return values
    
    def clear_input_fields(self):
        """Очистка полей ввода"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)
    
    def update_user_list(self, users):
        """Обновление списка пользователей"""
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Добавление пользователей
        for user in users:
            self.tree.insert("", tk.END, values=(
                user.id,
                user.name,
                user.email,
                user.age,
                "Удалить"
            ))
    
    def show_message(self, title, message):
        """Показ сообщения пользователю"""
        from tkinter import messagebox
        messagebox.showinfo(title, message)
```

```python
# controllers/app_controller.py
from models.user_model import UserManagementModel
from views.user_view import UserManagementView

class AppController:
    """
    Контроллер приложения
    """
    def __init__(self, root):
        self.root = root
        self.model = UserManagementModel()
        self.view = UserManagementView(
            root, 
            on_add_callback=self.add_user, 
            on_remove_callback=self.remove_user
        )
        
        # Подключение модели к представлению
        self.model.attach_observer(self.update_view)
        self.update_view()
    
    def add_user(self, values):
        """Добавление пользователя"""
        try:
            name = values["name"].strip()
            email = values["email"].strip()
            age = int(values["age"]) if values["age"] else 0
            
            if not name or not email:
                raise ValueError("Имя и email обязательны")
            
            self.model.add_user(name, email, age)
            self.view.show_message("Успех", "Пользователь добавлен")
        except ValueError as e:
            self.view.show_message("Ошибка", f"Некорректные данные: {e}")
    
    def remove_user(self, user_id):
        """Удаление пользователя"""
        if self.model.remove_user(user_id):
            self.view.show_message("Успех", "Пользователь удален")
        else:
            self.view.show_message("Ошибка", "Пользователь не найден")
    
    def update_view(self):
        """Обновление представления"""
        users = self.model.get_users()
        self.view.update_user_list(users)

# main.py
import tkinter as tk
from controllers.app_controller import AppController

def main():
    root = tk.Tk()
    root.title("GUI Приложение с MVC")
    root.geometry("800x600")
    
    controller = AppController(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()
```

---

## 6. Практические примеры

### Пример 1: Калькулятор с MVC

```python
class CalculatorModel:
    """
    Модель калькулятора
    """
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Сброс состояния калькулятора"""
        self.current_value = 0
        self.previous_value = 0
        self.operator = None
        self.new_number = True
    
    def enter_number(self, number):
        """Ввод числа"""
        if self.new_number:
            self.current_value = number
            self.new_number = False
        else:
            self.current_value = self.current_value * 10 + number
    
    def enter_operator(self, op):
        """Ввод оператора"""
        if not self.new_number and self.operator:
            self.calculate()
        
        self.previous_value = self.current_value
        self.operator = op
        self.new_number = True
    
    def calculate(self):
        """Выполнение вычисления"""
        if self.operator == "+":
            self.current_value = self.previous_value + self.current_value
        elif self.operator == "-":
            self.current_value = self.previous_value - self.current_value
        elif self.operator == "*":
            self.current_value = self.previous_value * self.current_value
        elif self.operator == "/":
            if self.current_value != 0:
                self.current_value = self.previous_value / self.current_value
            else:
                raise ZeroDivisionError("Деление на ноль")
        
        self.operator = None
        self.new_number = True
    
    def get_display_value(self):
        """Получение значения для отображения"""
        return self.current_value

class CalculatorView:
    """
    Представление калькулятора
    """
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.setup_ui()
    
    def setup_ui(self):
        """Настройка интерфейса калькулятора"""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Дисплей
        self.display_var = tk.StringVar(value="0")
        display = ttk.Entry(main_frame, textvariable=self.display_var, 
                           font=("Arial", 16), justify="right", state="readonly")
        display.pack(fill=tk.X, pady=(0, 10))
        
        # Кнопки
        button_frame = ttk.Frame(main_frame)
        button_frame.pack()
        
        # Цифровые кнопки
        for i in range(9, -1, -1):
            btn = ttk.Button(button_frame, text=str(i), width=5, 
                            command=lambda x=i: self.controller.number_click(x))
            btn.grid(row=(9-i)//3 + 1, column=(9-i)%3, padx=2, pady=2)
        
        # Операторы
        operators = ["+", "-", "*", "/", "="]
        for i, op in enumerate(operators):
            btn = ttk.Button(button_frame, text=op, width=5,
                           command=lambda x=op: self.controller.operator_click(x))
            btn.grid(row=i, column=3, padx=2, pady=2)
        
        # Кнопка сброса
        reset_btn = ttk.Button(button_frame, text="C", width=5,
                              command=self.controller.reset_click)
        reset_btn.grid(row=0, column=4, padx=2, pady=2)

class CalculatorController:
    """
    Контроллер калькулятора
    """
    def __init__(self, root):
        self.model = CalculatorModel()
        self.view = CalculatorView(root, self)
    
    def number_click(self, number):
        """Обработка нажатия цифровой кнопки"""
        self.model.enter_number(number)
        self.update_display()
    
    def operator_click(self, operator):
        """Обработка нажатия оператора"""
        if operator == "=":
            try:
                self.model.calculate()
            except ZeroDivisionError:
                self.view.show_error("Деление на ноль")
                self.model.reset()
        else:
            self.model.enter_operator(operator)
        self.update_display()
    
    def reset_click(self):
        """Обработка нажатия кнопки сброса"""
        self.model.reset()
        self.update_display()
    
    def update_display(self):
        """Обновление дисплея"""
        self.view.display_var.set(str(self.model.get_display_value()))

# Запуск калькулятора
def run_calculator():
    root = tk.Tk()
    root.title("Калькулятор MVC")
    root.geometry("300x400")
    
    controller = CalculatorController(root)
    
    root.mainloop()
```

### Пример 2: Список задач с MVP

```python
class Task:
    """
    Модель задачи
    """
    def __init__(self, title, description="", completed=False):
        self.title = title
        self.description = description
        self.completed = completed
        self.id = id(self)  # Простой ID для демонстрации

class TaskModel:
    """
    Модель управления задачами
    """
    def __init__(self):
        self.tasks = []
        self._observers = []
    
    def add_task(self, title, description=""):
        """Добавление задачи"""
        task = Task(title, description)
        self.tasks.append(task)
        self._notify_observers()
        return task
    
    def remove_task(self, task_id):
        """Удаление задачи"""
        self.tasks = [task for task in self.tasks if task.id != task_id]
        self._notify_observers()
    
    def toggle_task(self, task_id):
        """Переключение статуса задачи"""
        for task in self.tasks:
            if task.id == task_id:
                task.completed = not task.completed
                self._notify_observers()
                break
    
    def get_tasks(self):
        """Получение всех задач"""
        return self.tasks
    
    def attach_observer(self, observer):
        """Добавление наблюдателя"""
        self._observers.append(observer)
    
    def _notify_observers(self):
        """Уведомление наблюдателей"""
        for observer in self._observers:
            observer()

class TaskView:
    """
    Представление списка задач
    """
    def __init__(self, root):
        self.root = root
        self.presenter = None  # Будет установлен позже
        self.setup_ui()
    
    def setup_ui(self):
        """Настройка интерфейса"""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="Список задач", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Поле ввода задачи
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=5)
        
        self.task_entry = ttk.Entry(input_frame)
        self.task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        add_btn = ttk.Button(input_frame, text="Добавить", 
                            command=self.on_add_task)
        add_btn.pack(side=tk.RIGHT)
        
        # Список задач
        self.task_frame = ttk.Frame(main_frame)
        self.task_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    
    def on_add_task(self):
        """Обработка добавления задачи"""
        if self.presenter:
            title = self.task_entry.get()
            if title.strip():
                self.presenter.add_task(title)
                self.task_entry.delete(0, tk.END)
    
    def refresh_tasks(self, tasks):
        """Обновление списка задач"""
        # Очистка текущего списка
        for widget in self.task_frame.winfo_children():
            widget.destroy()
        
        # Создание новых элементов задач
        for task in tasks:
            self.create_task_widget(task)
    
    def create_task_widget(self, task):
        """Создание виджета для задачи"""
        task_frame = ttk.Frame(self.task_frame)
        task_frame.pack(fill=tk.X, pady=2)
        
        # Чекбокс для статуса
        var = tk.BooleanVar(value=task.completed)
        checkbox = ttk.Checkbutton(
            task_frame, 
            variable=var, 
            command=lambda t=task: self.on_toggle_task(t)
        )
        checkbox.pack(side=tk.LEFT)
        
        # Название задачи
        label_text = task.title
        if task.completed:
            label_text = f"[Выполнено] {label_text}"
        
        label = ttk.Label(task_frame, text=label_text)
        label.pack(side=tk.LEFT, padx=(10, 0), fill=tk.X, expand=True)
        
        # Кнопка удаления
        delete_btn = ttk.Button(
            task_frame, 
            text="Удалить", 
            command=lambda t=task: self.on_delete_task(t),
            width=10
        )
        delete_btn.pack(side=tk.RIGHT)
    
    def on_toggle_task(self, task):
        """Обработка переключения статуса задачи"""
        if self.presenter:
            self.presenter.toggle_task(task.id)
    
    def on_delete_task(self, task):
        """Обработка удаления задачи"""
        if self.presenter:
            self.presenter.remove_task(task.id)

class TaskPresenter:
    """
    Презентер для управления задачами
    """
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.presenter = self
        
        # Подключение к модели
        self.model.attach_observer(self.update_view)
        
        # Инициализация представления
        self.update_view()
    
    def add_task(self, title):
        """Добавление задачи"""
        self.model.add_task(title)
    
    def remove_task(self, task_id):
        """Удаление задачи"""
        self.model.remove_task(task_id)
    
    def toggle_task(self, task_id):
        """Переключение статуса задачи"""
        self.model.toggle_task(task_id)
    
    def update_view(self):
        """Обновление представления"""
        tasks = self.model.get_tasks()
        self.view.refresh_tasks(tasks)

# Запуск приложения списка задач
def run_task_app():
    root = tk.Tk()
    root.title("Список задач MVP")
    root.geometry("500x400")
    
    model = TaskModel()
    view = TaskView(root)
    presenter = TaskPresenter(model, view)
    
    root.mainloop()
```

---

## Заключение

Архитектурные паттерны MVC, MVP и MVVM позволяют создавать более организованные и поддерживаемые GUI-приложения. Они обеспечивают разделение ответственности между различными компонентами приложения, что упрощает тестирование, развитие и сопровождение кода.

## Контрольные вопросы:
1. В чем разница между MVC, MVP и MVVM?
2. Какие преимущества дает использование архитектурных паттернов?
3. Как реализовать наблюдатель в архитектуре MVC?
4. Какие компоненты входят в каждый из паттернов?
5. Как организовать код в соответствии с архитектурными паттернами?
