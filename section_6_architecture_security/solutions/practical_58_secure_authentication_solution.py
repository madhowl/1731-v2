#!/usr/bin/env python3
"""
Практическое занятие 58: Безопасная аутентификация
Решение упражнений
"""

import os
import secrets
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from dataclasses import dataclass


# ==============================================================================
# УПРАЖНЕНИЕ 1: JWT токены
# ==============================================================================

print("=" * 60)
print("Упражнение 1: JWT токены")
print("=" * 60)


class JWTManager:
    """Менеджер JWT токенов (упрощённая реализация)"""
    
    def __init__(self, secret_key: str = None, algorithm: str = 'HS256'):
        self.secret_key = secret_key or secrets.token_hex(32)
        self.algorithm = algorithm
    
    def create_access_token(self, data: dict, expires_delta: timedelta = None) -> str:
        """Создание access токена"""
        import base64
        import json
        
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=1)
        
        to_encode.update({
            'exp': expire.timestamp(),
            'iat': datetime.utcnow().timestamp(),
            'type': 'access'
        })
        
        header = base64.urlsafe_b64encode(json.dumps({'alg': self.algorithm}).encode()).decode().rstrip('=')
        payload = base64.urlsafe_b64encode(json.dumps(to_encode).encode()).decode().rstrip('=')
        
        import hmac
        signature = base64.urlsafe_b64encode(
            hmac.new(self.secret_key.encode(), f"{header}.{payload}".encode(), 'sha256').digest()
        ).decode().rstrip('=')
        
        return f"{header}.{payload}.{signature}"
    
    def create_refresh_token(self, data: dict) -> str:
        """Создание refresh токена"""
        import base64
        import json
        import hmac
        
        to_encode = data.copy()
        
        expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({
            'exp': expire.timestamp(),
            'iat': datetime.utcnow().timestamp(),
            'type': 'refresh'
        })
        
        header = base64.urlsafe_b64encode(json.dumps({'alg': self.algorithm}).encode()).decode().rstrip('=')
        payload = base64.urlsafe_b64encode(json.dumps(to_encode).encode()).decode().rstrip('=')
        
        signature = base64.urlsafe_b64encode(
            hmac.new(self.secret_key.encode(), f"{header}.{payload}".encode(), 'sha256').digest()
        ).decode().rstrip('=')
        
        return f"{header}.{payload}.{signature}"
    
    def decode_token(self, token: str) -> dict:
        """Декодирование токена"""
        import base64
        import json
        import hmac
        
        parts = token.split('.')
        if len(parts) != 3:
            raise ValueError("Invalid token format")
        
        header, payload, signature = parts
        
        expected_signature = base64.urlsafe_b64encode(
            hmac.new(self.secret_key.encode(), f"{header}.{payload}".encode(), 'sha256').digest()
        ).decode().rstrip('=')
        
        if signature != expected_signature:
            raise ValueError("Invalid signature")
        
        payload_data = json.loads(base64.urlsafe_b64decode(payload + '=='))
        
        exp = payload_data.get('exp')
        if exp and datetime.utcnow().timestamp() > exp:
            raise ValueError("Token has expired")
        
        return payload_data
    
    def verify_token(self, token: str) -> bool:
        """Проверка токена"""
        try:
            self.decode_token(token)
            return True
        except ValueError:
            return False


jwt_manager = JWTManager()

user_data = {'sub': 'user123', 'email': 'user@example.com'}

access_token = jwt_manager.create_access_token(user_data)
print(f"Access token: {access_token[:50]}...")

refresh_token = jwt_manager.create_refresh_token(user_data)
print(f"Refresh token: {refresh_token[:50]}...")

payload = jwt_manager.decode_token(access_token)
print(f"Payload: {payload}")

is_valid = jwt_manager.verify_token(access_token)
print(f"Valid: {is_valid}")


# ==============================================================================
# УПРАЖНЕНИЕ 2: OAuth 2.0 клиент
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 2: OAuth 2.0 клиент")
print("=" * 60)


class OAuthClient:
    """OAuth 2.0 клиент"""
    
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.state = None
    
    def get_authorization_url(self, scope: str = "read:user") -> str:
        """Получение URL для авторизации"""
        self.state = secrets.token_urlsafe(32)
        
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': scope,
            'state': self.state
        }
        
        from urllib.parse import urlencode
        base_url = 'https://github.com/login/oauth/authorize'
        return f"{base_url}?{urlencode(params)}"
    
    def validate_state(self, state: str) -> bool:
        """Проверка state для защиты от CSRF"""
        return state == self.state and state is not None


oauth_client = OAuthClient(
    client_id='your-client-id',
    client_secret='your-client-secret',
    redirect_uri='http://localhost:5000/callback'
)

auth_url = oauth_client.get_authorization_url()
print(f"Authorization URL: {auth_url}")
print(f"State: {oauth_client.state}")


# ==============================================================================
# УПРАЖНЕНИЕ 3: Безопасные сессии
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 3: Безопасные сессии")
print("=" * 60)


class SessionManager:
    """Менеджер сессий"""
    
    def __init__(self, secret_key: str = None):
        self.secret_key = secret_key or secrets.token_hex(32)
        self.sessions: Dict[str, Dict[str, Any]] = {}
    
    def create_session(self, user_id: str, data: Dict = None) -> str:
        """Создание сессии"""
        session_id = secrets.token_urlsafe(32)
        
        self.sessions[session_id] = {
            'user_id': user_id,
            'data': data or {},
            'created_at': datetime.utcnow().timestamp(),
            'expires_at': (datetime.utcnow() + timedelta(hours=1)).timestamp()
        }
        
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Получение сессии"""
        session = self.sessions.get(session_id)
        
        if not session:
            return None
        
        if datetime.utcnow().timestamp() > session['expires_at']:
            del self.sessions[session_id]
            return None
        
        return session
    
    def delete_session(self, session_id: str):
        """Удаление сессии"""
        if session_id in self.sessions:
            del self.sessions[session_id]
    
    def generate_csrf_token(self) -> str:
        """Генерация CSRF токена"""
        return secrets.token_hex(32)


session_manager = SessionManager()

session_id = session_manager.create_session('user123', {'username': 'john'})
print(f"Session created: {session_id}")

session = session_manager.get_session(session_id)
print(f"Session data: {session}")

csrf_token = session_manager.generate_csrf_token()
print(f"CSRF token: {csrf_token}")


# ==============================================================================
# УПРАЖНЕНИЕ 4: Двухфакторная аутентификация (TOTP)
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 4: Двухфакторная аутентификация")
print("=" * 60)


class TOTPAuthenticator:
    """TOTP аутентификатор (упрощённая реализация)"""
    
    @staticmethod
    def generate_secret() -> str:
        """Генерация секретного ключа"""
        return secrets.token_base64(16).replace('=', '')
    
    @staticmethod
    def get_current_token(secret: str) -> str:
        """Получение текущего токена (симуляция)"""
        import hashlib
        import time
        
        counter = int(time.time() // 30)
        hmac_hash = hashlib.hmac.new(
            secret.encode(),
            str(counter).encode(),
            'sha1'
        ).digest()
        
        offset = hmac_hash[-1] & 0x0f
        code = (hmac_hash[offset:offset + 4])[0] & 0x7f
        for i in range(1, 4):
            code = (code << 8) | ((hmac_hash[offset + i])[0] & 0xff)
        
        return str(code % 1000000).zfill(6)
    
    @staticmethod
    def verify(secret: str, token: str) -> bool:
        """Проверка TOTP токена"""
        current_token = TOTPAuthenticator.get_current_token(secret)
        
        for offset in [-1, 0, 1]:
            import hashlib
            import time
            
            counter = int(time.time() // 30) + offset
            hmac_hash = hashlib.hmac.new(
                secret.encode(),
                str(counter).encode(),
                'sha1'
            ).digest()
            
            offset_byte = hmac_hash[-1] & 0x0f
            code = (hmac_hash[offset_byte:offset_byte + 4])[0] & 0x7f
            for i in range(1, 4):
                code = (code << 8) | ((hmac_hash[offset_byte + i])[0] & 0xff)
            
            check_token = str(code % 1000000).zfill(6)
            if check_token == token:
                return True
        
        return False


secret = TOTPAuthenticator.generate_secret()
print(f"Generated secret: {secret}")

current_token = TOTPAuthenticator.get_current_token(secret)
print(f"Current token: {current_token}")

is_valid = TOTPAuthenticator.verify(secret, current_token)
print(f"Token valid: {is_valid}")

is_valid_wrong = TOTPAuthenticator.verify(secret, "000000")
print(f"Wrong token valid: {is_valid_wrong}")


print("\n" + "=" * 60)
print("Все упражнения выполнены!")
print("=" * 60)
