# Практическое занятие 57: Основы криптографии

## Симметричное и асимметричное шифрование, хеширование, цифровые подписи

### Цель занятия:
Изучить основы криптографии, освоить алгоритмы шифрования и хеширования, научиться применять криптографические методы на практике.

### Задачи:
1. Понять основные криптографические концепции
2. Освоить симметричное и асимметричное шифрование
3. Научиться использовать хеширование
4. Создать систему цифровых подписей

### План работы:
1. Введение в криптографию
2. Симметричное шифрование
3. Асимметричное шифрование
4. Хеширование
5. Цифровые подписи
6. Практические задания

---

## 1. Введение в криптографию

Криптография - это наука о защите информации с помощью математических методов.

### Основные понятия:

- **Шифрование** - преобразование данных в непонятный вид
- **Расшифровка** - обратное преобразование
- **Ключ** - параметр для шифрования/расшифровки
- **Хеширование** - преобразование данных в фиксированный размер
- **Цифровая подпись** - аутентификация источника данных

---

## 2. Симметричное шифрование

### Пример 1: AES шифрование

```python
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
import os
import base64

class AESCipher:
    """AES шифрование"""
    
    def __init__(self, key: bytes):
        # Ключ должен быть 16, 24 или 32 байта
        if len(key) not in [16, 24, 32]:
            raise ValueError("Key must be 16, 24, or 32 bytes")
        self.key = key
    
    def encrypt(self, plaintext: str) -> str:
        """Шифрование строки"""
        # Генерация случайного IV
        iv = os.urandom(16)
        
        # Создание шифра
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv),
            backend=default_backend()
        )
        encryptor = cipher.encryptor()
        
        # Добавление padding
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(plaintext.encode()) + padder.finalize()
        
        # Шифрование
        ciphertext = encryptor.update(padded_data) + encryptor.finalize()
        
        # Объединение IV и ciphertext
        result = iv + ciphertext
        return base64.b64encode(result).decode()
    
    def decrypt(self, encrypted: str) -> str:
        """Расшифровка строки"""
        # Декодирование из base64
        data = base64.b64decode(encrypted)
        
        # Извлечение IV
        iv = data[:16]
        ciphertext = data[16:]
        
        # Создание шифра
        cipher = Cipher(
            algorithms.AES(self.key),
            modes.CBC(iv),
            backend=default_backend()
        )
        decryptor = cipher.decryptor()
        
        # Расшифровка
        padded_data = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Удаление padding
        unpadder = padding.PKCS7(128).unpadder()
        data = unpadder.update(padded_data) + unpadder.finalize()
        
        return data.decode()

# Использование
key = os.urandom(32)  # 256-битный ключ
cipher = AESCipher(key)

encrypted = cipher.encrypt("Secret message")
print(f"Encrypted: {encrypted}")

decrypted = cipher.decrypt(encrypted)
print(f"Decrypted: {decrypted}")
```

### Пример 2: Fernet (symmetric encryption)

```python
from cryptography.fernet import Fernet

# Генерация ключа
key = Fernet.generate_key()
print(f"Key: {key}")

# Создание шифра
cipher = Fernet(key)

# Шифрование
message = b"Hello, World!"
encrypted = cipher.encrypt(message)
print(f"Encrypted: {encrypted}")

# Расшифровка
decrypted = cipher.decrypt(encrypted)
print(f"Decrypted: {decrypted}")

# Шифрование строки
text = "Привет, мир!"
encrypted_text = cipher.encrypt(text.encode())
decrypted_text = cipher.decrypt(encrypted_text).decode()
print(f"Original: {text}, Decrypted: {decrypted_text}")
```

---

## 3. Асимметричное шифрование

### Пример 3: RSA шифрование

```python
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import base64

class RSACipher:
    """RSA шифрование"""
    
    def __init__(self):
        self.private_key = None
        self.public_key = None
    
    def generate_keys(self, key_size: int = 2048):
        """Генерация ключей"""
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_size,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()
    
    def load_private_key(self, private_pem: bytes):
        """Загрузка приватного ключа"""
        from cryptography.hazmat.primitives.serialization import load_pem_private_key
        self.private_key = load_pem_private_key(
            private_pem,
            password=None,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()
    
    def load_public_key(self, public_pem: bytes):
        """Загрузка публичного ключа"""
        from cryptography.hazmat.primitives.serialization import load_pem_public_key
        self.public_key = load_pem_public_key(
            public_pem,
            backend=default_backend()
        )
    
    def get_public_key_pem(self) -> bytes:
        """Получение публичного ключа в PEM формате"""
        from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
        return self.public_key.public_bytes(
            encoding=Encoding.PEM,
            format=PublicFormat.SubjectPublicKeyInfo
        )
    
    def get_private_key_pem(self) -> bytes:
        """Получение приватного ключа в PEM формате"""
        from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, NoEncryption
        return self.private_key.private_bytes(
            encoding=Encoding.PEM,
            format=PrivateFormat.PKCS8,
            encryption_algorithm=NoEncryption()
        )
    
    def encrypt(self, data: bytes) -> bytes:
        """Шифрование данных публичным ключом"""
        ciphertext = self.public_key.encrypt(
            data,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return base64.b64encode(ciphertext)
    
    def decrypt(self, encrypted_data: bytes) -> bytes:
        """Расшифровка данных приватным ключом"""
        ciphertext = base64.b64decode(encrypted_data)
        return self.private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

# Использование
rsa_cipher = RSACipher()
rsa_cipher.generate_keys()

# Публичный ключ для шифрования
public_key_pem = rsa_cipher.get_public_key_pem()
print(f"Public key: {public_key_pem[:50]}...")

# Шифрование
message = b"Secret message for RSA encryption"
encrypted = rsa_cipher.encrypt(message)
print(f"Encrypted: {encrypted[:50]}...")

# Расшифровка
decrypted = rsa_cipher.decrypt(encrypted)
print(f"Decrypted: {decrypted}")
```

---

## 4. Хеширование

### Пример 4: Хеширование паролей

```python
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import base64
import os

class PasswordHasher:
    """Безопасное хеширование паролей"""
    
    def __init__(self, iterations: int = 100000):
        self.iterations = iterations
        self.algorithm = hashes.SHA256()
    
    def hash_password(self, password: str) -> str:
        """Хеширование пароля"""
        # Генерация соли
        salt = os.urandom(16)
        
        # Создание KDF
        kdf = PBKDF2HMAC(
            algorithm=self.algorithm,
            length=32,
            salt=salt,
            iterations=self.iterations,
            backend=default_backend()
        )
        
        # Хеширование
        key = kdf.derive(password.encode())
        
        # Объединение соли и хеша
        result = salt + key
        return base64.b64encode(result).decode()
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Проверка пароля"""
        try:
            # Декодирование
            data = base64.b64decode(hashed)
            
            # Извлечение соли и хеша
            salt = data[:16]
            stored_hash = data[16:]
            
            # Создание KDF с той же солью
            kdf = PBKDF2HMAC(
                algorithm=self.algorithm,
                length=32,
                salt=salt,
                iterations=self.iterations,
                backend=default_backend()
            )
            
            # Хеширование введённого пароля
            key = kdf.derive(password.encode())
            
            # Сравнение
            return key == stored_hash
        
        except Exception:
            return False

# Использование
hasher = PasswordHasher()

# Хеширование пароля
password = "MySecurePassword123!"
hashed = hasher.hash_password(password)
print(f"Hashed password: {hashed}")

# Проверка пароля
print(f"Correct password: {hasher.verify_password(password, hashed)}")
print(f"Wrong password: {hasher.verify_password('wrong', hashed)}")
```

### Пример 5: Хеширование файлов

```python
import hashlib

def hash_file(filepath: str, algorithm: str = 'sha256') -> str:
    """Вычисление хеша файла"""
    hash_func = hashlib.new(algorithm)
    
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hash_func.update(chunk)
    
    return hash_func.hexdigest()

def hash_data(data: str, algorithm: str = 'sha256') -> str:
    """Вычисление хеша данных"""
    hash_func = hashlib.new(algorithm)
    hash_func.update(data.encode())
    return hash_func.hexdigest()

# Примеры использования
text = "Hello, World!"

# Разные алгоритмы
print(f"MD5: {hashlib.md5(text.encode()).hexdigest()}")
print(f"SHA1: {hashlib.sha1(text.encode()).hexdigest()}")
print(f"SHA256: {hashlib.sha256(text.encode()).hexdigest()}")
print(f"SHA512: {hashlib.sha512(text.encode()).hexdigest()}")

# Проверка целостности файла
original_hash = "dffd6021bb2bd5b0af9292906b6083ff94f716c4de7d6427a1cb96f7a2baf2c"
# if hash_file("document.pdf") == original_hash:
#     print("File is intact")
```

---

## 5. Цифровые подписи

### Пример 6: Создание и проверка подписи

```python
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import base64

class DigitalSignature:
    """Цифровая подпись"""
    
    def __init__(self):
        self.private_key = None
        self.public_key = None
    
    def generate_keys(self):
        """Генерация ключей для подписи"""
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()
    
    def sign(self, data: str) -> bytes:
        """Создание подписи"""
        return self.private_key.sign(
            data.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
    
    def verify(self, data: str, signature: bytes) -> bool:
        """Проверка подписи"""
        try:
            self.public_key.verify(
                signature,
                data.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False
    
    def sign_detached(self, data: bytes) -> bytes:
        """Создание отдельной подписи"""
        return self.private_key.sign(
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
    
    def verify_detached(self, data: bytes, signature: bytes) -> bool:
        """Проверка отдельной подписи"""
        try:
            self.public_key.verify(
                signature,
                data,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False

# Использование
sig = DigitalSignature()
sig.generate_keys()

# Создание подписи
message = "Important document"
signature = sig.sign(message)
print(f"Signature: {base64.b64encode(signature).decode()}")

# Проверка подписи
is_valid = sig.verify(message, signature)
print(f"Valid: {is_valid}")

# Проверка с изменённым сообщением
is_valid_tampered = sig.verify(message + "modified", signature)
print(f"Valid after modification: {is_valid_tampered}")
```

---

## 6. Практические задания

### Задание 1: Шифрование данных

Создайте систему для шифрования конфиденциальных данных:
- AES шифрование для данных
- Безопасное хранение ключей
- Шифрование/расшифровка файлов

### Задание 2: Хеширование паролей

Реализуйте систему хеширования паролей:
- PBKDF2 для безопасного хеширования
- Проверка пароля
- Защита от rainbow table атак

### Задание 3: Асимметричное шифрование

Создайте систему для безопасной передачи данных:
- Генерация RSA ключей
- Шифрование публичным ключом
- Расшифровка приватным ключом

### Задание 4: Цифровые подписи

Реализуйте систему цифровых подписей:
- Создание подписи документа
- Проверка подписи
- Защита от подделки

### Задание 5: Комплексная система безопасности

Создайте комплексную систему:
- Шифрование данных пользователя
- Безопасное хеширование паролей
- Цифровые подписи для важных документов

---

## Контрольные вопросы:

1. В чём разница между симметричным и асимметричным шифрованием?
2. Что такое PBKDF2 и зачем он используется?
3. Как работает цифровая подпись?
4. Зачем нужна соль при хешировании паролей?
5. Какие атаки на криптографические системы вы знаете?

---

## Дополнительные материалы:

- Cryptography Documentation: https://cryptography.io/
- OWASP Cryptographic Storage Cheat Sheet
