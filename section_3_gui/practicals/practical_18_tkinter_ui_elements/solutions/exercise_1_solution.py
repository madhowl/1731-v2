# Решение упражнения 1: Форма регистрации

import tkinter as tk
from tkinter import ttk, messagebox

class RegistrationFormSolution:
    """
    Решение упражнения 1: Создание формы регистрации
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Форма регистрации - Решение")
        self.root.geometry("500x600")
        
        self.create_widgets()
    
    def create_widgets(self):
        """
        Создание виджетов формы регистрации
        """
        # Основной фрейм
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        title_label = ttk.Label(main_frame, text="Регистрация пользователя", 
                               font=("Arial", 16, "bold"))
        title_label.pack(pady=10)
        
        # Поля формы
        fields = [
            ("Имя:", "name", False),
            ("Фамилия:", "surname", False),
            ("Email:", "email", False),
            ("Пароль:", "password", True),
            ("Подтверждение пароля:", "confirm_password", True)
        ]
        
        self.entries = {}
        for label, field_name, is_password in fields:
            frame = ttk.Frame(main_frame)
            frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(frame, text=label, width=20).pack(side=tk.LEFT)
            
            if is_password:
                entry = ttk.Entry(frame, show="*")
            else:
                entry = ttk.Entry(frame)
            
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            self.entries[field_name] = entry
        
        # Поле для возраста
        age_frame = ttk.Frame(main_frame)
        age_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(age_frame, text="Возраст:", width=20).pack(side=tk.LEFT)
        self.age_spinbox = ttk.Spinbox(age_frame, from_=1, to=120, width=10)
        self.age_spinbox.pack(side=tk.LEFT)
        
        # Пол
        gender_frame = ttk.Frame(main_frame)
        gender_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(gender_frame, text="Пол:", width=20).pack(side=tk.LEFT)
        
        self.gender_var = tk.StringVar(value="male")
        gender_radio_frame = ttk.Frame(gender_frame)
        gender_radio_frame.pack(side=tk.LEFT)
        
        ttk.Radiobutton(gender_radio_frame, text="Мужской", 
                       variable=self.gender_var, value="male").pack(side=tk.LEFT, padx=(5, 10))
        ttk.Radiobutton(gender_radio_frame, text="Женский", 
                       variable=self.gender_var, value="female").pack(side=tk.LEFT)
        
        # Интересы
        interests_frame = ttk.LabelFrame(main_frame, text="Интересы", padding="10")
        interests_frame.pack(fill=tk.X, pady=10)
        
        self.interests_vars = {}
        interests = ["Программирование", "Музыка", "Спорт", "Чтение", "Путешествия"]
        
        for i, interest in enumerate(interests):
            var = tk.BooleanVar()
            chk = ttk.Checkbutton(interests_frame, text=interest, variable=var)
            chk.grid(row=i//2, column=i%2, sticky="w", padx=5, pady=2)
            self.interests_vars[interest] = var
        
        # Подписка на рассылку
        self.newsletter_var = tk.BooleanVar()
        newsletter_chk = ttk.Checkbutton(main_frame, 
                                       text="Подписаться на рассылку", 
                                       variable=self.newsletter_var)
        newsletter_chk.pack(anchor="w", pady=5)
        
        # Кнопка регистрации
        register_btn = ttk.Button(main_frame, text="Зарегистрироваться", 
                               command=self.submit_form)
        register_btn.pack(pady=20)
    
    def submit_form(self):
        """
        Обработка отправки формы
        """
        # Сбор данных формы
        data = {
            "name": self.entries["name"].get().strip(),
            "surname": self.entries["surname"].get().strip(),
            "email": self.entries["email"].get().strip(),
            "password": self.entries["password"].get(),
            "confirm_password": self.entries["confirm_password"].get(),
            "age": self.age_spinbox.get(),
            "gender": self.gender_var.get(),
            "newsletter": self.newsletter_var.get()
        }
        
        # Проверка обязательных полей
        if not data["name"]:
            messagebox.showerror("Ошибка", "Имя обязательно!")
            return
        
        if not data["surname"]:
            messagebox.showerror("Ошибка", "Фамилия обязательна!")
            return
        
        if not data["email"]:
            messagebox.showerror("Ошибка", "Email обязателен!")
            return
        
        if "@" not in data["email"] or "." not in data["email"].split("@")[-1]:
            messagebox.showerror("Ошибка", "Некорректный формат email!")
            return
        
        if not data["password"]:
            messagebox.showerror("Ошибка", "Пароль обязателен!")
            return
        
        if data["password"] != data["confirm_password"]:
            messagebox.showerror("Ошибка", "Пароли не совпадают!")
            return
        
        if len(data["password"]) < 6:
            messagebox.showerror("Ошибка", "Пароль должен быть не менее 6 символов!")
            return
        
        # Проверка возраста
        try:
            age = int(data["age"])
            if age <= 0 or age > 150:
                raise ValueError("Некорректный возраст")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректный возраст!")
            return
        
        # Сбор интересов
        selected_interests = [interest for interest, var in self.interests_vars.items() if var.get()]
        
        # Вывод данных
        result_text = f"""
        Регистрация прошла успешно!
        
        Данные пользователя:
        Имя: {data['name']}
        Фамилия: {data['surname']}
        Email: {data['email']}
        Возраст: {data['age']}
        Пол: {'Мужской' if data['gender'] == 'male' else 'Женский'}
        Интересы: {', '.join(selected_interests) if selected_interests else 'Нет выбранных интересов'}
        Подписка на рассылку: {'Да' if data['newsletter'] else 'Нет'}
        """
        
        messagebox.showinfo("Успех", result_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = RegistrationFormSolution(root)
    root.mainloop()
