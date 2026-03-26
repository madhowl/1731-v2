# Практическое занятие 62: Шифрование данных

## Шифрование данных в покое, прозрачное шифрование, управление ключами

### Цель занятия:
Изучить методы шифрования данных, освоить прозрачное шифрование, научиться управлять ключами.

### Задачи:
1. Понять основы шифрования данных
2. Освоить прозрачное шифрование
3. Научиться управлять ключами
4. Реализовать защиту данных

### План работы:
1. Шифрование в покое
2. Прозрачное шифрование
3. Управление ключами
4. Практические задания

---

## 1. Шифрование в покое

### Пример 1: Шифрование файлов

```python
from cryptography.fernet import Fernet
import os
import base64
import hashlib

class DataEncryption:
    """Шифрование данных"""
    
    def __init__(self, key: bytes = None):
        self.key = key or Fernet.generate_key()
        self.cipher = Fernet(self.key)
    
    def encrypt_data(self, data: bytes) -> bytes:
        """Шифрование данных"""
        return self.cipher.encrypt(data)
    
    def decrypt_data(self, encrypted_data: bytes) -> bytes:
        """Расшифровка данных"""
        return self.cipher.decrypt(encrypted_data)
    
    def encrypt_file(self, input_path: str, output_path: str = None):
        """Шифрование файла"""
        output_path = output_path or f"{input_path}.encrypted"
        
        with open(input_path, 'rb') as f:
            data = f.read()
        
        encrypted = self.encrypt_data(data)
        
        with open(output_path, 'wb') as f:
            f.write(encrypted)
    
    def decrypt_file(self, input_path: str, output_path: str = None):
        """Расшифровка файла"""
        output_path = output_path or input_path.replace('.encrypted', '.decrypted')
        
        with open(input_path, 'rb') as f:
            encrypted = f.read()
        
        decrypted = self.decrypt_data(encrypted)
        
        with open(output_path, 'wb') as f:
            f.write(decrypted)
    
    @staticmethod
    def derive_key(password: str, salt: bytes = None) -> bytes:
        """Создание ключа из пароля"""
        salt = salt or os.urandom(16)
        key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        return base64.urlsafe_b64encode(key)

# Использование
enc = DataEncryption()

# Шифрование данных
data = b"Secret data"
encrypted = enc.encrypt_data(data)
decrypted = enc.decrypt_data(encrypted)

print(f"Original: {data}")
print(f"Encrypted: {encrypted}")
print(f"Decrypted: {decrypted}")
```

---

## 2. Шифрование данных в БД

### Пример 2: Шифрование полей БД

```python
from cryptography.fernet import Fernet
from dataclasses import dataclass

class EncryptedField:
    """Декоратор для шифрования полей"""
    
    def __init__(self, cipher: Fernet):
        self.cipher = cipher
    
    def __get__(self, obj, objtype=None):
        value = getattr(obj, '_encrypted_value', None)
        if value:
            return self.cipher.decrypt(value).decode()
        return None
    
    def __set__(self, obj, value):
        if value:
            encrypted = self.cipher.encrypt(value.encode() if isinstance(value, str) else value)
            setattr(obj, '_encrypted_value', encrypted)
        else:
            setattr(obj, '_encrypted_value', None)

class SecureUser:
    """Пользователь с шифрованными данными"""
    
    def __init__(self, cipher: Fernet):
        self.cipher = cipher
        self._email = None
    
    email = EncryptedField(Fernet.generate_key())
    
    def __init__(self, email: str = None):
        self.email = email

# Использование
cipher = Fernet(Fernet.generate_key())
user = SecureUser(cipher)
user.email = "user@example.com"

print(f"Email: {user.email}")
```

---

## 3. Практические задания

### Задание 1: Шифрование файлов

Создайте систему шифрования файлов с управлением ключами.

### Задание 2: Шифрование БД

Реализуйте шифрование полей в базе данных.

### Задание 3: KMS

Создайте простую систему управления ключами.

### Задание 4: Прозрачное шифрование

Реализуйте прозрачное шифрование для API.

---

## Контрольные вопросы:

1. Что такое шифрование в покое?
2. Как управлять ключами шифрования?
3. Что такое прозрачное шифрование?
