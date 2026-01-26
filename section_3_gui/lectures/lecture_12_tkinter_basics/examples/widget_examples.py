# Примеры виджетов Tkinter

import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.colorchooser as colorchooser

class WidgetExamples:
    """
    Примеры использования различных виджетов Tkinter
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Примеры виджетов Tkinter")
        self.root.geometry("800x600")
        
        # Создание вкладок для разных виджетов
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Создание вкладок
        self.create_button_tab()
        self.create_input_tab()
        self.create_selection_tab()
        self.create_container_tab()
        
    def create_button_tab(self):
        """
        Создание вкладки с кнопками и переключателями
        """
        button_frame = ttk.Frame(self.notebook)
        self.notebook.add(button_frame, text="Кнопки")
        
        # Кнопки
        ttk.Label(button_frame, text="Кнопки:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=10)
        
        button_panel = ttk.Frame(button_frame)
        button_panel.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(button_panel, text="Обычная кнопка", 
                  command=self.on_regular_button_click).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_panel, text="Стилизованная кнопка", 
                  style="Accent.TButton",
                  command=self.on_styled_button_click).pack(side=tk.LEFT, padx=5)
        
        # Флажки
        ttk.Label(button_frame, text="Флажки:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(20, 10))
        
        self.checkbox_vars = {
            "Опция 1": tk.BooleanVar(),
            "Опция 2": tk.BooleanVar(),
            "Опция 3": tk.BooleanVar()
        }
        
        checkbox_frame = ttk.Frame(button_frame)
        checkbox_frame.pack(fill=tk.X, padx=10)
        
        for text, var in self.checkbox_vars.items():
            ttk.Checkbutton(checkbox_frame, text=text, variable=var, 
                           command=lambda t=text, v=var: self.on_checkbox_click(t, v.get())).pack(anchor="w", pady=2)
        
        # Переключатели
        ttk.Label(button_frame, text="Переключатели:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(20, 10))
        
        self.radio_var = tk.StringVar(value="choice1")
        
        radio_frame = ttk.Frame(button_frame)
        radio_frame.pack(fill=tk.X, padx=10)
        
        choices = ["Выбор 1", "Выбор 2", "Выбор 3"]
        for choice in choices:
            ttk.Radiobutton(
                radio_frame, 
                text=choice, 
                variable=self.radio_var, 
                value=choice.lower().replace(" ", ""),
                command=lambda: self.on_radio_click(self.radio_var.get())
            ).pack(anchor="w", pady=2)
    
    def create_input_tab(self):
        """
        Создание вкладки с элементами ввода
        """
        input_frame = ttk.Frame(self.notebook)
        self.notebook.add(input_frame, text="Ввод")
        
        # Поле ввода
        ttk.Label(input_frame, text="Поле ввода:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=10)
        
        self.entry_var = tk.StringVar()
        entry = ttk.Entry(input_frame, textvariable=self.entry_var, width=50)
        entry.pack(fill=tk.X, padx=10, pady=5)
        entry.insert(0, "Введите текст здесь...")
        
        # Текстовая область
        ttk.Label(input_frame, text="Текстовая область:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(20, 10))
        
        text_frame = ttk.Frame(input_frame)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.text_area = tk.Text(text_frame, wrap=tk.WORD, height=8)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.text_area.yview)
        self.text_area.configure(yscrollcommand=scrollbar.set)
        
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_area.insert("1.0", "Это многострочное текстовое поле.\n\nЗдесь можно вводить и редактировать текст.")
        
        # Spinbox
        ttk.Label(input_frame, text="Spinbox (числовое поле):", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(20, 10))
        
        self.spinbox_var = tk.IntVar(value=0)
        spinbox = ttk.Spinbox(input_frame, from_=-10, to=10, textvariable=self.spinbox_var, width=10)
        spinbox.pack(anchor="w", padx=10, pady=5)
        
        # Scale (ползунок)
        ttk.Label(input_frame, text="Ползунок (Scale):", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(20, 10))
        
        self.scale_var = tk.DoubleVar(value=50.0)
        scale = ttk.Scale(input_frame, from_=0, to=100, variable=self.scale_var, 
                         command=self.on_scale_change, length=300)
        scale.pack(fill=tk.X, padx=10, pady=5)
        
        self.scale_label = ttk.Label(input_frame, text=f"Значение: {self.scale_var.get():.1f}")
        self.scale_label.pack(anchor="w", padx=10)
    
    def create_selection_tab(self):
        """
        Создание вкладки с элементами выбора
        """
        selection_frame = ttk.Frame(self.notebook)
        self.notebook.add(selection_frame, text="Выбор")
        
        # Combobox
        ttk.Label(selection_frame, text="Combobox (выпадающий список):", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=10)
        
        self.combo_var = tk.StringVar()
        combo = ttk.Combobox(
            selection_frame, 
            textvariable=self.combo_var,
            values=["Вариант 1", "Вариант 2", "Вариант 3", "Длинный вариант с названием", "Еще один вариант"],
            state="readonly"
        )
        combo.pack(fill=tk.X, padx=10, pady=5)
        combo.set("Выберите вариант")
        combo.bind("<<ComboboxSelected>>", self.on_combo_select)
        
        # Listbox
        ttk.Label(selection_frame, text="Listbox (список):", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(20, 10))
        
        listbox_frame = ttk.Frame(selection_frame)
        listbox_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.listbox = tk.Listbox(listbox_frame)
        scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=scrollbar.set)
        
        # Добавление элементов в список
        for i in range(1, 21):
            self.listbox.insert(tk.END, f"Элемент {i}")
        
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Привязка события выбора
        self.listbox.bind("<<ListboxSelect>>", self.on_listbox_select)
        
        # Color chooser
        ttk.Label(selection_frame, text="Выбор цвета:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(20, 10))
        
        color_frame = ttk.Frame(selection_frame)
        color_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.color_label = tk.Label(color_frame, text="Выбранный цвет", bg="white", fg="black", 
                                   width=20, height=2, relief="sunken")
        self.color_label.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(color_frame, text="Выбрать цвет", 
                  command=self.choose_color).pack(side=tk.LEFT)
    
    def create_container_tab(self):
        """
        Создание вкладки с контейнерами
        """
        container_frame = ttk.Frame(self.notebook)
        self.notebook.add(container_frame, text="Контейнеры")
        
        # PanedWindow
        ttk.Label(container_frame, text="PanedWindow (разделительная панель):", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=10)
        
        paned_window = ttk.PanedWindow(container_frame, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Левая панель
        left_frame = ttk.Frame(paned_window, width=200, height=300)
        paned_window.add(left_frame, weight=1)
        
        ttk.Label(left_frame, text="Левая панель").pack(pady=20)
        ttk.Button(left_frame, text="Кнопка слева").pack(pady=10)
        
        # Правая панель
        right_frame = ttk.Frame(paned_window, width=200, height=300)
        paned_window.add(right_frame, weight=2)
        
        ttk.Label(right_frame, text="Правая панель").pack(pady=20)
        ttk.Button(right_frame, text="Кнопка справа").pack(pady=10)
        
        # Notebook (вкладки внутри вкладок)
        ttk.Label(container_frame, text="Внутренние вкладки:", font=("Arial", 12, "bold")).pack(anchor="w", padx=10, pady=(20, 10))
        
        inner_notebook = ttk.Notebook(container_frame)
        inner_notebook.pack(fill=tk.X, padx=10, pady=5)
        
        # Внутренние вкладки
        tab1 = ttk.Frame(inner_notebook)
        tab2 = ttk.Frame(inner_notebook)
        
        inner_notebook.add(tab1, text="Вкладка 1")
        inner_notebook.add(tab2, text="Вкладка 2")
        
        ttk.Label(tab1, text="Содержимое внутренней вкладки 1").pack(pady=20)
        ttk.Label(tab2, text="Содержимое внутренней вкладки 2").pack(pady=20)
    
    def on_regular_button_click(self):
        """
        Обработчик нажатия обычной кнопки
        """
        messagebox.showinfo("Информация", "Нажата обычная кнопка!")
    
    def on_styled_button_click(self):
        """
        Обработчик нажатия стилизованной кнопки
        """
        messagebox.showinfo("Информация", "Нажата стилизованная кнопка!")
    
    def on_checkbox_click(self, text, value):
        """
        Обработчик нажатия флажка
        """
        print(f"Флажок '{text}' {'отмечен' if value else 'снят'}")
    
    def on_radio_click(self, value):
        """
        Обработчик выбора переключателя
        """
        print(f"Выбран переключатель: {value}")
    
    def on_scale_change(self, value):
        """
        Обработчик изменения значения ползунка
        """
        self.scale_label.config(text=f"Значение: {float(value):.1f}")
    
    def on_combo_select(self, event):
        """
        Обработчик выбора в комбобоксе
        """
        print(f"Выбран элемент: {self.combo_var.get()}")
    
    def on_listbox_select(self, event):
        """
        Обработчик выбора в списке
        """
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            value = self.listbox.get(index)
            print(f"Выбран элемент списка: {value}")
    
    def choose_color(self):
        """
        Открытие диалога выбора цвета
        """
        color = colorchooser.askcolor(title="Выберите цвет")
        if color[1]:  # Если цвет выбран
            self.color_label.config(bg=color[1], text=f"Цвет: {color[1]}")
    
    def run(self):
        """
        Запуск приложения
        """
        self.root.mainloop()

class GridManagerDemo:
    """
    Демонстрация использования менеджера размещения Grid
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Демонстрация Grid менеджера")
        self.root.geometry("700x500")
        
        self.create_grid_layout()
    
    def create_grid_layout(self):
        """
        Создание интерфейса с использованием Grid
        """
        # Настройка сетки для главного окна
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=2)
        self.root.rowconfigure(1, weight=1)
        
        # Заголовок
        header = ttk.Label(self.root, text="Grid менеджер размещения", 
                          font=("Arial", 16, "bold"))
        header.grid(row=0, column=0, columnspan=2, pady=20, sticky="ew")
        
        # Левая колонка
        left_frame = ttk.LabelFrame(self.root, text="Левая панель", padding=10)
        left_frame.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=5)
        
        # Настройка сетки для левой колонки
        left_frame.columnconfigure(0, weight=1)
        
        ttk.Button(left_frame, text="Кнопка 1").grid(row=0, column=0, sticky="ew", pady=5)
        ttk.Button(left_frame, text="Кнопка 2").grid(row=1, column=0, sticky="ew", pady=5)
        ttk.Button(left_frame, text="Кнопка 3").grid(row=2, column=0, sticky="ew", pady=5)
        
        # Правая колонка
        right_frame = ttk.LabelFrame(self.root, text="Правая панель", padding=10)
        right_frame.grid(row=1, column=1, sticky="nsew", padx=(5, 10), pady=5)
        
        # Настройка сетки для правой колонки
        right_frame.columnconfigure(0, weight=1)
        right_frame.rowconfigure(1, weight=1)
        
        # Ввод
        ttk.Label(right_frame, text="Поле ввода:").grid(row=0, column=0, sticky="w", pady=(0, 5))
        entry = ttk.Entry(right_frame)
        entry.grid(row=0, column=1, sticky="ew", pady=(0, 5))
        
        # Текстовая область
        text_area = tk.Text(right_frame, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(right_frame, orient=tk.VERTICAL, command=text_area.yview)
        text_area.configure(yscrollcommand=scrollbar.set)
        
        text_area.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=5)
        scrollbar.grid(row=1, column=2, sticky="ns", pady=5)
        
        # Кнопки внизу
        button_frame = ttk.Frame(right_frame)
        button_frame.grid(row=2, column=0, columnspan=3, pady=10)
        
        ttk.Button(button_frame, text="ОК").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Отмена").pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Применить").pack(side=tk.LEFT, padx=5)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    print("Выберите демонстрацию:")
    print("1 - Примеры виджетов")
    print("2 - Grid менеджер")
    
    choice = input("Введите номер (1 или 2): ").strip()
    
    if choice == "1":
        app = WidgetExamples()
        app.run()
    elif choice == "2":
        app = GridManagerDemo()
        app.run()
    else:
        print("Неверный выбор")
