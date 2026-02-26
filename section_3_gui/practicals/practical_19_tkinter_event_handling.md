# Практическое занятие 19: Tkinter - обработка событий

## Цель занятия
Изучить механизмы обработки событий в Tkinter, включая привязку обработчиков к виджетам, работу с различными типами событий и создание интерактивных приложений.

## Задачи
1. Освоить метод bind() для привязки обработчиков событий
2. Изучить обработку событий мыши (клики, движение, перетаскивание)
3. Научиться обрабатывать события клавиатуры
4. Реализовать передачу данных через события
5. Создать интерактивное приложение «Рисовалка»

## Ход работы

### 1. Основы обработки событий

Создайте файл `event_handling.py` и реализуйте функции для работы с событиями:

#### Обработка событий мыши

```python
import tkinter as tk
from tkinter import ttk

def create_canvas_with_mouse_events(parent, width=400, height=300):
    """
    Создает Canvas с обработкой событий мыши
    
    Args:
        parent: Родительский виджет
        width: Ширина холста
        height: Высота холста
        
    Returns:
        tk.Canvas: Холст с привязанными событиями
    """
    # ВАШ КОД ЗДЕСЬ - создайте Canvas и привяжите обработчики событий:
    # <Button-1> - левый клик
    # <Button-3> - правый клик
    # <B1-Motion> - перетаскивание с левой кнопкой
    # <Motion> - движение мыши
    pass  # Замените на ваш код
```

#### Обработка событий клавиатуры

```python
def create_widget_with_keyboard_events(parent):
    """
    Создает виджет с обработкой событий клавиатуры
    
    Args:
        parent: Родительский виджет
        
    Returns:
        tk.Widget: Виджет с привязанными событиями клавиатуры
    """
    # ВАШ КОД ЗДЕСЬ - привяжите обработчики:
    # <Key> - любая клавиша
    # <Return> - Enter
    # <Escape> - Escape
    # <Control-c> - Ctrl+C
    pass  # Замените на ваш код
```

---

## 1. Теоретическая часть: Обработка событий в Tkinter

### Уровень 1 - Начальный

#### Задание 1.1: Обработка кликов мыши

Создайте приложение с Canvas, на котором реализуется обработка кликов:

```python
import tkinter as tk
from tkinter import ttk

class MouseEventDemo:
    """
    Демонстрация обработки событий мыши
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Обработка кликов мыши")
        self.root.geometry("500x400")
        
        # ВАШ КОД ЗДЕСЬ - создайте основные переменные:
        # Счетчик кликов
        # Текущие координаты
        # Список фигур
        pass  # Замените на ваш код
        
    def create_canvas_area(self):
        """
        Создает область Canvas для рисования
        """
        # ВАШ КОД ЗДЕСЬ - создайте Canvas
        # Привяжите обработчики событий мыши:
        # <Button-1> - левый клик (рисование круга)
        # <Button-3> - правый клик (рисование квадрата)
        # <Motion> - отображение координат
        pass  # Замените на ваш код
        
    def on_left_click(self, event):
        """
        Обрабатывает левый клик мыши
        
        Args:
            event: Объект события
        """
        # ВАШ КОД ЗДЕСЬ - нарисуйте круг по клику
        pass  # Замените на ваш код
        
    def on_right_click(self, event):
        """
        Обрабатывает правый клик мыши
        
        Args:
            event: Объект события
        """
        # ВАШ КОД ЗДЕСЬ - нарисуйте квадрат по клику
        pass  # Замените на ваш код
        
    def on_mouse_move(self, event):
        """
        Обрабатывает движение мыши
        
        Args:
            event: Объект события
        """
        # ВАШ КОД ЗДЕСЬ - обновите отображение координат
        pass  # Замените на ваш код

# Пример использования:
# root = tk.Tk()
# demo = MouseEventDemo(root)
# root.mainloop()
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import tkinter as tk
from tkinter import ttk

class MouseEventDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Обработка кликов мыши")
        self.root.geometry("500x400")
        
        self.click_count = 0
        self.shapes = []
        
        self.create_ui()
        
    def create_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Метка для отображения информации
        self.info_label = ttk.Label(main_frame, text="Кликните на холсте")
        self.info_label.pack(pady=5)
        
        # Метка для координат
        self.coord_label = ttk.Label(main_frame, text="Координаты: - , -")
        self.coord_label.pack(pady=5)
        
        # Canvas
        self.canvas = tk.Canvas(main_frame, width=450, height=300, bg="white")
        self.canvas.pack()
        
        # Привязка событий
        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.canvas.bind("<Motion>", self.on_mouse_move)
        
    def on_left_click(self, event):
        self.click_count += 1
        x, y = event.x, event.y
        
        # Рисуем круг
        radius = 20
        self.canvas.create_oval(x - radius, y - radius, x + radius, y + radius,
                                fill="blue", outline="darkblue")
        
        self.info_label.config(text=f"Левый клик #{self.click_count}")
        
    def on_right_click(self, event):
        x, y = event.x, event.y
        
        # Рисуем квадрат
        size = 40
        self.canvas.create_rectangle(x - size//2, y - size//2,
                                     x + size//2, y + size//2,
                                     fill="red", outline="darkred")
        
        self.info_label.config(text=f"Правый клик")
        
    def on_mouse_move(self, event):
        self.coord_label.config(text=f"Координаты: {event.x}, {event.y}")

# Пример использования:
root = tk.Tk()
demo = MouseEventDemo(root)
root.mainloop()
```

</details>

#### Задание 1.2: Обработка клавиатуры

Разработайте приложение с управлением объектом с клавиатуры:

```python
import tkinter as tk
from tkinter import ttk

class KeyboardEventDemo:
    """
    Демонстрация обработки событий клавиатуры
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Управление с клавиатуры")
        
        # ВАШ КОД ЗДЕСЬ - создайте переменные для позиции объекта
        # и цвета
        pass  # Замените на ваш код
        
    def create_game_area(self):
        """
        Создает игровую область с управлением
        """
        # ВАШ КОД ЗДЕСЬ - создайте Canvas
        # Привяжите обработчики клавиатуры:
        # <Key> или <KeyPress> - нажатие клавиши
        # Стрелки -мещение объекта пере
        # Буквы - изменение цвета
        # Ctrl+<Key> - комбинации клавиш
        pass  # Замените на ваш код
        
    def on_key_press(self, event):
        """
        Обрабатывает нажатие клавиши
        
        Args:
            event: Объект события
        """
        # ВАШ КОД ЗДЕСЬ - обработайте нажатия:
        # Стрелки - перемещение
        # R, G, B - изменение цвета
        # Ctrl+Q - выход
        pass  # Замените на ваш код
        
    def move_object(self, dx, dy):
        """
        Перемещает объект
        
        Args:
            dx: Смещение по X
            dy: Смещение по Y
        """
        # ВАШ КОД ЗДЕСЬ - переместите объект
        pass  # Замените на ваш код
        
    def change_color(self, color):
        """
        Изменяет цвет объекта
        
        Args:
            color: Новый цвет
        """
        # ВАШ КОД ЗДЕСЬ - измените цвет объекта
        pass  # Замените на ваш код

# Пример использования:
# root = tk.Tk()
# demo = KeyboardEventDemo(root)
# root.mainloop()
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import tkinter as tk
from tkinter import ttk

class KeyboardEventDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Управление с клавиатуры")
        self.root.geometry("500x400")
        
        # Позиция объекта
        self.x = 225
        self.y = 175
        self.step = 20
        
        # Цвет объекта
        self.colors = {"red": "красный", "green": "зеленый", 
                      "blue": "синий", "yellow": "желтый"}
        self.current_color = "red"
        
        self.create_ui()
        
    def create_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Инструкция
        info_text = ("Управление:\n"
                    "Стрелки - перемещение\n"
                    "R - красный, G - зеленый, B - синий, Y - желтый\n"
                    "Ctrl+Q - выход")
        
        ttk.Label(main_frame, text=info_text, justify=tk.LEFT).pack(pady=5)
        
        # Canvas
        self.canvas = tk.Canvas(main_frame, width=450, height=300, bg="white")
        self.canvas.pack(pady=10)
        
        # Рисуем объект
        self.object_id = self.canvas.create_oval(
            self.x - 25, self.y - 25, self.x + 25, self.y + 25,
            fill=self.current_color, outline="black"
        )
        
        # Метка статуса
        self.status_label = ttk.Label(main_frame, text="Позиция: 225, 175 | Цвет: красный")
        self.status_label.pack()
        
        # Фокус на Canvas для обработки клавиш
        self.canvas.focus_set()
        self.canvas.bind("<Key>", self.on_key_press)
        
    def on_key_press(self, event):
        # Перемещение стрелками
        if event.keysym == "Up":
            self.move_object(0, -self.step)
        elif event.keysym == "Down":
            self.move_object(0, self.step)
        elif event.keysym == "Left":
            self.move_object(-self.step, 0)
        elif event.keysym == "Right":
            self.move_object(self.step, 0)
            
        # Изменение цвета
        elif event.keysym.lower() == "r":
            self.change_color("red")
        elif event.keysym.lower() == "g":
            self.change_color("green")
        elif event.keysym.lower() == "b":
            self.change_color("blue")
        elif event.keysym.lower() == "y":
            self.change_color("yellow")
            
        # Выход по Ctrl+Q
        elif event.keysym.lower() == "q" and event.state & 4:
            self.root.quit()
            
    def move_object(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy
        
        # Проверка границ
        if 25 <= new_x <= 425 and 25 <= new_y <= 275:
            self.x = new_x
            self.y = new_y
            self.canvas.move(self.object_id, dx, dy)
            self.update_status()
            
    def change_color(self, color):
        self.current_color = color
        self.canvas.itemconfig(self.object_id, fill=color)
        self.update_status()
        
    def update_status(self):
        color_name = self.colors.get(self.current_color, self.current_color)
        self.status_label.config(text=f"Позиция: {self.x}, {self.y} | Цвет: {color_name}")

# Пример использования:
root = tk.Tk()
demo = KeyboardEventDemo(root)
root.mainloop()
```

</details>

### Уровень 2 - Средний

#### Задание 2.1: Передача данных через события

Создайте приложение с несколькими кнопками и передачей данных:

```python
import tkinter as tk
from tkinter import ttk

class DataPassingDemo:
    """
    Демонстрация передачи данных через события
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Передача данных")
        
        # ВАШ КОД ЗДЕСЬ - создайте счетчик и историю нажатий
        pass  # Замените на ваш код
        
    def create_buttons(self):
        """
        Создает кнопки с обработчиками
        """
        # ВАШ КОД ЗДЕСЬ - создайте кнопки:
        # Используйте lambda-функции для передачи параметров
        # Передавайте данные о виджете через атрибуты события
        pass  # Замените на ваш код
        
    def on_button_click(self, button_id, event=None):
        """
        Обрабатывает нажатие кнопки
        
        Args:
            button_id: Идентификатор кнопки
            event: Объект события (опционально)
        """
        # ВАШ КОД ЗДЕСЬ - обработайте нажатие
        pass  # Замените на ваш код

# Пример использования:
# root = tk.Tk()
# demo = DataPassingDemo(root)
# root.mainloop()
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import tkinter as tk
from tkinter import ttk

class DataPassingDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Передача данных через события")
        self.root.geometry("400x300")
        
        self.click_history = []
        
        self.create_ui()
        
    def create_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        ttk.Label(main_frame, text="Передача данных в обработчики", 
                  font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Кнопки с разными способами передачи данных
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)
        
        # Способ 1: Lambda с параметрами
        for i in range(1, 4):
            btn = ttk.Button(btn_frame, text=f"Кнопка {i}",
                            command=lambda i=i: self.on_button_click(i))
            btn.pack(pady=5)
        
        # Способ 2: Кнопки с передачей данных через атрибуты виджета
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=15)
        
        data_btn_frame = ttk.Frame(main_frame)
        data_btn_frame.pack(pady=10)
        
        # Кнопка с данными
        self.data_btn = ttk.Button(data_btn_frame, text="Кнопка с данными",
                                  command=self.on_data_button_click)
        self.data_btn.pack()
        
        # Привязка события с передачей данных
        self.data_btn.bind("<Button-1>", lambda e, btn=self.data_btn: 
                         self.on_button_with_event(e, btn))
        
        # История нажатий
        ttk.Label(main_frame, text="История нажатий:").pack(anchor=tk.W)
        
        self.history_text = tk.Text(main_frame, height=6, width=40, state=tk.DISABLED)
        self.history_text.pack(pady=5)
        
    def on_button_click(self, button_id):
        self.click_history.append(f"Нажата кнопка {button_id}")
        self.update_history()
        
    def on_data_button_click(self):
        self.click_history.append("Нажата кнопка с данными")
        self.update_history()
        
    def on_button_with_event(self, event, button):
        # Получение данных из события
        x, y = event.x, event.y
        widget_name = button.cget('text')
        self.click_history.append(f"{widget_name} в позиции ({x}, {y})")
        self.update_history()
        
    def update_history(self):
        self.history_text.config(state=tk.NORMAL)
        self.history_text.delete(1.0, tk.END)
        for item in self.click_history[-5:]:
            self.history_text.insert(tk.END, item + "\n")
        self.history_text.config(state=tk.DISABLED)

# Пример использования:
root = tk.Tk()
demo = DataPassingDemo(root)
root.mainloop()
```

</details>

#### Задание 2.2: Кастомные события

Реализуйте систему пользовательских событий:

```python
import tkinter as tk
from tkinter import ttk

class CustomEventDemo:
    """
    Демонстрация кастомных событий
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Кастомные события")
        
        # ВАШ КОД ЗДЕСЬ - создайте генератор событий
        pass  # Замените на ваш код
        
    def create_event_system(self):
        """
        Создает систему кастомных событий
        """
        # ВАШ КОД ЗДЕСЬ - реализуйте:
        # Создание собственных событий с generate_event()
        # Обработка через bind()
        # Передача данных в событии
        pass  # Замените на ваш код
        
    def trigger_custom_event(self, event_name, data=None):
        """
        Генерирует кастомное событие
        
        Args:
            event_name: Имя события
            data: Данные для передачи
        """
        # ВАШ КОД ЗДЕСЬ - сгенерируйте событие
        pass  # Замените на ваш код

# Пример использования:
# root = tk.Tk()
# demo = CustomEventDemo(root)
# root.mainloop()
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import tkinter as tk
from tkinter import ttk

class CustomEventDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Кастомные события")
        self.root.geometry("400x350")
        
        self.event_count = 0
        
        self.create_ui()
        self.setup_custom_events()
        
    def create_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Система кастомных событий", 
                  font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Кнопки для генерации событий
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Событие: Пользователь вошел",
                  command=lambda: self.trigger_event("<<UserLogin>>")).pack(pady=5)
        
        ttk.Button(btn_frame, text="Событие: Данные сохранены",
                  command=lambda: self.trigger_event("<<DataSaved>>")).pack(pady=5)
        
        ttk.Button(btn_frame, text="Событие: Ошибка",
                  command=lambda: self.trigger_event("<<Error>>")).pack(pady=5)
        
        # Лог событий
        ttk.Label(main_frame, text="История событий:").pack(anchor=tk.W, pady=(20, 5))
        
        self.event_log = tk.Text(main_frame, height=8, width=40, state=tk.DISABLED)
        self.event_log.pack(pady=5)
        
    def setup_custom_events(self):
        # Привязка обработчиков к кастомным событиям
        self.root.bind("<<UserLogin>>", self.on_user_login)
        self.root.bind("<<DataSaved>>", self.on_data_saved)
        self.root.bind("<<Error>>", self.on_error)
        
    def trigger_event(self, event_name):
        self.event_count += 1
        
        # Генерация события
        self.root.event_generate(event_name, when="tail")
        
    def on_user_login(self, event):
        self.log_event(f"Событие #{self.event_count}: Пользователь вошел в систему")
        
    def on_data_saved(self, event):
        self.log_event(f"Событие #{self.event_count}: Данные успешно сохранены")
        
    def on_error(self, event):
        self.log_event(f"Событие #{self.event_count}: Произошла ошибка!")
        
    def log_event(self, message):
        self.event_log.config(state=tk.NORMAL)
        self.event_log.insert(tk.END, message + "\n")
        self.event_log.see(tk.END)
        self.event_log.config(state=tk.DISABLED)

# Пример использования:
root = tk.Tk()
demo = CustomEventDemo(root)
root.mainloop()
```

</details>

### Уровень 3 - Продвинутый

#### Задание 3.1: Создание приложения «Рисовалка»

Разработайте интерактивное приложение «Рисовалка»:

```python
import tkinter as tk
from tkinter import ttk, colorchooser, filedialog

class DrawingApp:
    """
    Приложение для рисования
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Рисовалка")
        
        # ВАШ КОД ЗДЕСЬ - инициализируйте переменные:
        # Текущий инструмент (карандаш, линия, прямоугольник, эллипс)
        # Текущий цвет
        # Текущая толщина линии
        # Состояние рисования (рисуем или нет)
        # Координаты начальной точки
        pass  # Замените на ваш код
        
    def create_toolbar(self):
        """
        Создает панель инструментов
        """
        # ВАШ КОД ЗДЕСЬ - создайте кнопки выбора инструментов
        # Карандаш, Линия, Прямоугольник, Эллипс, Ластик
        pass  # Замените на ваш код
        
    def create_canvas(self):
        """
        Создает холст для рисования
        """
        # ВАШ КОД ЗДЕСЬ - создайте Canvas с обработкой:
        # <B1-Motion> - рисование при движении
        # <Button-1> - начало рисования фигуры
        # <ButtonRelease-1> - конец рисования
        pass  # Замените на ваш код
        
    def start_drawing(self, event):
        """
        Начинает рисование
        
        Args:
            event: Событие
        """
        # ВАШ КОД ЗДЕСЬ - сохраните начальную позицию
        pass  # Замените на ваш код
        
    def draw(self, event):
        """
        Рисует (для карандаша)
        
        Args:
            event: Событие
        """
        # ВАШ КОД ЗДЕСЬ - рисуйте линию до текущей позиции
        pass  # Замените на ваш код
        
    def stop_drawing(self, event):
        """
        Завершает рисование
        
        Args:
            event: Событие
        """
        # ВАШ КОД ЗДЕСЬ - завершите рисование фигуры
        pass  # Замените на ваш код
        
    def select_tool(self, tool):
        """
        Выбирает инструмент
        
        Args:
            tool: Имя инструмента
        """
        # ВАШ КОД ЗДЕСЬ - измените текущий инструмент
        pass  # Замените на ваш код
        
    def select_color(self):
        """
        Выбирает цвет
        """
        # ВАШ КОД ЗДЕСЬ - откройте диалог выбора цвета
        pass  # Замените на ваш код
        
    def clear_canvas(self):
        """
        Очищает холст
        """
        # ВАШ КОД ЗДЕСЬ - очистите холст
        pass  # Замените на ваш код

# Пример использования:
# root = tk.Tk()
# app = DrawingApp(root)
# root.mainloop()
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import tkinter as tk
from tkinter import ttk, colorchooser, filedialog

class DrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Рисовалка")
        self.root.geometry("800x600")
        
        # Состояние
        self.current_tool = "pencil"
        self.current_color = "black"
        self.line_width = 2
        self.drawing = False
        self.start_x = None
        self.start_y = None
        self.last_x = None
        self.last_y = None
        
        self.create_toolbar()
        self.create_color_bar()
        self.create_canvas()
        self.create_status_bar()
        
    def create_toolbar(self):
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        tools = [("Карандаш", "pencil"), ("Линия", "line"), 
                ("Прямоугольник", "rectangle"), ("Эллипс", "ellipse"),
                ("Ластик", "eraser")]
        
        for text, tool in tools:
            btn = ttk.Button(toolbar, text=text, 
                           command=lambda t=tool: self.select_tool(t))
            btn.pack(side=tk.LEFT, padx=2, pady=2)
            
        # Очистка
        ttk.Button(toolbar, text="Очистить", 
                  command=self.clear_canvas).pack(side=tk.RIGHT, padx=5)
                  
    def create_color_bar(self):
        colors_frame = ttk.Frame(self.root)
        colors_frame.pack(side=tk.TOP, fill=tk.X)
        
        color_btn = ttk.Button(colors_frame, text="Выбрать цвет",
                              command=self.select_color)
        color_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Цветные кнопки
        for color in ["black", "red", "blue", "green", "yellow", "orange", "purple"]:
            btn = tk.Button(colors_frame, bg=color, width=3,
                          command=lambda c=color: self.set_color(c))
            btn.pack(side=tk.LEFT, padx=2)
            
    def create_canvas(self):
        self.canvas = tk.Canvas(self.root, bg="white", cursor="crosshair")
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Привязка событий
        self.canvas.bind("<Button-1>", self.start_drawing)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_drawing)
        
    def create_status_bar(self):
        self.status = ttk.Label(self.root, text="Инструмент: Карандаш | Цвет: black")
        self.status.pack(side=tk.BOTTOM, fill=tk.X)
        
    def select_tool(self, tool):
        self.current_tool = tool
        tool_names = {"pencil": "Карандаш", "line": "Линия",
                     "rectangle": "Прямоугольник", "ellipse": "Эллипс",
                     "eraser": "Ластик"}
        self.status.config(text=f"Инструмент: {tool_names[tool]} | Цвет: {self.current_color}")
        
    def set_color(self, color):
        self.current_color = color
        self.status.config(text=f"Инструмент: ... | Цвет: {color}")
        
    def select_color(self):
        color = colorchooser.askcolor(color=self.current_color)[1]
        if color:
            self.set_color(color)
            
    def start_drawing(self, event):
        self.drawing = True
        self.start_x = event.x
        self.start_y = event.y
        self.last_x = event.x
        self.last_y = event.y
        
        if self.current_tool == "pencil" or self.current_tool == "eraser":
            self.prev_shape = None
            
    def draw(self, event):
        if not self.drawing:
            return
            
        if self.current_tool == "pencil":
            color = self.current_color
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                  fill=color, width=self.line_width)
            self.last_x = event.x
            self.last_y = event.y
            
        elif self.current_tool == "eraser":
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                  fill="white", width=10)
            self.last_x = event.x
            self.last_y = event.y
            
    def stop_drawing(self, event):
        if not self.drawing:
            return
            
        self.drawing = False
        
        if self.current_tool == "line":
            self.canvas.create_line(self.start_x, self.start_y, event.x, event.y,
                                   fill=self.current_color, width=self.line_width)
                                   
        elif self.current_tool == "rectangle":
            self.canvas.create_rectangle(self.start_x, self.start_y, event.x, event.y,
                                         outline=self.current_color, width=self.line_width)
                                         
        elif self.current_tool == "ellipse":
            self.canvas.create_oval(self.start_x, self.start_y, event.x, event.y,
                                   outline=self.current_color, width=self.line_width)
                                   
    def clear_canvas(self):
        self.canvas.delete("all")

# Пример использования:
root = tk.Tk()
app = DrawingApp(root)
root.mainloop()
```

</details>

---

## Требования к отчету
- Исходный код всех созданных приложений
- Примеры работы с различными типами событий
- Объяснение передачи данных через события
- Описание архитектуры приложения «Рисовалка»

## Критерии оценки
- Корректная обработка событий: 50%
- Использование различных типов событий: 30%
- Качество кода и документация: 20%
