# Решения для практического занятия 19: Tkinter - обработка событий

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import random
import time
from typing import Dict, Any, List, Callable
import threading


# =============================================================================
# Задание 1: Обработка кликов мыши
# =============================================================================

class MouseEventApp:
    """Приложение для обработки кликов мыши"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Задание 1: Обработка кликов мыши")
        self.root.geometry("700x600")
        
        # Canvas для рисования
        self.canvas = tk.Canvas(self.root, bg="white", width=680, height=500)
        self.canvas.pack(pady=10)
        
        # Информационная панель
        info_frame = ttk.Frame(self.root)
        info_frame.pack(fill=tk.X, padx=10)
        
        self.coord_label = ttk.Label(info_frame, text="Координаты: (0, 0)", foreground="blue")
        self.coord_label.pack(anchor=tk.W)
        
        # Кнопка для очистки холста
        ttk.Button(info_frame, text="Очистить", command=self.clear_canvas).pack(pady=5)
        
        # Привязываем события мыши
        self.canvas.bind("<Button-1>", self.left_click)  # Левый клик
        self.canvas.bind("<Button-3>", self.right_click)  # Правый клик (на Windows это Button-3)
        self.canvas.bind("<Motion>", self.mouse_move)   # Движение мыши
        self.canvas.bind("<Double-Button-1>", self.double_click)  # Двойной клик
    
    def left_click(self, event):
        """Обработка левого клика - рисует круг"""
        x, y = event.x, event.y
        self.coord_label.config(text=f"Координаты: ({x}, {y}) - ЛКМ")
        
        # Рисуем круг
        radius = 20
        self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, 
                               outline="blue", width=2, fill="")
    
    def right_click(self, event):
        """Обработка правого клика - рисует квадрат"""
        x, y = event.x, event.y
        self.coord_label.config(text=f"Координаты: ({x}, {y}) - ПКМ")
        
        # Рисуем квадрат
        size = 25
        self.canvas.create_rectangle(x-size, y-size, x+size, y+size, 
                                    outline="red", width=2, fill="")
    
    def mouse_move(self, event):
        """Обновление координат при движении мыши"""
        x, y = event.x, event.y
        # Обновляем координаты, но не меняем цвет, чтобы не перекрывать информацию о клике
        if not hasattr(self, '_last_click_time') or time.time() - self._last_click_time > 0.5:
            self.coord_label.config(text=f"Координаты: ({x}, {y})")
    
    def double_click(self, event):
        """Обработка двойного клика - очищает холст"""
        self.clear_canvas()
    
    def clear_canvas(self):
        """Очистка холста"""
        self.canvas.delete("all")
    
    def run(self):
        self.root.mainloop()


# =============================================================================
# Задание 2: Обработка клавиатуры
# =============================================================================

class KeyboardEventApp:
    """Приложение для обработки клавиатуры"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Задание 2: Обработка клавиатуры")
        self.root.geometry("700x600")
        
        # Canvas для перемещения объекта
        self.canvas = tk.Canvas(self.root, bg="lightgray", width=680, height=500)
        self.canvas.pack(pady=10)
        
        # Создаем объект для перемещения
        self.obj_x = 340
        self.obj_y = 250
        self.obj_size = 30
        self.object = self.canvas.create_rectangle(
            self.obj_x - self.obj_size//2, 
            self.obj_y - self.obj_size//2,
            self.obj_x + self.obj_size//2,
            self.obj_y + self.obj_size//2,
            fill="blue", outline="black"
        )
        
        # Информационная панель
        info_frame = ttk.Frame(self.root)
        info_frame.pack(fill=tk.X, padx=10)
        
        self.key_label = ttk.Label(info_frame, text="Последняя нажатая клавиша: -", foreground="green")
        self.key_label.pack(anchor=tk.W)
        
        # Инструкции
        instructions = tk.Label(info_frame, 
                               text="Используйте стрелки для перемещения, R/G/B для изменения цвета, Ctrl+C/V для действий",
                               font=("Arial", 10))
        instructions.pack(pady=5)
        
        # Привязываем события клавиатуры
        self.root.bind("<KeyPress>", self.key_pressed)
        self.root.bind("<Control-c>", self.ctrl_c_pressed)
        self.root.bind("<Control-v>", self.ctrl_v_pressed)
        
        # Устанавливаем фокус на окно для получения событий клавиатуры
        self.root.focus_set()
    
    def key_pressed(self, event):
        """Обработка нажатия клавиши"""
        key = event.keysym
        self.key_label.config(text=f"Последняя нажатая клавиша: {key}")
        
        # Перемещение объекта по стрелкам
        step = 10
        if key == "Left":
            self.obj_x = max(self.obj_size//2, self.obj_x - step)
        elif key == "Right":
            self.obj_x = min(680 - self.obj_size//2, self.obj_x + step)
        elif key == "Up":
            self.obj_y = max(self.obj_size//2, self.obj_y - step)
        elif key == "Down":
            self.obj_y = min(500 - self.obj_size//2, self.obj_y + step)
        elif key.lower() == "r":
            self.canvas.itemconfig(self.object, fill="red")
        elif key.lower() == "g":
            self.canvas.itemconfig(self.object, fill="green")
        elif key.lower() == "b":
            self.canvas.itemconfig(self.object, fill="blue")
        
        # Обновляем позицию объекта
        self.canvas.coords(
            self.object,
            self.obj_x - self.obj_size//2,
            self.obj_y - self.obj_size//2,
            self.obj_x + self.obj_size//2,
            self.obj_y + self.obj_size//2
        )
    
    def ctrl_c_pressed(self, event):
        """Обработка комбинации Ctrl+C"""
        self.key_label.config(text="Нажата комбинация: Ctrl+C", foreground="red")
        messagebox.showinfo("Информация", "Вы скопировали объект!")
        return "break"  # Предотвращаем дальнейшую обработку
    
    def ctrl_v_pressed(self, event):
        """Обработка комбинации Ctrl+V"""
        self.key_label.config(text="Нажата комбинация: Ctrl+V", foreground="red")
        messagebox.showinfo("Информация", "Вы вставили объект!")
        return "break"  # Предотвращаем дальнейшую обработку
    
    def run(self):
        self.root.mainloop()


# =============================================================================
# Задание 3: Передача данных через события
# =============================================================================

class DataTransferApp:
    """Приложение для передачи данных через события"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Задание 3: Передача данных через события")
        self.root.geometry("700x600")
        
        # Основной фрейм
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Фрейм для кнопок
        button_frame = ttk.LabelFrame(main_frame, text="Кнопки с передачей данных")
        button_frame.pack(fill=tk.X, pady=10)
        
        # Создаем кнопки с разными данными
        self.button_data = {}
        colors = ["красная", "зеленая", "синяя", "желтая", "оранжевая", "фиолетовая"]
        
        for i, color in enumerate(colors):
            btn = ttk.Button(
                button_frame, 
                text=f"Кнопка {i+1} ({color})", 
                command=lambda c=color, n=i+1: self.button_clicked(c, n)
            )
            btn.pack(side=tk.LEFT, padx=5, pady=5)
            self.button_data[btn] = {"color": color, "number": i+1}
        
        # Фрейм для кнопок с передачей через bind
        bind_frame = ttk.LabelFrame(main_frame, text="Кнопки с передачей через bind")
        bind_frame.pack(fill=tk.X, pady=10)
        
        self.bind_buttons = []
        for i in range(3):
            btn = ttk.Button(bind_frame, text=f"Bind Кнопка {i+1}")
            btn.pack(side=tk.LEFT, padx=5, pady=5)
            # Привязываем событие с передачей данных через lambda
            btn.bind("<Button-1>", lambda e, n=i+1: self.bind_button_clicked(e, n))
            self.bind_buttons.append(btn)
        
        # Фрейм для списка с событиями
        list_frame = ttk.LabelFrame(main_frame, text="Список с событиями")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Создаем список
        self.listbox = tk.Listbox(list_frame)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        items = ["Элемент 1", "Элемент 2", "Элемент 3", "Элемент 4", "Элемент 5"]
        for item in items:
            self.listbox.insert(tk.END, item)
        
        # Привязываем событие выбора
        self.listbox.bind("<<ListboxSelect>>", self.listbox_selected)
        
        # Метка для отображения информации
        self.info_label = ttk.Label(main_frame, text="Информация будет отображаться здесь", foreground="blue")
        self.info_label.pack(pady=10)
    
    def button_clicked(self, color, number):
        """Обработчик кнопки с передачей данных"""
        info = f"Нажата {color} кнопка #{number}"
        self.info_label.config(text=info)
        print(info)
    
    def bind_button_clicked(self, event, number):
        """Обработчик кнопки, привязанной через bind"""
        widget = event.widget
        info = f"Нажата Bind Кнопка #{number} (текст: {widget.cget('text')})"
        self.info_label.config(text=info)
        print(info)
    
    def listbox_selected(self, event):
        """Обработчик выбора в списке"""
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            value = self.listbox.get(index)
            info = f"Выбран элемент: {value} (индекс: {index})"
            self.info_label.config(text=info)
            print(info)
    
    def run(self):
        self.root.mainloop()


# =============================================================================
# Задание 4: Кастомные события
# =============================================================================

class CustomEventApp:
    """Приложение для демонстрации кастомных событий"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Задание 4: Кастомные события")
        self.root.geometry("700x600")
        
        # Основной фрейм
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas для демонстрации событий
        self.canvas = tk.Canvas(main_frame, bg="white", width=680, height=400)
        self.canvas.pack(pady=10)
        
        # Кнопки для генерации кастомных событий
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Событие 1", 
                  command=lambda: self.generate_custom_event("<<CustomEvent1>>", {"data": "Событие 1"})).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Событие 2", 
                  command=lambda: self.generate_custom_event("<<CustomEvent2>>", {"data": "Событие 2", "value": 42})).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Событие 3", 
                  command=lambda: self.generate_custom_event("<<CustomEvent3>>", {"data": "Событие 3", "source": "Button"})).pack(side=tk.LEFT, padx=5)
        
        # Кнопка для подписки/отписки
        self.subscription_button = ttk.Button(button_frame, text="Подписаться", 
                                            command=self.toggle_subscription)
        self.subscription_button.pack(side=tk.LEFT, padx=5)
        self.subscribed = True
        self._event_data = None  # Хранилище для данных кастомных событий
        
        # Метка для отображения событий
        self.event_label = ttk.Label(main_frame, text="Ожидание событий...", foreground="purple")
        self.event_label.pack(pady=10)
        
        # Текстовое поле для лога событий
        self.event_log = tk.Text(main_frame, height=8, state=tk.DISABLED)
        self.event_log.pack(fill=tk.X, pady=5)
        
        # Привязываем кастомные события
        self.root.bind("<<CustomEvent1>>", self.handle_custom_event1)
        self.root.bind("<<CustomEvent2>>", self.handle_custom_event2)
        self.root.bind("<<CustomEvent3>>", self.handle_custom_event3)
        
        # Генерируем событие через таймер
        self.schedule_periodic_event()
    
    def generate_custom_event(self, event_name, data):
        """Генерирует кастомное событие"""
        # Сохраняем данные в атрибуте экземпляра для передачи в обработчик
        self._event_data = data
        self.root.event_generate(event_name, when="tail")
    
    def handle_custom_event1(self, event):
        """Обработчик кастомного события 1"""
        data = self._event_data
        self.event_label.config(text=f"Обработано: {data}")
        self.log_event(f"CustomEvent1: {data}")
    
    def handle_custom_event2(self, event):
        """Обработчик кастомного события 2"""
        data = self._event_data
        self.event_label.config(text=f"Обработано: {data}")
        self.log_event(f"CustomEvent2: {data}")
    
    def handle_custom_event3(self, event):
        """Обработчик кастомного события 3"""
        data = self._event_data
        self.event_label.config(text=f"Обработано: {data}")
        self.log_event(f"CustomEvent3: {data}")
    
    def schedule_periodic_event(self):
        """Планирует периодическую генерацию события"""
        if self.subscribed:
            self.generate_custom_event("<<PeriodicEvent>>", {"time": time.time()})
        
        # Планируем следующее событие через 2 секунды
        self.root.after(2000, self.schedule_periodic_event)
    
    def toggle_subscription(self):
        """Переключает подписку на периодические события"""
        self.subscribed = not self.subscribed
        if self.subscribed:
            self.subscription_button.config(text="Подписаться")
            self.event_label.config(text="Подписка возобновлена")
        else:
            self.subscription_button.config(text="Отписаться")
            self.event_label.config(text="Подписка отключена")
    
    def log_event(self, event_info):
        """Логирует событие"""
        self.event_log.config(state=tk.NORMAL)
        self.event_log.insert(tk.END, f"{time.strftime('%H:%M:%S')} - {event_info}\n")
        self.event_log.see(tk.END)
        self.event_log.config(state=tk.DISABLED)
    
    def run(self):
        self.root.mainloop()


# =============================================================================
# Задание 5: Комплексное приложение "Рисовалка"
# =============================================================================

class DrawingApp:
    """Комплексное приложение "Рисовалка" с обработкой событий"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Задание 5: Комплексное приложение (Рисовалка)")
        self.root.geometry("900x700")
        
        # Переменные состояния
        self.drawing = False
        self.current_color = "black"
        self.current_tool = "pen"  # pen, rectangle, circle, eraser
        self.start_x = None
        self.start_y = None
        self.current_item = None
        
        # Создаем меню
        self.create_menu()
        
        # Создаем панель инструментов
        self.create_toolbar()
        
        # Canvas для рисования
        self.canvas = tk.Canvas(self.root, bg="white", width=880, height=600, cursor="cross")
        self.canvas.pack(pady=10)
        
        # Привязываем события мыши
        self.canvas.bind("<ButtonPress-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)
        
        # Привязываем события клавиатуры
        self.root.bind("<KeyPress>", self.key_pressed)
        
        # Устанавливаем фокус на окно для получения событий клавиатуры
        self.root.focus_set()
        
        # Статусная панель
        self.status_label = ttk.Label(self.root, text="Инструмент: Ручка | Цвет: черный", relief=tk.SUNKEN)
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM)
    
    def create_menu(self):
        """Создает меню приложения"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Меню File
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Сохранить", command=self.save_image)
        file_menu.add_command(label="Загрузить", command=self.load_image)
        file_menu.add_separator()
        file_menu.add_command(label="Очистить", command=self.clear_canvas)
        file_menu.add_command(label="Выход", command=self.root.quit)
    
    def create_toolbar(self):
        """Создает панель инструментов"""
        toolbar = ttk.Frame(self.root, relief=tk.RAISED, borderwidth=1)
        toolbar.pack(fill=tk.X, padx=10, pady=5)
        
        # Инструменты
        ttk.Label(toolbar, text="Инструменты:").pack(side=tk.LEFT, padx=(5, 10))
        
        tools = [("pen", "Ручка"), ("rectangle", "Прямоугольник"), ("circle", "Круг"), ("eraser", "Ластик")]
        self.tool_var = tk.StringVar(value="pen")
        
        for tool, label in tools:
            ttk.Radiobutton(toolbar, text=label, variable=self.tool_var, value=tool, 
                           command=lambda t=tool: self.select_tool(t)).pack(side=tk.LEFT, padx=5)
        
        # Цвета
        ttk.Label(toolbar, text="Цвет:").pack(side=tk.LEFT, padx=(20, 10))
        
        colors = ["black", "red", "green", "blue", "yellow", "purple", "orange", "pink"]
        self.color_var = tk.StringVar(value="black")
        
        color_frame = ttk.Frame(toolbar)
        color_frame.pack(side=tk.LEFT)
        
        for color in colors:
            btn = tk.Button(color_frame, bg=color, width=2, height=1, 
                           command=lambda c=color: self.select_color(c))
            btn.pack(side=tk.LEFT, padx=1)
        
        # Размер кисти
        ttk.Label(toolbar, text="Размер:").pack(side=tk.LEFT, padx=(20, 5))
        self.brush_size = tk.Scale(toolbar, from_=1, to=20, orient=tk.HORIZONTAL, 
                                  command=self.change_brush_size)
        self.brush_size.set(5)
        self.brush_size.pack(side=tk.LEFT, padx=5)
    
    def select_tool(self, tool):
        """Выбирает инструмент"""
        self.current_tool = tool
        self.update_status()
    
    def select_color(self, color):
        """Выбирает цвет"""
        self.current_color = color
        self.update_status()
    
    def change_brush_size(self, size):
        """Изменяет размер кисти"""
        self.update_status()
    
    def update_status(self):
        """Обновляет статусную информацию"""
        tool_names = {
            "pen": "Ручка",
            "rectangle": "Прямоугольник", 
            "circle": "Круг",
            "eraser": "Ластик"
        }
        tool_name = tool_names.get(self.current_tool, self.current_tool)
        self.status_label.config(text=f"Инструмент: {tool_name} | Цвет: {self.current_color} | Размер: {self.brush_size.get()}")
    
    def start_draw(self, event):
        """Начинает рисование"""
        self.drawing = True
        self.start_x = event.x
        self.start_y = event.y
        
        if self.current_tool == "pen":
            # Для ручки сразу создаем первую точку
            self.current_item = self.canvas.create_line(
                self.start_x, self.start_y, self.start_x, self.start_y,
                fill=self.current_color, width=self.brush_size.get(), capstyle=tk.ROUND, smooth=tk.TRUE
            )
        elif self.current_tool == "rectangle":
            self.current_item = self.canvas.create_rectangle(
                self.start_x, self.start_y, self.start_x, self.start_y,
                outline=self.current_color, width=self.brush_size.get()
            )
        elif self.current_tool == "circle":
            self.current_item = self.canvas.create_oval(
                self.start_x, self.start_y, self.start_x, self.start_y,
                outline=self.current_color, width=self.brush_size.get()
            )
        elif self.current_tool == "eraser":
            # Ластик работает как толстая ручка белого цвета
            self.current_item = self.canvas.create_line(
                self.start_x, self.start_y, self.start_x, self.start_y,
                fill="white", width=self.brush_size.get()*3, capstyle=tk.ROUND, smooth=tk.TRUE
            )
    
    def draw(self, event):
        """Продолжает рисование"""
        if self.drawing and self.current_item:
            if self.current_tool == "pen" or self.current_tool == "eraser":
                # Для ручки и ластика добавляем линии
                self.canvas.coords(
                    self.current_item,
                    self.start_x, self.start_y, event.x, event.y
                )
                self.start_x = event.x
                self.start_y = event.y
            else:
                # Для прямоугольника и круга обновляем размер
                self.canvas.coords(
                    self.current_item,
                    self.start_x, self.start_y, event.x, event.y
                )
    
    def stop_draw(self, event):
        """Завершает рисование"""
        self.drawing = False
        self.current_item = None
    
    def clear_canvas(self):
        """Очищает холст"""
        self.canvas.delete("all")
    
    def save_image(self):
        """Сохраняет изображение"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".ps",
            filetypes=[("PostScript", "*.ps"), ("All Files", "*.*")]
        )
        if file_path:
            self.canvas.postscript(file=file_path)
            messagebox.showinfo("Сохранение", f"Изображение сохранено в {file_path}")
    
    def load_image(self):
        """Загружает изображение"""
        messagebox.showinfo("Загрузка", "Функция загрузки изображения")
    
    def key_pressed(self, event):
        """Обработка нажатия клавиши"""
        if event.keysym.lower() == 'c':
            self.clear_canvas()
        elif event.keysym.lower() == 'q':
            self.root.quit()
    
    def run(self):
        self.root.mainloop()


# =============================================================================
# Главная функция для запуска приложений
# =============================================================================

def main():
    """Главная функция для демонстрации решений"""
    print("Решения для практического занятия 19: Tkinter - обработка событий")
    print("=" * 70)
    print("Выберите приложение для запуска:")
    print("1 - Обработка кликов мыши")
    print("2 - Обработка клавиатуры")
    print("3 - Передача данных через события")
    print("4 - Кастомные события")
    print("5 - Рисовалка")
    print("0 - Выход")
    print("=" * 70)
    
    choice = input("Ваш выбор: ")
    
    if choice == "1":
        app = MouseEventApp()
        app.run()
    elif choice == "2":
        app = KeyboardEventApp()
        app.run()
    elif choice == "3":
        app = DataTransferApp()
        app.run()
    elif choice == "4":
        app = CustomEventApp()
        app.run()
    elif choice == "5":
        app = DrawingApp()
        app.run()
    else:
        print("До свидания!")


if __name__ == "__main__":
    main()
