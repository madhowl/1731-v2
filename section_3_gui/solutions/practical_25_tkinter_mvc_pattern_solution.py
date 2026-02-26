#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Практическое занятие 25: Tkinter - паттерн MVC
Решение задач по применению паттерна Model-View-Controller

Автор: AI Assistant
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime


# ==============================================================================
# БАЗОВЫЕ КОМПОНЕНТЫ MVC
# ==============================================================================

class Observable:
    """Базовый класс для наблюдателя (паттерн Observer)"""
    
    def __init__(self):
        self._observers = []
    
    def add_observer(self, observer):
        """Добавить наблюдателя"""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def remove_observer(self, observer):
        """Удалить наблюдателя"""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify_observers(self, *args, **kwargs):
        """Уведомить всех наблюдателей"""
        for observer in self._observers:
            observer.update(*args, **kwargs)


# ==============================================================================
# ЗАДАЧА 1: Разделение компонентов MVC
# ==============================================================================

class TaskModel(Observable):
    """Model: Класс для хранения данных задач"""
    
    def __init__(self):
        super().__init__()
        self.tasks = []
        self.file_path = "tasks.json"
        self.load()
    
    def add_task(self, title, description=""):
        """Добавить задачу"""
        task = {
            "id": len(self.tasks) + 1,
            "title": title,
            "description": description,
            "completed": False,
            "created_at": datetime.now().isoformat()
        }
        self.tasks.append(task)
        self.save()
        self.notify_observers()
        return task
    
    def remove_task(self, task_id):
        """Удалить задачу"""
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                removed = self.tasks.pop(i)
                self.save()
                self.notify_observers()
                return removed
        return None
    
    def toggle_task(self, task_id):
        """Переключить статус выполнения"""
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = not task["completed"]
                self.save()
                self.notify_observers()
                return task
        return None
    
    def update_task(self, task_id, title=None, description=None):
        """Обновить задачу"""
        for task in self.tasks:
            if task["id"] == task_id:
                if title is not None:
                    task["title"] = title
                if description is not None:
                    task["description"] = description
                self.save()
                self.notify_observers()
                return task
        return None
    
    def get_tasks(self):
        """Получить все задачи"""
        return self.tasks.copy()
    
    def get_task(self, task_id):
        """Получить задачу по ID"""
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        return None
    
    def save(self):
        """Сохранить в файл"""
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.tasks, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
    
    def load(self):
        """Загрузить из файла"""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    self.tasks = json.load(f)
            except Exception as e:
                print(f"Ошибка загрузки: {e}")
                self.tasks = []


class TaskView:
    """View: Класс для отображения интерфейса"""
    
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.task_widgets = {}  # {task_id: checkbox}
        
        self.create_view()
    
    def create_view(self):
        """Создание представления"""
        # Заголовок
        title = ttk.Label(
            self.root, 
            text="Список задач", 
            font=("Arial", 16, "bold")
        )
        title.pack(pady=10)
        
        # Фрейм для списка задач
        list_frame = ttk.Frame(self.root)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10)
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Listbox
        self.listbox = tk.Listbox(
            list_frame, 
            yscrollcommand=scrollbar.set,
            font=("Arial", 11),
            height=15
        )
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.listbox.yview)
        
        # Привязка событий
        self.listbox.bind("<Double-Button-1>", self.on_double_click)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        
        # Панель ввода
        input_frame = ttk.Frame(self.root)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(input_frame, text="Задача:").pack(side=tk.LEFT, padx=5)
        
        self.entry = ttk.Entry(input_frame)
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.entry.bind("<Return>", lambda e: self.controller.add_task())
        
        # Кнопки
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=5)
        
        ttk.Button(
            btn_frame, 
            text="Добавить", 
            command=self.controller.add_task
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame, 
            text="Удалить", 
            command=self.controller.remove_task
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            btn_frame, 
            text="Редактировать", 
            command=self.controller.edit_task
        ).pack(side=tk.LEFT, padx=5)
        
        self.details_label = ttk.Label(self.root, text="", font=("Arial", 9))
        self.details_label.pack(pady=5)
    
    def get_input(self):
        """Получить ввод пользователя"""
        return self.entry.get()
    
    def clear_input(self):
        """Очистить поле ввода"""
        self.entry.delete(0, tk.END)
    
    def set_tasks(self, tasks):
        """Отобразить задачи"""
        self.listbox.delete(0, tk.END)
        self.task_widgets.clear()
        
        for task in tasks:
            status = "✓" if task["completed"] else "○"
            text = f"{status} {task['title']}"
            self.listbox.insert(tk.END, text)
            self.task_widgets[task["id"]] = len(tasks) - 1
    
    def get_selected_index(self):
        """Получить индекс выбранной задачи"""
        selection = self.listbox.curselection()
        if selection:
            return selection[0]
        return None
    
    def get_selected_task_id(self):
        """Получить ID выбранной задачи"""
        index = self.get_selected_index()
        if index is not None:
            tasks = self.controller.model.get_tasks()
            if 0 <= index < len(tasks):
                return tasks[index]["id"]
        return None
    
    def on_select(self, event):
        """Обработка выбора"""
        task_id = self.get_selected_task_id()
        if task_id:
            task = self.controller.model.get_task(task_id)
            if task:
                details = f"Создано: {task.get('created_at', 'N/A')}"
                self.details_label.config(text=details)
    
    def on_double_click(self, event):
        """Обработка двойного клика - переключение статуса"""
        task_id = self.get_selected_task_id()
        if task_id:
            self.controller.toggle_task(task_id)
    
    def show_edit_dialog(self, task):
        """Показать диалог редактирования"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Редактирование задачи")
        dialog.geometry("400x200")
        dialog.transient(self.root)
        dialog.grab_set()
        
        ttk.Label(dialog, text="Название:").pack(pady=5)
        title_entry = ttk.Entry(dialog, width=40)
        title_entry.insert(0, task["title"])
        title_entry.pack(pady=5)
        
        ttk.Label(dialog, text="Описание:").pack(pady=5)
        desc_text = tk.Text(dialog, width=40, height=4)
        desc_text.insert("1.0", task.get("description", ""))
        desc_text.pack(pady=5)
        
        def save():
            title = title_entry.get().strip()
            description = desc_text.get("1.0", tk.END).strip()
            if title:
                self.controller.update_task(task["id"], title, description)
                dialog.destroy()
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Сохранить", command=save).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Отмена", command=dialog.destroy).pack(side=tk.LEFT, padx=5)


class TaskController:
    """Controller: Класс для обработки событий"""
    
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.model.add_observer(self)
        # Не вызываем self.update() сразу - представление может быть ещё не готово
    
    def init_view(self):
        """Инициализировать представление после его создания"""
        self.update()
    
    def add_task(self):
        """Добавить задачу"""
        title = self.view.get_input()
        if title:
            self.model.add_task(title)
            self.view.clear_input()
    
    def remove_task(self):
        """Удалить задачу"""
        task_id = self.view.get_selected_task_id()
        if task_id:
            if messagebox.askyesno("Подтверждение", "Удалить выбранную задачу?"):
                self.model.remove_task(task_id)
    
    def toggle_task(self, task_id):
        """Переключить статус задачи"""
        self.model.toggle_task(task_id)
    
    def edit_task(self):
        """Редактировать задачу"""
        task_id = self.view.get_selected_task_id()
        if task_id:
            task = self.model.get_task(task_id)
            if task:
                self.view.show_edit_dialog(task)
    
    def update_task(self, task_id, title, description):
        """Обновить задачу"""
        self.model.update_task(task_id, title, description)
    
    def update(self):
        """Обновить представление"""
        tasks = self.model.get_tasks()
        self.view.set_tasks(tasks)


# ==============================================================================
# ЗАДАЧА 2: Приложение списка задач (полная реализация)
# ==============================================================================

class TodoApp:
    """Приложение To-Do с полной реализацией MVC"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Задача 2: Приложение To-Do")
        self.root.geometry("600x500")
        
        # Создание MVC компонентов (в правильном порядке)
        self.model = TaskModel()
        # Сначала создаём контроллер без представления
        self.controller = TaskController(self.model, None)
        # Потом создаём представление с контроллером
        self.view = TaskView(self.root, self.controller)
        # Обновляем контроллер ссылкой на представление
        self.controller.view = self.view
        self.controller.init_view()


# ==============================================================================
# ЗАДАЧА 3: Приложение заметок
# ==============================================================================

class Note:
    """Модель заметки"""
    
    def __init__(self, id, title, content):
        self.id = id
        self.title = title
        self.content = content
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at


class NotesModel(Observable):
    """Model для заметок"""
    
    def __init__(self):
        super().__init__()
        self.notes = []
        self.file_path = "notes.json"
        self.load()
    
    def add_note(self, title, content=""):
        """Добавить заметку"""
        note_id = max([n.id for n in self.notes], default=0) + 1
        note = Note(note_id, title, content)
        self.notes.append(note)
        self.save()
        self.notify_observers()
        return note
    
    def remove_note(self, note_id):
        """Удалить заметку"""
        for i, note in enumerate(self.notes):
            if note.id == note_id:
                removed = self.notes.pop(i)
                self.save()
                self.notify_observers()
                return removed
        return None
    
    def update_note(self, note_id, title=None, content=None):
        """Обновить заметку"""
        for note in self.notes:
            if note.id == note_id:
                if title is not None:
                    note.title = title
                if content is not None:
                    note.content = content
                note.updated_at = datetime.now().isoformat()
                self.save()
                self.notify_observers()
                return note
        return None
    
    def get_notes(self):
        """Получить все заметки"""
        return self.notes.copy()
    
    def get_note(self, note_id):
        """Получить заметку по ID"""
        for note in self.notes:
            if note.id == note_id:
                return note
        return None
    
    def search_notes(self, query):
        """Поиск заметок"""
        query = query.lower()
        return [n for n in self.notes 
                if query in n.title.lower() or query in n.content.lower()]
    
    def save(self):
        """Сохранить в файл"""
        try:
            data = [{"id": n.id, "title": n.title, "content": n.content,
                    "created_at": n.created_at, "updated_at": n.updated_at}
                   for n in self.notes]
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
    
    def load(self):
        """Загрузить из файла"""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.notes = [Note(d["id"], d["title"], d["content"]) 
                                 for d in data]
            except Exception as e:
                print(f"Ошибка загрузки: {e}")
                self.notes = []


class NotesView:
    """View для заметок"""
    
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        
        self.create_view()
    
    def create_view(self):
        """Создание представления"""
        # Основной контейнер с разделением
        main_frame = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Левая панель - список заметок
        left_frame = ttk.Frame(main_frame, width=200)
        main_frame.add(left_frame, weight=1)
        
        # Поиск
        search_frame = ttk.Frame(left_frame)
        search_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.search_entry = ttk.Entry(search_frame)
        self.search_entry.pack(fill=tk.X)
        self.search_entry.bind("<KeyRelease>", lambda e: self.controller.search())
        
        # Список заметок
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5)
        
        self.listbox = tk.Listbox(list_frame, font=("Arial", 10))
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox.bind("<<ListboxSelect>>", lambda e: self.controller.select_note())
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=scrollbar.set)
        
        # Кнопки списка
        btn_frame = ttk.Frame(left_frame)
        btn_frame.pack(pady=5)
        
        ttk.Button(btn_frame, text="+", width=5, command=self.controller.add_note).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="-", width=5, command=self.controller.delete_note).pack(side=tk.LEFT, padx=2)
        
        # Правая панель - редактор
        right_frame = ttk.Frame(main_frame)
        main_frame.add(right_frame, weight=2)
        
        # Заголовок заметки
        title_frame = ttk.Frame(right_frame)
        title_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(title_frame, text="Заголовок:").pack(side=tk.LEFT)
        self.title_entry = ttk.Entry(title_frame, font=("Arial", 12, "bold"))
        self.title_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Текст заметки
        self.text = tk.Text(right_frame, wrap=tk.WORD, font=("Arial", 11))
        self.text.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.text.bind("<<Modified>>", lambda e: self.controller.mark_dirty())
        
        # Статус
        self.status_label = ttk.Label(right_frame, text="")
        self.status_label.pack(pady=5)
        
        self.current_note_id = None
        self.is_dirty = False
    
    def set_notes(self, notes):
        """Отобразить список заметок"""
        self.listbox.delete(0, tk.END)
        for note in notes:
            self.listbox.insert(tk.END, note.title or "Без названия")
    
    def get_selected_note_id(self):
        """Получить ID выбранной заметки"""
        selection = self.listbox.curselection()
        if selection:
            notes = self.controller.model.get_notes()
            if 0 <= selection[0] < len(notes):
                return notes[selection[0]].id
        return None
    
    def display_note(self, note):
        """Отобразить заметку"""
        if note:
            self.current_note_id = note.id
            self.title_entry.delete(0, tk.END)
            self.title_entry.insert(0, note.title)
            self.text.delete("1.0", tk.END)
            self.text.insert("1.0", note.content)
            self.is_dirty = False
            self.status_label.config(text=f"Обновлено: {note.updated_at}")
        else:
            self.current_note_id = None
            self.title_entry.delete(0, tk.END)
            self.text.delete("1.0", tk.END)
            self.status_label.config(text="")
    
    def get_current_content(self):
        """Получить текущее содержимое"""
        return self.text.get("1.0", tk.END).strip()
    
    def get_current_title(self):
        """Получить текущий заголовок"""
        return self.title_entry.get().strip()
    
    def mark_saved(self):
        """Отметить как сохраненное"""
        self.is_dirty = False
    
    def show_search_results(self, notes):
        """Показать результаты поиска"""
        self.listbox.delete(0, tk.END)
        for note in notes:
            self.listbox.insert(tk.END, f"[{note.title}] {note.content[:50]}...")


class NotesController:
    """Controller для заметок"""
    
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.model.add_observer(self)
        # Не вызываем self.update() сразу - представление может быть ещё не готово
    
    def init_view(self):
        """Инициализировать представление после его создания"""
        self.update()
    
    def add_note(self):
        """Добавить заметку"""
        title = "Новая заметка"
        note = self.model.add_note(title, "")
        self.view.display_note(note)
        self.view.title_entry.focus()
        self.view.title_entry.select_range(0, tk.END)
    
    def delete_note(self):
        """Удалить заметку"""
        note_id = self.view.get_selected_note_id()
        if note_id:
            if messagebox.askyesno("Подтверждение", "Удалить заметку?"):
                self.model.remove_note(note_id)
    
    def select_note(self):
        """Выбрать заметку"""
        # Сохранить текущую, если есть изменения
        if self.view.current_note_id and self.view.is_dirty:
            self.save_current()
        
        note_id = self.view.get_selected_note_id()
        if note_id:
            note = self.model.get_note(note_id)
            self.view.display_note(note)
    
    def save_current(self):
        """Сохранить текущую заметку"""
        if self.view.current_note_id:
            title = self.view.get_current_title()
            content = self.view.get_current_content()
            self.model.update_note(self.view.current_note_id, title, content)
            self.view.mark_saved()
    
    def mark_dirty(self):
        """Отметить как измененное"""
        self.view.is_dirty = True
        self.view.text.edit_modified(False)
    
    def search(self):
        """Поиск заметок"""
        query = self.view.search_entry.get().strip()
        if query:
            results = self.model.search_notes(query)
            self.view.show_search_results(results)
        else:
            self.update()
    
    def update(self):
        """Обновить представление"""
        notes = self.model.get_notes()
        self.view.set_notes(notes)


class NotesApp:
    """Приложение заметок"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Задача 3: Приложение заметок")
        self.root.geometry("800x600")
        
        self.model = NotesModel()
        # Сначала создаём контроллер без представления
        self.controller = NotesController(self.model, None)
        # Потом создаём представление с контроллером
        self.view = NotesView(self.root, self.controller)
        # Обновляем контроллер ссылкой на представление
        self.controller.view = self.view
        self.controller.init_view()


# ==============================================================================
# ЗАДАЧА 4: Адресная книга
# ==============================================================================

class Contact:
    """Модель контакта"""
    
    def __init__(self, id, name, phone, email, address=""):
        self.id = id
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address


class ContactsModel(Observable):
    """Model для контактов"""
    
    def __init__(self):
        super().__init__()
        self.contacts = []
        self.file_path = "contacts.json"
        self.load()
    
    def add_contact(self, name, phone, email, address=""):
        """Добавить контакт"""
        contact_id = max([c.id for c in self.contacts], default=0) + 1
        contact = Contact(contact_id, name, phone, email, address)
        self.contacts.append(contact)
        self.save()
        self.notify_observers()
        return contact
    
    def remove_contact(self, contact_id):
        """Удалить контакт"""
        for i, contact in enumerate(self.contacts):
            if contact.id == contact_id:
                removed = self.contacts.pop(i)
                self.save()
                self.notify_observers()
                return removed
        return None
    
    def update_contact(self, contact_id, name=None, phone=None, email=None, address=None):
        """Обновить контакт"""
        for contact in self.contacts:
            if contact.id == contact_id:
                if name is not None:
                    contact.name = name
                if phone is not None:
                    contact.phone = phone
                if email is not None:
                    contact.email = email
                if address is not None:
                    contact.address = address
                self.save()
                self.notify_observers()
                return contact
        return None
    
    def get_contacts(self):
        """Получить все контакты"""
        return sorted(self.contacts, key=lambda c: c.name)
    
    def get_contact(self, contact_id):
        """Получить контакт по ID"""
        for contact in self.contacts:
            if contact.id == contact_id:
                return contact
        return None
    
    def search_contacts(self, query):
        """Поиск контактов"""
        query = query.lower()
        return [c for c in self.contacts 
                if query in c.name.lower() or query in c.phone.lower() or query in c.email.lower()]
    
    def validate_contact(self, name, phone, email):
        """Валидация контакта"""
        errors = []
        
        if not name or len(name.strip()) < 2:
            errors.append("Имя должно содержать минимум 2 символа")
        
        if not phone or len(phone.strip()) < 7:
            errors.append("Телефон должен содержать минимум 7 цифр")
        
        if email and "@" not in email:
            errors.append("Email должен содержать символ @")
        
        return errors
    
    def export_csv(self, filename):
        """Экспорт в CSV"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("ID,Имя,Телефон,Email,Адрес\n")
                for c in self.contacts:
                    f.write(f'{c.id},"{c.name}","{c.phone}","{c.email}","{c.address}"\n')
            return True
        except Exception as e:
            print(f"Ошибка экспорта: {e}")
            return False
    
    def import_csv(self, filename):
        """Импорт из CSV"""
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                lines = f.readlines()[1:]  # Пропустить заголовок
                for line in lines:
                    parts = line.strip().split(",")
                    if len(parts) >= 3:
                        name = parts[1].strip('"')
                        phone = parts[2].strip('"')
                        email = parts[3].strip('"') if len(parts) > 3 else ""
                        address = parts[4].strip('"') if len(parts) > 4 else ""
                        self.add_contact(name, phone, email, address)
            return True
        except Exception as e:
            print(f"Ошибка импорта: {e}")
            return False
    
    def save(self):
        """Сохранить в файл"""
        try:
            data = [{"id": c.id, "name": c.name, "phone": c.phone, 
                    "email": c.email, "address": c.address}
                   for c in self.contacts]
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Ошибка сохранения: {e}")
    
    def load(self):
        """Загрузить из файла"""
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.contacts = [Contact(d["id"], d["name"], d["phone"], 
                                           d["email"], d.get("address", ""))
                                   for d in data]
            except Exception as e:
                print(f"Ошибка загрузки: {e}")
                self.contacts = []


class ContactsView:
    """View для контактов"""
    
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        
        self.create_view()
    
    def create_view(self):
        """Создание представления"""
        # Таблица контактов
        table_frame = ttk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Treeview для таблицы
        columns = ("name", "phone", "email")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        self.tree.heading("name", text="Имя")
        self.tree.heading("phone", text="Телефон")
        self.tree.heading("email", text="Email")
        
        self.tree.column("name", width=150)
        self.tree.column("phone", width=120)
        self.tree.column("email", width=180)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Скроллбар
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.config(yscrollcommand=scrollbar.set)
        
        self.tree.bind("<Double-Button-1>", lambda e: self.controller.edit_contact())
        
        # Панель управления
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(control_frame, text="Добавить", command=self.controller.add_contact).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Редактировать", command=self.controller.edit_contact).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Удалить", command=self.controller.delete_contact).pack(side=tk.LEFT, padx=5)
        
        # Поиск
        ttk.Label(control_frame, text="Поиск:").pack(side=tk.LEFT, padx=(20, 5))
        self.search_entry = ttk.Entry(control_frame, width=20)
        self.search_entry.pack(side=tk.LEFT)
        self.search_entry.bind("<KeyRelease>", lambda e: self.controller.search())
        
        # Экспорт/импорт
        ttk.Button(control_frame, text="Экспорт", command=self.controller.export_data).pack(side=tk.RIGHT, padx=5)
        ttk.Button(control_frame, text="Импорт", command=self.controller.import_data).pack(side=tk.RIGHT, padx=5)
    
    def set_contacts(self, contacts):
        """Отобразить контакты"""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        for contact in contacts:
            self.tree.insert("", tk.END, values=(contact.name, contact.phone, contact.email), 
                           tags=(str(contact.id),))
    
    def get_selected_contact_id(self):
        """Получить ID выбранного контакта"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            tags = item["tags"]
            if tags:
                return int(tags[0])
        return None
    
    def show_contact_form(self, contact=None, parent=None):
        """Показать форму контакта"""
        parent = parent or self.root
        
        dialog = tk.Toplevel(parent)
        dialog.title("Контакт" if contact else "Новый контакт")
        dialog.geometry("400x300")
        dialog.transient(parent)
        dialog.grab_set()
        
        form_frame = ttk.Frame(dialog, padding=20)
        form_frame.pack(fill=tk.BOTH, expand=True)
        
        # Поля
        fields = {}
        
        ttk.Label(form_frame, text="Имя:").grid(row=0, column=0, sticky=tk.W, pady=5)
        name_entry = ttk.Entry(form_frame, width=30)
        name_entry.grid(row=0, column=1, pady=5)
        fields["name"] = name_entry
        
        ttk.Label(form_frame, text="Телефон:").grid(row=1, column=0, sticky=tk.W, pady=5)
        phone_entry = ttk.Entry(form_frame, width=30)
        phone_entry.grid(row=1, column=1, pady=5)
        fields["phone"] = phone_entry
        
        ttk.Label(form_frame, text="Email:").grid(row=2, column=0, sticky=tk.W, pady=5)
        email_entry = ttk.Entry(form_frame, width=30)
        email_entry.grid(row=2, column=1, pady=5)
        fields["email"] = email_entry
        
        ttk.Label(form_frame, text="Адрес:").grid(row=3, column=0, sticky=tk.W, pady=5)
        address_entry = ttk.Entry(form_frame, width=30)
        address_entry.grid(row=3, column=1, pady=5)
        fields["address"] = address_entry
        
        # Заполнить данные, если редактирование
        if contact:
            name_entry.insert(0, contact.name)
            phone_entry.insert(0, contact.phone)
            email_entry.insert(0, contact.email)
            address_entry.insert(0, contact.address)
        
        # Кнопки
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(pady=20)
        
        def save():
            name = name_entry.get().strip()
            phone = phone_entry.get().strip()
            email = email_entry.get().strip()
            address = address_entry.get().strip()
            
            errors = self.controller.model.validate_contact(name, phone, email)
            
            if errors:
                messagebox.showerror("Ошибки", "\n".join(errors))
            else:
                if contact:
                    self.controller.update_contact(contact.id, name, phone, email, address)
                else:
                    self.controller.add_contact(name, phone, email, address)
                dialog.destroy()
        
        ttk.Button(btn_frame, text="Сохранить", command=save).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Отмена", command=dialog.destroy).pack(side=tk.LEFT, padx=5)


class ContactsController:
    """Controller для контактов"""
    
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.model.add_observer(self)
        # Не вызываем self.update() сразу - представление может быть ещё не готово
    
    def init_view(self):
        """Инициализировать представление после его создания"""
        self.update()
    
    def add_contact(self, name=None, phone=None, email=None, address=""):
        """Добавить контакт"""
        if name is None:
            # Вызов из кнопки - показать форму
            self.view.show_contact_form()
        else:
            # Вызов с параметрами - напрямую добавить
            self.model.add_contact(name, phone, email, address)
    
    def delete_contact(self):
        """Удалить контакт"""
        contact_id = self.view.get_selected_contact_id()
        if contact_id:
            if messagebox.askyesno("Подтверждение", "Удалить контакт?"):
                self.model.remove_contact(contact_id)
    
    def edit_contact(self):
        """Редактировать контакт"""
        contact_id = self.view.get_selected_contact_id()
        if contact_id:
            contact = self.model.get_contact(contact_id)
            if contact:
                self.view.show_contact_form(contact)
    
    def update_contact(self, contact_id, name, phone, email, address):
        """Обновить контакт"""
        self.model.update_contact(contact_id, name, phone, email, address)
    
    def search(self):
        """Поиск"""
        query = self.view.search_entry.get().strip()
        if query:
            results = self.model.search_contacts(query)
            self.view.set_contacts(results)
        else:
            self.update()
    
    def export_data(self):
        """Экспорт данных"""
        filename = tk.filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if filename:
            if self.model.export_csv(filename):
                messagebox.showinfo("Успех", "Данные экспортированы")
    
    def import_data(self):
        """Импорт данных"""
        filename = tk.filedialog.askopenfilename(
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        if filename:
            if self.model.import_csv(filename):
                messagebox.showinfo("Успех", "Данные импортированы")
                self.update()
    
    def update(self):
        """Обновить представление"""
        contacts = self.model.get_contacts()
        self.view.set_contacts(contacts)


class ContactsApp:
    """Приложение адресная книга"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Задача 4: Адресная книга")
        self.root.geometry("600x500")
        
        self.model = ContactsModel()
        # Сначала создаём контроллер без представления
        self.controller = ContactsController(self.model, None)
        # Потом создаём представление с контроллером
        self.view = ContactsView(self.root, self.controller)
        # Обновляем контроллер ссылкой на представление
        self.controller.view = self.view
        self.controller.init_view()


# ==============================================================================
# ЗАДАЧА 5: Архитектура приложения (MVC с разделением по модулям)
# ==============================================================================

class FullMVCDemo:
    """Демонстрация полной архитектуры MVC"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Задача 5: Архитектура MVC")
        self.root.geometry("800x600")
        
        # Notebook для разных приложений
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # To-Do
        todo_frame = ttk.Frame(notebook)
        notebook.add(todo_frame, text="Задачи")
        
        self.todo_model = TaskModel()
        self.todo_controller = TaskController(self.todo_model, None)
        self.todo_view = TaskView(todo_frame, self.todo_controller)
        self.todo_controller.view = self.todo_view
        self.todo_controller.init_view()
        
        # Заметки
        notes_frame = ttk.Frame(notebook)
        notebook.add(notes_frame, text="Заметки")
        
        self.notes_model = NotesModel()
        self.notes_controller = NotesController(self.notes_model, None)
        self.notes_view = NotesView(notes_frame, self.notes_controller)
        self.notes_controller.view = self.notes_view
        self.notes_controller.init_view()
        
        # Контакты
        contacts_frame = ttk.Frame(notebook)
        notebook.add(contacts_frame, text="Контакты")
        
        self.contacts_model = ContactsModel()
        self.contacts_controller = ContactsController(self.contacts_model, None)
        self.contacts_view = ContactsView(contacts_frame, self.contacts_controller)
        self.contacts_controller.view = self.contacts_view
        self.contacts_controller.init_view()


# ==============================================================================
# ГЛАВНОЕ МЕНЮ ПРИЛОЖЕНИЯ
# ==============================================================================

class MainApp:
    """Главное приложение с выбором задач"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Практическое занятие 25: Tkinter - паттерн MVC")
        self.root.geometry("500x400")
        
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
            ("Задача 1: MVC структура", self.open_task1),
            ("Задача 2: Приложение To-Do", self.open_task2),
            ("Задача 3: Приложение заметок", self.open_task3),
            ("Задача 4: Адресная книга", self.open_task4),
            ("Задача 5: Полная архитектура", self.open_task5),
        ]
        
        for text, command in tasks:
            btn = ttk.Button(main_frame, text=text, width=35, command=command)
            btn.pack(pady=5)
        
        ttk.Button(main_frame, text="Выход", command=self.root.quit).pack(pady=20)
    
    def open_task1(self):
        """Открыть задачу 1"""
        window = tk.Toplevel(self.root)
        window.title("Задача 1: MVC структура")
        window.geometry("500x400")
        
        frame = ttk.Frame(window, padding=20)
        frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(
            frame, 
            text="MVC (Model-View-Controller)",
            font=("Arial", 14, "bold")
        ).pack(pady=10)
        
        ttk.Label(
            frame,
            text="Model - хранит данные и бизнес-логику\n"
                 "View - отображает данные пользователю\n"
                 "Controller - обрабатывает действия пользователя",
            justify=tk.LEFT
        ).pack(pady=10)
        
        TodoApp(window)
    
    def open_task2(self):
        """Открыть задачу 2"""
        window = tk.Toplevel(self.root)
        TodoApp(window)
    
    def open_task3(self):
        """Открыть задачу 3"""
        window = tk.Toplevel(self.root)
        NotesApp(window)
    
    def open_task4(self):
        """Открыть задачу 4"""
        window = tk.Toplevel(self.root)
        ContactsApp(window)
    
    def open_task5(self):
        """Открыть задачу 5"""
        window = tk.Toplevel(self.root)
        FullMVCDemo(window)


def main():
    """Точка входа"""
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
