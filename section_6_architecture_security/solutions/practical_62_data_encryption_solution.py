#!/usr/bin/env python3
"""
Практическое занятие 62: Шифрование данных
Решение упражнений
"""

import base64
import hashlib
import os
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass


# ==============================================================================
# УПРАЖНЕНИЕ 1: Data Encryption with Fernet
# ==============================================================================

print("=" * 60)
print("Упражнение 1: Data Encryption with Fernet")
print("=" * 60)


class SimpleEncryption:
    """Простое шифрование данных (симуляция с использованием base64)"""
    
    @staticmethod
    def generate_key() -> bytes:
        """Генерация ключа шифрования"""
        return base64.urlsafe_b64encode(os.urandom(32))
    
    @staticmethod
    def encrypt(data: str, key: bytes) -> str:
        """Шифрование данных (симуляция)"""
        encrypted = base64.b64encode(data.encode())
        return encrypted.decode()
    
    @staticmethod
    def decrypt(encrypted_data: str, key: bytes) -> str:
        """Расшифровка данных (симуляция)"""
        decrypted = base64.b64decode(encrypted_data.encode())
        return decrypted.decode()


key = SimpleEncryption.generate_key()
print(f"Generated key: {key[:20]}...")

original = "Sensitive data: password123"
encrypted = SimpleEncryption.encrypt(original, key)
decrypted = SimpleEncryption.decrypt(encrypted, key)

print(f"Original: {original}")
print(f"Encrypted: {encrypted}")
print(f"Decrypted: {decrypted}")


# ==============================================================================
# УПРАЖНЕНИЕ 2: Hash Functions
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 2: Hash Functions")
print("=" * 60)


class SecureHasher:
    """Безопасное хэширование"""
    
    @staticmethod
    def hash_md5(data: str) -> str:
        """MD5 хэширование (небезопасно!)"""
        return hashlib.md5(data.encode()).hexdigest()
    
    @staticmethod
    def hash_sha256(data: str) -> str:
        """SHA-256 хэширование"""
        return hashlib.sha256(data.encode()).hexdigest()
    
    @staticmethod
    def hash_sha512(data: str) -> str:
        """SHA-512 хэширование"""
        return hashlib.sha512(data.encode()).hexdigest()
    
    @staticmethod
    def hash_password(password: str, salt: bytes = None) -> Tuple[str, bytes]:
        """Хэширование пароля с солью"""
        if salt is None:
            salt = os.urandom(32)
        
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode(),
            salt,
            100000
        )
        
        return base64.b64encode(key).decode(), base64.b64encode(salt).decode()
    
    @staticmethod
    def verify_password(password: str, hashed: str, salt: str) -> bool:
        """Проверка пароля"""
        salt_decoded = base64.b64decode(salt.encode())
        new_hash, _ = SecureHasher.hash_password(password, salt_decoded)
        return new_hash == hashed


hasher = SecureHasher()

password = "MySecurePassword123"
hashed_password, salt = hasher.hash_password(password)

print(f"Password: {password}")
print(f"Salt: {salt}")
print(f"Hashed: {hashed_password}")

is_valid = hasher.verify_password(password, hashed_password, salt)
print(f"Password valid: {is_valid}")

is_invalid = hasher.verify_password("wrong_password", hashed_password, salt)
print(f"Wrong password detected: {not is_invalid}")


# ==============================================================================
# УПРАЖНЕНИЕ 3: Symmetric Encryption
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 3: Symmetric Encryption")
print("=" * 60)


class SymmetricEncryption:
    """Симметричное шифрование (симуляция)"""
    
    def __init__(self, key: bytes = None):
        if key is None:
            key = os.urandom(32)
        self.key = key
    
    def generate_key(self) -> bytes:
        """Генерация ключа"""
        return os.urandom(32)
    
    def encrypt(self, plaintext: str) -> str:
        """Шифрование"""
        encrypted = base64.b64encode(plaintext.encode())
        return encrypted.decode()
    
    def decrypt(self, ciphertext: str) -> str:
        """Расшифровка"""
        decrypted = base64.b64decode(ciphertext.encode())
        return decrypted.decode()


sym_enc = SymmetricEncryption()

message = "Secret message for encryption"
encrypted = sym_enc.encrypt(message)
decrypted = sym_enc.decrypt(encrypted)

print(f"Original: {message}")
print(f"Encrypted: {encrypted}")
print(f"Decrypted: {decrypted}")


# ==============================================================================
# УПРАЖНЕНИЕ 4: Asymmetric Encryption
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 4: Asymmetric Encryption")
print("=" * 60)


class AsymmetricEncryption:
    """Асимметричное шифрование (симуляция)"""
    
    def __init__(self):
        self.public_key = "public_key_placeholder"
        self.private_key = "private_key_placeholder"
    
    def generate_keypair(self) -> Tuple[str, str]:
        """Генерация ключевой пары"""
        self.public_key = base64.b64encode(os.urandom(32)).decode()
        self.private_key = base64.b64encode(os.urandom(32)).decode()
        return self.public_key, self.private_key
    
    def encrypt(self, plaintext: str, public_key: str) -> str:
        """Шифрование с открытым ключом"""
        encrypted = base64.b64encode(plaintext.encode())
        return encrypted.decode()
    
    def decrypt(self, ciphertext: str, private_key: str) -> str:
        """Расшифровка с закрытым ключом"""
        decrypted = base64.b64decode(ciphertext.encode())
        return decrypted.decode()


asym_enc = AsymmetricEncryption()
pub_key, priv_key = asym_enc.generate_keypair()

message = "Top secret message"
encrypted = asym_enc.encrypt(message, pub_key)
decrypted = asym_enc.decrypt(encrypted, priv_key)

print(f"Original: {message}")
print(f"Public Key: {pub_key[:20]}...")
print(f"Private Key: {priv_key[:20]}...")
print(f"Encrypted: {encrypted}")
print(f"Decrypted: {decrypted}")


# ==============================================================================
# УПРАЖНЕНИЕ 5: File Encryption
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 5: File Encryption")
print("=" * 60)


class FileEncryption:
    """Шифрование файлов"""
    
    def __init__(self, key: bytes = None):
        if key is None:
            key = os.urandom(32)
        self.key = key
    
    def calculate_checksum(self, filepath: str) -> str:
        """Вычисление контрольной суммы файла"""
        sha256_hash = hashlib.sha256()
        
        try:
            with open(filepath, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()
        except FileNotFoundError:
            return "file_not_found"
    
    def verify_integrity(self, filepath: str, expected_checksum: str) -> bool:
        """Проверка целостности файла"""
        actual_checksum = self.calculate_checksum(filepath)
        return actual_checksum == expected_checksum


file_enc = FileEncryption()

print("File encryption class created")
print("Note: Use real cryptography libraries for production")


print("\n" + "=" * 60)
print("Все упражнения выполнены!")
print("=" * 60)
