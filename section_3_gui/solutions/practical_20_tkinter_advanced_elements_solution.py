# Решения для практического занятия 20: Tkinter - продвинутые элементы

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
import random
from typing import Dict, Any, List
import json


# =============================================================================
# Задание 1: Treeview
# =============================================================================

class TreeviewExercise:
    """Упражнение с Treeview"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Задание 1: Treeview")
        self.root.geometry("800x600")
        
        # Создаем Treeview с прокруткой
        tree_frame = ttk.Frame(self.root)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tree_scrollbar = ttk.Scrollbar(tree_frame)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scrollbar.set)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        tree_scrollbar.config(command=self.tree.yview)
        
        # Определяем колонки
        self.tree['columns'] = ("Имя", "Возраст", "Должность", "Зарплата")
        
        # Форматируем колонки
        self.tree.column("#0", width=0, stretch=tk.NO)  # Скрытая колонка
        self.tree.column("Имя", anchor=tk.W, width=120)
        self.tree.column("Возраст", anchor=tk.CENTER, width=80)
        self.tree.column("Должность", anchor=tk.W, width=150)
        self.tree.column("Зарплата", anchor=tk.E, width=100)
        
        # Создаем заголовки
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("Имя", text="Имя", anchor=tk.W)
        self.tree.heading("Возраст", text="Возраст", anchor=tk.W)
        self.tree.heading("Должность", text="Должность", anchor=tk.W)
        self.tree.heading("Зарплата", text="Зарплата", anchor=tk.W)
        
        # Добавляем данные
        self.add_sample_data()
        
        # Кнопки управления
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Добавить", command=self.add_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Удалить", command=self.remove_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Редактировать", command=self.edit_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Сортировать по имени", command=lambda: self.sort_column("Имя")).pack(side=tk.LEFT, padx=5)
        
        # Привязываем события
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.bind("<Double-Button-1>", self.on_double_click)
    
    def add_sample_data(self):
        """Добавляет образцы данных в дерево"""
        # Добавляем элементы верхнего уровня (отделы)
        hr_dept = self.tree.insert("", tk.END, text="Отдел HR", values=("", "", "HR", ""))
        dev_dept = self.tree.insert("", tk.END, text="Отдел разработки", values=("", "", "Dev", ""))
        sales_dept = self.tree.insert("", tk.END, text="Отдел продаж", values=("", "", "Sales", ""))
        
        # Добавляем сотрудников в отделы
        employees = [
            ("Иванов Иван", 30, "Менеджер", 120000),
            ("Петрова Мария", 28, "Ассистент", 80000)
        ]
        for emp in employees:
            self.tree.insert(hr_dept, tk.END, values=emp)
        
        employees = [
            ("Сидоров Алексей", 35, "Старший разработчик", 150000),
            ("Козлова Елена", 26, "Младший разработчик", 90000),
            ("Морозов Дмитрий", 32, "Архитектор", 200000)
        ]
        for emp in employees:
            self.tree.insert(dev_dept, tk.END, values=emp)
        
        employees = [
            ("Волкова Анна", 29, "Менеджер по продажам", 110000),
            ("Никитин Сергей", 31, "Директор по продажам", 180000)
        ]
        for emp in employees:
            self.tree.insert(sales_dept, tk.END, values=emp)
    
    def add_item(self):
        """Добавляет новый элемент"""
        # В реальном приложении здесь был бы диалог добавления
        new_emp = (f"Новый Сотрудник {len(self.tree.get_children())}", 
                  random.randint(22, 60), "Стажер", 60000)
        selected = self.tree.selection()
        if selected:
            parent = selected[0]
        else:
            parent = ""
        self.tree.insert(parent, tk.END, values=new_emp)
    
    def remove_item(self):
        """Удаляет выбранный элемент"""
        selected = self.tree.selection()
        if selected:
            self.tree.delete(selected)
    
    def edit_item(self):
        """Редактирует выбранный элемент"""
        selected = self.tree.selection()
        if selected:
            # В реальном приложении здесь был бы диалог редактирования
            item = self.tree.item(selected)
            print(f"Редактирование элемента: {item}")
            messagebox.showinfo("Редактирование", f"Редактирование элемента: {item['values']}")
    
    def sort_column(self, col):
        """Сортирует колонку"""
        # Получаем все элементы
        children = self.tree.get_children()
        # Сортируем по значению в колонке
        values = []
        for child in children:
            val = self.tree.set(child, col)
            values.append((val, child))
        
        # Сортируем значения
        values.sort(key=lambda x: str(x[0]))
        
        # Переставляем элементы в отсортированном порядке
        for i, (_, child) in enumerate(values):
            self.tree.move(child, '', i)
    
    def on_tree_select(self, event):
        """Обработка выбора элемента в дереве"""
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected)
            print(f"Выбран элемент: {item}")
    
    def on_double_click(self, event):
        """Обработка двойного клика"""
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            # Двойной клик по ячейке - редактирование
            self.edit_item()
    
    def run(self):
        self.root.mainloop()


# =============================================================================
# Задание 2: Progressbar
# =============================================================================

class ProgressbarExercise:
    """Упражнение с Progressbar"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Задание 2: Progressbar")
        self.root.geometry("700x600")
        
        # Создаем фреймы для разных типов прогресс баров
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Определенный прогресс бар
        det_frame = ttk.LabelFrame(main_frame, text="Определенный прогресс бар")
        det_frame.pack(fill=tk.X, pady=5)
        
        self.determinate_pb = ttk.Progressbar(det_frame, mode='determinate', maximum=100)
        self.determinate_pb.pack(fill=tk.X, pady=5)
        
        det_buttons = ttk.Frame(det_frame)
        det_buttons.pack(fill=tk.X, pady=5)
        
        ttk.Button(det_buttons, text="Запустить", command=self.start_determinate).pack(side=tk.LEFT, padx=5)
        ttk.Button(det_buttons, text="Стоп", command=self.stop_determinate).pack(side=tk.LEFT, padx=5)
        ttk.Button(det_buttons, text="Сброс", command=self.reset_determinate).pack(side=tk.LEFT, padx=5)
        
        # Неопределенный прогресс бар
        indet_frame = ttk.LabelFrame(main_frame, text="Неопределенный прогресс бар")
        indet_frame.pack(fill=tk.X, pady=10)
        
        self.indeterminate_pb = ttk.Progressbar(indet_frame, mode='indeterminate')
        self.indeterminate_pb.pack(fill=tk.X, pady=5)
        
        indet_buttons = ttk.Frame(indet_frame)
        indet_buttons.pack(fill=tk.X, pady=5)
        
        ttk.Button(indet_buttons, text="Старт", command=self.start_indeterminate).pack(side=tk.LEFT, padx=5)
        ttk.Button(indet_buttons, text="Стоп", command=self.stop_indeterminate).pack(side=tk.LEFT, padx=5)
        
        # Множественные прогресс бары
        multi_frame = ttk.LabelFrame(main_frame, text="Множественные прогресс бары")
        multi_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.progress_bars = []
        for i in range(5):
            pb_frame = ttk.Frame(multi_frame)
            pb_frame.pack(fill=tk.X, pady=2)
            
            ttk.Label(pb_frame, text=f"Задача {i+1}:").pack(side=tk.LEFT)
            pb = ttk.Progressbar(pb_frame, mode='determinate', maximum=100)
            pb.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
            self.progress_bars.append(pb)
        
        multi_buttons = ttk.Frame(multi_frame)
        multi_buttons.pack(fill=tk.X, pady=5)
        
        ttk.Button(multi_buttons, text="Запустить все", command=self.start_all_progress).pack(side=tk.LEFT, padx=5)
        ttk.Button(multi_buttons, text="Синхронизировать", command=self.sync_progress).pack(side=tk.LEFT, padx=5)
        
        # Индикатор выполнения
        self.status_label = ttk.Label(main_frame, text="Готово", foreground="green")
        self.status_label.pack(pady=5)
    
    def start_determinate(self):
        """Запускает определенный прогресс бар"""
        def update_progress():
            for i in range(101):
                self.determinate_pb['value'] = i
                self.root.update()
                time.sleep(0.02)
            self.status_label.config(text="Определенный прогресс завершен", foreground="blue")
        
        # Запускаем в отдельном потоке, чтобы не блокировать интерфейс
        thread = threading.Thread(target=update_progress)
        thread.daemon = True
        thread.start()
    
    def stop_determinate(self):
        """Останавливает определенный прогресс бар"""
        self.determinate_pb.stop()
    
    def reset_determinate(self):
        """Сбрасывает определенный прогресс бар"""
        self.determinate_pb['value'] = 0
        self.status_label.config(text="Прогресс сброшен", foreground="green")
    
    def start_indeterminate(self):
        """Запускает неопределенный прогресс бар"""
        self.indeterminate_pb.start(10)  # Обновление каждые 10мс
        self.status_label.config(text="Неопределенный прогресс запущен", foreground="orange")
    
    def stop_indeterminate(self):
        """Останавливает неопределенный прогресс бар"""
        self.indeterminate_pb.stop()
        self.status_label.config(text="Неопределенный прогресс остановлен", foreground="green")
    
    def start_all_progress(self):
        """Запускает все прогресс бары"""
        def update_multiple():
            for i in range(101):
                for pb in self.progress_bars:
                    pb['value'] = i
                self.root.update()
                time.sleep(0.01)
            self.status_label.config(text="Все прогресс бары завершены", foreground="blue")
        
        thread = threading.Thread(target=update_multiple)
        thread.daemon = True
        thread.start()
    
    def sync_progress(self):
        """Синхронизирует прогресс бары"""
        current_max = max(pb['value'] for pb in self.progress_bars)
        for pb in self.progress_bars:
            pb['value'] = current_max
    
    def run(self):
        self.root.mainloop()


# =============================================================================
# Задание 3: Notebook
# =============================================================================

class NotebookExercise:
    """Упражнение с Notebook"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Задание 3: Notebook")
        self.root.geometry("800x600")
        
        # Создаем Notebook
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Создаем вкладки
        self.create_tabs()
        
        # Кнопки управления вкладками
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Добавить вкладку", command=self.add_tab).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Удалить вкладку", command=self.remove_tab).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Показать количество", command=self.show_count).pack(side=tk.LEFT, padx=5)
        
        # Привязываем событие переключения вкладок
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_change)
    
    def create_tabs(self):
        """Создает начальные вкладки"""
        # Вкладка 1: Информация
        tab1 = ttk.Frame(self.notebook)
        self.notebook.add(tab1, text="Информация")
        
        ttk.Label(tab1, text="Это первая вкладка", font=("Arial", 16)).pack(pady=20)
        ttk.Button(tab1, text="Кнопка вкладки 1", 
                  command=lambda: self.tab_button_clicked(1)).pack(pady=10)
        
        # Вкладка 2: Настройки
        tab2 = ttk.Frame(self.notebook)
        self.notebook.add(tab2, text="Настройки")
        
        ttk.Label(tab2, text="Это вторая вкладка", font=("Arial", 16)).pack(pady=20)
        self.settings_var = tk.StringVar(value="Значение по умолчанию")
        ttk.Entry(tab2, textvariable=self.settings_var).pack(pady=5)
        ttk.Button(tab2, text="Сохранить настройки", 
                  command=self.save_settings).pack(pady=10)
        
        # Вкладка 3: Данные
        tab3 = ttk.Frame(self.notebook)
        self.notebook.add(tab3, text="Данные")
        
        # Добавляем Treeview на вкладку данных
        tree_frame = ttk.Frame(tab3)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tree_scrollbar = ttk.Scrollbar(tree_frame)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree = ttk.Treeview(tree_frame, columns=("Value",), show="tree headings", 
                           yscrollcommand=tree_scrollbar.set)
        tree.heading("#0", text="Ключ")
        tree.heading("Value", text="Значение")
        tree.column("#0", width=150)
        tree.column("Value", width=200)
        
        tree.pack(fill=tk.BOTH, expand=True)
        tree_scrollbar.config(command=tree.yview)
        
        # Добавляем данные в Treeview
        data = {
            "Пользователь": "Иванов Иван",
            "Email": "ivanov@example.com",
            "Телефон": "+7 (999) 123-45-67"
        }
        for key, value in data.items():
            tree.insert("", tk.END, text=key, values=(value,))
    
    def add_tab(self):
        """Добавляет новую вкладку"""
        tab_num = len(self.notebook.tabs()) + 1
        new_tab = ttk.Frame(self.notebook)
        self.notebook.add(new_tab, text=f"Вкладка {tab_num}")
        
        ttk.Label(new_tab, text=f"Содержимое вкладки {tab_num}", font=("Arial", 14)).pack(pady=20)
        ttk.Button(new_tab, text=f"Кнопка вкладки {tab_num}", 
                  command=lambda: self.tab_button_clicked(tab_num)).pack(pady=10)
    
    def remove_tab(self):
        """Удаляет текущую вкладку"""
        current_tab = self.notebook.select()
        if current_tab:
            # Не удаляем, если это последняя вкладка
            tabs_count = len(self.notebook.tabs())
            if tabs_count > 1:
                self.notebook.forget(current_tab)
            else:
                messagebox.showwarning("Предупреждение", "Нельзя удалить последнюю вкладку")
    
    def show_count(self):
        """Показывает количество вкладок"""
        count = len(self.notebook.tabs())
        messagebox.showinfo("Информация", f"Количество вкладок: {count}")
    
    def on_tab_change(self, event):
        """Обработка переключения вкладок"""
        current_tab = self.notebook.index(self.notebook.select())
        tab_text = self.notebook.tab(current_tab, "text")
        print(f"Переключена вкладка на: {tab_text}")
    
    def tab_button_clicked(self, tab_num):
        """Обработка нажатия кнопки на вкладке"""
        print(f"Нажата кнопка на вкладке {tab_num}")
    
    def save_settings(self):
        """Сохранение настроек"""
        print(f"Сохранение настроек: {self.settings_var.get()}")
        messagebox.showinfo("Сохранение", f"Настройки сохранены: {self.settings_var.get()}")
    
    def run(self):
        self.root.mainloop()


# =============================================================================
# Задание 4: PanedWindow
# =============================================================================

class PanedWindowExercise:
    """Упражнение с PanedWindow"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Задание 4: PanedWindow")
        self.root.geometry("900x700")
        
        # Создаем основной PanedWindow (горизонтальный)
        self.main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        self.main_paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Левая панель
        left_frame = ttk.Frame(self.main_paned, width=300, height=600)
        self.main_paned.add(left_frame, weight=1)
        
        # Левая панель с вертикальным разделителем
        left_paned = ttk.PanedWindow(left_frame, orient=tk.VERTICAL)
        left_paned.pack(fill=tk.BOTH, expand=True)
        
        # Верхняя часть левой панели
        top_left = ttk.Frame(left_paned)
        left_paned.add(top_left, weight=1)
        
        ttk.Label(top_left, text="Верхняя часть левой панели", font=("Arial", 12)).pack(pady=20)
        
        # Добавляем список
        listbox_frame = ttk.Frame(top_left)
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        listbox_scrollbar = ttk.Scrollbar(listbox_frame)
        listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.left_listbox = tk.Listbox(listbox_frame, yscrollcommand=listbox_scrollbar.set)
        self.left_listbox.pack(fill=tk.BOTH, expand=True)
        listbox_scrollbar.config(command=self.left_listbox.yview)
        
        # Заполняем список
        for i in range(20):
            self.left_listbox.insert(tk.END, f"Элемент {i+1}")
        
        # Нижняя часть левой панели
        bottom_left = ttk.Frame(left_paned)
        left_paned.add(bottom_left, weight=1)
        
        ttk.Label(bottom_left, text="Нижняя часть левой панели", font=("Arial", 12)).pack(pady=20)
        
        # Правая панель
        right_frame = ttk.Frame(self.main_paned, width=600, height=600)
        self.main_paned.add(right_frame, weight=2)
        
        # Правая панель с горизонтальным разделителем
        right_paned = ttk.PanedWindow(right_frame, orient=tk.HORIZONTAL)
        right_paned.pack(fill=tk.BOTH, expand=True)
        
        # Левая часть правой панели
        right_left = ttk.Frame(right_paned)
        right_paned.add(right_left, weight=1)
        
        ttk.Label(right_left, text="Левая часть правой панели", font=("Arial", 12)).pack(pady=20)
        
        # Добавляем Treeview
        tree_frame = ttk.Frame(right_left)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tree_scrollbar = ttk.Scrollbar(tree_frame)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.right_tree = ttk.Treeview(tree_frame, columns=("Value",), show="tree headings",
                                      yscrollcommand=tree_scrollbar.set)
        self.right_tree.heading("#0", text="Ключ")
        self.right_tree.heading("Value", text="Значение")
        self.right_tree.column("#0", width=100)
        self.right_tree.column("Value", width=150)
        
        self.right_tree.pack(fill=tk.BOTH, expand=True)
        tree_scrollbar.config(command=self.right_tree.yview)
        
        # Заполняем Treeview
        data = {
            "Файл 1": "document.pdf",
            "Файл 2": "image.jpg",
            "Файл 3": "data.xlsx"
        }
        for key, value in data.items():
            self.right_tree.insert("", tk.END, text=key, values=(value,))
        
        # Правая часть правой панели
        right_right = ttk.Frame(right_paned)
        right_paned.add(right_right, weight=1)
        
        ttk.Label(right_right, text="Правая часть правой панели", font=("Arial", 12)).pack(pady=20)
        
        # Добавляем текстовое поле
        text_frame = ttk.Frame(right_right)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        text_scrollbar = ttk.Scrollbar(text_frame)
        text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.right_text = tk.Text(text_frame, yscrollcommand=text_scrollbar.set)
        self.right_text.pack(fill=tk.BOTH, expand=True)
        text_scrollbar.config(command=self.right_text.yview)
        
        # Добавляем пример текста
        sample_text = "Это пример текста для правой части правой панели.\n" * 20
        self.right_text.insert(tk.END, sample_text)
    
    def run(self):
        self.root.mainloop()


# =============================================================================
# Задание 5: Комплексное приложение "Менеджер задач"
# =============================================================================

class TaskManagerApp:
    """Комплексное приложение - менеджер задач"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Задание 5: Менеджер задач")
        self.root.geometry("1000x700")
        
        # Данные задач
        self.tasks = []
        self.task_id_counter = 1
        
        # Создаем интерфейс
        self.create_widgets()
        
        # Добавляем примеры задач
        self.add_sample_tasks()
    
    def create_widgets(self):
        """Создает виджеты приложения"""
        # Основной фрейм с разделителем
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True)
        
        # Левая панель - список задач
        left_frame = ttk.Frame(main_paned)
        main_paned.add(left_frame, weight=2)
        
        # Заголовок
        ttk.Label(left_frame, text="Список задач", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Фрейм для кнопок
        button_frame = ttk.Frame(left_frame)
        button_frame.pack(fill=tk.X, padx=10)
        
        ttk.Button(button_frame, text="Добавить", command=self.add_task).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Редактировать", command=self.edit_task).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Удалить", command=self.delete_task).pack(side=tk.LEFT, padx=2)
        
        # Treeview для задач
        tree_frame = ttk.Frame(left_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tree_scrollbar = ttk.Scrollbar(tree_frame)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.task_tree = ttk.Treeview(tree_frame, columns=("Статус", "Приоритет", "Дата"), 
                                      show="tree headings", yscrollcommand=tree_scrollbar.set)
        self.task_tree.heading("#0", text="Задача")
        self.task_tree.heading("Статус", text="Статус")
        self.task_tree.heading("Приоритет", text="Приоритет")
        self.task_tree.heading("Дата", text="Срок")
        
        self.task_tree.column("#0", width=250)
        self.task_tree.column("Статус", width=100)
        self.task_tree.column("Приоритет", width=80)
        self.task_tree.column("Дата", width=100)
        
        self.task_tree.pack(fill=tk.BOTH, expand=True)
        tree_scrollbar.config(command=self.task_tree.yview)
        
        # Привязываем событие выбора
        self.task_tree.bind("<<TreeviewSelect>>", self.on_task_select)
        
        # Правая панель - детали задачи
        right_frame = ttk.Frame(main_paned)
        main_paned.add(right_frame, weight=1)
        
        ttk.Label(right_frame, text="Детали задачи", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Детали задачи
        detail_frame = ttk.LabelFrame(right_frame, text="Информация")
        detail_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(detail_frame, text="Название:").pack(anchor=tk.W, padx=5, pady=2)
        self.detail_name = ttk.Label(detail_frame, text="-", font=("Arial", 10, "bold"))
        self.detail_name.pack(anchor=tk.W, padx=5, pady=2)
        
        ttk.Label(detail_frame, text="Описание:").pack(anchor=tk.W, padx=5, pady=2)
        self.detail_description = tk.Text(detail_frame, height=5, wrap=tk.WORD)
        self.detail_description.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(detail_frame, text="Статус:").pack(anchor=tk.W, padx=5, pady=2)
        self.detail_status = ttk.Label(detail_frame, text="-")
        self.detail_status.pack(anchor=tk.W, padx=5, pady=2)
        
        # Прогресс выполнения
        ttk.Label(detail_frame, text="Прогресс:").pack(anchor=tk.W, padx=5, pady=2)
        self.progress_var = tk.IntVar(value=0)
        self.progress_bar = ttk.Progressbar(detail_frame, mode='determinate', maximum=100, variable=self.progress_var)
        self.progress_bar.pack(fill=tk.X, padx=5, pady=2)
        
        self.progress_label = ttk.Label(detail_frame, text="0%")
        self.progress_label.pack(anchor=tk.W, padx=5, pady=2)
    
    def add_sample_tasks(self):
        """Добавляет примеры задач"""
        sample_tasks = [
            ("Разработать UI", "Высокий", "В работе", "2024-12-31"),
            ("Написать тесты", "Средний", "В ожидании", "2024-12-25"),
            ("Документация", "Низкий", "Завершена", "2024-12-20"),
        ]
        
        for name, priority, status, date in sample_tasks:
            self.tasks.append({
                "id": self.task_id_counter,
                "name": name,
                "description": "Описание задачи",
                "priority": priority,
                "status": status,
                "date": date,
                "progress": 50 if status == "В работе" else (100 if status == "Завершена" else 0)
            })
            self.task_tree.insert("", tk.END, text=name, values=(status, priority, date))
            self.task_id_counter += 1
    
    def add_task(self):
        """Добавляет новую задачу"""
        new_task = f"Новая задача {self.task_id_counter}"
        self.tasks.append({
            "id": self.task_id_counter,
            "name": new_task,
            "description": "Описание",
            "priority": "Средний",
            "status": "В ожидании",
            "date": "2024-12-31",
            "progress": 0
        })
        self.task_tree.insert("", tk.END, text=new_task, values=("В ожидании", "Средний", "2024-12-31"))
        self.task_id_counter += 1
    
    def edit_task(self):
        """Редактирует выбранную задачу"""
        messagebox.showinfo("Редактирование", "Функция редактирования задачи")
    
    def delete_task(self):
        """Удаляет выбранную задачу"""
        selected = self.task_tree.selection()
        if selected:
            self.task_tree.delete(selected)
            messagebox.showinfo("Удаление", "Задача удалена")
    
    def on_task_select(self, event):
        """Обработка выбора задачи"""
        selected = self.task_tree.selection()
        if selected:
            # Обновляем детали
            item = self.task_tree.item(selected[0])
            values = item['values']
            if values:
                self.detail_name.config(text=item['text'])
                self.detail_status.config(text=values[0])
                self.progress_var.set(50)
                self.progress_label.config(text="50%")
    
    def run(self):
        self.root.mainloop()


# =============================================================================
# Главная функция для запуска приложений
# =============================================================================

def main():
    """Главная функция для демонстрации решений"""
    print("Решения для практического занятия 20: Tkinter - продвинутые элементы")
    print("=" * 70)
    print("Выберите приложение для запуска:")
    print("1 - Treeview")
    print("2 - Progressbar")
    print("3 - Notebook")
    print("4 - PanedWindow")
    print("5 - Менеджер задач")
    print("0 - Выход")
    print("=" * 70)
    
    choice = input("Ваш выбор: ")
    
    if choice == "1":
        app = TreeviewExercise()
        app.run()
    elif choice == "2":
        app = ProgressbarExercise()
        app.run()
    elif choice == "3":
        app = NotebookExercise()
        app.run()
    elif choice == "4":
        app = PanedWindowExercise()
        app.run()
    elif choice == "5":
        app = TaskManagerApp()
        app.run()
    else:
        print("До свидания!")


if __name__ == "__main__":
    main()
