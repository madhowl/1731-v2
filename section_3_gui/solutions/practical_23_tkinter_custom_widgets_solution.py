#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Практическое занятие 23: Tkinter - создание пользовательских виджетов
Решение задач по созданию собственных виджетов

Автор: AI Assistant
"""

import tkinter as tk
from tkinter import ttk, messagebox
import re


# ==============================================================================
# ЗАДАЧА 1: Расширение стандартных виджетов
# ==============================================================================

class IconButton(ttk.Button):
    """Кнопка с иконкой и подсказкой (tooltip)"""
    
    def __init__(self, master=None, text="", icon=None, tooltip="", **kwargs):
        super().__init__(master, text=text, **kwargs)
        self.tooltip = tooltip
        self.icon = icon
        
        if tooltip:
            self.bind("<Enter>", self.show_tooltip)
            self.bind("<Leave>", self.hide_tooltip)
            self.tooltip_window = None
    
    def show_tooltip(self, event):
        """Показать подсказку"""
        if self.tooltip:
            x = self.winfo_rootx() + 20
            y = self.winfo_rooty() + self.winfo_height() + 5
            self.tooltip_window = tk.Toplevel(self)
            self.tooltip_window.wm_overrideredirect(True)
            self.tooltip_window.wm_geometry(f"+{x}+{y}")
            label = tk.Label(
                self.tooltip_window, 
                text=self.tooltip, 
                background="#ffffe0",
                relief=tk.SOLID,
                borderwidth=1,
                font=("Arial", 9)
            )
            label.pack()
    
    def hide_tooltip(self, event):
        """Скрыть подсказку"""
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None


class ValidatedEntry(ttk.Entry):
    """Поле ввода с валидацией"""
    
    def __init__(self, master=None, validation_type="none", **kwargs):
        self.validation_type = validation_type
        self.validation_error = ""
        
        # Настройка валидации
        vcmd = (master.register(self.validate), '%P')
        super().__init__(master, validate="key", validatecommand=vcmd, **kwargs)
        
        self.error_label = None
    
    def validate(self, new_value):
        """Валидация ввода"""
        if self.validation_type == "none":
            return True
        elif self.validation_type == "int":
            return new_value == "" or new_value.lstrip('-').isdigit()
        elif self.validation_type == "float":
            return new_value == "" or self._is_float(new_value)
        elif self.validation_type == "email":
            return new_value == "" or self._is_valid_email(new_value)
        elif self.validation_type == "phone":
            return new_value == "" or self._is_valid_phone(new_value)
        return True
    
    def _is_float(self, value):
        """Проверка на число с плавающей точкой"""
        try:
            float(value)
            return True
        except ValueError:
            return False
    
    def _is_valid_email(self, email):
        """Проверка email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def _is_valid_phone(self, phone):
        """Проверка телефона"""
        pattern = r'^[\d\s\+\-\(\)]+$'
        return bool(re.match(pattern, phone)) and len(phone) >= 10


class ImageLabel(ttk.Label):
    """Метка с поддержкой изображений и адаптивным размером"""
    
    def __init__(self, master=None, image_path=None, **kwargs):
        super().__init__(master, **kwargs)
        self.image = None
        
        if image_path:
            self.set_image(image_path)
    
    def set_image(self, image_path):
        """Установить изображение"""
        try:
            self.image = tk.PhotoImage(file=image_path)
            self.config(image=self.image)
        except tk.TclError:
            # Если изображение не найдено, используем заглушку
            self.config(text="[Изображение]")
    
    def clear_image(self):
        """Очистить изображение"""
        self.image = None
        self.config(image="")


class StatefulButton(ttk.Button):
    """Кнопка с дополнительными состояниями (normal, hover, disabled, pressed)"""
    
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        
        # Состояния
        self.is_hovered = False
        self.is_pressed = False
        
        # Привязка событий
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Button-1>", self.on_press)
        self.bind("<ButtonRelease-1>", self.on_release)
        
        # Применение стилей
        self.apply_style()
    
    def on_enter(self, event):
        """Обработка наведения"""
        self.is_hovered = True
        self.apply_style()
    
    def on_leave(self, event):
        """Обработка ухода курсора"""
        self.is_hovered = False
        self.is_pressed = False
        self.apply_style()
    
    def on_press(self, event):
        """Обработка нажатия"""
        self.is_pressed = True
        self.apply_style()
    
    def on_release(self, event):
        """Обработка отпускания"""
        self.is_pressed = False
        self.apply_style()
    
    def apply_style(self):
        """Применение стиля на основе состояния"""
        if self.instate(['disabled']):
            self.config(style='Disabled.TButton')
        elif self.is_pressed:
            self.config(style='Pressed.TButton')
        elif self.is_hovered:
            self.config(style='Hover.TButton')
        else:
            self.config(style='TButton')


# ==============================================================================
# ЗАДАЧА 2: Составные виджеты
# ==============================================================================

class SearchBar(ttk.Frame):
    """Поле поиска с кнопкой и очисткой"""
    
    def __init__(self, master=None, placeholder="Поиск...", **kwargs):
        super().__init__(master, **kwargs)
        
        self.placeholder = placeholder
        
        # Поле ввода
        self.entry = ttk.Entry(self)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.entry.insert(0, placeholder)
        self.entry.config(foreground='grey')
        
        # Привязка событий для placeholder
        self.entry.bind("<FocusIn>", self.on_focus_in)
        self.entry.bind("<FocusOut>", self.on_focus_out)
        
        # Кнопка поиска
        self.search_button = ttk.Button(
            self, 
            text="🔍", 
            width=3,
            command=self.on_search
        )
        self.search_button.pack(side=tk.RIGHT)
        
        # Кнопка очистки
        self.clear_button = ttk.Button(
            self, 
            text="✕", 
            width=3,
            command=self.clear
        )
        self.clear_button.pack(side=tk.RIGHT, padx=(2, 0))
        
        # Команда поиска (коллбэк)
        self.search_command = None
    
    def on_focus_in(self, event):
        """Очистка placeholder при фокусе"""
        if self.entry.get() == self.placeholder:
            self.entry.delete(0, tk.END)
            self.entry.config(foreground='black')
    
    def on_focus_out(self, event):
        """Восстановление placeholder при потере фокуса"""
        if not self.entry.get():
            self.entry.insert(0, self.placeholder)
            self.entry.config(foreground='grey')
    
    def clear(self):
        """Очистка поля"""
        self.entry.delete(0, tk.END)
        self.entry.insert(0, self.placeholder)
        self.entry.config(foreground='grey')
        if self.search_command:
            self.search_command("")
    
    def on_search(self):
        """Обработка поиска"""
        value = self.get()
        if value != self.placeholder and self.search_command:
            self.search_command(value)
    
    def get(self):
        """Получить значение"""
        value = self.entry.get()
        return value if value != self.placeholder else ""
    
    def set_search_command(self, command):
        """Установить команду поиска"""
        self.search_command = command


class PasswordEntry(ttk.Frame):
    """Поле ввода пароля с кнопкой показа/скрытия"""
    
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.is_visible = False
        
        # Поле ввода
        self.entry = ttk.Entry(self, show="*")
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Кнопка показа/скрытия
        self.toggle_button = ttk.Button(
            self, 
            text="👁", 
            width=3,
            command=self.toggle_visibility
        )
        self.toggle_button.pack(side=tk.RIGHT, padx=(2, 0))
    
    def toggle_visibility(self):
        """Переключить видимость пароля"""
        self.is_visible = not self.is_visible
        
        # Сохраняем текущий текст
        current = self.entry.get()
        
        # Меняем режим отображения
        if self.is_visible:
            self.entry.config(show="")
            self.toggle_button.config(text="🙈")
        else:
            self.entry.config(show="*")
            self.toggle_button.config(text="👁")
        
        # Восстанавливаем текст
        self.entry.delete(0, tk.END)
        self.entry.insert(0, current)
    
    def get(self):
        """Получить значение пароля"""
        return self.entry.get()
    
    def set(self, value):
        """Установить значение пароля"""
        self.entry.delete(0, tk.END)
        self.entry.insert(0, value)


class NumberPicker(ttk.Frame):
    """Счетчик (spinbox с кнопками +/-)"""
    
    def __init__(self, master=None, min_value=0, max_value=100, step=1, default=0, **kwargs):
        super().__init__(master, **kwargs)
        
        self.min_value = min_value
        self.max_value = max_value
        self.step = step
        self.current_value = default
        
        # Кнопка уменьшения
        self.minus_button = ttk.Button(
            self, 
            text="-", 
            width=3,
            command=self.decrement
        )
        self.minus_button.pack(side=tk.LEFT)
        
        # Поле ввода
        self.entry = ttk.Entry(self, width=8, justify="center")
        self.entry.insert(0, str(default))
        self.entry.pack(side=tk.LEFT, padx=5)
        self.entry.bind("<FocusOut>", self.on_value_changed)
        self.entry.bind("<Return>", self.on_value_changed)
        
        # Кнопка увеличения
        self.plus_button = ttk.Button(
            self, 
            text="+", 
            width=3,
            command=self.increment
        )
        self.plus_button.pack(side=tk.LEFT)
        
        # Команда изменения (коллбэк)
        self.change_command = None
    
    def increment(self):
        """Увеличить значение"""
        new_value = self.current_value + self.step
        if new_value <= self.max_value:
            self.current_value = new_value
            self.update_display()
            if self.change_command:
                self.change_command(self.current_value)
    
    def decrement(self):
        """Уменьшить значение"""
        new_value = self.current_value - self.step
        if new_value >= self.min_value:
            self.current_value = new_value
            self.update_display()
            if self.change_command:
                self.change_command(self.current_value)
    
    def update_display(self):
        """Обновить отображение"""
        self.entry.delete(0, tk.END)
        self.entry.insert(0, str(self.current_value))
    
    def on_value_changed(self, event):
        """Обработка изменения значения вручную"""
        try:
            value = int(self.entry.get())
            if self.min_value <= value <= self.max_value:
                self.current_value = value
                if self.change_command:
                    self.change_command(self.current_value)
            else:
                self.update_display()
        except ValueError:
            self.update_display()
    
    def get(self):
        """Получить текущее значение"""
        return self.current_value
    
    def set(self, value):
        """Установить значение"""
        if self.min_value <= value <= self.max_value:
            self.current_value = value
            self.update_display()
            if self.change_command:
                self.change_command(self.current_value)


class SearchableCombobox(ttk.Frame):
    """Выпадающий список с поиском"""
    
    def __init__(self, master=None, values=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.values = values or []
        self.filtered_values = self.values.copy()
        
        # Поле поиска
        self.search_entry = ttk.Entry(self)
        self.search_entry.pack(fill=tk.X)
        self.search_entry.bind("<KeyRelease>", self.on_search)
        
        # Список (Listbox вместо Combobox для поиска)
        self.frame = ttk.Frame(self)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        self.listbox = tk.Listbox(self.frame)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox.bind("<Double-Button-1>", self.on_select)
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(self.frame, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)
        
        # Заполнение списка
        self.update_list()
    
    def on_search(self, event):
        """Поиск по мере ввода"""
        search_text = self.search_entry.get().lower()
        self.filtered_values = [
            v for v in self.values 
            if search_text in v.lower()
        ]
        self.update_list()
    
    def update_list(self):
        """Обновить список"""
        self.listbox.delete(0, tk.END)
        for value in self.filtered_values:
            self.listbox.insert(tk.END, value)
    
    def on_select(self, event):
        """Обработка выбора"""
        selection = self.listbox.curselection()
        if selection:
            self.selected_value = self.filtered_values[selection[0]]
    
    def get(self):
        """Получить выбранное значение"""
        try:
            return self.selected_value
        except AttributeError:
            return None


# ==============================================================================
# ЗАДАЧА 3: Панельные виджеты
# ==============================================================================

class Toolbar(ttk.Frame):
    """Панель инструментов с группировкой кнопок"""
    
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.groups = []
        self.current_group = None
    
    def add_group(self, label=""):
        """Добавить группу кнопок"""
        if self.current_group:
            # Разделитель между группами
            ttk.Separator(self, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        
        group_frame = ttk.Frame(self)
        group_frame.pack(side=tk.LEFT)
        
        if label:
            ttk.Label(group_frame, text=label, font=("Arial", 8)).pack(side=tk.LEFT, padx=(5, 2))
        
        self.current_group = group_frame
        return group_frame
    
    def add_button(self, text, command, icon=None):
        """Добавить кнопку в текущую группу"""
        if self.current_group:
            btn = ttk.Button(
                self.current_group, 
                text=text, 
                command=command
            )
            btn.pack(side=tk.LEFT, padx=2)
            return btn


class CollapsibleSidebar(ttk.Frame):
    """Боковая панель с сворачиванием"""
    
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.is_collapsed = False
        self.collapsed_width = 30
        self.expanded_width = 200
        
        # Кнопка сворачивания/разворачивания
        self.toggle_btn = ttk.Button(
            self, 
            text="◀", 
            width=2,
            command=self.toggle
        )
        self.toggle_btn.place(x=0, y=0)
        
        # Основная область
        self.content_frame = ttk.Frame(self, padding=(30, 5, 5, 5))
        self.content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Заголовок
        self.title = ttk.Label(
            self.content_frame, 
            text="Боковая панель", 
            font=("Arial", 12, "bold")
        )
        self.title.pack(pady=5)
        
        # Контейнер для элементов
        self.items_frame = ttk.Frame(self.content_frame)
        self.items_frame.pack(fill=tk.BOTH, expand=True)
    
    def toggle(self):
        """Переключить состояние"""
        self.is_collapsed = not self.is_collapsed
        
        if self.is_collapsed:
            self.toggle_btn.config(text="▶")
            self.place(width=self.collapsed_width)
            self.content_frame.pack_forget()
        else:
            self.toggle_btn.config(text="◀")
            self.place(width=self.expanded_width)
            self.content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=(30, 5, 5, 5))
    
    def add_item(self, text, command):
        """Добавить элемент"""
        btn = ttk.Button(
            self.items_frame, 
            text=text, 
            command=command,
            width=20
        )
        btn.pack(pady=2)


class SimpleTabs(ttk.Frame):
    """Вкладки без использования ttk.Notebook"""
    
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.tabs = {}
        self.active_tab = None
        
        # Панель вкладок
        self.tab_bar = ttk.Frame(self)
        self.tab_bar.pack(side=tk.TOP, fill=tk.X)
        
        # Контейнер для содержимого
        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
    def add_tab(self, name, title):
        """Добавить вкладку"""
        btn = ttk.Button(
            self.tab_bar, 
            text=title,
            command=lambda: self.show_tab(name)
        )
        btn.pack(side=tk.LEFT, padx=2)
        
        # Фрейм содержимого
        content = ttk.Frame(self.content_frame)
        
        self.tabs[name] = {
            'button': btn,
            'content': content
        }
        
        return content
    
    def show_tab(self, name):
        """Показать вкладку"""
        # Скрыть все содержимое
        for tab_data in self.tabs.values():
            tab_data['content'].pack_forget()
        
        # Показать выбранную
        if name in self.tabs:
            self.tabs[name]['content'].pack(fill=tk.BOTH, expand=True)
            self.active_tab = name
        
        # Обновить стиль кнопок
        for tab_name, tab_data in self.tabs.items():
            if tab_name == name:
                tab_data['button'].config(style='Accent.TButton')
            else:
                tab_data['button'].config(style='TButton')


class Accordion(ttk.Frame):
    """Аккордеон (вертикальный сворачиваемый список)"""
    
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.items = {}
    
    def add_section(self, title):
        """Добавить секцию"""
        section = AccordionSection(self, title)
        section.pack(fill=tk.X, pady=2)
        self.items[title] = section
        return section.content_frame
    
    def expand_all(self):
        """Развернуть все"""
        for section in self.values():
            section.expand()
    
    def collapse_all(self):
        """Свернуть все"""
        for section in self.values():
            section.collapse()
    
    def values(self):
        """Получить все секции"""
        return self.items.values()


class AccordionSection(ttk.Frame):
    """Секция аккордеона"""
    
    def __init__(self, master, title):
        super().__init__(master, relief=tk.RAISED, borderwidth=1)
        
        self.is_expanded = False
        
        # Заголовок
        self.header = ttk.Frame(self)
        self.header.pack(fill=tk.X)
        
        self.title_label = ttk.Label(
            self.header, 
            text=title, 
            font=("Arial", 10, "bold")
        )
        self.title_label.pack(side=tk.LEFT, padx=5)
        
        self.toggle_btn = ttk.Button(
            self.header, 
            text="▼", 
            width=3,
            command=self.toggle
        )
        self.toggle_btn.pack(side=tk.RIGHT)
        
        # Содержимое
        self.content_frame = ttk.Frame(self, padding=5)
    
    def toggle(self):
        """Переключить состояние"""
        if self.is_expanded:
            self.collapse()
        else:
            self.expand()
    
    def expand(self):
        """Развернуть"""
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.toggle_btn.config(text="▲")
        self.is_expanded = True
    
    def collapse(self):
        """Свернуть"""
        self.content_frame.pack_forget()
        self.toggle_btn.config(text="▼")
        self.is_expanded = False


# ==============================================================================
# ЗАДАЧА 4: Формы и диалоги
# ==============================================================================

class DynamicForm(ttk.Frame):
    """Форма ввода с динамическими полями"""
    
    def __init__(self, master=None, fields=None, **kwargs):
        super().__init__(master, **kwargs)
        
        self.fields = fields or []
        self.field_widgets = {}
        
        self.create_form()
    
    def create_form(self):
        """Создание формы"""
        for field in self.fields:
            self.add_field(field)
    
    def add_field(self, field_config):
        """Добавить поле"""
        name = field_config['name']
        field_type = field_config.get('type', 'text')
        label_text = field_config.get('label', name)
        
        # Метка
        lbl = ttk.Label(self, text=label_text)
        lbl.grid(row=len(self.field_widgets), column=0, sticky=tk.W, pady=5)
        
        # Поле ввода в зависимости от типа
        if field_type == 'text':
            widget = ttk.Entry(self)
        elif field_type == 'password':
            widget = PasswordEntry(self)
        elif field_type == 'number':
            widget = ttk.Spinbox(self, from_=0, to=100)
        elif field_type == 'textarea':
            widget = tk.Text(self, height=3)
        elif field_type == 'select':
            widget = ttk.Combobox(self, values=field_config.get('values', []))
        else:
            widget = ttk.Entry(self)
        
        widget.grid(row=len(self.field_widgets), column=1, sticky=tk.EW, pady=5, padx=(5, 0))
        
        self.field_widgets[name] = widget
    
    def get_values(self):
        """Получить значения всех полей"""
        values = {}
        for name, widget in self.field_widgets.items():
            if isinstance(widget, tk.Text):
                values[name] = widget.get("1.0", tk.END).strip()
            elif isinstance(widget, PasswordEntry):
                values[name] = widget.get()
            else:
                try:
                    values[name] = widget.get()
                except (AttributeError, ValueError):
                    values[name] = ""
        return values


class ConfirmationDialog:
    """Диалог подтверждения"""
    
    def __init__(self, parent, title, message):
        self.result = False
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("300x150")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Сообщение
        msg_label = ttk.Label(
            self.dialog, 
            text=message, 
            wraplength=250,
            justify=tk.CENTER
        )
        msg_label.pack(pady=20)
        
        # Кнопки
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(pady=10)
        
        ttk.Button(
            btn_frame, 
            text="Да", 
            command=self.on_yes
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame, 
            text="Нет", 
            command=self.on_no
        ).pack(side=tk.LEFT, padx=5)
        
        # Центрирование
        self.dialog.update_idletasks()
        x = parent.winfo_x() + (parent.winfo_width() - 300) // 2
        y = parent.winfo_y() + (parent.winfo_height() - 150) // 2
        self.dialog.geometry(f"+{x}+{y}")
    
    def on_yes(self):
        """Обработка нажатия Да"""
        self.result = True
        self.dialog.destroy()
    
    def on_no(self):
        """Обработка нажатия Нет"""
        self.result = False
        self.dialog.destroy()
    
    def show(self):
        """Показать диалог и вернуть результат"""
        self.dialog.wait_window()
        return self.result


class Wizard:
    """Мастер создания (wizard)"""
    
    def __init__(self, parent, title, steps):
        self.steps = steps
        self.current_step = 0
        self.result = {}
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Прогресс
        self.progress = ttk.Progressbar(
            self.dialog, 
            mode='determinate',
            length=450
        )
        self.progress.pack(pady=10)
        
        # Заголовок шага
        self.step_label = ttk.Label(
            self.dialog, 
            text="", 
            font=("Arial", 12, "bold")
        )
        self.step_label.pack(pady=5)
        
        # Содержимое
        self.content_frame = ttk.Frame(self.dialog)
        self.content_frame.pack(fill=tk.BOTH, expand=True, padx=20)
        
        # Кнопки
        self.btn_frame = ttk.Frame(self.dialog)
        self.btn_frame.pack(pady=10)
        
        self.back_btn = ttk.Button(
            self.btn_frame, 
            text="Назад", 
            command=self.back,
            state=tk.DISABLED
        )
        self.back_btn.pack(side=tk.LEFT, padx=5)
        
        self.next_btn = ttk.Button(
            self.btn_frame, 
            text="Далее", 
            command=self.next
        )
        self.next_btn.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            self.btn_frame, 
            text="Отмена", 
            command=self.cancel
        ).pack(side=tk.LEFT, padx=5)
        
        self.show_step(0)
    
    def show_step(self, step_num):
        """Показать шаг"""
        self.current_step = step_num
        
        # Обновить UI
        self.progress['value'] = (step_num + 1) / len(self.steps) * 100
        
        if step_num < len(self.steps):
            step = self.steps[step_num]
            self.step_label.config(text=f"Шаг {step_num + 1}: {step['title']}")
            
            # Очистить содержимое
            for widget in self.content_frame.winfo_children():
                widget.destroy()
            
            # Создать содержимое шага
            if 'content' in step:
                step['content'](self.content_frame)
        
        # Обновить кнопки
        self.back_btn.config(state=tk.NORMAL if step_num > 0 else tk.DISABLED)
        
        if step_num == len(self.steps) - 1:
            self.next_btn.config(text="Готово")
        else:
            self.next_btn.config(text="Далее")
    
    def back(self):
        """Назад"""
        if self.current_step > 0:
            self.show_step(self.current_step - 1)
    
    def next(self):
        """Далее"""
        if self.current_step < len(self.steps) - 1:
            self.show_step(self.current_step + 1)
        else:
            self.dialog.destroy()
    
    def cancel(self):
        """Отмена"""
        self.result = None
        self.dialog.destroy()


class SelectionDialog:
    """Модальное окно выбора"""
    
    def __init__(self, parent, title, items):
        self.selected = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("300x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Список
        self.listbox = tk.Listbox(self.dialog)
        self.listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        for item in items:
            self.listbox.insert(tk.END, item)
        
        # Кнопки
        btn_frame = ttk.Frame(self.dialog)
        btn_frame.pack(pady=10)
        
        ttk.Button(
            btn_frame, 
            text="Выбрать", 
            command=self.select
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame, 
            text="Отмена", 
            command=self.dialog.destroy
        ).pack(side=tk.LEFT, padx=5)
    
    def select(self):
        """Выбор элемента"""
        selection = self.listbox.curselection()
        if selection:
            self.selected = self.listbox.get(selection[0])
        self.dialog.destroy()


# ==============================================================================
# ЗАДАЧА 5: Библиотека компонентов (полное демо-приложение)
# ==============================================================================

class ComponentLibraryDemo:
    """Демонстрация библиотеки компонентов"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Задача 5: Библиотека компонентов")
        self.root.geometry("800x600")
        
        self.create_demo()
    
    def create_demo(self):
        """Создание демонстрации"""
        # Notebook для разных категорий
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # Вкладка 1: Расширенные виджеты
        tab1 = ttk.Frame(notebook, padding=10)
        notebook.add(tab1, text="Расширенные виджеты")
        self.create_extended_widgets_tab(tab1)
        
        # Вкладка 2: Составные виджеты
        tab2 = ttk.Frame(notebook, padding=10)
        notebook.add(tab2, text="Составные виджеты")
        self.create_compound_widgets_tab(tab2)
        
        # Вкладка 3: Панельные виджеты
        tab3 = ttk.Frame(notebook, padding=10)
        notebook.add(tab3, text="Панельные виджеты")
        self.create_panel_widgets_tab(tab3)
        
        # Вкладка 4: Формы и диалоги
        tab4 = ttk.Frame(notebook, padding=10)
        notebook.add(tab4, text="Формы и диалоги")
        self.create_forms_dialogs_tab(tab4)
    
    def create_extended_widgets_tab(self, parent):
        """Вкладка расширенных виджетов"""
        # Кнопка с иконкой и подсказкой
        ttk.Label(parent, text="Кнопка с подсказкой:").grid(row=0, column=0, sticky=tk.W, pady=5)
        IconButton(
            parent, 
            text="Наведите курсор", 
            tooltip="Это всплывающая подсказка!"
        ).grid(row=0, column=1, sticky=tk.W, pady=5)
        
        # Поле с валидацией
        ttk.Label(parent, text="Email валидация:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ValidatedEntry(parent, validation_type="email", width=30).grid(
            row=1, column=1, sticky=tk.W, pady=5
        )
        
        ttk.Label(parent, text="Телефон валидация:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ValidatedEntry(parent, validation_type="phone", width=30).grid(
            row=2, column=1, sticky=tk.W, pady=5
        )
        
        # Кнопка с состояниями
        ttk.Label(parent, text="Кнопка с состояниями:").grid(row=3, column=0, sticky=tk.W, pady=5)
        StatefulButton(parent, text="Наведите/нажмите").grid(
            row=3, column=1, sticky=tk.W, pady=5
        )
    
    def create_compound_widgets_tab(self, parent):
        """Вкладка составных виджетов"""
        # Поиск
        ttk.Label(parent, text="Поиск:").grid(row=0, column=0, sticky=tk.W, pady=5)
        search = SearchBar(parent)
        search.set_search_command(lambda x: print(f"Поиск: {x}"))
        search.grid(row=0, column=1, sticky=tk.EW, pady=5)
        parent.columnconfigure(1, weight=1)
        
        # Пароль
        ttk.Label(parent, text="Пароль:").grid(row=1, column=0, sticky=tk.W, pady=5)
        PasswordEntry(parent).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Счетчик
        ttk.Label(parent, text="Счетчик:").grid(row=2, column=0, sticky=tk.W, pady=5)
        NumberPicker(parent, min_value=0, max_value=100, step=5, default=50).grid(
            row=2, column=1, sticky=tk.W, pady=5
        )
        
        # Выпадающий список с поиском
        ttk.Label(parent, text="Выбор из списка:").grid(row=3, column=0, sticky=tk.W, pady=5)
        SearchableCombobox(
            parent, 
            values=["Python", "Java", "JavaScript", "C++", "C#", "Go", "Rust"]
        ).grid(row=3, column=1, sticky=tk.EW, pady=5)
    
    def create_panel_widgets_tab(self, parent):
        """Вкладка панельных виджетов"""
        # Тулбар
        ttk.Label(parent, text="Панель инструментов:").pack(anchor=tk.W, pady=5)
        toolbar = Toolbar(parent)
        toolbar.pack(fill=tk.X, pady=5)
        
        group1 = toolbar.add_group("Файл")
        toolbar.add_button("Новый", lambda: print("Новый"))
        toolbar.add_button("Открыть", lambda: print("Открыть"))
        
        group2 = toolbar.add_group("Правка")
        toolbar.add_button("Копировать", lambda: print("Копировать"))
        toolbar.add_button("Вставить", lambda: print("Вставить"))
        
        # Вкладки
        ttk.Label(parent, text="Вкладки:").pack(anchor=tk.W, pady=5)
        tabs = SimpleTabs(parent)
        tabs.pack(fill=tk.BOTH, expand=True, pady=5)
        
        tab1 = tabs.add_tab("tab1", "Вкладка 1")
        ttk.Label(tab1, text="Содержимое первой вкладки").pack()
        
        tab2 = tabs.add_tab("tab2", "Вкладка 2")
        ttk.Label(tab2, text="Содержимое второй вкладки").pack()
        
        # Аккордеон
        ttk.Label(parent, text="Аккордеон:").pack(anchor=tk.W, pady=5)
        accordion = Accordion(parent)
        accordion.pack(fill=tk.BOTH, expand=True, pady=5)
        
        sec1 = accordion.add_section("Секция 1")
        ttk.Label(sec1, text="Содержимое секции 1").pack()
        
        sec2 = accordion.add_section("Секция 2")
        ttk.Label(sec2, text="Содержимое секции 2").pack()
    
    def create_forms_dialogs_tab(self, parent):
        """Вкладка форм и диалогов"""
        # Динамическая форма
        ttk.Label(parent, text="Динамическая форма:").pack(anchor=tk.W, pady=5)
        
        form = DynamicForm(parent, fields=[
            {'name': 'username', 'label': 'Имя пользователя:', 'type': 'text'},
            {'name': 'email', 'label': 'Email:', 'type': 'text'},
            {'name': 'password', 'label': 'Пароль:', 'type': 'password'},
            {'name': 'age', 'label': 'Возраст:', 'type': 'number'},
            {'name': 'role', 'label': 'Роль:', 'type': 'select', 'values': ['Admin', 'User', 'Guest']},
        ])
        form.pack(fill=tk.X, pady=5)
        
        # Кнопки форм
        btn_frame = ttk.Frame(parent)
        btn_frame.pack(pady=10)
        
        ttk.Button(
            btn_frame, 
            text="Показать значения", 
            command=lambda: print(form.get_values())
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame, 
            text="Диалог подтверждения", 
            command=lambda: self.show_confirm()
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame, 
            text="Мастер", 
            command=lambda: self.show_wizard()
        ).pack(side=tk.LEFT, padx=5)
    
    def show_confirm(self):
        """Показать диалог подтверждения"""
        result = ConfirmationDialog(
            self.root, 
            "Подтверждение", 
            "Вы уверены, что хотите продолжить?"
        ).show()
        print(f"Результат подтверждения: {result}")
    
    def show_wizard(self):
        """Показать мастер"""
        Wizard(
            self.root, 
            "Мастер создания",
            [
                {'title': 'Шаг 1: Имя', 'content': lambda p: ttk.Label(p, text="Введите ваше имя").pack()},
                {'title': 'Шаг 2: Email', 'content': lambda p: ttk.Label(p, text="Введите email").pack()},
                {'title': 'Шаг 3: Готово', 'content': lambda p: ttk.Label(p, text="Спасибо!").pack()},
            ]
        )


# ==============================================================================
# ГЛАВНОЕ МЕНЮ ПРИЛОЖЕНИЯ
# ==============================================================================

class MainApp:
    """Главное приложение с выбором задач"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Практическое занятие 23: Tkinter - пользовательские виджеты")
        self.root.geometry("600x500")
        
        self.create_main_menu()
    
    def create_main_menu(self):
        """Создание главного меню"""
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        title = ttk.Label(
            main_frame, 
            text="Выберите задачу:",
            font=("Arial", 16, "bold")
        )
        title.pack(pady=(0, 20))
        
        tasks = [
            ("Задача 1: Расширение стандартных виджетов", self.open_task1),
            ("Задача 2: Составные виджеты", self.open_task2),
            ("Задача 3: Панельные виджеты", self.open_task3),
            ("Задача 4: Формы и диалоги", self.open_task4),
            ("Задача 5: Библиотека компонентов", self.open_task5),
        ]
        
        for text, command in tasks:
            btn = ttk.Button(main_frame, text=text, width=40, command=command)
            btn.pack(pady=5)
        
        ttk.Button(main_frame, text="Выход", command=self.root.quit).pack(pady=20)
    
    def open_task1(self):
        """Открыть задачу 1"""
        window = tk.Toplevel(self.root)
        window.title("Задача 1: Расширение стандартных виджетов")
        window.geometry("400x300")
        
        frame = ttk.Frame(window, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Примеры расширенных виджетов
        ttk.Label(frame, text="Кнопка с подсказкой:").grid(row=0, column=0, sticky=tk.W, pady=5)
        IconButton(frame, text="Наведите курсор", tooltip="Это подсказка!").grid(
            row=0, column=1, sticky=tk.W, pady=5
        )
        
        ttk.Label(frame, text="Email валидация:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ValidatedEntry(frame, validation_type="email", width=25).grid(
            row=1, column=1, sticky=tk.W, pady=5
        )
        
        ttk.Label(frame, text="Числовая валидация:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ValidatedEntry(frame, validation_type="int", width=25).grid(
            row=2, column=1, sticky=tk.W, pady=5
        )
    
    def open_task2(self):
        """Открыть задачу 2"""
        window = tk.Toplevel(self.root)
        window.title("Задача 2: Составные виджеты")
        window.geometry("400x350")
        
        frame = ttk.Frame(window, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Поиск
        ttk.Label(frame, text="Поиск:").grid(row=0, column=0, sticky=tk.W, pady=5)
        search = SearchBar(frame)
        search.grid(row=0, column=1, sticky=tk.EW, pady=5)
        frame.columnconfigure(1, weight=1)
        
        # Пароль
        ttk.Label(frame, text="Пароль:").grid(row=1, column=0, sticky=tk.W, pady=5)
        PasswordEntry(frame).grid(row=1, column=1, sticky=tk.W, pady=5)
        
        # Счетчик
        ttk.Label(frame, text="Счетчик:").grid(row=2, column=0, sticky=tk.W, pady=5)
        NumberPicker(frame, min_value=0, max_value=100, step=5, default=10).grid(
            row=2, column=1, sticky=tk.W, pady=5
        )
        
        # Выпадающий список с поиском
        ttk.Label(frame, text="Выбор:").grid(row=3, column=0, sticky=tk.W, pady=5)
        combo = SearchableCombobox(
            frame, 
            values=["Python", "Java", "JavaScript", "C++", "Go", "Rust", "Ruby"]
        )
        combo.grid(row=3, column=1, sticky=tk.EW, pady=5)
    
    def open_task3(self):
        """Открыть задачу 3"""
        window = tk.Toplevel(self.root)
        window.title("Задача 3: Панельные виджеты")
        window.geometry("500x400")
        
        # Создаем сплиттер (sidebar + content)
        sidebar = CollapsibleSidebar(window)
        sidebar.place(x=0, y=0, height=400)
        
        sidebar.add_item("Главная", lambda: print("Главная"))
        sidebar.add_item("Проекты", lambda: print("Проекты"))
        sidebar.add_item("Задачи", lambda: print("Задачи"))
        
        # Основная область
        content = ttk.Frame(window, padding=(210, 10, 10, 10))
        content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        ttk.Label(content, text="Аккордеон:", font=("Arial", 12, "bold")).pack(pady=10)
        
        accordion = Accordion(content)
        accordion.pack(fill=tk.BOTH, expand=True)
        
        for i in range(1, 4):
            sec = accordion.add_section(f"Секция {i}")
            ttk.Label(sec, text=f"Содержимое секции {i}").pack()
    
    def open_task4(self):
        """Открыть задачу 4"""
        window = tk.Toplevel(self.root)
        window.title("Задача 4: Формы и диалоги")
        window.geometry("450x400")
        
        frame = ttk.Frame(window, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Динамическая форма
        form = DynamicForm(frame, fields=[
            {'name': 'name', 'label': 'Имя:', 'type': 'text'},
            {'name': 'email', 'label': 'Email:', 'type': 'text'},
            {'name': 'password', 'label': 'Пароль:', 'type': 'password'},
            {'name': 'age', 'label': 'Возраст:', 'type': 'number'},
        ])
        form.pack(fill=tk.X, pady=10)
        
        ttk.Button(
            frame, 
            text="Диалог подтверждения", 
            command=lambda: ConfirmationDialog(
                window, 
                "Подтверждение", 
                "Вы уверены?"
            ).show()
        ).pack(pady=5)
        
        ttk.Button(
            frame, 
            text="Окно выбора", 
            command=lambda: SelectionDialog(
                window, 
                "Выберите элемент",
                ["Элемент 1", "Элемент 2", "Элемент 3"]
            )
        ).pack(pady=5)
        
        ttk.Button(
            frame, 
            text="Мастер", 
            command=lambda: Wizard(
                window,
                "Мастер",
                [
                    {'title': 'Шаг 1', 'content': lambda p: ttk.Label(p, text="Шаг 1").pack()},
                    {'title': 'Шаг 2', 'content': lambda p: ttk.Label(p, text="Шаг 2").pack()},
                ]
            )
        ).pack(pady=5)
    
    def open_task5(self):
        """Открыть задачу 5 - полная библиотека"""
        window = tk.Toplevel(self.root)
        ComponentLibraryDemo(window)


def main():
    """Точка входа"""
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
