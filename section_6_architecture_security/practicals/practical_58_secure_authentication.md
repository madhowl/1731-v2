# Практическое занятие 58: Безопасная аутентификация

## JWT, OAuth 2.0, сессии, двухфакторная аутентификация

### Цель занятия:
Изучить методы безопасной аутентификации, освоить JWT токены, OAuth 2.0, научиться реализовывать надёжную систему аутентификации.

### Задачи:
1. Понять основы аутентификации
2. Освоить JWT токены
3. Изучить OAuth 2.0
4. Реализовать двухфакторную аутентификацию

### План работы:
1. Основы аутентификации
2. JWT токены
3. OAuth 2.0
4. Сессии и cookies
5. Двухфакторная аутентификация
6. Практические задания

---

## 1. Основы аутентификации

Аутентификация - это процесс проверки подлинности пользователя.

### Методы аутентификации:

- **Один фактор** - только пароль
- **Два фактора** - пароль + что-то другое
- **Многофакторная** - несколько методов

---

## 2. JWT токены

### Пример 1: Работа с JWT

```python
import jwt
from datetime import datetime, timedelta
import os

class JWTManager:
    """Менеджер JWT токенов"""
    
    def __init__(self, secret_key: str = None, algorithm: str = 'HS256'):
        self.secret_key = secret_key or os.urandom(32).hex()
        self.algorithm = algorithm
    
    def create_access_token(self, data: dict, expires_delta: timedelta = None) -> str:
        """Создание access токена"""
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=1)
        
        to_encode.update({
            'exp': expire,
            'iat': datetime.utcnow(),
            'type': 'access'
        })
        
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def create_refresh_token(self, data: dict) -> str:
        """Создание refresh токена"""
        to_encode = data.copy()
        
        expire = datetime.utcnow() + timedelta(days=7)
        to_encode.update({
            'exp': expire,
            'iat': datetime.utcnow(),
            'type': 'refresh'
        })
        
        return jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
    
    def decode_token(self, token: str) -> dict:
        """Декодирование токена"""
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm]
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise ValueError("Token has expired")
        except jwt.InvalidTokenError as e:
            raise ValueError(f"Invalid token: {e}")
    
    def verify_token(self, token: str) -> bool:
        """Проверка токена"""
        try:
            self.decode_token(token)
            return True
        except ValueError:
            return False

# Использование
jwt_manager = JWTManager()

# Создание токенов
user_data = {'sub': 'user123', 'email': 'user@example.com'}

access_token = jwt_manager.create_access_token(user_data)
print(f"Access token: {access_token[:50]}...")

refresh_token = jwt_manager.create_refresh_token(user_data)
print(f"Refresh token: {refresh_token[:50]}...")

# Декодирование
payload = jwt_manager.decode_token(access_token)
print(f"Payload: {payload}")

# Проверка
is_valid = jwt_manager.verify_token(access_token)
print(f"Valid: {is_valid}")
```

### Пример 2: JWT в Flask

```python
from flask import Flask, request, jsonify
from functools import wraps
import jwt

app = Flask(__name__)
SECRET_KEY = "your-secret-key"

def token_required(f):
    """Декоратор для проверки токена"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Получение токена из заголовка
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            request.user = data
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(*args, **kwargs)
    
    return decorated

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Проверка credentials (упрощённо)
    if data.get('username') == 'admin' and data.get('password') == 'password':
        token = jwt.encode(
            {
                'sub': 'admin',
                'username': 'admin',
                'exp': datetime.utcnow() + timedelta(hours=1)
            },
            SECRET_KEY,
            algorithm='HS256'
        )
        return jsonify({'token': token})
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/protected', methods=['GET'])
@token_required
def protected():
    return jsonify({
        'message': 'Protected data',
        'user': request.user
    })

if __name__ == '__main__':
    app.run(debug=True)
```

---

## 3. OAuth 2.0

### Пример 3: OAuth 2.0 клиент

```python
import requests
from urllib.parse import urlencode
import secrets

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
        
        # Пример для GitHub
        base_url = 'https://github.com/login/oauth/authorize'
        return f"{base_url}?{urlencode(params)}"
    
    def exchange_code_for_token(self, code: str) -> dict:
        """Обмен кода на токен"""
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': code,
            'grant_type': 'authorization_code',
            'redirect_uri': self.redirect_uri
        }
        
        response = requests.post(
            'https://github.com/login/oauth/access_token',
            data=data,
            headers={'Accept': 'application/json'}
        )
        
        return response.json()
    
    def get_user_info(self, access_token: str) -> dict:
        """Получение информации о пользователе"""
        response = requests.get(
            'https://api.github.com/user',
            headers={
                'Authorization': f'token {access_token}',
                'Accept': 'application/json'
            }
        )
        
        return response.json()

# Использование
oauth_client = OAuthClient(
    client_id='your-client-id',
    client_secret='your-client-secret',
    redirect_uri='http://localhost:5000/callback'
)

# Получение URL авторизации
auth_url = oauth_client.get_authorization_url()
print(f"Authorization URL: {auth_url}")

# Обмен кода на токен (после redirect)
# token_data = oauth_client.exchange_code_for_token('code-from-callback')
# access_token = token_data['access_token']

# Получение информации о пользователе
# user_info = oauth_client.get_user_info(access_token)
```

---

## 4. Сессии и cookies

### Пример 4: Безопасные сессии

```python
from flask import Flask, session, request, jsonify
from flask.sessions import SecureCookieSessionInterface
import secrets

app = Flask(__name__)

# Безопасная конфигурация
app.secret_key = secrets.token_hex(32)
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
    PERMANENT_SESSION_LIFETIME=3600  # 1 час
)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Проверка credentials
    if data.get('username') == 'admin' and data.get('password') == 'password':
        session['user_id'] = 'user123'
        session['username'] = 'admin'
        session.permanent = True
        return jsonify({'message': 'Logged in'})
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({'message': 'Logged out'})

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    return jsonify({
        'user_id': session['user_id'],
        'username': session['username']
    })

# Защита от CSRF
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])

# Генерация CSRF токена
@app.before_request
def csrf_protect():
    if request.method == "POST":
        token = session.get('csrf_token')
        if not token or token != request.form.get('csrf_token'):
            return jsonify({'error': 'CSRF token missing'}), 403

@app.route('/setup-csrf')
def setup_csrf():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(32)
    return jsonify({'csrf_token': session['csrf_token']})
```

---

## 5. Двухфакторная аутентификация

### Пример 5: TOTP аутентификация

```python
import pyotp
import secrets

class TOTPAuthenticator:
    """TOTP аутентификатор"""
    
    @staticmethod
    def generate_secret() -> str:
        """Генерация секретного ключа"""
        return pyotp.random_base32()
    
    @staticmethod
    def get_provisioning_uri(secret: str, email: str, issuer: str = "MyApp") -> str:
        """Получение URI для настройки в приложении"""
        totp = pyotp.TOTP(secret)
        return totp.provisioning_uri(name=email, issuer_name=issuer)
    
    @staticmethod
    def verify(secret: str, token: str) -> bool:
        """Проверка TOTP токена"""
        totp = pyotp.TOTP(secret)
        return totp.verify(token)
    
    @staticmethod
    def get_current_token(secret: str) -> str:
        """Получение текущего токена"""
        totp = pyotp.TOTP(secret)
        return totp.now()

class TwoFactorAuth:
    """Двухфакторная аутентификация"""
    
    def __init__(self):
        self.users = {}  # В реальном приложении - база данных
    
    def enable_2fa(self, user_id: str) -> dict:
        """Включение 2FA для пользователя"""
        secret = TOTPAuthenticator.generate_secret()
        self.users[user_id] = {
            'secret': secret,
            'enabled': True
        }
        
        return {
            'secret': secret,
            'qr_uri': TOTPAuthenticator.get_provisioning_uri(
                secret,
                f"{user_id}@example.com",
                "MyApp"
            )
        }
    
    def verify_2fa(self, user_id: str, token: str) -> bool:
        """Проверка 2FA кода"""
        if user_id not in self.users:
            return False
        
        secret = self.users[user_id]['secret']
        return TOTPAuthenticator.verify(secret, token)
    
    def disable_2fa(self, user_id: str) -> bool:
        """Отключение 2FA"""
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False

# Использование
auth_2fa = TwoFactorAuth()

# Включение 2FA
result = auth_2fa.enable_2fa("user123")
print(f"Secret: {result['secret']}")
print(f"QR URI: {result['qr_uri']}")

# Получение текущего токена для тестирования
current_token = TOTPAuthenticator.get_current_token(result['secret'])
print(f"Current token: {current_token}")

# Проверка
is_valid = auth_2fa.verify_2fa("user123", current_token)
print(f"Valid: {is_valid}")
```

---

## 6. Практические задания

### Задание 1: JWT система

Создайте систему аутентификации на основе JWT:
- Генерация access и refresh токенов
- Проверка токенов
- Refresh токенов

### Задание 2: OAuth 2.0

Реализуйте OAuth 2.0 провайдер:
- Авторизация
- Обмен кода на токен
- Получение данных пользователя

### Задание 3: Сессии

Создайте безопасную систему сессий:
- Защищённые cookies
- CSRF защита
- Безопасное хранение сессий

### Задание 4: Двухфакторная аутентификация

Реализуйте 2FA:
- Генерация TOTP ключей
- QR код для настройки
- Проверка кодов

### Задание 5: Комплексная система аутентификации

Создайте полную систему аутентификации:
- Регистрация и вход
- JWT токены
- 2FA опционально
- Защита от brute force

---

## Контрольные вопросы:

1. Что такое JWT и какие преимущества он даёт?
2. Как работает OAuth 2.0?
3. Зачем нужна двухфакторная аутентификация?
4. Какие меры безопасности для сессий вы знаете?
5. Что такое CSRF и как от него защититься?
