# Практическое занятие 18: Tkinter - элементы пользовательского интерфейса

## Цель занятия
Изучить основные элементы пользовательского интерфейса в Tkinter, включая виджеты для ввода данных, отображения информации, навигации и взаимодействия с пользователем.

## Задачи
1. Освоить виджеты ввода данных (Entry, Text, Spinbox, Combobox)
2. Изучить кнопки и переключатели (Button, Checkbutton, Radiobutton, Scale)
3. Научиться отображать информацию с помощью Label, Message, Canvas
4. Освоить навигационные элементы (Notebook, PanedWindow, Menu, Toolbar)
5. Создать комплексное приложение «Форма регистрации»

## Ход работы

### 1. Виджеты ввода данных

Создайте файл `input_widgets.py` и реализуйте функции для работы с виджетами ввода:

#### Виджеты для однострочного и многострочного ввода

```python
import tkinter as tk
from tkinter import ttk
from tkinter import ttk, messagebox

def create_entry_widget(parent, width=30):
    """
    Создает однострочное поле ввода
    
    Args:
        parent: Родительский виджет
        width: Ширина поля
        
    Returns:
        tuple: (фрейм, виджет Entry)
    """
    # ВАШ КОД ЗДЕСЬ - создайте поле Entry
    pass  # Замените на ваш код

def create_text_widget(parent, width=40, height=10):
    """
    Создает многострочное поле ввода
    
    Args:
        parent: Родительский виджет
        width: Ширина
        height: Высота
        
    Returns:
        tuple: (фрейм, виджет Text)
    """
    # ВАШ КОД ЗДЕСЬ - создайте текстовую область Text
    pass  # Замените на ваш код

def create_spinbox_widget(parent, from_=0, to=100, increment=1):
    """
    Создает спинбокс (выбор из диапазона)
    
    Args:
        parent: Родительский виджет
        from_: Минимальное значение
        to: Максимальное значение
        increment: Шаг изменения
        
    Returns:
        tuple: (фрейм, виджет Spinbox)
    """
    # ВАШ КОД ЗДЕСЬ - создайте Spinbox
    pass  # Замените на ваш код

def create_combobox_widget(parent, values):
    """
    Создает комбобокс (выбор из списка)
    
    Args:
        parent: Родительский виджет
        values: Список значений
        
    Returns:
        tuple: (фрейм, виджет Combobox)
    """
    # ВАШ КОД ЗДЕСЬ - создайте Combobox
    pass  # Замените на ваш код
```

---

## 1. Теоретическая часть: Элементы пользовательского интерфейса

### Уровень 1 - Начальный

#### Задание 1.1: Основные виджеты ввода

Создайте приложение с основными виджетами ввода:

```python
import tkinter as tk
from tkinter import ttk

class InputWidgetsDemo:
    """
    Демонстрация виджетов ввода
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Виджеты ввода")
        self.root.geometry("400x500")
        
        # ВАШ КОД ЗДЕСЬ - создайте фрейм для размещения виджетов
        # Создайте Entry для ввода имени
        # Создайте Text для ввода комментария
        # Создайте Spinbox для выбора возраста
        # Создайте Combobox для выбора страны
        pass  # Замените на ваш код
        
    def on_submit(self):
        """
        Обрабатывает нажатие кнопки отправки
        """
        # ВАШ КОД ЗДЕСЬ - получите значения из виджетов и выведите их
        pass  # Замените на ваш код

# Пример использования:
# root = tk.Tk()
# demo = InputWidgetsDemo(root)
# root.mainloop()
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import tkinter as tk
from tkinter import ttk, messagebox

class InputWidgetsDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Виджеты ввода")
        self.root.geometry("400x500")
        
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        ttk.Label(main_frame, text="Форма регистрации", 
                  font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Имя пользователя (Entry)
        ttk.Label(main_frame, text="Имя:").pack(anchor=tk.W, pady=(10, 0))
        self.name_entry = ttk.Entry(main_frame, width=30)
        self.name_entry.pack(fill=tk.X, pady=5)
        
        # Комментарий (Text)
        ttk.Label(main_frame, text="Комментарий:").pack(anchor=tk.W, pady=(10, 0))
        self.comment_text = tk.Text(main_frame, width=30, height=5)
        self.comment_text.pack(fill=tk.BOTH, pady=5)
        
        # Возраст (Spinbox)
        ttk.Label(main_frame, text="Возраст:").pack(anchor=tk.W, pady=(10, 0))
        self.age_spinbox = ttk.Spinbox(main_frame, from_=1, to=150, width=28)
        self.age_spinbox.set(25)
        self.age_spinbox.pack(pady=5)
        
        # Страна (Combobox)
        ttk.Label(main_frame, text="Страна:").pack(anchor=tk.W, pady=(10, 0))
        self.country_var = tk.StringVar()
        self.country_combobox = ttk.Combobox(
            main_frame, 
            textvariable=self.country_var,
            values=["Россия", "Украина", "Беларусь", "Казахстан", "Другая"],
            width=28,
            state="readonly"
        )
        self.country_combobox.pack(pady=5)
        
        # Кнопка отправки
        submit_btn = ttk.Button(main_frame, text="Отправить", command=self.on_submit)
        submit_btn.pack(pady=20)
        
    def on_submit(self):
        name = self.name_entry.get()
        comment = self.comment_text.get("1.0", tk.END).strip()
        age = self.age_spinbox.get()
        country = self.country_var.get()
        
        messagebox.showinfo("Результат", 
                           f"Имя: {name}\n"
                           f"Возраст: {age}\n"
                           f"Страна: {country}\n"
                           f"Комментарий: {comment[:50]}...")

# Пример использования:
root = tk.Tk()
demo = InputWidgetsDemo(root)
root.mainloop()
```

</details>

#### Задание 1.2: Кнопки и переключатели

Реализуйте интерфейс с различными типами кнопок и переключателей:

```python
import tkinter as tk
from tkinter import ttk

class ButtonsDemo:
    """
    Демонстрация кнопок и переключателей
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Кнопки и переключатели")
        
        # ВАШ КОД ЗДЕСЬ - создайте:
        # Обычные кнопки (ttk.Button)
        # Флажки (Checkbutton) для множественного выбора
        # Переключатели (Radiobutton) для одиночного выбора
        # Ползунок (Scale) для выбора значения
        pass  # Замените на ваш код
        
    def on_check_changed(self):
        """
        Обрабатывает изменение флажка
        """
        # ВАШ КОД ЗДЕСЬ - получите состояние флажков
        pass  # Замените на ваш код
        
    def on_radio_changed(self):
        """
        Обрабатывает изменение переключателя
        """
        # ВАШ КОД ЗДЕСЬ - получите выбранное значение
        pass  # Замените на ваш код
        
    def on_scale_changed(self, value):
        """
        Обрабатывает изменение ползунка
        
        Args:
            value: Текущее значение ползунка
        """
        # ВАШ КОД ЗДЕСЬ - получите значение ползунка
        pass  # Замените на ваш код

# Пример использования:
# root = tk.Tk()
# demo = ButtonsDemo(root)
# root.mainloop()
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import tkinter as tk
from tkinter import ttk

class ButtonsDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Кнопки и переключатели")
        self.root.geometry("400x450")
        
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        ttk.Label(main_frame, text="Управление интерфейсом", 
                  font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Обычные кнопки
        ttk.Label(main_frame, text="Кнопки:").pack(anchor=tk.W, pady=(10, 5))
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(btn_frame, text="ОК", command=self.on_ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Отмена", command=self.on_cancel).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Применить", command=self.on_apply).pack(side=tk.LEFT, padx=5)
        
        # Флажки (Checkbutton) - множественный выбор
        ttk.Label(main_frame, text="Опции (множественный выбор):").pack(anchor=tk.W, pady=(15, 5))
        
        self.var_dark = tk.BooleanVar(value=True)
        self.var_auto = tk.BooleanVar(value=False)
        self.var_notify = tk.BooleanVar(value=True)
        
        ttk.Checkbutton(main_frame, text="Тёмная тема", 
                        variable=self.var_dark).pack(anchor=tk.W)
        ttk.Checkbutton(main_frame, text="Автосохранение", 
                        variable=self.var_auto).pack(anchor=tk.W)
        ttk.Checkbutton(main_frame, text="Уведомления", 
                        variable=self.var_notify).pack(anchor=tk.W)
        
        # Переключатели (Radiobutton) - одиночный выбор
        ttk.Label(main_frame, text="Размер шрифта (одиночный выбор):").pack(anchor=tk.W, pady=(15, 5))
        
        self.font_size = tk.StringVar(value="medium")
        
        for size, text in [("small", "Маленький"), 
                           ("medium", "Средний"), 
                           ("large", "Большой")]:
            ttk.Radiobutton(main_frame, text=text, variable=self.font_size,
                          value=size, command=self.on_radio_changed).pack(anchor=tk.W)
        
        # Ползунок (Scale)
        ttk.Label(main_frame, text="Громкость:").pack(anchor=tk.W, pady=(15, 5))
        
        self.volume = tk.IntVar(value=75)
        volume_scale = ttk.Scale(main_frame, from_=0, to=100, 
                                 variable=self.volume, command=self.on_scale_changed)
        volume_scale.pack(fill=tk.X, pady=5)
        
        self.volume_label = ttk.Label(main_frame, text="75%")
        self.volume_label.pack(pady=(0, 10))
        
    def on_ok(self):
        print("Нажата кнопка ОК")
        
    def on_cancel(self):
        print("Нажата кнопка Отмена")
        
    def on_apply(self):
        print("Нажата кнопка Применить")
        
    def on_radio_changed(self):
        print(f"Выбран размер шрифта: {self.font_size.get()}")
        
    def on_scale_changed(self, value):
        self.volume_label.config(text=f"{value}%")

# Пример использования:
root = tk.Tk()
demo = ButtonsDemo(root)
root.mainloop()
```

</details>

### Уровень 2 - Средний

#### Задание 2.1: Отображение информации

Создайте элементы для отображения информации:

```python
import tkinter as tk
from tkinter import ttk

class DisplayWidgetsDemo:
    """
    Демонстрация виджетов отображения информации
    """
    def __init__(self, root):
        self.root = root
        
        # ВАШ КОД ЗДЕСЬ - создайте:
        # Label для отображения текста
        # Label с изображением (если есть файл)
        # Message для многострочного текста с переносом
        # Canvas для отображения графики
        pass  # Замените на ваш код
        
    def update_label(self, text):
        """
        Обновляет текст метки
        
        Args:
            text: Новый текст
        """
        # ВАШ КОД ЗДЕСЬ - обновите текст метки
        pass  # Замените на ваш код

# Пример использования:
# root = tk.Tk()
# demo = DisplayWidgetsDemo(root)
# root.mainloop()
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import tkinter as tk
from tkinter import ttk

class DisplayWidgetsDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Виджеты отображения")
        self.root.geometry("500x400")
        
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        ttk.Label(main_frame, text="Виджеты отображения информации", 
                  font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Простой Label
        ttk.Label(main_frame, text="Простой текст (Label):").pack(anchor=tk.W, pady=(10, 5))
        self.status_label = ttk.Label(main_frame, text="Статус: Ожидание...", 
                                      foreground="blue")
        self.status_label.pack(anchor=tk.W, pady=5)
        
        # Label с разными шрифтами
        ttk.Label(main_frame, text="Разные стили:").pack(anchor=tk.W, pady=(15, 5))
        
        style_frame = ttk.Frame(main_frame)
        style_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(style_frame, text="Обычный", font=('Arial', 10)).pack(side=tk.LEFT, padx=10)
        ttk.Label(style_frame, text="Жирный", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=10)
        ttk.Label(style_frame, text="Курсив", font=('Arial', 10, 'italic')).pack(side=tk.LEFT, padx=10)
        
        # Message (многострочный текст с переносом)
        ttk.Label(main_frame, text="Message (автоперенос):").pack(anchor=tk.W, pady=(15, 5))
        
        long_text = ("Это длинный текст, который автоматически переносится на новую строку "
                    "в виджете Message. Это полезно для отображения справки или описания.")
        message = tk.Message(main_frame, text=long_text, width=300)
        message.pack(anchor=tk.W, pady=5)
        
        # Canvas для графики
        ttk.Label(main_frame, text="Canvas (графика):").pack(anchor=tk.W, pady=(15, 5))
        
        canvas_frame = ttk.Frame(main_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.canvas = tk.Canvas(canvas_frame, width=300, height=100, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Рисуем фигуры на Canvas
        self.canvas.create_oval(10, 10, 50, 50, fill="red", outline="darkred")
        self.canvas.create_rectangle(60, 10, 100, 50, fill="blue", outline="darkblue")
        self.canvas.create_line(110, 30, 180, 30, fill="green", width=3)
        self.canvas.create_text(240, 30, text="Фигуры", fill="purple")
        
    def update_label(self, text):
        self.status_label.config(text=f"Статус: {text}")

# Пример использования:
root = tk.Tk()
demo = DisplayWidgetsDemo(root)
root.mainloop()
```

</details>

#### Задание 2.2: Навигационные элементы

Реализуйте навигационные элементы:

```python
import tkinter as tk
from tkinter import ttk

class NavigationDemo:
    """
    Демонстрация навигационных элементов
    """
    def __init__(self, root):
        self.root = root
        
        # ВАШ КОД ЗДЕСЬ - создайте:
        # Notebook (вкладки) для организации интерфейса
        # PanedWindow для разделения области
        # Menu для меню приложения
        # Toolbar для инструментов
        pass  # Замените на ваш код

# Пример использования:
# root = tk.Tk()
# demo = NavigationDemo(root)
# root.mainloop()
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import tkinter as tk
from tkinter import ttk

class NavigationDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Навигационные элементы")
        self.root.geometry("600x400")
        
        # Создаем меню
        self.create_menu()
        
        # Создаем тулбар
        self.create_toolbar()
        
        # Создаем Notebook с вкладками
        self.create_notebook()
        
        # Создаем PanedWindow
        self.create_panedwindow()
        
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Файл
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Новый", command=self.on_new)
        file_menu.add_command(label="Открыть", command=self.on_open)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        
        # Правка
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Правка", menu=edit_menu)
        edit_menu.add_command(label="Копировать", command=self.on_copy)
        edit_menu.add_command(label="Вставить", command=self.on_paste)
        
    def create_toolbar(self):
        toolbar = ttk.Frame(self.root, relief=tk.RAISED)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        ttk.Button(toolbar, text="Новый", command=self.on_new).pack(side=tk.LEFT, padx=2, pady=2)
        ttk.Button(toolbar, text="Открыть", command=self.on_open).pack(side=tk.LEFT, padx=2, pady=2)
        ttk.Button(toolbar, text="Сохранить", command=self.on_save).pack(side=tk.LEFT, padx=2, pady=2)
        
    def create_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Вкладка 1
        tab1 = ttk.Frame(self.notebook)
        self.notebook.add(tab1, text="Основное")
        ttk.Label(tab1, text="Содержимое первой вкладки").pack(pady=20)
        
        # Вкладка 2
        tab2 = ttk.Frame(self.notebook)
        self.notebook.add(tab2, text="Настройки")
        ttk.Label(tab2, text="Содержимое второй вкладки").pack(pady=20)
        
    def create_panedwindow(self):
        # Дополнительная панель внизу
        paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        left = ttk.Frame(paned)
        paned.add(left, weight=1)
        ttk.Label(left, text="Левая панель").pack(pady=10)
        
        right = ttk.Frame(paned)
        paned.add(right, weight=2)
        ttk.Label(right, text="Правая панель").pack(pady=10)
        
    def on_new(self):
        print("Новый файл")
        
    def on_open(self):
        print("Открыть файл")
        
    def on_save(self):
        print("Сохранить файл")
        
    def on_copy(self):
        print("Копировать")
        
    def on_paste(self):
        print("Вставить")

# Пример использования:
root = tk.Tk()
demo = NavigationDemo(root)
root.mainloop()
```

</details>

### Уровень 3 - Продвинутый

#### Задание 3.1: Создание приложения «Форма регистрации»

Создайте полноценное приложение «Форма регистрации»:

```python
import tkinter as tk
from tkinter import ttk, messagebox

class RegistrationForm:
    """
    Форма регистрации с использованием изученных виджетов
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Форма регистрации")
        self.root.geometry("500x600")
        
        # ВАШ КОД ЗДЕСЬ - создайте полную форму регистрации:
        # Поля: имя, email, пароль, подтверждение пароля
        # Выбор пола (Radiobutton)
        # Интересы (Checkbutton)
        # Дата рождения (Spinbox или Combobox)
        # Согласие с условиями (Checkbutton)
        # Кнопки "Зарегистрироваться" и "Очистить"
        
        pass  # Замените на ваш код
        
    def validate_form(self):
        """
        Проверяет корректность заполнения формы
        
        Returns:
            bool: True если форма валидна
        """
        # ВАШ КОД ЗДЕСЬ - реализуйте валидацию:
        # Проверка заполнения обязательных полей
        # Проверка формата email
        # Проверка совпадения паролей
        pass  # Замените на ваш код
        
    def submit_form(self):
        """
        Обрабатывает отправку формы
        """
        # ВАШ КОД ЗДЕСЬ - при успешной валидации выведите данные
        pass  # Замените на ваш код
        
    def clear_form(self):
        """
        Очищает все поля формы
        """
        # ВАШ КОД ЗДЕСЬ - очистите все поля
        pass  # Замените на ваш код

# Пример использования:
# root = tk.Tk()
# form = RegistrationForm(root)
# root.mainloop()
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import tkinter as tk
from tkinter import ttk, messagebox
import re

class RegistrationForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Форма регистрации")
        self.root.geometry("500x650")
        
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        ttk.Label(main_frame, text="Регистрация нового пользователя", 
                  font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Имя пользователя
        ttk.Label(main_frame, text="Имя пользователя *:").pack(anchor=tk.W, pady=(10, 0))
        self.username_entry = ttk.Entry(main_frame, width=40)
        self.username_entry.pack(fill=tk.X, pady=5)
        
        # Email
        ttk.Label(main_frame, text="Email *:").pack(anchor=tk.W, pady=(10, 0))
        self.email_entry = ttk.Entry(main_frame, width=40)
        self.email_entry.pack(fill=tk.X, pady=5)
        
        # Пароль
        ttk.Label(main_frame, text="Пароль *:").pack(anchor=tk.W, pady=(10, 0))
        self.password_entry = ttk.Entry(main_frame, width=40, show="*")
        self.password_entry.pack(fill=tk.X, pady=5)
        
        # Подтверждение пароля
        ttk.Label(main_frame, text="Подтверждение пароля *:").pack(anchor=tk.W, pady=(10, 0))
        self.confirm_password_entry = ttk.Entry(main_frame, width=40, show="*")
        self.confirm_password_entry.pack(fill=tk.X, pady=5)
        
        # Пол
        ttk.Label(main_frame, text="Пол:").pack(anchor=tk.W, pady=(15, 0))
        self.gender_var = tk.StringVar(value="not_specified")
        
        gender_frame = ttk.Frame(main_frame)
        gender_frame.pack(anchor=tk.W, pady=5)
        
        ttk.Radiobutton(gender_frame, text="Мужской", variable=self.gender_var,
                       value="male").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(gender_frame, text="Женский", variable=self.gender_var,
                       value="female").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(gender_frame, text="Не указан", variable=self.gender_var,
                       value="not_specified").pack(side=tk.LEFT, padx=10)
        
        # Дата рождения
        ttk.Label(main_frame, text="Дата рождения:").pack(anchor=tk.W, pady=(15, 0))
        
        dob_frame = ttk.Frame(main_frame)
        dob_frame.pack(anchor=tk.W, pady=5)
        
        self.day_var = tk.StringVar()
        self.month_var = tk.StringVar()
        self.year_var = tk.StringVar()
        
        day_combo = ttk.Combobox(dob_frame, textvariable=self.day_var, width=5,
                                  values=[str(i) for i in range(1, 32)], state="readonly")
        day_combo.pack(side=tk.LEFT, padx=2)
        
        month_combo = ttk.Combobox(dob_frame, textvariable=self.month_var, width=10,
                                    values=["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
                                           "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"],
                                    state="readonly")
        month_combo.pack(side=tk.LEFT, padx=2)
        
        year_combo = ttk.Combobox(dob_frame, textvariable=self.year_var, width=8,
                                   values=[str(i) for i in range(1950, 2024)], state="readonly")
        year_combo.pack(side=tk.LEFT, padx=2)
        
        # Интересы
        ttk.Label(main_frame, text="Интересы:").pack(anchor=tk.W, pady=(15, 0))
        
        self.interests = {
            "sport": tk.BooleanVar(),
            "music": tk.BooleanVar(),
            "reading": tk.BooleanVar(),
            "gaming": tk.BooleanVar()
        }
        
        interests_frame = ttk.Frame(main_frame)
        interests_frame.pack(anchor=tk.W, pady=5)
        
        ttk.Checkbutton(interests_frame, text="Спорт", 
                       variable=self.interests["sport"]).pack(side=tk.LEFT, padx=10)
        ttk.Checkbutton(interests_frame, text="Музыка", 
                       variable=self.interests["music"]).pack(side=tk.LEFT, padx=10)
        ttk.Checkbutton(interests_frame, text="Чтение", 
                       variable=self.interests["reading"]).pack(side=tk.LEFT, padx=10)
        ttk.Checkbutton(interests_frame, text="Игры", 
                       variable=self.interests["gaming"]).pack(side=tk.LEFT, padx=10)
        
        # Согласие
        self.agree_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(main_frame, text="Я согласен с условиями использования *",
                       variable=self.agree_var).pack(anchor=tk.W, pady=(20, 0))
        
        # Кнопки
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Зарегистрироваться", 
                  command=self.submit_form).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Очистить", 
                  command=self.clear_form).pack(side=tk.LEFT, padx=5)
        
    def validate_form(self):
        # Проверка обязательных полей
        if not self.username_entry.get().strip():
            messagebox.showerror("Ошибка", "Введите имя пользователя!")
            return False
            
        if not self.email_entry.get().strip():
            messagebox.showerror("Ошибка", "Введите email!")
            return False
            
        if not self.password_entry.get():
            messagebox.showerror("Ошибка", "Введите пароль!")
            return False
            
        if not self.confirm_password_entry.get():
            messagebox.showerror("Ошибка", "Подтвердите пароль!")
            return False
            
        # Проверка email
        email = self.email_entry.get()
        if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
            messagebox.showerror("Ошибка", "Введите корректный email!")
            return False
            
        # Проверка паролей
        if self.password_entry.get() != self.confirm_password_entry.get():
            messagebox.showerror("Ошибка", "Пароли не совпадают!")
            return False
            
        # Проверка согласия
        if not self.agree_var.get():
            messagebox.showerror("Ошибка", "Вы должны согласиться с условиями!")
            return False
            
        return True
        
    def submit_form(self):
        if self.validate_form():
            username = self.username_entry.get()
            email = self.email_entry.get()
            gender = self.gender_var.get()
            interests = [k for k, v in self.interests.items() if v.get()]
            
            messagebox.showinfo("Успех", 
                              f"Регистрация успешна!\n\n"
                              f"Имя: {username}\n"
                              f"Email: {email}\n"
                              f"Пол: {gender}\n"
                              f"Интересы: {', '.join(interests)}")
            
    def clear_form(self):
        self.username_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.confirm_password_entry.delete(0, tk.END)
        self.gender_var.set("not_specified")
        self.day_var.set("")
        self.month_var.set("")
        self.year_var.set("")
        for var in self.interests.values():
            var.set(False)
        self.agree_var.set(False)

# Пример использования:
root = tk.Tk()
form = RegistrationForm(root)
root.mainloop()
```

</details>

---

## Требования к отчету
- Исходный код всех созданных приложений
- Скриншоты интерфейсов
- Описание использования каждого виджета
- Объяснение обработки событий виджетов

## Критерии оценки
- Функциональность виджетов: 50%
- Удобство интерфейса: 30%
- Качество кода: 20%
