# Лекция 14: Tkinter - продвинутые элементы

## Canvas, меню, диалоговые окна, продвинутая компоновка

### План лекции:
1. Виджет Canvas
2. Меню и контекстные меню
3. Диалоговые окна
4. Продвинутая компоновка (grid, place)
5. Работа с изображениями
6. Практические примеры

---

## 1. Виджет Canvas

### Основные возможности Canvas

Canvas - это мощный виджет для рисования графики, текста и других элементов. Он позволяет создавать интерактивные графические интерфейсы.

```python
import tkinter as tk

class CanvasDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Canvas Demo")
        self.root.geometry("800x600")
        
        # Создание Canvas
        self.canvas = tk.Canvas(root, width=780, height=500, bg="white", relief="sunken", bd=2)
        self.canvas.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Добавление инструментов рисования
        self.setup_tools()
        
        # Рисование начальных фигур
        self.draw_initial_shapes()
    
    def setup_tools(self):
        # Панель инструментов
        toolbar = tk.Frame(self.root)
        toolbar.pack(fill="x", padx=10)
        
        tk.Button(toolbar, text="Очистить", command=self.clear_canvas).pack(side="left", padx=5)
        tk.Button(toolbar, text="Рисовать круг", command=self.draw_circle).pack(side="left", padx=5)
        tk.Button(toolbar, text="Рисовать прямоугольник", command=self.draw_rectangle).pack(side="left", padx=5)
        tk.Button(toolbar, text="Рисовать линию", command=self.draw_line).pack(side="left", padx=5)
        
        # Выбор цвета
        tk.Label(toolbar, text="Цвет:").pack(side="left", padx=(20, 5))
        self.color_var = tk.StringVar(value="black")
        color_options = ["black", "red", "blue", "green", "yellow", "purple"]
        color_menu = tk.OptionMenu(toolbar, self.color_var, *color_options)
        color_menu.pack(side="left", padx=5)
        
        # Размер кисти
        tk.Label(toolbar, text="Размер:").pack(side="left", padx=(20, 5))
        self.brush_size = tk.Scale(toolbar, from_=1, to=20, orient="horizontal", length=100)
        self.brush_size.set(5)
        self.brush_size.pack(side="left", padx=5)
    
    def draw_initial_shapes(self):
        # Рисование различных фигур на Canvas
        # Прямоугольник
        self.canvas.create_rectangle(50, 50, 150, 100, fill="lightblue", outline="navy", width=2)
        
        # Овал
        self.canvas.create_oval(200, 50, 300, 150, fill="lightgreen", outline="darkgreen", width=2)
        
        # Многоугольник
        self.canvas.create_polygon(350, 50, 400, 100, 350, 150, fill="pink", outline="magenta", width=2)
        
        # Линия
        self.canvas.create_line(50, 200, 150, 250, fill="red", width=3)
        
        # Текст
        self.canvas.create_text(400, 200, text="Текст на Canvas", font=("Arial", 16), fill="purple")
        
        # Дуга
        self.canvas.create_arc(500, 50, 600, 150, start=0, extent=180, fill="yellow", outline="orange", style="pieslice")
        
        # Изображение (только если файл существует)
        # try:
        #     self.img = tk.PhotoImage(file="sample.png")  # Замените на реальный путь к изображению
        #     self.canvas.create_image(650, 100, image=self.img)
        # except tk.TclError:
        #     self.canvas.create_text(650, 100, text="Изображение\nне найдено", font=("Arial", 10))
    
    def clear_canvas(self):
        """Очистка холста"""
        self.canvas.delete("all")
    
    def draw_circle(self):
        """Рисование круга"""
        color = self.color_var.get()
        size = self.brush_size.get()
        self.canvas.create_oval(100, 300, 100 + size*4, 300 + size*4, 
                               fill=color, outline=color, width=size)
    
    def draw_rectangle(self):
        """Рисование прямоугольника"""
        color = self.color_var.get()
        size = self.brush_size.get()
        self.canvas.create_rectangle(200, 300, 200 + size*6, 300 + size*4, 
                                    fill="", outline=color, width=size)
    
    def draw_line(self):
        """Рисование линии"""
        color = self.color_var.get()
        size = self.brush_size.get()
        self.canvas.create_line(300, 300, 300 + size*10, 300 + size*5, 
                               fill=color, width=size)

# Пример рисования с мышью
class DrawingCanvas:
    def __init__(self, root):
        self.root = root
        self.root.title("Canvas с рисованием мышью")
        self.root.geometry("800x600")
        
        self.canvas = tk.Canvas(root, bg="white", width=780, height=500)
        self.canvas.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Переменные для рисования
        self.last_x, self.last_y = None, None
        self.color = "black"
        self.brush_size = 2
        
        # Привязка событий мыши
        self.canvas.bind("<Button-1>", self.start_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)
        
        # Панель инструментов
        self.setup_drawing_tools()
    
    def setup_drawing_tools(self):
        toolbar = tk.Frame(self.root)
        toolbar.pack(fill="x", padx=10, pady=5)
        
        tk.Label(toolbar, text="Цвет:").pack(side="left", padx=(0, 5))
        colors = ["black", "red", "blue", "green", "yellow", "purple", "orange", "brown"]
        for color in colors:
            btn = tk.Button(
                toolbar, 
                bg=color, 
                width=2, 
                command=lambda c=color: setattr(self, 'color', c)
            )
            btn.pack(side="left", padx=2)
        
        tk.Label(toolbar, text="Размер:").pack(side="left", padx=(20, 5))
        self.size_scale = tk.Scale(toolbar, from_=1, to=20, orient="horizontal", command=self.change_brush_size)
        self.size_scale.set(2)
        self.size_scale.pack(side="left", padx=5)
    
    def start_draw(self, event):
        self.last_x, self.last_y = event.x, event.y
    
    def draw(self, event):
        if self.last_x and self.last_y:
            self.canvas.create_line(
                self.last_x, self.last_y, 
                event.x, event.y,
                fill=self.color, 
                width=self.brush_size,
                capstyle=tk.ROUND,
                smooth=tk.TRUE
            )
        self.last_x, self.last_y = event.x, event.y
    
    def stop_draw(self, event):
        self.last_x, self.last_y = None, None
    
    def change_brush_size(self, val):
        self.brush_size = int(val)

root = tk.Tk()
app = CanvasDemo(root)
root.mainloop()
```

### Анимация на Canvas

```python
import tkinter as tk
import math
import time

class CanvasAnimation:
    def __init__(self, root):
        self.root = root
        self.root.title("Canvas Animation")
        self.root.geometry("800x600")
        
        self.canvas = tk.Canvas(root, bg="black", width=780, height=500)
        self.canvas.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Создание анимируемых объектов
        self.create_animated_objects()
        
        # Запуск анимации
        self.animate()
    
    def create_animated_objects(self):
        # Создание кругов для анимации
        self.circles = []
        for i in range(5):
            circle = self.canvas.create_oval(
                100 + i*50, 100 + i*30, 130 + i*50, 130 + i*30,
                fill=f"#{i*3}ff{i*5}", outline="white"
            )
            self.circles.append({
                'id': circle,
                'x': 100 + i*50,
                'y': 100 + i*30,
                'dx': (i+1) * 2,
                'dy': (i+1) % 2 * 3 - 1
            })
        
        # Создание текста с эффектом
        self.text_id = self.canvas.create_text(
            400, 250, 
            text="Анимация на Canvas", 
            font=("Arial", 24, "bold"),
            fill="white"
        )
        self.text_angle = 0
    
    def animate(self):
        # Анимация кругов
        for circle in self.circles:
            # Перемещение
            self.canvas.move(circle['id'], circle['dx'], circle['dy'])
            
            # Получение координат
            pos = self.canvas.coords(circle['id'])
            
            # Отскок от стен
            if pos[0] <= 0 or pos[2] >= 780:
                circle['dx'] *= -1
            if pos[1] <= 0 or pos[3] >= 500:
                circle['dy'] *= -1
        
        # Анимация текста
        self.text_angle += 5
        if self.text_angle >= 360:
            self.text_angle = 0
        
        # Изменение цвета текста
        hue = (self.text_angle / 360) * 255
        color = f"#{int(hue):02x}{int(255-hue):02x}{int(hue/2):02x}"
        self.canvas.itemconfig(self.text_id, fill=color)
        
        # Повтор анимации
        self.root.after(50, self.animate)  # Обновление каждые 50 мс

# root = tk.Tk()
# animation = CanvasAnimation(root)
# root.mainloop()
```

---

## 2. Меню и контекстные меню

### Основные типы меню

```python
import tkinter as tk
from tkinter import messagebox, filedialog

class MenuDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Демонстрация меню")
        self.root.geometry("800x600")
        
        # Создание меню
        self.create_menu()
        
        # Создание контекстного меню
        self.create_context_menu()
        
        # Текстовая область для демонстрации
        self.text_area = tk.Text(root, wrap=tk.WORD)
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Привязка правой кнопки мыши к контекстному меню
        self.text_area.bind("<Button-3>", self.show_context_menu)
    
    def create_menu(self):
        # Создание меню
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Меню "Файл"
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        
        file_menu.add_command(label="Новый", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Открыть", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Сохранить", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.exit_app, accelerator="Alt+F4")
        
        # Меню "Правка"
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Правка", menu=edit_menu)
        
        edit_menu.add_command(label="Отменить", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Повторить", command=self.redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Вырезать", command=self.cut, accelerator="Ctrl+X")
        edit_menu.add_command(label="Копировать", command=self.copy, accelerator="Ctrl+C")
        edit_menu.add_command(label="Вставить", command=self.paste, accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Выделить все", command=self.select_all, accelerator="Ctrl+A")
        
        # Меню "Вид"
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Вид", menu=view_menu)
        
        self.show_toolbar = tk.BooleanVar(value=True)
        view_menu.add_checkbutton(label="Показать панель инструментов", 
                                 variable=self.show_toolbar, 
                                 command=self.toggle_toolbar)
        
        self.show_status_bar = tk.BooleanVar(value=True)
        view_menu.add_checkbutton(label="Показать строку состояния", 
                                 variable=self.show_status_bar, 
                                 command=self.toggle_status_bar)
        
        # Подменю с выбором темы
        theme_menu = tk.Menu(view_menu, tearoff=0)
        view_menu.add_cascade(label="Тема", menu=theme_menu)
        
        themes = ["Светлая", "Темная", "Синяя", "Зеленая"]
        self.current_theme = tk.StringVar(value="Светлая")
        
        for theme in themes:
            theme_menu.add_radiobutton(label=theme, 
                                     variable=self.current_theme, 
                                     value=theme, 
                                     command=self.change_theme)
        
        # Меню "Помощь"
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Помощь", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.about)
    
    def create_context_menu(self):
        # Создание контекстного меню
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Вырезать", command=self.cut)
        self.context_menu.add_command(label="Копировать", command=self.copy)
        self.context_menu.add_command(label="Вставить", command=self.paste)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Выбрать все", command=self.select_all)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Очистить", command=self.clear_text)
    
    def show_context_menu(self, event):
        """Показ контекстного меню"""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    def new_file(self):
        """Создание нового файла"""
        if self.text_area.edit_modified():
            result = messagebox.askyesnocancel("Несохраненные изменения", 
                                            "Сохранить изменения перед созданием нового файла?")
            if result:
                self.save_file()
            elif result is None:
                return  # Отмена
        
        self.text_area.delete(1.0, tk.END)
        self.root.title("Безымянный - Текстовый редактор")
    
    def open_file(self):
        """Открытие файла"""
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
                
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(1.0, content)
                self.text_area.edit_modified(False)
                
                self.root.title(f"{file_path} - Текстовый редактор")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось открыть файл:\n{str(e)}")
    
    def save_file(self):
        """Сохранение файла"""
        # В реальном приложении здесь должна быть реализация сохранения
        messagebox.showinfo("Сохранение", "Файл сохранен!")
    
    def exit_app(self):
        """Выход из приложения"""
        if self.text_area.edit_modified():
            result = messagebox.askyesnocancel("Несохраненные изменения", 
                                            "Сохранить изменения перед выходом?")
            if result:
                self.save_file()
                self.root.quit()
            elif result is None:
                pass  # Отмена выхода
            else:
                self.root.quit()
        else:
            self.root.quit()
    
    def undo(self):
        """Отмена действия"""
        try:
            self.text_area.edit_undo()
        except tk.TclError:
            pass
    
    def redo(self):
        """Повтор действия"""
        try:
            self.text_area.edit_redo()
        except tk.TclError:
            pass
    
    def cut(self):
        """Вырезать"""
        self.text_area.event_generate("<<Cut>>")
    
    def copy(self):
        """Копировать"""
        self.text_area.event_generate("<<Copy>>")
    
    def paste(self):
        """Вставить"""
        self.text_area.event_generate("<<Paste>>")
    
    def select_all(self):
        """Выделить все"""
        self.text_area.tag_add(tk.SEL, "1.0", tk.END)
        self.text_area.mark_set(tk.INSERT, "1.0")
        self.text_area.see(tk.INSERT)
        return "break"
    
    def clear_text(self):
        """Очистка текста"""
        self.text_area.delete(1.0, tk.END)
    
    def toggle_toolbar(self):
        """Переключение видимости панели инструментов"""
        if self.show_toolbar.get():
            print("Панель инструментов показана")
        else:
            print("Панель инструментов скрыта")
    
    def toggle_status_bar(self):
        """Переключение видимости строки состояния"""
        if self.show_status_bar.get():
            print("Строка состояния показана")
        else:
            print("Строка состояния скрыта")
    
    def change_theme(self):
        """Изменение темы"""
        theme = self.current_theme.get()
        print(f"Тема изменена на: {theme}")
        # В реальном приложении здесь менялись бы стили
    
    def about(self):
        """О программе"""
        messagebox.showinfo("О программе", "Текстовый редактор v1.0\n\nДемонстрация работы меню в Tkinter")

root = tk.Tk()
app = MenuDemo(root)
root.mainloop()
```

---

## 3. Диалоговые окна

### Встроенные диалоговые окна

```python
import tkinter as tk
from tkinter import messagebox, filedialog, colorchooser, simpledialog

class DialogDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Диалоговые окна")
        self.root.geometry("600x500")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Основная панель с кнопками для разных диалогов
        main_frame = tk.Frame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Информационные диалоги
        info_frame = tk.LabelFrame(main_frame, text="Информационные диалоги", padx=10, pady=10)
        info_frame.pack(fill="x", pady=5)
        
        tk.Button(info_frame, text="Info Message", command=self.show_info).pack(side="left", padx=5)
        tk.Button(info_frame, text="Warning Message", command=self.show_warning).pack(side="left", padx=5)
        tk.Button(info_frame, text="Error Message", command=self.show_error).pack(side="left", padx=5)
        
        # Вопросительные диалоги
        question_frame = tk.LabelFrame(main_frame, text="Вопросительные диалоги", padx=10, pady=10)
        question_frame.pack(fill="x", pady=5)
        
        tk.Button(question_frame, text="Yes/No", command=self.ask_yes_no).pack(side="left", padx=5)
        tk.Button(question_frame, text="OK/Cancel", command=self.ask_ok_cancel).pack(side="left", padx=5)
        tk.Button(question_frame, text="Retry/Cancel", command=self.ask_retry_cancel).pack(side="left", padx=5)
        tk.Button(question_frame, text="Yes/No/Cancel", command=self.ask_yes_no_cancel).pack(side="left", padx=5)
        
        # Диалоги выбора
        selection_frame = tk.LabelFrame(main_frame, text="Диалоги выбора", padx=10, pady=10)
        selection_frame.pack(fill="x", pady=5)
        
        tk.Button(selection_frame, text="Выбрать файл", command=self.select_file).pack(side="left", padx=5)
        tk.Button(selection_frame, text="Выбрать папку", command=self.select_folder).pack(side="left", padx=5)
        tk.Button(selection_frame, text="Выбрать цвет", command=self.select_color).pack(side="left", padx=5)
        tk.Button(selection_frame, text="Ввести текст", command=self.input_text).pack(side="left", padx=5)
        
        # Результаты
        self.result_label = tk.Label(main_frame, text="Результаты появятся здесь", 
                                    bg="lightgray", height=10, wraplength=500)
        self.result_label.pack(fill="x", pady=20, padx=10)
    
    def show_info(self):
        messagebox.showinfo("Информация", "Это информационное сообщение!")
        self.result_label.config(text="Показано информационное сообщение")
    
    def show_warning(self):
        messagebox.showwarning("Предупреждение", "Это предупреждающее сообщение!")
        self.result_label.config(text="Показано предупреждение")
    
    def show_error(self):
        messagebox.showerror("Ошибка", "Это сообщение об ошибке!")
        self.result_label.config(text="Показана ошибка")
    
    def ask_yes_no(self):
        result = messagebox.askyesno("Вопрос", "Вы уверены?")
        self.result_label.config(text=f"Результат Yes/No: {result}")
    
    def ask_ok_cancel(self):
        result = messagebox.askokcancel("Подтверждение", "Продолжить выполнение?")
        self.result_label.config(text=f"Результат OK/Cancel: {result}")
    
    def ask_retry_cancel(self):
        result = messagebox.askretrycancel("Повтор", "Повторить попытку?")
        self.result_label.config(text=f"Результат Retry/Cancel: {result}")
    
    def ask_yes_no_cancel(self):
        result = messagebox.askyesnocancel("Вопрос", "Сохранить изменения?")
        self.result_label.config(text=f"Результат Yes/No/Cancel: {result}")
    
    def select_file(self):
        file_path = filedialog.askopenfilename(
            title="Выберите файл",
            filetypes=[
                ("Текстовые файлы", "*.txt"),
                ("Python файлы", "*.py"),
                ("Все файлы", "*.*")
            ]
        )
        if file_path:
            self.result_label.config(text=f"Выбран файл: {file_path}")
        else:
            self.result_label.config(text="Файл не выбран")
    
    def select_folder(self):
        folder_path = filedialog.askdirectory(title="Выберите папку")
        if folder_path:
            self.result_label.config(text=f"Выбрана папка: {folder_path}")
        else:
            self.result_label.config(text="Папка не выбрана")
    
    def select_color(self):
        color = colorchooser.askcolor(title="Выберите цвет")
        if color[1]:  # Проверяем, что цвет был выбран
            self.result_label.config(text=f"Выбран цвет: {color[1]}", bg=color[1])
        else:
            self.result_label.config(text="Цвет не выбран", bg="lightgray")
    
    def input_text(self):
        text = simpledialog.askstring("Ввод текста", "Введите ваше имя:")
        if text:
            self.result_label.config(text=f"Введен текст: {text}")
        else:
            self.result_label.config(text="Текст не введен")

root = tk.Tk()
app = DialogDemo(root)
root.mainloop()
```

### Пользовательские диалоговые окна

```python
import tkinter as tk
from tkinter import ttk

class CustomDialog:
    def __init__(self, parent, title="Диалог", fields=None):
        self.parent = parent
        self.result = None
        
        # Создание диалогового окна
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)  # Окно поверх родительского
        self.dialog.grab_set()  # Блокировка родительского окна
        
        # Центрирование диалога
        self.center_dialog()
        
        # Создание элементов
        self.fields = fields or []
        self.entries = {}
        self.create_widgets()
        
        # Привязка клавиш
        self.dialog.bind('<Return>', self.ok)
        self.dialog.bind('<Escape>', self.cancel)
    
    def center_dialog(self):
        """Центрирование диалога относительно родительского окна"""
        self.dialog.update_idletasks()
        
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()
        
        dialog_width = self.dialog.winfo_width()
        dialog_height = self.dialog.winfo_height()
        
        x = parent_x + (parent_width // 2) - (dialog_width // 2)
        y = parent_y + (parent_height // 2) - (dialog_height // 2)
        
        self.dialog.geometry(f"+{x}+{y}")
    
    def create_widgets(self):
        # Основной фрейм
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Создание полей ввода
        for i, field in enumerate(self.fields):
            ttk.Label(main_frame, text=field + ":").grid(row=i, column=0, sticky="w", pady=5)
            
            entry = ttk.Entry(main_frame, width=30)
            entry.grid(row=i, column=1, sticky="ew", pady=5, padx=(10, 0))
            
            self.entries[field] = entry
        
        # Настройка растягивания
        main_frame.columnconfigure(1, weight=1)
        
        # Кнопки
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=len(self.fields), column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="OK", command=self.ok).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Отмена", command=self.cancel).pack(side="left", padx=5)
        
        # Установка фокуса на первое поле
        if self.entries:
            list(self.entries.values())[0].focus_set()
    
    def ok(self, event=None):
        """Обработка нажатия OK"""
        self.result = {}
        for field, entry in self.entries.items():
            self.result[field] = entry.get()
        self.dialog.destroy()
    
    def cancel(self, event=None):
        """Обработка нажатия Отмена"""
        self.result = None
        self.dialog.destroy()
    
    def show(self):
        """Показ диалога и возврат результата"""
        self.dialog.wait_window()  # Ждем закрытия окна
        return self.result

class CustomDialogDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Пользовательские диалоги")
        self.root.geometry("600x400")
        
        self.create_widgets()
    
    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        ttk.Button(main_frame, text="Открыть диалог пользователя", 
                  command=self.open_user_dialog).pack(pady=10)
        
        ttk.Button(main_frame, text="Открыть диалог настроек", 
                  command=self.open_settings_dialog).pack(pady=10)
        
        self.result_label = ttk.Label(main_frame, text="Результаты появятся здесь")
        self.result_label.pack(pady=20)
    
    def open_user_dialog(self):
        """Открытие диалога для ввода пользовательской информации"""
        fields = ["Имя", "Фамилия", "Email", "Телефон"]
        dialog = CustomDialog(self.root, "Информация о пользователе", fields)
        result = dialog.show()
        
        if result:
            info = ", ".join([f"{k}: {v}" for k, v in result.items()])
            self.result_label.config(text=f"Введена информация: {info}")
    
    def open_settings_dialog(self):
        """Открытие диалога настроек"""
        fields = ["Сервер", "Порт", "Интервал обновления", "Язык"]
        dialog = CustomDialog(self.root, "Настройки приложения", fields)
        result = dialog.show()
        
        if result:
            settings = ", ".join([f"{k}: {v}" for k, v in result.items()])
            self.result_label.config(text=f"Настройки: {settings}")

root = tk.Tk()
app = CustomDialogDemo(root)
root.mainloop()
```

---

## 4. Продвинутая компоновка

### Grid менеджер

```python
import tkinter as tk
from tkinter import ttk

class GridLayoutDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Grid Layout Demo")
        self.root.geometry("800x600")
        
        self.create_grid_layout()
    
    def create_grid_layout(self):
        # Создание основного фрейма
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill="both", expand=True)
        
        # Настройка сетки для основного фрейма
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=2)
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Левая колонка (меню)
        left_frame = ttk.LabelFrame(main_frame, text="Меню", padding="10")
        left_frame.grid(row=0, column=0, rowspan=3, sticky="nsew", padx=(0, 5))
        
        # Настройка растягивания для левой колонки
        left_frame.rowconfigure(0, weight=1)
        left_frame.columnconfigure(0, weight=1)
        
        # Добавление элементов в левую колонку
        menu_items = ["Главная", "Файл", "Правка", "Вид", "Помощь"]
        for i, item in enumerate(menu_items):
            ttk.Button(left_frame, text=item, command=lambda x=item: print(f"Выбрано: {x}")).pack(fill="x", pady=2)
        
        # Верхняя панель
        top_frame = ttk.LabelFrame(main_frame, text="Инструменты", padding="10")
        top_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0), pady=(0, 5))
        
        # Настройка растягивания для верхней панели
        for i in range(4):
            top_frame.columnconfigure(i, weight=1)
        
        tools = ["Открыть", "Сохранить", "Копировать", "Вставить"]
        for i, tool in enumerate(tools):
            ttk.Button(top_frame, text=tool).grid(row=0, column=i, padx=2, sticky="ew")
        
        # Центральная область
        center_frame = ttk.LabelFrame(main_frame, text="Рабочая область", padding="10")
        center_frame.grid(row=1, column=1, sticky="nsew", padx=(5, 0), pady=5)
        
        # Настройка растягивания для центральной области
        center_frame.columnconfigure(0, weight=1)
        center_frame.rowconfigure(0, weight=1)
        
        # Текстовая область с прокруткой
        text_frame = ttk.Frame(center_frame)
        text_frame.pack(fill="both", expand=True)
        
        text_area = tk.Text(text_frame)
        v_scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=text_area.yview)
        h_scrollbar = ttk.Scrollbar(text_frame, orient="horizontal", command=text_area.xview)
        
        text_area.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        text_area.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        # Нижняя панель
        bottom_frame = ttk.LabelFrame(main_frame, text="Статус", padding="10")
        bottom_frame.grid(row=2, column=1, sticky="nsew", padx=(5, 0), pady=(5, 0))
        
        # Настройка растягивания для нижней панели
        bottom_frame.columnconfigure(1, weight=1)
        
        ttk.Label(bottom_frame, text="Готов:").grid(row=0, column=0, sticky="w")
        status_label = ttk.Label(bottom_frame, text="Готов", relief="sunken")
        status_label.grid(row=0, column=1, sticky="ew", padx=(5, 0))

class FormLayoutDemo:
    """Демонстрация создания форм с помощью grid"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Form Layout Demo")
        self.root.geometry("700x500")
        
        self.create_form()
    
    def create_form(self):
        # Основной фрейм формы
        form_frame = ttk.Frame(self.root, padding="20")
        form_frame.pack(fill="both", expand=True)
        
        # Заголовок формы
        title_label = ttk.Label(form_frame, text="Регистрация пользователя", font=("Arial", 16, "bold"))
        title_label.grid(row=0, columnspan=2, pady=(0, 20))
        
        # Поля формы
        fields = [
            ("Имя:", 1),
            ("Фамилия:", 2),
            ("Email:", 3),
            ("Пароль:", 4),
            ("Подтверждение пароля:", 5),
            ("Дата рождения:", 6),
            ("Город:", 7),
            ("Интересы:", 8)
        ]
        
        self.entries = {}
        
        for field_name, row in fields:
            ttk.Label(form_frame, text=field_name).grid(row=row, column=0, sticky="w", pady=5, padx=(0, 10))
            
            if field_name == "Интересы:":
                # Для интересов используем текстовую область
                text_area = tk.Text(form_frame, height=4, width=30)
                text_area.grid(row=row, column=1, sticky="ew", pady=5)
                self.entries[field_name] = text_area
            elif "Пароль" in field_name:
                # Для полей пароля используем маску
                entry = ttk.Entry(form_frame, width=30, show="*")
                entry.grid(row=row, column=1, sticky="ew", pady=5)
                self.entries[field_name] = entry
            else:
                entry = ttk.Entry(form_frame, width=30)
                entry.grid(row=row, column=1, sticky="ew", pady=5)
                self.entries[field_name] = entry
        
        # Настройка растягивания колонок
        form_frame.columnconfigure(1, weight=1)
        
        # Кнопки
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Отправить", command=self.submit_form).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Очистить", command=self.clear_form).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Отмена", command=self.cancel_form).pack(side="left", padx=5)
    
    def submit_form(self):
        """Обработка отправки формы"""
        data = {}
        for field_name, entry in self.entries.items():
            if isinstance(entry, tk.Text):
                data[field_name] = entry.get("1.0", tk.END).strip()
            else:
                data[field_name] = entry.get()
        
        print("Данные формы:", data)
        # Здесь можно добавить валидацию и обработку данных
    
    def clear_form(self):
        """Очистка формы"""
        for entry in self.entries.values():
            if isinstance(entry, tk.Text):
                entry.delete("1.0", tk.END)
            else:
                entry.delete(0, tk.END)
    
    def cancel_form(self):
        """Отмена формы"""
        self.root.destroy()

root = tk.Tk()
app = GridLayoutDemo(root)
root.mainloop()
```

### Place менеджер

```python
import tkinter as tk
from tkinter import ttk

class PlaceLayoutDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Place Layout Demo")
        self.root.geometry("800x600")
        
        self.create_place_layout()
    
    def create_place_layout(self):
        # Создание холста для демонстрации точного позиционирования
        canvas = tk.Canvas(self.root, bg="lightblue", width=800, height=600)
        canvas.pack(fill="both", expand=True)
        
        # Примеры использования place с абсолютными координатами
        absolute_btn = tk.Button(canvas, text="Абсолютная позиция", bg="red", fg="white")
        absolute_btn.place(x=100, y=50)
        
        # Примеры использования place с относительными координатами
        relative_btn = tk.Button(canvas, text="Относительная позиция", bg="green", fg="white")
        relative_btn.place(relx=0.5, rely=0.3, anchor="center")  # По центру по горизонтали, на 30% по вертикали
        
        # Кнопка в правом верхнем углу
        corner_btn = tk.Button(canvas, text="Угловая", bg="blue", fg="white")
        corner_btn.place(relx=1.0, rely=0.0, anchor="ne")  # Правый верхний угол
        
        # Кнопка в центре экрана
        center_btn = tk.Button(canvas, text="Центр", bg="purple", fg="white", font=("Arial", 14))
        center_btn.place(relx=0.5, rely=0.5, anchor="center")
        
        # Кнопка в левом нижнем углу
        bottom_left_btn = tk.Button(canvas, text="Низ слева", bg="orange", fg="black")
        bottom_left_btn.place(relx=0.0, rely=1.0, anchor="sw")
        
        # Пример создания сложного интерфейса с place
        self.create_complex_interface(canvas)
    
    def create_complex_interface(self, canvas):
        # Создание круговой диаграммы (упрощенная)
        chart_frame = tk.Frame(canvas, bg="white", relief="sunken", bd=2)
        chart_frame.place(relx=0.2, rely=0.6, width=200, height=200)
        
        # Заголовок диаграммы
        tk.Label(chart_frame, text="Диаграмма", bg="white", font=("Arial", 12, "bold")).pack(pady=5)
        
        # Создание сегментов диаграммы
        canvas_chart = tk.Canvas(chart_frame, width=180, height=150, bg="white", highlightthickness=0)
        canvas_chart.pack()
        
        # Рисование сегментов круговой диаграммы
        segments = [
            {"label": "Python", "value": 40, "color": "blue"},
            {"label": "Java", "value": 25, "color": "red"},
            {"label": "JS", "value": 20, "color": "yellow"},
            {"label": "C++", "value": 15, "color": "green"}
        ]
        
        start_angle = 0
        for segment in segments:
            angle = segment["value"] * 3.6  # 360/100 = 3.6
            canvas_chart.create_arc(
                40, 20, 140, 120,
                start=start_angle,
                extent=angle,
                fill=segment["color"],
                outline="black"
            )
            start_angle += angle
        
        # Интерактивная панель управления
        control_frame = tk.Frame(canvas, bg="lightgray", relief="raised", bd=2)
        control_frame.place(relx=0.65, rely=0.6, width=250, height=200)
        
        tk.Label(control_frame, text="Панель управления", bg="lightgray", font=("Arial", 12, "bold")).pack(pady=10)
        
        # Кнопки управления
        tk.Button(control_frame, text="Запуск", bg="lightgreen", width=15).pack(pady=5)
        tk.Button(control_frame, text="Пауза", bg="orange", width=15).pack(pady=5)
        tk.Button(control_frame, text="Стоп", bg="red", fg="white", width=15).pack(pady=5)
        
        # Индикатор состояния
        self.status_indicator = tk.Label(control_frame, text="ГОТОВ", bg="green", fg="white", width=15)
        self.status_indicator.pack(pady=10)
        
        # Кнопка для изменения состояния
        tk.Button(control_frame, text="Изменить статус", command=self.toggle_status, width=15).pack(pady=5)
    
    def toggle_status(self):
        """Переключение индикатора состояния"""
        current_text = self.status_indicator.cget("text")
        if current_text == "ГОТОВ":
            self.status_indicator.config(text="РАБОТА", bg="orange")
        else:
            self.status_indicator.config(text="ГОТОВ", bg="green")

class MixedLayoutDemo:
    """Демонстрация комбинации разных менеджеров компоновки"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Mixed Layout Demo")
        self.root.geometry("900x700")
        
        self.create_mixed_layout()
    
    def create_mixed_layout(self):
        # Используем pack для основных разделов
        header_frame = tk.Frame(self.root, bg="navy", height=60)
        header_frame.pack(fill="x")
        
        tk.Label(header_frame, text="Заголовок приложения", fg="white", bg="navy", font=("Arial", 16)).pack(pady=15)
        
        # Центральная область с grid
        center_frame = tk.Frame(self.root)
        center_frame.pack(fill="both", expand=True)
        
        # Левая боковая панель (grid)
        sidebar_frame = tk.Frame(center_frame, bg="lightgray", width=200)
        sidebar_frame.pack(side="left", fill="y", padx=(0, 5))
        
        # Добавляем элементы в боковую панель
        tk.Label(sidebar_frame, text="Навигация", bg="lightgray", font=("Arial", 12, "bold")).pack(pady=10)
        
        nav_items = ["Главная", "Профиль", "Настройки", "Помощь"]
        for item in nav_items:
            tk.Button(sidebar_frame, text=item, width=18, anchor="w", 
                     command=lambda x=item: print(f"Переход к {x}")).pack(pady=2, padx=5, fill="x")
        
        # Основная рабочая область (grid)
        main_area = tk.Frame(center_frame)
        main_area.pack(side="left", fill="both", expand=True, padx=5)
        
        # Используем grid внутри основной области
        main_area.columnconfigure(0, weight=1)
        main_area.columnconfigure(1, weight=1)
        main_area.rowconfigure(2, weight=1)
        
        # Заголовок основной области
        tk.Label(main_area, text="Рабочая область", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Кнопки действий
        tk.Button(main_area, text="Действие 1", width=15).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(main_area, text="Действие 2", width=15).grid(row=1, column=1, padx=5, pady=5)
        
        # Текстовая область с прокруткой
        text_frame = tk.Frame(main_area)
        text_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", pady=10)
        
        text_area = tk.Text(text_frame, wrap=tk.WORD)
        scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=text_area.yview)
        text_area.configure(yscrollcommand=scrollbar.set)
        
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Добавляем немного текста для демонстрации прокрутки
        sample_text = "\n".join([f"Это строка {i+1} с образцовым текстом для демонстрации прокрутки." for i in range(50)])
        text_area.insert("1.0", sample_text)
        
        # Нижняя панель с place
        bottom_frame = tk.Frame(self.root, bg="darkblue", height=40)
        bottom_frame.pack(side="bottom", fill="x")
        
        # Используем place для точного позиционирования элементов в нижней панели
        tk.Label(bottom_frame, text="© 2026 MyApp", fg="white", bg="darkblue").place(relx=0.02, rely=0.5, anchor="w")
        
        status_label = tk.Label(bottom_frame, text="Готов", fg="white", bg="darkgreen")
        status_label.place(relx=0.98, rely=0.5, anchor="e")
        
        # Кнопка в центре нижней панели
        tk.Button(bottom_frame, text="Инфо", command=self.show_info, bg="lightblue").place(relx=0.5, rely=0.5, anchor="center")

    def show_info(self):
        print("Показ информации")

root = tk.Tk()
app = MixedLayoutDemo(root)
root.mainloop()
```

---

## 5. Работа с изображениями

### Использование изображений в Tkinter

```python
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk  # Для работы с изображениями (установка: pip install Pillow)

class ImageDemo:
    def __init__(self, root):
        self.root = root
        self.root.title("Работа с изображениями")
        self.root.geometry("800x600")
        
        self.create_image_interface()
    
    def create_image_interface(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill="both", expand=True)
        
        # Заголовок
        ttk.Label(main_frame, text="Демонстрация работы с изображениями", 
                 font=("Arial", 16, "bold")).pack(pady=10)
        
        # Создание Canvas для отображения изображений
        canvas = tk.Canvas(main_frame, width=600, height=400, bg="white")
        canvas.pack(pady=10)
        
        # Попытка загрузить и отобразить изображение
        try:
            # Создаем изображение для демонстрации
            self.create_sample_image(canvas)
        except ImportError:
            # PIL не установлен, создаем простую графику
            self.create_simple_graphics(canvas)
        
        # Панель инструментов для работы с изображениями
        self.create_image_tools(main_frame)
    
    def create_sample_image(self, canvas):
        """Создание и отображение образцового изображения"""
        # Создаем изображение с помощью Pillow
        from PIL import Image, ImageDraw, ImageFont
        
        # Создаем новое изображение
        img = Image.new('RGB', (400, 300), color='lightblue')
        draw = ImageDraw.Draw(img)
        
        # Рисуем элементы на изображении
        draw.rectangle([50, 50, 350, 250], outline='red', width=3)
        draw.ellipse([100, 100, 300, 200], fill='yellow', outline='orange')
        draw.text((150, 150), "Tkinter + Pillow", fill='purple')
        
        # Преобразуем в формат, подходящий для Tkinter
        self.photo = ImageTk.PhotoImage(img)
        
        # Отображаем на Canvas
        canvas.create_image(300, 200, image=self.photo)
    
    def create_simple_graphics(self, canvas):
        """Создание простой графики без PIL"""
        # Рисуем простые фигуры как замену изображениям
        canvas.create_rectangle(100, 500, 350, outline="blue", width=2)
        canvas.create_oval(200, 100, 400, 300, fill="lightgreen", outline="darkgreen")
        canvas.create_text(300, 200, text="Без PIL", font=("Arial", 20), fill="red")
        canvas.create_line(100, 50, 500, 350, fill="purple", width=3)
    
    def create_image_tools(self, parent):
        """Создание инструментов для работы с изображениями"""
        tools_frame = ttk.LabelFrame(parent, text="Инструменты для изображений", padding="10")
        tools_frame.pack(fill="x", pady=10)
        
        # Кнопки для загрузки и сохранения
        ttk.Button(tools_frame, text="Загрузить изображение", 
                  command=self.load_image).pack(side="left", padx=5)
        ttk.Button(tools_frame, text="Сохранить изображение", 
                  command=self.save_image).pack(side="left", padx=5)
        ttk.Button(tools_frame, text="Изменить размер", 
                  command=self.resize_image).pack(side="left", padx=5)
        ttk.Button(tools_frame, text="Повернуть", 
                  command=self.rotate_image).pack(side="left", padx=5)
    
    def load_image(self):
        """Загрузка изображения из файла"""
        try:
            from PIL import Image, ImageTk
            import tkinter.filedialog as fd
            
            file_path = fd.askopenfilename(
                title="Выберите изображение",
                filetypes=[
                    ("Изображения", "*.png *.jpg *.jpeg *.gif *.bmp"),
                    ("PNG", "*.png"),
                    ("JPG", "*.jpg *.jpeg"),
                    ("Все файлы", "*.*")
                ]
            )
            
            if file_path:
                # Загружаем изображение
                img = Image.open(file_path)
                
                # Масштабируем, если слишком большое
                max_size = (600, 400)
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                
                # Преобразуем для Tkinter
                self.loaded_photo = ImageTk.PhotoImage(img)
                
                # Обновляем Canvas (здесь потребуется ссылка на Canvas)
                print(f"Изображение загружено: {file_path}")
                print(f"Размер: {img.size}")
        except ImportError:
            print("Pillow не установлен. Установите с помощью: pip install Pillow")
    
    def save_image(self):
        """Сохранение изображения"""
        try:
            import tkinter.filedialog as fd
            
            file_path = fd.asksaveasfilename(
                title="Сохранить изображение",
                defaultextension=".png",
                filetypes=[
                    ("PNG", "*.png"),
                    ("JPEG", "*.jpg"),
                    ("GIF", "*.gif"),
                    ("Все файлы", "*.*")
                ]
            )
            
            if file_path:
                # Здесь должна быть реализация сохранения изображения
                print(f"Изображение сохранено: {file_path}")
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
    
    def resize_image(self):
        """Изменение размера изображения"""
        print("Изменение размера изображения")
        # Реализация изменения размера
    
    def rotate_image(self):
        """Поворот изображения"""
        print("Поворот изображения")
        # Реализация поворота

class ImageViewer:
    """Простой просмотрщик изображений"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Просмотрщик изображений")
        self.root.geometry("800x600")
        
        self.current_image = None
        self.image_path = None
        
        self.create_viewer_interface()
    
    def create_viewer_interface(self):
        # Меню
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Открыть", command=self.load_image, accelerator="Ctrl+O")
        file_menu.add_command(label="Сохранить", command=self.save_image, accelerator="Ctrl+S")
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        
        # Панель инструментов
        toolbar = tk.Frame(self.root, bg="lightgray", height=40)
        toolbar.pack(side="top", fill="x")
        
        tk.Button(toolbar, text="Открыть", command=self.load_image).pack(side="left", padx=2, pady=5)
        tk.Button(toolbar, text="Сохранить", command=self.save_image).pack(side="left", padx=2, pady=5)
        tk.Button(toolbar, text="Масштаб +", command=self.zoom_in).pack(side="left", padx=2, pady=5)
        tk.Button(toolbar, text="Масштаб -", command=self.zoom_out).pack(side="left", padx=2, pady=5)
        tk.Button(toolbar, text="Сброс", command=self.reset_zoom).pack(side="left", padx=2, pady=5)
        
        # Canvas для отображения изображения
        self.canvas = tk.Canvas(self.root, bg="gray")
        self.canvas.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Строка состояния
        self.status_bar = tk.Label(self.root, text="Готов", relief="sunken", anchor="w")
        self.status_bar.pack(side="bottom", fill="x")
        
        # Привязка горячих клавиш
        self.root.bind('<Control-o>', lambda e: self.load_image())
        self.root.bind('<Control-s>', lambda e: self.save_image())
        self.root.bind('<plus>', lambda e: self.zoom_in())
        self.root.bind('<minus>', lambda e: self.zoom_out())
    
    def load_image(self):
        """Загрузка изображения"""
        try:
            from PIL import Image, ImageTk
            import tkinter.filedialog as fd
            
            file_path = fd.askopenfilename(
                title="Выберите изображение",
                filetypes=[
                    ("Изображения", "*.png *.jpg *.jpeg *.gif *.bmp *.tiff"),
                    ("PNG", "*.png"),
                    ("JPEG", "*.jpg *.jpeg"),
                    ("GIF", "*.gif"),
                    ("Все файлы", "*.*")
                ]
            )
            
            if file_path:
                # Загружаем изображение
                self.original_image = Image.open(file_path)
                self.current_image = self.original_image.copy()
                self.image_path = file_path
                self.display_image()
                
                # Обновляем статус
                self.status_bar.config(text=f"Изображение: {file_path} | Размер: {self.original_image.size}")
        except ImportError:
            print("Pillow не установлен. Установите с помощью: pip install Pillow")
        except Exception as e:
            print(f"Ошибка загрузки изображения: {e}")
    
    def display_image(self):
        """Отображение изображения на Canvas"""
        if self.current_image:
            # Преобразуем изображение для Tkinter
            self.photo = ImageTk.PhotoImage(self.current_image)
            
            # Очищаем Canvas
            self.canvas.delete("all")
            
            # Отображаем изображение в центре Canvas
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            if canvas_width > 1 and canvas_height > 1:
                self.canvas.create_image(canvas_width//2, canvas_height//2, image=self.photo)
            else:
                # Если размеры Canvas еще не определены, используем фиксированные значения
                self.canvas.create_image(400, 300, image=self.photo)
    
    def zoom_in(self):
        """Увеличение изображения"""
        if self.current_image:
            # Увеличиваем на 25%
            width, height = self.current_image.size
            new_size = (int(width * 1.25), int(height * 1.25))
            self.current_image = self.original_image.resize(new_size, Image.Resampling.LANCZOS)
            self.display_image()
    
    def zoom_out(self):
        """Уменьшение изображения"""
        if self.current_image:
            # Уменьшаем на 20%
            width, height = self.current_image.size
            new_size = (int(width * 0.8), int(height * 0.8))
            self.current_image = self.original_image.resize(new_size, Image.Resampling.LANCZOS)
            self.display_image()
    
    def reset_zoom(self):
        """Сброс масштаба"""
        if self.original_image:
            self.current_image = self.original_image.copy()
            self.display_image()

root = tk.Tk()
app = ImageViewer(root)
root.mainloop()
```

---

## 6. Практические примеры

### Пример 1: Калькулятор с графическим интерфейсом

```python
import tkinter as tk
from tkinter import messagebox

class CalculatorGUI:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Калькулятор")
        self.window.geometry("300x400")
        self.window.resizable(False, False)
        
        # Переменные состояния
        self.current = "0"
        self.previous = ""
        self.operator = ""
        self.should_reset = False
        
        self.create_display()
        self.create_buttons()
        
    def create_display(self):
        # Дисплей калькулятора
        self.display_var = tk.StringVar(value="0")
        display = tk.Entry(
            self.window,
            textvariable=self.display_var,
            font=("Arial", 18),
            justify="right",
            state="readonly",
            readonlybackground="white",
            fg="black"
        )
        display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=5, pady=5)
    
    def create_buttons(self):
        # Определяем кнопки
        buttons = [
            ("C", 1, 0), ("±", 1, 1), ("%", 1, 2), ("÷", 1, 3),
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("×", 2, 3),
            ("4", 3, 0), ("5", 3, 1), ("6", 3, 2), ("-", 3, 3),
            ("1", 4, 0), ("2", 4, 1), ("3", 4, 2), ("+", 4, 3),
            ("0", 5, 0), (".", 5, 2), ("=", 5, 3)
        ]
        
        # Создаем кнопки
        for (text, row, col) in buttons:
            if text == "0":
                # Кнопка 0 занимает 2 колонки
                btn = tk.Button(
                    self.window,
                    text=text,
                    font=("Arial", 14),
                    command=lambda t=text: self.button_click(t)
                )
                btn.grid(row=row, column=col, columnspan=2, sticky="nsew", padx=2, pady=2)
            elif text == ".":
                # Кнопка точки
                btn = tk.Button(
                    self.window,
                    text=text,
                    font=("Arial", 14),
                    command=lambda t=text: self.button_click(t)
                )
                btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
            elif text == "=":
                # Кнопка равно
                btn = tk.Button(
                    self.window,
                    text=text,
                    font=("Arial", 14),
                    bg="orange",
                    fg="white",
                    command=lambda t=text: self.button_click(t)
                )
                btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
            else:
                # Обычные кнопки
                btn = tk.Button(
                    self.window,
                    text=text,
                    font=("Arial", 14),
                    command=lambda t=text: self.button_click(t)
                )
                if text in "C±%":
                    btn.config(bg="lightgray")
                elif text in "÷×-+":
                    btn.config(bg="orange", fg="white")
                
                btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
        
        # Настройка растягивания сетки
        for i in range(6):
            self.window.rowconfigure(i, weight=1)
        for j in range(4):
            self.window.columnconfigure(j, weight=1)
    
    def button_click(self, value):
        if value.isdigit() or value == ".":
            self.input_number(value)
        elif value in "+-×÷":
            self.input_operator(value)
        elif value == "=":
            self.calculate()
        elif value == "C":
            self.clear()
        elif value == "±":
            self.change_sign()
        elif value == "%":
            self.percentage()
    
    def input_number(self, number):
        if self.should_reset:
            self.current = "0"
            self.should_reset = False
        
        if self.current == "0" and number != ".":
            self.current = number
        elif number == "." and "." not in self.current:
            self.current += number
        elif number != ".":
            self.current += number
        
        self.display_var.set(self.current)
    
    def input_operator(self, operator):
        if self.operator and not self.should_reset:
            self.calculate()
        
        self.previous = self.current
        self.operator = operator
        self.should_reset = True
    
    def calculate(self):
        if self.operator and self.previous:
            try:
                prev_num = float(self.previous)
                curr_num = float(self.current)
                
                if self.operator == "+":
                    result = prev_num + curr_num
                elif self.operator == "-":
                    result = prev_num - curr_num
                elif self.operator == "×":
                    result = prev_num * curr_num
                elif self.operator == "÷":
                    if curr_num == 0:
                        raise ZeroDivisionError("Деление на ноль")
                    result = prev_num / curr_num
                
                # Форматируем результат
                if result.is_integer():
                    result = int(result)
                
                self.current = str(result)
                self.display_var.set(self.current)
                self.operator = ""
                self.previous = ""
                self.should_reset = True
            except ZeroDivisionError:
                messagebox.showerror("Ошибка", "Деление на ноль невозможно!")
                self.clear()
            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка вычисления: {str(e)}")
                self.clear()
    
    def clear(self):
        self.current = "0"
        self.previous = ""
        self.operator = ""
        self.should_reset = False
        self.display_var.set(self.current)
    
    def change_sign(self):
        if self.current != "0":
            if self.current.startswith("-"):
                self.current = self.current[1:]
            else:
                self.current = "-" + self.current
            self.display_var.set(self.current)
    
    def percentage(self):
        try:
            result = float(self.current) / 100
            if result.is_integer():
                result = int(result)
            self.current = str(result)
            self.display_var.set(self.current)
        except:
            pass
    
    def run(self):
        self.window.mainloop()

# Запуск калькулятора
if __name__ == "__main__":
    calc = CalculatorGUI()
    calc.run()
```

### Пример 2: Текстовый редактор

```python
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os

class TextEditor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Текстовый редактор")
        self.root.geometry("800x600")
        
        self.current_file = None
        self.text_changed = False
        
        self.create_menu()
        self.create_toolbar()
        self.create_text_area()
        self.create_status_bar()
        self.setup_bindings()
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Меню "Файл"
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        
        file_menu.add_command(label="Новый", command=self.new_file, accelerator="Ctrl+N")
        file_menu.add_command(label="Открыть", command=self.open_file, accelerator="Ctrl+O")
        file_menu.add_command(label="Сохранить", command=self.save_file, accelerator="Ctrl+S")
        file_menu.add_command(label="Сохранить как...", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.exit_app, accelerator="Alt+F4")
        
        # Меню "Правка"
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Правка", menu=edit_menu)
        
        edit_menu.add_command(label="Отменить", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Повторить", command=self.redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Вырезать", command=self.cut, accelerator="Ctrl+X")
        edit_menu.add_command(label="Копировать", command=self.copy, accelerator="Ctrl+C")
        edit_menu.add_command(label="Вставить", command=self.paste, accelerator="Ctrl+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Найти", command=self.find_text, accelerator="Ctrl+F")
        edit_menu.add_command(label="Заменить", command=self.replace_text, accelerator="Ctrl+H")
        edit_menu.add_separator()
        edit_menu.add_command(label="Выделить все", command=self.select_all, accelerator="Ctrl+A")
        
        # Меню "Вид"
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Вид", menu=view_menu)
        
        self.show_toolbar_var = tk.BooleanVar(value=True)
        view_menu.add_checkbutton(label="Панель инструментов", 
                                 variable=self.show_toolbar_var, 
                                 command=self.toggle_toolbar)
        
        self.show_status_bar_var = tk.BooleanVar(value=True)
        view_menu.add_checkbutton(label="Строка состояния", 
                                 variable=self.show_status_bar_var, 
                                 command=self.toggle_status_bar)
    
    def create_toolbar(self):
        self.toolbar = tk.Frame(self.root, bg="lightgray", height=40, relief="raised", bd=1)
        self.toolbar.pack(side="top", fill="x")
        
        # Кнопки панели инструментов
        tk.Button(self.toolbar, text="Новый", command=self.new_file).pack(side="left", padx=2, pady=5)
        tk.Button(self.toolbar, text="Открыть", command=self.open_file).pack(side="left", padx=2, pady=5)
        tk.Button(self.toolbar, text="Сохранить", command=self.save_file).pack(side="left", padx=2, pady=5)
        
        tk.Frame(self.toolbar, width=2, bg="gray").pack(side="left", fill="y", padx=5, pady=5)  # Разделитель
        
        tk.Button(self.toolbar, text="Вырезать", command=self.cut).pack(side="left", padx=2, pady=5)
        tk.Button(self.toolbar, text="Копировать", command=self.copy).pack(side="left", padx=2, pady=5)
        tk.Button(self.toolbar, text="Вставить", command=self.paste).pack(side="left", padx=2, pady=5)
    
    def create_text_area(self):
        # Создаем фрейм для текстовой области с прокруткой
        text_frame = tk.Frame(self.root)
        text_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Текстовая область
        self.text_area = tk.Text(
            text_frame,
            wrap=tk.WORD,
            undo=True,
            font=("Consolas", 11),
            padx=10,
            pady=10
        )
        
        # Прокрутка
        v_scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=self.text_area.yview)
        h_scrollbar = tk.Scrollbar(text_frame, orient="horizontal", command=self.text_area.xview)
        
        self.text_area.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Упаковка элементов
        self.text_area.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        # Настройка растягивания
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)
    
    def create_status_bar(self):
        self.status_bar = tk.Label(
            self.root, 
            text="Готов", 
            relief=tk.SUNKEN, 
            anchor=tk.W,
            bg="lightgray"
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def setup_bindings(self):
        # Привязка горячих клавиш
        self.root.bind('<Control-n>', lambda e: self.new_file())
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-s>', lambda e: self.save_file())
        self.root.bind('<Control-f>', lambda e: self.find_text())
        self.root.bind('<Control-h>', lambda e: self.replace_text())
        self.root.bind('<Control-a>', lambda e: self.select_all())
        self.root.bind('<Alt-F4>', lambda e: self.exit_app())
        
        # Отслеживание изменений текста
        self.text_area.bind("<<Modified>>", self.on_text_modified)
    
    def on_text_modified(self, event=None):
        if self.text_area.edit_modified():
            self.text_changed = True
            self.update_title()
            self.text_area.edit_modified(False)
    
    def update_title(self):
        title = "Текстовый редактор"
        if self.current_file:
            title += f" - {os.path.basename(self.current_file)}"
        if self.text_changed:
            title += " *"
        self.root.title(title)
    
    def new_file(self):
        if self.text_changed:
            self.ask_save_changes()
        
        self.text_area.delete(1.0, tk.END)
        self.current_file = None
        self.text_changed = False
        self.update_title()
        self.status_bar.config(text="Создан новый файл")
    
    def open_file(self):
        if self.text_changed:
            if self.ask_save_changes() == "cancel":
                return
        
        file_path = filedialog.askopenfilename(
            title="Открыть файл",
            filetypes=[
                ("Текстовые файлы", "*.txt"),
                ("Python файлы", "*.py"),
                ("HTML файлы", "*.html"),
                ("Все файлы", "*.*")
            ]
        )
        
        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    content = file.read()
                
                self.text_area.delete(1.0, tk.END)
                self.text_area.insert(1.0, content)
                
                self.current_file = file_path
                self.text_changed = False
                self.update_title()
                
                self.status_bar.config(text=f"Открыт файл: {file_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось открыть файл:\n{str(e)}")
    
    def save_file(self):
        if self.current_file:
            try:
                content = self.text_area.get(1.0, tk.END + "-1c")
                with open(self.current_file, 'w', encoding='utf-8') as file:
                    file.write(content)
                
                self.text_changed = False
                self.update_title()
                self.status_bar.config(text=f"Файл сохранен: {self.current_file}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")
        else:
            self.save_as_file()
    
    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(
            title="Сохранить файл как",
            defaultextension=".txt",
            filetypes=[
                ("Текстовые файлы", "*.txt"),
                ("Python файлы", "*.py"),
                ("HTML файлы", "*.html"),
                ("Все файлы", "*.*")
            ]
        )
        
        if file_path:
            try:
                content = self.text_area.get(1.0, tk.END + "-1c")
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                
                self.current_file = file_path
                self.text_changed = False
                self.update_title()
                
                self.status_bar.config(text=f"Файл сохранен: {file_path}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл:\n{str(e)}")
    
    def exit_app(self):
        if self.text_changed:
            result = self.ask_save_changes()
            if result == "cancel":
                return
        
        self.root.quit()
    
    def ask_save_changes(self):
        result = messagebox.askyesnocancel(
            "Сохранить изменения",
            "Сохранить изменения перед закрытием?"
        )
        
        if result is True:  # Да
            self.save_file()
            if self.text_changed:  # Если сохранение не удалось
                return "cancel"
        elif result is False:  # Нет
            pass
        else:  # Отмена
            return "cancel"
    
    def undo(self):
        try:
            self.text_area.edit_undo()
        except tk.TclError:
            pass
    
    def redo(self):
        try:
            self.text_area.edit_redo()
        except tk.TclError:
            pass
    
    def cut(self):
        self.text_area.event_generate("<<Cut>>")
    
    def copy(self):
        self.text_area.event_generate("<<Copy>>")
    
    def paste(self):
        self.text_area.event_generate("<<Paste>>")
    
    def select_all(self):
        self.text_area.tag_add(tk.SEL, "1.0", tk.END)
        self.text_area.mark_set(tk.INSERT, "1.0")
        self.text_area.see(tk.INSERT)
        return "break"
    
    def find_text(self):
        # Простой поиск текста
        search_term = simpledialog.askstring("Найти", "Введите текст для поиска:")
        if search_term:
            # Очищаем предыдущие выделения
            self.text_area.tag_remove("found", "1.0", tk.END)
            
            start_pos = "1.0"
            while True:
                pos = self.text_area.search(search_term, start_pos, tk.END)
                if not pos:
                    break
                
                end_pos = f"{pos}+{len(search_term)}c"
                self.text_area.tag_add("found", pos, end_pos)
                start_pos = end_pos
            
            # Настройка выделения
            self.text_area.tag_config("found", background="yellow", foreground="black")
    
    def replace_text(self):
        # Простая замена текста
        find_text = simpledialog.askstring("Найти", "Введите текст для поиска:")
        if find_text:
            replace_text = simpledialog.askstring("Заменить", "Введите текст для замены:")
            if replace_text is not None:
                content = self.text_area.get("1.0", tk.END)
                new_content = content.replace(find_text, replace_text)
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert("1.0", new_content)
    
    def toggle_toolbar(self):
        if self.show_toolbar_var.get():
            self.toolbar.pack(side="top", fill="x")
        else:
            self.toolbar.pack_forget()
    
    def toggle_status_bar(self):
        if self.show_status_bar_var.get():
            self.status_bar.pack(side="bottom", fill="x")
        else:
            self.status_bar.pack_forget()
    
    def run(self):
        self.root.mainloop()

# Запуск текстового редактора
if __name__ == "__main__":
    editor = TextEditor()
    editor.run()
```

---

## Заключение

Tkinter предоставляет мощный инструментарий для создания графических интерфейсов в Python. В этой лекции мы рассмотрели:
1. Основы создания окон и виджетов
2. Использование различных менеджеров компоновки
3. Работу с событиями и обработчиками
4. Создание сложных интерфейсов с использованием разных типов виджетов
5. Работу с изображениями
6. Практические примеры приложений

Tkinter особенно полезен для создания настольных приложений, инструментов автоматизации и служебных программ, где не требуется очень современный внешний вид.

## Контрольные вопросы:
1. Какие менеджеры компоновки доступны в Tkinter?
2. В чем разница между pack, grid и place?
3. Как обрабатываются события в Tkinter?
4. Как создать диалоговое окно в Tkinter?
5. Как работать с изображениями в Tkinter?
