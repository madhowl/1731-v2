# Практическое занятие 20: Tkinter - продвинутые элементы

## Цель занятия
Изучить продвинутые элементы интерфейса Tkinter, включая Treeview, Progressbar, Notebook, PanedWindow, Combobox с кастомными списками и другие сложные виджеты.

## Задачи
1. Освоить виджет Treeview для отображения древовидных структур
2. Изучить Progressbar для индикации выполнения
3. Научиться использовать Notebook для создания вкладок
4. Освоить PanedWindow для создания разделяемых панелей
5. Создать приложение «Менеджер задач» с использованием всех элементов

## Ход работы

### 1. Продвинутые виджеты Tkinter

Создайте файл `advanced_widgets.py` и реализуйте функции для работы с продвинутыми виджетами:

#### Treeview - древовидные списки

```python
import tkinter as tk
from tkinter import ttk

def create_treeview(parent, columns):
    """
    Создает Treeview с указанными колонками
    
    Args:
        parent: Родительский виджет
        columns: Список названий колонок
        
    Returns:
        tuple: (Treeview, Scrollbar)
    """
    # ВАШ КОД ЗДЕСЬ - создайте Treeview с колонками
    # Добавьте вертикальный скроллбар
    pass  # Замените на ваш код

def add_tree_item(treeview, parent, values):
    """
    Добавляет элемент в Treeview
    
    Args:
        treeview: Виджет Treeview
        parent: Родительский элемент (пустая строка для корневого)
        values: Значения для всех колонок
    """
    # ВАШ КОД ЗДЕСЬ - добавьте элемент в дерево
    pass  # Замените на ваш код
```

#### Progressbar - индикаторы прогресса

```python
def create_progressbar(parent, mode='determinate'):
    """
    Создает Progressbar
    
    Args:
        parent: Родительский виджет
        mode: Режим ('determinate' или 'indeterminate')
        
    Returns:
        ttk.Progressbar: Созданный Progressbar
    """
    # ВАШ КОД ЗДЕСЬ - создайте Progressbar
    pass  # Замените на ваш код
```

---

## 1. Теоретическая часть: Продвинутые виджеты Tkinter

### Уровень 1 - Начальный

#### Задание 1.1: Treeview - древовидные списки

Создайте приложение с Treeview:

```python
import tkinter as tk
from tkinter import ttk

class TreeviewDemo:
    """
    Демонстрация Treeview
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Treeview - древовидные списки")
        self.root.geometry("500x400")
        
        # ВАШ КОД ЗДЕСЬ - создайте структуру данных
        # Создайте Treeview с колонками (Имя, Возраст, Город)
        # Добавьте элементы с несколькими уровнями вложенности
        pass  # Замените на ваш код
        
    def setup_treeview(self):
        """
        Настраивает Treeview
        """
        # ВАШ КОД ЗДЕСЬ - настройте колонки
        # Добавьте обработчик двойного клика для редактирования
        pass  # Замените на ваш код
        
    def add_sample_data(self):
        """
        Добавляет тестовые данные
        """
        # ВАШ КОД ЗДЕСЬ - добавьте элементы:
        # Корневой уровень - категории
        # Вложенный уровень - элементы
        pass  # Замените на ваш код

# Пример использования:
# root = tk.Tk()
# demo = TreeviewDemo(root)
# root.mainloop()
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import tkinter as tk
from tkinter import ttk

class TreeviewDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Treeview - древовидные списки")
        self.root.geometry("500x400")
        
        self.create_ui()
        self.add_sample_data()
        
    def create_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        ttk.Label(main_frame, text="Древовидный список", 
                  font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Treeview с скроллбарами
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Вертикальный скроллбар
        vsb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Горизонтальный скроллбар
        hsb = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Treeview
        self.tree = ttk.Treeview(tree_frame, columns=("name", "age", "city"),
                                show="headings", yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        vsb.config(command=self.tree.yview)
        hsb.config(command=self.tree.xview)
        
        # Настройка колонок
        self.tree.heading("name", text="Имя")
        self.tree.heading("age", text="Возраст")
        self.tree.heading("city", text="Город")
        
        self.tree.column("name", width=150)
        self.tree.column("age", width=80)
        self.tree.column("city", width=120)
        
        # Обработчик двойного клика
        self.tree.bind("<Double-1>", self.on_double_click)
        
    def add_sample_data(self):
        # Корневой элемент - Семья
        family = self.tree.insert("", tk.END, text="Семья", values=("", "", ""))
        
        # Родители
        self.tree.insert(family, tk.END, text="", values=("Анна", "35", "Москва"))
        self.tree.insert(family, tk.END, text="", values=("Иван", "38", "Москва"))
        
        # Дети
        children = self.tree.insert(family, tk.END, text="Дети", values=("", "", ""))
        self.tree.insert(children, tk.END, text="", values=("Мария", "10", "Москва"))
        self.tree.insert(children, tk.END, text="", values=("Петр", "7", "Москва"))
        
        # Работа
        work = self.tree.insert("", tk.END, text="Работа", values=("", "", ""))
        self.tree.insert(work, tk.END, text="", values=("Компания А", "", "Москва"))
        self.tree.insert(work, tk.END, text="", values=("Компания Б", "", "Санкт-Петербург"))
        
    def on_double_click(self, event):
        # Получение элемента по клику
        item = self.tree.identify('item', event.x, event.y)
        if item:
            print(f"Выбран элемент: {self.tree.item(item)}")

# Пример использования:
root = tk.Tk()
demo = TreeviewDemo(root)
root.mainloop()
```

</details>

#### Задание 1.2: Progressbar - индикаторы прогресса

Реализуйте различные виды прогресс-баров:

```python
import tkinter as tk
from tkinter import ttk

class ProgressbarDemo:
    """
    Демонстрация Progressbar
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Progressbar - индикаторы прогресса")
        
        # ВАШ КОД ЗДЕСЬ - создайте:
        # Определенный прогресс-бар (determinate)
        # Неопределенный прогресс-бар (indeterminate)
        # Кнопки запуска/остановки
        pass  # Замените на ваш код
        
    def start_determinate(self):
        """
        Запускает определенный прогресс-бар
        """
        # ВАШ КОД ЗДЕСЬ - реализуйте анимацию
        pass  # Замените на ваш код
        
    def start_indeterminate(self):
        """
        Запускает неопределенный прогресс-бар
        """
        # ВАШ КОД ЗДЕСЬ - реализуйте анимацию
        pass  # Замените на ваш код

# Пример использования:
# root = tk.Tk()
# demo = ProgressbarDemo(root)
# root.mainloop()
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import tkinter as tk
from tkinter import ttk

class ProgressbarDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Progressbar - индикаторы прогресса")
        self.root.geometry("450x350")
        
        self.determinate_running = False
        self.indeterminate_running = False
        
        self.create_ui()
        
    def create_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Индикаторы прогресса", 
                  font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Определенный прогресс-бар
        ttk.Label(main_frame, text="Определенный прогресс:").pack(anchor=tk.W, pady=(10, 5))
        
        self.det_progress = ttk.Progressbar(main_frame, mode='determinate', length=400)
        self.det_progress.pack(pady=5)
        
        det_btn_frame = ttk.Frame(main_frame)
        det_btn_frame.pack(pady=5)
        
        ttk.Button(det_btn_frame, text="Старт", 
                  command=self.start_determinate).pack(side=tk.LEFT, padx=5)
        ttk.Button(det_btn_frame, text="Стоп", 
                  command=self.stop_determinate).pack(side=tk.LEFT, padx=5)
        ttk.Button(det_btn_frame, text="Сброс", 
                  command=self.reset_determinate).pack(side=tk.LEFT, padx=5)
        
        # Неопределенный прогресс-бар
        ttk.Label(main_frame, text="Неопределенный прогресс:").pack(anchor=tk.W, pady=(20, 5))
        
        self.indet_progress = ttk.Progressbar(main_frame, mode='indeterminate', length=400)
        self.indet_progress.pack(pady=5)
        
        indet_btn_frame = ttk.Frame(main_frame)
        indet_btn_frame.pack(pady=5)
        
        ttk.Button(indet_btn_frame, text="Старт", 
                  command=self.start_indeterminate).pack(side=tk.LEFT, padx=5)
        ttk.Button(indet_btn_frame, text="Стоп", 
                  command=self.stop_indeterminate).pack(side=tk.LEFT, padx=5)
        
        # Множественные прогресс-бары
        ttk.Label(main_frame, text="Множественные задачи:").pack(anchor=tk.W, pady=(20, 5))
        
        self.task_progress = []
        for i in range(3):
            ttk.Label(main_frame, text=f"Задача {i+1}:").pack(anchor=tk.W)
            pb = ttk.Progressbar(main_frame, mode='determinate', length=400)
            pb.pack(pady=2)
            self.task_progress.append(pb)
            
        ttk.Button(main_frame, text="Запустить все задачи", 
                  command=self.run_all_tasks).pack(pady=10)
        
    def start_determinate(self):
        self.determinate_running = True
        self.det_progress['value'] = 0
        self.update_determinate()
        
    def update_determinate(self):
        if not self.determinate_running:
            return
            
        current = self.det_progress['value']
        if current < 100:
            self.det_progress['value'] = current + 2
            self.root.after(50, self.update_determinate)
        else:
            self.determinate_running = False
            
    def stop_determinate(self):
        self.determinate_running = False
        
    def reset_determinate(self):
        self.det_progress['value'] = 0
        
    def start_indeterminate(self):
        if not self.indeterminate_running:
            self.indeterminate_running = True
            self.indet_progress.start(10)
            
    def stop_indeterminate(self):
        self.indet_progress.stop()
        self.indeterminate_running = False
        
    def run_all_tasks(self):
        self.task_count = 0
        self.update_tasks()
        
    def update_tasks(self):
        if self.task_count >= len(self.task
            
        pb = self.task_progress_progress):
            return[self.task_count]
        current = pb['value']
        
        if current < 100:
            pb['value'] = current + 5
            self.root.after(30, self.update_tasks)
        else:
            self.task_count += 1
            if self.task_count < len(self.task_progress):
                self.root.after(30, self.update_tasks)

# Пример использования:
root = tk.Tk()
demo = ProgressbarDemo(root)
root.mainloop()
```

</details>

### Уровень 2 - Средний

#### Задание 2.1: Notebook - создание вкладок

Создайте интерфейс с вкладками:

```python
import tkinter as tk
from tkinter import ttk

class NotebookDemo:
    """
    Демонстрация Notebook (вкладки)
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Notebook - вкладки")
        
        # ВАШ КОД ЗДЕСЬ - создайте Notebook
        # Добавьте несколько вкладок с разным содержимым
        # Обработайте события переключения вкладок
        pass  # Замените на ваш код
        
    def add_tab(self, title, content):
        """
        Добавляет новую вкладку
        
        Args:
            title: Заголовок вкладки
            content: Содержимое вкладки
        """
        # ВАШ КОД ЗДЕСЬ - добавьте вкладку
        pass  # Замените на ваш код

# Пример использования:
# root = tk.Tk()
# demo = NotebookDemo(root)
# root.mainloop()
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import tkinter as tk
from tkinter import ttk

class NotebookDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Notebook - вкладки")
        self.root.geometry("500x400")
        
        self.create_ui()
        
    def create_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        ttk.Label(main_frame, text="Вкладки (Notebook)", 
                  font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Notebook
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Обработчик переключения вкладок
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        
        # Вкладка 1 - Форма
        self.tab1 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab1, text="Форма")
        self.create_form_tab()
        
        # Вкладка 2 - Список
        self.tab2 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab2, text="Список")
        self.create_list_tab()
        
        # Вкладка 3 - Настройки
        self.tab3 = ttk.Frame(self.notebook)
        self.notebook.add(self.tab3, text="Настройки")
        self.create_settings_tab()
        
        # Панель управления вкладками
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(pady=10)
        
        ttk.Button(control_frame, text="Добавить вкладку", 
                  command=self.add_new_tab).pack(side=tk.LEFT, padx=5)
        
        self.tab_count = 3
        
    def create_form_tab(self):
        frame = ttk.Frame(self.tab1, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Форма ввода данных", 
                  font=('Arial', 12)).pack(pady=10)
        
        ttk.Label(frame, text="Имя:").pack(anchor=tk.W, pady=(10, 0))
        ttk.Entry(frame, width=30).pack(pady=5)
        
        ttk.Label(frame, text="Email:").pack(anchor=tk.W, pady=(10, 0))
        ttk.Entry(frame, width=30).pack(pady=5)
        
        ttk.Label(frame, text="Комментарий:").pack(anchor=tk.W, pady=(10, 0))
        tk.Text(frame, width=30, height=5).pack(pady=5)
        
    def create_list_tab(self):
        frame = ttk.Frame(self.tab2, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Список элементов", 
                  font=('Arial', 12)).pack(pady=10)
        
        listbox = tk.Listbox(frame)
        listbox.pack(fill=tk.BOTH, expand=True)
        
        for item in ["Элемент 1", "Элемент 2", "Элемент 3", "Элемент 4", "Элемент 5"]:
            listbox.insert(tk.END, item)
            
    def create_settings_tab(self):
        frame = ttk.Frame(self.tab3, padding="20")
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(frame, text="Настройки приложения", 
                  font=('Arial', 12)).pack(pady=10)
        
        ttk.Checkbutton(frame, text="Автосохранение").pack(anchor=tk.W, pady=5)
        ttk.Checkbutton(frame, text="Уведомления").pack(anchor=tk.W, pady=5)
        ttk.Checkbutton(frame, text="Тёмная тема").pack(anchor=tk.W, pady=5)
        
    def on_tab_changed(self, event):
        current_tab = self.notebook.index(self.notebook.select())
        print(f"Переключено на вкладку {current_tab}")
        
    def add_new_tab(self):
        self.tab_count += 1
        new_tab = ttk.Frame(self.notebook)
        self.notebook.add(new_tab, text=f"Вкладка {self.tab_count}")
        
        ttk.Label(new_tab, text=f"Содержимое вкладки {self.tab_count}", 
                  padding=20).pack()

# Пример использования:
root = tk.Tk()
demo = NotebookDemo(root)
root.mainloop()
```

</details>

#### Задание 2.2: PanedWindow - разделяемые панели

Реализуйте интерфейс с разделителями:

```python
import tkinter as tk
from tkinter import ttk

class PanedWindowDemo:
    """
    Демонстрация PanedWindow
    """
    def __init__(self, root):
        self.root = root
        self.root.title("PanedWindow - разделяемые панели")
        
        # ВАШ КОД ЗДЕСЬ - создайте:
        # Горизонтальное разделение
        # Вертикальное разделение
        # Возможность изменения размера панелей
        pass  # Замените на ваш код

# Пример использования:
# root = tk.Tk()
# demo = PanedWindowDemo(root)
# root.mainloop()
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import tkinter as tk
from tkinter import ttk

class PanedWindowDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("PanedWindow - разделяемые панели")
        self.root.geometry("700x500")
        
        self.create_ui()
        
    def create_ui(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="PanedWindow - разделяемые панели", 
                  font=('Arial', 14, 'bold'), padding=10).pack()
        
        # Горизонтальное разделение (левая и правая панель)
        h_paned = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        h_paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Левая панель
        left_frame = ttk.Frame(h_paned)
        ttk.Label(left_frame, text="Левая панель\n\nСодержимое").pack(pady=20)
        
        listbox = tk.Listbox(left_frame)
        listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        for i in range(10):
            listbox.insert(tk.END, f"Элемент {i+1}")
            
        h_paned.add(left_frame, weight=1)
        
        # Правая панель с вертикальным разделением
        v_paned = ttk.PanedWindow(h_paned, orient=tk.VERTICAL)
        h_paned.add(v_paned, weight=2)
        
        # Верхняя правая панель
        top_right = ttk.Frame(v_paned)
        ttk.Label(top_right, text="Верхняя правая панель").pack(pady=10)
        ttk.Entry(top_right, width=30).pack(pady=5)
        ttk.Button(top_right, text="Кнопка").pack(pady=5)
        
        v_paned.add(top_right, weight=1)
        
        # Нижняя правая панель
        bottom_right = ttk.Frame(v_paned)
        ttk.Label(bottom_right, text="Нижняя правая панель\n\nМожно менять размер").pack(pady=20)
        
        v_paned.add(bottom_right, weight=1)

# Пример использования:
root = tk.Tk()
demo = PanedWindowDemo(root)
root.mainloop()
```

</details>

### Уровень 3 - Продвинутый

#### Задание 3.1: Создание приложения «Менеджер задач»

Разработайте приложение «Менеджер задач»:

```python
import tkinter as tk
from tkinter import ttk, messagebox

class TaskManager:
    """
    Приложение для управления задачами
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Менеджер задач")
        
        # ВАШ КОД ЗДЕСЬ - инициализируйте структуру данных задач
        # Создайте интерфейс с:
        # Treeview для списка задач
        # Формой добавления/редактирования
        # Progressbar для отображения прогресса
        # Вкладками для категорий
        pass  # Замените на ваш код
        
    def add_task(self, title, description, priority, category):
        """
        Добавляет новую задачу
        
        Args:
            title: Название задачи
            description: Описание
            priority: Приоритет
            category: Категория
        """
        # ВАШ КОД ЗДЕСЬ - добавьте задачу в структуру данных
        pass  # Замените на ваш код
        
    def update_task(self, task_id, title, description, priority, status):
        """
        Обновляет задачу
        
        Args:
            task_id: ID задачи
            title: Название
            description: Описание
            priority: Приоритет
            status: Статус выполнения
        """
        # ВАШ КОД ЗДЕСЬ - обновите задачу
        pass  # Замените на ваш код
        
    def delete_task(self, task_id):
        """
        Удаляет задачу
        
        Args:
            task_id: ID задачи
        """
        # ВАШ КОД ЗДЕСЬ - удалите задачу
        pass  # Замените на ваш код
        
    def calculate_progress(self):
        """
        Вычисляет прогресс выполнения
        
        Returns:
            float: Процент выполнения
        """
        # ВАШ КОД ЗДЕСЬ - вычислите прогресс
        pass  # Замените на ваш код

# Пример использования:
# root = tk.Tk()
# app = TaskManager(root)
# root.mainloop()
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import tkinter as tk
from tkinter import ttk, messagebox

class TaskManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Менеджер задач")
        self.root.geometry("800x600")
        
        self.tasks = []
        self.task_id_counter = 1
        
        self.create_ui()
        self.add_sample_tasks()
        
    def create_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        ttk.Label(main_frame, text="Менеджер задач", 
                  font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Прогресс
        ttk.Label(main_frame, text="Прогресс выполнения:").pack(anchor=tk.W)
        
        self.progress = ttk.Progressbar(main_frame, mode='determinate', length=750)
        self.progress.pack(pady=5)
        
        self.progress_label = ttk.Label(main_frame, text="0%")
        self.progress_label.pack(anchor=tk.W)
        
        # PanedWindow для разделения
        h_paned = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        h_paned.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Левая панель - список задач
        left_frame = ttk.Frame(h_paned)
        
        # Treeview для задач
        columns = ("id", "title", "priority", "status")
        self.task_tree = ttk.Treeview(left_frame, columns=columns, show="headings")
        
        self.task_tree.heading("id", text="ID")
        self.task_tree.heading("title", text="Название")
        self.task_tree.heading("priority", text="Приоритет")
        self.task_tree.heading("status", text="Статус")
        
        self.task_tree.column("id", width=50)
        self.task_tree.column("title", width=250)
        self.task_tree.column("priority", width=100)
        self.task_tree.column("status", width=100)
        
        vsb = ttk.Scrollbar(left_frame, orient=tk.VERTICAL, command=self.task_tree.yview)
        self.task_tree.configure(yscrollcommand=vsb.set)
        
        self.task_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        
        h_paned.add(left_frame, weight=2)
        
        # Правая панель - форма
        right_frame = ttk.Frame(h_paned)
        
        ttk.Label(right_frame, text="Управление задачами", 
                  font=('Arial', 12, 'bold')).pack(pady=10)
        
        # Форма
        ttk.Label(right_frame, text="Название:").pack(anchor=tk.W, padx=5)
        self.title_entry = ttk.Entry(right_frame, width=30)
        self.title_entry.pack(pady=5)
        
        ttk.Label(right_frame, text="Описание:").pack(anchor=tk.W, padx=5)
        self.desc_text = tk.Text(right_frame, width=30, height=5)
        self.desc_text.pack(pady=5)
        
        ttk.Label(right_frame, text="Приоритет:").pack(anchor=tk.W, padx=5)
        self.priority_var = tk.StringVar(value="Средний")
        priority_combo = ttk.Combobox(right_frame, textvariable=self.priority_var,
                                      values=["Высокий", "Средний", "Низкий"], 
                                      state="readonly", width=27)
        priority_combo.pack(pady=5)
        
        ttk.Label(right_frame, text="Статус:").pack(anchor=tk.W, padx=5)
        self.status_var = tk.StringVar(value="В ожидании")
        status_combo = ttk.Combobox(right_frame, textvariable=self.status_var,
                                    values=["В ожидании", "В процессе", "Выполнено"],
                                    state="readonly", width=27)
        status_combo.pack(pady=5)
        
        # Кнопки
        btn_frame = ttk.Frame(right_frame)
        btn_frame.pack(pady=15)
        
        ttk.Button(btn_frame, text="Добавить", 
                  command=self.add_task_from_form).pack(pady=5, fill=tk.X)
        ttk.Button(btn_frame, text="Изменить", 
                  command=self.update_task_from_form).pack(pady=5, fill=tk.X)
        ttk.Button(btn_frame, text="Удалить", 
                  command=self.delete_selected_task).pack(pady=5, fill=tk.X)
        
        h_paned.add(right_frame, weight=1)
        
    def add_task_from_form(self):
        title = self.title_entry.get()
        if not title:
            messagebox.showerror("Ошибка", "Введите название задачи!")
            return
            
        description = self.desc_text.get("1.0", tk.END).strip()
        priority = self.priority_var.get()
        status = self.status_var.get()
        
        task_id = self.task_id_counter
        self.task_id_counter += 1
        
        self.tasks.append({
            "id": task_id,
            "title": title,
            "description": description,
            "priority": priority,
            "status": status
        })
        
        self.task_tree.insert("", tk.END, values=(task_id, title, priority, status))
        self.update_progress()
        
        self.clear_form()
        
    def update_task_from_form(self):
        selected = self.task_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите задачу для изменения!")
            return
            
        item = self.task_tree.item(selected[0])
        task_id = item['values'][0]
        
        title = self.title_entry.get()
        description = self.desc_text.get("1.0", tk.END).strip()
        priority = self.priority_var.get()
        status = self.status_var.get()
        
        for task in self.tasks:
            if task["id"] == task_id:
                task["title"] = title
                task["description"] = description
                task["priority"] = priority
                task["status"] = status
                break
                
        self.task_tree.item(selected[0], values=(task_id, title, priority, status))
        self.update_progress()
        
    def delete_selected_task(self):
        selected = self.task_tree.selection()
        if not selected:
            messagebox.showwarning("Внимание", "Выберите задачу для удаления!")
            return
            
        item = self.task_tree.item(selected[0])
        task_id = item['values'][0]
        
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        self.task_tree.delete(selected[0])
        self.update_progress()
        
    def clear_form(self):
        self.title_entry.delete(0, tk.END)
        self.desc_text.delete("1.0", tk.END)
        self.priority_var.set("Средний")
        self.status_var.set("В ожидании")
        
    def update_progress(self):
        if not self.tasks:
            self.progress['value'] = 0
            self.progress_label.config(text="0%")
            return
            
        completed = sum(1 for t in self.tasks if t["status"] == "Выполнено")
        total = len(self.tasks)
        percentage = (completed / total) * 100
        
        self.progress['value'] = percentage
        self.progress_label.config(text=f"{int(percentage)}% ({completed}/{total})")
        
    def add_sample_tasks(self):
        sample_tasks = [
            ("Изучить Tkinter", "Освоить базовые виджеты", "Высокий", "В процессе"),
            ("Создать проект", "Разработать приложение", "Средний", "В ожидании"),
            ("Написать документацию", "Описать функции", "Низкий", "В ожидании")
        ]
        
        for title, desc, priority, status in sample_tasks:
            self.title_entry.insert(0, title)
            self.desc_text.insert("1.0", desc)
            self.priority_var.set(priority)
            self.status_var.set(status)
            self.add_task_from_form()

# Пример использования:
root = tk.Tk()
app = TaskManager(root)
root.mainloop()
```

</details>

---

## Требования к отчету
- Исходный код всех созданных приложений
- Скриншоты интерфейсов
- Описание особенностей каждого виджета
- Объяснение архитектуры приложения «Менеджер задач»

## Критерии оценки
- Корректная реализация виджетов: 50%
- Использование всех типов виджетов: 30%
- Качество интерфейса: 20%
