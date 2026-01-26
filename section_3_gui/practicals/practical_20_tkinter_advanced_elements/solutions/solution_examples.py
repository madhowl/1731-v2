# Решения для практического занятия 20: Tkinter - продвинутые элементы

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import time
import random
from typing import Dict, Any, List
import json
import math

# Решение задания 1: Treeview
class TreeviewSolution:
    """Решение для задания 1: Treeview"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Решение задания 1: Treeview")
        self.root.geometry("900x700")
        
        # Создаем Treeview с прокруткой
        tree_frame = ttk.Frame(self.root)
        tree_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Горизонтальная и вертикальная прокрутка
        tree_vertical_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        tree_vertical_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        tree_horizontal_scrollbar = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        tree_horizontal_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.tree = ttk.Treeview(tree_frame, 
                                yscrollcommand=tree_vertical_scrollbar.set,
                                xscrollcommand=tree_horizontal_scrollbar.set)
        
        # Определяем колонки
        self.tree['columns'] = ("Имя", "Возраст", "Должность", "Зарплата", "Отдел")
        
        # Форматируем колонки
        self.tree.column("#0", width=0, stretch=tk.NO)  # Скрытая колонка
        self.tree.column("Имя", anchor=tk.W, width=120)
        self.tree.column("Возраст", anchor=tk.CENTER, width=60)
        self.tree.column("Должность", anchor=tk.W, width=150)
        self.tree.column("Зарплата", anchor=tk.E, width=100)
        self.tree.column("Отдел", anchor=tk.W, width=120)
        
        # Создаем заголовки
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.heading("Имя", text="Имя", anchor=tk.W)
        self.tree.heading("Возраст", text="Возраст", anchor=tk.W)
        self.tree.heading("Должность", text="Должность", anchor=tk.W)
        self.tree.heading("Зарплата", text="Зарплата", anchor=tk.W)
        self.tree.heading("Отдел", text="Отдел", anchor=tk.W)
        
        # Добавляем данные
        self.add_sample_data()
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        tree_vertical_scrollbar.config(command=self.tree.yview)
        tree_horizontal_scrollbar.config(command=self.tree.xview)
        
        # Кнопки управления
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Добавить", command=self.add_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Удалить", command=self.remove_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Редактировать", command=self.edit_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Сортировать по имени", command=lambda: self.sort_column("Имя")).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Контекстное меню", command=self.show_context_menu).pack(side=tk.LEFT, padx=5)
        
        # Привязываем события
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.bind("<Double-Button-1>", self.on_double_click)
        self.tree.bind("<Button-3>", self.show_context_menu)
    
    def add_sample_data(self):
        """Добавляет образцы данных в дерево"""
        # Добавляем элементы верхнего уровня (отделы)
        hr_dept = self.tree.insert("", tk.END, text="Отдел HR", values=("", "", "HR", "", "HR"))
        dev_dept = self.tree.insert("", tk.END, text="Отдел разработки", values=("", "", "Dev", "", "Dev"))
        sales_dept = self.tree.insert("", tk.END, text="Отдел продаж", values=("", "", "Sales", "", "Sales"))
        mgmt_dept = self.tree.insert("", tk.END, text="Менеджмент", values=("", "", "Management", "", "Mgmt"))
        
        # Добавляем сотрудников в отделы
        employees = [
            ("Иванов Иван", 30, "Менеджер", 120000, "HR"),
            ("Петрова Мария", 28, "Ассистент", 80000, "HR"),
            ("Сидоров Алексей", 35, "Старший менеджер", 150000, "HR")
        ]
        for emp in employees:
            self.tree.insert(hr_dept, tk.END, values=emp)
        
        employees = [
            ("Сидоров Алексей", 35, "Старший разработчик", 150000, "Dev"),
            ("Козлова Елена", 26, "Младший разработчик", 90000, "Dev"),
            ("Морозов Дмитрий", 32, "Архитектор", 200000, "Dev"),
            ("Волков Андрей", 29, "Тестировщик", 100000, "Dev"),
            ("Кузнецова Ольга", 27, "Frontend-разработчик", 130000, "Dev")
        ]
        for emp in employees:
            self.tree.insert(dev_dept, tk.END, values=emp)
        
        employees = [
            ("Волкова Анна", 29, "Менеджер по продажам", 110000, "Sales"),
            ("Никитин Сергей", 31, "Директор по продажам", 180000, "Sales"),
            ("Макарова Татьяна", 26, "Специалист по работе с клиентами", 85000, "Sales")
        ]
        for emp in employees:
            self.tree.insert(sales_dept, tk.END, values=emp)
        
        employees = [
            ("Козлов Михаил", 45, "Генеральный директор", 500000, "Mgmt"),
            ("Лебедева Юлия", 42, "Финансовый директор", 400000, "Mgmt"),
            ("Семенов Игорь", 40, "Технический директор", 450000, "Mgmt")
        ]
        for emp in employees:
            self.tree.insert(mgmt_dept, tk.END, values=emp)
    
    def add_item(self):
        """Добавляет новый элемент"""
        # В реальном приложении здесь был бы диалог добавления
        selected = self.tree.selection()
        if selected:
            parent = selected[0]
        else:
            parent = ""
        
        new_emp = (f"Новый Сотрудник {len(self.tree.get_children())}", 
                  random.randint(22, 60), "Стажер", 60000, "HR")
        self.tree.insert(parent, tk.END, values=new_emp)
    
    def remove_item(self):
        """Удаляет выбранный элемент"""
        selected = self.tree.selection()
        if selected:
            # Проверяем, является ли элемент родительским
            if self.tree.get_children(selected[0]):  # Если у элемента есть дети
                if messagebox.askyesno("Подтверждение", "Удалить элемент вместе с дочерними элементами?"):
                    self.tree.delete(selected[0])
            else:
                self.tree.delete(selected[0])
    
    def edit_item(self):
        """Редактирует выбранный элемент"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Предупреждение", "Выберите элемент для редактирования")
            return
        
        item = self.tree.item(selected[0])
        values = item['values']
        
        # Создаем диалог редактирования
        dialog = tk.Toplevel(self.root)
        dialog.title("Редактировать элемент")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Поля ввода
        fields = ["Имя", "Возраст", "Должность", "Зарплата", "Отдел"]
        entries = {}
        
        for i, field in enumerate(fields):
            ttk.Label(dialog, text=field + ":").grid(row=i, column=0, sticky=tk.W, padx=5, pady=5)
            entry = ttk.Entry(dialog)
            entry.grid(row=i, column=1, sticky=tk.EW, padx=5, pady=5)
            entries[field] = entry
            
            # Устанавливаем текущие значения
            if i < len(values):
                entry.insert(0, values[i])
        
        # Растягиваем колонки
        dialog.columnconfigure(1, weight=1)
        
        # Кнопки
        button_frame = ttk.Frame(dialog)
        button_frame.grid(row=len(fields), column=0, columnspan=2, pady=10)
        
        def save_changes():
            new_values = [entries[field].get() for field in fields]
            self.tree.item(selected[0], values=new_values)
            dialog.destroy()
        
        ttk.Button(button_frame, text="Сохранить", command=save_changes).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Отмена", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
    
    def sort_column(self, col):
        """Сортирует колонку"""
        # Получаем все элементы
        children = self.tree.get_children()
        # Сортируем по значению в колонке
        values_with_items = []
        for child in children:
            val = self.tree.set(child, col)
            # Для числовых значений преобразуем для корректной сортировки
            try:
                numeric_val = float(val)
                values_with_items.append((numeric_val, child))
            except ValueError:
                # Для текстовых значений используем строку
                values_with_items.append((val, child))
        
        # Сортируем значения
        values_with_items.sort(key=lambda x: x[0])
        
        # Переставляем элементы в отсортированном порядке
        for i, (_, child) in enumerate(values_with_items):
            self.tree.move(child, '', i)
    
    def show_context_menu(self, event=None):
        """Показывает контекстное меню"""
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="Добавить", command=self.add_item)
        menu.add_command(label="Удалить", command=self.remove_item)
        menu.add_command(label="Редактировать", command=self.edit_item)
        menu.add_separator()
        menu.add_command(label="Сортировать по возрасту", command=lambda: self.sort_column("Возраст"))
        menu.add_command(label="Сортировать по зарплате", command=lambda: self.sort_column("Зарплата"))
        
        if event:
            menu.post(event.x_root, event.y_root)
        else:
            # Если событие не передано, показываем меню в центре виджета
            x = self.tree.winfo_rootx() + self.tree.winfo_width() // 2
            y = self.tree.winfo_rooty() + self.tree.winfo_height() // 2
            menu.post(x, y)
    
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

# Решение задания 2: Progressbar
class ProgressbarSolution:
    """Решение для задания 2: Progressbar"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Решение задания 2: Progressbar")
        self.root.geometry("800x700")
        
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
        ttk.Button(multi_buttons, text="Разное заполнение", command=self.fill_different).pack(side=tk.LEFT, padx=5)
        
        # Индикатор выполнения
        self.status_label = ttk.Label(main_frame, text="Готово", foreground="green")
        self.status_label.pack(pady=5)
        
        # Кнопка для демонстрации индикации выполнения длительной операции
        ttk.Button(main_frame, text="Длительная операция", command=self.long_operation).pack(pady=5)
    
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
    
    def fill_different(self):
        """Заполняет прогресс бары по-разному"""
        def fill_bars():
            for i, pb in enumerate(self.progress_bars):
                for j in range(0, 101, 5):
                    pb['value'] = j
                    self.root.update()
                    time.sleep(0.01 + i * 0.005)  # Разное время для каждого бара
        
        thread = threading.Thread(target=fill_bars)
        thread.daemon = True
        thread.start()
    
    def long_operation(self):
        """Демонстрирует длительную операцию с прогресс баром"""
        def simulate_long_operation():
            # Показываем неопределенный прогресс бар
            self.indeterminate_pb.start(10)
            self.status_label.config(text="Выполняется длительная операция...", foreground="red")
            
            # Имитируем длительную операцию
            time.sleep(3)
            
            # Останавливаем неопределенный прогресс бар
            self.indeterminate_pb.stop()
            self.status_label.config(text="Операция завершена", foreground="green")
        
        thread = threading.Thread(target=simulate_long_operation)
        thread.daemon = True
        thread.start()
    
    def run(self):
        self.root.mainloop()

# Решение задания 3: Notebook
class NotebookSolution:
    """Решение для задания 3: Notebook"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Решение задания 3: Notebook")
        self.root.geometry("900x700")
        
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
        ttk.Button(button_frame, text="Сохранить состояние", command=self.save_state).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Загрузить состояние", command=self.load_state).pack(side=tk.LEFT, padx=5)
        
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
            "Телефон": "+7 (999) 123-45-67",
            "Должность": "Разработчик",
            "Отдел": "IT"
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
    
    def save_state(self):
        """Сохраняет состояние вкладок"""
        state = {
            'current_tab': self.notebook.index(self.notebook.select()),
            'tab_count': len(self.notebook.tabs()),
            'settings': self.settings_var.get() if hasattr(self, 'settings_var') else ''
        }
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(state, f, ensure_ascii=False, indent=2)
                messagebox.showinfo("Сохранение", "Состояние сохранено!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка сохранения: {str(e)}")
    
    def load_state(self):
        """Загружает состояние вкладок"""
        filename = filedialog.askopenfilename(
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    state = json.load(f)
                
                # Восстанавливаем текущую вкладку (если возможно)
                if state['current_tab'] < len(self.notebook.tabs()):
                    self.notebook.select(state['current_tab'])
                
                # Восстанавливаем настройки
                if hasattr(self, 'settings_var'):
                    self.settings_var.set(state.get('settings', ''))
                
                messagebox.showinfo("Загрузка", "Состояние загружено!")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка загрузки: {str(e)}")
    
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

# Решение задания 4: PanedWindow
class PanedWindowSolution:
    """Решение для задания 4: PanedWindow"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Решение задания 4: PanedWindow")
        self.root.geometry("1000x800")
        
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
            "Файл 3": "data.xlsx",
            "Папка 1": "folder/",
            "Папка 2": "project/"
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
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Сбросить пропорции", command=self.reset_proportions).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Изменить веса", command=self.change_weights).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Добавить панель", command=self.add_panel).pack(side=tk.LEFT, padx=5)
    
    def reset_proportions(self):
        """Сбрасывает пропорции панелей"""
        # Удаляем все панели
        for pane in self.main_paned.panes():
            self.main_paned.forget(pane)
        
        # Восстанавливаем с начальными весами
        left_frame = ttk.Frame(self.main_paned, width=300, height=600)
        right_frame = ttk.Frame(self.main_paned, width=600, height=600)
        
        self.main_paned.add(left_frame, weight=1)
        self.main_paned.add(right_frame, weight=2)
        
        # Восстанавливаем содержимое левой панели
        left_paned = ttk.PanedWindow(left_frame, orient=tk.VERTICAL)
        left_paned.pack(fill=tk.BOTH, expand=True)
        
        top_left = ttk.Frame(left_paned)
        left_paned.add(top_left, weight=1)
        
        ttk.Label(top_left, text="Верхняя часть левой панели", font=("Arial", 12)).pack(pady=20)
        
        listbox_frame = ttk.Frame(top_left)
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        listbox_scrollbar = ttk.Scrollbar(listbox_frame)
        listbox_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.left_listbox = tk.Listbox(listbox_frame, yscrollcommand=listbox_scrollbar.set)
        self.left_listbox.pack(fill=tk.BOTH, expand=True)
        listbox_scrollbar.config(command=self.left_listbox.yview)
        
        for i in range(20):
            self.left_listbox.insert(tk.END, f"Элемент {i+1}")
        
        bottom_left = ttk.Frame(left_paned)
        left_paned.add(bottom_left, weight=1)
        
        ttk.Label(bottom_left, text="Нижняя часть левой панели", font=("Arial", 12)).pack(pady=20)
    
    def change_weights(self):
        """Изменяет веса панелей"""
        # Удаляем и добавляем панели с новыми весами
        current_widgets = []
        for pane in self.main_paned.panes():
            widget = self.main_paned.panecget(pane, 'window')
            weight = self.main_paned.panecget(pane, 'weight')
            current_widgets.append((widget, int(weight)))
            self.main_paned.forget(pane)
        
        # Меняем веса (увеличиваем вес правой панели)
        for widget, old_weight in current_widgets:
            new_weight = old_weight * 2 if old_weight > 1 else 1
            self.main_paned.add(widget, weight=new_weight)
    
    def add_panel(self):
        """Добавляет дополнительную панель"""
        # Создаем новую панель
        new_panel = ttk.Frame(self.main_paned, width=200, height=600)
        
        # Добавляем содержимое
        ttk.Label(new_panel, text="Новая панель", font=("Arial", 12)).pack(pady=20)
        
        # Добавляем как самую правую панель
        self.main_paned.add(new_panel, weight=1)
    
    def run(self):
        self.root.mainloop()

# Решение задания 5: Комплексное приложение "Менеджер задач"
class TaskManagerSolution:
    """Решение для задания 5: Комплексное приложение - Менеджер задач"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Решение задания 5: Менеджер задач")
        self.root.geometry("1200x800")
        
        # Данные задач
        self.tasks = [
            {"id": 1, "title": "Создать проект", "priority": "Высокий", "status": "В процессе", "progress": 75},
            {"id": 2, "title": "Написать документацию", "priority": "Средний", "status": "Ожидает", "progress": 0},
            {"id": 3, "title": "Тестирование", "priority": "Высокий", "status": "Завершено", "progress": 100},
            {"id": 4, "title": "Развертывание", "priority": "Низкий", "status": "Ожидает", "progress": 0},
            {"id": 5, "title": "Обновление зависимостей", "priority": "Средний", "status": "В процессе", "progress": 30}
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

# Дополнительные примеры использования продвинутых элементов
class AdvancedElementsExamples:
    """Дополнительные примеры использования продвинутых элементов"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Дополнительные примеры продвинутых элементов")
        self.root.geometry("1000x800")
        
        # Создаем ноутбук для различных примеров
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Вкладка для Combobox с кастомным списком
        self.combobox_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.combobox_frame, text="Combobox")
        self.create_combobox_example()
        
        # Вкладка для других продвинутых элементов
        self.other_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.other_frame, text="Другие элементы")
        self.create_other_examples()
    
    def create_combobox_example(self):
        """Создает пример с кастомным Combobox"""
        frame = ttk.LabelFrame(self.combobox_frame, text="Пример кастомного Combobox")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Combobox с кастомным списком
        ttk.Label(frame, text="Выберите страну:").pack(anchor=tk.W, pady=5)
        countries = ["Россия", "США", "Канада", "Великобритания", "Германия", "Франция", "Япония", "Китай", "Индия"]
        self.country_combo = ttk.Combobox(frame, values=countries, state="normal")
        self.country_combo.pack(fill=tk.X, pady=5)
        self.country_combo.bind("<<ComboboxSelected>>", self.on_country_select)
        
        # Combobox с автозаполнением
        ttk.Label(frame, text="Введите город (с автозаполнением):").pack(anchor=tk.W, pady=(10, 5))
        cities = ["Москва", "Санкт-Петербург", "Новосибирск", "Екатеринбург", "Казань", "Нижний Новгород", "Челябинск", "Самара"]
        self.city_entry = AutocompleteCombobox(frame, values=cities)
        self.city_entry.pack(fill=tk.X, pady=5)
        
        # Кнопка для получения значений
        ttk.Button(frame, text="Получить значения", command=self.get_values).pack(pady=10)
        
        # Метка для отображения выбранных значений
        self.values_label = ttk.Label(frame, text="Выбранные значения будут здесь", foreground="blue")
        self.values_label.pack(pady=5)
    
    def on_country_select(self, event):
        """Обработка выбора страны"""
        country = self.country_combo.get()
        self.values_label.config(text=f"Выбрана страна: {country}")
    
    def get_values(self):
        """Получает значения из всех виджетов"""
        country = self.country_combo.get()
        city = self.city_entry.get()
        values_text = f"Страна: {country}, Город: {city}"
        self.values_label.config(text=values_text)
    
    def create_other_examples(self):
        """Создает примеры других продвинутых элементов"""
        frame = ttk.LabelFrame(self.other_frame, text="Другие продвинутые элементы")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Scrollbar с Canvas
        canvas_frame = ttk.Frame(frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        canvas_scrollbar = ttk.Scrollbar(canvas_frame)
        canvas_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        canvas = tk.Canvas(canvas_frame, bg="lightblue", yscrollcommand=canvas_scrollbar.set)
        canvas.pack(fill=tk.BOTH, expand=True)
        canvas_scrollbar.config(command=canvas.yview)
        
        # Добавляем много содержимого на Canvas для демонстрации прокрутки
        for i in range(50):
            canvas.create_text(100, i*30, text=f"Текстовая строка {i+1}", anchor=tk.W)
        
        # Text с продвинутыми возможностями
        text_frame = ttk.LabelFrame(frame, text="Продвинутый Text")
        text_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        text_scrollbar = ttk.Scrollbar(text_frame)
        text_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.advanced_text = tk.Text(text_frame, wrap=tk.WORD, yscrollcommand=text_scrollbar.set)
        self.advanced_text.pack(fill=tk.BOTH, expand=True)
        text_scrollbar.config(command=self.advanced_text.yview)
        
        # Добавляем пример текста с разными стилями
        sample_text = "Это пример текста с различными стилями.\n" * 20
        self.advanced_text.insert(tk.END, sample_text)
        
        # Добавляем теги для разных стилей
        self.advanced_text.tag_add("highlight", "1.0", "1.20")
        self.advanced_text.tag_config("highlight", background="yellow", foreground="black")
        
        # Кнопка для добавления тегов
        ttk.Button(frame, text="Добавить выделение", command=self.add_highlight).pack(pady=5)
    
    def add_highlight(self):
        """Добавляет выделение к выделенному тексту"""
        try:
            start = self.advanced_text.index(tk.SEL_FIRST)
            end = self.advanced_text.index(tk.SEL_LAST)
            self.advanced_text.tag_add("highlight", start, end)
            self.advanced_text.tag_config("highlight", background="yellow", foreground="black")
        except tk.TclError:
            # Нет выделенного текста
            messagebox.showinfo("Информация", "Сначала выделите текст")
    
    def run(self):
        self.root.mainloop()

class AutocompleteCombobox(ttk.Combobox):
    """Combobox с автозаполнением"""
    def __init__(self, parent, values=None, **kwargs):
        super().__init__(parent, values=values, **kwargs)
        self.values = values or []
        self.bind('<KeyRelease>', self.handle_keyrelease)
    
    def handle_keyrelease(self, event):
        """Обработка нажатия клавиш для автозаполнения"""
        if event.keysym in ['Up', 'Down', 'Return', 'Tab']:
            return
        
        current_text = self.get()
        if current_text:
            # Находим совпадения
            matches = [val for val in self.values if val.lower().startswith(current_text.lower())]
            if matches:
                # Устанавливаем первый матч как значение
                self.set(matches[0])
                # Выделяем текст после введенной части
                self.selection_range(len(current_text), tk.END)
                # Устанавливаем курсор в конец
                self.icursor(tk.END)

# Примеры использования:
if __name__ == "__main__":
    print("=== Решения для практического занятия 20 ===")
    
    print("\n1. Решение задания 1: Treeview")
    # tree_solution = TreeviewSolution()
    # tree_solution.run()  # Закомментировано для предотвращения автоматического запуска
    
    print("\n2. Решение задания 2: Progressbar")
    # progress_solution = ProgressbarSolution()
    # progress_solution.run()  # Закомментировано
    
    print("\n3. Решение задания 3: Notebook")
    # notebook_solution = NotebookSolution()
    # notebook_solution.run()  # Закомментировано
    
    print("\n4. Решение задания 4: PanedWindow")
    # paned_solution = PanedWindowSolution()
    # paned_solution.run()  # Закомментировано
    
    print("\n5. Решение задания 5: Комплексное приложение (Менеджер задач)")
    # task_solution = TaskManagerSolution()
    # task_solution.run()  # Закомментировано
    
    print("\n6. Дополнительные примеры")
    # advanced_solution = AdvancedElementsExamples()
    # advanced_solution.run()  # Закомментировано
    
    # Для демонстрации запустим только одно приложение
    print("Для запуска приложений раскомментируйте соответствующие строки в коде")