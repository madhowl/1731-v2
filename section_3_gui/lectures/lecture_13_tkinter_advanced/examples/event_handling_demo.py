# Примеры обработки событий в Tkinter

import tkinter as tk
from tkinter import ttk, messagebox
import time

class EventHandlingDemo:
    """
    Демонстрация обработки событий в Tkinter
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Обработка событий в Tkinter")
        self.root.geometry("800x600")
        
        # Переменные для отслеживания событий
        self.click_count = 0
        self.key_press_count = 0
        self.mouse_position = tk.StringVar(value="Позиция мыши: (0, 0)")
        
        self.setup_ui()
        self.setup_events()
    
    def setup_ui(self):
        """
        Создание пользовательского интерфейса
        """
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="Демонстрация обработки событий", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Информационная панель
        info_frame = ttk.LabelFrame(main_frame, text="Информация о событиях", padding="10")
        info_frame.pack(fill=tk.X, pady=5)
        
        self.info_label = ttk.Label(info_frame, text="Нажмите на элементы для генерации событий")
        self.info_label.pack()
        
        self.position_label = ttk.Label(info_frame, textvariable=self.mouse_position)
        self.position_label.pack(pady=5)
        
        # Счетчики событий
        counters_frame = ttk.LabelFrame(main_frame, text="Счетчики событий", padding="10")
        counters_frame.pack(fill=tk.X, pady=5)
        
        self.click_counter = ttk.Label(counters_frame, text="Клики: 0")
        self.click_counter.pack(anchor="w")
        
        self.key_counter = ttk.Label(counters_frame, text="Нажатия клавиш: 0")
        self.key_counter.pack(anchor="w", pady=(5, 0))
        
        # Рабочая область
        work_area = ttk.LabelFrame(main_frame, text="Рабочая область", padding="10")
        work_area.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Canvas для демонстрации событий мыши
        self.canvas = tk.Canvas(work_area, bg="white", width=600, height=300)
        self.canvas.pack(pady=10)
        
        # Добавим несколько элементов на Canvas
        self.canvas.create_rectangle(50, 50, 150, 100, fill="lightblue", tags="rect")
        self.canvas.create_oval(200, 50, 300, 150, fill="lightgreen", tags="oval")
        self.canvas.create_text(400, 100, text="Текст", font=("Arial", 16), tags="text")
        
        # Панель инструментов
        toolbar = ttk.Frame(main_frame)
        toolbar.pack(fill=tk.X, pady=5)
        
        ttk.Button(toolbar, text="Кнопка 1", command=self.on_button_click).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar, text="Кнопка 2", command=lambda: self.on_button_click("Кнопка 2")).pack(side=tk.LEFT, padx=5)
        
        # Поле ввода для демонстрации событий клавиатуры
        ttk.Label(toolbar, text="Поле ввода:").pack(side=tk.LEFT, padx=(20, 5))
        self.entry = ttk.Entry(toolbar, width=20)
        self.entry.pack(side=tk.LEFT, padx=5)
    
    def setup_events(self):
        """
        Настройка обработчиков событий
        """
        # События окна
        self.root.bind("<Key>", self.on_key_press)
        self.root.bind("<Button-1>", self.on_window_click)
        self.root.bind("<Motion>", self.on_mouse_move)
        
        # События Canvas
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<Double-Button-1>", self.on_canvas_double_click)
        self.canvas.bind("<Button-3>", self.show_context_menu)  # ПКМ
        
        # События элементов на Canvas
        self.canvas.tag_bind("rect", "<Button-1>", lambda e: self.on_shape_click("прямоугольник"))
        self.canvas.tag_bind("oval", "<Button-1>", lambda e: self.on_shape_click("овал"))
        self.canvas.tag_bind("text", "<Button-1>", lambda e: self.on_shape_click("текст"))
        
        # События для поля ввода
        self.entry.bind("<Return>", self.on_enter_key)
        self.entry.bind("<FocusIn>", self.on_focus_in)
        self.entry.bind("<FocusOut>", self.on_focus_out)
        
        # Контекстное меню для Canvas
        self.create_context_menu()
    
    def create_context_menu(self):
        """
        Создание контекстного меню
        """
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Очистить Canvas", command=self.clear_canvas)
        self.context_menu.add_command(label="Добавить фигуру", command=self.add_random_shape)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Выход", command=self.root.quit)
    
    def on_button_click(self, button_name="Кнопка"):
        """
        Обработчик нажатия кнопки
        """
        self.click_count += 1
        self.info_label.config(text=f"Нажата {button_name}")
        self.update_click_counter()
    
    def on_canvas_click(self, event):
        """
        Обработчик клика по Canvas
        """
        self.click_count += 1
        self.info_label.config(text=f"Клик по Canvas на позиции ({event.x}, {event.y})")
        self.update_click_counter()
        
        # Добавляем точку на Canvas
        self.canvas.create_oval(
            event.x-5, event.y-5, event.x+5, event.y+5,
            fill="red", outline="darkred", width=2
        )
    
    def on_canvas_double_click(self, event):
        """
        Обработчик двойного клика по Canvas
        """
        self.info_label.config(text=f"Двойной клик по Canvas на позиции ({event.x}, {event.y})")
        # Добавляем большую фигуру по двойному клику
        self.canvas.create_rectangle(
            event.x-20, event.y-20, event.x+20, event.y+20,
            outline="blue", width=3, fill=""
        )
    
    def on_shape_click(self, shape_name):
        """
        Обработчик клика по форме на Canvas
        """
        self.click_count += 1
        self.info_label.config(text=f"Нажата {shape_name}")
        self.update_click_counter()
        
        # Меняем цвет формы
        self.canvas.itemconfig(f"current", fill=self.get_random_color())
    
    def on_key_press(self, event):
        """
        Обработчик нажатия клавиши
        """
        self.key_press_count += 1
        self.info_label.config(text=f"Нажата клавиша: {event.keysym}")
        self.key_counter.config(text=f"Нажатия клавиш: {self.key_press_count}")
    
    def on_window_click(self, event):
        """
        Обработчик клика по окну
        """
        # Обновляем счетчик только если клик не на Canvas
        if event.widget != self.canvas:
            self.click_count += 1
            self.update_click_counter()
    
    def on_mouse_move(self, event):
        """
        Обработчик перемещения мыши
        """
        # Обновляем позицию мыши каждые 10 пикселей для оптимизации
        if event.x % 10 == 0 and event.y % 10 == 0:
            self.mouse_position.set(f"Позиция мыши: ({event.x}, {event.y})")
    
    def on_enter_key(self, event):
        """
        Обработчик нажатия Enter в поле ввода
        """
        text = self.entry.get()
        self.info_label.config(text=f"Текст в поле ввода: '{text}'")
        self.entry.delete(0, tk.END)  # Очищаем поле после ввода
    
    def on_focus_in(self, event):
        """
        Обработчик получения фокуса
        """
        self.info_label.config(text="Поле ввода получило фокус")
    
    def on_focus_out(self, event):
        """
        Обработчик потери фокуса
        """
        self.info_label.config(text="Поле ввода потеряло фокус")
    
    def show_context_menu(self, event):
        """
        Показ контекстного меню
        """
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    def update_click_counter(self):
        """
        Обновление счетчика кликов
        """
        self.click_counter.config(text=f"Клики: {self.click_count}")
    
    def clear_canvas(self):
        """
        Очистка Canvas
        """
        self.canvas.delete("all")
        self.info_label.config(text="Canvas очищен")
    
    def add_random_shape(self):
        """
        Добавление случайной формы на Canvas
        """
        import random
        
        shape_type = random.choice(["rectangle", "oval", "polygon"])
        x = random.randint(50, 550)
        y = random.randint(50, 250)
        
        if shape_type == "rectangle":
            self.canvas.create_rectangle(x, y, x+50, y+30, fill=self.get_random_color())
        elif shape_type == "oval":
            self.canvas.create_oval(x, y, x+50, y+30, fill=self.get_random_color())
        elif shape_type == "polygon":
            points = [x, y, x+25, y-20, x+50, y, x+35, y+30, x+15, y+30]
            self.canvas.create_polygon(points, fill=self.get_random_color())
        
        self.info_label.config(text=f"Добавлена {shape_type}")
    
    def get_random_color(self):
        """
        Получение случайного цвета
        """
        import random
        colors = ["red", "green", "blue", "yellow", "purple", "orange", "pink", "cyan"]
        return random.choice(colors)

class AdvancedEventHandling:
    """
    Продвинутая обработка событий
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Продвинутая обработка событий")
        self.root.geometry("900x700")
        
        # Переменные состояния
        self.is_dragging = False
        self.drag_start_x = 0
        self.drag_start_y = 0
        self.current_item = None
        
        self.setup_advanced_ui()
        self.setup_advanced_events()
    
    def setup_advanced_ui(self):
        """
        Создание интерфейса с продвинутыми элементами
        """
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        title = ttk.Label(main_frame, text="Продвинутая обработка событий", 
                         font=("Arial", 16, "bold"))
        title.pack(pady=10)
        
        # Canvas для интерактивных элементов
        self.interactive_canvas = tk.Canvas(main_frame, bg="white", width=700, height=400)
        self.interactive_canvas.pack(pady=10)
        
        # Добавляем несколько интерактивных элементов
        self.create_interactive_elements()
        
        # Панель управления
        control_frame = ttk.LabelFrame(main_frame, text="Управление событиями", padding="10")
        control_frame.pack(fill=tk.X, pady=5)
        
        # Кнопки для демонстрации событий
        ttk.Button(control_frame, text="Запустить анимацию", 
                  command=self.start_animation).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Остановить анимацию", 
                  command=self.stop_animation).pack(side=tk.LEFT, padx=5)
        
        self.animation_running = False
        self.animation_id = None
        
        # Метка для отображения информации о событиях
        self.event_info = tk.Text(control_frame, height=4, width=60)
        self.event_info.pack(fill=tk.X, pady=(10, 0))
    
    def create_interactive_elements(self):
        """
        Создание интерактивных элементов на Canvas
        """
        # Создаем несколько фигур, которые можно перетаскивать
        self.rectangles = []
        for i in range(3):
            rect = self.interactive_canvas.create_rectangle(
                50 + i*100, 50, 100 + i*100, 100,
                fill=f"#{i*5}ff{i*3}", 
                outline="black", 
                width=2,
                tags="draggable"
            )
            self.rectangles.append(rect)
            
            # Добавляем текст к каждой фигуре
            self.interactive_canvas.create_text(
                75 + i*100, 75,
                text=f"Фигура {i+1}",
                fill="white",
                tags="draggable"
            )
        
        # Создаем овалы
        self.ovals = []
        for i in range(2):
            oval = self.interactive_canvas.create_oval(
                50 + i*150, 150, 120 + i*150, 220,
                fill=f"#{i*3}ff{i*5}", 
                outline="darkblue", 
                width=2,
                tags="draggable"
            )
            self.ovals.append(oval)
            
            self.interactive_canvas.create_text(
                85 + i*150, 185,
                text=f"Овал {i+1}",
                fill="black",
                tags="draggable"
            )
    
    def setup_advanced_events(self):
        """
        Настройка продвинутых событий
        """
        # Привязка событий перетаскивания к элементам с тегом "draggable"
        self.interactive_canvas.tag_bind("draggable", "<ButtonPress-1>", self.on_drag_start)
        self.interactive_canvas.tag_bind("draggable", "<B1-Motion>", self.on_drag_motion)
        self.interactive_canvas.tag_bind("draggable", "<ButtonRelease-1>", self.on_drag_release)
        
        # Привязка событий для отслеживания мыши
        self.interactive_canvas.bind("<Enter>", self.on_canvas_enter)
        self.interactive_canvas.bind("<Leave>", self.on_canvas_leave)
        
        # Привязка событий клавиатуры
        self.interactive_canvas.focus_set()
        self.interactive_canvas.bind("<KeyPress-d>", self.on_delete_key)
        self.interactive_canvas.bind("<KeyPress-r>", self.on_rotate_key)
        
        # Привязка события прокрутки (для масштабирования)
        self.interactive_canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        self.interactive_canvas.bind("<Button-4>", self.on_mouse_wheel_up)  # Linux
        self.interactive_canvas.bind("<Button-5>", self.on_mouse_wheel_down)  # Linux
    
    def on_drag_start(self, event):
        """
        Начало перетаскивания элемента
        """
        self.is_dragging = True
        self.drag_start_x = event.x
        self.drag_start_y = event.y
        self.current_item = self.interactive_canvas.find_closest(event.x, event.y)[0]
        
        # Поднимаем элемент наверх, чтобы он был виден поверх других
        self.interactive_canvas.tag_raise(self.current_item)
        
        # Изменяем цвет при начале перетаскивания
        current_fill = self.interactive_canvas.itemcget(self.current_item, "fill")
        if current_fill and current_fill != "":
            self.interactive_canvas.itemconfig(self.current_item, outline="red", width=3)
        
        self.log_event(f"Начало перетаскивания элемента {self.current_item}")
    
    def on_drag_motion(self, event):
        """
        Перемещение элемента при перетаскивании
        """
        if self.is_dragging and self.current_item:
            # Вычисляем смещение
            delta_x = event.x - self.drag_start_x
            delta_y = event.y - self.drag_start_y
            
            # Перемещаем элемент
            self.interactive_canvas.move(self.current_item, delta_x, delta_y)
            
            # Обновляем начальную позицию
            self.drag_start_x = event.x
            self.drag_start_y = event.y
    
    def on_drag_release(self, event):
        """
        Окончание перетаскивания элемента
        """
        if self.current_item:
            # Возвращаем исходную ширину обводки
            self.interactive_canvas.itemconfig(self.current_item, width=2)
            self.log_event(f"Окончание перетаскивания элемента {self.current_item}")
        
        self.is_dragging = False
        self.current_item = None
    
    def on_canvas_enter(self, event):
        """
        Событие входа мыши в Canvas
        """
        self.log_event("Мышь вошла в Canvas")
        self.interactive_canvas.config(relief="sunken")
    
    def on_canvas_leave(self, event):
        """
        Событие выхода мыши из Canvas
        """
        self.log_event("Мышь покинула Canvas")
        self.interactive_canvas.config(relief="flat")
    
    def on_delete_key(self, event):
        """
        Удаление выбранного элемента по клавише D
        """
        if self.current_item:
            self.interactive_canvas.delete(self.current_item)
            self.log_event(f"Элемент {self.current_item} удален")
            self.current_item = None
    
    def on_rotate_key(self, event):
        """
        Поворот элемента по клавише R (в реальном приложении)
        """
        self.log_event("Клавиша R нажата (функция поворота)")
    
    def on_mouse_wheel(self, event):
        """
        Событие прокрутки колеса мыши (Windows)
        """
        scale_factor = 1.1 if event.delta > 0 else 0.9
        self.scale_canvas(scale_factor)
        self.log_event(f"Масштабирование: {scale_factor:.1f}")
    
    def on_mouse_wheel_up(self, event):
        """
        Событие прокрутки вверх (Linux)
        """
        self.scale_canvas(1.1)
        self.log_event("Масштабирование вверх")
    
    def on_mouse_wheel_down(self, event):
        """
        Событие прокрутки вниз (Linux)
        """
        self.scale_canvas(0.9)
        self.log_event("Масштабирование вниз")
    
    def scale_canvas(self, factor):
        """
        Масштабирование элементов на Canvas
        """
        # В реальном приложении здесь происходило бы масштабирование
        # Для демонстрации просто выводим сообщение
        self.log_event(f"Масштабирование на фактор {factor:.1f}")
    
    def start_animation(self):
        """
        Запуск анимации элементов
        """
        if not self.animation_running:
            self.animation_running = True
            self.animate_elements()
            self.log_event("Анимация запущена")
    
    def stop_animation(self):
        """
        Остановка анимации
        """
        if self.animation_running:
            self.animation_running = False
            if self.animation_id:
                self.interactive_canvas.after_cancel(self.animation_id)
            self.log_event("Анимация остановлена")
    
    def animate_elements(self):
        """
        Анимация элементов на Canvas
        """
        if not self.animation_running:
            return
        
        # Простая анимация движения
        for rect in self.rectangles:
            coords = self.interactive_canvas.coords(rect)
            if coords:
                x1, y1, x2, y2 = coords
                # Двигаем элемент вниз и вправо
                self.interactive_canvas.move(rect, 1, 1)
                
                # Если элемент выходит за границы, возвращаем его
                if x2 > 700 or y2 > 400:
                    self.interactive_canvas.moveto(rect, 50, 50)
        
        # Повторяем анимацию через 50 миллисекунд
        self.animation_id = self.interactive_canvas.after(50, self.animate_elements)
    
    def log_event(self, message):
        """
        Логирование события
        """
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S.%f")[:-3]
        self.event_info.insert(tk.END, f"[{timestamp}] {message}\n")
        self.event_info.see(tk.END)  # Прокручиваем к последней строке

def main():
    """
    Основная функция демонстрации
    """
    root = tk.Tk()
    
    # Для демонстрации выберите один из классов:
    app = EventHandlingDemo(root)
    # app = AdvancedEventHandling(root)
    
    root.mainloop()

if __name__ == "__main__":
    main()
