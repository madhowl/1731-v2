# Практическое занятие 22: Tkinter - управление макетом

## Цель занятия
Изучить основные менеджеры геометрии в Tkinter (pack, grid, place), научиться создавать сложные макеты интерфейсов и понимать принципы размещения виджетов в окне.

## Задачи
1. Освоить менеджер pack для простых макетов
2. Изучить менеджер grid для табличных макетов
3. Научиться использовать менеджер place для точного позиционирования
4. Комбинировать менеджеры для создания сложных интерфейсов
5. Создать адаптивный интерфейс

## Ход работы

### 1. Основы менеджера pack

```python
import tkinter as tk
from tkinter import ttk

def demo_pack_vertical(parent):
    """
    Демонстрация вертикального макета
    
    Args:
        parent: Родительский виджет
    """
    # ВАШ КОД ЗДЕСЬ - создайте вертикальный макет
    # Используйте side=tk.TOP, fill=tk.BOTH, expand=True
    pass
```

---

## 1. Теоретическая часть: Менеджеры геометрии

### Уровень 1 - Начальный

#### Задание 1.1: Менеджер pack

Создайте вертикальный и горизонтальный макеты:

```python
import tkinter as tk
from tkinter import ttk

class PackDemo:
    """
    Демонстрация менеджера pack
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Менеджер pack")
        self.root.geometry("400x350")
        
        # ВАШ КОД ЗДЕСЬ - создайте вертикальный макет с кнопками
        pass
        
    def create_vertical_layout(self, parent):
        """
        Создает вертикальный макет
        
        Args:
            parent: Родительский виджет
        """
        # ВАШ КОД ЗДЕСЬ - создайте frame и добавьте кнопки
        # Используйте pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)
        pass
        
    def create_horizontal_layout(self, parent):
        """
        Создает горизонтальный макет
        
        Args:
            parent: Родительский виджет
        """
        # ВАШ КОД ЗДЕСЬ - создайте панель инструментов
        # Используйте pack(side=tk.LEFT, padx=2)
        pass
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import tkinter as tk
from tkinter import ttk

class PackDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Менеджер pack")
        self.root.geometry("400x350")
        
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Вертикальный макет:", font=('Arial', 12, 'bold')).pack(pady=5)
        
        # Вертикальный макет
        for i in range(5):
            btn = ttk.Button(main_frame, text=f"Кнопка {i+1}")
            btn.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=15)
        
        ttk.Label(main_frame, text="Горизонтальный макет:", font=('Arial', 12, 'bold')).pack(pady=5)
        
        # Горизонтальный макет
        toolbar = ttk.Frame(main_frame)
        toolbar.pack(fill=tk.X)
        
        for text in ["Новый", "Открыть", "Сохранить", "Выход"]:
            btn = ttk.Button(toolbar, text=text)
            btn.pack(side=tk.LEFT, padx=2)

root = tk.Tk()
demo = PackDemo(root)
root.mainloop()
```

</details>

#### Задание 1.2: Менеджер grid

Освойте табличное размещение:

```python
import tkinter as tk
from tkinter import ttk

class GridDemo:
    """
    Демонстрация менеджера grid
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Менеджер grid")
        
        # ВАШ КОД ЗДЕСЬ - создайте форму с grid
        # Используйте row, column, rowspan, columnspan, sticky
        pass
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import tkinter as tk
from tkinter import ttk

class GridDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Менеджер grid")
        self.root.geometry("400x300")
        
        main_frame = ttk.Frame(root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Форма ввода
        labels = ["Имя:", "Email:", "Телефон:", "Адрес:"]
        
        for i, label_text in enumerate(labels):
            lbl = ttk.Label(main_frame, text=label_text)
            lbl.grid(row=i, column=0, sticky=tk.W, padx=5, pady=10)
            
            entry = ttk.Entry(main_frame, width=30)
            entry.grid(row=i, column=1, padx=5, pady=10)
        
        # Кнопка с объединением колонок
        btn = ttk.Button(main_frame, text="Отправить")
        btn.grid(row=len(labels), column=0, columnspan=2, pady=20)

root = tk.Tk()
demo = GridDemo(root)
root.mainloop()
```

</details>

### Уровень 2 - Средний

#### Задание 2.1: Менеджер place

Изучите абсолютное позиционирование:

```python
class PlaceDemo:
    """
    Демонстрация менеджера place
    """
    def __init__(self, root):
        self.root = root
        
        # ВАШ КОД ЗДЕСЬ - используйте place для позиционирования
        # x, y - абсолютные координаты
        # relx, rely - относительные (0-1)
        # relwidth, relheight - относительные размеры
        pass
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import tkinter as tk
from tkinter import ttk

class PlaceDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Менеджер place")
        self.root.geometry("500x400")
        
        frame = ttk.Frame(root, borderwidth=2, relief=tk.GROOVE)
        frame.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.8)
        
        # Абсолютное позиционирование
        ttk.Label(frame, text="Левый верхний (x=10, y=10)").place(x=10, y=10)
        ttk.Label(frame, text="Правый нижний").place(x=300, y=250)
        
        # Центр
        ttk.Label(frame, text="ЦЕНТР", background="lightblue").place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Область
        ttk.Label(frame, text="Область", background="lightgreen").place(relx=0.2, rely=0.2, relwidth=0.6, relheight=0.3)

root = tk.Tk()
demo = PlaceDemo(root)
root.mainloop()
```

</details>

#### Задание 2.2: Комбинирование менеджеров

Создайте сложный макет:

```python
class ComplexLayout:
    """
    Комбинирование менеджеров
    """
    def __init__(self, root):
        # ВАШ КОД ЗДЕСЬ - создайте:
        # Меню (pack)
        # Тулбар (pack)
        # Боковую панель (pack + grid)
        # Основную область (pack)
        # Статус бар (pack)
        pass
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import tkinter as tk
from tkinter import ttk

class ComplexLayout:
    def __init__(self, root):
        self.root = root
        self.root.title("Сложный макет")
        self.root.geometry("700x500")
        
        # Меню
        menubar = tk.Menu(root)
        root.config(menu=menubar)
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Выход", command=root.quit)
        
        # Тулбар
        toolbar = ttk.Frame(root, relief=tk.RAISED)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        for text in ["Новый", "Открыть", "Сохранить"]:
            ttk.Button(toolbar, text=text).pack(side=tk.LEFT, padx=2, pady=2)
        
        # Боковая панель + основная область
        content = ttk.PanedWindow(root, orient=tk.HORIZONTAL)
        content.pack(fill=tk.BOTH, expand=True)
        
        sidebar = ttk.Frame(content, width=150)
        ttk.Label(sidebar, text="Сайдбар").pack(pady=20)
        for i in range(5):
            ttk.Button(sidebar, text=f"Пункт {i+1}").pack(pady=2)
        
        content.add(sidebar)
        
        main_area = ttk.Frame(content)
        ttk.Label(main_area, text="Основная область", font=('Arial', 14)).pack(pady=20)
        
        # Форма в main_area с grid
        for i, label in enumerate(["Поле 1:", "Поле 2:", "Поле 3:"]):
            ttk.Label(main_area, text=label).grid(row=i, column=0, padx=5, pady=5, sticky=tk.W)
            ttk.Entry(main_area, width=30).grid(row=i, column=1, padx=5, pady=5)
        
        content.add(main_area)
        
        # Статус бар
        status = ttk.Label(root, text="Готов", relief=tk.SUNKEN, anchor=tk.W)
        status.pack(side=tk.BOTTOM, fill=tk.X)

root = tk.Tk()
app = ComplexLayout(root)
root.mainloop()
```

</details>

### Уровень 3 - Продвинутый

#### Задание 3.1: Адаптивный интерфейс

Создайте приложение с адаптивным дизайном:

```python
class ResponsiveApp:
    """
    Адаптивный интерфейс
    """
    def __init__(self, root):
        self.root = root
        
        # ВАШ КОД ЗДЕСЬ - создайте интерфейс с:
        # weight для реагирования на изменение размера
        # minwidth/minheight для минимальных размеров
        # Скроллбар для больших областей
        pass
        
    def setup_resizable(self):
        """
        Настраивает адаптивность
        """
        # ВАШ КОД ЗДЕСЬ - используйте columnconfigure и rowconfigure с weight
        pass
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import tkinter as tk
from tkinter import ttk

class ResponsiveApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Адаптивный интерфейс")
        self.root.geometry("600x400")
        
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Настройка весов для адаптивности
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        
        # Левая панель (фиксированная ширина)
        left = ttk.Frame(main_frame, width=150)
        left.grid(row=0, column=0, sticky=(tk.N, tk.S), padx=(0, 10))
        
        ttk.Label(left, text="Меню", font=('Arial', 12, 'bold')).pack(pady=10)
        
        for i in range(5):
            btn = ttk.Button(left, text=f"Пункт {i+1}")
            btn.pack(fill=tk.X, pady=2)
        
        # Правая панель (растягивается)
        right = ttk.Frame(main_frame)
        right.grid(row=0, column=1, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        right.rowconfigure(0, weight=1)
        right.columnconfigure(0, weight=1)
        
        # Текстовая область со скроллбаром
        text_frame = ttk.Frame(right)
        text_frame.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        text_frame.rowconfigure(0, weight=1)
        text_frame.columnconfigure(0, weight=1)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        text = tk.Text(text_frame, yscrollcommand=scrollbar.set)
        text.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        
        scrollbar.config(command=text.yview)
        
        # Кнопки внизу
        btn_frame = ttk.Frame(right)
        btn_frame.grid(row=1, column=0, sticky=(tk.E, tk.W), pady=(10, 0))
        
        ttk.Button(btn_frame, text="Сохранить").pack(side=tk.RIGHT, padx=5)
        ttk.Button(btn_frame, text="Очистить").pack(side=tk.RIGHT)

root = tk.Tk()
app = ResponsiveApp(root)
root.mainloop()
```

</details>

---

## Требования к отчету
- Исходный код всех созданных приложений
- Скриншоты интерфейсов
- Описание использованных менеджеров геометрии
- Объяснение принципов адаптивного дизайна

## Критерии оценки
- Функциональность: 50%
- Качество кода: 20%
- Документация: 15%
- Сложность реализации: 15%
