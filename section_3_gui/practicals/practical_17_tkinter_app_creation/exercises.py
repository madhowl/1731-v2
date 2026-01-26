# Упражнения для практического занятия 17: Создание GUI с помощью Tkinter

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import os
import json
from typing import Dict, Any, List, Optional
import threading
import time

# Задание 1: Создание базового окна
class BasicWindowApp:
    """Приложение с базовым окном Tkinter"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Базовое окно Tkinter")
        self.root.geometry("600x400")
        self.root.resizable(True, True)
        
        # Устанавливаем иконку (если файл существует)
        try:
            if os.path.exists("icon.ico"):
                self.root.iconbitmap("icon.ico")
        except:
            pass  # Игнорируем ошибку, если иконка не найдена
        
        # Центральное размещение окна
        self.center_window()
        
        # Обработчик закрытия окна
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Основной фрейм
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Метка с приветствием
        self.welcome_label = tk.Label(
            self.main_frame, 
            text="Добро пожаловать в приложение Tkinter!", 
            font=("Arial", 16),
            fg="blue"
        )
        self.welcome_label.pack(pady=20)
        
        # Кнопка для демонстрации
        self.demo_button = tk.Button(
            self.main_frame,
            text="Нажми меня!",
            command=self.button_clicked,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12)
        )
        self.demo_button.pack(pady=10)
    
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
        if messagebox.askokcancel("Выход", "Вы уверены, что хотите выйти?"):
            self.root.destroy()
    
    def button_clicked(self):
        """Обработчик нажатия кнопки"""
        messagebox.showinfo("Информация", "Кнопка была нажата!")
    
    def run(self):
        self.root.mainloop()

# Задание 2: Работа с виджетами
class WidgetCollectionApp:
    """Приложение с коллекцией виджетов"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Коллекция виджетов Tkinter")
        self.root.geometry("700x600")
        
        # Переменные для связи с виджетами
        self.text_var = tk.StringVar(value="Введите текст здесь")
        self.check_var = tk.BooleanVar()
        self.radio_var = tk.StringVar(value="option1")
        self.combo_var = tk.StringVar()
        
        # Создаем вкладки для организации виджетов
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Вкладка с основными виджетами
        self.basic_widgets_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.basic_widgets_tab, text="Основные виджеты")
        self.create_basic_widgets()
        
        # Вкладка с расширенными виджетами
        self.advanced_widgets_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.advanced_widgets_tab, text="Расширенные виджеты")
        self.create_advanced_widgets()
    
    def create_basic_widgets(self):
        """Создает основные виджеты"""
        # Фрейм для основных виджетов
        frame = ttk.LabelFrame(self.basic_widgets_tab, text="Основные виджеты")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Кнопки
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Обычная кнопка", command=self.normal_button_click).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Встроенная кнопка", style="Accent.TButton", command=self.accent_button_click).pack(side=tk.LEFT, padx=5)
        
        # Метка
        ttk.Label(frame, text="Это обычная метка").pack(pady=5)
        
        # Поле ввода
        entry = ttk.Entry(frame, textvariable=self.text_var, width=30)
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
        ttk.Checkbutton(frame, text="Флажок", variable=self.check_var, command=self.checkbox_changed).pack(pady=5)
        
        # Переключатели
        radio_frame = ttk.Frame(frame)
        radio_frame.pack(fill=tk.X, pady=5)
        
        ttk.Radiobutton(radio_frame, text="Опция 1", variable=self.radio_var, value="option1", command=self.radio_changed).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(radio_frame, text="Опция 2", variable=self.radio_var, value="option2", command=self.radio_changed).pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(radio_frame, text="Опция 3", variable=self.radio_var, value="option3", command=self.radio_changed).pack(side=tk.LEFT, padx=5)
    
    def create_advanced_widgets(self):
        """Создает расширенные виджеты"""
        # Фрейм для расширенных виджетов
        frame = ttk.LabelFrame(self.advanced_widgets_tab, text="Расширенные виджеты")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Комбинированный список
        combo_frame = ttk.Frame(frame)
        combo_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(combo_frame, text="Комбинированный список:").pack(anchor=tk.W)
        self.combo_box = ttk.Combobox(combo_frame, textvariable=self.combo_var, values=["Элемент 1", "Элемент 2", "Элемент 3", "Элемент 4"])
        self.combo_box.pack(fill=tk.X, pady=5)
        self.combo_box.bind("<<ComboboxSelected>>", self.combo_selected)
        
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
        
        # Прогресс бар
        progress_frame = ttk.Frame(frame)
        progress_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(progress_frame, text="Прогресс бар:").pack(anchor=tk.W)
        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        # Кнопка для запуска прогресса
        ttk.Button(progress_frame, text="Запустить прогресс", command=self.start_progress).pack(pady=5)
    
    def normal_button_click(self):
        """Обработчик обычной кнопки"""
        messagebox.showinfo("Информация", "Нажата обычная кнопка")
    
    def accent_button_click(self):
        """Обработчик акцентной кнопки"""
        messagebox.showinfo("Информация", "Нажата акцентная кнопка")
    
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
    
    def combo_selected(self, event):
        """Обработчик выбора в комбинированном списке"""
        selected = self.combo_var.get()
        self.text_area.insert(tk.END, f"Выбран элемент: {selected}\n")
        self.text_area.see(tk.END)
    
    def start_progress(self):
        """Запускает анимацию прогресса"""
        self.progress_bar.start(10)
        # Останавливаем через 3 секунды
        self.root.after(3000, self.stop_progress)
    
    def stop_progress(self):
        """Останавливает анимацию прогресса"""
        self.progress_bar.stop()
    
    def run(self):
        self.root.mainloop()

# Задание 3: Расположение элементов
class LayoutManagementApp:
    """Приложение для демонстрации менеджеров размещения"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Менеджеры размещения Tkinter")
        self.root.geometry("800x600")
        
        # Создаем вкладки для разных менеджеров
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Вкладка для pack
        self.pack_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.pack_tab, text="Pack")
        self.create_pack_layout()
        
        # Вкладка для grid
        self.grid_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.grid_tab, text="Grid")
        self.create_grid_layout()
        
        # Вкладка для place
        self.place_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.place_tab, text="Place")
        self.create_place_layout()
    
    def create_pack_layout(self):
        """Создает макет с использованием pack"""
        # Основной фрейм
        frame = ttk.LabelFrame(self.pack_tab, text="Пример использования pack")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Верхняя панель
        top_frame = ttk.Frame(frame)
        top_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(top_frame, text="Слева", command=lambda: self.log_action("Pack - Кнопка СЛЕВА")).pack(side=tk.LEFT, padx=5)
        ttk.Button(top_frame, text="Справа", command=lambda: self.log_action("Pack - Кнопка СПРАВА")).pack(side=tk.RIGHT, padx=5)
        ttk.Button(top_frame, text="По центру", command=lambda: self.log_action("Pack - Кнопка ЦЕНТР")).pack(pady=5)
        
        # Средняя часть
        center_frame = ttk.Frame(frame)
        center_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        for i in range(3):
            ttk.Button(center_frame, text=f"Кнопка {i+1}", 
                      command=lambda x=i: self.log_action(f"Pack - Кнопка {x+1}")).pack(pady=2)
        
        # Нижняя панель
        bottom_frame = ttk.Frame(frame)
        bottom_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(bottom_frame, text="Нижняя панель").pack(pady=5)
    
    def create_grid_layout(self):
        """Создает макет с использованием grid"""
        # Основной фрейм
        frame = ttk.LabelFrame(self.grid_tab, text="Пример использования grid")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Создаем сетку 4x4
        for i in range(4):
            frame.columnconfigure(i, weight=1)
            frame.rowconfigure(i, weight=1)
        
        # Добавляем виджеты в сетку
        positions = [
            (0, 0, "Кнопка 1", "nw"), (0, 1, "Кнопка 2", "nsew"), (0, 2, "Кнопка 3", "ne"),
            (1, 0, "Кнопка 4", "w"), (1, 1, "Центр", "nsew"), (1, 2, "Кнопка 6", "e"),
            (2, 0, "Кнопка 7", "sw"), (2, 1, "Кнопка 8", "swe"), (2, 2, "Кнопка 9", "se")
        ]
        
        for row, col, text, sticky in positions:
            btn = ttk.Button(frame, text=text, command=lambda t=text: self.log_action(f"Grid - {t}"))
            btn.grid(row=row, column=col, sticky=sticky, padx=2, pady=2)
        
        # Текстовая область в нижней части
        text_frame = ttk.Frame(frame)
        text_frame.grid(row=3, column=0, columnspan=3, sticky="nsew", pady=5)
        
        text_scrollbar = ttk.Scrollbar(text_frame)
        text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.grid_text_area = tk.Text(text_frame, height=3, yscrollcommand=text_scrollbar.set)
        self.grid_text_area.pack(fill=tk.BOTH, expand=True)
        text_scrollbar.config(command=self.grid_text_area.yview)
    
    def create_place_layout(self):
        """Создает макет с использованием place"""
        # Основной фрейм
        frame = ttk.LabelFrame(self.place_tab, text="Пример использования place")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Создаем виджеты с точным позиционированием
        positions = [
            (50, 50, "Кнопка 1", lambda: self.log_action("Place - Кнопка 1")),
            (200, 50, "Кнопка 2", lambda: self.log_action("Place - Кнопка 2")),
            (50, 150, "Кнопка 3", lambda: self.log_action("Place - Кнопка 3")),
            (200, 150, "Кнопка 4", lambda: self.log_action("Place - Кнопка 4")),
            (125, 100, "Центр", lambda: self.log_action("Place - Центральная кнопка"))
        ]
        
        for x, y, text, command in positions:
            btn = ttk.Button(frame, text=text, command=command)
            btn.place(x=x, y=y)
        
        # Поле ввода в правом верхнем углу
        self.place_entry = ttk.Entry(frame)
        self.place_entry.place(relx=0.7, rely=0.1, anchor=tk.NE)
        ttk.Label(frame, text="Ввод:").place(relx=0.7, rely=0.05, anchor=tk.NE)
    
    def log_action(self, action):
        """Логирует действие в соответствующую текстовую область"""
        log_msg = f"{time.strftime('%H:%M:%S')} - {action}\n"
        
        # Добавляем в текстовую область на вкладке Grid
        self.grid_text_area.insert(tk.END, log_msg)
        self.grid_text_area.see(tk.END)
    
    def run(self):
        self.root.mainloop()

# Задание 4: Обработка событий
class EventHandlingApp:
    """Приложение для демонстрации обработки событий"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Обработка событий Tkinter")
        self.root.geometry("700x500")
        
        # Создаем Canvas для демонстрации событий мыши
        self.canvas = tk.Canvas(self.root, bg="white", width=680, height=400)
        self.canvas.pack(pady=10)
        
        # Привязываем события мыши
        self.canvas.bind("<Button-1>", self.left_click)  # Левый клик
        self.canvas.bind("<Button-3>", self.right_click)  # Правый клик (на Windows это Button-3)
        self.canvas.bind("<Motion>", self.mouse_move)  # Движение мыши
        self.canvas.bind("<Double-Button-1>", self.double_click)  # Двойной клик
        
        # Привязываем события клавиатуры
        self.root.bind("<KeyPress>", self.key_press)
        self.root.bind("<KeyRelease>", self.key_release)
        
        # Информационная панель
        info_frame = ttk.Frame(self.root)
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(info_frame, text="Координаты:").pack(side=tk.LEFT)
        self.coord_label = ttk.Label(info_frame, text="(0, 0)")
        self.coord_label.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(info_frame, text="Событие:").pack(side=tk.LEFT, padx=(20, 0))
        self.event_label = ttk.Label(info_frame, text="Нет")
        self.event_label.pack(side=tk.LEFT, padx=5)
        
        # Кнопка для фокусировки
        focus_button = ttk.Button(info_frame, text="Фокус", command=self.focus_here)
        focus_button.pack(side=tk.RIGHT, padx=5)
        focus_button.focus_set()  # Устанавливаем фокус на кнопку
    
    def left_click(self, event):
        """Обработка левого клика мыши"""
        self.coord_label.config(text=f"({event.x}, {event.y})")
        self.event_label.config(text="Левый клик")
        # Рисуем круг по клику
        self.canvas.create_oval(event.x-10, event.y-10, event.x+10, event.y+10, 
                               outline="blue", width=2)
    
    def right_click(self, event):
        """Обработка правого клика мыши"""
        self.coord_label.config(text=f"({event.x}, {event.y})")
        self.event_label.config(text="Правый клик")
        # Рисуем квадрат по клику
        self.canvas.create_rectangle(event.x-10, event.y-10, event.x+10, event.y+10, 
                                    outline="red", width=2)
    
    def mouse_move(self, event):
        """Обработка движения мыши"""
        self.coord_label.config(text=f"({event.x}, {event.y})")
        self.event_label.config(text="Движение мыши")
    
    def double_click(self, event):
        """Обработка двойного клика"""
        self.event_label.config(text="Двойной клик")
        # Очищаем холст по двойному клику
        self.canvas.delete("all")
    
    def key_press(self, event):
        """Обработка нажатия клавиши"""
        self.event_label.config(text=f"Клавиша: {event.keysym}")
        if event.keysym.lower() == 'c':
            self.canvas.delete("all")  # Очистить холст по клавише C
        elif event.keysym.lower() == 'q':
            self.root.quit()  # Выйти по клавише Q
    
    def key_release(self, event):
        """Обработка отпускания клавиши"""
        pass  # В этом примере не используем
    
    def focus_here(self):
        """Устанавливает фокус на кнопку"""
        self.event_label.config(text="Фокус установлен")
    
    def run(self):
        self.root.mainloop()

# Задание 5: Комплексное приложение "Калькулятор"
class CalculatorApp:
    """Калькулятор как комплексное приложение"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Калькулятор")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        # Переменные состояния
        self.current = "0"
        self.previous = ""
        self.operator = ""
        self.new_number = True
        
        # Создаем дисплей
        self.display_var = tk.StringVar(value="0")
        self.display = tk.Entry(
            self.root, 
            textvariable=self.display_var, 
            font=("Arial", 20), 
            justify="right",
            state="readonly",
            readonlybackground="white"
        )
        self.display.grid(row=0, column=0, columnspan=4, sticky="ew", padx=5, pady=5)
        
        # Создаем кнопки
        self.create_buttons()
        
        # Настраиваем grid weights
        for i in range(4):
            self.root.columnconfigure(i, weight=1)
        for i in range(6):
            self.root.rowconfigure(i, weight=1)
    
    def create_buttons(self):
        """Создает кнопки калькулятора"""
        # Кнопки цифр
        digits = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2),
            ('0', 4, 1), ('.', 4, 2)
        ]
        
        for (text, row, col) in digits:
            btn = tk.Button(
                self.root, 
                text=text, 
                font=("Arial", 14),
                command=lambda t=text: self.number_click(t)
            )
            btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
        
        # Кнопки операций
        operators = [
            ('/', 1, 3), ('*', 2, 3), ('-', 3, 3), ('+', 4, 3)
        ]
        
        for (text, row, col) in operators:
            btn = tk.Button(
                self.root, 
                text=text, 
                font=("Arial", 14),
                bg="#FF9800",
                fg="white",
                command=lambda t=text: self.operator_click(t)
            )
            btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
        
        # Специальные кнопки
        special_buttons = [
            ('C', 4, 0, self.clear_click, '#F44336'),
            ('=', 4, 3, self.equals_click, '#4CAF50'),
            ('±', 5, 0, self.sign_change_click, '#2196F3'),
            ('⌫', 5, 1, self.backspace_click, '#FF9800'),
            ('%', 5, 2, self.percent_click, '#9C27B0'),
            ('√', 5, 3, self.sqrt_click, '#607D8B')
        ]
        
        for (text, row, col, command, color) in special_buttons:
            btn = tk.Button(
                self.root,
                text=text,
                font=("Arial", 14),
                bg=color,
                fg="white",
                command=command
            )
            btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
    
    def number_click(self, number):
        """Обработка нажатия цифровой кнопки"""
        if self.new_number:
            self.current = number
            self.new_number = False
        else:
            if number == '.' and '.' in self.current:
                return  # Не допускаем двойные точки
            self.current += number
        
        self.display_var.set(self.current)
    
    def operator_click(self, op):
        """Обработка нажатия операционной кнопки"""
        if self.operator and not self.new_number:
            self.equals_click()  # Выполняем предыдущую операцию
        
        self.previous = self.current
        self.operator = op
        self.new_number = True
    
    def equals_click(self):
        """Обработка нажатия кнопки равно"""
        if self.operator and self.previous:
            try:
                prev_num = float(self.previous)
                curr_num = float(self.current)
                
                if self.operator == '+':
                    result = prev_num + curr_num
                elif self.operator == '-':
                    result = prev_num - curr_num
                elif self.operator == '*':
                    result = prev_num * curr_num
                elif self.operator == '/':
                    if curr_num == 0:
                        messagebox.showerror("Ошибка", "Деление на ноль!")
                        return
                    result = prev_num / curr_num
                
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
    
    def clear_click(self):
        """Обработка нажатия кнопки очистки"""
        self.current = "0"
        self.previous = ""
        self.operator = ""
        self.new_number = True
        self.display_var.set("0")
    
    def sign_change_click(self):
        """Изменение знака числа"""
        if self.current != "0":
            if self.current.startswith("-"):
                self.current = self.current[1:]
            else:
                self.current = "-" + self.current
            self.display_var.set(self.current)
    
    def backspace_click(self):
        """Удаление последнего символа"""
        if len(self.current) > 1:
            self.current = self.current[:-1]
        else:
            self.current = "0"
            self.new_number = True
        self.display_var.set(self.current)
    
    def percent_click(self):
        """Вычисление процента"""
        try:
            num = float(self.current) / 100
            self.current = str(num)
            self.display_var.set(self.current)
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный ввод!")
    
    def sqrt_click(self):
        """Вычисление квадратного корня"""
        try:
            num = float(self.current)
            if num < 0:
                messagebox.showerror("Ошибка", "Невозможно извлечь корень из отрицательного числа!")
                return
            result = num ** 0.5
            if result == int(result):
                result = int(result)
            self.current = str(result)
            self.display_var.set(self.current)
        except ValueError:
            messagebox.showerror("Ошибка", "Неверный ввод!")
    
    def run(self):
        self.root.mainloop()

# Примеры использования:
if __name__ == "__main__":
    print("=== Упражнения для практического занятия 17 ===")
    
    print("\n1. Базовое окно Tkinter:")
    # basic_app = BasicWindowApp()
    # basic_app.run()
    
    print("\n2. Коллекция виджетов:")
    # widget_app = WidgetCollectionApp()
    # widget_app.run()
    
    print("\n3. Менеджеры размещения:")
    # layout_app = LayoutManagementApp()
    # layout_app.run()
    
    print("\n4. Обработка событий:")
    # event_app = EventHandlingApp()
    # event_app.run()
    
    print("\n5. Калькулятор:")
    # calc_app = CalculatorApp()
    # calc_app.run()
    
    # Для демонстрации запустим только одно приложение
    print("Запуск приложения 'Калькулятор'...")
    app = CalculatorApp()
    app.run()