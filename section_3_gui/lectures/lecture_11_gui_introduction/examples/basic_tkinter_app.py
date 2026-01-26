# Примеры базового GUI-приложения с использованием Tkinter

import tkinter as tk
from tkinter import ttk, messagebox, filedialog

class BasicGUIApp:
    """
    Базовое GUI-приложение для демонстрации основных элементов интерфейса
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Базовое GUI-приложение")
        self.root.geometry("600x400")
        
        self.create_widgets()
    
    def create_widgets(self):
        """
        Создание основных виджетов приложения
        """
        # Создание фрейма для организации элементов
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="Добро пожаловать в GUI-приложение", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Поле ввода
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(input_frame, text="Введите текст:").pack(anchor=tk.W)
        
        self.text_entry = ttk.Entry(input_frame, width=50)
        self.text_entry.pack(fill=tk.X, pady=5)
        self.text_entry.insert(0, "Пример ввода текста")
        
        # Кнопки
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Показать сообщение", 
                  command=self.show_message).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Очистить поле", 
                  command=self.clear_field).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Выбрать файл", 
                  command=self.select_file).pack(side=tk.LEFT, padx=5)
        
        # Текстовая область
        text_frame = ttk.LabelFrame(main_frame, text="Текстовая область", padding="5")
        text_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.text_area = tk.Text(text_frame, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text_area.yview)
        self.text_area.configure(yscrollcommand=scrollbar.set)
        
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Добавим немного текста для примера
        sample_text = "Это пример текста в текстовой области.\n\nЗдесь можно вводить и редактировать многострочный текст."
        self.text_area.insert("1.0", sample_text)
    
    def show_message(self):
        """
        Показывает сообщение с содержимым поля ввода
        """
        text = self.text_entry.get()
        messagebox.showinfo("Сообщение", f"Вы ввели: {text}")
    
    def clear_field(self):
        """
        Очищает поле ввода
        """
        self.text_entry.delete(0, tk.END)
    
    def select_file(self):
        """
        Открывает диалог выбора файла
        """
        file_path = filedialog.askopenfilename(
            title="Выберите файл",
            filetypes=[
                ("Текстовые файлы", "*.txt"),
                ("Python файлы", "*.py"),
                ("Все файлы", "*.*")
            ]
        )
        if file_path:
            self.text_area.delete("1.0", tk.END)
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                self.text_area.insert("1.0", content)
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось прочитать файл:\n{str(e)}")
    
    def run(self):
        """
        Запуск приложения
        """
        self.root.mainloop()

class AdvancedGUIElements:
    """
    Примеры продвинутых элементов GUI
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Продвинутые элементы GUI")
        self.root.geometry("700x500")
        
        self.create_advanced_widgets()
    
    def create_advanced_widgets(self):
        """
        Создание продвинутых виджетов
        """
        # Создание вкладок
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Вкладка 1: Форма ввода данных
        self.create_input_form_tab(notebook)
        
        # Вкладка 2: Списки и таблицы
        self.create_list_table_tab(notebook)
        
        # Вкладка 3: Прогресс и выбор
        self.create_progress_choice_tab(notebook)
    
    def create_input_form_tab(self, parent):
        """
        Создание вкладки с формой ввода данных
        """
        form_frame = ttk.Frame(parent)
        parent.add(form_frame, text="Форма ввода")
        
        # Используем сетку для размещения элементов формы
        form_frame.columnconfigure(1, weight=1)
        
        # Имя
        ttk.Label(form_frame, text="Имя:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.name_entry = ttk.Entry(form_frame)
        self.name_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        
        # Фамилия
        ttk.Label(form_frame, text="Фамилия:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.surname_entry = ttk.Entry(form_frame)
        self.surname_entry.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        
        # Возраст
        ttk.Label(form_frame, text="Возраст:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.age_spinbox = ttk.Spinbox(form_frame, from_=1, to=120, width=10)
        self.age_spinbox.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        
        # Пол
        ttk.Label(form_frame, text="Пол:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.gender_var = tk.StringVar(value="male")
        gender_frame = ttk.Frame(form_frame)
        gender_frame.grid(row=3, column=1, sticky="w", padx=5, pady=5)
        
        ttk.Radiobutton(gender_frame, text="Мужской", variable=self.gender_var, 
                       value="male").pack(side=tk.LEFT)
        ttk.Radiobutton(gender_frame, text="Женский", variable=self.gender_var, 
                       value="female").pack(side=tk.LEFT, padx=(10, 0))
        
        # Интересы
        ttk.Label(form_frame, text="Интересы:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        interests_frame = ttk.Frame(form_frame)
        interests_frame.grid(row=4, column=1, sticky="w", padx=5, pady=5)
        
        self.interests = {
            "Программирование": tk.BooleanVar(),
            "Музыка": tk.BooleanVar(),
            "Спорт": tk.BooleanVar(),
            "Чтение": tk.BooleanVar()
        }
        
        for i, (interest, var) in enumerate(self.interests.items()):
            ttk.Checkbutton(interests_frame, text=interest, variable=var).grid(
                row=i//2, column=i%2, sticky="w", padx=5)
        
        # Кнопка отправки
        ttk.Button(form_frame, text="Отправить", 
                  command=self.submit_form).grid(row=5, column=0, columnspan=2, pady=20)
    
    def create_list_table_tab(self, parent):
        """
        Создание вкладки со списками и таблицами
        """
        list_frame = ttk.Frame(parent)
        parent.add(list_frame, text="Списки и таблицы")
        
        # Создание Treeview (таблица/дерево)
        columns = ("Имя", "Возраст", "Город")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="tree headings")
        
        # Настройка заголовков столбцов
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        
        # Добавление данных
        data = [
            ("Иван", "25", "Москва"),
            ("Мария", "30", "СПб"),
            ("Алексей", "22", "Новосибирск"),
            ("Елена", "28", "Екатеринбург")
        ]
        
        for item in data:
            self.tree.insert("", tk.END, values=item)
        
        # Добавление прокрутки
        tree_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=tree_scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
    
    def create_progress_choice_tab(self, parent):
        """
        Создание вкладки с прогрессом и выбором
        """
        progress_frame = ttk.Frame(parent)
        parent.add(progress_frame, text="Прогресс и выбор")
        
        # Прогресс бар
        ttk.Label(progress_frame, text="Прогресс бар:").pack(anchor="w", padx=10, pady=10)
        self.progress = ttk.Progressbar(progress_frame, mode="determinate", length=300)
        self.progress.pack(padx=10, pady=5)
        
        # Кнопка для запуска анимации прогресса
        self.progress_btn = ttk.Button(progress_frame, text="Запустить прогресс", 
                                      command=self.start_progress)
        self.progress_btn.pack(pady=10)
        
        # Combobox
        ttk.Label(progress_frame, text="Выберите значение:").pack(anchor="w", padx=10, pady=(20, 10))
        self.combo_var = tk.StringVar()
        combo = ttk.Combobox(progress_frame, textvariable=self.combo_var,
                           values=["Вариант 1", "Вариант 2", "Вариант 3"])
        combo.pack(padx=10, pady=5)
        combo.set("Выберите вариант")
    
    def submit_form(self):
        """
        Обработка отправки формы
        """
        name = self.name_entry.get()
        surname = self.surname_entry.get()
        age = self.age_spinbox.get()
        gender = self.gender_var.get()
        
        selected_interests = [interest for interest, var in self.interests.items() if var.get()]
        
        message = f"""
        Данные формы:
        Имя: {name}
        Фамилия: {surname}
        Возраст: {age}
        Пол: {"Мужской" if gender == "male" else "Женский"}
        Интересы: {", ".join(selected_interests)}
        """
        
        messagebox.showinfo("Отправленные данные", message)
    
    def start_progress(self):
        """
        Запуск анимации прогресса
        """
        import threading
        self.progress_btn.config(state="disabled")
        self.progress['value'] = 0
        
        def update_progress():
            for i in range(101):
                self.root.after(0, lambda val=i: self.progress.config(value=val))
                self.root.update_idletasks()
                import time
                time.sleep(0.05)
            self.root.after(0, lambda: self.progress_btn.config(state="normal"))
        
        thread = threading.Thread(target=update_progress, daemon=True)
        thread.start()
    
    def run(self):
        """
        Запуск приложения
        """
        self.root.mainloop()

if __name__ == "__main__":
    # Выбор примера для запуска
    print("Выберите пример:")
    print("1 - Базовое GUI-приложение")
    print("2 - Продвинутые элементы GUI")
    
    choice = input("Введите номер (1 или 2): ").strip()
    
    if choice == "1":
        app = BasicGUIApp()
        app.run()
    elif choice == "2":
        app = AdvancedGUIElements()
        app.run()
    else:
        print("Неверный выбор")
