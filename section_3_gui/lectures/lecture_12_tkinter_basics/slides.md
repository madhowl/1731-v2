# Лекция 12: Tkinter - основы

## Создание окон, виджеты, события, размещение элементов

### План лекции:
1. Введение в Tkinter
2. Создание окон
3. Основные виджеты Tkinter
4. События и обработчики
5. Размещение элементов (geometry managers)
6. Практические примеры

---

## 1. Введение в Tkinter

### Что такое Tkinter?

Tkinter - это стандартный интерфейс Python к библиотеке Tcl/Tk, которая используется для создания графических пользовательских интерфейсов. Tkinter входит в стандартную библиотеку Python, что делает его наиболее доступным вариантом для создания GUI-приложений.

```python
import tkinter as tk

# Простейшее приложение Tkinter
root = tk.Tk()  # Создание главного окна
root.title("Мое первое приложение")  # Заголовок окна
root.geometry("400x300")  # Размеры окна (ширина x высота)

# Запуск главного цикла событий
root.mainloop()
```

### Основные понятия Tkinter:

- **Widget (виджет)** - графический элемент интерфейса (кнопка, метка, поле ввода и т.д.)
- **Master/Parent widget** - родительский виджет, в котором размещаются другие виджеты
- **Event loop** - цикл событий, который обрабатывает действия пользователя
- **Geometry manager** - менеджер размещения, который определяет, где размещать виджеты

---

## 2. Создание окон

### Основное окно (Root Window)

```python
import tkinter as tk

class MainApplication:
    def __init__(self):
        # Создание основного окна
        self.root = tk.Tk()
        self.root.title("Главное окно приложения")
        self.root.geometry("600x400")
        
        # Настройки окна
        self.root.resizable(True, True)  # Разрешить изменение размера
        self.root.minsize(400, 300)      # Минимальный размер
        self.root.configure(bg="#f0f0f0")  # Цвет фона
        
        # Центрирование окна на экране
        self.center_window()
        
        # Добавление содержимого
        self.create_widgets()
    
    def center_window(self):
        """Центрирование окна на экране"""
        self.root.update_idletasks()  # Обновление окна перед расчетом
        
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def create_widgets(self):
        """Создание виджетов приложения"""
        # Метка с приветствием
        label = tk.Label(self.root, text="Добро пожаловать в приложение!", 
                        font=("Arial", 16), fg="blue", bg="#f0f0f0")
        label.pack(pady=20)
    
    def run(self):
        """Запуск приложения"""
        self.root.mainloop()

# Запуск приложения
if __name__ == "__main__":
    app = MainApplication()
    app.run()
```

### Дочерние окна (Toplevel)

```python
import tkinter as tk
from tkinter import messagebox

class ApplicationWithDialogs:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Приложение с диалогами")
        self.root.geometry("400x300")
        
        self.create_main_widgets()
    
    def create_main_widgets(self):
        # Кнопка для открытия дочернего окна
        dialog_btn = tk.Button(self.root, text="Открыть диалог", 
                              command=self.open_dialog)
        dialog_btn.pack(pady=20)
        
        # Кнопка для открытия сообщения
        msg_btn = tk.Button(self.root, text="Показать сообщение", 
                           command=self.show_message)
        msg_btn.pack(pady=10)
    
    def open_dialog(self):
        """Открытие дочернего окна"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Диалоговое окно")
        dialog.geometry("300x200")
        dialog.transient(self.root)  # Окно поверх основного
        dialog.grab_set()  # Блокировка основного окна
        
        # Содержимое диалога
        label = tk.Label(dialog, text="Это дочернее окно")
        label.pack(pady=20)
        
        close_btn = tk.Button(dialog, text="Закрыть", 
                             command=dialog.destroy)
        close_btn.pack(pady=10)
    
    def show_message(self):
        """Показать диалоговое сообщение"""
        messagebox.showinfo("Информация", "Это информационное сообщение!")
    
    def run(self):
        self.root.mainloop()

# Запуск приложения
if __name__ == "__main__":
    app = ApplicationWithDialogs()
    app.run()
```

---

## 3. Основные виджеты Tkinter

### Метки (Label)

```python
import tkinter as tk

root = tk.Tk()
root.title("Метки в Tkinter")
root.geometry("500x400")

# Простая метка
simple_label = tk.Label(root, text="Простая метка")
simple_label.pack(pady=5)

# Метка с настройками
styled_label = tk.Label(
    root,
    text="Стилизованная метка",
    font=("Arial", 14, "bold"),
    fg="white",
    bg="navy",
    padx=20,
    pady=10
)
styled_label.pack(pady=5)

# Метка с изображением
# photo = tk.PhotoImage(file="image.png")  # Путь к изображению
# img_label = tk.Label(root, image=photo)
# img_label.pack(pady=5)

# Многострочная метка
multiline_label = tk.Label(
    root,
    text="Это многострочная\nметка с переносом\nтекста",
    justify=tk.LEFT,
    relief=tk.RAISED,
    bd=2
)
multiline_label.pack(pady=5)

root.mainloop()
```

### Кнопки (Button)

```python
import tkinter as tk

root = tk.Tk()
root.title("Кнопки в Tkinter")
root.geometry("500x400")

# Простая кнопка
def simple_callback():
    print("Кнопка нажата!")

simple_btn = tk.Button(root, text="Простая кнопка", command=simple_callback)
simple_btn.pack(pady=5)

# Стилизованная кнопка
styled_btn = tk.Button(
    root,
    text="Стилизованная кнопка",
    font=("Arial", 12, "italic"),
    fg="white",
    bg="red",
    activebackground="darkred",
    activeforeground="white",
    padx=20,
    pady=10
)
styled_btn.pack(pady=5)

# Кнопка с изображением
# photo = tk.PhotoImage(file="icon.png")  # Путь к иконке
# img_btn = tk.Button(root, image=photo, command=simple_callback)
# img_btn.pack(pady=5)

# Кнопка-переключатель (кнопка с изменяющимся текстом)
state = True
def toggle_button():
    global state
    state = not state
    toggle_btn.config(text="Вкл" if state else "Выкл")

toggle_btn = tk.Button(root, text="Выкл", width=10, command=toggle_button)
toggle_btn.pack(pady=5)

# Кнопка с подсказкой (используя всплывающее окно)
def show_tooltip(event):
    tooltip = tk.Toplevel()
    tooltip.wm_overrideredirect(True)
    tooltip.geometry(f"+{event.x_root+10}+{event.y_root+10}")
    label = tk.Label(tooltip, text="Это подсказка", bg="yellow", relief="solid")
    label.pack()
    
    def hide_tooltip(event):
        tooltip.destroy()
    
    toggle_btn.bind("<Leave>", hide_tooltip)

toggle_btn.bind("<Enter>", show_tooltip)

root.mainloop()
```

### Поля ввода (Entry и Text)

```python
import tkinter as tk

root = tk.Tk()
root.title("Поля ввода в Tkinter")
root.geometry("600x500")

# Поле ввода одной строки (Entry)
tk.Label(root, text="Поле ввода (Entry):").pack(anchor="w", padx=10, pady=5)
entry = tk.Entry(root, width=30)
entry.pack(padx=10, pady=5)

# Поле ввода с маской (для паролей)
tk.Label(root, text="Поле ввода пароля:").pack(anchor="w", padx=10, pady=5)
password_entry = tk.Entry(root, width=30, show="*")
password_entry.pack(padx=10, pady=5)

# Текстовое поле (Text) - многострочный ввод
tk.Label(root, text="Текстовое поле (Text):").pack(anchor="w", padx=10, pady=5)
text_area = tk.Text(root, height=8, width=50)
text_area.pack(padx=10, pady=5)

# Кнопки для работы с текстом
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

def get_text():
    content = text_area.get("1.0", tk.END)  # Получить весь текст
    print("Содержимое текстового поля:")
    print(content)

def insert_text():
    text_area.insert(tk.END, "\nДобавленный текст")

def clear_text():
    text_area.delete("1.0", tk.END)  # Очистить всё содержимое

tk.Button(button_frame, text="Получить текст", command=get_text).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Вставить текст", command=insert_text).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Очистить", command=clear_text).pack(side=tk.LEFT, padx=5)

# Поле ввода с прокруткой
tk.Label(root, text="Текстовое поле с прокруткой:").pack(anchor="w", padx=10, pady=5)

text_frame = tk.Frame(root)
text_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

scrollable_text = tk.Text(text_frame, height=6, wrap=tk.WORD)
scrollbar = tk.Scrollbar(text_frame, orient=tk.VERTICAL, command=scrollable_text.yview)
scrollable_text.configure(yscrollcommand=scrollbar.set)

scrollable_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

root.mainloop()
```

### Флажки и переключатели (Checkbutton, Radiobutton)

```python
import tkinter as tk

root = tk.Tk()
root.title("Флажки и переключатели")
root.geometry("600x400")

# Фрейм для флажков
check_frame = tk.LabelFrame(root, text="Флажки (Checkbuttons)", padx=10, pady=10)
check_frame.pack(fill="x", padx=10, pady=10)

# Переменные для флажков
var1 = tk.BooleanVar()
var2 = tk.BooleanVar()
var3 = tk.IntVar()  # Также может быть IntVar

tk.Checkbutton(check_frame, text="Первый вариант", variable=var1).pack(anchor="w")
tk.Checkbutton(check_frame, text="Второй вариант", variable=var2).pack(anchor="w")
tk.Checkbutton(check_frame, text="Третий вариант", variable=var3, onvalue=1, offvalue=0).pack(anchor="w")

# Фрейм для переключателей
radio_frame = tk.LabelFrame(root, text="Переключатели (Radiobuttons)", padx=10, pady=10)
radio_frame.pack(fill="x", padx=10, pady=10)

# Переменная для группы переключателей
selected_option = tk.StringVar(value="option1")

tk.Radiobutton(radio_frame, text="Вариант 1", variable=selected_option, value="option1").pack(anchor="w")
tk.Radiobutton(radio_frame, text="Вариант 2", variable=selected_option, value="option2").pack(anchor="w")
tk.Radiobutton(radio_frame, text="Вариант 3", variable=selected_option, value="option3").pack(anchor="w")

# Кнопка для получения значений
def get_values():
    print(f"Флажки: {var1.get()}, {var2.get()}, {var3.get()}")
    print(f"Переключатель: {selected_option.get()}")

tk.Button(root, text="Получить значения", command=get_values).pack(pady=20)

root.mainloop()
```

---

## 4. События и обработчики

### Обработка событий мыши и клавиатуры

```python
import tkinter as tk

class EventHandlingDemo:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Обработка событий")
        self.root.geometry("600x500")
        
        # Метка для отображения событий
        self.event_label = tk.Label(self.root, text="События будут отображаться здесь", 
                                   bg="lightgray", height=5)
        self.event_label.pack(fill="x", padx=10, pady=10)
        
        # Фрейм для демонстрации событий
        self.canvas = tk.Canvas(self.root, bg="white", width=500, height=300)
        self.canvas.pack(padx=10, pady=10)
        
        # Привязка событий
        self.bind_events()
        
        # Кнопка для демонстрации горячих клавиш
        self.shortcut_btn = tk.Button(self.root, text="Кнопка (Ctrl+B)", 
                                     command=self.button_clicked)
        self.shortcut_btn.pack(pady=10)
        
        # Поле ввода для демонстрации событий клавиатуры
        self.entry = tk.Entry(self.root, width=50)
        self.entry.pack(pady=5)
        self.entry.bind("<KeyRelease>", self.on_key_release)
    
    def bind_events(self):
        # События мыши
        self.canvas.bind("<Button-1>", self.left_click)      # Левая кнопка
        self.canvas.bind("<Button-3>", self.right_click)     # Правая кнопка
        self.canvas.bind("<Motion>", self.mouse_move)        # Движение мыши
        self.canvas.bind("<Double-Button-1>", self.double_click)  # Двойной клик
        
        # События клавиатуры
        self.root.bind("<KeyPress>", self.key_press)
        self.root.bind("<Control-b>", self.ctrl_b_pressed)   # Горячая клавиша
        
        # События окна
        self.root.bind("<FocusIn>", self.focus_in)
        self.root.bind("<FocusOut>", self.focus_out)
    
    def left_click(self, event):
        self.event_label.config(text=f"Левый клик: ({event.x}, {event.y})")
        self.canvas.create_oval(event.x-5, event.y-5, event.x+5, event.y+5, 
                               fill="red", outline="black")
    
    def right_click(self, event):
        self.event_label.config(text=f"Правый клик: ({event.x}, {event.y})")
        self.canvas.create_rectangle(event.x-10, event.y-10, event.x+10, event.y+10, 
                                    fill="blue", outline="black")
    
    def mouse_move(self, event):
        # Обновляем текст каждые 50 движений для избежания перегрузки
        if event.x % 5 == 0 and event.y % 5 == 0:  # Упрощенная проверка
            self.event_label.config(text=f"Позиция мыши: ({event.x}, {event.y})")
    
    def double_click(self, event):
        self.event_label.config(text=f"Двойной клик: ({event.x}, {event.y})")
        self.canvas.delete("all")  # Очистить холст
    
    def key_press(self, event):
        self.event_label.config(text=f"Клавиша: {event.keysym}, Код: {event.keycode}")
    
    def ctrl_b_pressed(self, event):
        self.event_label.config(text="Нажата комбинация Ctrl+B")
        self.shortcut_btn.config(bg="yellow")
        self.root.after(500, lambda: self.shortcut_btn.config(bg="SystemButtonFace"))
        return "break"  # Предотвратить дальнейшую обработку события
    
    def button_clicked(self):
        self.event_label.config(text="Кнопка нажата")
    
    def on_key_release(self, event):
        self.event_label.config(text=f"Отпущена клавиша: {event.keysym}")
    
    def focus_in(self, event):
        self.event_label.config(text="Окно получило фокус")
    
    def focus_out(self, event):
        self.event_label.config(text="Окно потеряло фокус")
    
    def run(self):
        self.root.mainloop()

# Запуск демонстрации событий
if __name__ == "__main__":
    app = EventHandlingDemo()
    app.run()
```

### Контекстное меню

```python
import tkinter as tk

class ContextMenuDemo:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Контекстное меню")
        self.root.geometry("500x400")
        
        # Создание контекстного меню
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Копировать", command=self.copy_text)
        self.context_menu.add_command(label="Вставить", command=self.paste_text)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Очистить", command=self.clear_text)
        
        # Текстовое поле
        self.text_area = tk.Text(self.root, height=15, width=60)
        self.text_area.pack(padx=10, pady=10)
        
        # Привязка правой кнопки мыши к вызову контекстного меню
        self.text_area.bind("<Button-3>", self.show_context_menu)
        # Также работает на macOS с Control-клик
        self.text_area.bind("<Control-Button-1>", self.show_context_menu)
    
    def show_context_menu(self, event):
        """Показать контекстное меню"""
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    def copy_text(self):
        """Копировать выделенный текст"""
        try:
            selected_text = self.text_area.get(tk.SEL_FIRST, tk.SEL_LAST)
            self.root.clipboard_clear()
            self.root.clipboard_append(selected_text)
        except tk.TclError:
            # Нет выделенного текста
            pass
    
    def paste_text(self):
        """Вставить текст из буфера"""
        try:
            clipboard_text = self.root.clipboard_get()
            self.text_area.insert(tk.INSERT, clipboard_text)
        except tk.TclError:
            # Буфер пуст
            pass
    
    def clear_text(self):
        """Очистить текстовое поле"""
        self.text_area.delete(1.0, tk.END)
    
    def run(self):
        self.root.mainloop()

# Запуск демонстрации контекстного меню
if __name__ == "__main__":
    app = ContextMenuDemo()
    app.run()
```

---

## 5. Размещение элементов (Geometry Managers)

### Pack Manager

```python
import tkinter as tk

root = tk.Tk()
root.title("Pack Manager")
root.geometry("500x400")

# Пример 1: Простое размещение
tk.Label(root, text="Label 1", bg="red", fg="white").pack()
tk.Label(root, text="Label 2", bg="green", fg="white").pack()
tk.Label(root, text="Label 3", bg="blue", fg="white").pack()

# Пример 2: Размещение с параметрами
frame1 = tk.Frame(root, bg="lightgray", height=100)
frame1.pack(fill="x", padx=10, pady=5)

tk.Label(frame1, text="Слева", bg="yellow").pack(side="left", padx=5)
tk.Label(frame1, text="По центру", bg="orange").pack(side="left", padx=5)
tk.Label(frame1, text="Справа", bg="purple", fg="white").pack(side="right", padx=5)

# Пример 3: Заполнение пространства
frame2 = tk.Frame(root, bg="lightblue", height=150)
frame2.pack(fill="both", expand=True, padx=10, pady=5)

tk.Label(frame2, text="Растянутый Label", bg="pink").pack(fill="both", expand=True, padx=10, pady=10)

root.mainloop()
```

### Grid Manager

```python
import tkinter as tk

root = tk.Tk()
root.title("Grid Manager")
root.geometry("600x500")

# Создание формы входа
tk.Label(root, text="Форма входа", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=20)

# Поля ввода
tk.Label(root, text="Имя пользователя:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
username_entry = tk.Entry(root, width=30)
username_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Label(root, text="Пароль:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
password_entry = tk.Entry(root, width=30, show="*")
password_entry.grid(row=2, column=1, padx=5, pady=5)

# Чекбоксы
remember_var = tk.BooleanVar()
tk.Checkbutton(root, text="Запомнить меня", variable=remember_var).grid(row=3, column=1, sticky="w", padx=5, pady=5)

# Кнопки
button_frame = tk.Frame(root)
button_frame.grid(row=4, column=0, columnspan=2, pady=20)

tk.Button(button_frame, text="Вход", bg="lightgreen").pack(side="left", padx=5)
tk.Button(button_frame, text="Отмена", bg="lightcoral").pack(side="left", padx=5)

# Таблица данных
tk.Label(root, text="Таблица данных", font=("Arial", 14)).grid(row=5, column=0, columnspan=2, pady=20)

# Заголовки таблицы
headers = ["Имя", "Возраст", "Город"]
for col, header in enumerate(headers):
    tk.Label(root, text=header, relief="raised", bg="lightgray", font=("Arial", 10, "bold")).grid(row=6, column=col, sticky="ew", padx=1, pady=1)

# Данные таблицы
data = [
    ["Иван", "25", "Москва"],
    ["Мария", "30", "СПб"],
    ["Алексей", "22", "Новосибирск"]
]

for row_idx, row_data in enumerate(data):
    for col_idx, cell_data in enumerate(row_data):
        tk.Label(root, text=cell_data, relief="sunken", padx=5, pady=2).grid(row=7+row_idx, column=col_idx, sticky="ew", padx=1, pady=1)

# Настройка растягивания колонок
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=1)

root.mainloop()
```

### Place Manager

```python
import tkinter as tk

root = tk.Tk()
root.title("Place Manager")
root.geometry("600x400")
root.configure(bg="lightgray")

# Пример использования Place для точного позиционирования
label1 = tk.Label(root, text="Label 1", bg="red", fg="white", padx=20, pady=10)
label1.place(x=50, y=50)

label2 = tk.Label(root, text="Label 2", bg="green", fg="white", padx=20, pady=10)
label2.place(relx=0.5, rely=0.3, anchor="center")  # По центру по горизонтали, на 30% по вертикали

label3 = tk.Label(root, text="Label 3", bg="blue", fg="white", padx=20, pady=10)
label3.place(relx=1.0, rely=0.0, anchor="ne")  # В правом верхнем углу

# Кнопка в правом нижнем углу
button = tk.Button(root, text="Кнопка", bg="yellow")
button.place(relx=1.0, rely=1.0, anchor="se")  # В правом нижнем углу

# Круговая диаграмма (упрощенная)
canvas = tk.Canvas(root, width=200, height=200, bg="white", highlightthickness=2)
canvas.place(relx=0.5, rely=0.7, anchor="center")

# Рисование сегментов круговой диаграммы
canvas.create_arc(20, 20, 180, 180, start=0, extent=120, fill="red", outline="black")
canvas.create_arc(20, 20, 180, 180, start=120, extent=120, fill="green", outline="black")
canvas.create_arc(20, 20, 180, 180, start=240, extent=120, fill="blue", outline="black")

root.mainloop()
```

### Комбинация менеджеров размещения

```python
import tkinter as tk

class LayoutCombinationDemo:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Комбинация менеджеров размещения")
        self.root.geometry("800x600")
        
        self.create_layout()
    
    def create_layout(self):
        # Основной фрейм с pack
        main_frame = tk.Frame(self.root, bg="lightgray")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Верхняя панель с pack
        top_panel = tk.Frame(main_frame, bg="navy", height=50)
        top_panel.pack(fill="x")
        
        tk.Label(top_panel, text="Верхняя панель", fg="white", bg="navy", font=("Arial", 12)).pack(pady=10)
        
        # Центральная область с grid
        center_frame = tk.Frame(main_frame, bg="lightblue")
        center_frame.pack(fill="both", expand=True, pady=5)
        
        # Использование grid внутри центральной области
        for i in range(3):
            for j in range(3):
                btn = tk.Button(center_frame, text=f"Кнопка {i},{j}", width=10, height=2)
                btn.grid(row=i, column=j, padx=5, pady=5, sticky="nsew")
        
        # Настройка растягивания ячеек grid
        for i in range(3):
            center_frame.grid_rowconfigure(i, weight=1)
            center_frame.grid_columnconfigure(i, weight=1)
        
        # Нижняя панель с place
        bottom_frame = tk.Frame(main_frame, bg="darkgreen", height=100)
        bottom_frame.pack(fill="x", pady=(5, 0))
        
        # Внутри нижней панели используем place для точного позиционирования
        left_label = tk.Label(bottom_frame, text="Слева", bg="darkgreen", fg="white")
        left_label.place(relx=0.1, rely=0.5, anchor="center")
        
        center_label = tk.Label(bottom_frame, text="По центру", bg="darkgreen", fg="white")
        center_label.place(relx=0.5, rely=0.5, anchor="center")
        
        right_label = tk.Label(bottom_frame, text="Справа", bg="darkgreen", fg="white")
        right_label.place(relx=0.9, rely=0.5, anchor="center")
        
        # Кнопка в правом углу
        corner_btn = tk.Button(bottom_frame, text="Угол", bg="red", fg="white")
        corner_btn.place(relx=0.98, rely=0.95, anchor="se")
    
    def run(self):
        self.root.mainloop()

# Запуск демонстрации комбинации менеджеров
if __name__ == "__main__":
    app = LayoutCombinationDemo()
    app.run()
```

---

## 6. Практические примеры

### Пример 1: Простой калькулятор

```python
import tkinter as tk
from tkinter import messagebox

class SimpleCalculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Простой калькулятор")
        self.root.geometry("300x400")
        self.root.resizable(False, False)
        
        self.current_input = ""
        self.result_display = tk.StringVar(value="0")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Дисплей результата
        display_frame = tk.Frame(self.root)
        display_frame.pack(expand=True, fill="both")
        
        display = tk.Label(
            display_frame,
            textvariable=self.result_display,
            font=("Arial", 18),
            anchor="e",
            bg="white",
            fg="black",
            padx=10
        )
        display.pack(expand=True, fill="both", padx=5, pady=5)
        
        # Кнопки калькулятора
        buttons_frame = tk.Frame(self.root)
        buttons_frame.pack(expand=True, fill="both")
        
        # Определение кнопок
        buttons = [
            ['C', '±', '%', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '=']
        ]
        
        # Создание кнопок
        for i, row in enumerate(buttons):
            for j, text in enumerate(row):
                if text == '0':
                    # Кнопка 0 занимает 2 колонки
                    btn = tk.Button(
                        buttons_frame,
                        text=text,
                        font=("Arial", 14),
                        command=lambda t=text: self.button_click(t)
                    )
                    btn.grid(row=i, column=j, columnspan=2, sticky="nsew", padx=2, pady=2)
                elif text == '=':
                    # Кнопка = занимает 1 строку и 1 колонку
                    btn = tk.Button(
                        buttons_frame,
                        text=text,
                        font=("Arial", 14),
                        bg="orange",
                        fg="white",
                        command=lambda t=text: self.button_click(t)
                    )
                    btn.grid(row=i, column=j+1, rowspan=1, sticky="nsew", padx=2, pady=2)
                else:
                    btn = tk.Button(
                        buttons_frame,
                        text=text,
                        font=("Arial", 14),
                        command=lambda t=text: self.button_click(t)
                    )
                    if text in ['C', '±', '%']:
                        btn.config(bg="lightgray")
                    elif text in ['÷', '×', '-', '+', '=']:
                        btn.config(bg="orange", fg="white")
                    
                    btn.grid(row=i, column=j, sticky="nsew", padx=2, pady=2)
        
        # Настройка растягивания сетки
        for i in range(5):
            buttons_frame.rowconfigure(i, weight=1)
        for j in range(4):
            buttons_frame.columnconfigure(j, weight=1)
    
    def button_click(self, char):
        if char == 'C':
            self.current_input = ""
            self.result_display.set("0")
        elif char == '=':
            try:
                # Заменяем символы операций на Python-совместимые
                expression = self.current_input.replace('×', '*').replace('÷', '/')
                result = eval(expression)
                self.result_display.set(str(result))
                self.current_input = str(result)
            except Exception as e:
                messagebox.showerror("Ошибка", "Неверное выражение")
                self.current_input = ""
                self.result_display.set("0")
        elif char == '±':
            if self.current_input and self.current_input[0] == '-':
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
            self.result_display.set(self.current_input or "0")
        elif char == '%':
            try:
                result = eval(self.current_input) / 100
                self.result_display.set(str(result))
                self.current_input = str(result)
            except:
                pass
        else:
            if self.result_display.get() == "0" and char.isdigit():
                self.current_input = char
            else:
                self.current_input += char
            self.result_display.set(self.current_input)
    
    def run(self):
        self.root.mainloop()

# Запуск калькулятора
if __name__ == "__main__":
    calc = SimpleCalculator()
    calc.run()
```

### Пример 2: Текстовый редактор

```python
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog

class SimpleTextEditor:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Простой текстовый редактор")
        self.root.geometry("800x600")
        
        self.current_file = None
        self.text_changed = False
        
        self.create_menu()
        self.create_widgets()
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
        file_menu.add_command(label="Выход", command=self.exit_app)
        
        # Меню "Правка"
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Правка", menu=edit_menu)
        edit_menu.add_command(label="Отменить", command=self.undo, accelerator="Ctrl+Z")
        edit_menu.add_command(label="Повторить", command=self.redo, accelerator="Ctrl+Y")
        edit_menu.add_separator()
        edit_menu.add_command(label="Вырезать", command=self.cut, accelerator="Ctrl+X")
        edit_menu.add_command(label="Копировать", command=self.copy, accelerator="Ctrl+C")
        edit_menu.add_command(label="Вставить", command=self.paste, accelerator="Ctrl+V")
        edit_menu.add_command(label="Выделить все", command=self.select_all, accelerator="Ctrl+A")
    
    def create_widgets(self):
        # Создание текстовой области с прокруткой
        text_frame = tk.Frame(self.root)
        text_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.text_area = tk.Text(
            text_frame,
            wrap=tk.WORD,
            undo=True,
            font=("Consolas", 12)
        )
        
        # Добавление прокрутки
        scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=self.text_area.yview)
        self.text_area.configure(yscrollcommand=scrollbar.set)
        
        self.text_area.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Строка состояния
        self.status_bar = tk.Label(
            self.root,
            text="Готов",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def setup_bindings(self):
        # Привязка горячих клавиш
        self.root.bind('<Control-n>', lambda e: self.new_file())
        self.root.bind('<Control-o>', lambda e: self.open_file())
        self.root.bind('<Control-s>', lambda e: self.save_file())
        self.root.bind('<Control-a>', lambda e: self.select_all())
        
        # Отслеживание изменений текста
        self.text_area.bind('<KeyPress>', self.on_text_change)
        self.text_area.bind('<Button-1>', self.update_status)
        self.text_area.bind('<KeyRelease>', self.update_status)
    
    def on_text_change(self, event=None):
        self.text_changed = True
        self.update_title()
    
    def update_status(self, event=None):
        # Обновление информации в строке состояния
        line, col = self.text_area.index(tk.INSERT).split('.')
        words = len(self.text_area.get("1.0", tk.END).split())
        chars = len(self.text_area.get("1.0", tk.END)) - 1  # -1 для символа новой строки в конце
        
        status_text = f"Строка: {line}, Столбец: {col} | Слов: {words} | Символов: {chars}"
        self.status_bar.config(text=status_text)
    
    def update_title(self):
        title = "Простой текстовый редактор"
        if self.current_file:
            title += f" - {self.current_file}"
        if self.text_changed:
            title += " *"
        self.root.title(title)
    
    def new_file(self):
        if self.text_changed:
            result = messagebox.askyesnocancel("Сохранить изменения", "Сохранить изменения перед созданием нового файла?")
            if result:
                self.save_file()
            elif result is None:
                return  # Отмена действия
        
        self.text_area.delete(1.0, tk.END)
        self.current_file = None
        self.text_changed = False
        self.update_title()
        self.status_bar.config(text="Создан новый файл")
    
    def open_file(self):
        if self.text_changed:
            result = messagebox.askyesnocancel("Сохранить изменения", "Сохранить изменения перед открытием файла?")
            if result:
                self.save_file()
            elif result is None:
                return  # Отмена действия
        
        file_path = filedialog.askopenfilename(
            title="Открыть файл",
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
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
                content = self.text_area.get(1.0, tk.END + '-1c')  # -1c удаляет последний символ новой строки
                
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
            filetypes=[("Текстовые файлы", "*.txt"), ("Все файлы", "*.*")]
        )
        
        if file_path:
            try:
                content = self.text_area.get(1.0, tk.END + '-1c')
                
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
            result = messagebox.askyesnocancel("Выход", "Сохранить изменения перед выходом?")
            if result:
                self.save_file()
                self.root.quit()
            elif result is None:
                pass  # Остаться в приложении
            else:
                self.root.quit()
        else:
            self.root.quit()
    
    # Методы редактирования
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
        return 'break'
    
    def run(self):
        self.update_status()  # Обновить начальное состояние строки состояния
        self.root.mainloop()

# Запуск текстового редактора
if __name__ == "__main__":
    editor = SimpleTextEditor()
    editor.run()
```

---

## Заключение

Tkinter предоставляет мощный и гибкий способ создания графических интерфейсов в Python. Основные аспекты работы с Tkinter включают:

1. Создание окон и виджетов
2. Обработка событий пользователя
3. Использование менеджеров размещения для организации интерфейса
4. Применение различных видов виджетов для взаимодействия с пользователем

Tkinter особенно хорош для создания простых и средних приложений, где не требуется очень современный внешний вид. Это отличный инструмент для начинающих и для быстрого прототипирования интерфейсов.

## Контрольные вопросы:
1. В чем различие между pack, grid и place менеджерами?
2. Как обрабатываются события в Tkinter?
3. Какие основные виджеты доступны в Tkinter?
4. Как создать многооконное приложение?
5. Как реализовать контекстное меню в Tkinter?
