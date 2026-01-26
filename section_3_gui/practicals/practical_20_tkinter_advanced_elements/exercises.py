# Упражнения для практического занятия 20: Tkinter - продвинутые элементы

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
import random
from typing import Dict, Any, List
import json

# Задание 1: Treeview
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

# Задание 2: Progressbar
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

# Задание 3: Notebook
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
        if current_tab:  # Не удаляем, если это последняя вкладка
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

# Задание 4: PanedWindow
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
        
        # Кнопка для изменения пропорций
        ttk.Button(self.root, text="Сбросить пропорции", command=self.reset_proportions).pack(pady=5)
    
    def reset_proportions(self):
        """Сбрасывает пропорции панелей"""
        # Сбрасываем веса для восстановления начальных пропорций
        self.main_paned.forget(0)  # Удаляем левую панель
        self.main_paned.forget(0)  # Удаляем правую панель
        
        # Восстанавливаем панели с начальными весами
        left_frame = self.main_paned.pane(0)['widget']  # Получаем виджет левой панели
        right_frame = self.main_paned.pane(0)['widget']  # Получаем виджет правой панели
        
        self.main_paned.insert(0, left_frame, weight=1)
        self.main_paned.insert(1, right_frame, weight=2)
    
    def run(self):
        self.root.mainloop()

# Задание 5: Комплексное приложение "Менеджер задач"
class TaskManagerApp:
    """Комплексное приложение - Менеджер задач"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Задание 5: Менеджер задач")
        self.root.geometry("1000x700")
        
        # Данные задач
        self.tasks = [
            {"id": 1, "title": "Создать проект", "priority": "Высокий", "status": "В процессе", "progress": 75},
            {"id": 2, "title": "Написать документацию", "priority": "Средний", "status": "Ожидает", "progress": 0},
            {"id": 3, "title": "Тестирование", "priority": "Высокий", "status": "Завершено", "progress": 100},
            {"id": 4, "title": "Развертывание", "priority": "Низкий", "status": "Ожидает", "progress": 0}
        ]
        
        # Создаем меню
        self.create_menu()
        
        # Создаем основной интерфейс
        self.create_main_interface()
        
        # Создаем нижнюю панель статуса
        self.status_bar = ttk.Label(self.root, text="Готово", relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_menu(self):
        """Создает меню приложения"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Меню File
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Сохранить", command=self.save_tasks)
        file_menu.add_command(label="Загрузить", command=self.load_tasks)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        
        # Меню Edit
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Правка", menu=edit_menu)
        edit_menu.add_command(label="Добавить задачу", command=self.add_task_dialog)
        edit_menu.add_command(label="Удалить задачу", command=self.remove_task)
        edit_menu.add_command(label="Редактировать задачу", command=self.edit_task)
    
    def create_main_interface(self):
        """Создает основной интерфейс приложения"""
        # Основной PanedWindow
        main_paned = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Левая панель для фильтров
        filter_frame = ttk.LabelFrame(main_paned, text="Фильтры")
        main_paned.add(filter_frame, weight=1)
        
        # Фильтры
        ttk.Label(filter_frame, text="Приоритет:").pack(anchor=tk.W, pady=(10, 5))
        self.priority_filter = tk.StringVar(value="Все")
        priorities = ["Все", "Низкий", "Средний", "Высокий"]
        for priority in priorities:
            ttk.Radiobutton(filter_frame, text=priority, variable=self.priority_filter, 
                           value=priority, command=self.apply_filters).pack(anchor=tk.W)
        
        ttk.Label(filter_frame, text="Статус:").pack(anchor=tk.W, pady=(10, 5))
        self.status_filter = tk.StringVar(value="Все")
        statuses = ["Все", "Ожидает", "В процессе", "Завершено"]
        for status in statuses:
            ttk.Radiobutton(filter_frame, text=status, variable=self.status_filter, 
                           value=status, command=self.apply_filters).pack(anchor=tk.W)
        
        # Кнопка обновления
        ttk.Button(filter_frame, text="Сбросить фильтры", command=self.reset_filters).pack(pady=10)
        
        # Правая панель для основного содержимого
        content_frame = ttk.Frame(main_paned)
        main_paned.add(content_frame, weight=3)
        
        # Notebook для различных представлений
        self.notebook = ttk.Notebook(content_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Вкладка списка задач
        self.task_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.task_tab, text="Список задач")
        
        # Treeview для задач
        tree_frame = ttk.Frame(self.task_tab)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        tree_scrollbar = ttk.Scrollbar(tree_frame)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.task_tree = ttk.Treeview(tree_frame, columns=("Priority", "Status", "Progress"), 
                                     show="tree headings", yscrollcommand=tree_scrollbar.set)
        self.task_tree.heading("#0", text="Название")
        self.task_tree.heading("Priority", text="Приоритет")
        self.task_tree.heading("Status", text="Статус")
        self.task_tree.heading("Progress", text="Прогресс")
        self.task_tree.column("#0", width=200)
        self.task_tree.column("Priority", width=100)
        self.task_tree.column("Status", width=100)
        self.task_tree.column("Progress", width=100)
        
        self.task_tree.pack(fill=tk.BOTH, expand=True)
        tree_scrollbar.config(command=self.task_tree.yview)
        
        # Привязываем событие выбора
        self.task_tree.bind("<<TreeviewSelect>>", self.on_task_select)
        
        # Кнопки управления задачами
        button_frame = ttk.Frame(self.task_tab)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Добавить", command=self.add_task_dialog).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Редактировать", command=self.edit_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Удалить", command=self.remove_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Обновить", command=self.refresh_tasks).pack(side=tk.LEFT, padx=5)
        
        # Вкладка диаграммы
        chart_tab = ttk.Frame(self.notebook)
        self.notebook.add(chart_tab, text="Диаграмма прогресса")
        
        # Простая визуализация прогресса
        chart_frame = ttk.LabelFrame(chart_tab, text="Визуализация прогресса")
        chart_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.progress_chart = tk.Canvas(chart_frame, bg="white", height=400)
        self.progress_chart.pack(fill=tk.BOTH, expand=True)
        
        # Обновляем отображение
        self.refresh_tasks()
    
    def add_task_dialog(self):
        """Диалог добавления задачи"""
        # Создаем новое окно для добавления задачи
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавить задачу")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Поля ввода
        ttk.Label(dialog, text="Название:").pack(anchor=tk.W, padx=10, pady=5)
        title_entry = ttk.Entry(dialog)
        title_entry.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(dialog, text="Приоритет:").pack(anchor=tk.W, padx=10, pady=5)
        priority_var = tk.StringVar(value="Средний")
        priority_combo = ttk.Combobox(dialog, textvariable=priority_var, 
                                    values=["Низкий", "Средний", "Высокий"])
        priority_combo.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(dialog, text="Статус:").pack(anchor=tk.W, padx=10, pady=5)
        status_var = tk.StringVar(value="Ожидает")
        status_combo = ttk.Combobox(dialog, textvariable=status_var, 
                                  values=["Ожидает", "В процессе", "Завершено"])
        status_combo.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(dialog, text="Прогресс (%):").pack(anchor=tk.W, padx=10, pady=5)
        progress_var = tk.IntVar(value=0)
        progress_scale = ttk.Scale(dialog, from_=0, to=100, variable=progress_var, 
                                  orient=tk.HORIZONTAL)
        progress_scale.pack(fill=tk.X, padx=10, pady=5)
        
        # Кнопки
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, pady=20)
        
        def save_task():
            title = title_entry.get().strip()
            if not title:
                messagebox.showerror("Ошибка", "Название задачи не может быть пустым")
                return
            
            new_task = {
                "id": max([task["id"] for task in self.tasks], default=0) + 1,
                "title": title,
                "priority": priority_var.get(),
                "status": status_var.get(),
                "progress": progress_var.get()
            }
            
            self.tasks.append(new_task)
            self.refresh_tasks()
            dialog.destroy()
        
        ttk.Button(button_frame, text="Сохранить", command=save_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Отмена", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def remove_task(self):
        """Удаляет выбранную задачу"""
        selected = self.task_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите задачу для удаления")
            return
        
        # Получаем ID задачи из текста элемента
        item = self.task_tree.item(selected[0])
        task_title = item['text']
        
        # Найдем задачу по названию
        for i, task in enumerate(self.tasks):
            if task['title'] == task_title:
                del self.tasks[i]
                break
        
        self.refresh_tasks()
    
    def edit_task(self):
        """Редактирует выбранную задачу"""
        selected = self.task_tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите задачу для редактирования")
            return
        
        # Получаем данные задачи
        item = self.task_tree.item(selected[0])
        task_title = item['text']
        
        # Найдем задачу по названию
        task = None
        for t in self.tasks:
            if t['title'] == task_title:
                task = t
                break
        
        if not task:
            return
        
        # Открываем диалог редактирования
        self.open_edit_dialog(task)
    
    def open_edit_dialog(self, task):
        """Открывает диалог редактирования задачи"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Редактировать задачу")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Поля ввода с текущими значениями
        ttk.Label(dialog, text="Название:").pack(anchor=tk.W, padx=10, pady=5)
        title_entry = ttk.Entry(dialog)
        title_entry.insert(0, task['title'])
        title_entry.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(dialog, text="Приоритет:").pack(anchor=tk.W, padx=10, pady=5)
        priority_var = tk.StringVar(value=task['priority'])
        priority_combo = ttk.Combobox(dialog, textvariable=priority_var, 
                                    values=["Низкий", "Средний", "Высокий"])
        priority_combo.set(task['priority'])
        priority_combo.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(dialog, text="Статус:").pack(anchor=tk.W, padx=10, pady=5)
        status_var = tk.StringVar(value=task['status'])
        status_combo = ttk.Combobox(dialog, textvariable=status_var, 
                                  values=["Ожидает", "В процессе", "Завершено"])
        status_combo.set(task['status'])
        status_combo.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(dialog, text="Прогресс (%):").pack(anchor=tk.W, padx=10, pady=5)
        progress_var = tk.IntVar(value=task['progress'])
        progress_scale = ttk.Scale(dialog, from_=0, to=100, variable=progress_var, 
                                  orient=tk.HORIZONTAL)
        progress_scale.pack(fill=tk.X, padx=10, pady=5)
        
        # Кнопки
        button_frame = ttk.Frame(dialog)
        button_frame.pack(fill=tk.X, pady=20)
        
        def update_task():
            title = title_entry.get().strip()
            if not title:
                messagebox.showerror("Ошибка", "Название задачи не может быть пустым")
                return
            
            task['title'] = title
            task['priority'] = priority_var.get()
            task['status'] = status_var.get()
            task['progress'] = progress_var.get()
            
            self.refresh_tasks()
            dialog.destroy()
        
        ttk.Button(button_frame, text="Сохранить", command=update_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Отмена", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def on_task_select(self, event):
        """Обработка выбора задачи"""
        selected = self.task_tree.selection()
        if selected:
            item = self.task_tree.item(selected[0])
            self.status_bar.config(text=f"Выбрана задача: {item['text']}")
    
    def refresh_tasks(self):
        """Обновляет отображение задач"""
        # Очищаем дерево
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        # Добавляем задачи
        for task in self.filtered_tasks():
            self.task_tree.insert("", tk.END, text=task['title'], 
                                values=(task['priority'], task['status'], f"{task['progress']}%"))
        
        # Обновляем диаграмму
        self.update_chart()
    
    def filtered_tasks(self):
        """Возвращает отфильтрованные задачи"""
        priority = self.priority_filter.get()
        status = self.status_filter.get()
        
        filtered = self.tasks
        
        if priority != "Все":
            filtered = [task for task in filtered if task['priority'] == priority]
        
        if status != "Все":
            filtered = [task for task in filtered if task['status'] == status]
        
        return filtered
    
    def apply_filters(self):
        """Применяет фильтры"""
        self.refresh_tasks()
    
    def reset_filters(self):
        """Сбрасывает фильтры"""
        self.priority_filter.set("Все")
        self.status_filter.set("Все")
        self.refresh_tasks()
    
    def update_chart(self):
        """Обновляет диаграмму прогресса"""
        self.progress_chart.delete("all")
        
        if not self.tasks:
            self.progress_chart.create_text(200, 200, text="Нет задач для отображения", 
                                          font=("Arial", 14), fill="gray")
            return
        
        # Подсчитываем статусы задач
        statuses = {"Ожидает": 0, "В процессе": 0, "Завершено": 0}
        for task in self.tasks:
            statuses[task['status']] += 1
        
        # Рисуем круговую диаграмму
        total = len(self.tasks)
        if total == 0:
            return
        
        center_x, center_y = 200, 200
        radius = 100
        
        colors = {"Ожидает": "yellow", "В процессе": "orange", "Завершено": "green"}
        start_angle = 0
        
        for status, count in statuses.items():
            if count == 0:
                continue
            
            angle = 360 * count / total
            self.progress_chart.create_arc(
                center_x - radius, center_y - radius,
                center_x + radius, center_y + radius,
                start=start_angle, extent=angle,
                fill=colors[status], outline="black"
            )
            
            # Добавляем текст
            text_angle = start_angle + angle/2
            radian_angle = math.radians(text_angle)
            text_x = center_x + (radius/2) * math.cos(radian_angle)
            text_y = center_y + (radius/2) * math.sin(radian_angle)
            
            self.progress_chart.create_text(text_x, text_y, text=f"{status}: {count}", 
                                          fill="white", font=("Arial", 10, "bold"))
            
            start_angle += angle
        
        # Добавляем легенду
        legend_x, legend_y = 350, 50
        for i, (status, color) in enumerate(colors.items()):
            self.progress_chart.create_rectangle(legend_x, legend_y + i*30, 
                                               legend_x + 20, legend_y + i*30 + 20, 
                                               fill=color, outline="black")
            self.progress_chart.create_text(legend_x + 30, legend_y + i*30 + 10, 
                                          text=f"{status}: {statuses[status]}/{total}", 
                                          anchor=tk.W)
    
    def save_tasks(self):
        """Сохраняет задачи в файл"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.tasks, f, ensure_ascii=False, indent=2)
                messagebox.showinfo("Сохранение", "Задачи успешно сохранены!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {str(e)}")
    
    def load_tasks(self):
        """Загружает задачи из файла"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    loaded_tasks = json.load(f)
                
                # Проверяем формат данных
                if isinstance(loaded_tasks, list):
                    self.tasks = loaded_tasks
                    self.refresh_tasks()
                    messagebox.showinfo("Загрузка", "Задачи успешно загружены!")
                else:
                    messagebox.showerror("Ошибка", "Некорректный формат файла")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {str(e)}")
    
    def run(self):
        self.root.mainloop()

# Примеры использования:
if __name__ == "__main__":
    print("=== Упражнения для практического занятия 20 ===")
    
    print("\n1. Задание 1: Treeview")
    # tree_app = TreeviewExercise()
    # tree_app.run()  # Закомментировано для предотвращения автоматического запуска
    
    print("\n2. Задание 2: Progressbar")
    # progress_app = ProgressbarExercise()
    # progress_app.run()  # Закомментировано
    
    print("\n3. Задание 3: Notebook")
    # notebook_app = NotebookExercise()
    # notebook_app.run()  # Закомментировано
    
    print("\n4. Задание 4: PanedWindow")
    # paned_app = PanedWindowExercise()
    # paned_app.run()  # Закомментировано
    
    print("\n5. Задание 5: Комплексное приложение (Менеджер задач)")
    # task_app = TaskManagerApp()
    # task_app.run()  # Закомментировано
    
    print("\n6. Дополнительные примеры")
    # Для демонстрации запустим только одно приложение
    print("Для запуска приложений раскомментируйте соответствующие строки в коде")