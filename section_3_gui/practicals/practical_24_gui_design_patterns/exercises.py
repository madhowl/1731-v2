# Упражнения для практического занятия 24: GUI - паттерны проектирования

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from abc import ABC, abstractmethod
import json
import os
from typing import Dict, Any, List
import threading
import time
import random

# Задание 1: Паттерн MVC
class TaskModel:
    """Модель данных для задач"""
    def __init__(self):
        self.tasks = []
        self.next_id = 1
    
    def add_task(self, title: str, description: str = "", completed: bool = False):
        """Добавляет задачу"""
        task = {
            'id': self.next_id,
            'title': title,
            'description': description,
            'completed': completed,
            'created_at': __import__('datetime').datetime.now().isoformat()
        }
        self.tasks.append(task)
        self.next_id += 1
        return task['id']
    
    def update_task(self, task_id: int, title: str = None, description: str = None, completed: bool = None):
        """Обновляет задачу"""
        for task in self.tasks:
            if task['id'] == task_id:
                if title is not None:
                    task['title'] = title
                if description is not None:
                    task['description'] = description
                if completed is not None:
                    task['completed'] = completed
                task['updated_at'] = __import__('datetime').datetime.now().isoformat()
                return True
        return False
    
    def delete_task(self, task_id: int):
        """Удаляет задачу"""
        self.tasks = [task for task in self.tasks if task['id'] != task_id]
    
    def get_tasks(self, completed: bool = None) -> List[Dict[str, Any]]:
        """Получает задачи с фильтрацией по статусу"""
        if completed is None:
            return self.tasks.copy()
        return [task for task in self.tasks if task['completed'] == completed]
    
    def toggle_task_completion(self, task_id: int):
        """Переключает статус выполнения задачи"""
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = not task['completed']
                task['updated_at'] = __import__('datetime').datetime.now().isoformat()
                return True
        return False

class TaskView:
    """Представление для задач"""
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Заголовок
        title_label = ttk.Label(self.frame, text="Список задач", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Создаем Treeview для отображения задач
        tree_scrollbar = ttk.Scrollbar(self.frame)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(self.frame, columns=("Title", "Description", "Status"), 
                                show="tree headings", yscrollcommand=tree_scrollbar.set)
        self.tree.heading("#0", text="ID")
        self.tree.heading("Title", text="Заголовок")
        self.tree.heading("Description", text="Описание")
        self.tree.heading("Status", text="Статус")
        
        self.tree.column("#0", width=50)
        self.tree.column("Title", width=150)
        self.tree.column("Description", width=200)
        self.tree.column("Status", width=100)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        tree_scrollbar.config(command=self.tree.yview)
        
        # Кнопки управления
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.add_button = ttk.Button(button_frame, text="Добавить задачу")
        self.add_button.pack(side=tk.LEFT, padx=5)
        
        self.edit_button = ttk.Button(button_frame, text="Редактировать задачу")
        self.edit_button.pack(side=tk.LEFT, padx=5)
        
        self.delete_button = ttk.Button(button_frame, text="Удалить задачу")
        self.delete_button.pack(side=tk.LEFT, padx=5)
        
        self.refresh_button = ttk.Button(button_frame, text="Обновить")
        self.refresh_button.pack(side=tk.LEFT, padx=5)
    
    def update_tasks(self, tasks: List[Dict[str, Any]]):
        """Обновляет отображение задач"""
        # Очищаем дерево
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Добавляем задачи
        for task in tasks:
            status = "Выполнена" if task['completed'] else "В процессе"
            self.tree.insert("", tk.END, text=str(task['id']), 
                           values=(task['title'], task['description'], status))
    
    def get_selected_task_id(self) -> int:
        """Получает ID выбранной задачи"""
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            return int(item['text'])
        return None

class TaskController:
    """Контроллер для задач"""
    def __init__(self, model: TaskModel, view: TaskView):
        self.model = model
        self.view = view
        
        # Привязываем события к кнопкам
        self.view.add_button.config(command=self.add_task)
        self.view.edit_button.config(command=self.edit_task)
        self.view.delete_button.config(command=self.delete_task)
        self.view.refresh_button.config(command=self.refresh_tasks)
        
        # Привязываем событие выбора задачи
        self.view.tree.bind("<<TreeviewSelect>>", self.on_task_select)
        
        # Инициализируем отображение
        self.refresh_tasks()
    
    def add_task(self):
        """Добавляет задачу"""
        # В реальном приложении здесь был бы диалог добавления
        task_id = self.model.add_task("Новая задача", "Описание новой задачи")
        self.refresh_tasks()
        messagebox.showinfo("Информация", f"Добавлена задача с ID {task_id}")
    
    def edit_task(self):
        """Редактирует задачу"""
        task_id = self.view.get_selected_task_id()
        if task_id:
            # В реальном приложении здесь был бы диалог редактирования
            task = None
            for t in self.model.get_tasks():
                if t['id'] == task_id:
                    task = t
                    break
            if task:
                messagebox.showinfo("Редактирование", f"Редактирование задачи {task_id}: {task['title']}")
        else:
            messagebox.showwarning("Предупреждение", "Выберите задачу для редактирования")
    
    def delete_task(self):
        """Удаляет задачу"""
        task_id = self.view.get_selected_task_id()
        if task_id:
            self.model.delete_task(task_id)
            self.refresh_tasks()
            messagebox.showinfo("Информация", f"Удалена задача с ID {task_id}")
        else:
            messagebox.showwarning("Предупреждение", "Выберите задачу для удаления")
    
    def refresh_tasks(self):
        """Обновляет отображение задач"""
        tasks = self.model.get_tasks()
        self.view.update_tasks(tasks)
    
    def on_task_select(self, event):
        """Обработка выбора задачи"""
        task_id = self.view.get_selected_task_id()
        if task_id:
            # Найти задачу и отобразить информацию
            for task in self.model.get_tasks():
                if task['id'] == task_id:
                    messagebox.showinfo("Выбранная задача", 
                                      f"ID: {task['id']}\nНазвание: {task['title']}\nСтатус: {'Выполнена' if task['completed'] else 'В процессе'}")
                    break

class MVCApp:
    """Приложение с паттерном MVC"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Задание 1: Паттерн MVC")
        self.root.geometry("800x600")
        
        # Создаем модель, представление и контроллер
        model = TaskModel()
        view = TaskView(self.root)
        self.controller = TaskController(model, view)
    
    def run(self):
        self.root.mainloop()

# Задание 2: Паттерн MVP
class TaskPresenter:
    """Презентер для задач (MVP)"""
    def __init__(self, model: TaskModel, view):
        self.model = model
        self.view = view
        self.view.set_presenter(self)
        
        # Инициализируем отображение
        self.update_view()
    
    def add_task(self, title: str, description: str):
        """Добавляет задачу"""
        if title.strip():
            self.model.add_task(title, description)
            self.update_view()
            return True
        return False
    
    def update_task(self, task_id: int, title: str = None, description: str = None, completed: bool = None):
        """Обновляет задачу"""
        success = self.model.update_task(task_id, title, description, completed)
        if success:
            self.update_view()
        return success
    
    def delete_task(self, task_id: int):
        """Удаляет задачу"""
        self.model.delete_task(task_id)
        self.update_view()
    
    def toggle_task_completion(self, task_id: int):
        """Переключает статус задачи"""
        self.model.toggle_task_completion(task_id)
        self.update_view()
    
    def update_view(self):
        """Обновляет представление"""
        tasks = self.model.get_tasks()
        self.view.update_task_list(tasks)
    
    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """Получает все задачи"""
        return self.model.get_tasks()

class TaskViewMVP:
    """Представление для MVP паттерна"""
    def __init__(self, parent):
        self.presenter = None
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Заголовок
        title_label = ttk.Label(self.frame, text="MVP: Список задач", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Форма добавления задачи
        add_frame = ttk.Frame(self.frame)
        add_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(add_frame, text="Название:").pack(side=tk.LEFT)
        self.title_entry = ttk.Entry(add_frame)
        self.title_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        ttk.Label(add_frame, text="Описание:").pack(side=tk.LEFT, padx=(10, 0))
        self.desc_entry = ttk.Entry(add_frame)
        self.desc_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.add_task_btn = ttk.Button(add_frame, text="Добавить", command=self.add_task)
        self.add_task_btn.pack(side=tk.LEFT, padx=5)
        
        # Список задач
        list_frame = ttk.Frame(self.frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        tree_scrollbar = ttk.Scrollbar(list_frame)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(list_frame, columns=("Description", "Status"), 
                                show="tree headings", yscrollcommand=tree_scrollbar.set)
        self.tree.heading("#0", text="ID")
        self.tree.heading("Description", text="Описание")
        self.tree.heading("Status", text="Статус")
        
        self.tree.column("#0", width=50)
        self.tree.column("Description", width=200)
        self.tree.column("Status", width=100)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        tree_scrollbar.config(command=self.tree.yview)
        
        # Кнопки управления
        button_frame = ttk.Frame(self.frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        self.edit_btn = ttk.Button(button_frame, text="Редактировать", command=self.edit_task)
        self.edit_btn.pack(side=tk.LEFT, padx=5)
        
        self.delete_btn = ttk.Button(button_frame, text="Удалить", command=self.delete_task)
        self.delete_btn.pack(side=tk.LEFT, padx=5)
        
        self.toggle_btn = ttk.Button(button_frame, text="Переключить статус", command=self.toggle_status)
        self.toggle_btn.pack(side=tk.LEFT, padx=5)
        
        self.refresh_btn = ttk.Button(button_frame, text="Обновить", command=self.refresh_tasks)
        self.refresh_btn.pack(side=tk.LEFT, padx=5)
        
        # Привязываем событие выбора задачи
        self.tree.bind("<<TreeviewSelect>>", self.on_task_select)
    
    def set_presenter(self, presenter):
        """Устанавливает презентер"""
        self.presenter = presenter
    
    def update_task_list(self, tasks: List[Dict[str, Any]]):
        """Обновляет список задач"""
        # Очищаем дерево
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Добавляем задачи
        for task in tasks:
            status = "Выполнена" if task['completed'] else "В процессе"
            self.tree.insert("", tk.END, text=str(task['id']), 
                           values=(task['description'], status))
    
    def get_selected_task_id(self) -> int:
        """Получает ID выбранной задачи"""
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            return int(item['text'])
        return None
    
    def add_task(self):
        """Добавляет задачу через презентер"""
        title = self.title_entry.get().strip()
        description = self.desc_entry.get().strip()
        
        if self.presenter:
            success = self.presenter.add_task(title, description)
            if success:
                self.title_entry.delete(0, tk.END)
                self.desc_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Ошибка", "Название задачи не может быть пустым")
    
    def edit_task(self):
        """Редактирует задачу"""
        task_id = self.get_selected_task_id()
        if task_id and self.presenter:
            # В реальном приложении здесь был бы диалог редактирования
            task = None
            for t in self.presenter.get_all_tasks():
                if t['id'] == task_id:
                    task = t
                    break
            if task:
                messagebox.showinfo("Редактирование", f"Редактирование задачи {task_id}: {task['title']}")
        else:
            messagebox.showwarning("Предупреждение", "Выберите задачу для редактирования")
    
    def delete_task(self):
        """Удаляет задачу через презентер"""
        task_id = self.get_selected_task_id()
        if task_id and self.presenter:
            self.presenter.delete_task(task_id)
        else:
            messagebox.showwarning("Предупреждение", "Выберите задачу для удаления")
    
    def toggle_status(self):
        """Переключает статус задачи через презентер"""
        task_id = self.get_selected_task_id()
        if task_id and self.presenter:
            self.presenter.toggle_task_completion(task_id)
        else:
            messagebox.showwarning("Предупреждение", "Выберите задачу для переключения статуса")
    
    def refresh_tasks(self):
        """Обновляет список задач"""
        if self.presenter:
            self.presenter.update_view()
    
    def on_task_select(self, event):
        """Обработка выбора задачи"""
        pass  # MVP реализация не требует специальной обработки выбора

class MVPApp:
    """Приложение с паттерном MVP"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Задание 2: Паттерн MVP")
        self.root.geometry("800x600")
        
        # Создаем модель и представление
        model = TaskModel()
        view = TaskViewMVP(self.root)
        # Создаем презентер (он устанавливает себя в представление)
        self.presenter = TaskPresenter(model, view)
    
    def run(self):
        self.root.mainloop()

# Задание 3: Паттерн Command
class Command(ABC):
    """Абстрактный класс команды"""
    @abstractmethod
    def execute(self):
        pass
    
    @abstractmethod
    def undo(self):
        pass

class AddTaskCommand(Command):
    """Команда добавления задачи"""
    def __init__(self, model, title, description=""):
        self.model = model
        self.title = title
        self.description = description
        self.task_id = None
    
    def execute(self):
        """Выполняет команду добавления задачи"""
        self.task_id = self.model.add_task(self.title, self.description)
        return self.task_id
    
    def undo(self):
        """Отменяет команду добавления задачи"""
        if self.task_id:
            self.model.delete_task(self.task_id)
            return True
        return False

class DeleteTaskCommand(Command):
    """Команда удаления задачи"""
    def __init__(self, model, task_id):
        self.model = model
        self.task_id = task_id
        self.task_backup = None
    
    def execute(self):
        """Выполняет команду удаления задачи"""
        # Сохраняем задачу перед удалением
        for task in self.model.get_tasks():
            if task['id'] == self.task_id:
                self.task_backup = task.copy()
                break
        
        if self.task_backup:
            self.model.delete_task(self.task_id)
            return True
        return False
    
    def undo(self):
        """Отменяет команду удаления задачи"""
        if self.task_backup:
            # Восстанавливаем задачу
            self.model.tasks.append(self.task_backup)
            return True
        return False

class EditTaskCommand(Command):
    """Команда редактирования задачи"""
    def __init__(self, model, task_id, new_title, new_description):
        self.model = model
        self.task_id = task_id
        self.new_title = new_title
        self.new_description = new_description
        self.old_title = None
        self.old_description = None
        self.old_completed = None
    
    def execute(self):
        """Выполняет команду редактирования задачи"""
        for task in self.model.get_tasks():
            if task['id'] == self.task_id:
                self.old_title = task['title']
                self.old_description = task['description']
                self.old_completed = task['completed']
                break
        
        if self.old_title is not None:
            self.model.update_task(self.task_id, self.new_title, self.new_description)
            return True
        return False
    
    def undo(self):
        """Отменяет команду редактирования задачи"""
        if self.old_title is not None:
            self.model.update_task(self.task_id, self.old_title, self.old_description, self.old_completed)
            return True
        return False

class CommandInvoker:
    """Класс для выполнения команд"""
    def __init__(self):
        self.commands = []
        self.history = []
    
    def execute_command(self, command: Command):
        """Выполняет команду и добавляет в историю"""
        result = command.execute()
        self.history.append(command)
        return result
    
    def undo_last(self):
        """Отменяет последнюю команду"""
        if self.history:
            last_command = self.history.pop()
            return last_command.undo()
        return False
    
    def get_history_size(self):
        """Получает размер истории команд"""
        return len(self.history)

class CommandApp:
    """Приложение с паттерном Command"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Задание 3: Паттерн Command")
        self.root.geometry("900x700")
        
        # Модель данных
        self.model = TaskModel()
        
        # Инвокер команд
        self.invoker = CommandInvoker()
        
        # Создаем интерфейс
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="Редактор задач с поддержкой команд", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Форма добавления задачи
        add_frame = ttk.Frame(main_frame)
        add_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(add_frame, text="Название:").pack(side=tk.LEFT)
        self.add_title_entry = ttk.Entry(add_frame)
        self.add_title_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        ttk.Label(add_frame, text="Описание:").pack(side=tk.LEFT, padx=(10, 0))
        self.add_desc_entry = ttk.Entry(add_frame)
        self.add_desc_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.add_task_btn = ttk.Button(add_frame, text="Добавить задачу", command=self.add_task_command)
        self.add_task_btn.pack(side=tk.LEFT, padx=5)
        
        # Список задач
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        tree_scrollbar = ttk.Scrollbar(list_frame)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.task_tree = ttk.Treeview(list_frame, columns=("Description", "Status"), 
                                     show="tree headings", yscrollcommand=tree_scrollbar.set)
        self.task_tree.heading("#0", text="ID")
        self.task_tree.heading("Description", text="Описание")
        self.task_tree.heading("Status", text="Статус")
        
        self.task_tree.column("#0", width=50)
        self.task_tree.column("Description", width=200)
        self.task_tree.column("Status", width=100)
        
        self.task_tree.pack(fill=tk.BOTH, expand=True)
        tree_scrollbar.config(command=self.task_tree.yview)
        
        # Кнопки управления
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        self.delete_task_btn = ttk.Button(button_frame, text="Удалить задачу", command=self.delete_task_command)
        self.delete_task_btn.pack(side=tk.LEFT, padx=5)
        
        self.edit_task_btn = ttk.Button(button_frame, text="Редактировать задачу", command=self.edit_task_command)
        self.edit_task_btn.pack(side=tk.LEFT, padx=5)
        
        self.undo_btn = ttk.Button(button_frame, text="Отменить", command=self.undo_command)
        self.undo_btn.pack(side=tk.LEFT, padx=5)
        
        self.history_btn = ttk.Button(button_frame, text="История команд", command=self.show_history)
        self.history_btn.pack(side=tk.LEFT, padx=5)
        
        # Обновляем список задач
        self.update_task_list()
    
    def add_task_command(self):
        """Добавляет задачу с использованием команды"""
        title = self.add_title_entry.get().strip()
        description = self.add_desc_entry.get().strip()
        
        if title:
            command = AddTaskCommand(self.model, title, description)
            self.invoker.execute_command(command)
            self.add_title_entry.delete(0, tk.END)
            self.add_desc_entry.delete(0, tk.END)
            self.update_task_list()
        else:
            messagebox.showerror("Ошибка", "Название задачи не может быть пустым")
    
    def delete_task_command(self):
        """Удаляет задачу с использованием команды"""
        task_id = self.get_selected_task_id()
        if task_id:
            command = DeleteTaskCommand(self.model, task_id)
            self.invoker.execute_command(command)
            self.update_task_list()
        else:
            messagebox.showwarning("Предупреждение", "Выберите задачу для удаления")
    
    def edit_task_command(self):
        """Редактирует задачу с использованием команды"""
        task_id = self.get_selected_task_id()
        if task_id:
            # В реальном приложении здесь был бы диалог редактирования
            # Для простоты покажем сообщение
            task = None
            for t in self.model.get_tasks():
                if t['id'] == task_id:
                    task = t
                    break
            if task:
                new_title = f"Измененное: {task['title']}"
                new_desc = f"Измененное: {task['description']}"
                
                command = EditTaskCommand(self.model, task_id, new_title, new_desc)
                self.invoker.execute_command(command)
                self.update_task_list()
        else:
            messagebox.showwarning("Предупреждение", "Выберите задачу для редактирования")
    
    def undo_command(self):
        """Отменяет последнюю команду"""
        if self.invoker.undo_last():
            self.update_task_list()
            messagebox.showinfo("Информация", "Последняя команда отменена")
        else:
            messagebox.showwarning("Предупреждение", "Нет команд для отмены")
    
    def show_history(self):
        """Показывает историю команд"""
        history_size = self.invoker.get_history_size()
        messagebox.showinfo("История команд", f"Количество команд в истории: {history_size}")
    
    def get_selected_task_id(self) -> int:
        """Получает ID выбранной задачи"""
        selected = self.task_tree.selection()
        if selected:
            item = self.task_tree.item(selected[0])
            return int(item['text'])
        return None
    
    def update_task_list(self):
        """Обновляет список задач"""
        tasks = self.model.get_tasks()
        
        # Очищаем дерево
        for item in self.task_tree.get_children():
            self.task_tree.delete(item)
        
        # Добавляем задачи
        for task in tasks:
            status = "Выполнена" if task['completed'] else "В процессе"
            self.task_tree.insert("", tk.END, text=str(task['id']), 
                                values=(task['description'], status))
    
    def run(self):
        self.root.mainloop()

# Задание 4: Паттерн Observer в GUI
class Observable:
    """Наблюдаемый объект"""
    def __init__(self):
        self._observers = []
    
    def add_observer(self, observer):
        """Добавляет наблюдателя"""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def remove_observer(self, observer):
        """Удаляет наблюдателя"""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify_observers(self, event_data):
        """Уведомляет всех наблюдателей"""
        for observer in self._observers:
            observer.update(self, event_data)

class TaskObservableModel(Observable):
    """Модель задач с поддержкой наблюдения"""
    def __init__(self):
        super().__init__()
        self.tasks = []
        self.next_id = 1
    
    def add_task(self, title: str, description: str = "", completed: bool = False):
        """Добавляет задачу и уведомляет наблюдателей"""
        task = {
            'id': self.next_id,
            'title': title,
            'description': description,
            'completed': completed,
            'created_at': __import__('datetime').datetime.now().isoformat()
        }
        self.tasks.append(task)
        self.next_id += 1
        
        # Уведомляем наблюдателей
        self.notify_observers({
            'action': 'add',
            'task': task
        })
        
        return task['id']
    
    def update_task(self, task_id: int, title: str = None, description: str = None, completed: bool = None):
        """Обновляет задачу и уведомляет наблюдателей"""
        for task in self.tasks:
            if task['id'] == task_id:
                old_task = task.copy()
                
                if title is not None:
                    task['title'] = title
                if description is not None:
                    task['description'] = description
                if completed is not None:
                    task['completed'] = completed
                task['updated_at'] = __import__('datetime').datetime.now().isoformat()
                
                # Уведомляем наблюдателей
                self.notify_observers({
                    'action': 'update',
                    'old_task': old_task,
                    'new_task': task
                })
                
                return True
        return False
    
    def delete_task(self, task_id: int):
        """Удаляет задачу и уведомляет наблюдателей"""
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                deleted_task = task.copy()
                del self.tasks[i]
                
                # Уведомляем наблюдателей
                self.notify_observers({
                    'action': 'delete',
                    'task': deleted_task
                })
                
                return True
        return False

class Observer(ABC):
    """Интерфейс наблюдателя"""
    @abstractmethod
    def update(self, observable, event_data):
        pass

class TaskListView(Observer):
    """Представление списка задач как наблюдатель"""
    def __init__(self, parent):
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Заголовок
        title_label = ttk.Label(self.frame, text="Observer: Список задач", font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Создаем Treeview для отображения задач
        tree_scrollbar = ttk.Scrollbar(self.frame)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(self.frame, columns=("Description", "Status"), 
                                show="tree headings", yscrollcommand=tree_scrollbar.set)
        self.tree.heading("#0", text="ID")
        self.tree.heading("Description", text="Описание")
        self.tree.heading("Status", text="Статус")
        
        self.tree.column("#0", width=50)
        self.tree.column("Description", width=200)
        self.tree.column("Status", width=100)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        tree_scrollbar.config(command=self.tree.yview)
    
    def update(self, observable, event_data):
        """Обновление представления при изменении модели"""
        action = event_data['action']
        if action == 'add':
            task = event_data['task']
            status = "Выполнена" if task['completed'] else "В процессе"
            self.tree.insert("", tk.END, text=str(task['id']), 
                           values=(task['description'], status))
        elif action == 'update':
            task = event_data['new_task']
            # Найти и обновить элемент в дереве
            for item in self.tree.get_children():
                item_values = self.tree.item(item)
                if int(item_values['text']) == task['id']:
                    status = "Выполнена" if task['completed'] else "В процессе"
                    self.tree.item(item, values=(task['description'], status))
                    break
        elif action == 'delete':
            task = event_data['task']
            # Найти и удалить элемент из дерева
            for item in self.tree.get_children():
                item_values = self.tree.item(item)
                if int(item_values['text']) == task['id']:
                    self.tree.delete(item)
                    break
    
    def populate_tasks(self, tasks):
        """Заполняет дерево начальными задачами"""
        for task in tasks:
            status = "Выполнена" if task['completed'] else "В процессе"
            self.tree.insert("", tk.END, text=str(task['id']), 
                           values=(task['description'], status))

class StatusBarView(Observer):
    """Представление статуса как наблюдатель"""
    def __init__(self, parent):
        self.status_label = ttk.Label(parent, text="Готово", relief=tk.SUNKEN)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
    
    def update(self, observable, event_data):
        """Обновление статуса при изменении модели"""
        action = event_data['action']
        if action == 'add':
            task = event_data['task']
            self.status_label.config(text=f"Добавлена задача: {task['title']}")
        elif action == 'update':
            task = event_data['new_task']
            self.status_label.config(text=f"Обновлена задача: {task['title']}")
        elif action == 'delete':
            task = event_data['task']
            self.status_label.config(text=f"Удалена задача: {task['title']}")

class ObserverApp:
    """Приложение с паттерном Observer"""
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Задание 4: Паттерн Observer")
        self.root.geometry("800x600")
        
        # Создаем наблюдаемую модель
        self.model = TaskObservableModel()
        
        # Создаем наблюдателей
        self.task_list_view = TaskListView(self.root)
        self.status_bar_view = StatusBarView(self.root)
        
        # Регистрируем наблюдателей
        self.model.add_observer(self.task_list_view)
        self.model.add_observer(self.status_bar_view)
        
        # Заполняем начальными задачами
        initial_tasks = [
            {"title": "Изучить паттерн MVC", "description": "Прочитать документацию"},
            {"title": "Изучить паттерн MVP", "description": "Практическое задание"},
            {"title": "Изучить паттерн Command", "description": "Реализовать систему команд"}
        ]
        
        for task in initial_tasks:
            self.model.add_task(task['title'], task['description'])
        
        # Кнопки управления
        button_frame = ttk.Frame(self.root)
        button_frame.pack(fill=tk.X, pady=10)
        
        self.add_btn = ttk.Button(button_frame, text="Добавить задачу", command=self.add_task)
        self.add_btn.pack(side=tk.LEFT, padx=5)
        
        self.update_btn = ttk.Button(button_frame, text="Обновить задачу", command=self.update_task)
        self.update_btn.pack(side=tk.LEFT, padx=5)
        
        self.delete_btn = ttk.Button(button_frame, text="Удалить задачу", command=self.delete_task)
        self.delete_btn.pack(side=tk.LEFT, padx=5)
    
    def add_task(self):
        """Добавляет случайную задачу"""
        titles = ["Новая задача 1", "Задача 2", "Работа 3", "Проект 4", "Учеба 5"]
        descriptions = ["Описание задачи", "Детали проекта", "Требуется выполнить", "Срочно", "Важно"]
        
        title = random.choice(titles)
        desc = random.choice(descriptions)
        
        self.model.add_task(f"{title} ({len(self.model.tasks)})", desc)
    
    def update_task(self):
        """Обновляет случайную задачу"""
        if self.model.tasks:
            task = random.choice(self.model.tasks)
            task_id = task['id']
            self.model.update_task(task_id, f"Обновлено: {task['title']}", 
                                 f"Обновлено: {task['description']}", 
                                 not task['completed'])
    
    def delete_task(self):
        """Удаляет случайную задачу"""
        if self.model.tasks:
            task = random.choice(self.model.tasks)
            self.model.delete_task(task['id'])
    
    def run(self):
        self.root.mainloop()

# Задание 5: Комплексное приложение "Заметки"
class NoteModel(TaskObservableModel):
    """Модель заметок с поддержкой наблюдения"""
    def __init__(self):
        super().__init__()
        self.notes = []
        self.next_id = 1
    
    def add_note(self, title: str, content: str, tags: List[str] = None):
        """Добавляет заметку"""
        note = {
            'id': self.next_id,
            'title': title,
            'content': content,
            'tags': tags or [],
            'created_at': __import__('datetime').datetime.now().isoformat(),
            'updated_at': __import__('datetime').datetime.now().isoformat()
        }
        self.notes.append(note)
        self.next_id += 1
        
        # Уведомляем наблюдателей
        self.notify_observers({
            'action': 'add_note',
            'note': note
        })
        
        return note['id']
    
    def update_note(self, note_id: int, title: str = None, content: str = None, tags: List[str] = None):
        """Обновляет заметку"""
        for note in self.notes:
            if note['id'] == note_id:
                old_note = note.copy()
                
                if title is not None:
                    note['title'] = title
                if content is not None:
                    note['content'] = content
                if tags is not None:
                    note['tags'] = tags
                note['updated_at'] = __import__('datetime').datetime.now().isoformat()
                
                # Уведомляем наблюдателей
                self.notify_observers({
                    'action': 'update_note',
                    'old_note': old_note,
                    'new_note': note
                })
                
                return True
        return False
    
    def delete_note(self, note_id: int):
        """Удаляет заметку"""
        for i, note in enumerate(self.notes):
            if note['id'] == note_id:
                deleted_note = note.copy()
                del self.notes[i]
                
                # Уведомляем наблюдателей
                self.notify_observers({
                    'action': 'delete_note',
                    'note': deleted_note
                })
                
                return True
        return False
    
    def get_notes(self, tag: str = None) -> List[Dict[str, Any]]:
        """Получает заметки с фильтрацией по тегу"""
        if tag:
            return [note for note in self.notes if tag in note['tags']]
        return self.notes.copy()

class NoteCommand(Command):
    """Абстрактная команда для работы с заметками"""
    pass

class AddNoteCommand(NoteCommand):
    """Команда добавления заметки"""
    def __init__(self, model, title, content, tags=None):
        self.model = model
        self.title = title
        self.content = content
        self.tags = tags or []
        self.note_id = None
    
    def execute(self):
        """Выполняет команду добавления заметки"""
        self.note_id = self.model.add_note(self.title, self.content, self.tags)
        return self.note_id
    
    def undo(self):
        """Отменяет команду добавления заметки"""
        if self.note_id:
            self.model.delete_note(self.note_id)
            return True
        return False

class UpdateNoteCommand(NoteCommand):
    """Команда обновления заметки"""
    def __init__(self, model, note_id, new_title, new_content, new_tags=None):
        self.model = model
        self.note_id = note_id
        self.new_title = new_title
        self.new_content = new_content
        self.new_tags = new_tags or []
        self.old_title = None
        self.old_content = None
        self.old_tags = None
    
    def execute(self):
        """Выполняет команду обновления заметки"""
        for note in self.model.notes:
            if note['id'] == self.note_id:
                self.old_title = note['title']
                self.old_content = note['content']
                self.old_tags = note['tags']
                break
        
        if self.old_title is not None:
            self.model.update_note(self.note_id, self.new_title, self.new_content, self.new_tags)
            return True
        return False
    
    def undo(self):
        """Отменяет команду обновления заметки"""
        if self.old_title is not None:
            self.model.update_note(self.note_id, self.old_title, self.old_content, self.old_tags)
            return True
        return False

class DeleteNoteCommand(NoteCommand):
    """Команда удаления заметки"""
    def __init__(self, model, note_id):
        self.model = model
        self.note_id = note_id
        self.note_backup = None
    
    def execute(self):
        """Выполняет команду удаления заметки"""
        for note in self.model.notes:
            if note['id'] == self.note_id:
                self.note_backup = note.copy()
                break
        
        if self.note_backup:
            self.model.delete_note(self.note_id)
            return True
        return False
    
    def undo(self):
        """Отменяет команду удаления заметки"""
        if self.note_backup:
            # Восстанавливаем заметку
            self.model.notes.append(self.note_backup)
            # Так как у нас нет прямого доступа к next_id, обновляем его вручную
            self.model.next_id = max(note['id'] for note in self.model.notes) + 1 if self.model.notes else 1
            return True
        return False

class NotesApp(QMainWindow):
    """Комплексное приложение - Заметки с использованием MVC, Command и Observer"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Задание 5: Комплексное приложение (Заметки)")
        self.setGeometry(100, 100, 1000, 700)
        
        # Создаем модель
        self.model = NoteModel()
        
        # Создаем инвокер команд
        self.command_invoker = CommandInvoker()
        
        # Создаем меню
        self.create_menu()
        
        # Создаем тулбар
        self.create_toolbar()
        
        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной макет
        layout = QHBoxLayout()
        
        # Левая панель - список заметок
        left_panel = self.create_notes_list_panel()
        layout.addWidget(left_panel, 1)
        
        # Правая панель - редактор заметки
        right_panel = self.create_note_editor_panel()
        layout.addWidget(right_panel, 2)
        
        central_widget.setLayout(layout)
        
        # Статус бар
        self.status_bar = self.statusBar()
        self.status_bar.showMessage("Готово")
    
    def create_menu(self):
        """Создает меню приложения"""
        menubar = self.menuBar()
        
        # Меню File
        file_menu = menubar.addMenu("Файл")
        
        save_action = QAction("Сохранить", self)
        save_action.triggered.connect(self.save_notes)
        file_menu.addAction(save_action)
        
        load_action = QAction("Загрузить", self)
        load_action.triggered.connect(self.load_notes)
        file_menu.addAction(load_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Выход", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
    
    def create_toolbar(self):
        """Создает тулбар"""
        toolbar = self.addToolBar("Основные")
        
        add_action = QAction("Добавить", self)
        add_action.triggered.connect(self.add_note)
        toolbar.addAction(add_action)
        
        delete_action = QAction("Удалить", self)
        delete_action.triggered.connect(self.delete_selected_note)
        toolbar.addAction(delete_action)
        
        undo_action = QAction("Отменить", self)
        undo_action.triggered.connect(self.undo_last_action)
        toolbar.addAction(undo_action)
    
    def create_notes_list_panel(self):
        """Создает панель со списком заметок"""
        panel = QFrame()
        panel_layout = QVBoxLayout()
        
        # Заголовок
        title_label = QLabel("Список заметок")
        title_label.setFont(QFont("Arial", 12, QFont.Bold))
        panel_layout.addWidget(title_label)
        
        # Список заметок
        self.notes_list = QListWidget()
        panel_layout.addWidget(self.notes_list)
        
        # Кнопки управления
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton("Добавить")
        add_btn.clicked.connect(self.add_note)
        button_layout.addWidget(add_btn)
        
        delete_btn = QPushButton("Удалить")
        delete_btn.clicked.connect(self.delete_selected_note)
        button_layout.addWidget(delete_btn)
        
        panel_layout.addLayout(button_layout)
        
        panel.setLayout(panel_layout)
        return panel
    
    def create_note_editor_panel(self):
        """Создает панель редактирования заметки"""
        panel = QFrame()
        panel_layout = QVBoxLayout()
        
        # Заголовок
        title_label = QLabel("Редактор заметки")
        title_label.setFont(QFont("Arial", 12, QFont.Bold))
        panel_layout.addWidget(title_label)
        
        # Поле заголовка
        panel_layout.addWidget(QLabel("Заголовок:"))
        self.note_title_entry = QLineEdit()
        panel_layout.addWidget(self.note_title_entry)
        
        # Поле тегов
        panel_layout.addWidget(QLabel("Теги (через запятую):"))
        self.note_tags_entry = QLineEdit()
        panel_layout.addWidget(self.note_tags_entry)
        
        # Поле содержимого
        panel_layout.addWidget(QLabel("Содержимое:"))
        self.note_content_text = QTextEdit()
        panel_layout.addWidget(self.note_content_text)
        
        # Кнопка сохранения
        save_btn = QPushButton("Сохранить изменения")
        save_btn.clicked.connect(self.save_note)
        panel_layout.addWidget(save_btn)
        
        panel.setLayout(panel_layout)
        return panel
    
    def add_note(self):
        """Добавляет новую заметку"""
        title = f"Новая заметка {len(self.model.notes) + 1}"
        content = "Содержимое новой заметки..."
        tags = ["новое", "заметка"]
        
        command = AddNoteCommand(self.model, title, content, tags)
        self.command_invoker.execute_command(command)
        
        self.status_bar.showMessage(f"Добавлена заметка: {title}")
        self.update_notes_list()
    
    def delete_selected_note(self):
        """Удаляет выбранную заметку"""
        selected = self.notes_list.currentRow()
        if selected >= 0:
            item = self.notes_list.item(selected)
            note_id = int(item.text().split()[1])  # Извлекаем ID из текста "Заметка #ID"
            
            command = DeleteNoteCommand(self.model, note_id)
            self.command_invoker.execute_command(command)
            
            self.status_bar.showMessage(f"Удалена заметка с ID {note_id}")
            self.update_notes_list()
        else:
            messagebox.showwarning("Предупреждение", "Выберите заметку для удаления")
    
    def save_note(self):
        """Сохраняет изменения в заметке"""
        selected = self.notes_list.currentRow()
        if selected >= 0:
            item = self.notes_list.item(selected)
            note_id = int(item.text().split()[1])  # Извлекаем ID
            
            title = self.note_title_entry.text()
            content = self.note_content_text.toPlainText()
            tags = [tag.strip() for tag in self.note_tags_entry.text().split(",") if tag.strip()]
            
            command = UpdateNoteCommand(self.model, note_id, title, content, tags)
            self.command_invoker.execute_command(command)
            
            self.status_bar.showMessage(f"Сохранены изменения в заметке {note_id}")
            self.update_notes_list()
        else:
            messagebox.showwarning("Предупреждение", "Выберите заметку для редактирования")
    
    def undo_last_action(self):
        """Отменяет последнее действие"""
        if self.command_invoker.undo_last():
            self.status_bar.showMessage("Последнее действие отменено")
            self.update_notes_list()
        else:
            messagebox.showwarning("Предупреждение", "Нет действий для отмены")
    
    def update_notes_list(self):
        """Обновляет список заметок"""
        self.notes_list.clear()
        
        for note in self.model.notes:
            item_text = f"Заметка #{note['id']}: {note['title']}"
            self.notes_list.addItem(item_text)
    
    def save_notes(self):
        """Сохраняет все заметки в файл"""
        filename, _ = QFileDialog.getSaveFileName(self, "Сохранить заметки", "", 
                                                 "JSON Files (*.json);;All Files (*)")
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.model.notes, f, ensure_ascii=False, indent=2)
                self.status_bar.showMessage(f"Заметки сохранены в {filename}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {str(e)}")
    
    def load_notes(self):
        """Загружает заметки из файла"""
        filename, _ = QFileDialog.getOpenFileName(self, "Загрузить заметки", "", 
                                                 "JSON Files (*.json);;All Files (*)")
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    loaded_notes = json.load(f)
                
                self.model.notes = loaded_notes
                if self.model.notes:
                    self.model.next_id = max(note['id'] for note in self.model.notes) + 1
                else:
                    self.model.next_id = 1
                
                self.update_notes_list()
                self.status_bar.showMessage(f"Заметки загружены из {filename}")
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось загрузить файл: {str(e)}")

# Примеры использования:
if __name__ == "__main__":
    print("=== Упражнения для практического занятия 24 ===")
    
    print("\n1. Задание 1: Паттерн MVC")
    # mvc_app = MVCApp()
    # mvc_app.run()  # Закомментировано для предотвращения автоматического запуска
    
    print("\n2. Задание 2: Паттерн MVP")
    # mvp_app = MVPApp()
    # mvp_app.run()  # Закомментировано
    
    print("\n3. Задание 3: Паттерн Command")
    # command_app = CommandApp()
    # command_app.run()  # Закомментировано
    
    print("\n4. Задание 4: Паттерн Observer")
    # observer_app = ObserverApp()
    # observer_app.run()  # Закомментировано
    
    print("\n5. Задание 5: Комплексное приложение (Заметки)")
    # app = QApplication(sys.argv)
    # notes_app = NotesApp()
    # notes_app.show()
    # sys.exit(app.exec_())  # Закомментировано
    
    print("\n6. Дополнительные примеры")
    # Для демонстрации запустим только одно приложение
    print("Для запуска приложений раскомментируйте соответствующие строки в коде")