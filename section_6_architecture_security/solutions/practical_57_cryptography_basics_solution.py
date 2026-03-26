#!/usr/bin/env python3
"""
Практическое занятие 57: Основы криптографии
Решение упражнений
"""

import os
import base64
import hashlib
from typing import Optional, Dict, Any


# ==============================================================================
# УПРАЖНЕНИЕ 1: Симметричное шифрование (AES)
# ==============================================================================

print("=" * 60)
print("Упражнение 1: Симметричное шифрование (AES)")
print("=" * 60)


try:
    from cryptography.fernet import Fernet
    
    class AESCipher:
        """AES шифрование"""
        
        def __init__(self, key: bytes = None):
            self.key = key or Fernet.generate_key()
            self.cipher = Fernet(self.key)
        
        def encrypt(self, plaintext: str) -> str:
            return self.cipher.encrypt(plaintext.encode()).decode()
        
        def decrypt(self, encrypted: str) -> str:
            return self.cipher.decrypt(encrypted.encode()).decode()
    
    cipher = AESCipher()
    
    encrypted = cipher.encrypt("Secret message")
    print(f"Encrypted: {encrypted}")
    
    decrypted = cipher.decrypt(encrypted)
    print(f"Decrypted: {decrypted}")
    
except ImportError:
    print("cryptography library not installed - using mock implementation")
    
    class MockCipher:
        def __init__(self, key: bytes = None):
            self.key = key or os.urandom(32)
        
        def encrypt(self, plaintext: str) -> str:
            return base64.b64encode(plaintext.encode()).decode() + "_mock"
        
        def decrypt(self, encrypted: str) -> str:
            return base64.b64decode(encrypted.replace("_mock", "")).decode()
    
    cipher = MockCipher()
    encrypted = cipher.encrypt("Secret message")
    print(f"Encrypted (mock): {encrypted}")
    decrypted = cipher.decrypt(encrypted)
    print(f"Decrypted: {decrypted}")


# ==============================================================================
# УПРАЖНЕНИЕ 2: Хеширование паролей
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 2: Хеширование паролей")
print("=" * 60)


class PasswordHasher:
    """Безопасное хеширование паролей"""
    
    @staticmethod
    def hash_password(password: str, salt: bytes = None) -> str:
        salt = salt or os.urandom(16)
        key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        result = salt + key
        return base64.b64encode(result).decode()
    
    @staticmethod
    def verify_password(password: str, hashed: str) -> bool:
        try:
            data = base64.b64decode(hashed)
            salt = data[:16]
            stored_hash = data[16:]
            
            key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
            return key == stored_hash
        except Exception:
            return False


hasher = PasswordHasher()

password = "MySecurePassword123!"
hashed = hasher.hash_password(password)
print(f"Hashed password: {hashed}")

print(f"Correct password: {hasher.verify_password(password, hashed)}")
print(f"Wrong password: {hasher.verify_password('wrong', hashed)}")


# ==============================================================================
# УПРАЖНЕНИЕ 3: Хеширование файлов
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 3: Хеширование файлов")
print("=" * 60)


def hash_data(data: str, algorithm: str = 'sha256') -> str:
    """Вычисление хеша данных"""
    hash_func = hashlib.new(algorithm)
    hash_func.update(data.encode())
    return hash_func.hexdigest()


text = "Hello, World!"

print(f"MD5: {hashlib.md5(text.encode()).hexdigest()}")
print(f"SHA1: {hashlib.sha1(text.encode()).hexdigest()}")
print(f"SHA256: {hashlib.sha256(text.encode()).hexdigest()}")
print(f"SHA512: {hashlib.sha512(text.encode()).hexdigest()}")


# ==============================================================================
# УПРАЖНЕНИЕ 4: Асимметричное шифрование (RSA)
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 4: Асимметричное шифрование (RSA)")
print("=" * 60)


try:
    from cryptography.hazmat.primitives.asymmetric import rsa, padding
    from cryptography.hazmat.primitives import hashes
    
    class RSACipher:
        def __init__(self):
            self.private_key = None
            self.public_key = None
        
        def generate_keys(self, key_size: int = 2048):
            self.private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=key_size
            )
            self.public_key = self.private_key.public_key()
        
        def encrypt(self, data: bytes) -> bytes:
            return self.public_key.encrypt(
                data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
        
        def decrypt(self, encrypted_data: bytes) -> bytes:
            return self.private_key.decrypt(
                encrypted_data,
                padding.OAEP(
                    mgf=padding.MGF1(algorithm=hashes.SHA256()),
                    algorithm=hashes.SHA256(),
                    label=None
                )
            )
    
    rsa_cipher = RSACipher()
    rsa_cipher.generate_keys()
    
    message = b"Secret message for RSA encryption"
    encrypted = rsa_cipher.encrypt(message)
    print(f"Encrypted (base64): {base64.b64encode(encrypted).decode()[:50]}...")
    
    decrypted = rsa_cipher.decrypt(encrypted)
    print(f"Decrypted: {decrypted.decode()}")

except ImportError:
    print("cryptography library not installed")


# ==============================================================================
# УПРАЖНЕНИЕ 5: Цифровые подписи
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 5: Цифровые подписи")
print("=" * 60)


try:
    from cryptography.hazmat.primitives.asymmetric import rsa, padding
    from cryptography.hazmat.primitives import hashes
    
    class DigitalSignature:
        def __init__(self):
            self.private_key = None
            self.public_key = None
        
        def generate_keys(self):
            self.private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048
            )
            self.public_key = self.private_key.public_key()
        
        def sign(self, data: str) -> bytes:
            return self.private_key.sign(
                data.encode(),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
        
        def verify(self, data: str, signature: bytes) -> bool:
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
    
    sig = DigitalSignature()
    sig.generate_keys()
    
    message = "Important document"
    signature = sig.sign(message)
    print(f"Signature: {base64.b64encode(signature).decode()[:50]}...")
    
    is_valid = sig.verify(message, signature)
    print(f"Valid: {is_valid}")
    
    is_valid_tampered = sig.verify(message + "modified", signature)
    print(f"Valid after modification: {is_valid_tampered}")

except ImportError:
    print("cryptography library not installed")


print("\n" + "=" * 60)
print("Все упражнения выполнены!")
print("=" * 60)
