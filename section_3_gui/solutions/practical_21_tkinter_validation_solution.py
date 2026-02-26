# Решения для практического занятия 21: Tkinter - валидация ввода

import tkinter as tk
from tkinter import ttk, messagebox
import re


# =============================================================================
# Основное приложение валидации
# =============================================================================

class ValidationApp:
    """Приложение для валидации ввода"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Валидация ввода")
        self.root.geometry("400x300")
        
        # Создание элементов интерфейса
        self.create_widgets()
        
    def create_widgets(self):
        """Создает виджеты приложения"""
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
        
        # Поле для ввода пароля
        tk.Label(self.root, text="Пароль:").grid(row=3, column=0, sticky=tk.W, padx=10, pady=5)
        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(self.root, textvariable=self.password_var, show="*")
        self.password_entry.grid(row=3, column=1, padx=10, pady=5)
        
        # Поле для подтверждения пароля
        tk.Label(self.root, text="Подтверждение:").grid(row=4, column=0, sticky=tk.W, padx=10, pady=5)
        self.confirm_password_var = tk.StringVar()
        self.confirm_password_entry = tk.Entry(self.root, textvariable=self.confirm_password_var, show="*")
        self.confirm_password_entry.grid(row=4, column=1, padx=10, pady=5)
        
        # Кнопка отправки
        submit_btn = tk.Button(self.root, text="Отправить", command=self.validate_all)
        submit_btn.grid(row=5, column=0, columnspan=2, pady=20)
        
        # Метка для вывода результата
        self.result_label = tk.Label(self.root, text="", fg="red", wraplength=350)
        self.result_label.grid(row=6, column=0, columnspan=2)
        
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
    
    def validate_password(self, password):
        """Проверяет надежность пароля"""
        # Минимум 8 символов, хотя бы одна цифра
        if len(password) < 8:
            return False
        if not re.search(r'\d', password):
            return False
        return True
    
    def validate_passwords_match(self, password, confirm):
        """Проверяет совпадение паролей"""
        return password == confirm
    
    def validate_all(self):
        """Выполняет валидацию всех полей"""
        email = self.email_var.get()
        phone = self.phone_var.get()
        age = self.age_var.get()
        password = self.password_var.get()
        confirm = self.confirm_password_var.get()
        
        errors = []
        
        # Проверка email
        if not email:
            errors.append("Email обязателен")
            self.email_entry.config(bg="#ffcccc")
        elif not self.validate_email(email):
            errors.append("Неверный формат email")
            self.email_entry.config(bg="#ffcccc")
        else:
            self.email_entry.config(bg="white")
            
        # Проверка телефона
        if not phone:
            errors.append("Телефон обязателен")
            self.phone_entry.config(bg="#ffcccc")
        elif not self.validate_phone(phone):
            errors.append("Неверный формат телефона")
            self.phone_entry.config(bg="#ffcccc")
        else:
            self.phone_entry.config(bg="white")
            
        # Проверка возраста
        if not age:
            errors.append("Возраст обязателен")
            self.age_entry.config(bg="#ffcccc")
        elif not self.validate_age(age):
            errors.append("Возраст должен быть от 1 до 120")
            self.age_entry.config(bg="#ffcccc")
        else:
            self.age_entry.config(bg="white")
        
        # Проверка пароля
        if not password:
            errors.append("Пароль обязателен")
            self.password_entry.config(bg="#ffcccc")
        elif not self.validate_password(password):
            errors.append("Пароль должен быть минимум 8 символов и содержать цифру")
            self.password_entry.config(bg="#ffcccc")
        else:
            self.password_entry.config(bg="white")
        
        # Проверка подтверждения пароля
        if not confirm:
            errors.append("Подтверждение пароля обязательно")
            self.confirm_password_entry.config(bg="#ffcccc")
        elif not self.validate_passwords_match(password, confirm):
            errors.append("Пароли не совпадают")
            self.confirm_password_entry.config(bg="#ffcccc")
        else:
            self.confirm_password_entry.config(bg="white")
        
        # Вывод результатов
        if errors:
            self.result_label.config(text="\n".join(errors), fg="red")
        else:
            self.result_label.config(text="Все данные корректны!", fg="green")
            messagebox.showinfo("Успех", "Все данные введены корректно!")


# =============================================================================
# Расширенная валидация с использованием регистрации
# =============================================================================

class ExtendedValidationApp:
    """Расширенное приложение с комплексной валидацией"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Расширенная валидация")
        self.root.geometry("500x600")
        
        # Создаем Notebook для организации
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Вкладка личных данных
        self.personal_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.personal_tab, text="Личные данные")
        self.create_personal_tab()
        
        # Вкладка контактных данных
        self.contact_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.contact_tab, text="Контактные данные")
        self.create_contact_tab()
        
        # Вкладка безопасности
        self.security_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.security_tab, text="Безопасность")
        self.create_security_tab()
        
        # Кнопка валидации
        self.validate_btn = ttk.Button(self.root, text="Проверить все", command=self.validate_all)
        self.validate_btn.pack(pady=10)
        
        # Результат
        self.result_text = tk.Text(self.root, height=8, state=tk.DISABLED)
        self.result_text.pack(fill=tk.X, padx=10, pady=5)
    
    def create_personal_tab(self):
        """Создает вкладку личных данных"""
        frame = ttk.LabelFrame(self.personal_tab, text="Личные данные")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Имя
        ttk.Label(frame, text="Имя:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.first_name_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.first_name_var, width=30).grid(row=0, column=1, padx=5, pady=5)
        
        # Фамилия
        ttk.Label(frame, text="Фамилия:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.last_name_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.last_name_var, width=30).grid(row=1, column=1, padx=5, pady=5)
        
        # Дата рождения
        ttk.Label(frame, text="Дата рождения:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.birth_date_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.birth_date_var, width=30).grid(row=2, column=1, padx=5, pady=5)
        
    def create_contact_tab(self):
        """Создает вкладку контактных данных"""
        frame = ttk.LabelFrame(self.contact_tab, text="Контактные данные")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Email
        ttk.Label(frame, text="Email:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.email_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.email_var, width=30).grid(row=0, column=1, padx=5, pady=5)
        
        # Телефон
        ttk.Label(frame, text="Телефон:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.phone_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.phone_var, width=30).grid(row=1, column=1, padx=5, pady=5)
        
        # Адрес
        ttk.Label(frame, text="Адрес:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.address_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.address_var, width=30).grid(row=2, column=1, padx=5, pady=5)
        
    def create_security_tab(self):
        """Создает вкладку безопасности"""
        frame = ttk.LabelFrame(self.security_tab, text="Безопасность")
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Пароль
        ttk.Label(frame, text="Пароль:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.password_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.password_var, show="*", width=30).grid(row=0, column=1, padx=5, pady=5)
        
        # Подтверждение
        ttk.Label(frame, text="Подтверждение:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.confirm_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.confirm_var, show="*", width=30).grid(row=1, column=1, padx=5, pady=5)
        
        # Индикатор надежности пароля
        ttk.Label(frame, text="Надежность:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.strength_var = tk.StringVar(value="Не определена")
        ttk.Label(frame, textvariable=self.strength_var).grid(row=2, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Связываем проверку пароля с изменением
        self.password_var.trace('w', self.check_password_strength)
    
    def check_password_strength(self, *args):
        """Проверяет надежность пароля"""
        password = self.password_var.get()
        
        if len(password) == 0:
            self.strength_var.set("Не определена")
            return
        
        score = 0
        
        if len(password) >= 8:
            score += 1
        if len(password) >= 12:
            score += 1
        if re.search(r'[a-z]', password):
            score += 1
        if re.search(r'[A-Z]', password):
            score += 1
        if re.search(r'\d', password):
            score += 1
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 1
        
        if score <= 2:
            self.strength_var.set("Слабый")
        elif score <= 4:
            self.strength_var.set("Средний")
        else:
            self.strength_var.set("Сильный")
    
    def validate_all(self):
        """Валидирует все данные"""
        errors = []
        
        # Валидация имени
        first_name = self.first_name_var.get()
        if not first_name or len(first_name) < 2:
            errors.append("Имя должно содержать минимум 2 символа")
        
        # Валидация фамилии
        last_name = self.last_name_var.get()
        if not last_name or len(last_name) < 2:
            errors.append("Фамилия должна содержать минимум 2 символа")
        
        # Валидация email
        email = self.email_var.get()
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            errors.append("Неверный формат email")
        
        # Валидация телефона
        phone = self.phone_var.get()
        digits = re.sub(r'\D', '', phone)
        if len(digits) < 10:
            errors.append("Телефон должен содержать минимум 10 цифр")
        
        # Валидация пароля
        password = self.password_var.get()
        if len(password) < 8:
            errors.append("Пароль должен быть минимум 8 символов")
        
        # Валидация подтверждения
        if password != self.confirm_var.get():
            errors.append("Пароли не совпадают")
        
        # Вывод результатов
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        
        if errors:
            self.result_text.insert(tk.END, "Ошибки валидации:\n")
            for i, error in enumerate(errors, 1):
                self.result_text.insert(tk.END, f"{i}. {error}\n")
        else:
            self.result_text.insert(tk.END, "Все данные корректны!")
            messagebox.showinfo("Успех", "Валидация прошла успешно!")
        
        self.result_text.config(state=tk.DISABLED)
    
    def run(self):
        self.root.mainloop()


# =============================================================================
# Главная функция
# =============================================================================

def main():
    """Главная функция для запуска приложений"""
    print("Решения для практического занятия 21: Tkinter - валидация ввода")
    print("=" * 70)
    print("Выберите приложение для запуска:")
    print("1 - Базовая валидация")
    print("2 - Расширенная валидация")
    print("0 - Выход")
    print("=" * 70)
    
    choice = input("Ваш выбор: ")
    
    if choice == "1":
        root = tk.Tk()
        app = ValidationApp(root)
        root.mainloop()
    elif choice == "2":
        app = ExtendedValidationApp()
        app.run()
    else:
        print("До свидания!")


if __name__ == "__main__":
    main()
