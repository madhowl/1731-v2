# Примеры продвинутых виджетов Tkinter

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, colorchooser
import os
from datetime import datetime

class AdvancedWidgetsDemo:
    """
    Демонстрация продвинутых виджетов Tkinter
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Продвинутые виджеты Tkinter")
        self.root.geometry("900x700")
        
        # Создание вкладок для разных виджетов
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Создание вкладок
        self.create_tree_view_tab()
        self.create_notebook_tab()
        self.create_progress_tab()
        self.create_text_tab()
        
    def create_tree_view_tab(self):
        """
        Создание вкладки с TreeView (таблицы и иерархические данные)
        """
        tree_frame = ttk.Frame(self.notebook)
        self.notebook.add(tree_frame, text="Tree View")
        
        # Описание
        desc_label = ttk.Label(tree_frame, text="TreeView для отображения иерархических данных", 
                              font=("Arial", 12, "bold"))
        desc_label.pack(pady=10)
        
        # Создание TreeView
        columns = ("Имя", "Возраст", "Город", "Должность")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="tree headings")
        
        # Настройка заголовков
        self.tree.heading("#0", text="ID")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Добавление данных
        parent1 = self.tree.insert("", tk.END, text="Отдел 1", values=("", "", "", ""))
        parent2 = self.tree.insert("", tk.END, text="Отдел 2", values=("", "", "", ""))
        
        # Добавление дочерних элементов
        self.tree.insert(parent1, tk.END, text="Сотрудник 1", values=("Иван Иванов", "30", "Москва", "Программист"))
        self.tree.insert(parent1, tk.END, text="Сотрудник 2", values=("Мария Петрова", "25", "СПб", "Дизайнер"))
        self.tree.insert(parent2, tk.END, text="Сотрудник 3", values=("Алексей Сидоров", "35", "Новосибирск", "Менеджер"))
        
        # Добавление прокрутки
        tree_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 5), pady=5)
        
        # Кнопки управления
        button_frame = ttk.Frame(tree_frame)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Добавить элемент", 
                  command=self.add_tree_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Удалить элемент", 
                  command=self.delete_tree_item).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Очистить", 
                  command=self.clear_tree).pack(side=tk.LEFT, padx=5)
    
    def create_notebook_tab(self):
        """
        Создание вкладки с Notebook (внутренние вкладки)
        """
        notebook_frame = ttk.Frame(self.notebook)
        self.notebook.add(notebook_frame, text="Notebook")
        
        # Внутренний notebook
        inner_notebook = ttk.Notebook(notebook_frame)
        inner_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Создание внутренних вкладок
        for i in range(1, 5):
            tab = ttk.Frame(inner_notebook)
            inner_notebook.add(tab, text=f"Вкладка {i}")
            
            label = ttk.Label(tab, text=f"Содержимое вкладки {i}", font=("Arial", 14))
            label.pack(pady=50)
            
            # Добавим немного интерактивности
            button = ttk.Button(tab, text=f"Кнопка на вкладке {i}", 
                               command=lambda x=i: self.notebook_button_click(x))
            button.pack(pady=10)
    
    def create_progress_tab(self):
        """
        Создание вкладки с прогресс барами
        """
        progress_frame = ttk.Frame(self.notebook)
        self.notebook.add(progress_frame, text="Прогресс")
        
        # Описание
        desc_label = ttk.Label(progress_frame, text="Примеры использования прогресс баров", 
                              font=("Arial", 12, "bold"))
        desc_label.pack(pady=10)
        
        # Determinate прогресс бар
        ttk.Label(progress_frame, text="Определенный прогресс (determinate):").pack(anchor="w", padx=20)
        self.determinate_pb = ttk.Progressbar(progress_frame, mode="determinate", length=400)
        self.determinate_pb.pack(pady=5)
        
        # Кнопки управления
        det_button_frame = ttk.Frame(progress_frame)
        det_button_frame.pack(pady=10)
        
        ttk.Button(det_button_frame, text="Начать", 
                  command=self.start_determinate_progress).pack(side=tk.LEFT, padx=5)
        ttk.Button(det_button_frame, text="Остановить", 
                  command=self.stop_progress).pack(side=tk.LEFT, padx=5)
        ttk.Button(det_button_frame, text="Сбросить", 
                  command=self.reset_progress).pack(side=tk.LEFT, padx=5)
        
        # Indeterminate прогресс бар
        ttk.Label(progress_frame, text="Неопределенный прогресс (indeterminate):").pack(anchor="w", padx=20, pady=(20, 0))
        self.indeterminate_pb = ttk.Progressbar(progress_frame, mode="indeterminate", length=400)
        self.indeterminate_pb.pack(pady=5)
        
        ind_button_frame = ttk.Frame(progress_frame)
        ind_button_frame.pack(pady=10)
        
        ttk.Button(ind_button_frame, text="Начать анимацию", 
                  command=self.start_indeterminate_progress).pack(side=tk.LEFT, padx=5)
        ttk.Button(ind_button_frame, text="Остановить", 
                  command=self.stop_progress).pack(side=tk.LEFT, padx=5)
        
        # Скачка с прогрессом выполнения задачи
        ttk.Label(progress_frame, text="Прогресс выполнения задачи:").pack(anchor="w", padx=20, pady=(20, 0))
        self.task_pb = ttk.Progressbar(progress_frame, mode="determinate", length=400)
        self.task_pb.pack(pady=5)
        
        ttk.Button(progress_frame, text="Выполнить задачу", 
                  command=self.simulate_task).pack(pady=10)
    
    def create_text_tab(self):
        """
        Создание вкладки с расширенным текстовым редактором
        """
        text_frame = ttk.Frame(self.notebook)
        self.notebook.add(text_frame, text="Текстовый редактор")
        
        # Создание текстового редактора с прокруткой
        text_editor_frame = ttk.Frame(text_frame)
        text_editor_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Текстовая область
        self.text_area = tk.Text(
            text_editor_frame,
            wrap=tk.WORD,
            undo=True,
            font=("Consolas", 11)
        )
        
        # Прокрутки
        v_scrollbar = ttk.Scrollbar(text_editor_frame, orient=tk.VERTICAL, command=self.text_area.yview)
        h_scrollbar = ttk.Scrollbar(text_editor_frame, orient=tk.HORIZONTAL, command=self.text_area.xview)
        
        self.text_area.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        self.text_area.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Настройка растягивания сетки
        text_editor_frame.grid_rowconfigure(0, weight=1)
        text_editor_frame.grid_columnconfigure(0, weight=1)
        
        # Панель инструментов
        toolbar = ttk.Frame(text_frame)
        toolbar.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(toolbar, text="Открыть", command=self.open_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Сохранить", command=self.save_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Очистить", command=self.clear_text).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Шрифт", command=self.change_font).pack(side=tk.LEFT, padx=2)
        
        # Добавим немного текста для примера
        sample_text = "\n".join([
            "Это пример расширенного текстового редактора.",
            "",
            "Здесь вы можете:",
            "1. Вводить и редактировать текст",
            "2. Использовать прокрутку для навигации",
            "3. Открывать и сохранять файлы",
            "4. Менять шрифт и размер",
            "",
            "Этот редактор поддерживает отмену действий (Ctrl+Z) и повтор (Ctrl+Y).",
            "Также доступны горизонтальная и вертикальная прокрутка."
        ])
        
        self.text_area.insert("1.0", sample_text)
    
    def add_tree_item(self):
        """
        Добавление элемента в TreeView
        """
        # В реальном приложении здесь открывалось бы диалоговое окно для ввода данных
        item_id = self.tree.insert("", tk.END, text="Новый элемент", 
                                  values=("Имя", "25", "Город", "Должность"))
        messagebox.showinfo("Добавление", f"Элемент с ID {item_id} добавлен")
    
    def delete_tree_item(self):
        """
        Удаление выбранного элемента из TreeView
        """
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.delete(selected_item)
            messagebox.showinfo("Удаление", "Элемент удален")
        else:
            messagebox.showwarning("Удаление", "Сначала выберите элемент для удаления")
    
    def clear_tree(self):
        """
        Очистка всех элементов из TreeView
        """
        for item in self.tree.get_children():
            self.tree.delete(item)
        messagebox.showinfo("Очистка", "Все элементы удалены")
    
    def notebook_button_click(self, tab_number):
        """
        Обработчик нажатия кнопки на внутренней вкладке
        """
        messagebox.showinfo("Информация", f"Нажата кнопка на вкладке {tab_number}")
    
    def start_determinate_progress(self):
        """
        Запуск определенного прогресса
        """
        import threading
        self.determinate_pb['value'] = 0
        threading.Thread(target=self.update_progress, daemon=True).start()
    
    def update_progress(self):
        """
        Обновление прогресса в отдельном потоке
        """
        for i in range(101):
            self.root.after(0, lambda val=i: self.determinate_pb.config(value=val))
            self.root.update_idletasks()
            import time
            time.sleep(0.05)
    
    def start_indeterminate_progress(self):
        """
        Запуск неопределенного прогресса
        """
        self.indeterminate_pb.start(10)
    
    def stop_progress(self):
        """
        Остановка всех прогресс баров
        """
        self.determinate_pb.stop()
        self.indeterminate_pb.stop()
        self.task_pb.stop()
    
    def reset_progress(self):
        """
        Сброс всех прогресс баров
        """
        self.determinate_pb['value'] = 0
        self.task_pb['value'] = 0
    
    def simulate_task(self):
        """
        Симуляция выполнения задачи с прогрессом
        """
        import threading
        self.task_pb['value'] = 0
        
        def task_simulation():
            for i in range(101):
                self.root.after(0, lambda val=i: self.task_pb.config(value=val))
                import time
                time.sleep(0.03)
        
        threading.Thread(target=task_simulation, daemon=True).start()
    
    def open_file(self):
        """
        Открытие файла в текстовом редакторе
        """
        file_path = filedialog.askopenfilename(
            title="Открыть файл",
            filetypes=[
                ("Текстовые файлы", "*.txt"),
                ("Python файлы", "*.py"),
                ("Все файлы", "*.*")
            ]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert("1.0", content)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось открыть файл:\n{str(e)}")
    
    def save_file(self):
        """
        Сохранение содержимого текстового редактора
        """
        file_path = filedialog.asksaveasfilename(
            title="Сохранить файл",
            defaultextension=".txt",
            filetypes=[
                ("Текстовые файлы", "*.txt"),
                ("Python файлы", "*.py"),
                ("Все файлы", "*.*")
            ]
        )
        
        if file_path:
            try:
                content = self.text_area.get("1.0", tk.END + "-1c")  # -1c удаляет последнюю пустую строку
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                
                messagebox.showinfo("Сохранение", "Файл успешно сохранен")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")
    
    def clear_text(self):
        """
        Очистка текстовой области
        """
        if messagebox.askyesno("Очистка", "Вы уверены, что хотите очистить текстовую область?"):
            self.text_area.delete("1.0", tk.END)
    
    def change_font(self):
        """
        Изменение шрифта текстовой области
        """
        # Простая реализация выбора шрифта
        fonts = ["Arial", "Times New Roman", "Consolas", "Courier New", "Verdana"]
        font_sizes = [8, 10, 11, 12, 14, 16, 18, 20]
        
        # В реальном приложении здесь было бы диалоговое окно выбора шрифта
        current_font = self.text_area.cget("font").split()
        current_family = current_font[0] if current_font else "Arial"
        current_size = int(current_font[1]) if len(current_font) > 1 else 11
        
        # Просто увеличим размер шрифта на 2 пункта
        new_size = current_size + 2 if current_size < 20 else 8
        self.text_area.config(font=(current_family, new_size))
    
    def run(self):
        """
        Запуск приложения
        """
        self.root.mainloop()

class CustomWidgetsDemo:
    """
    Демонстрация создания пользовательских виджетов
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("Пользовательские виджеты")
        self.root.geometry("800x600")
        
        self.create_custom_widgets()
    
    def create_custom_widgets(self):
        """
        Создание пользовательских виджетов
        """
        # Создание фрейма для пользовательских виджетов
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="Пользовательские виджеты", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Кастомный виджет: цветной фрейм с меткой
        color_frame = self.create_color_frame(main_frame, "Красный фрейм", "red", 1)
        color_frame.pack(fill=tk.X, pady=5)
        
        color_frame = self.create_color_frame(main_frame, "Зеленый фрейм", "green", 2)
        color_frame.pack(fill=tk.X, pady=5)
        
        color_frame = self.create_color_frame(main_frame, "Синий фрейм", "blue", 3)
        color_frame.pack(fill=tk.X, pady=5)
        
        # Кастомный виджет: счётчик
        counter_frame = self.create_counter(main_frame, "Счётчик:")
        counter_frame.pack(fill=tk.X, pady=20)
        
        # Кастомный виджет: поле ввода с валидацией
        validation_frame = self.create_validated_input(main_frame, "Email:")
        validation_frame.pack(fill=tk.X, pady=5)
    
    def create_color_frame(self, parent, text, color, number):
        """
        Создание цветного фрейма с меткой и кнопкой
        """
        frame = ttk.Frame(parent)
        
        # Метка с цветным фоном
        label = tk.Label(frame, text=text, bg=color, fg="white", width=20)
        label.pack(side=tk.LEFT, padx=(0, 10))
        
        # Кнопка с обратным вызовом
        button = ttk.Button(frame, text=f"Кнопка {number}", 
                           command=lambda: self.custom_widget_action(text))
        button.pack(side=tk.LEFT)
        
        return frame
    
    def create_counter(self, parent, label_text):
        """
        Создание виджета счётчика
        """
        frame = ttk.Frame(parent)
        
        ttk.Label(frame, text=label_text).pack(side=tk.LEFT, padx=(0, 10))
        
        self.counter_var = tk.IntVar(value=0)
        counter_label = ttk.Label(frame, textvariable=self.counter_var, width=10, 
                                 relief="sunken", anchor="center")
        counter_label.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(frame, text="+", width=5, 
                  command=lambda: self.counter_var.set(self.counter_var.get() + 1)).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame, text="-", width=5, 
                  command=lambda: self.counter_var.set(self.counter_var.get() - 1)).pack(side=tk.LEFT, padx=2)
        ttk.Button(frame, text="Сброс", width=7, 
                  command=lambda: self.counter_var.set(0)).pack(side=tk.LEFT, padx=2)
        
        return frame
    
    def create_validated_input(self, parent, label_text):
        """
        Создание поля ввода с валидацией
        """
        frame = ttk.Frame(parent)
        
        ttk.Label(frame, text=label_text).pack(side=tk.LEFT, padx=(0, 10))
        
        self.email_var = tk.StringVar()
        email_entry = ttk.Entry(frame, textvariable=self.email_var, width=30)
        email_entry.pack(side=tk.LEFT, padx=5)
        
        # Добавим валидацию при изменении
        self.email_var.trace('w', self.validate_email)
        
        self.email_status = ttk.Label(frame, text="✓", foreground="green")
        self.email_status.pack(side=tk.LEFT, padx=5)
        
        return frame
    
    def validate_email(self, *args):
        """
        Простая валидация email
        """
        email = self.email_var.get()
        if "@" in email and "." in email.split("@")[-1]:
            self.email_status.config(text="✓", foreground="green")
        else:
            self.email_status.config(text="✗", foreground="red")
    
    def custom_widget_action(self, widget_name):
        """
        Обработчик действий пользовательских виджетов
        """
        messagebox.showinfo("Действие", f"Нажата кнопка в {widget_name}")

def main():
    """
    Основная функция демонстрации
    """
    root = tk.Tk()
    app = AdvancedWidgetsDemo(root)
    app.run()

if __name__ == "__main__":
    main()
