# Практическое занятие 23: Tkinter - создание пользовательских виджетов

## Цель занятия
Научиться создавать собственные виджеты в Tkinter, расширять функциональность стандартных виджетов и строить библиотеки переиспользуемых компонентов интерфейса.

## Задачи
1. Освоить расширение стандартных виджетов
2. Научиться создавать составные виджеты
3. Изучить создание панельных компонентов
4. Создать переиспользуемые формы и диалоги
5. Построить библиотеку компонентов

## Ход работы

### 1. Расширение стандартных виджетов

```python
import tkinter as tk
from tkinter import ttk

class ExtendedButton(ttk.Button):
    """
    Расширенная кнопка с иконкой и подсказкой
    """
    def __init__(self, master=None, **kwargs):
        # ВАШ КОД ЗДЕСЬ - инициализируйте кнопку
        pass
```

---

## 1. Теоретическая часть: Создание пользовательских виджетов

### Уровень 1 - Начальный

#### Задание 1.1: Расширение стандартных виджетов

Создайте пользовательские классы на основе стандартных виджетов:

```python
class CustomButton(ttk.Button):
    """
    Расширенная кнопка с иконкой и подсказкой
    """
    def __init__(self, master=None, **kwargs):
        # ВАШ КОД ЗДЕСЬ - расширьте функциональность кнопки
        # Добавьте иконку
        # Добавьте подсказку (tooltip)
        pass
        
class ValidatedEntry(ttk.Entry):
    """
    Поле ввода с валидацией
    """
    def __init__(self, master=None, **kwargs):
        # ВАШ КОД ЗДЕСЬ - создайте поле с валидацией
        pass
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import tkinter as tk
from tkinter import ttk

class CustomButton(ttk.Button):
    def __init__(self, master=None, icon=None, tooltip=None, **kwargs):
        super().__init__(master, **kwargs)
        
        if icon:
            self.configure(image=icon, compound=tk.LEFT)
        
        if tooltip:
            self.tooltip = ToolTip(self, tooltip)
            
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tooltip = None
        self.widget.bind("<Enter>", self.show)
        self.widget.bind("<Leave>", self.hide)
        
    def show(self, event=None):
        x = self.widget.winfo_rootx() + 20
        y = self.widget.winfo_rooty() + self.widget.winfo_height() + 5
        self.tooltip = tk.Toplevel(self.widget)
        self.tooltip.wm_overrideredirect(True)
        self.tooltip.wm_geometry(f"+{x}+{y}")
        label = ttk.Label(self.tooltip, text=self.text, background="#ffffdd")
        label.pack()

    def hide(self, event=None):
        if self.tooltip:
            self.tooltip.destroy()
            self.tooltip = None
```

</details>

### Уровень 2 - Средний

#### Задание 2.1: Составные виджеты

Создайте сложные виджеты из нескольких компонентов:

```python
class SearchBar(ttk.Frame):
    """
    Поле поиска с кнопкой и очисткой
    """
    def __init__(self, master=None, **kwargs):
        # ВАШ КОД ЗДЕСЬ - создайте:
        # Поле ввода
        # Кнопку поиска
        # Кнопку очистки
        pass
        
class PasswordEntry(ttk.Frame):
    """
    Поле ввода пароля с кнопкой показа/скрытия
    """
    def __init__(self, master=None, **kwargs):
        # ВАШ КОД ЗДЕСЬ - создайте поле с кнопкой "глаз"
        pass
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import tkinter as tk
from tkinter import ttk

class SearchBar(ttk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.entry = ttk.Entry(self)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.search_btn = ttk.Button(self, text="🔍")
        self.search_btn.pack(side=tk.LEFT)
        
        self.clear_btn = ttk.Button(self, text="✕", command=self.clear)
        self.clear_btn.pack(side=tk.LEFT)
        
    def get(self):
        return self.entry.get()
        
    def clear(self):
        self.entry.delete(0, tk.END)

class PasswordEntry(ttk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.show_password = tk.BooleanVar(value=False)
        
        self.entry = ttk.Entry(self, show="*")
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.toggle_btn = ttk.Checkbutton(
            self, text="👁", variable=self.show_password,
            command=self.toggle_visibility
        )
        self.toggle_btn.pack(side=tk.LEFT, padx=5)
        
    def toggle_visibility(self):
        self.entry.config(show="" if self.show_password.get() else "*")
        
    def get(self):
        return self.entry.get()
```

</details>

### Уровень 3 - Продвинутый

#### Задание 3.1: Библиотека компонентов

Создайте модуль с переиспользуемыми виджетами:

```python
# Создайте файл custom_widgets.py
# Реализуйте не менее 5 виджетов:
# - NumberPicker (счетчик)
# - CardWidget (карточка)
# - FormBuilder (построитель форм)
# - Accordion (аккордеон)
# - ModalDialog (модальный диалог)

class NumberPicker(ttk.Frame):
    """
    Виджет выбора числа с кнопками +/-
    """
    def __init__(self, master=None, **kwargs):
        # ВАШ КОД ЗДЕСЬ - создайте счетчик
        pass
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import tkinter as tk
from tkinter import ttk

class NumberPicker(ttk.Frame):
    def __init__(self, master=None, min_value=0, max_value=100, step=1, **kwargs):
        super().__init__(master, **kwargs)
        
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.value = tk.IntVar(value=min_value)
        
        self.decrease_btn = ttk.Button(self, text="-", width=3, command=self.decrease)
        self.decrease_btn.pack(side=tk.LEFT)
        
        self.entry = ttk.Entry(self, textvariable=self.value, width=6, justify=tk.CENTER)
        self.entry.pack(side=tk.LEFT, padx=5)
        
        self.increase_btn = ttk.Button(self, text="+", width=3, command=self.increase)
        self.increase_btn.pack(side=tk.LEFT)
        
    def decrease(self):
        new_value = self.value.get() - self.step
        if new_value >= self.min_value:
            self.value.set(new_value)
            
    def increase(self):
        new_value = self.value.get() + self.step
        if new_value <= self.max_value:
            self.value.set(new_value)
            
    def get(self):
        return self.value.get()

# Пример использования:
root = tk.Tk()
picker = NumberPicker(root, min_value=0, max_value=100, step=5)
picker.pack(pady=20)
root.mainloop()
```

</details>

---

## Требования к отчету
- Исходный код всех созданных виджетов
- Скриншоты примеров
- Описание архитектуры компонентов
- Примеры использования

## Критерии оценки
- Качество кода: 30%
- Функциональность: 30%
- Переиспользуемость: 20%
- Документация: 20%
