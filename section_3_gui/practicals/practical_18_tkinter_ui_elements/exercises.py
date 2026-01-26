# Упражнения для практического занятия 18: Tkinter - элементы пользовательского интерфейса

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
import os
import json
from typing import Dict, Any, List, Optional
import threading
import time
import math

# Задание 1: Основные виджеты ввода
class InputWidgetsApp:
    """Приложение с основными виджетами ввода"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Задание 1: Основные виджеты ввода")
        self.root.geometry("700x600")
        
        # Создаем фрейм для виджетов ввода
        input_frame = ttk.LabelFrame(self.root, text="Виджеты ввода")
        input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Entry (одиночный ввод)
        entry_frame = ttk.Frame(input_frame)
        entry_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(entry_frame, text="Entry (одиночный ввод):").pack(anchor=tk.W)
        self.entry_var = tk.StringVar(value="Введите текст...")
        self.entry_widget = ttk.Entry(entry_frame, textvariable=self.entry_var, width=40)
        self.entry_widget.pack(fill=tk.X, pady=2)
        
        # Text (многострочный ввод)
        text_frame = ttk.Frame(input_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        ttk.Label(text_frame, text="Text (многострочный ввод):").pack(anchor=tk.W)
        
        text_scrollbar = ttk.Scrollbar(text_frame)
        text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_widget = tk.Text(text_frame, height=6, wrap=tk.WORD, yscrollcommand=text_scrollbar.set)
        self.text_widget.pack(fill=tk.BOTH, expand=True, pady=2)
        text_scrollbar.config(command=self.text_widget.yview)
        
        # Spinbox (выбор из диапазона)
        spinbox_frame = ttk.Frame(input_frame)
        spinbox_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(spinbox_frame, text="Spinbox (диапазон 1-100):").pack(anchor=tk.W)
        self.spinbox_var = tk.IntVar(value=50)
        self.spinbox_widget = tk.Spinbox(spinbox_frame, from_=1, to=100, textvariable=self.spinbox_var, width=10)
        self.spinbox_widget.pack(pady=2)
        
        # Combobox (выбор из списка)
        combo_frame = ttk.Frame(input_frame)
        combo_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(combo_frame, text="Combobox (выбор из списка):").pack(anchor=tk.W)
        self.combo_var = tk.StringVar()
        self.combo_widget = ttk.Combobox(combo_frame, textvariable=self.combo_var, 
                                        values=["Элемент 1", "Элемент 2", "Элемент 3", "Элемент 4", "Элемент 5"])
        self.combo_widget.pack(fill=tk.X, pady=2)
        self.combo_widget.bind("<<ComboboxSelected>>", self.combo_selected)
        
        # Кнопка для демонстрации получения значений
        ttk.Button(input_frame, text="Получить значения", command=self.get_values).pack(pady=10)
        
        # Метка для отображения полученных значений
        self.values_label = ttk.Label(input_frame, text="Значения будут отображены здесь", foreground="blue")
        self.values_label.pack(pady=5)
    
    def combo_selected(self, event):
        """Обработчик выбора в комбинированном списке"""
        selected = self.combo_var.get()
        self.text_widget.insert(tk.END, f"Выбран элемент: {selected}\n")
        self.text_widget.see(tk.END)
    
    def get_values(self):
        """Получает значения из всех виджетов ввода"""
        entry_value = self.entry_var.get()
        text_value = self.text_widget.get("1.0", tk.END).strip()
        spinbox_value = self.spinbox_var.get()
        combo_value = self.combo_var.get()
        
        values_text = f"Entry: '{entry_value}'\nText: '{text_value[:50]}...'\nSpinbox: {spinbox_value}\nCombobox: '{combo_value}'"
        self.values_label.config(text=values_text)
    
    def run(self):
        self.root.mainloop()

# Задание 2: Кнопки и переключатели
class ButtonToggleApp:
    """Приложение с кнопками и переключателями"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Задание 2: Кнопки и переключатели")
        self.root.geometry("700x600")
        
        # Создаем фрейм для кнопок
        button_frame = ttk.LabelFrame(self.root, text="Кнопки и переключатели")
        button_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Обычные кнопки
        normal_buttons_frame = ttk.Frame(button_frame)
        normal_buttons_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(normal_buttons_frame, text="Обычные кнопки:").pack(anchor=tk.W)
        
        button_row = ttk.Frame(normal_buttons_frame)
        button_row.pack(fill=tk.X)
        
        ttk.Button(button_row, text="Кнопка 1", command=lambda: self.button_clicked("1")).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_row, text="Кнопка 2", command=lambda: self.button_clicked("2")).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_row, text="Кнопка 3", command=lambda: self.button_clicked("3")).pack(side=tk.LEFT, padx=5)
        
        # Стилизованные кнопки
        styled_buttons_frame = ttk.Frame(button_frame)
        styled_buttons_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(styled_buttons_frame, text="Стилизованные кнопки:").pack(anchor=tk.W)
        
        style = ttk.Style()
        style.configure("Accent.TButton", foreground="white", background="#3498db")
        
        styled_row = ttk.Frame(styled_buttons_frame)
        styled_row.pack(fill=tk.X)
        
        ttk.Button(styled_row, text="Акцентная кнопка", style="Accent.TButton", 
                  command=lambda: self.styled_button_clicked("акцентная")).pack(side=tk.LEFT, padx=5)
        ttk.Button(styled_row, text="Обычная кнопка", 
                  command=lambda: self.styled_button_clicked("обычная")).pack(side=tk.LEFT, padx=5)
        
        # Checkbuttons (флажки)
        check_frame = ttk.LabelFrame(button_frame, text="Флажки (Checkbuttons)")
        check_frame.pack(fill=tk.X, pady=10)
        
        self.check_vars = {}
        checks = ["Опция 1", "Опция 2", "Опция 3", "Опция 4"]
        
        for i, option in enumerate(checks):
            var = tk.BooleanVar()
            self.check_vars[option] = var
            ttk.Checkbutton(check_frame, text=option, variable=var, 
                           command=lambda opt=option: self.check_changed(opt)).pack(anchor=tk.W)
        
        # Radiobuttons (переключатели)
        radio_frame = ttk.LabelFrame(button_frame, text="Переключатели (Radiobuttons)")
        radio_frame.pack(fill=tk.X, pady=10)
        
        self.radio_var = tk.StringVar(value="option1")
        options = ["Вариант 1", "Вариант 2", "Вариант 3", "Вариант 4"]
        
        for option in options:
            ttk.Radiobutton(radio_frame, text=option, variable=self.radio_var, 
                           value=option, command=self.radio_changed).pack(anchor=tk.W)
        
        # Scale (шкала)
        scale_frame = ttk.Frame(button_frame)
        scale_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(scale_frame, text="Scale (шкала):").pack(anchor=tk.W)
        
        self.scale_var = tk.DoubleVar()
        scale = ttk.Scale(scale_frame, from_=0, to=100, variable=self.scale_var, 
                         orient=tk.HORIZONTAL, command=self.scale_changed)
        scale.pack(fill=tk.X, pady=5)
        
        self.scale_label = ttk.Label(scale_frame, text="Значение: 0.0")
        self.scale_label.pack()
        
        # Кнопка для получения состояния всех переключателей
        ttk.Button(button_frame, text="Получить состояние", command=self.get_state).pack(pady=10)
        
        # Метка для отображения состояния
        self.state_label = ttk.Label(button_frame, text="Состояние будет отображено здесь", foreground="green")
        self.state_label.pack(pady=5)
    
    def button_clicked(self, button_num):
        """Обработчик нажатия обычной кнопки"""
        print(f"Нажата кнопка {button_num}")
    
    def styled_button_clicked(self, button_type):
        """Обработчик нажатия стилизованной кнопки"""
        print(f"Нажата {button_type} кнопка")
    
    def check_changed(self, option):
        """Обработчик изменения флажка"""
        state = "отмечен" if self.check_vars[option].get() else "не отмечен"
        print(f"Флажок '{option}' {state}")
    
    def radio_changed(self):
        """Обработчик изменения переключателя"""
        selected = self.radio_var.get()
        print(f"Выбран вариант: {selected}")
    
    def scale_changed(self, value):
        """Обработчик изменения шкалы"""
        self.scale_label.config(text=f"Значение: {float(value):.1f}")
    
    def get_state(self):
        """Получает состояние всех переключателей"""
        check_states = {opt: var.get() for opt, var in self.check_vars.items()}
        radio_state = self.radio_var.get()
        scale_value = self.scale_var.get()
        
        state_text = f"Флажки: {check_states}\nПереключатель: {radio_state}\nШкала: {scale_value:.1f}"
        self.state_label.config(text=state_text)
    
    def run(self):
        self.root.mainloop()

# Задание 3: Отображение информации
class InfoDisplayApp:
    """Приложение для отображения информации"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Задание 3: Отображение информации")
        self.root.geometry("800x600")
        
        # Создаем фрейм для элементов отображения
        display_frame = ttk.LabelFrame(self.root, text="Элементы отображения информации")
        display_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Label (обычная метка)
        label_frame = ttk.Frame(display_frame)
        label_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(label_frame, text="Label (обычная метка):", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        self.label_widget = ttk.Label(label_frame, text="Это простая текстовая метка", 
                                     foreground="blue", background="lightgray", padding=5)
        self.label_widget.pack(fill=tk.X, pady=2)
        
        # Label с изображением
        image_frame = ttk.Frame(display_frame)
        image_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(image_frame, text="Label с изображением:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        
        # Создаем простое изображение с помощью Canvas
        self.image_canvas = tk.Canvas(image_frame, width=200, height=100, bg="white")
        self.image_canvas.pack(pady=5)
        
        # Рисуем простую фигуру на Canvas как "изображение"
        self.image_canvas.create_rectangle(50, 25, 150, 75, fill="lightblue", outline="black", width=2)
        self.image_canvas.create_text(100, 50, text="Изображение", font=("Arial", 12))
        
        # Message (многострочный текст)
        message_frame = ttk.Frame(display_frame)
        message_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(message_frame, text="Message (многострочный текст):", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        
        long_text = ("Это пример многострочного текста, который может быть достаточно длинным "
                    "и должен автоматически переноситься на новую строку при достижении "
                    "границы виджета. Виджет Message идеально подходит для отображения "
                    "такого рода информации.")
        
        self.message_widget = tk.Message(message_frame, text=long_text, width=400, 
                                        relief=tk.SUNKEN, padx=10, pady=10)
        self.message_widget.pack(fill=tk.X, pady=5)
        
        # Canvas (графика)
        canvas_frame = ttk.LabelFrame(display_frame, text="Canvas (графика)")
        canvas_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.canvas_widget = tk.Canvas(canvas_frame, bg="white", width=750, height=200)
        self.canvas_widget.pack(pady=5)
        
        # Рисуем примеры фигур на Canvas
        self.canvas_widget.create_line(50, 150, 50, fill="red", width=3)
        self.canvas_widget.create_oval(200, 25, 300, 75, fill="green", outline="black")
        self.canvas_widget.create_rectangle(350, 25, 450, 75, fill="blue", outline="black")
        self.canvas_widget.create_polygon(500, 75, 550, 25, 600, 75, fill="purple", outline="black")
        self.canvas_widget.create_text(400, 125, text="Пример текста на Canvas", font=("Arial", 14))
        
        # Кнопка для обновления Canvas
        ttk.Button(display_frame, text="Обновить Canvas", command=self.update_canvas).pack(pady=5)
    
    def update_canvas(self):
        """Обновляет содержимое Canvas"""
        self.canvas_widget.delete("all")  # Очищаем Canvas
        
        # Рисуем новые фигуры
        import random
        colors = ["red", "green", "blue", "purple", "orange", "yellow"]
        
        for i in range(5):
            x = random.randint(50, 700)
            y = random.randint(50, 150)
            size = random.randint(20, 50)
            color = random.choice(colors)
            
            self.canvas_widget.create_rectangle(x-size, y-size, x+size, y+size, 
                                              fill=color, outline="black")
    
    def run(self):
        self.root.mainloop()

# Задание 4: Навигационные элементы
class NavigationElementsApp:
    """Приложение с навигационными элементами"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Задание 4: Навигационные элементы")
        self.root.geometry("900x700")
        
        # Создаем меню
        self.create_menu()
        
        # Создаем тулбар
        self.create_toolbar()
        
        # Создаем основной фрейм
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Notebook (вкладки)
        notebook_frame = ttk.LabelFrame(main_frame, text="Notebook (вкладки)")
        notebook_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.notebook = ttk.Notebook(notebook_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Создаем вкладки
        self.create_notebook_tabs()
        
        # PanedWindow (разделитель области)
        paned_frame = ttk.LabelFrame(main_frame, text="PanedWindow (разделитель области)")
        paned_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        self.paned_window = ttk.PanedWindow(paned_frame, orient=tk.HORIZONTAL)
        self.paned_window.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Левая панель
        left_panel = ttk.Frame(self.paned_window)
        self.paned_window.add(left_panel, weight=1)
        
        ttk.Label(left_panel, text="Левая панель").pack(pady=20)
        ttk.Button(left_panel, text="Левая кнопка", command=lambda: self.log_action("Левая кнопка")).pack(pady=10)
        
        # Правая панель
        right_panel = ttk.Frame(self.paned_window)
        self.paned_window.add(right_panel, weight=2)
        
        ttk.Label(right_panel, text="Правая панель").pack(pady=20)
        ttk.Button(right_panel, text="Правая кнопка", command=lambda: self.log_action("Правая кнопка")).pack(pady=10)
        
        # Лог действий
        self.action_log = tk.Text(main_frame, height=6, state=tk.DISABLED)
        self.action_log.pack(fill=tk.X, pady=5)
    
    def create_menu(self):
        """Создает меню приложения"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Меню File
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Новый", command=lambda: self.log_action("Menu: Новый"))
        file_menu.add_command(label="Открыть", command=lambda: self.log_action("Menu: Открыть"))
        file_menu.add_command(label="Сохранить", command=lambda: self.log_action("Menu: Сохранить"))
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        
        # Меню Edit
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Правка", menu=edit_menu)
        edit_menu.add_command(label="Копировать", command=lambda: self.log_action("Menu: Копировать"))
        edit_menu.add_command(label="Вставить", command=lambda: self.log_action("Menu: Вставить"))
        edit_menu.add_command(label="Удалить", command=lambda: self.log_action("Menu: Удалить"))
        
        # Меню Help
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.show_about)
    
    def create_toolbar(self):
        """Создает тулбар"""
        toolbar = ttk.Frame(self.root, relief=tk.RAISED, borderwidth=1)
        toolbar.pack(fill=tk.X, padx=10, pady=2)
        
        ttk.Button(toolbar, text="Новый", command=lambda: self.log_action("Toolbar: Новый")).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Открыть", command=lambda: self.log_action("Toolbar: Открыть")).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Сохранить", command=lambda: self.log_action("Toolbar: Сохранить")).pack(side=tk.LEFT, padx=2)
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        ttk.Button(toolbar, text="Копировать", command=lambda: self.log_action("Toolbar: Копировать")).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Вставить", command=lambda: self.log_action("Toolbar: Вставить")).pack(side=tk.LEFT, padx=2)
    
    def create_notebook_tabs(self):
        """Создает вкладки для Notebook"""
        # Вкладка 1
        tab1 = ttk.Frame(self.notebook)
        self.notebook.add(tab1, text="Вкладка 1")
        
        ttk.Label(tab1, text="Содержимое первой вкладки").pack(pady=20)
        ttk.Button(tab1, text="Кнопка вкладки 1", command=lambda: self.log_action("Вкладка 1")).pack(pady=10)
        
        # Вкладка 2
        tab2 = ttk.Frame(self.notebook)
        self.notebook.add(tab2, text="Вкладка 2")
        
        ttk.Label(tab2, text="Содержимое второй вкладки").pack(pady=20)
        ttk.Button(tab2, text="Кнопка вкладки 2", command=lambda: self.log_action("Вкладка 2")).pack(pady=10)
        
        # Вкладка 3
        tab3 = ttk.Frame(self.notebook)
        self.notebook.add(tab3, text="Вкладка 3")
        
        ttk.Label(tab3, text="Содержимое третьей вкладки").pack(pady=20)
        ttk.Button(tab3, text="Кнопка вкладки 3", command=lambda: self.log_action("Вкладка 3")).pack(pady=10)
    
    def log_action(self, action):
        """Логирует действие"""
        self.action_log.config(state=tk.NORMAL)
        self.action_log.insert(tk.END, f"{time.strftime('%H:%M:%S')} - {action}\n")
        self.action_log.see(tk.END)
        self.action_log.config(state=tk.DISABLED)
    
    def show_about(self):
        """Показывает окно 'О программе'"""
        messagebox.showinfo("О программе", "Приложение для демонстрации навигационных элементов")
    
    def run(self):
        self.root.mainloop()

# Задание 5: Комплексное приложение "Форма регистрации"
class RegistrationFormApp:
    """Комплексное приложение - форма регистрации"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Комплексное приложение: Форма регистрации")
        self.root.geometry("600x800")
        
        # Основной фрейм
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="Форма регистрации", font=("Arial", 18, "bold"))
        title_label.pack(pady=20)
        
        # Фрейм для формы
        form_frame = ttk.LabelFrame(main_frame, text="Информация пользователя")
        form_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Имя
        name_frame = ttk.Frame(form_frame)
        name_frame.pack(fill=tk.X, pady=5)
        ttk.Label(name_frame, text="Имя:*", width=15).pack(side=tk.LEFT)
        self.first_name_var = tk.StringVar()
        self.first_name_entry = ttk.Entry(name_frame, textvariable=self.first_name_var)
        self.first_name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Фамилия
        surname_frame = ttk.Frame(form_frame)
        surname_frame.pack(fill=tk.X, pady=5)
        ttk.Label(surname_frame, text="Фамилия:*", width=15).pack(side=tk.LEFT)
        self.last_name_var = tk.StringVar()
        self.last_name_entry = ttk.Entry(surname_frame, textvariable=self.last_name_var)
        self.last_name_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Email
        email_frame = ttk.Frame(form_frame)
        email_frame.pack(fill=tk.X, pady=5)
        ttk.Label(email_frame, text="Email:*", width=15).pack(side=tk.LEFT)
        self.email_var = tk.StringVar()
        self.email_entry = ttk.Entry(email_frame, textvariable=self.email_var)
        self.email_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Пароль
        password_frame = ttk.Frame(form_frame)
        password_frame.pack(fill=tk.X, pady=5)
        ttk.Label(password_frame, text="Пароль:*", width=15).pack(side=tk.LEFT)
        self.password_var = tk.StringVar()
        self.password_entry = ttk.Entry(password_frame, textvariable=self.password_var, show="*")
        self.password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Подтверждение пароля
        confirm_password_frame = ttk.Frame(form_frame)
        confirm_password_frame.pack(fill=tk.X, pady=5)
        ttk.Label(confirm_password_frame, text="Подтверждение:*", width=15).pack(side=tk.LEFT)
        self.confirm_password_var = tk.StringVar()
        self.confirm_password_entry = ttk.Entry(confirm_password_frame, textvariable=self.confirm_password_var, show="*")
        self.confirm_password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Дата рождения
        dob_frame = ttk.Frame(form_frame)
        dob_frame.pack(fill=tk.X, pady=5)
        ttk.Label(dob_frame, text="Дата рождения:", width=15).pack(side=tk.LEFT)
        self.dob_day = tk.StringVar(value="День")
        self.dob_month = tk.StringVar(value="Месяц")
        self.dob_year = tk.StringVar(value="Год")
        
        day_combo = ttk.Combobox(dob_frame, textvariable=self.dob_day, values=[str(i) for i in range(1, 32)], width=5)
        day_combo.pack(side=tk.LEFT, padx=5)
        
        month_combo = ttk.Combobox(dob_frame, textvariable=self.dob_month, values=[
            "Янв", "Фев", "Мар", "Апр", "Май", "Июн",
            "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"
        ], width=7)
        month_combo.pack(side=tk.LEFT, padx=5)
        
        year_combo = ttk.Combobox(dob_frame, textvariable=self.dob_year, values=[str(i) for i in range(1950, 2025)], width=7)
        year_combo.pack(side=tk.LEFT, padx=5)
        
        # Пол
        gender_frame = ttk.Frame(form_frame)
        gender_frame.pack(fill=tk.X, pady=5)
        ttk.Label(gender_frame, text="Пол:", width=15).pack(side=tk.LEFT)
        
        self.gender_var = tk.StringVar(value="Не указан")
        ttk.Radiobutton(gender_frame, text="Мужской", variable=self.gender_var, value="Мужской").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(gender_frame, text="Женский", variable=self.gender_var, value="Женский").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(gender_frame, text="Другой", variable=self.gender_var, value="Другой").pack(side=tk.LEFT, padx=10)
        
        # Интересы
        interests_frame = ttk.LabelFrame(form_frame, text="Интересы")
        interests_frame.pack(fill=tk.X, pady=10)
        
        self.interest_vars = {}
        interests = ["Программирование", "Дизайн", "Маркетинг", "Менеджмент", "Аналитика"]
        
        for i, interest in enumerate(interests):
            var = tk.BooleanVar()
            self.interest_vars[interest] = var
            col = i % 3  # Распределяем по 3 колонки
            row = i // 3
            ttk.Checkbutton(interests_frame, text=interest, variable=var).grid(
                row=row, column=col, sticky=tk.W, padx=10, pady=2)
        
        # Соглашение
        agreement_frame = ttk.Frame(form_frame)
        agreement_frame.pack(fill=tk.X, pady=10)
        
        self.agreement_var = tk.BooleanVar()
        agreement_check = ttk.Checkbutton(agreement_frame, text="Я согласен с условиями использования", 
                                         variable=self.agreement_var)
        agreement_check.pack(anchor=tk.W)
        
        # Кнопки
        button_frame = ttk.Frame(form_frame)
        button_frame.pack(fill=tk.X, pady=20)
        
        ttk.Button(button_frame, text="Очистить", command=self.clear_form).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Зарегистрироваться", command=self.register).pack(side=tk.RIGHT, padx=5)
        
        # Лог действий
        self.log_text = tk.Text(main_frame, height=8, state=tk.DISABLED)
        self.log_text.pack(fill=tk.X, pady=10)
    
    def validate_form(self) -> bool:
        """Валидация формы регистрации"""
        errors = []
        
        # Проверка обязательных полей
        if not self.first_name_var.get().strip():
            errors.append("Имя обязательно для заполнения")
        
        if not self.last_name_var.get().strip():
            errors.append("Фамилия обязательна для заполнения")
        
        if not self.email_var.get().strip():
            errors.append("Email обязателен для заполнения")
        elif "@" not in self.email_var.get() or "." not in self.email_var.get():
            errors.append("Некорректный формат email")
        
        if not self.password_var.get():
            errors.append("Пароль обязателен для заполнения")
        elif len(self.password_var.get()) < 6:
            errors.append("Пароль должен быть не менее 6 символов")
        
        if self.password_var.get() != self.confirm_password_var.get():
            errors.append("Пароли не совпадают")
        
        if not self.agreement_var.get():
            errors.append("Необходимо согласие с условиями использования")
        
        if errors:
            messagebox.showerror("Ошибки валидации", "\n".join(errors))
            return False
        
        return True
    
    def register(self):
        """Обработка регистрации"""
        if self.validate_form():
            # Собираем данные формы
            user_data = {
                'first_name': self.first_name_var.get(),
                'last_name': self.last_name_var.get(),
                'email': self.email_var.get(),
                'password': '*' * len(self.password_var.get()),  # Не показываем пароль
                'dob': f"{self.dob_day.get()} {self.dob_month.get()} {self.dob_year.get()}",
                'gender': self.gender_var.get(),
                'interests': [interest for interest, var in self.interest_vars.items() if var.get()],
                'agreed_to_terms': self.agreement_var.get()
            }
            
            # Логируем успешную регистрацию
            self.log_action(f"Успешная регистрация: {user_data['first_name']} {user_data['last_name']}")
            messagebox.showinfo("Успех", "Регистрация прошла успешно!")
            
            # Очищаем форму
            self.clear_form()
        else:
            self.log_action("Попытка регистрации с ошибками валидации")
    
    def clear_form(self):
        """Очистка формы"""
        self.first_name_var.set("")
        self.last_name_var.set("")
        self.email_var.set("")
        self.password_var.set("")
        self.confirm_password_var.set("")
        
        self.dob_day.set("День")
        self.dob_month.set("Месяц")
        self.dob_year.set("Год")
        
        self.gender_var.set("Не указан")
        
        for var in self.interest_vars.values():
            var.set(False)
        
        self.agreement_var.set(False)
    
    def log_action(self, action):
        """Логирование действий"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, f"{time.strftime('%H:%M:%S')} - {action}\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def run(self):
        self.root.mainloop()

# Дополнительные примеры использования виджетов
class AdvancedWidgetExamples:
    """Дополнительные примеры продвинутого использования виджетов"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Дополнительные примеры виджетов")
        self.root.geometry("900x800")
        
        # Создаем ноутбук для различных примеров
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Вкладка для продвинутых Entry
        self.entry_examples_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.entry_examples_frame, text="Продвинутые Entry")
        self.create_advanced_entry_examples()
        
        # Вкладка для Treeview
        self.treeview_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.treeview_frame, text="Treeview")
        self.create_treeview_example()
        
        # Вкладка для Progressbar
        self.progress_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.progress_frame, text="Прогресс бары")
        self.create_progress_examples()
    
    def create_advanced_entry_examples(self):
        """Создает примеры продвинутого использования Entry"""
        frame = ttk.LabelFrame(self.entry_examples_frame, text="Продвинутые возможности Entry")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Entry с плейсхолдером
        placeholder_frame = ttk.Frame(frame)
        placeholder_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(placeholder_frame, text="Entry с плейсхолдером:").pack(anchor=tk.W)
        self.placeholder_entry = PlaceholderEntry(placeholder_frame, placeholder="Введите текст здесь...")
        self.placeholder_entry.pack(fill=tk.X, pady=5)
        
        # Entry с валидацией
        validation_frame = ttk.Frame(frame)
        validation_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(validation_frame, text="Entry с валидацией (только цифры):").pack(anchor=tk.W)
        vcmd = (self.root.register(self.validate_numeric), '%P')
        self.numeric_entry = ttk.Entry(validation_frame, validate='key', validatecommand=vcmd)
        self.numeric_entry.pack(fill=tk.X, pady=5)
        
        # Entry с маской (например, для телефона)
        mask_frame = ttk.Frame(frame)
        mask_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(mask_frame, text="Entry с маской (телефон):").pack(anchor=tk.W)
        self.phone_entry = MaskedEntry(mask_frame, mask='+7 (XXX) XXX-XX-XX')
        self.phone_entry.pack(fill=tk.X, pady=5)
        
        # Кнопка для демонстрации получения значений
        ttk.Button(frame, text="Получить значения", command=self.get_advanced_values).pack(pady=10)
        
        self.advanced_values_label = ttk.Label(frame, text="Значения будут здесь", foreground="blue")
        self.advanced_values_label.pack(pady=5)
    
    def validate_numeric(self, value):
        """Валидация ввода - только цифры"""
        if value == "":
            return True
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    def get_advanced_values(self):
        """Получение значений из продвинутых Entry"""
        placeholder_value = self.placeholder_entry.get()
        numeric_value = self.numeric_entry.get()
        phone_value = self.phone_entry.get()
        
        values_text = f"Placeholder: '{placeholder_value}'\nNumeric: '{numeric_value}'\nPhone: '{phone_value}'"
        self.advanced_values_label.config(text=values_text)
    
    def create_treeview_example(self):
        """Создает пример использования Treeview"""
        frame = ttk.LabelFrame(self.treeview_frame, text="Пример Treeview (таблица/дерево)")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Создаем Treeview с прокруткой
        tree_scrollbar = ttk.Scrollbar(frame)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.treeview = ttk.Treeview(frame, yscrollcommand=tree_scrollbar.set)
        self.treeview.pack(fill=tk.BOTH, expand=True)
        
        tree_scrollbar.config(command=self.treeview.yview)
        
        # Определяем колонки
        self.treeview['columns'] = ("Имя", "Возраст", "Должность", "Зарплата")
        
        # Форматируем колонки
        self.treeview.column("#0", width=0, stretch=tk.NO)  # Скрытая колонка
        self.treeview.column("Имя", anchor=tk.W, width=120)
        self.treeview.column("Возраст", anchor=tk.CENTER, width=80)
        self.treeview.column("Должность", anchor=tk.W, width=150)
        self.treeview.column("Зарплата", anchor=tk.E, width=100)
        
        # Создаем заголовки
        self.treeview.heading("#0", text="", anchor=tk.W)
        self.treeview.heading("Имя", text="Имя", anchor=tk.W)
        self.treeview.heading("Возраст", text="Возраст", anchor=tk.W)
        self.treeview.heading("Должность", text="Должность", anchor=tk.W)
        self.treeview.heading("Зарплата", text="Зарплата", anchor=tk.W)
        
        # Добавляем данные
        employees = [
            ("Иванов Иван", 30, "Разработчик", 120000),
            ("Петрова Мария", 28, "Дизайнер", 90000),
            ("Сидоров Алексей", 35, "Менеджер", 150000),
            ("Козлова Елена", 26, "Аналитик", 100000),
            ("Морозов Дмитрий", 32, "Тестировщик", 85000)
        ]
        
        for emp in employees:
            self.treeview.insert(parent='', index='end', values=emp)
        
        # Кнопки управления
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Добавить", command=self.add_employee).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Удалить", command=self.remove_employee).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Выбрать", command=self.select_employee).pack(side=tk.LEFT, padx=5)
    
    def add_employee(self):
        """Добавляет сотрудника в Treeview"""
        # В реальном приложении здесь был бы диалог добавления
        new_emp = (f"Новый Сотрудник {len(self.treeview.get_children())+1}", 25, "Стажер", 50000)
        self.treeview.insert(parent='', index='end', values=new_emp)
    
    def remove_employee(self):
        """Удаляет выбранного сотрудника из Treeview"""
        selected = self.treeview.selection()
        if selected:
            self.treeview.delete(selected)
    
    def select_employee(self):
        """Обрабатывает выбор сотрудника"""
        selected = self.treeview.selection()
        if selected:
            item = self.treeview.item(selected)
            values = item['values']
            messagebox.showinfo("Выбранный сотрудник", f"Имя: {values[0]}, Возраст: {values[1]}")
    
    def create_progress_examples(self):
        """Создает примеры использования Progressbar"""
        frame = ttk.LabelFrame(self.progress_frame, text="Примеры Progressbar")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Determinate progress bar
        det_frame = ttk.Frame(frame)
        det_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(det_frame, text="Определенный прогресс бар:").pack(anchor=tk.W)
        self.determinate_pb = ttk.Progressbar(det_frame, mode='determinate', maximum=100)
        self.determinate_pb.pack(fill=tk.X, pady=5)
        
        # Кнопка для запуска анимации
        ttk.Button(det_frame, text="Запустить анимацию", command=self.animate_progress).pack(pady=5)
        
        # Indeterminate progress bar
        indet_frame = ttk.Frame(frame)
        indet_frame.pack(fill=tk.X, pady=10)
        
        ttk.Label(indet_frame, text="Неопределенный прогресс бар:").pack(anchor=tk.W)
        self.indeterminate_pb = ttk.Progressbar(indet_frame, mode='indeterminate')
        self.indeterminate_pb.pack(fill=tk.X, pady=5)
        
        # Кнопки управления
        control_frame = ttk.Frame(indet_frame)
        control_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(control_frame, text="Старт", command=self.start_indeterminate).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Стоп", command=self.stop_indeterminate).pack(side=tk.LEFT, padx=5)
    
    def animate_progress(self):
        """Анимирует определенный прогресс бар"""
        def animate():
            for i in range(101):
                self.determinate_pb['value'] = i
                self.root.update()
                time.sleep(0.02)
            self.determinate_pb['value'] = 0  # Сброс после анимации
        
        # Запускаем анимацию в отдельном потоке
        animation_thread = threading.Thread(target=animate)
        animation_thread.daemon = True
        animation_thread.start()
    
    def start_indeterminate(self):
        """Запускает неопределенный прогресс бар"""
        self.indeterminate_pb.start(10)  # Обновление каждые 10мс
    
    def stop_indeterminate(self):
        """Останавливает неопределенный прогресс бар"""
        self.indeterminate_pb.stop()
    
    def run(self):
        self.root.mainloop()

# Вспомогательные классы для продвинутых виджетов
class PlaceholderEntry(tk.Entry):
    """Entry с плейсхолдером"""
    def __init__(self, master, placeholder="", color='grey'):
        super().__init__(master)
        
        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']
        
        self.insert(0, self.placeholder)
        self.config(fg=self.placeholder_color)
        
        self.bind('<FocusIn>', self.focus_in)
        self.bind('<FocusOut>', self.focus_out)
    
    def focus_in(self, *args):
        if self.get() == self.placeholder and self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self.config(fg=self.default_fg_color)
    
    def focus_out(self, *args):
        if not self.get():
            self.insert(0, self.placeholder)
            self.config(fg=self.placeholder_color)
    
    def get(self):
        content = super().get()
        if content == self.placeholder and self['fg'] == self.placeholder_color:
            return ''
        return content

class MaskedEntry(tk.Entry):
    """Entry с маской ввода"""
    def __init__(self, master, mask=""):
        super().__init__(master)
        self.mask = mask
        self.mask_char = 'X'
        
        self.bind('<KeyRelease>', self.on_key_release)
    
    def on_key_release(self, event):
        if event.keysym not in ['BackSpace', 'Delete', 'Left', 'Right', 'Up', 'Down', 'Tab']:
            current_text = self.get()
            masked_text = self.apply_mask(current_text)
            cursor_pos = self.index(tk.INSERT)
            
            self.delete(0, tk.END)
            self.insert(0, masked_text)
            self.icursor(cursor_pos)
    
    def apply_mask(self, text):
        result = ""
        text_index = 0
        
        for mask_char in self.mask:
            if mask_char == self.mask_char and text_index < len(text):
                result += text[text_index]
                text_index += 1
            else:
                result += mask_char
        
        return result

# Примеры использования:
if __name__ == "__main__":
    print("=== Упражнения для практического занятия 18 ===")
    
    print("\n1. Задание 1: Основные виджеты ввода")
    # input_app = InputWidgetsApp()
    # input_app.run()  # Закомментировано для предотвращения автоматического запуска
    
    print("\n2. Задание 2: Кнопки и переключатели")
    # button_app = ButtonToggleApp()
    # button_app.run()  # Закомментировано
    
    print("\n3. Задание 3: Отображение информации")
    # info_app = InfoDisplayApp()
    # info_app.run()  # Закомментировано
    
    print("\n4. Задание 4: Навигационные элементы")
    # nav_app = NavigationElementsApp()
    # nav_app.run()  # Закомментировано
    
    print("\n5. Задание 5: Комплексное приложение (Форма регистрации)")
    # reg_app = RegistrationFormApp()
    # reg_app.run()  # Закомментировано
    
    print("\n6. Дополнительные примеры")
    # advanced_app = AdvancedWidgetExamples()
    # advanced_app.run()  # Закомментировано
    
    # Для демонстрации запустим только одно приложение
    print("Для запуска приложений раскомментируйте соответствующие строки в коде")