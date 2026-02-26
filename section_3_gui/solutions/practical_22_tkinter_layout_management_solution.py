#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Практическое занятие 22: Tkinter - управление макетом
Решение задач по менеджерам геометрии (pack, grid, place)

Автор: AI Assistant
"""

import tkinter as tk
from tkinter import ttk, messagebox
import math
import ast
import operator


# ==============================================================================
# ЗАДАЧА 1: Менеджер pack - Вертикальный и горизонтальный макеты
# ==============================================================================

class PackManagerDemo:
    """Демонстрация менеджера pack"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Задача 1: Pack Manager")
        self.root.geometry("400x500")
        
        self.create_vertical_layout()
        self.create_horizontal_toolbar()
    
    def create_vertical_layout(self):
        """Создание вертикального макета с кнопками"""
        # Основной контейнер
        main_frame = ttk.Frame(self.root)
        main_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Заголовок
        title_label = ttk.Label(
            main_frame, 
            text="Вертикальный макет (pack)", 
            font=("Arial", 14, "bold")
        )
        title_label.pack(side=tk.TOP, pady=(0, 10))
        
        # Фрейм для вертикальных кнопок
        button_frame = ttk.Frame(main_frame, relief=tk.RIDGE, borderwidth=2)
        button_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Кнопки с разными параметрами pack
        buttons_config = [
            ("Кнопка 1 (TOP + FILL=X)", {"side": tk.TOP, "fill": tk.X, "padx": 5, "pady": 5}),
            ("Кнопка 2 (TOP + FILL=BOTH + EXPAND)", {"side": tk.TOP, "fill": tk.BOTH, "expand": True, "padx": 5, "pady": 5}),
            ("Кнопка 3 (TOP + FILL=X)", {"side": tk.TOP, "fill": tk.X, "padx": 5, "pady": 5}),
            ("Кнопка 4 (BOTTOM + FILL=X)", {"side": tk.BOTTOM, "fill": tk.X, "padx": 5, "pady": 5}),
        ]
        
        for text, params in buttons_config:
            btn = ttk.Button(button_frame, text=text)
            btn.pack(**params)
        
        # Фрейм с разными направлениями заполнения
        fill_demo_frame = ttk.LabelFrame(main_frame, text="Разные направления заполнения", padding=10)
        fill_demo_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, pady=10)
        
        # LEFT заполнение
        left_frame = ttk.Frame(fill_demo_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        ttk.Label(left_frame, text="LEFT").pack()
        ttk.Button(left_frame, text="Кнопка 1").pack(side=tk.LEFT, padx=2)
        ttk.Button(left_frame, text="Кнопка 2").pack(side=tk.LEFT, padx=2)
        
        # RIGHT заполнение
        right_frame = ttk.Frame(fill_demo_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        ttk.Label(right_frame, text="RIGHT").pack()
        ttk.Button(right_frame, text="Кнопка 1").pack(side=tk.RIGHT, padx=2)
        ttk.Button(right_frame, text="Кнопка 2").pack(side=tk.RIGHT, padx=2)
    
    def create_horizontal_toolbar(self):
        """Создание горизонтальной панели инструментов"""
        toolbar = ttk.Frame(self.root, relief=tk.RAISED, borderwidth=1)
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Горизонтальный макет для тулбара
        ttk.Button(toolbar, text="Новый").pack(side=tk.LEFT, padx=2, pady=2)
        ttk.Button(toolbar, text="Открыть").pack(side=tk.LEFT, padx=2, pady=2)
        ttk.Button(toolbar, text="Сохранить").pack(side=tk.LEFT, padx=2, pady=2)
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=2)
        
        ttk.Button(toolbar, text="Копировать").pack(side=tk.LEFT, padx=2, pady=2)
        ttk.Button(toolbar, text="Вставить").pack(side=tk.LEFT, padx=2, pady=2)
        
        # Растягивающаяся метка для разделения
        ttk.Label(toolbar, text="").pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        ttk.Button(toolbar, text="Выход", command=self.root.quit).pack(side=tk.LEFT, padx=2, pady=2)


# ==============================================================================
# ЗАДАЧА 2: Менеджер grid - Калькулятор и форма ввода
# ==============================================================================

class CalculatorApp:
    """Калькулятор с использованием grid"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Задача 2: Grid Manager - Калькулятор")
        self.root.geometry("300x400")
        self.root.resizable(False, False)
        
        self.expression = ""
        self.create_calculator()
    
    def create_calculator(self):
        """Создание калькулятора"""
        # Поле ввода (дисплей)
        self.display = ttk.Entry(self.root, font=("Arial", 24), justify="right")
        self.display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)
        
        # Настройка весов для адаптивности
        for i in range(4):
            self.root.columnconfigure(i, weight=1)
        for i in range(1, 6):
            self.root.rowconfigure(i, weight=1)
        
        # Кнопки калькулятора
        buttons = [
            ("C", 1, 0), ("(", 1, 1), (")", 1, 2), ("/", 1, 3),
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("*", 2, 3),
            ("4", 3, 0), ("5", 3, 1), ("6", 3, 2), ("-", 3, 3),
            ("1", 4, 0), ("2", 4, 1), ("3", 4, 2), ("+", 4, 3),
            ("0", 5, 0, 2), (".", 5, 2), ("=", 5, 3),
        ]
        
        for btn in buttons:
            text = btn[0]
            row = btn[1]
            col = btn[2]
            colspan = btn[3] if len(btn) > 3 else 1
            
            button = ttk.Button(
                self.root, 
                text=text,
                command=lambda t=text: self.on_button_click(t)
            )
            button.grid(row=row, column=col, columnspan=colspan, 
                       sticky="nsew", padx=2, pady=2)
    
    def on_button_click(self, text):
        """Обработка нажатия кнопки"""
        if text == "C":
            self.expression = ""
        elif text == "=":
            try:
                result = self.safe_eval(self.expression)
                self.expression = str(result)
            except Exception:
                self.expression = "Ошибка"
                return
        else:
            self.expression += text
        
        self.display.delete(0, tk.END)
        self.display.insert(tk.END, self.expression)

    def safe_eval(self, expr: str) -> float:
        """Безопасное вычисление математических выражений"""
        # Разрешённые символы: цифры, операторы, скобки, точка
        allowed = set("0123456789.+-*/() ")
        if not all(c in allowed for c in expr.strip()):
            raise ValueError("Недопустимые символы в выражении")
        
        # Безопасная реализация без использования eval()
        try:
            # Простая реализация калькулятора
            return self._evaluate_expression(expr.strip())
        except Exception as e:
            raise ValueError(f"Ошибка вычисления: {e}")
    
    def _evaluate_expression(self, expr: str) -> float:
        """Вспомогательный метод для безопасного вычисления"""
        # Упрощённая реализация: используем ast для безопасного парсинга
        operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.USub: operator.neg,
            ast.UAdd: operator.pos,
        }
        
        def eval_node(node):
            if isinstance(node, ast.Constant):  # Python 3.8+
                if isinstance(node.value, (int, float)):
                    return node.value
                raise ValueError("Недопустимое значение")
            elif isinstance(node, ast.Num):  # Python 3.7 и ранее
                return node.n
            elif isinstance(node, ast.BinOp):
                left = eval_node(node.left)
                right = eval_node(node.right)
                return operators[type(node.op)](left, right)
            elif isinstance(node, ast.UnaryOp):
                operand = eval_node(node.operand)
                return operators[type(node.op)](operand)
            elif isinstance(node, ast.Expression):
                return eval_node(node.body)
            else:
                raise ValueError("Недопустимая операция")
        
        tree = ast.parse(expr, mode='eval')
        return eval_node(tree.body)


class InputFormDemo:
    """Форма ввода данных с использованием grid"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Задача 2: Grid Manager - Форма ввода")
        self.root.geometry("400x300")
        
        self.create_form()
    
    def create_form(self):
        """Создание формы ввода"""
        # Основной контейнер с отступами
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Настройка весов колонок
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=2)
        
        # Заголовок
        title = ttk.Label(main_frame, text="Регистрация", font=("Arial", 16, "bold"))
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Поля формы
        fields = [
            ("Имя:", "Введите имя"),
            ("Фамилия:", "Введите фамилию"),
            ("Email:", "example@mail.ru"),
            ("Телефон:", "+7 (999) 000-00-00"),
        ]
        
        self.entries = {}
        
        for i, (label, placeholder) in enumerate(fields, start=1):
            lbl = ttk.Label(main_frame, text=label)
            lbl.grid(row=i, column=0, sticky=tk.W, pady=10, padx=(0, 10))
            
            entry = ttk.Entry(main_frame)
            entry.insert(0, placeholder)
            entry.grid(row=i, column=1, sticky=tk.EW, pady=10)
            
            self.entries[label] = entry
        
        # Кнопки
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=len(fields) + 1, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Отправить", command=self.submit_form).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Очистить", command=self.clear_form).pack(side=tk.LEFT, padx=5)
    
    def submit_form(self):
        """Обработка отправки формы"""
        data = {label: entry.get() for label, entry in self.entries.items()}
        messagebox.showinfo("Данные", f"Отправлено:\n{chr(10).join(f'{k}: {v}' for k, v in data.items())}")
    
    def clear_form(self):
        """Очистка формы"""
        for entry in self.entries.values():
            entry.delete(0, tk.END)


# ==============================================================================
# ЗАДАЧА 3: Менеджер place - Абсолютное позиционирование
# ==============================================================================

class PlaceManagerDemo:
    """Демонстрация менеджера place"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Задача 3: Place Manager")
        self.root.geometry("500x400")
        
        self.create_place_demo()
    
    def create_place_demo(self):
        """Создание демонстрации place"""
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        title = ttk.Label(
            main_frame, 
            text="Абсолютное и относительное позиционирование",
            font=("Arial", 12)
        )
        title.place(x=10, y=10)
        
        # Абсолютное позиционирование
        abs_frame = ttk.LabelFrame(main_frame, text="Абсолютное (x, y)", padding=10)
        abs_frame.place(x=20, y=50, width=200, height=150)
        
        for i in range(3):
            btn = ttk.Button(abs_frame, text=f"Кнопка {i+1}")
            btn.place(x=10 + i*60, y=10 + i*30)
        
        # Относительное позиционирование
        rel_frame = ttk.LabelFrame(main_frame, text="Относительное (relx, rely)", padding=10)
        rel_frame.place(relx=0.55, rely=0.15, relwidth=0.4, relheight=0.7)
        
        # Центрированная кнопка
        center_btn = ttk.Button(rel_frame, text="Центр (relx=0.5, rely=0.5)")
        center_btn.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Растянутая метка
        label = ttk.Label(rel_frame, text="Растянутая метка", background="#e0e0e0", anchor=tk.CENTER)
        label.place(relx=0, rely=0.1, relwidth=1.0, height=30)
        
        # Система позиционирования (сетка)
        overlay_frame = ttk.LabelFrame(main_frame, text="Оверлей на изображении", padding=5)
        overlay_frame.place(x=20, y=220, width=450, height=150)
        
        # Фоновое "изображение" (зеленый прямоугольник)
        bg_canvas = tk.Canvas(overlay_frame, width=430, height=120, bg="#90EE90")
        bg_canvas.pack()
        
        # Оверлей текст
        bg_canvas.create_text(215, 60, text="Оверлей текста", font=("Arial", 14), fill="white")
        
        # Кнопка поверх "изображения"
        overlay_btn = ttk.Button(overlay_frame, text="Нажми меня")
        overlay_btn.place(relx=0.5, rely=0.8, anchor=tk.CENTER)


# ==============================================================================
# ЗАДАЧА 4: Комбинирование менеджеров - Главное окно приложения
# ==============================================================================

class ComplexLayoutApp:
    """Сложный макет с комбинированием менеджеров"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Задача 4: Комбинирование менеджеров")
        self.root.geometry("800x600")
        
        self.create_menu()
        self.create_toolbar()
        self.create_main_layout()
        self.create_statusbar()
    
    def create_menu(self):
        """Создание меню"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Файл меню
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Новый", command=lambda: self.status("Новый файл"))
        file_menu.add_command(label="Открыть", command=lambda: self.status("Открыть файл"))
        file_menu.add_command(label="Сохранить", command=lambda: self.status("Сохранить файл"))
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        
        # Правка меню
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Правка", menu=edit_menu)
        edit_menu.add_command(label="Копировать", command=lambda: self.status("Копировать"))
        edit_menu.add_command(label="Вставить", command=lambda: self.status("Вставить"))
        
        # Вид меню
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Вид", menu=view_menu)
        view_menu.add_command(label="Панель инструментов", command=lambda: self.status("Панель инструментов"))
        view_menu.add_command(label="Строка статуса", command=lambda: self.status("Строка статуса"))
        
        # Справка меню
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.show_about)
    
    def create_toolbar(self):
        """Создание панели инструментов (pack)"""
        toolbar = ttk.Frame(self.root, relief=tk.RAISED, borderwidth=1)
        toolbar.pack(side=tk.TOP, fill=tk.X)
        
        # Используем pack для горизонтальной панели
        ttk.Button(toolbar, text="📁 Новый", command=lambda: self.status("Новый")).pack(side=tk.LEFT, padx=2, pady=2)
        ttk.Button(toolbar, text="📂 Открыть", command=lambda: self.status("Открыть")).pack(side=tk.LEFT, padx=2, pady=2)
        ttk.Button(toolbar, text="💾 Сохранить", command=lambda: self.status("Сохранить")).pack(side=tk.LEFT, padx=2, pady=2)
        
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        ttk.Button(toolbar, text="✂️ Копировать", command=lambda: self.status("Копировать")).pack(side=tk.LEFT, padx=2, pady=2)
        ttk.Button(toolbar, text="📋 Вставить", command=lambda: self.status("Вставить")).pack(side=tk.LEFT, padx=2, pady=2)
        
        # Растягивающийся спейсер
        ttk.Label(toolbar, text="").pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Поиск с использованием pack
        search_frame = ttk.Frame(toolbar)
        search_frame.pack(side=tk.RIGHT, padx=5)
        
        self.search_entry = ttk.Entry(search_frame, width=20)
        self.search_entry.pack(side=tk.LEFT, padx=2)
        ttk.Button(search_frame, text="🔍").pack(side=tk.LEFT, padx=2)
    
    def create_main_layout(self):
        """Создание основного макета с использованием pack и grid"""
        # Основной контейнер - используем pack
        main_container = ttk.Frame(self.root)
        main_container.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Боковая панель (sidebar) - pack слева
        sidebar = ttk.Frame(main_container, width=200, relief=tk.RAISED, borderwidth=1)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)  # Сохраняем ширину
        
        # Содержимое боковой панели
        ttk.Label(sidebar, text="Навигация", font=("Arial", 12, "bold")).pack(pady=10)
        
        nav_buttons = ["Главная", "Проекты", "Задачи", "Контакты"]
        for btn_text in nav_buttons:
            ttk.Button(sidebar, text=f"  {btn_text}").pack(fill=tk.X, padx=5, pady=2)
        
        # Основная область - используем pack и grid
        content_area = ttk.Frame(main_container)
        content_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Панель с вкладками (grid)
        tabs_frame = ttk.Frame(content_area)
        tabs_frame.pack(side=tk.TOP, fill=tk.X)
        
        self.tabs = {}
        tab_names = ["Документ 1", "Документ 2", "Документ 3"]
        
        for i, name in enumerate(tab_names):
            btn = ttk.Button(
                tabs_frame, 
                text=name,
                command=lambda n=name: self.open_tab(n)
            )
            btn.grid(row=0, column=i, padx=2, pady=2)
        
        # Область содержимого с grid
        content_frame = ttk.LabelFrame(content_area, text="Содержимое", padding=10)
        content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Сетка с формой
        content_frame.columnconfigure(0, weight=1)
        content_frame.columnconfigure(1, weight=2)
        
        ttk.Label(content_frame, text="Заголовок:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(content_frame).grid(row=0, column=1, sticky=tk.EW, pady=5)
        
        ttk.Label(content_frame, text="Описание:").grid(row=1, column=0, sticky=tk.NW, pady=5)
        text = tk.Text(content_frame, height=5)
        text.grid(row=1, column=1, sticky=tk.EW, pady=5)
        
        # Кнопки действий
        action_frame = ttk.Frame(content_frame)
        action_frame.grid(row=2, column=0, columnspan=2, pady=10)
        ttk.Button(action_frame, text="Сохранить", command=lambda: self.status("Сохранено")).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Отмена").pack(side=tk.LEFT, padx=5)
    
    def create_statusbar(self):
        """Создание панели статуса (pack)"""
        self.statusbar = ttk.Label(self.root, text="Готов", relief=tk.SUNKEN, anchor=tk.W)
        self.statusbar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def status(self, message):
        """Обновление строки статуса"""
        self.statusbar.config(text=message)
    
    def open_tab(self, name):
        """Открытие вкладки"""
        self.status(f"Открыта вкладка: {name}")
    
    def show_about(self):
        """Показ диалога о программе"""
        messagebox.showinfo("О программе", "Приложение с сложным макетом\n\n"
                         "Демонстрация комбинирования:\n"
                         "- pack (тулбар, статусбар)\n"
                         "- grid (основная область)\n"
                         "- place (меню)")


# ==============================================================================
# ЗАДАЧА 5: Адаптивный интерфейс
# ==============================================================================

class ResponsiveApp:
    """Адаптивное приложение с изменяемым размером"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Задача 5: Адаптивный интерфейс")
        self.root.geometry("600x400")
        self.root.minsize(400, 300)
        
        self.create_responsive_layout()
        self.create_splitter()
        self.create_scrollable_area()
    
    def create_responsive_layout(self):
        """Создание адаптивного макета"""
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Настройка весов для адаптивности
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=2)
        main_frame.rowconfigure(0, weight=1)
        
        # Левая панель
        left_panel = ttk.LabelFrame(main_frame, text="Левая панель", padding=10)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(5, 2), pady=5)
        
        # Содержимое левой панели
        ttk.Label(left_panel, text="Список элементов:").pack(anchor=tk.W)
        
        self.listbox = tk.Listbox(left_panel)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        for i in range(20):
            self.listbox.insert(tk.END, f"Элемент {i+1}")
        
        # Скроллбар для списка
        scrollbar = ttk.Scrollbar(left_panel, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)
        
        # Правая панель
        right_panel = ttk.LabelFrame(main_frame, text="Правая панель", padding=10)
        right_panel.grid(row=0, column=1, sticky="new", padx=(2, 5), pady=5)
        
        # Минимальная высота для правой панели
        right_panel.grid_propagate(False)
        right_panel.rowconfigure(0, weight=1)
        
        # Заголовок
        ttk.Label(right_panel, text="Детали выбранного элемента", font=("Arial", 12)).pack(pady=(0, 10))
        
        # Текстовая область
        text_area = tk.Text(right_panel, wrap=tk.WORD)
        text_area.pack(fill=tk.BOTH, expand=True)
        text_area.insert(tk.END, "Выберите элемент из списка слева для просмотра деталей.\n\n"
                        "Этот интерфейс адаптируется к изменению размера окна.\n"
                        "Используйте веса (weight) для правильного распределения пространства.")
    
    def create_splitter(self):
        """Создание сплиттера (дополнительная панель внизу)"""
        bottom_frame = ttk.LabelFrame(self.root, text="Нижняя панель", padding=10)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=5, pady=(0, 5))
        
        # Минимальные размеры
        bottom_frame.pack_propagate(False)
        bottom_frame.configure(height=80)
        
        # Горизонтальная адаптивность
        for i in range(3):
            bottom_frame.columnconfigure(i, weight=1)
        
        # Три равные секции
        for i, name in enumerate(["Секция A", "Секция B", "Секция C"]):
            frame = ttk.Frame(bottom_frame, relief=tk.RIDGE, borderwidth=1)
            frame.grid(row=0, column=i, sticky="nsew", padx=2)
            
            ttk.Label(frame, text=name, anchor=tk.CENTER).pack(fill=tk.X)
            ttk.Entry(frame).pack(fill=tk.X, padx=5, pady=5)
    
    def create_scrollable_area(self):
        """Создание области со скроллированием (дополнительная функция)"""
        # Дополнительная демонстрация - не добавляем в основной интерфейс
        pass


# ==============================================================================
# ГЛАВНОЕ МЕНЮ ПРИЛОЖЕНИЯ
# ==============================================================================

class MainApp:
    """Главное приложение с выбором задач"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Практическое занятие 22: Tkinter - управление макетом")
        self.root.geometry("500x400")
        
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
            ("Задача 1: Pack Manager", self.open_pack_demo),
            ("Задача 2a: Калькулятор (grid)", self.open_calculator),
            ("Задача 2b: Форма ввода (grid)", self.open_form),
            ("Задача 3: Place Manager", self.open_place_demo),
            ("Задача 4: Комбинирование менеджеров", self.open_complex_layout),
            ("Задача 5: Адаптивный интерфейс", self.open_responsive),
        ]
        
        for text, command in tasks:
            btn = ttk.Button(main_frame, text=text, width=35, command=command)
            btn.pack(pady=5)
        
        ttk.Button(main_frame, text="Выход", command=self.root.quit).pack(pady=20)
    
    def open_pack_demo(self):
        """Открыть демонстрацию pack"""
        window = tk.Toplevel(self.root)
        PackManagerDemo(window)
    
    def open_calculator(self):
        """Открыть калькулятор"""
        window = tk.Toplevel(self.root)
        CalculatorApp(window)
    
    def open_form(self):
        """Открыть форму ввода"""
        window = tk.Toplevel(self.root)
        InputFormDemo(window)
    
    def open_place_demo(self):
        """Открыть демонстрацию place"""
        window = tk.Toplevel(self.root)
        PlaceManagerDemo(window)
    
    def open_complex_layout(self):
        """Открыть сложный макет"""
        window = tk.Toplevel(self.root)
        ComplexLayoutApp(window)
    
    def open_responsive(self):
        """Открыть адаптивный интерфейс"""
        window = tk.Toplevel(self.root)
        ResponsiveApp(window)


def main():
    """Точка входа"""
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
