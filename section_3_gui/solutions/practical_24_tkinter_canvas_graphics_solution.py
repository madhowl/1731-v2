#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Практическое занятие 24: Tkinter - Canvas и графика
Решение задач по работе с виджетом Canvas

Автор: AI Assistant
"""

import tkinter as tk
from tkinter import ttk, colorchooser, filedialog
import math
import random
import time


# ==============================================================================
# ЗАДАЧА 1: Основы Canvas
# ==============================================================================

class CanvasBasicsDemo:
    """Демонстрация основных операций с Canvas"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Задача 1: Основы Canvas")
        self.root.geometry("600x500")
        
        self.create_canvas_demo()
    
    def create_canvas_demo(self):
        """Создание демонстрации"""
        # Создание Canvas
        self.canvas = tk.Canvas(self.root, bg="white", width=580, height=450)
        self.canvas.pack(padx=10, pady=10)
        
        # Линии
        self.canvas.create_line(10, 10, 100, 10, fill="red", width=2, dash=(4, 2))
        self.canvas.create_line(10, 30, 100, 50, fill="blue", width=3, arrow=tk.LAST)
        self.canvas.create_line(10, 60, 100, 60, fill="green", width=5)
        
        # Прямоугольники
        self.canvas.create_rectangle(120, 10, 200, 80, fill="lightblue", outline="blue", width=2)
        self.canvas.create_rectangle(210, 10, 250, 80, fill="lightgreen", outline="green")
        
        # Овалы/эллипсы
        self.canvas.create_oval(10, 100, 100, 160, fill="lightyellow", outline="orange", width=2)
        self.canvas.create_oval(120, 100, 200, 180, fill="pink", outline="red")
        
        # Многоугольники
        self.canvas.create_polygon(
            300, 10, 350, 60, 400, 10, 380, 80, 320, 80,
            fill="purple", outline="darkviolet", width=2
        )
        self.canvas.create_polygon(
            420, 10, 450, 40, 480, 10, 480, 60, 450, 80, 420, 60,
            fill="cyan", outline="darkcyan"
        )
        
        # Текст
        self.canvas.create_text(300, 120, text="Заголовок", font=("Arial", 14, "bold"), fill="darkblue")
        self.canvas.create_text(300, 150, text="Обычный текст", font=("Arial", 10), fill="black", anchor=tk.W)
        self.canvas.create_text(300, 180, text="Текст с углом", font=("Arial", 10), fill="gray", angle=45)
        
        # Дуги
        self.canvas.create_arc(10, 200, 100, 280, start=0, extent=180, fill="lightcoral", outline="red")
        self.canvas.create_arc(120, 200, 200, 280, start=45, extent=270, style=tk.ARC, outline="blue")
        
        # Сложные фигуры - рисунок домика
        house_x, house_y = 350, 100
        # Стены
        self.canvas.create_rectangle(
            house_x, house_y + 50, house_x + 100, house_y + 150,
            fill="sandybrown", outline="brown", width=2
        )
        # Крыша
        self.canvas.create_polygon(
            house_x - 10, house_y + 50,
            house_x + 50, house_y,
            house_x + 110, house_y + 50,
            fill="brown", outline="darkbrown", width=2
        )
        # Окно
        self.canvas.create_rectangle(
            house_x + 20, house_y + 70, house_x + 50, house_y + 100,
            fill="lightblue", outline="darkblue"
        )
        # Дверь
        self.canvas.create_rectangle(
            house_x + 65, house_y + 90, house_x + 90, house_y + 150,
            fill="tan", outline="saddlebrown"
        )


# ==============================================================================
# ЗАДАЧА 2: Интерактивная графика
# ==============================================================================

class InteractiveGraphics:
    """Интерактивные объекты на Canvas"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Задача 2: Интерактивная графика")
        self.root.geometry("700x500")
        
        self.objects = []
        self.selected_object = None
        self.drag_data = {"x": 0, "y": 0, "item": None}
        
        self.create_canvas()
        self.create_toolbar()
        self.create_objects()
    
    def create_canvas(self):
        """Создание Canvas"""
        self.canvas = tk.Canvas(self.root, bg="white", width=680, height=450)
        self.canvas.pack(side=tk.BOTTOM, padx=10, pady=10)
        
        # Привязка событий
        self.canvas.tag_bind("draggable", "<Button-1>", self.on_click)
        self.canvas.tag_bind("draggable", "<B1-Motion>", self.on_drag)
        self.canvas.tag_bind("draggable", "<ButtonRelease-1>", self.on_release)
        self.canvas.tag_bind("draggable", "<Double-Button-1>", self.on_double_click)
        
        # Привязка для создания новых объектов
        self.canvas.bind("<Button-3>", self.on_right_click)
    
    def create_toolbar(self):
        """Создание панели инструментов"""
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        ttk.Label(toolbar, text="ЛКМ: перетаскивание, ПКМ: создать, Двойной ЛКМ: удалить").pack()
    
    def create_objects(self):
        """Создание демонстрационных объектов"""
        # Перетаскиваемые прямоугольники
        colors = ["red", "green", "blue", "orange", "purple"]
        
        for i, color in enumerate(colors):
            x = 50 + i * 120
            y = 150
            
            obj = self.canvas.create_rectangle(
                x, y, x + 80, y + 60,
                fill=color, outline="black", width=2,
                tags=("draggable", f"rect_{i}")
            )
            
            self.canvas.create_text(
                x + 40, y + 30,
                text=f"Объект {i+1}",
                tags=("draggable", f"text_{i}")
            )
            
            self.objects.append(obj)
        
        # Перетаскиваемый круг
        circle = self.canvas.create_oval(
            550, 150, 630, 230,
            fill="gold", outline="orange", width=2,
            tags=("draggable", "circle")
        )
        self.canvas.create_text(
            590, 190, text="Круг",
            tags=("draggable", "circle_text")
        )
        self.objects.append(circle)
    
    def on_click(self, event):
        """Обработка клика"""
        # Найти объект под курсором
        item = self.canvas.find_closest(event.x, event.y)
        
        if item:
            # Выбрать объект
            self.select_object(item[0])
            
            # Начать перетаскивание
            self.drag_data["item"] = item[0]
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y
    
    def on_drag(self, event):
        """Обработка перетаскивания"""
        if self.drag_data["item"]:
            dx = event.x - self.drag_data["x"]
            dy = event.y - self.drag_data["y"]
            
            self.canvas.move(self.drag_data["item"], dx, dy)
            
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y
    
    def on_release(self, event):
        """Обработка отпускания"""
        self.drag_data["item"] = None
    
    def on_double_click(self, event):
        """Обработка двойного клика - удаление"""
        item = self.canvas.find_closest(event.x, event.y)
        if item:
            self.canvas.delete(item[0])
            if item[0] in self.objects:
                self.objects.remove(item[0])
    
    def on_right_click(self, event):
        """Создание нового объекта по клику"""
        color = colorchooser.askcolor(title="Выберите цвет")[1]
        if color:
            size = 60
            obj = self.canvas.create_rectangle(
                event.x - size//2, event.y - size//2,
                event.x + size//2, event.y + size//2,
                fill=color, outline="black", width=2,
                tags=("draggable",)
            )
            self.objects.append(obj)
    
    def select_object(self, item):
        """Выделение объекта"""
        # Сбросить предыдущее выделение
        if self.selected_object:
            current_width = self.canvas.itemcget(self.selected_object, "outlinewidth")
            self.canvas.itemconfig(self.selected_object, outline="black", width=2)
        
        # Выделить новый объект
        self.selected_object = item
        self.canvas.itemconfig(item, outline="red", width=3)


class ResizableObjects:
    """Изменение размера объектов"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Задача 2: Изменение размера объектов")
        self.root.geometry("600x450")
        
        self.selected = None
        self.resize_handle = None
        
        self.create_canvas()
        self.create_sample_objects()
    
    def create_canvas(self):
        """Создание Canvas"""
        self.canvas = tk.Canvas(self.root, bg="white", width=580, height=420)
        self.canvas.pack(padx=10, pady=10)
        
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)
    
    def create_sample_objects(self):
        """Создание образцов объектов"""
        # Объект с точками изменения размера
        self.shape = self.canvas.create_rectangle(
            100, 100, 300, 250,
            fill="lightblue", outline="blue", width=2,
            tags=("resizable",)
        )
        
        # Метки для изменения размера (углы)
        self.handles = []
        corners = [(100, 100), (300, 100), (100, 250), (300, 250)]
        
        for x, y in corners:
            handle = self.canvas.create_oval(
                x - 5, y - 5, x + 5, y + 5,
                fill="red", outline="darkred",
                tags=("handle",)
            )
            self.handles.append(handle)
    
    def on_click(self, event):
        """Обработка клика"""
        item = self.canvas.find_closest(event.x, event.y)
        if item:
            tags = self.canvas.gettags(item[0])
            if "handle" in tags:
                self.resize_handle = item[0]
            elif "resizable" in tags:
                self.selected = item[0]
    
    def on_drag(self, event):
        """Перетаскивание"""
        if self.resize_handle:
            # Изменение размера
            coords = self.canvas.coords(self.shape)
            
            if self.resize_handle == self.handles[0]:  # Левый верхний
                self.canvas.coords(self.shape, event.x, event.y, coords[2], coords[3])
            elif self.resize_handle == self.handles[1]:  # Правый верхний
                self.canvas.coords(self.shape, coords[0], event.y, event.x, coords[3])
            elif self.resize_handle == self.handles[2]:  # Левый нижний
                self.canvas.coords(self.shape, event.x, coords[1], coords[2], event.y)
            elif self.resize_handle == self.handles[3]:  # Правый нижний
                self.canvas.coords(self.shape, coords[0], coords[1], event.x, event.y)
            
            self.update_handles()
    
    def on_release(self, event):
        """Отпускание"""
        self.resize_handle = None
        self.selected = None
    
    def update_handles(self):
        """Обновить положение ручек"""
        coords = self.canvas.coords(self.shape)
        positions = [(coords[0], coords[1]), (coords[2], coords[1]), 
                     (coords[0], coords[3]), (coords[2], coords[3])]
        
        for handle, pos in zip(self.handles, positions):
            self.canvas.coords(handle, pos[0] - 5, pos[1] - 5, pos[0] + 5, pos[1] + 5)


# ==============================================================================
# ЗАДАЧА 3: Анимация
# ==============================================================================

class SimpleAnimation:
    """Простая анимация движения"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Задача 3: Простая анимация")
        self.root.geometry("500x400")
        
        self.running = True
        self.create_animation()
    
    def create_animation(self):
        """Создание анимации"""
        self.canvas = tk.Canvas(self.root, bg="white", width=480, height=380)
        self.canvas.pack(padx=10, pady=10)
        
        # Объект для анимации (мяч)
        self.ball = self.canvas.create_oval(
            200, 150, 250, 200,
            fill="red", outline="darkred", width=2
        )
        
        # Направление движения
        self.dx = 3
        self.dy = 2
        
        # Кнопки управления
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=5)
        
        ttk.Button(btn_frame, text="Старт", command=self.start).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Стоп", command=self.stop).pack(side=tk.LEFT, padx=5)
        
        self.animate()
    
    def animate(self):
        """Анимация движения"""
        if self.running:
            # Перемещение
            self.canvas.move(self.ball, self.dx, self.dy)
            
            # Получение координат
            coords = self.canvas.coords(self.ball)
            
            # Проверка границ
            if coords[0] <= 0 or coords[2] >= 480:
                self.dx = -self.dx
            if coords[1] <= 0 or coords[3] >= 380:
                self.dy = -self.dy
            
            # Запуск следующего кадра
            self.root.after(20, self.animate)
    
    def start(self):
        """Запуск анимации"""
        self.running = True
        self.animate()
    
    def stop(self):
        """Остановка анимации"""
        self.running = False


class AnimatedClock:
    """Анимированные часы"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Задача 3: Анимированные часы")
        self.root.geometry("400x450")
        
        self.create_clock()
    
    def create_clock(self):
        """Создание часов"""
        self.canvas = tk.Canvas(self.root, bg="white", width=380, height=400)
        self.canvas.pack(padx=10, pady=10)
        
        self.center_x = 190
        self.center_y = 180
        self.radius = 120
        
        # Рисуем циферблат
        self.draw_clock_face()
        
        # Запуск обновления
        self.update_clock()
    
    def draw_clock_face(self):
        """Рисование циферблата"""
        # Круг
        self.canvas.create_oval(
            self.center_x - self.radius, 
            self.center_y - self.radius,
            self.center_x + self.radius, 
            self.center_y + self.radius,
            outline="black", width=3
        )
        
        # Часовые деления
        for i in range(12):
            angle = i * 30 * math.pi / 180
            x1 = self.center_x + (self.radius - 15) * math.sin(angle)
            y1 = self.center_y - (self.radius - 15) * math.cos(angle)
            x2 = self.center_x + (self.radius - 5) * math.sin(angle)
            y2 = self.center_y - (self.radius - 5) * math.cos(angle)
            
            self.canvas.create_line(x1, y1, x2, y2, width=3)
        
        # Минутные деления
        for i in range(60):
            if i % 5 != 0:
                angle = i * 6 * math.pi / 180
                x1 = self.center_x + (self.radius - 10) * math.sin(angle)
                y1 = self.center_y - (self.radius - 10) * math.cos(angle)
                x2 = self.center_x + (self.radius - 5) * math.sin(angle)
                y2 = self.center_y - (self.radius - 5) * math.cos(angle)
                
                self.canvas.create_line(x1, y1, x2, y2, width=1)
    
    def update_clock(self):
        """Обновление времени"""
        # Удаление стрелок
        self.canvas.delete("hands")
        
        # Получение текущего времени
        current_time = time.localtime()
        hours = current_time.tm_hour % 12
        minutes = current_time.tm_min
        seconds = current_time.tm_sec
        
        # Секундная стрелка
        sec_angle = seconds * 6 * math.pi / 180
        sec_x = self.center_x + (self.radius - 20) * math.sin(sec_angle)
        sec_y = self.center_y - (self.radius - 20) * math.cos(sec_angle)
        self.canvas.create_line(
            self.center_x, self.center_y, sec_x, sec_y,
            fill="red", width=1, tags="hands"
        )
        
        # Минутная стрелка
        min_angle = (minutes + seconds/60) * 6 * math.pi / 180
        min_x = self.center_x + (self.radius - 40) * math.sin(min_angle)
        min_y = self.center_y - (self.radius - 40) * math.cos(min_angle)
        self.canvas.create_line(
            self.center_x, self.center_y, min_x, min_y,
            fill="blue", width=2, tags="hands"
        )
        
        # Часовая стрелка
        hour_angle = (hours + minutes/60) * 30 * math.pi / 180
        hour_x = self.center_x + (self.radius - 70) * math.sin(hour_angle)
        hour_y = self.center_y - (self.radius - 70) * math.cos(hour_angle)
        self.canvas.create_line(
            self.center_x, self.center_y, hour_x, hour_y,
            fill="black", width=3, tags="hands"
        )
        
        # Центр
        self.canvas.create_oval(
            self.center_x - 5, self.center_y - 5,
            self.center_x + 5, self.center_y + 5,
            fill="black", tags="hands"
        )
        
        # Цифровое время
        time_str = time.strftime("%H:%M:%S")
        self.canvas.create_text(
            self.center_x, self.center_y + 80,
            text=time_str, font=("Arial", 16),
            tags="hands"
        )
        
        # Обновление каждую секунду
        self.root.after(1000, self.update_clock)


# ==============================================================================
# ЗАДАЧА 4: Графический редактор
# ==============================================================================

class GraphicEditor:
    """Простой графический редактор"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Задача 4: Графический редактор")
        self.root.geometry("900x650")
        
        self.current_tool = "pencil"
        self.current_color = "black"
        self.line_width = 2
        self.start_x = None
        self.start_y = None
        self.current_shape = None
        self.last_x = None
        self.last_y = None
        
        self.create_toolbar()
        self.create_canvas()
        self.create_color_palette()
    
    def create_toolbar(self):
        """Создание панели инструментов"""
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        # Инструменты
        ttk.Label(toolbar, text="Инструмент:").pack(side=tk.LEFT, padx=5)
        
        tools = [
            ("✏️ Карандаш", "pencil"),
            ("📏 Линия", "line"),
            ("⬜ Прямоугольник", "rectangle"),
            ("⭕ Эллипс", "ellipse"),
            ("🧹 Ластик", "eraser"),
        ]
        
        for text, tool in tools:
            btn = ttk.Button(
                toolbar, text=text,
                command=lambda t=tool: self.set_tool(t)
            )
            btn.pack(side=tk.LEFT, padx=2)
        
        # Толщина линии
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        ttk.Label(toolbar, text="Толщина:").pack(side=tk.LEFT)
        self.width_var = tk.IntVar(value=2)
        width_spin = ttk.Spinbox(
            toolbar, from_=1, to=20, width=5,
            textvariable=self.width_var,
            command=self.update_width
        )
        width_spin.pack(side=tk.LEFT, padx=5)
        
        # Кнопки сохранения/очистки
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        
        ttk.Button(toolbar, text="💾 Сохранить", command=self.save_image).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="📂 Открыть", command=self.open_image).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="🗑 Очистить", command=self.clear_canvas).pack(side=tk.LEFT, padx=2)
    
    def create_color_palette(self):
        """Создание палитры цветов"""
        palette_frame = ttk.Frame(self.root)
        palette_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=5)
        
        ttk.Label(palette_frame, text="Цвет:").pack(side=tk.LEFT, padx=5)
        
        colors = ["black", "red", "green", "blue", "yellow", "orange", "purple", "brown", "gray", "white"]
        
        for color in colors:
            btn = tk.Canvas(palette_frame, width=25, height=25, bg=color, highlightthickness=1, highlightbackground="gray")
            btn.pack(side=tk.LEFT, padx=2)
            btn.bind("<Button-1>", lambda e, c=color: self.set_color(c))
        
        # Выбор цвета
        ttk.Button(palette_frame, text="Другой...", command=self.choose_color).pack(side=tk.LEFT, padx=10)
        
        # Текущий цвет
        self.color_preview = tk.Canvas(palette_frame, width=30, height=30, bg="black", highlightthickness=2, highlightbackground="gray")
        self.color_preview.pack(side=tk.LEFT, padx=5)
    
    def create_canvas(self):
        """Создание холста"""
        self.canvas = tk.Canvas(self.root, bg="white", width=880, height=550)
        self.canvas.pack(padx=5, pady=5)
        
        # События мыши
        self.canvas.bind("<Button-1>", self.on_mouse_down)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_up)
    
    def set_tool(self, tool):
        """Установить инструмент"""
        self.current_tool = tool
    
    def set_color(self, color):
        """Установить цвет"""
        self.current_color = color
        self.color_preview.config(bg=color)
    
    def update_width(self):
        """Обновить толщину линии"""
        try:
            self.line_width = int(self.width_var.get())
        except ValueError:
            self.line_width = 2
    
    def choose_color(self):
        """Выбор цвета из диалога"""
        color = colorchooser.askcolor(title="Выберите цвет")[1]
        if color:
            self.set_color(color)
    
    def on_mouse_down(self, event):
        """Нажатие кнопки мыши"""
        self.start_x = event.x
        self.start_y = event.y
        self.last_x = event.x
        self.last_y = event.y
        
        if self.current_tool in ["line", "rectangle", "ellipse"]:
            if self.current_tool == "line":
                self.current_shape = self.canvas.create_line(
                    self.start_x, self.start_y, event.x, event.y,
                    fill=self.current_color, width=self.line_width
                )
            elif self.current_tool == "rectangle":
                self.current_shape = self.canvas.create_rectangle(
                    self.start_x, self.start_y, event.x, event.y,
                    outline=self.current_color, width=self.line_width
                )
            elif self.current_tool == "ellipse":
                self.current_shape = self.canvas.create_oval(
                    self.start_x, self.start_y, event.x, event.y,
                    outline=self.current_color, width=self.line_width
                )
    
    def on_mouse_drag(self, event):
        """Перетаскивание мыши"""
        if self.current_tool == "pencil":
            # Карандаш - рисование линий
            self.canvas.create_line(
                self.last_x, self.last_y, event.x, event.y,
                fill=self.current_color, width=self.line_width,
                capstyle=tk.ROUND
            )
            self.last_x = event.x
            self.last_y = event.y
        
        elif self.current_tool == "eraser":
            # Ластик - рисование белым
            self.canvas.create_line(
                self.last_x, self.last_y, event.x, event.y,
                fill="white", width=self.line_width * 3,
                capstyle=tk.ROUND
            )
            self.last_x = event.x
            self.last_y = event.y
        
        elif self.current_tool in ["line", "rectangle", "ellipse"] and self.current_shape:
            # Предпросмотр фигуры
            if self.current_tool == "line":
                self.canvas.coords(self.current_shape, self.start_x, self.start_y, event.x, event.y)
            elif self.current_tool == "rectangle":
                self.canvas.coords(self.current_shape, self.start_x, self.start_y, event.x, event.y)
            elif self.current_tool == "ellipse":
                self.canvas.coords(self.current_shape, self.start_x, self.start_y, event.x, event.y)
    
    def on_mouse_up(self, event):
        """Отпускание кнопки мыши"""
        self.current_shape = None
    
    def clear_canvas(self):
        """Очистка холста"""
        self.canvas.delete("all")
    
    def save_image(self):
        """Сохранение изображения"""
        # Реализация сохранения (упрощенная)
        filename = filedialog.asksaveasfilename(
            defaultextension=".ps",
            filetypes=[("PostScript", "*.ps"), ("All Files", "*.*")]
        )
        if filename:
            self.canvas.postscript(file=filename)
    
    def open_image(self):
        """Открытие изображения"""
        # Реализация открытия (упрощенная)
        filename = filedialog.askopenfilename(
            filetypes=[("Images", "*.png *.gif *.ppm"), ("All Files", "*.*")]
        )
        # Здесь можно загрузить изображение


# ==============================================================================
# ЗАДАЧА 5: Игра на Canvas
# ==============================================================================

class PongGame:
    """Игра Пинг-Понг"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Задача 5: Игра Пинг-Понг")
        self.root.geometry("700x500")
        
        self.running = False
        self.paused = False
        
        # Игровые параметры
        self.canvas_width = 680
        self.canvas_height = 460
        
        # Ракетки
        self.paddle_width = 10
        self.paddle_height = 80
        self.paddle_speed = 8
        
        # Мяч
        self.ball_size = 15
        self.ball_dx = 4
        self.ball_dy = 4
        
        # Счет
        self.player_score = 0
        self.computer_score = 0
        
        self.create_game()
        self.show_start_screen()
    
    def create_game(self):
        """Создание игры"""
        self.canvas = tk.Canvas(
            self.root, 
            bg="black", 
            width=self.canvas_width, 
            height=self.canvas_height
        )
        self.canvas.pack(padx=10, pady=10)
        
        # Игровые объекты
        self.player_paddle = self.canvas.create_rectangle(
            20, self.canvas_height//2 - self.paddle_height//2,
            20 + self.paddle_width, self.canvas_height//2 + self.paddle_height//2,
            fill="white"
        )
        
        self.computer_paddle = self.canvas.create_rectangle(
            self.canvas_width - 20 - self.paddle_width, self.canvas_height//2 - self.paddle_height//2,
            self.canvas_width - 20, self.canvas_height//2 + self.paddle_height//2,
            fill="white"
        )
        
        self.ball = self.canvas.create_oval(
            self.canvas_width//2 - self.ball_size//2,
            self.canvas_height//2 - self.ball_size//2,
            self.canvas_width//2 + self.ball_size//2,
            self.canvas_height//2 + self.ball_size//2,
            fill="white"
        )
        
        # Счет
        self.score_text = self.canvas.create_text(
            self.canvas_width//2, 30,
            text="0 : 0",
            fill="white",
            font=("Arial", 24, "bold")
        )
        
        # Средняя линия
        for i in range(0, self.canvas_height, 30):
            self.canvas.create_line(
                self.canvas_width//2, i,
                self.canvas_width//2, i + 15,
                fill="gray", width=2
            )
        
        # Управление - привязываем к canvas для надежной обработки клавиш
        self.canvas.bind("<KeyPress>", self.on_key_press)
        self.canvas.bind("<KeyRelease>", self.on_key_release)
        self.canvas.focus_set()  # Устанавливаем фокус на canvas для обработки клавиш
        
        self.keys_pressed = {"Up": False, "Down": False}
    
    def show_start_screen(self):
        """Показать стартовый экран"""
        self.start_text = self.canvas.create_text(
            self.canvas_width//2, self.canvas_height//2,
            text="Нажмите ПРОБЕЛ для начала игры",
            fill="white",
            font=("Arial", 18)
        )
    
    def start_game(self):
        """Начало игры"""
        self.running = True
        self.canvas.delete(self.start_text)
        self.game_loop()
    
    def on_key_press(self, event):
        """Обработка нажатия клавиш"""
        if event.keysym == "Up":
            self.keys_pressed["Up"] = True
        elif event.keysym == "Down":
            self.keys_pressed["Down"] = True
        elif event.keysym == "space" and not self.running:
            self.start_game()
    
    def on_key_release(self, event):
        """Обработка отпускания клавиш"""
        if event.keysym == "Up":
            self.keys_pressed["Up"] = False
        elif event.keysym == "Down":
            self.keys_pressed["Down"] = False
    
    def move_paddles(self):
        """Перемещение ракеток"""
        # Игрок
        if self.keys_pressed["Up"]:
            coords = self.canvas.coords(self.player_paddle)
            if coords[1] > 0:
                self.canvas.move(self.player_paddle, 0, -self.paddle_speed)
        
        if self.keys_pressed["Down"]:
            coords = self.canvas.coords(self.player_paddle)
            if coords[3] < self.canvas_height:
                self.canvas.move(self.player_paddle, 0, self.paddle_speed)
        
        # Компьютер (простая логика)
        ball_coords = self.canvas.coords(self.ball)
        ball_center_y = (ball_coords[1] + ball_coords[3]) / 2
        
        comp_coords = self.canvas.coords(self.computer_paddle)
        comp_center_y = (comp_coords[1] + comp_coords[3]) / 2
        
        if comp_center_y < ball_center_y - 10:
            if comp_coords[3] < self.canvas_height:
                self.canvas.move(self.computer_paddle, 0, self.paddle_speed * 0.7)
        elif comp_center_y > ball_center_y + 10:
            if comp_coords[1] > 0:
                self.canvas.move(self.computer_paddle, 0, -self.paddle_speed * 0.7)
    
    def move_ball(self):
        """Перемещение мяча"""
        self.canvas.move(self.ball, self.ball_dx, self.ball_dy)
        
        coords = self.canvas.coords(self.ball)
        
        # Отскок от верха и низа
        if coords[1] <= 0 or coords[3] >= self.canvas_height:
            self.ball_dy = -self.ball_dy
        
        # Отскок от ракеток
        # Игрок
        player_coords = self.canvas.coords(self.player_paddle)
        if (coords[0] <= player_coords[2] and 
            coords[1] >= player_coords[1] and 
            coords[3] <= player_coords[3]):
            self.ball_dx = abs(self.ball_dx)
            self.ball_dx += 0.2  # Ускорение
        
        # Компьютер
        comp_coords = self.canvas.coords(self.computer_paddle)
        if (coords[2] >= comp_coords[0] and 
            coords[1] >= comp_coords[1] and 
            coords[3] <= comp_coords[3]):
            self.ball_dx = -abs(self.ball_dx)
        
        # Гол
        if coords[0] <= 0:
            self.computer_score += 1
            self.reset_ball()
        
        if coords[2] >= self.canvas_width:
            self.player_score += 1
            self.reset_ball()
        
        # Обновление счета
        self.canvas.itemconfig(
            self.score_text, 
            text=f"{self.player_score} : {self.computer_score}"
        )
    
    def reset_ball(self):
        """Сброс мяча"""
        # Остановка
        self.canvas.coords(
            self.ball,
            self.canvas_width//2 - self.ball_size//2,
            self.canvas_height//2 - self.ball_size//2,
            self.canvas_width//2 + self.ball_size//2,
            self.canvas_height//2 + self.ball_size//2
        )
        
        # Случайное направление
        self.ball_dx = 4 * (1 if random.random() > 0.5 else -1)
        self.ball_dy = 4 * (1 if random.random() > 0.5 else -1)
    
    def game_loop(self):
        """Игровой цикл"""
        if self.running:
            self.move_paddles()
            self.move_ball()
            self.root.after(20, self.game_loop)


# ==============================================================================
# ГЛАВНОЕ МЕНЮ ПРИЛОЖЕНИЯ
# ==============================================================================

class MainApp:
    """Главное приложение с выбором задач"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Практическое занятие 24: Tkinter - Canvas и графика")
        self.root.geometry("500x450")
        
        self.create_main_menu()
    
    def create_main_menu(self):
        """Создание главного меню"""
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title = ttk.Label(
            main_frame, 
            text="Выберите задачу:",
            font=("Arial", 16, "bold")
        )
        title.pack(pady=(0, 20))
        
        tasks = [
            ("Задача 1: Основы Canvas", self.open_task1),
            ("Задача 2a: Интерактивная графика", self.open_task2a),
            ("Задача 2b: Изменение размера объектов", self.open_task2b),
            ("Задача 3a: Простая анимация", self.open_task3a),
            ("Задача 3b: Анимированные часы", self.open_task3b),
            ("Задача 4: Графический редактор", self.open_task4),
            ("Задача 5: Игра Пинг-Понг", self.open_task5),
        ]
        
        for text, command in tasks:
            btn = ttk.Button(main_frame, text=text, width=35, command=command)
            btn.pack(pady=5)
        
        ttk.Button(main_frame, text="Выход", command=self.root.quit).pack(pady=20)
    
    def open_task1(self):
        """Открыть задачу 1"""
        window = tk.Toplevel(self.root)
        CanvasBasicsDemo(window)
    
    def open_task2a(self):
        """Открыть задачу 2a"""
        window = tk.Toplevel(self.root)
        InteractiveGraphics(window)
    
    def open_task2b(self):
        """Открыть задачу 2b"""
        window = tk.Toplevel(self.root)
        ResizableObjects(window)
    
    def open_task3a(self):
        """Открыть задачу 3a"""
        window = tk.Toplevel(self.root)
        SimpleAnimation(window)
    
    def open_task3b(self):
        """Открыть задачу 3b"""
        window = tk.Toplevel(self.root)
        AnimatedClock(window)
    
    def open_task4(self):
        """Открыть задачу 4"""
        window = tk.Toplevel(self.root)
        GraphicEditor(window)
    
    def open_task5(self):
        """Открыть задачу 5"""
        window = tk.Toplevel(self.root)
        PongGame(window)


def main():
    """Точка входа"""
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
