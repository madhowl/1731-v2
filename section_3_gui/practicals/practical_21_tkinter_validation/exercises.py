# Упражнения для практического занятия 21: Tkinter - валидация ввода

import tkinter as tk
from tkinter import ttk, messagebox
import re

class ValidationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Валидация ввода")
        self.root.geometry("400x300")
        
        # Создание элементов интерфейса
        self.create_widgets()
        
    def create_widgets(self):
        # Поле для ввода email
        tk.Label(self.root, text="Email:").grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        self.email_var = tk.StringVar()
        self.email_entry = tk.Entry(self.root, textvariable=self.email_var)
        self.email_entry.grid(row=0, column=1, padx=10, pady=5)
        
        # Поле для ввода телефона
        tk.Label(self.root, text="Телефон:").grid(row=1, column=0, sticky=tk.W, padx=10, pady=5)
        self.phone_var = tk.StringVar()
        self.phone_entry = tk.Entry(self.root, textvariable=self.phone_var)
        self.phone_entry.grid(row=1, column=1, padx=10, pady=5)
        
        # Поле для ввода возраста
        tk.Label(self.root, text="Возраст:").grid(row=2, column=0, sticky=tk.W, padx=10, pady=5)
        self.age_var = tk.StringVar()
        self.age_entry = tk.Entry(self.root, textvariable=self.age_var)
        self.age_entry.grid(row=2, column=1, padx=10, pady=5)
        
        # Кнопка отправки
        submit_btn = tk.Button(self.root, text="Отправить", command=self.validate_all)
        submit_btn.grid(row=3, column=0, columnspan=2, pady=20)
        
        # Метка для вывода результата
        self.result_label = tk.Label(self.root, text="", fg="red")
        self.result_label.grid(row=4, column=0, columnspan=2)
    
    def validate_email(self, email):
        """Проверяет формат email"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_phone(self, phone):
        """Проверяет формат телефона"""
        # Простая проверка: только цифры, длина от 10 до 15
        digits_only = re.sub(r'\D', '', phone)
        return len(digits_only) >= 10 and len(digits_only) <= 15
    
    def validate_age(self, age_str):
        """Проверяет возраст (диапазон от 1 до 120)"""
        try:
            age = int(age_str)
            return 1 <= age <= 120
        except ValueError:
            return False
    
    def validate_all(self):
        """Выполняет валидацию всех полей"""
        email = self.email_var.get()
        phone = self.phone_var.get()
        age = self.age_var.get()
        
        errors = []
        
        # Проверка email
        if not self.validate_email(email):
            errors.append("Неверный формат email")
            self.email_entry.config(bg="#ffcccc")  # Красный фон
        else:
            self.email_entry.config(bg="white")
            
        # Проверка телефона
        if not self.validate_phone(phone):
            errors.append("Неверный формат телефона")
            self.phone_entry.config(bg="#ffcccc")  # Красный фон
        else:
            self.phone_entry.config(bg="white")
            
        # Проверка возраста
        if not self.validate_age(age):
            errors.append("Возраст должен быть от 1 до 120")
            self.age_entry.config(bg="#ffcccc")  # Красный фон
        else:
            self.age_entry.config(bg="white")
            
        # Вывод результатов
        if errors:
            self.result_label.config(text="\n".join(errors))
        else:
            self.result_label.config(text="Все данные корректны!", fg="green")
            messagebox.showinfo("Успех", "Все данные введены корректно!")

if __name__ == "__main__":
    root = tk.Tk()
    app = ValidationApp(root)
    root.mainloop()