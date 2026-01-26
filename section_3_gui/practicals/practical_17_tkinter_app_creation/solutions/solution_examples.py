# Решения для практического занятия 17: Создание GUI с помощью Tkinter

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import os
import json
from typing import Dict, Any, List, Optional
import threading
import time
import math
import random

# Решение задания 1: Создание базового окна
class BasicWindowSolution:
    """Решение для задания 1: Создание базового окна"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Решение задания 1: Базовое окно")
        self.root.geometry("600x400")
        self.root.resizable(True, True)
        
        # Устанавливаем иконку (если файл существует)
        try:
            if os.path.exists("app_icon.ico"):
                self.root.iconbitmap("app_icon.ico")
        except:
            pass  # Игнорируем ошибку, если иконка не найдена
        
        # Центрируем окно на экране
        self.center_window()
        
        # Обработчик закрытия окна
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Основной фрейм
        self.main_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Приветственная метка
        self.welcome_label = tk.Label(
            self.main_frame,
            text="Добро пожаловать в приложение Tkinter!",
            font=("Arial", 18, "bold"),
            fg="#2c3e50",
            bg="#f0f0f0"
        )
        self.welcome_label.pack(pady=20)
        
        # Описание функций
        description = tk.Label(
            self.main_frame,
            text="Это базовое окно Tkinter с настройками размера,\nпозиционированием и обработкой закрытия.",
            font=("Arial", 12),
            fg="#7f8c8d",
            bg="#f0f0f0"
        )
        description.pack(pady=10)
        
        # Кнопка для демонстрации
        self.demo_button = tk.Button(
            self.main_frame,
            text="Проверить решение",
            command=self.demo_action,
            bg="#3498db",
            fg="white",
            font=("Arial", 12, "bold"),
            padx=20,
            pady=10
        )
        self.demo_button.pack(pady=20)
        
        # Метка для отображения статуса
        self.status_label = tk.Label(
            self.main_frame,
            text="Готово к работе",
            font=("Arial", 10),
            fg="#27ae60",
            bg="#f0f0f0"
        )
        self.status_label.pack(pady=10)
    
    def center_window(self):
        """Центрирует окно на экране"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def on_closing(self):
        """Обработчик закрытия окна"""
        if messagebox.askokcancel("Выход", "Вы уверены, что хотите закрыть приложение?"):
            self.root.destroy()
    
    def demo_action(self):
        """Демонстрационное действие для кнопки"""
        self.status_label.config(text="Кнопка нажата!", fg="#e74c3c")
        self.root.after(2000, lambda: self.status_label.config(text="Готово к работе", fg="#27ae60"))
    
    def run(self):
        self.root.mainloop()

# Решение задания 2: Работа с виджетами
class WidgetCollectionSolution:
    """Решение для задания 2: Работа с виджетами"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Решение задания 2: Коллекция виджетов")
        self.root.geometry("800x600")
        
        # Создаем ноутбук для организации виджетов
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Создаем вкладки
        self.basic_widgets_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.basic_widgets_frame, text="Основные виджеты")
        self.create_basic_widgets()
        
        self.interactive_widgets_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.interactive_widgets_frame, text="Интерактивные виджеты")
        self.create_interactive_widgets()
        
        self.advanced_widgets_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.advanced_widgets_frame, text="Расширенные виджеты")
        self.create_advanced_widgets()
    
    def create_basic_widgets(self):
        """Создает основные виджеты"""
        # Фрейм для основных виджетов
        frame = ttk.LabelFrame(self.basic_widgets_frame, text="Основные виджеты")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Кнопки
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Обычная кнопка", command=self.normal_button_click).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Стилизованная кнопка", style="Accent.TButton", command=self.accent_button_click).pack(side=tk.LEFT, padx=5)
        
        # Метка
        ttk.Label(frame, text="Это обычная метка").pack(pady=5)
        
        # Поле ввода
        self.entry_var = tk.StringVar(value="Введите текст здесь...")
        entry = ttk.Entry(frame, textvariable=self.entry_var, width=30)
        entry.pack(pady=5)
        
        # Текстовая область
        text_frame = ttk.Frame(frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        text_scrollbar = ttk.Scrollbar(text_frame)
        text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_area = tk.Text(text_frame, height=5, wrap=tk.WORD, yscrollcommand=text_scrollbar.set)
        self.text_area.pack(fill=tk.BOTH, expand=True)
        text_scrollbar.config(command=self.text_area.yview)
        
        # Флажок
        self.check_var = tk.BooleanVar()
        ttk.Checkbutton(frame, text="Флажок", variable=self.check_var, command=self.checkbox_changed).pack(pady=5)
        
        # Переключатели
        radio_frame = ttk.Frame(frame)
        radio_frame.pack(fill=tk.X, pady=5)
        
        self.radio_var = tk.StringVar(value="option1")
        ttk.Radiobutton(radio_frame, text="Опция 1", variable=self.radio_var, value="option1", command=self.radio_changed).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(radio_frame, text="Опция 2", variable=self.radio_var, value="option2", command=self.radio_changed).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(radio_frame, text="Опция 3", variable=self.radio_var, value="option3", command=self.radio_changed).pack(side=tk.LEFT, padx=5)
    
    def create_interactive_widgets(self):
        """Создает интерактивные виджеты"""
        # Фрейм для интерактивных виджетов
        frame = ttk.LabelFrame(self.interactive_widgets_frame, text="Интерактивные виджеты")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Слайдер
        slider_frame = ttk.Frame(frame)
        slider_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(slider_frame, text="Слайдер:").pack(anchor=tk.W)
        self.slider_var = tk.DoubleVar()
        slider = ttk.Scale(slider_frame, from_=0, to=100, variable=self.slider_var, orient=tk.HORIZONTAL, command=self.slider_changed)
        slider.pack(fill=tk.X, pady=5)
        
        self.slider_label = ttk.Label(slider_frame, text="Значение: 0.0")
        self.slider_label.pack()
        
        # Прогресс бар
        progress_frame = ttk.Frame(frame)
        progress_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(progress_frame, text="Прогресс бар:").pack(anchor=tk.W)
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        # Кнопка для запуска анимации прогресса
        ttk.Button(progress_frame, text="Запустить анимацию", command=self.animate_progress).pack(pady=5)
    
    def create_advanced_widgets(self):
        """Создает расширенные виджеты"""
        # Фрейм для расширенных виджетов
        frame = ttk.LabelFrame(self.advanced_widgets_frame, text="Расширенные виджеты")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Комбинированный список
        combo_frame = ttk.Frame(frame)
        combo_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(combo_frame, text="Комбинированный список:").pack(anchor=tk.W)
        self.combo_var = tk.StringVar()
        combo = ttk.Combobox(combo_frame, textvariable=self.combo_var, values=["Элемент 1", "Элемент 2", "Элемент 3", "Элемент 4"])
        combo.pack(fill=tk.X, pady=5)
        combo.bind("<<ComboboxSelected>>", self.combo_selected)
        
        # Список
        list_frame = ttk.Frame(frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        ttk.Label(list_frame, text="Список:").pack(anchor=tk.W)
        
        list_scrollbar = ttk.Scrollbar(list_frame)
        list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.listbox = tk.Listbox(list_frame, yscrollcommand=list_scrollbar.set)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        list_scrollbar.config(command=self.listbox.yview)
        
        # Добавляем элементы в список
        for i in range(1, 21):
            self.listbox.insert(tk.END, f"Элемент {i}")
        
        # Привязываем событие выбора
        self.listbox.bind("<<ListboxSelect>>", self.listbox_selected)
    
    def normal_button_click(self):
        """Обработчик обычной кнопки"""
        messagebox.showinfo("Информация", "Нажата обычная кнопка")
    
    def accent_button_click(self):
        """Обработчик стилизованной кнопки"""
        messagebox.showinfo("Информация", "Нажата стилизованная кнопка")
    
    def checkbox_changed(self):
        """Обработчик изменения флажка"""
        state = "отмечен" if self.check_var.get() else "не отмечен"
        self.text_area.insert(tk.END, f"Флажок {state}\n")
        self.text_area.see(tk.END)
    
    def radio_changed(self):
        """Обработчик изменения переключателя"""
        selected = self.radio_var.get()
        self.text_area.insert(tk.END, f"Выбрана опция: {selected}\n")
        self.text_area.see(tk.END)
    
    def slider_changed(self, value):
        """Обработчик изменения слайдера"""
        self.slider_label.config(text=f"Значение: {float(value):.1f}")
        self.progress_var.set(float(value))
    
    def animate_progress(self):
        """Анимация прогресс бара"""
        def animate():
            for i in range(101):
                self.progress_var.set(i)
                self.root.update()
                time.sleep(0.02)
            self.progress_var.set(0)
        
        # Запускаем анимацию в отдельном потоке, чтобы не блокировать интерфейс
        animation_thread = threading.Thread(target=animate)
        animation_thread.daemon = True
        animation_thread.start()
    
    def combo_selected(self, event):
        """Обработчик выбора в комбинированном списке"""
        selected = self.combo_var.get()
        self.text_area.insert(tk.END, f"Выбран элемент: {selected}\n")
        self.text_area.see(tk.END)
    
    def listbox_selected(self, event):
        """Обработчик выбора в списке"""
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            value = self.listbox.get(index)
            self.text_area.insert(tk.END, f"Выбран из списка: {value}\n")
            self.text_area.see(tk.END)
    
    def run(self):
        self.root.mainloop()

# Решение задания 3: Расположение элементов
class LayoutManagementSolution:
    """Решение для задания 3: Расположение элементов"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Решение задания 3: Расположение элементов")
        self.root.geometry("900x700")
        
        # Создаем ноутбук для демонстрации разных менеджеров
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Вкладка для pack
        self.pack_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.pack_frame, text="Pack")
        self.create_pack_layout()
        
        # Вкладка для grid
        self.grid_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.grid_frame, text="Grid")
        self.create_grid_layout()
        
        # Вкладка для place
        self.place_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.place_frame, text="Place")
        self.create_place_layout()
    
    def create_pack_layout(self):
        """Создает макет с использованием pack"""
        # Фрейм для примера pack
        frame = ttk.LabelFrame(self.pack_frame, text="Пример использования pack")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Верхняя панель
        top_frame = ttk.Frame(frame)
        top_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(top_frame, text="Слева", command=lambda: self.log_pack_action("Кнопка СЛЕВА")).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Справа", command=lambda: self.log_pack_action("Кнопка СПРАВА")).pack(side=tk.RIGHT, padx=5)
        ttk.Button(top_frame, text="По центру", command=lambda: self.log_pack_action("Кнопка ЦЕНТР")).pack(pady=5)
        
        # Средняя часть с фреймами
        middle_frame = ttk.Frame(frame)
        middle_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Левая колонка
        left_col = ttk.Frame(middle_frame, relief=tk.RAISED, borderwidth=1)
        left_col.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        for i in range(3):
            ttk.Button(left_col, text=f"Лево {i+1}", 
                      command=lambda x=i: self.log_pack_action(f"Левая кнопка {x+1}")).pack(pady=2, padx=5)
        
        # Правая колонка
        right_col = ttk.Frame(middle_frame, relief=tk.RAISED, borderwidth=1)
        right_col.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        for i in range(3):
            ttk.Button(right_col, text=f"Право {i+1}", 
                      command=lambda x=i: self.log_pack_action(f"Правая кнопка {x+1}")).pack(pady=2, padx=5)
        
        # Нижняя панель
        bottom_frame = ttk.Frame(frame)
        bottom_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(bottom_frame, text="Нижняя панель с pack").pack(pady=5)
        
        # Лог для действий
        self.pack_log = tk.Text(frame, height=5, state=tk.DISABLED)
        self.pack_log.pack(fill=tk.X, pady=5)
    
    def log_pack_action(self, action):
        """Логирует действие для pack примера"""
        self.pack_log.config(state=tk.NORMAL)
        self.pack_log.insert(tk.END, f"Pack: {action}\n")
        self.pack_log.see(tk.END)
        self.pack_log.config(state=tk.DISABLED)
    
    def create_grid_layout(self):
        """Создает макет с использованием grid"""
        # Фрейм для примера grid
        frame = ttk.LabelFrame(self.grid_frame, text="Пример использования grid")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Настраиваем сетку
        for i in range(4):
            frame.columnconfigure(i, weight=1)
            frame.rowconfigure(i, weight=1)
        
        # Создаем сетку кнопок
        positions = [
            (0, 0, "Кнопка 1", "nw"), (0, 1, "Кнопка 2", "nsew"), (0, 2, "Кнопка 3", "ne"),
            (1, 0, "Кнопка 4", "w"), (1, 1, "Центр", "nsew"), (1, 2, "Кнопка 6", "e"),
            (2, 0, "Кнопка 7", "sw"), (2, 1, "Кнопка 8", "swe"), (2, 2, "Кнопка 9", "se")
        ]
        
        for row, col, text, sticky in positions:
            btn = ttk.Button(frame, text=text, command=lambda t=text: self.log_grid_action(f"Grid - {t}"))
            btn.grid(row=row, column=col, sticky=sticky, padx=2, pady=2)
        
        # Добавляем дополнительные элементы
        # Поле ввода внизу
        input_frame = ttk.Frame(frame)
        input_frame.grid(row=3, column=0, columnspan=4, sticky="ew", pady=5)
        
        ttk.Label(input_frame, text="Ввод с grid:").pack(anchor=tk.W)
        self.grid_entry = ttk.Entry(input_frame)
        self.grid_entry.pack(fill=tk.X, pady=2)
        
        ttk.Button(input_frame, text="Отправить", command=self.grid_submit).pack(pady=2)
        
        # Лог для действий
        self.grid_log = tk.Text(frame, height=5, state=tk.DISABLED)
        self.grid_log.grid(row=4, column=0, columnspan=4, sticky="ew", pady=5)
    
    def log_grid_action(self, action):
        """Логирует действие для grid примера"""
        self.grid_log.config(state=tk.NORMAL)
        self.grid_log.insert(tk.END, f"{action}\n")
        self.grid_log.see(tk.END)
        self.grid_log.config(state=tk.DISABLED)
    
    def grid_submit(self):
        """Обработчик отправки в grid примере"""
        text = self.grid_entry.get()
        if text:
            self.log_grid_action(f"Отправлено: {text}")
            self.grid_entry.delete(0, tk.END)
    
    def create_place_layout(self):
        """Создает макет с использованием place"""
        # Фрейм для примера place
        frame = ttk.LabelFrame(self.place_frame, text="Пример использования place")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Создаем виджеты с точным позиционированием
        elements = [
            (50, 50, "Кнопка 1", lambda: self.log_place_action("Кнопка 1")),
            (200, 50, "Кнопка 2", lambda: self.log_place_action("Кнопка 2")),
            (50, 150, "Кнопка 3", lambda: self.log_place_action("Кнопка 3")),
            (200, 150, "Кнопка 4", lambda: self.log_place_action("Кнопка 4")),
            (125, 100, "Центр", lambda: self.log_place_action("Центральная кнопка"))
        ]
        
        for x, y, text, command in elements:
            btn = ttk.Button(frame, text=text, command=command)
            btn.place(x=x, y=y)
        
        # Поле ввода в правом верхнем углу
        self.place_entry = ttk.Entry(frame)
        self.place_entry.place(relx=0.7, rely=0.1, anchor=tk.NE)
        ttk.Label(frame, text="Ввод:").place(relx=0.7, rely=0.05, anchor=tk.NE)
        
        # Кнопка в левом нижнем углу
        ttk.Button(frame, text="Лево-низ", 
                  command=lambda: self.log_place_action("Кнопка в левом нижнем углу")).place(relx=0.1, rely=0.9, anchor=tk.SW)
        
        # Лог для действий
        self.place_log = tk.Text(frame, height=5, state=tk.DISABLED)
        self.place_log.place(relx=0.5, rely=0.8, anchor=tk.CENTER, relwidth=0.9, height=80)
    
    def log_place_action(self, action):
        """Логирует действие для place примера"""
        self.place_log.config(state=tk.NORMAL)
        self.place_log.insert(tk.END, f"Place: {action}\n")
        self.place_log.see(tk.END)
        self.place_log.config(state=tk.DISABLED)
    
    def run(self):
        self.root.mainloop()

# Решение задания 4: Обработка событий
class EventHandlingSolution:
    """Решение для задания 4: Обработка событий"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Решение задания 4: Обработка событий")
        self.root.geometry("800x600")
        
        # Создаем Canvas для демонстрации событий мыши
        self.canvas = tk.Canvas(self.root, bg="white", width=780, height=450)
        self.canvas.pack(pady=10)
        
        # Привязываем события мыши
        self.canvas.bind("<Button-1>", self.left_click)  # Левый клик
        self.canvas.bind("<Button-3>", self.right_click)  # Правый клик
        self.canvas.bind("<B1-Motion>", self.mouse_drag)  # Перетаскивание левой кнопкой
        self.canvas.bind("<Motion>", self.mouse_move)  # Движение мыши
        self.canvas.bind("<Double-Button-1>", self.double_click)  # Двойной клик
        
        # Привязываем события клавиатуры
        self.root.bind("<KeyPress>", self.key_press)
        self.root.bind("<KeyRelease>", self.key_release)
        self.root.bind("<Control-c>", self.ctrl_c)
        self.root.bind("<Control-v>", self.ctrl_v)
        
        # Информационная панель
        info_frame = ttk.Frame(self.root)
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Координаты
        coord_frame = ttk.Frame(info_frame)
        coord_frame.pack(side=tk.LEFT)
        
        ttk.Label(coord_frame, text="Координаты:").pack(anchor=tk.W)
        self.coord_label = ttk.Label(coord_frame, text="(0, 0)")
        self.coord_label.pack(anchor=tk.W)
        
        # Событие
        event_frame = ttk.Frame(info_frame)
        event_frame.pack(side=tk.LEFT, padx=20)
        
        ttk.Label(event_frame, text="Событие:").pack(anchor=tk.W)
        self.event_label = ttk.Label(event_frame, text="Нет")
        self.event_label.pack(anchor=tk.W)
        
        # Клавиша
        key_frame = ttk.Frame(info_frame)
        key_frame.pack(side=tk.LEFT, padx=20)
        
        ttk.Label(key_frame, text="Клавиша:").pack(anchor=tk.W)
        self.key_label = ttk.Label(key_frame, text="Нет")
        self.key_label.pack(anchor=tk.W)
        
        # Кнопка фокуса
        focus_btn = ttk.Button(info_frame, text="Фокус", command=self.focus_here)
        focus_btn.pack(side=tk.RIGHT, padx=5)
        focus_btn.focus_set()  # Устанавливаем фокус на кнопку
    
    def left_click(self, event):
        """Обработка левого клика мыши"""
        self.coord_label.config(text=f"({event.x}, {event.y})")
        self.event_label.config(text="Левый клик")
        # Рисуем круг по клику
        self.canvas.create_oval(event.x-10, event.y-10, event.x+10, event.y+10, 
                               outline="blue", width=2, tags="click")
    
    def right_click(self, event):
        """Обработка правого клика мыши"""
        self.coord_label.config(text=f"({event.x}, {event.y})")
        self.event_label.config(text="Правый клик")
        # Рисуем квадрат по клику
        self.canvas.create_rectangle(event.x-10, event.y-10, event.x+10, event.y+10, 
                                    outline="red", width=2, tags="click")
    
    def mouse_drag(self, event):
        """Обработка перетаскивания мыши"""
        self.coord_label.config(text=f"({event.x}, {event.y})")
        self.event_label.config(text="Перетаскивание")
        # Рисуем точку при перетаскивании
        self.canvas.create_oval(event.x-2, event.y-2, event.x+2, event.y+2, 
                               fill="black", tags="drag")
    
    def mouse_move(self, event):
        """Обработка движения мыши без нажатия"""
        self.coord_label.config(text=f"({event.x}, {event.y})")
        # Не обновляем событие при движении, чтобы не перегружать информацию
    
    def double_click(self, event):
        """Обработка двойного клика"""
        self.event_label.config(text="Двойной клик")
        # Очищаем холст по двойному клику
        self.canvas.delete("click", "drag", "draw")
    
    def key_press(self, event):
        """Обработка нажатия клавиши"""
        self.key_label.config(text=event.keysym)
        self.event_label.config(text=f"Нажата: {event.keysym}")
        
        # Обработка специальных клавиш
        if event.keysym == "c":
            self.canvas.delete("all")  # Очистить холст по клавише C
        elif event.keysym == "q":
            self.root.quit()  # Выйти по клавише Q
        elif event.keysym == "r":
            # Нарисовать случайную фигуру
            x = random.randint(50, 730)
            y = random.randint(50, 400)
            size = random.randint(10, 30)
            color = random.choice(["red", "blue", "green", "yellow", "purple"])
            self.canvas.create_rectangle(x-size, y-size, x+size, y+size, 
                                        fill=color, outline="black", tags="draw")
    
    def key_release(self, event):
        """Обработка отпускания клавиши"""
        # В этом примере не используем
        pass
    
    def ctrl_c(self, event):
        """Обработка комбинации Ctrl+C"""
        self.event_label.config(text="Ctrl+C")
        messagebox.showinfo("Информация", "Комбинация Ctrl+C нажата!")
        return "break"  # Предотвращаем дальнейшую обработку
    
    def ctrl_v(self, event):
        """Обработка комбинации Ctrl+V"""
        self.event_label.config(text="Ctrl+V")
        messagebox.showinfo("Информация", "Комбинация Ctrl+V нажата!")
        return "break"  # Предотвращаем дальнейшую обработку
    
    def focus_here(self):
        """Установка фокуса на окно"""
        self.root.focus_set()
        self.event_label.config(text="Фокус установлен")
    
    def run(self):
        self.root.mainloop()

# Решение задания 5: Комплексное приложение
class CalculatorSolution:
    """Решение для задания 5: Комплексное приложение - Калькулятор"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Калькулятор - Решение задания 5")
        self.root.geometry("400x600")
        self.root.resizable(False, False)
        
        # Переменные состояния калькулятора
        self.current = "0"
        self.previous = ""
        self.operator = ""
        self.new_number = True
        
        # Создаем дисплей
        self.display_var = tk.StringVar(value="0")
        display_frame = tk.Frame(self.root, bg="#2c3e50", padx=10, pady=10)
        display_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.display = tk.Entry(
            display_frame,
            textvariable=self.display_var,
            font=("Arial", 24),
            justify="right",
            state="readonly",
            readonlybackground="#ecf0f1",
            fg="#2c3e50"
        )
        self.display.pack(fill=tk.BOTH, expand=True)
        
        # Создаем фрейм для кнопок
        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Определяем кнопки
        buttons = [
            [
                ("C", self.clear, "#e74c3c"), ("±", self.sign_change, "#95a5a6"), ("%", self.percent, "#95a5a6"), ("/", lambda: self.set_operator("/"), "#f39c12")
            ],
            [
                ("7", lambda: self.number_click("7"), "#bdc3c7"), ("8", lambda: self.number_click("8"), "#bdc3c7"), ("9", lambda: self.number_click("9"), "#bdc3c7"), ("*", lambda: self.set_operator("*"), "#f39c12")
            ],
            [
                ("4", lambda: self.number_click("4"), "#bdc3c7"), ("5", lambda: self.number_click("5"), "#bdc3c7"), ("6", lambda: self.number_click("6"), "#bdc3c7"), ("-", lambda: self.set_operator("-"), "#f39c12")
            ],
            [
                ("1", lambda: self.number_click("1"), "#bdc3c7"), ("2", lambda: self.number_click("2"), "#bdc3c7"), ("3", lambda: self.number_click("3"), "#bdc3c7"), ("+", lambda: self.set_operator("+"), "#f39c12")
            ],
            [
                ("0", lambda: self.number_click("0"), "#bdc3c7"), (".", lambda: self.number_click("."), "#bdc3c7"), ("⌫", self.backspace, "#e67e22"), ("=", self.equals, "#2ecc71")
            ]
        ]
        
        # Создаем кнопки
        for i, row in enumerate(buttons):
            for j, (text, command, color) in enumerate(row):
                btn = tk.Button(
                    buttons_frame,
                    text=text,
                    font=("Arial", 18),
                    bg=color,
                    fg="white",
                    command=command,
                    relief=tk.RAISED,
                    bd=2
                )
                btn.grid(row=i, column=j, sticky="nsew", padx=2, pady=2)
        
        # Настраиваем вес столбцов и строк
        for i in range(4):
            buttons_frame.columnconfigure(i, weight=1)
        for i in range(5):
            buttons_frame.rowconfigure(i, weight=1)
    
    def number_click(self, number):
        """Обработка нажатия цифровой кнопки"""
        if self.new_number:
            self.current = number
            self.new_number = False
        else:
            # Предотвращаем ввод нескольких точек
            if number == "." and "." in self.current:
                return
            self.current += number
        
        self.display_var.set(self.current)
    
    def set_operator(self, op):
        """Установка оператора"""
        if self.operator and not self.new_number:
            self.equals()  # Выполняем предыдущую операцию
        
        self.previous = self.current
        self.operator = op
        self.new_number = True
    
    def equals(self):
        """Выполнение операции равно"""
        if self.operator and self.previous:
            try:
                prev_num = float(self.previous)
                curr_num = float(self.current)
                
                if self.operator == "+":
                    result = prev_num + curr_num
                elif self.operator == "-":
                    result = prev_num - curr_num
                elif self.operator == "*":
                    result = prev_num * curr_num
                elif self.operator == "/":
                    if curr_num == 0:
                        messagebox.showerror("Ошибка", "Деление на ноль!")
                        return
                    result = prev_num / curr_num
                else:
                    return  # Неизвестный оператор
                
                # Форматируем результат
                if result == int(result):
                    result = int(result)
                
                self.current = str(result)
                self.display_var.set(self.current)
                self.operator = ""
                self.previous = ""
                self.new_number = True
            except ValueError:
                messagebox.showerror("Ошибка", "Неверный ввод!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка вычисления: {str(e)}")
    
    def clear(self):
        """Очистка калькулятора"""
        self.current = "0"
        self.previous = ""
        self.operator = ""
        self.new_number = True
        self.display_var.set("0")
    
    def sign_change(self):
        """Смена знака числа"""
        if self.current != "0":
            if self.current.startswith("-"):
                self.current = self.current[1:]
            else:
                self.current = "-" + self.current
            self.display_var.set(self.current)
    
    def percent(self):
        """Вычисление процента"""
        try:
            num = float(self.current) / 100
            self.current = str(num)
            self.display_var.set(self.current)
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный ввод!")
    
    def backspace(self):
        """Удаление последнего символа"""
        if len(self.current) > 1:
            self.current = self.current[:-1]
        else:
            self.current = "0"
            self.new_number = True
        self.display_var.set(self.current)
    
    def run(self):
        self.root.mainloop()

# Дополнительные примеры использования Tkinter
class AdvancedTkinterExamples:
    """Дополнительные примеры продвинутого использования Tkinter"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Дополнительные примеры Tkinter")
        self.root.geometry("800x700")
        
        # Создаем ноутбук для различных примеров
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Вкладка для Canvas примеров
        self.canvas_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.canvas_frame, text="Canvas примеры")
        self.create_canvas_examples()
        
        # Вкладка для Toplevel окон
        self.toplevel_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.toplevel_frame, text="Доп. окна")
        self.create_toplevel_examples()
        
        # Вкладка для стилизации
        self.style_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.style_frame, text="Стилизация")
        self.create_styling_examples()
    
    def create_canvas_examples(self):
        """Создает примеры использования Canvas"""
        # Фрейм для примеров Canvas
        frame = ttk.LabelFrame(self.canvas_frame, text="Примеры Canvas")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas для рисования
        self.canvas = tk.Canvas(frame, bg="white", width=750, height=500)
        self.canvas.pack(pady=10)
        
        # Кнопки для различных примеров
        buttons_frame = ttk.Frame(frame)
        buttons_frame.pack(fill=tk.X)
        
        ttk.Button(buttons_frame, text="Нарисовать фигуры", command=self.draw_shapes).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Анимация", command=self.animate_shapes).pack(side=tk.LEFT, padx=5)
        ttk.Button(buttons_frame, text="Очистить", command=self.clear_canvas).pack(side=tk.LEFT, padx=5)
    
    def draw_shapes(self):
        """Рисует различные фигуры на Canvas"""
        self.canvas.delete("all")
        
        # Рисуем несколько фигур
        self.canvas.create_rectangle(50, 150, 150, fill="red", outline="black", width=2)
        self.canvas.create_oval(200, 50, 300, 150, fill="green", outline="black", width=2)
        self.canvas.create_polygon(350, 400, 150, 300, 150, fill="blue", outline="black", width=2)
        self.canvas.create_line(50, 200, 400, 200, fill="purple", width=3)
        self.canvas.create_text(225, 250, text="Пример текста на Canvas", font=("Arial", 16), fill="orange")
        
        # Рисуем дугу
        self.canvas.create_arc(50, 300, 150, 400, start=0, extent=180, fill="yellow", outline="black")
    
    def animate_shapes(self):
        """Анимирует фигуры на Canvas"""
        self.canvas.delete("all")
        
        # Создаем движущийся объект
        moving_rect = self.canvas.create_rectangle(50, 200, 80, 230, fill="red", outline="black")
        
        def move_rect():
            current_coords = self.canvas.coords(moving_rect)
            if current_coords:
                x1, y1, x2, y2 = current_coords
                if x2 < 700:
                    self.canvas.move(moving_rect, 5, 0)
                    self.root.after(50, move_rect)  # Повторяем через 50мс
        
        move_rect()
    
    def clear_canvas(self):
        """Очищает Canvas"""
        self.canvas.delete("all")
    
    def create_toplevel_examples(self):
        """Создает примеры использования Toplevel окон"""
        frame = ttk.LabelFrame(self.toplevel_frame, text="Примеры дополнительных окон")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Кнопки для создания разных типов окон
        ttk.Button(frame, text="Диалоговое окно", command=self.show_dialog).pack(pady=10)
        ttk.Button(frame, text="Настройки", command=self.show_settings).pack(pady=10)
        ttk.Button(frame, text="О программе", command=self.show_about).pack(pady=10)
    
    def show_dialog(self):
        """Показывает диалоговое окно"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Диалоговое окно")
        dialog.geometry("300x150")
        dialog.transient(self.root)  # Делаем окно зависимым
        dialog.grab_set()  # Захватываем фокус
        
        tk.Label(dialog, text="Это диалоговое окно").pack(pady=20)
        
        button_frame = ttk.Frame(dialog)
        button_frame.pack(pady=10)
        
        def close_dialog():
            dialog.destroy()
        
        ttk.Button(button_frame, text="OK", command=close_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Отмена", command=close_dialog).pack(side=tk.LEFT, padx=5)
    
    def show_settings(self):
        """Показывает окно настроек"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Настройки")
        settings_window.geometry("400x300")
        settings_window.transient(self.root)
        
        # Создаем вкладки для разных настроек
        notebook = ttk.Notebook(settings_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Вкладка общих настроек
        general_frame = ttk.Frame(notebook)
        notebook.add(general_frame, text="Общие")
        
        ttk.Label(general_frame, text="Имя пользователя:").pack(anchor=tk.W, pady=5)
        username_entry = ttk.Entry(general_frame)
        username_entry.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(general_frame, text="Тема интерфейса:").pack(anchor=tk.W, pady=5)
        theme_combo = ttk.Combobox(general_frame, values=["Светлая", "Темная", "Системная"])
        theme_combo.pack(fill=tk.X, padx=10, pady=5)
        theme_combo.set("Системная")
        
        # Вкладка безопасности
        security_frame = ttk.Frame(notebook)
        notebook.add(security_frame, text="Безопасность")
        
        ttk.Checkbutton(security_frame, text="Включить двухфакторную аутентификацию").pack(anchor=tk.W, pady=5)
        ttk.Checkbutton(security_frame, text="Запрашивать пароль при запуске").pack(anchor=tk.W, pady=5)
    
    def show_about(self):
        """Показывает окно "О программе" """
        about_text = """
        Приложение "Примеры Tkinter"
        
        Версия: 1.0.0
        Автор: Разработчик приложений
        Лицензия: MIT
        
        Этот пример демонстрирует различные возможности
        библиотеки Tkinter для создания GUI приложений.
        """
        
        messagebox.showinfo("О программе", about_text)
    
    def create_styling_examples(self):
        """Создает примеры стилизации"""
        frame = ttk.LabelFrame(self.style_frame, text="Примеры стилизации")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Создаем стиль
        style = ttk.Style()
        style.configure("Custom.TButton", foreground="white", background="#3498db", font=("Arial", 12, "bold"))
        style.map("Custom.TButton", 
                 foreground=[('active', 'white')],
                 background=[('active', '#2980b9')])
        
        # Примеры стилизованных кнопок
        ttk.Button(frame, text="Обычная кнопка", style="TButton").pack(pady=5)
        ttk.Button(frame, text="Стилизованная кнопка", style="Custom.TButton").pack(pady=5)
        
        # Примеры цветовых схем
        themes_frame = ttk.LabelFrame(frame, text="Цветовые схемы")
        themes_frame.pack(fill=tk.X, pady=10)
        
        themes = [
            ("Accent.TButton", "Акцентная кнопка"),
            ("Outline.TButton", "Контурная кнопка"),
            ("Link.TLabel", "Ссылка")
        ]
        
        for style_name, label in themes:
            try:
                ttk.Button(themes_frame, text=label, style=style_name).pack(pady=2)
            except tk.TclError:
                # Некоторые стили могут не поддерживаться в данной теме
                ttk.Label(themes_frame, text=f"{label} (стиль не поддерживается)").pack(pady=2)
    
    def run(self):
        self.root.mainloop()

def demonstrate_tkinter_solutions():
    """Демонстрирует все решения для практического занятия 17"""
    print("=== Решения для практического занятия 17: Tkinter ===")
    
    print("\n1. Решение задания 1: Базовое окно")
    # basic_solution = BasicWindowSolution()
    # basic_solution.run()  # Закомментировано, чтобы не открывать окно автоматически
    
    print("\n2. Решение задания 2: Коллекция виджетов")
    # widget_solution = WidgetCollectionSolution()
    # widget_solution.run()  # Закомментировано
    
    print("\n3. Решение задания 3: Расположение элементов")
    # layout_solution = LayoutManagementSolution()
    # layout_solution.run()  # Закомментировано
    
    print("\n4. Решение задания 4: Обработка событий")
    # event_solution = EventHandlingSolution()
    # event_solution.run()  # Закомментировано
    
    print("\n5. Решение задания 5: Калькулятор")
    # calc_solution = CalculatorSolution()
    # calc_solution.run()  # Закомментировано
    
    print("\n6. Дополнительные примеры")
    # advanced_examples = AdvancedTkinterExamples()
    # advanced_examples.run()  # Закомментировано
    
    # Для демонстрации запустим только одно приложение
    print("Для запуска приложений раскомментируйте соответствующие строки в коде")

if __name__ == "__main__":
    demonstrate_tkinter_solutions()