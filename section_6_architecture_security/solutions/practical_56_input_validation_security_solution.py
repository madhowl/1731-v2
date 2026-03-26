#!/usr/bin/env python3
"""
Практическое занятие 56: Валидация входных данных
Решение упражнений
"""

import re
import html
from typing import Optional, List, Dict, Any
from dataclasses import dataclass


# ==============================================================================
# УПРАЖНЕНИЕ 1: Комплексная валидация
# ==============================================================================

print("=" * 60)
print("Упражнение 1: Комплексная валидация")
print("=" * 60)


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
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            errors.append("Invalid email format")
        
        if len(email) > 254:
            errors.append("Email is too long")
        
        sanitized = email.strip().lower()
        
        return ValidationResult(len(errors) == 0, errors, sanitized)
    
    @staticmethod
    def validate_username(username: str) -> ValidationResult:
        errors = []
        
        if not username:
            errors.append("Username is required")
            return ValidationResult(False, errors)
        
        if len(username) < 3:
            errors.append("Username must be at least 3 characters")
        
        if len(username) > 30:
            errors.append("Username is too long")
        
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            errors.append("Username can only contain letters, numbers, - and _")
        
        sanitized = username.strip().lower()
        
        return ValidationResult(len(errors) == 0, errors, sanitized)
    
    @staticmethod
    def validate_password(password: str) -> ValidationResult:
        errors = []
        
        if not password:
            errors.append("Password is required")
            return ValidationResult(False, errors)
        
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
            return ValidationResult(True, [], "")
        
        sanitized = re.sub(r'[^\d+]', '', phone)
        
        if not re.match(r'^\+?\d{10,15}$', sanitized):
            errors.append("Invalid phone number format")
        
        return ValidationResult(len(errors) == 0, errors, sanitized)
    
    @staticmethod
    def validate_url(url: str) -> ValidationResult:
        errors = []
        
        if not url:
            return ValidationResult(True, [], "")
        
        url_pattern = r'^https?://[^\s/$.?#].[^\s]*$'
        if not re.match(url_pattern, url, re.IGNORECASE):
            errors.append("Invalid URL format")
        
        return ValidationResult(len(errors) == 0, errors, url)
    
    @staticmethod
    def sanitize_html(dirty_html: str) -> str:
        """Санитизация HTML"""
        allowed_tags = ['b', 'i', 'u', 'em', 'strong', 'a', 'p', 'br']
        
        for tag in allowed_tags:
            dirty_html = re.sub(f'<{tag}([^>]*)>', f'<{tag}>', dirty_html)
        
        dangerous = ['<script', 'javascript:', 'onerror=', 'onclick=']
        for dangerous_tag in dangerous:
            dirty_html = dirty_html.replace(dangerous_tag, '')
        
        return dirty_html
    
    @staticmethod
    def sanitize_sql(unsafe_string: str) -> str:
        return unsafe_string.replace("'", "''")


validator = InputValidator()

result = validator.validate_email("  User@Example.com  ")
print(f"Email validation:")
print(f"  Valid: {result.is_valid}")
print(f"  Errors: {result.errors}")
print(f"  Sanitized: {result.sanitized_value}")

result = validator.validate_password("weak")
print(f"\nPassword validation:")
print(f"  Valid: {result.is_valid}")
print(f"  Errors: {result.errors}")


# ==============================================================================
# УПРАЖНЕНИЕ 2: Защита от SQL инъекций
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 2: Защита от SQL инъекций")
print("=" * 60)


class SecureDatabase:
    """Безопасная работа с базой данных"""
    
    @staticmethod
    def safe_query(query: str, params: tuple = None):
        """Безопасный запрос (параметризованный)"""
        # В реальном приложении здесь был бы код работы с БД
        return {'query': query, 'params': params, 'safe': True}
    
    @staticmethod
    def safe_insert(table: str, data: dict):
        """Безопасная вставка"""
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        return SecureDatabase.safe_query(query, tuple(data.values()))


# Пример использования
print("Параметризованный запрос:")
result = SecureDatabase.safe_query(
    "SELECT * FROM users WHERE username = %s",
    ("admin",)
)
print(f"  Query: {result['query']}")
print(f"  Params: {result['params']}")


# ==============================================================================
# УПРАЖНЕНИЕ 3: Защита от XSS
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 3: Защита от XSS")
print("=" * 60)


def display_comment_safe(comment: str) -> str:
    safe_comment = html.escape(comment)
    return f"<div class='comment'>{safe_comment}</div>"


def display_comment_template(comment: str) -> str:
    return f"<div class='comment'>{comment}</div>"


# Тестирование
unsafe_comment = "<script>alert('XSS')</script>Hello"
safe_comment = display_comment_safe(unsafe_comment)
print(f"Unsafe: {unsafe_comment}")
print(f"Safe: {safe_comment}")


# ==============================================================================
# УПРАЖНЕНИЕ 4: Защита от Path Traversal
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 4: Защита от Path Traversal")
print("=" * 60)


from pathlib import Path


class SafeFileHandler:
    """Безопасная обработка файлов"""
    
    def __init__(self, base_directory: str):
        self.base_directory = Path(base_directory).resolve()
    
    def _validate_path(self, file_path: str) -> Path:
        safe_path = file_path.replace('..', '')
        
        full_path = (self.base_directory / safe_path).resolve()
        
        if not str(full_path).startswith(str(self.base_directory)):
            raise ValueError("Access denied: Path outside allowed directory")
        
        return full_path
    
    def read_file(self, filename: str) -> str:
        try:
            path = self._validate_path(filename)
            
            if not path.exists():
                raise FileNotFoundError(f"File not found: {filename}")
            
            if not path.is_file():
                raise ValueError("Not a file")
            
            return f"Content of {path}"
        
        except (ValueError, FileNotFoundError):
            raise


handler = SafeFileHandler("/var/www/uploads")

print("Безопасные запросы:")
try:
    content = handler.read_file("documents/report.txt")
    print(f"  OK: {content}")
except Exception as e:
    print(f"  Error: {e}")

print("\nПопытка атаки path traversal:")
try:
    content = handler.read_file("../../etc/passwd")
except ValueError as e:
    print(f"  Blocked: {e}")


# ==============================================================================
# УПРАЖНЕНИЕ 5: Pydantic валидация
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 5: Валидация данных (упрощённая)")
print("=" * 60)


class UserRegistration:
    """Модель регистрации пользователя"""
    
    def __init__(self, username: str, email: str, password: str, phone: str = None):
        self.username = username
        self.email = email
        self.password = password
        self.phone = phone
        self._validate()
    
    def _validate(self):
        errors = []
        
        username_result = InputValidator.validate_username(self.username)
        if not username_result.is_valid:
            errors.extend(username_result.errors)
        
        email_result = InputValidator.validate_email(self.email)
        if not email_result.is_valid:
            errors.extend(email_result.errors)
        
        password_result = InputValidator.validate_password(self.password)
        if not password_result.is_valid:
            errors.extend(password_result.errors)
        
        if phone := self.phone:
            phone_result = InputValidator.validate_phone(phone)
            if not phone_result.is_valid:
                errors.extend(phone_result.errors)
        
        if errors:
            raise ValueError("; ".join(errors))
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'username': self.username,
            'email': self.email,
            'password': '***',
            'phone': self.phone
        }


try:
    user = UserRegistration(
        username="john_doe",
        email="john@example.com",
        password="SecurePass123!",
        phone="+79991234567"
    )
    print(f"User created: {user.to_dict()}")
except ValueError as e:
    print(f"Validation error: {e}")

try:
    user = UserRegistration(
        username="jo",
        email="invalid-email",
        password="weak",
        phone="invalid"
    )
except ValueError as e:
    print(f"Validation errors: {e}")


print("\n" + "=" * 60)
print("Все упражнения выполнены!")
print("=" * 60)
