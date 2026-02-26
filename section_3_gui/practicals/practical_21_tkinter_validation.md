# Практическое занятие 21: Tkinter - валидация ввода

## Цель занятия
Научиться проверять и фильтровать пользовательский ввод в GUI-приложениях с использованием библиотеки Tkinter, освоить механизмы валидации и создавать отзывчивый интерфейс с обратной связью.

## Задачи
1. Изучить механизмы валидации ввода в Tkinter
2. Освоить использование валидаторов в виджетах Entry
3. Реализовать проверку данных с отображением ошибок
4. Создать форму с комплексной валидацией

## Ход работы

### 1. Основы валидации в Tkinter

Создайте файл `validation.py` и реализуйте функции для работы с валидацией:

#### Валидация email

```python
import re

def validate_email(email):
    """
    Проверяет корректность email адреса
    
    Args:
        email: Строка для проверки
        
    Returns:
        bool: True если email корректен
    """
    # ВАШ КОД ЗДЕСЬ - реализуйте проверку формата email
    # Используйте регулярное выражение
    pass  # Замените на ваш код
```

#### Валидация телефона

```python
def validate_phone(phone):
    """
    Проверяет корректность номера телефона
    
    Args:
        phone: Строка для проверки
        
    Returns:
        bool: True если номер корректен
    """
    # ВАШ КОД ЗДЕСЬ - реализуйте проверку формата телефона
    pass  # Замените на ваш код
```

#### Валидация возраста

```python
def validate_age(age):
    """
    Проверяет корректность возраста
    
    Args:
        age: Число для проверки
        
    Returns:
        bool: True если возраст в допустимом диапазоне
    """
    # ВАШ КОД ЗДЕСЬ - проверьте диапазон (например, 0-150)
    pass  # Замените на ваш код
```

---

## 1. Теоретическая часть: Валидация ввода в Tkinter

### Уровень 1 - Начальный

#### Задание 1.1: Базовая валидация с использованием register

Создайте форму с полями ввода и валидацией:

```python
import tkinter as tk
from tkinter import ttk
import re

class BasicValidationForm:
    """
    Форма с базовой валидацией
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Валидация формы")
        self.root.geometry("450x400")
        
        # ВАШ КОД ЗДЕСЬ - создайте валидаторы
        # Создайте форму с полями: email, телефон, возраст
        # Настройте валидацию для каждого поля
        pass  # Замените на ваш код
        
    def create_email_field(self):
        """
        Создает поле для ввода email с валидацией
        """
        # ВАШ КОД ЗДЕСЬ - создайте Label и Entry
        # Настройте валидатор через register
        # Тип валидации: 'key' - при вводе, 'focusout' - при потере фокуса
        pass  # Замените на ваш код
        
    def validate_email_input(self, action, index, value_if_allowed, 
                           prior_value, text, validation_type, trigger_type):
        """
        Валидирует ввод email
        
        Args:
            action: Тип действия (1-вставка, 0-удаление, -1-другое)
            index: Индекс символа
            value_if_allowed: Значение если валидация пройдена
            prior_value: Предыдущее значение
            text: Вводимый текст
            validation_type: Тип валидации
            trigger_type: Триггер
            
        Returns:
            bool: True если ввод разрешен
        """
        # ВАШ КОД ЗДЕСЬ - верните True/False на основе проверки
        pass  # Замените на ваш код

# Пример использования:
# root = tk.Tk()
# form = BasicValidationForm(root)
# root.mainloop()
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import tkinter as tk
from tkinter import ttk
import re

class BasicValidationForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Валидация формы")
        self.root.geometry("450x400")
        
        self.create_ui()
        
    def create_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Форма регистрации", 
                  font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Email
        ttk.Label(main_frame, text="Email:").pack(anchor=tk.W, pady=(10, 0))
        
        vcmd = (self.root.register(self.validate_email), 
                '%d', '%i', '%P', '%s', '%S', '%v', '%V')
        
        self.email_entry = ttk.Entry(main_frame, width=35, validate='key', 
                                    validatecommand=vcmd)
        self.email_entry.pack(pady=5, anchor=tk.W)
        
        self.email_error = ttk.Label(main_frame, text="", foreground="red")
        self.email_error.pack(anchor=tk.W)
        
        # Телефон
        ttk.Label(main_frame, text="Телефон:").pack(anchor=tk.W, pady=(10, 0))
        
        vcmd_phone = (self.root.register(self.validate_phone),
                     '%d', '%i', '%P', '%s', '%S', '%v', '%V')
        
        self.phone_entry = ttk.Entry(main_frame, width=35, validate='key',
                                    validatecommand=vcmd_phone)
        self.phone_entry.pack(pady=5, anchor=tk.W)
        
        self.phone_error = ttk.Label(main_frame, text="", foreground="red")
        self.phone_error.pack(anchor=tk.W)
        
        # Возраст
        ttk.Label(main_frame, text="Возраст:").pack(anchor=tk.W, pady=(10, 0))
        
        vcmd_age = (self.root.register(self.validate_age),
                   '%d', '%i', '%P', '%s', '%S', '%v', '%V')
        
        self.age_entry = ttk.Entry(main_frame, width=35, validate='key',
                                  validatecommand=vcmd_age)
        self.age_entry.pack(pady=5, anchor=tk.W)
        
        self.age_error = ttk.Label(main_frame, text="", foreground="red")
        self.age_error.pack(anchor=tk.W)
        
        # Кнопка проверки
        ttk.Button(main_frame, text="Проверить форму", 
                  command=self.validate_all).pack(pady=20)
        
    def validate_email(self, action, index, value_if_allowed, 
                      prior_value, text, validation_type, trigger_type):
        # Разрешаем удаление
        if action == '0':
            return True
            
        # Проверяем только цифры, буквы, @, ., -, _
        allowed_chars = set('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@.-_')
        
        if all(c in allowed_chars for c in text):
            return True
        return False
        
    def validate_phone(self, action, index, value_if_allowed,
                      prior_value, text, validation_type, trigger_type):
        if action == '0':
            return True
            
        # Разрешаем только цифры, +, -, (, )
        allowed_chars = set('0123456789+-() ')
        
        if all(c in allowed_chars for c in text):
            return True
        return False
        
    def validate_age(self, action, index, value_if_allowed,
                   prior_value, text, validation_type, trigger_type):
        if action == '0':
            return True
            
        # Разрешаем только цифры
        if text.isdigit():
            if value_if_allowed:
                age = int(value_if_allowed) if value_if_allowed else 0
                if age <= 150:
                    return True
        return False
        
    def validate_all(self):
        email = self.email_entry.get()
        phone = self.phone_entry.get()
        age = self.age_entry.get()
        
        # Валидация email
        email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(email_pattern, email):
            self.email_error.config(text="Некорректный email!")
        else:
            self.email_error.config(text="✓", foreground="green")
            
        # Валидация телефона
        if len(phone) < 10:
            self.phone_error.config(text="Слишком короткий номер!")
        else:
            self.phone_error.config(text="✓", foreground="green")
            
        # Валидация возраста
        if not age:
            self.age_error.config(text="Введите возраст!")
        else:
            age_int = int(age)
            if age_int < 1 or age_int > 150:
                self.age_error.config(text="Некорректный возраст!")
            else:
                self.age_error.config(text="✓", foreground="green")

# Пример использования:
root = tk.Tk()
form = BasicValidationForm(root)
root.mainloop()
```

</details>

### Уровень 2 - Средний

#### Задание 2.1: Визуальная обратная связь при валидации

Реализуйте подсветку полей с ошибками:

```python
import tkinter as tk
from tkinter import ttk

class VisualValidation:
    """
    Форма с визуальной валидацией
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Визуальная валидация")
        
        # ВАШ КОД ЗДЕСЬ - создайте форму с подсветкой:
        # Нормальное состояние - белый фон
        # Ошибка - красный фон
        # Успех - зеленый фон
        pass  # Замените на ваш код
        
    def set_field_error(self, widget):
        """
        Устанавливает состояние ошибки для поля
        
        Args:
            widget: Виджет поля
        """
        # ВАШ КОД ЗДЕСЬ - измените стиль поля на "ошибка"
        pass  # Замените на ваш код
        
    def set_field_success(self, widget):
        """
        Устанавливает состояние успеха для поля
        
        Args:
            widget: Виджет поля
        """
        # ВАШ КОД ЗДЕСЬ - измените стиль поля на "успех"
        pass  # Замените на ваш код

# Пример использования:
# root = tk.Tk()
# form = VisualValidation(root)
# root.mainloop()
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import tkinter as tk
from tkinter import ttk
import re

class VisualValidation:
    def __init__(self, root):
        self.root = root
        self.root.title("Визуальная валидация")
        self.root.geometry("450x350")
        
        # Стили для полей
        self.style = ttk.Style()
        self.style.configure('Normal.TEntry', fieldbackground='white')
        self.style.configure('Error.TEntry', fieldbackground='#ffcccc')
        self.style.configure('Success.TEntry', fieldbackground='#ccffcc')
        
        self.create_ui()
        
    def create_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Форма с визуальной валидацией", 
                  font=('Arial', 14, 'bold')).pack(pady=10)
        
        # Поле Email
        ttk.Label(main_frame, text="Email:").pack(anchor=tk.W, pady=(10, 0))
        self.email_entry = ttk.Entry(main_frame, width=35, style='Normal.TEntry')
        self.email_entry.pack(pady=5, anchor=tk.W)
        self.email_entry.bind('<FocusOut>', lambda e: self.validate_field('email'))
        
        # Поле Телефон
        ttk.Label(main_frame, text="Телефон:").pack(anchor=tk.W, pady=(10, 0))
        self.phone_entry = ttk.Entry(main_frame, width=35, style='Normal.TEntry')
        self.phone_entry.pack(pady=5, anchor=tk.W)
        self.phone_entry.bind('<FocusOut>', lambda e: self.validate_field('phone'))
        
        # Поле Пароль
        ttk.Label(main_frame, text="Пароль:").pack(anchor=tk.W, pady=(10, 0))
        self.password_entry = ttk.Entry(main_frame, width=35, show="*", style='Normal.TEntry')
        self.password_entry.pack(pady=5, anchor=tk.W)
        self.password_entry.bind('<FocusOut>', lambda e: self.validate_field('password'))
        
        # Поле Подтверждение пароля
        ttk.Label(main_frame, text="Подтвердите пароль:").pack(anchor=tk.W, pady=(10, 0))
        self.confirm_entry = ttk.Entry(main_frame, width=35, show="*", style='Normal.TEntry')
        self.confirm_entry.pack(pady=5, anchor=tk.W)
        self.confirm_entry.bind('<FocusOut>', lambda e: self.validate_field('confirm'))
        
        # Кнопка
        ttk.Button(main_frame, text="Зарегистрироваться", 
                  command=self.submit_form).pack(pady=20)
        
    def validate_field(self, field_name):
        if field_name == 'email':
            value = self.email_entry.get()
            pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            if re.match(pattern, value):
                self.email_entry.configure(style='Success.TEntry')
                return True
            else:
                self.email_entry.configure(style='Error.TEntry')
                return False
                
        elif field_name == 'phone':
            value = self.phone_entry.get()
            if len(value) >= 10 and value.replace('+', '').replace('-', '').replace('(', '').replace(')', '').replace(' ', '').isdigit():
                self.phone_entry.configure(style='Success.TEntry')
                return True
            else:
                self.phone_entry.configure(style='Error.TEntry')
                return False
                
        elif field_name == 'password':
            value = self.password_entry.get()
            if len(value) >= 6:
                self.password_entry.configure(style='Success.TEntry')
                return True
            else:
                self.password_entry.configure(style='Error.TEntry')
                return False
                
        elif field_name == 'confirm':
            value = self.confirm_entry.get()
            password = self.password_entry.get()
            if value == password and value != '':
                self.confirm_entry.configure(style='Success.TEntry')
                return True
            else:
                self.confirm_entry.configure(style='Error.TEntry')
                return False
                
        return False
        
    def submit_form(self):
        errors = []
        
        if not self.validate_field('email'):
            errors.append("Некорректный email")
        if not self.validate_field('phone'):
            errors.append("Некорректный телефон")
        if not self.validate_field('password'):
            errors.append("Слишком короткий пароль")
        if not self.validate_field('confirm'):
            errors.append("Пароли не совпадают")
            
        if errors:
            print("Ошибки:", errors)
        else:
            print("Форма валидна!")

# Пример использования:
root = tk.Tk()
form = VisualValidation(root)
root.mainloop()
```

</details>

### Уровень 3 - Продвинутый

#### Задание 3.1: Комплексная форма с валидацией

Создайте полноценную форму регистрации с комплексной валидацией:

```python
import tkinter as tk
from tkinter import ttk, messagebox

class RegistrationForm:
    """
    Форма регистрации с комплексной валидацией
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Регистрация")
        
        # ВАШ КОД ЗДЕСЬ - создайте форму с:
        # Множественными полями ввода
        # Валидацией при потере фокуса
        # Проверкой при отправке формы
        # Визуальной обратной связью
        pass  # Замените на ваш код
        
    def validate_all_fields(self):
        """
        Проверяет все поля формы
        
        Returns:
            dict: Словарь с результатами валидации
        """
        # ВАШ КОД ЗДЕСЬ - верните результаты проверки всех полей
        pass  # Замените на ваш код
        
    def submit(self):
        """
        Обрабатывает отправку формы
        """
        # ВАШ КОД ЗДЕСЬ - при успешной валидации покажите сообщение
        pass  # Замените на ваш код

# Пример использования:
# root = tk.Tk()
# form = RegistrationForm(root)
# root.mainloop()
```

<details>
<summary>Подсказка (раскройте, если нужна помощь)</summary>

```python
import tkinter as tk
from tkinter import ttk, messagebox
import re

class RegistrationForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Регистрация")
        self.root.geometry("500x550")
        
        # Стили
        self.style = ttk.Style()
        self.style.configure('Normal.TEntry', fieldbackground='white')
        self.style.configure('Error.TEntry', fieldbackground='#ffcccc')
        self.style.configure('Success.TEntry', fieldbackground='#ccffcc')
        
        self.fields = {}
        self.create_ui()
        
    def create_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Форма регистрации", 
                  font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Имя пользователя
        self.create_field(main_frame, "Имя пользователя:", "username", 
                         validator=self.validate_username)
        
        # Email
        self.create_field(main_frame, "Email:", "email",
                         validator=self.validate_email)
        
        # Пароль
        self.create_field(main_frame, "Пароль:", "password",
                         validator=self.validate_password, show="*")
        
        # Подтверждение пароля
        self.create_field(main_frame, "Подтвердите пароль:", "confirm_password",
                         validator=self.validate_confirm, show="*")
        
        # Телефон
        self.create_field(main_frame, "Телефон:", "phone",
                         validator=self.validate_phone)
        
        # Дата рождения
        self.create_field(main_frame, "Дата рождения:", "birthdate",
                         validator=self.validate_birthdate)
        
        # Чекбокс согласия
        self.accept_var = tk.BooleanVar()
        ttk.Checkbutton(main_frame, text="Я принимаю условия использования",
                       variable=self.accept_var).pack(pady=15)
        
        # Кнопки
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)
        
        ttk.Button(btn_frame, text="Зарегистрироваться", 
                  command=self.submit).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Очистить", 
                  command=self.clear_form).pack(side=tk.LEFT, padx=5)
        
    def create_field(self, parent, label, field_name, validator=None, show=None):
        ttk.Label(parent, text=label).pack(anchor=tk.W, pady=(10, 0))
        
        entry = ttk.Entry(parent, width=35, show=show, style='Normal.TEntry')
        entry.pack(pady=5, anchor=tk.W)
        
        error_label = ttk.Label(parent, text="", foreground="red", font=('Arial', 8))
        error_label.pack(anchor=tk.W)
        
        if validator:
            entry.bind('<FocusOut>', lambda e, v=validator, f=field_name: 
                     self.on_validate(v, f))
        
        self.fields[field_name] = {
            'entry': entry,
            'error': error_label,
            'validator': validator,
            'valid': False
        }
        
    def on_validate(self, validator, field_name):
        value = self.fields[field_name]['entry'].get()
        is_valid, error_msg = validator(value)
        
        self.fields[field_name]['valid'] = is_valid
        
        if is_valid:
            self.fields[field_name]['entry'].configure(style='Success.TEntry')
            self.fields[field_name]['error'].config(text="✓", foreground="green")
        else:
            self.fields[field_name]['entry'].configure(style='Error.TEntry')
            self.fields[field_name]['error'].config(text=error_msg)
            
    def validate_username(self, value):
        if not value:
            return False, "Обязательное поле"
        if len(value) < 3:
            return False, "Минимум 3 символа"
        if not re.match(r'^[a-zA-Zа-яА-ЯёЁ0-9_]+$', value):
            return False, "Только буквы, цифры и _"
        return True, ""
        
    def validate_email(self, value):
        if not value:
            return False, "Обязательное поле"
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(pattern, value):
            return False, "Некорректный email"
        return True, ""
        
    def validate_password(self, value):
        if not value:
            return False, "Обязательное поле"
        if len(value) < 6:
            return False, "Минимум 6 символов"
        if not re.search(r'[A-Za-z]', value):
            return False, "Должна быть хотя бы одна буква"
        if not re.search(r'[0-9]', value):
            return False, "Должна быть хотя бы одна цифра"
        return True, ""
        
    def validate_confirm(self, value):
        if not value:
            return False, "Обязательное поле"
        password = self.fields['password']['entry'].get()
        if value != password:
            return False, "Пароли не совпадают"
        return True, ""
        
    def validate_phone(self, value):
        if not value:
            return True, ""  # Необязательное поле
        cleaned = value.replace('+', '').replace('-', '').replace('(', '').replace(')', '').replace(' ', '')
        if not cleaned.isdigit() or len(cleaned) < 10:
            return False, "Некорректный номер"
        return True, ""
        
    def validate_birthdate(self, value):
        if not value:
            return True, ""  # Необязательное поле
        # Простая проверка формата ДД.ММ.ГГГГ
        if not re.match(r'^\d{2}\.\d{2}\.\d{4}$', value):
            return False, "Формат: ДД.ММ.ГГГГ"
        return True, ""
        
    def submit(self):
        # Проверяем все обязательные поля
        required = ['username', 'email', 'password', 'confirm_password']
        
        for field_name in required:
            validator = self.fields[field_name]['validator']
            self.on_validate(validator, field_name)
            
        # Проверяем чекбокс
        if not self.accept_var.get():
            messagebox.showwarning("Внимание", "Вы должны принять условия использования!")
            return
            
        # Проверяем общее состояние
        all_valid = all(self.fields[f]['valid'] for f in required)
        
        if all_valid:
            messagebox.showinfo("Успех", "Регистрация успешна!")
        else:
            messagebox.showerror("Ошибка", "Исправьте ошибки в форме!")
            
    def clear_form(self):
        for field_data in self.fields.values():
            field_data['entry'].delete(0, tk.END)
            field_data['entry'].configure(style='Normal.TEntry')
            field_data['error'].config(text="")
            field_data['valid'] = False
        self.accept_var.set(False)

# Пример использования:
root = tk.Tk()
form = RegistrationForm(root)
root.mainloop()
```

</details>

---

## Требования к отчету
- Исходный код всех созданных приложений
- Описание механизмов валидации в Tkinter
- Скриншоты интерфейсов
- Примеры обработки ошибок

## Критерии оценки
- Корректность валидации: 50%
- Визуальная обратная связь: 30%
- Качество кода: 20%
