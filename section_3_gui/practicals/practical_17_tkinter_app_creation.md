# Практическое занятие 17: Создание GUI с помощью Tkinter

## Цель занятия
Изучить основы создания графических интерфейсов с использованием библиотеки Tkinter, включая создание окон, виджетов, обработку событий и построение интерфейса.

## Задачи
1. Освоить создание и настройку главного окна приложения
2. Изучить основные виджеты Tkinter (кнопки, метки, поля ввода)
3. Научиться использовать менеджеры размещения (pack, grid, place)
4. Реализовать обработку событий в приложении
5. Создать комплексное приложение «Калькулятор»

## Ход работы

### 1. Создание и настройка главного окна

Создайте файл `main_window.py` и реализуйте функции для работы с окном:

#### Основные параметры окна

```python
import tkinter as tk import ttk


from tkinterdef create_main_window():
    """
    Создает главное окно приложения с базовыми настройками
    
    Returns:
        tk.Tk: Главное окно приложения
    """
    # ВАШ КОД ЗДЕСЬ - создайте окно с заголовком, размерами и положением
    pass  # Замените на ваш код

def set_window_icon(window, icon_path=None):
    """
    Устанавливает иконку для окна
    
    Args:
        window: Окно для установки иконки
        icon_path: Путь к файлу иконки
    """
    # ВАШ КОД ЗДЕСЬ - установите иконку приложения
    pass  # Замените на ваш код

def setup_window_close_handler(window, callback):
    """
    Настраивает обработчик закрытия окна
    
    Args:
        window: Окно для настройки
        callback: Функция-обработчик закрытия
    """
    # ВАШ КОД ЗДЕСЬ - реализуйте обработку закрытия окна
    pass  # Замените на ваш код
```

---

## 1. Теоретическая часть: Основы Tkinter

### Уровень 1 - Начальный

#### Задание 1.1: Создание базового окна приложения

Создайте приложение с основным окном:

```python
import tkinter as tk
from tkinter import ttk

class BasicApp:
    """
    Базовое приложение с главным окном
    """
    def __init__(self):
        # ВАШ КОД ЗДЕСЬ - создайте главное окно
        # Установите заголовок окна
        # Установите размеры (например, 800x600)
        # Установите начальное положение окна по центру экрана
        pass  # Замените на ваш код
        
    def run(self):
        # ВАШ КОД ЗДЕСЬ - запустите главный цикл приложения
        pass  # Замените на ваш код

# Пример использования:
# app = BasicApp()
# app.run()
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import tkinter as tk
from tkinter import ttk

class BasicApp:
    """
    Базовое приложение с главным окном
    """
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Мое первое приложение")
        self.root.geometry("800x600")
        
        # Центрирование окна на экране
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # Настройка обработчика закрытия окна
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
    
    def on_closing(self):
        # ВАШ КОД ЗДЕСЬ - добавьте логику при закрытии окна
        self.root.destroy()
    
    def run(self):
        self.root.mainloop()

# Пример использования:
app = BasicApp()
app.run()
```

</details>

#### Задание 1.2: Работа с основными виджетами

Создайте интерфейс с основными виджетами:

```python
import tkinter as tk
from tkinter import ttk

class WidgetDemo:
    """
    Демонстрация основных виджетов Tkinter
    """
    def __init__(self, root):
        self.root = root
        # ВАШ КОД ЗДЕСЬ - создайте фрейм для размещения виджетов
        pass  # Замените на ваш код
        
    def create_label(self, text, parent=None):
        """
        Создает текстовую метку
        
        Args:
            text: Текст метки
            parent: Родительский виджет
            
        Returns:
            tk.Label: Созданная метка
        """
        # ВАШ КОД ЗДЕСЬ - создайте и верните метку
        pass  # Замените на ваш код
        
    def create_button(self, text, command, parent=None):
        """
        Создает кнопку
        
        Args:
            text: Текст на кнопке
            command: Функция-обработчик
            parent: Родительский виджет
            
        Returns:
            tk.Button: Созданная кнопка
        """
        # ВАШ КОД ЗДЕСЬ - создайте и верните кнопку
        pass  # Замените на ваш код
        
    def create_entry(self, parent=None, width=30):
        """
        Создает поле ввода
        
        Args:
            parent: Родительский виджет
            width: Ширина поля
            
        Returns:
            tk.Entry: Созданное поле ввода
        """
        # ВАШ КОД ЗДЕСЬ - создайте и верните поле ввода
        pass  # Замените на ваш код
        
    def create_text_area(self, parent=None, width=40, height=10):
        """
        Создает текстовую область
        
        Args:
            parent: Родительский виджет
            width: Ширина
            height: Высота
            
        Returns:
            tk.Text: Созданная текстовая область
        """
        # ВАШ КОД ЗДЕСЬ - создайте и верните текстовую область
        pass  # Замените на ваш код

# Пример использования:
# root = tk.Tk()
# demo = WidgetDemo(root)
# demo.create_label("Привет, мир!", root)
# demo.create_button("Нажми меня", lambda: print("Нажато!"), root)
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import tkinter as tk
from tkinter import ttk

class WidgetDemo:
    """
    Демонстрация основных виджетов Tkinter
    """
    def __init__(self, root):
        self.root = root
        self.frame = ttk.Frame(root, padding="10")
        self.frame.pack(fill=tk.BOTH, expand=True)
        
    def create_label(self, text, parent=None):
        if parent is None:
            parent = self.frame
        label = ttk.Label(parent, text=text)
        label.pack(pady=5)
        return label
        
    def create_button(self, text, command, parent=None):
        if parent is None:
            parent = self.frame
        button = ttk.Button(parent, text=text, command=command)
        button.pack(pady=5)
        return button
        
    def create_entry(self, parent=None, width=30):
        if parent is None:
            parent = self.frame
        entry = ttk.Entry(parent, width=width)
        entry.pack(pady=5)
        return entry
        
    def create_text_area(self, parent=None, width=40, height=10):
        if parent is None:
            parent = self.frame
        text = tk.Text(parent, width=width, height=height)
        text.pack(pady=5)
        return text

# Пример использования:
root = tk.Tk()
demo = WidgetDemo(root)
demo.create_label("Привет, мир!")
demo.create_button("Нажми меня", lambda: print("Нажато!"))
entry = demo.create_entry()
text = demo.create_text_area()
root.mainloop()
```

</details>

### Уровень 2 - Средний

#### Задание 2.1: Использование менеджеров размещения

Изучите различные менеджеры размещения:

```python
import tkinter as tk
from tkinter import ttk

class LayoutDemo:
    """
    Демонстрация менеджеров размещения
    """
    def __init__(self, root):
        self.root = root
        
    def demo_pack(self, parent=None):
        """
        Демонстрация менеджера pack
        
        Args:
            parent: Родительский виджет
        """
        # ВАШ КОД ЗДЕСЬ - создайте вертикальный макет с несколькими кнопками
        # Используйте параметры: side, fill, expand, padx, pady
        pass  # Замените на ваш код
        
    def demo_grid(self, parent=None):
        """
        Демонстрация менеджера grid
        
        Args:
            parent: Родительский виджет
        """
        # ВАШ КОД ЗДЕСЬ - создайте табличный макет (например, калькулятор)
        # Используйте параметры: row, column, rowspan, columnspan, sticky
        pass  # Замените на ваш код
        
    def demo_place(self, parent=None):
        """
        Демонстрация менеджера place
        
        Args:
            parent: Родительский виджет
        """
        # ВАШ КОД ЗДЕСЬ - разместите виджеты по координатам
        # Используйте параметры: x, y, relx, rely, relwidth, relheight
        pass  # Замените на ваш код

# Пример использования:
# root = tk.Tk()
# layout_demo = LayoutDemo(root)
# layout_demo.demo_pack(root)
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import tkinter as tk
from tkinter import ttk

class LayoutDemo:
    def __init__(self, root):
        self.root = root
        
    def demo_pack(self, parent=None):
        if parent is None:
            parent = self.root
            
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Вертикальный макет
        for i in range(5):
            btn = ttk.Button(frame, text=f"Кнопка {i+1}")
            btn.pack(fill=tk.X, padx=5, pady=2)
        
        # Горизонтальный макет (панель инструментов)
        toolbar = ttk.Frame(parent)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        for text in ["Новый", "Открыть", "Сохранить"]:
            btn = ttk.Button(toolbar, text=text)
            btn.pack(side=tk.LEFT, padx=2, pady=2)
    
    def demo_grid(self, parent=None):
        if parent is None:
            parent = self.root
            
        frame = ttk.Frame(parent, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Простая форма ввода
        labels = ["Имя:", "Email:", "Телефон:"]
        for i, label_text in enumerate(labels):
            lbl = ttk.Label(frame, text=label_text)
            lbl.grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)
            
            entry = ttk.Entry(frame, width=30)
            entry.grid(row=i, column=1, padx=5, pady=5)
        
        # Кнопка с объединением колонок
        btn = ttk.Button(frame, text="Отправить")
        btn.grid(row=len(labels), column=0, columnspan=2, pady=10)
    
    def demo_place(self, parent=None):
        if parent is None:
            parent = self.root
            
        frame = ttk.Frame(parent, width=400, height=300, borderwidth=2, relief=tk.SUNKEN)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Абсолютное позиционирование
        label1 = ttk.Label(frame, text="Левый верхний угол")
        label1.place(x=10, y=10)
        
        # Относительное позиционирование (центр)
        label2 = ttk.Label(frame, text="По центру")
        label2.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Позиционирование с размерами
        label3 = ttk.Label(frame, text="Область", background="lightblue")
        label3.place(relx=0.2, rely=0.2, relwidth=0.6, relheight=0.3)

# Пример использования:
root = tk.Tk()
layout_demo = LayoutDemo(root)
layout_demo.demo_pack(root)
root.mainloop()
```

</details>

#### Задание 2.2: Обработка событий

Реализуйте обработку различных событий:

```python
import tkinter as tk
from tkinter import ttk

class EventHandler:
    """
    Обработчик событий в Tkinter
    """
    def __init__(self, root):
        self.root = root
        self.click_count = 0
        
    def bind_mouse_events(self, widget):
        """
        Привязывает обработчики событий мыши
        
        Args:
            widget: Виджет для привязки событий
        """
        # ВАШ КОД ЗДЕСЬ - реализуйте обработку кликов мыши
        # <Button-1> - левый клик
        # <Button-3> - правый клик
        # <Double-Button-1> - двойной клик
        pass  # Замените на ваш код
        
    def bind_keyboard_events(self, widget):
        """
        Привязывает обработчики событий клавиатуры
        
        Args:
            widget: Виджет для привязки событий
        """
        # ВАШ КОД ЗДЕСЬ - реализуйте обработку нажатий клавиш
        # <Key> - любая клавиша
        # <Return> - Enter
        # <Escape> - Escape
        pass  # Замените на ваш код
        
    def bind_widget_events(self, widget):
        """
        Привязывает обработчики событий виджета
        
        Args:
            widget: Виджет для привязки событий
        """
        # ВАШ КОД ЗДЕСЬ - реализуйте обработку событий виджета
        # <FocusIn> - получение фокуса
        # <FocusOut> - потеря фокуса
        pass  # Замените на ваш код

# Пример использования:
# root = tk.Tk()
# handler = EventHandler(root)
# canvas = tk.Canvas(root, width=400, height=300)
# canvas.pack()
# handler.bind_mouse_events(canvas)
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import tkinter as tk
from tkinter import ttk

class EventHandler:
    def __init__(self, root):
        self.root = root
        self.click_count = 0
        self.key_count = 0
        
    def bind_mouse_events(self, widget):
        # Обработка левого клика
        widget.bind("<Button-1>", self.on_left_click)
        # Обработка правого клика
        widget.bind("<Button-3>", self.on_right_click)
        # Обработка двойного клика
        widget.bind("<Double-Button-1>", self.on_double_click)
        # Перемещение мыши
        widget.bind("<Motion>", self.on_mouse_move)
        
    def on_left_click(self, event):
        self.click_count += 1
        print(f"Левый клик #{self.click_count} в точке ({event.x}, {event.y})")
        
    def on_right_click(self, event):
        print(f"Правый клик в точке ({event.x}, {event.y})")
        
    def on_double_click(self, event):
        print(f"Двойной клик в точке ({event.x}, {event.y})")
        
    def on_mouse_move(self, event):
        # Не выводим каждый раз, только при отладке
        pass
        
    def bind_keyboard_events(self, widget):
        widget.bind("<Key>", self.on_key_press)
        
    def on_key_press(self, event):
        self.key_count += 1
        print(f"Нажата клавиша #{self.key_count}: {event.keysym}")
        
    def bind_widget_events(self, widget):
        widget.bind("<FocusIn>", self.on_focus_in)
        widget.bind("<FocusOut>", self.on_focus_out)
        
    def on_focus_in(self, event):
        print("Виджет получил фокус")
        
    def on_focus_out(self, event):
        print("Виджет потерял фокус")

# Пример использования:
root = tk.Tk()
handler = EventHandler(root)

canvas = tk.Canvas(root, width=400, height=300, bg="white")
canvas.pack()

handler.bind_mouse_events(canvas)
handler.bind_keyboard_events(canvas)
handler.bind_widget_events(canvas)

root.mainloop()
```

</details>

### Уровень 3 - Продвинутый

#### Задание 3.1: Создание приложения «Калькулятор»

Создайте полноценное приложение «Калькулятор»:

```python
import tkinter as tk
from tkinter import ttk

class Calculator:
    """
    Приложение «Калькулятор» с графическим интерфейсом
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор")
        self.root.geometry("300x400")
        
        # Переменная для хранения текущего выражения
        self.expression = ""
        self.input_text = tk.StringVar()
        
        # ВАШ КОД ЗДЕСЬ - инициализируйте компоненты калькулятора
        pass  # Замените на ваш код
        
    def create_display(self):
        """
        Создает дисплей калькулятора
        """
        # ВАШ КОД ЗДЕСЬ - создайте поле для отображения ввода/результата
        pass  # Замените на ваш код
        
    def create_buttons(self):
        """
        Создает кнопки калькулятора
        """
        # ВАШ КОД ЗДЕСЬ - создайте кнопки для цифр и операций
        # Расположите их в виде сетки
        pass  # Замените на ваш код
        
    def btn_click(self, item):
        """
        Обрабатывает нажатие кнопки с цифрой или операцией
        
        Args:
            item: Символ на нажатой кнопке
        """
        # ВАШ КОД ЗДЕСЬ - реализуйте добавление символа к выражению
        pass  # Замените на ваш код
        
    def btn_clear(self):
        """
        Очищает дисплей калькулятора
        """
        # ВАШ КОД ЗДЕСЬ - очистите выражение
        pass  # Замените на ваш код
        
    def btn_equal(self):
        """
        Вычисляет результат выражения
        """
        # ВАШ КОД ЗДЕСЬ - вычислите и отобразите результат
        # Обработайте возможные ошибки
        pass  # Замените на ваш код

# Пример использования:
# root = tk.Tk()
# calc = Calculator(root)
# root.mainloop()
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import tkinter as tk
from tkinter import ttk

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор")
        self.root.geometry("300x400")
        self.root.resizable(False, False)
        
        self.expression = ""
        self.input_text = tk.StringVar()
        
        self.create_display()
        self.create_buttons()
        
    def create_display(self):
        input_frame = ttk.Frame(self.root, height=80)
        input_frame.pack(side=tk.TOP, fill=tk.X)
        
        input_field = ttk.Entry(
            input_frame, 
            textvariable=self.input_text, 
            font=('arial', 24, 'bold'),
            justify='right',
            state='readonly'
        )
        input_field.pack(fill=tk.BOTH, padx=10, pady=10)
        
    def create_buttons(self):
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Раскладка кнопок
        buttons = [
            ('C', 1, 0), ('/', 1, 1), ('*', 1, 2), ('-', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('+', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('=', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('0', 4, 3),
            ('.', 5, 0)
        ]
        
        for (text, row, col) in buttons:
            if text == '=':
                btn = ttk.Button(
                    btn_frame, 
                    text=text,
                    command=self.btn_equal
                )
            elif text == 'C':
                btn = ttk.Button(
                    btn_frame, 
                    text=text,
                    command=self.btn_clear
                )
            else:
                btn = ttk.Button(
                    btn_frame, 
                    text=text,
                    command=lambda t=text: self.btn_click(t)
                )
            
            btn.grid(row=row, column=col, sticky='nsew', padx=3, pady=3)
        
        # Настройка растяжения колонок и строк
        for i in range(4):
            btn_frame.columnconfigure(i, weight=1)
        for i in range(6):
            btn_frame.rowconfigure(i, weight=1)
            
    def btn_click(self, item):
        self.expression = self.expression + str(item)
        self.input_text.set(self.expression)
        
    def btn_clear(self):
        self.expression = ""
        self.input_text.set("")
        
    def btn_equal(self):
        try:
            result = str(eval(self.expression))
            self.input_text.set(result)
            self.expression = result
        except Exception as e:
            self.input_text.set("Ошибка")
            self.expression = ""

# Пример использования:
root = tk.Tk()
calc = Calculator(root)
root.mainloop()
```

</details>

---

## Требования к отчету
- Исходный код всех созданных приложений
- Скриншоты интерфейсов
- Описание архитектуры каждого приложения
- Объяснение использования менеджеров размещения

## Критерии оценки
- Функциональность приложений: 50%
- Качество интерфейса: 30%
- Качество кода: 20%
