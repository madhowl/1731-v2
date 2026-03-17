# Лекция 29: Работа с внешними API

## OAuth, авторизация, работа с популярными API (Google, Facebook и др.)

### Цель лекции:
- Познакомиться с концепцией OAuth
- Изучить процессы авторизации через внешние API
- Освоить интеграцию с популярными API

### План лекции:
1. Введение в OAuth
2. Типы OAuth
3. Процесс аутентификации
4. Интеграция с популярными API
5. Безопасность при работе с API

---

## 1. Введение в OAuth

OAuth (Open Authorization) — открытый стандарт авторизации, позволяющий предоставить третьей стороне ограниченный доступ к защищенным ресурсам пользователя без передачи учетных данных.

### Зачем нужен OAuth:
- Безопасная авторизация без передачи паролей
- Контроль доступа к ресурсам
- Единая точка входа для нескольких сервисов

### Основные участники OAuth:
- **Resource Owner** - пользователь, владелец ресурса
- **Client** - приложение, запрашивающее доступ
- **Resource Server** - сервер, хранящий защищенные ресурсы
- **Authorization Server** - сервер, выдающий токены доступа

### OAuth 1.0a vs OAuth 2.0:
- **OAuth 1.0a**: основан на подписях запросов, более сложный в реализации
- **OAuth 2.0**: основан на токенах доступа, более гибкий и простой

---

## 2. Типы OAuth

### OAuth 2.0 Flow Types:
1. **Authorization Code** - для веб-приложений с серверной частью
2. **Implicit** - для клиентских приложений (браузерных)
3. **Resource Owner Password Credentials** - для доверенных приложений
4. **Client Credentials** - для машинного взаимодействия

### Authorization Code Flow (наиболее безопасный):
```
1. Клиент перенаправляет пользователя на сервер авторизации
2. Пользователь вводит учетные данные и дает разрешение
3. Сервер возвращает authorization code
4. Клиент обменивает код на access token
5. Клиент использует токен для доступа к ресурсам
```

### Пример структуры токена:
```json
{
  "access_token": "ya29.AHES6ZRN3-Hbcdsdsdsd...",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "1/ff8sdssdsd..."
}
```

---

## 3. Процесс аутентификации

### Общая схема OAuth 2.0:
```python
import requests
from urllib.parse import urlencode

# Шаг 1: Перенаправление на страницу авторизации
authorization_url = "https://provider.com/oauth/authorize?"
params = {
    'client_id': 'your_client_id',
    'redirect_uri': 'your_redirect_uri',
    'response_type': 'code',
    'scope': 'read:user,user:email'
}
auth_url = authorization_url + urlencode(params)

# Шаг 2: После одобрения, пользователь возвращается с authorization code
# Этот код должен быть обменян на access token

# Шаг 3: Обмен кода на токен
token_url = "https://provider.com/oauth/token"
token_data = {
    'client_id': 'your_client_id',
    'client_secret': 'your_client_secret',
    'redirect_uri': 'your_redirect_uri',
    'grant_type': 'authorization_code',
    'code': 'received_code'
}
response = requests.post(token_url, data=token_data)
tokens = response.json()
```

### Использование access token:
```python
# Использование токена для доступа к API
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}
response = requests.get('https://api.provider.com/user', headers=headers)
user_data = response.json()
```

---

## 4. Интеграция с популярными API

### Google API:
```python
import requests
import json

# Получение данных пользователя Google
def get_google_user(access_token):
    url = 'https://www.googleapis.com/oauth2/v2/userinfo'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    return response.json()

# Получение списка событий Google Calendar
def get_google_calendar_events(access_token):
    url = 'https://www.googleapis.com/calendar/v3/calendars/primary/events'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.get(url, headers=headers)
    return response.json()
```

### Facebook API:
```python
# Получение информации о пользователе Facebook
def get_facebook_user(access_token):
    url = f'https://graph.facebook.com/me?access_token={access_token}&fields=id,name,email,picture'
    response = requests.get(url)
    return response.json()
```

### GitHub API:
```python
# Получение информации о пользователе GitHub
def get_github_user(access_token):
    url = 'https://api.github.com/user'
    headers = {
        'Authorization': f'token {access_token}'
    }
    response = requests.get(url, headers=headers)
    return response.json()
```

### Настройка OAuth с использованием библиотеки requests-oauthlib:
```python
from requests_oauthlib import OAuth2Session

# Инициализация OAuth2 сессии
client_id = 'your_client_id'
client_secret = 'your_client_secret'
redirect_uri = 'your_redirect_uri'
scope = ['read:user', 'user:email']

oauth = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)

# Получение URL для авторизации
authorization_url, state = oauth.authorization_url(
    'https://provider.com/oauth/authorize'
)

# После получения authorization code
token = oauth.fetch_token(
    'https://provider.com/oauth/token',
    client_secret=client_secret,
    authorization_response=authorization_response
)

# Использование сессии для запросов к API
r = oauth.get('https://api.provider.com/user')
user_data = r.json()
```

---

## 5. Безопасность при работе с API

### Лучшие практики:
- Хранение токенов в защищенном месте (не в localStorage для веб-приложений)
- Использование HTTPS для всех запросов
- Проверка истечения срока действия токенов
- Обработка refresh token для обновления доступа

### Пример обновления токена:
```python
def refresh_access_token(refresh_token, client_id, client_secret):
    url = 'https://provider.com/oauth/token'
    data = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': client_id,
        'client_secret': client_secret
    }
    response = requests.post(url, data=data)
    return response.json()
```

### Защита от CSRF:
- Использование параметра state при авторизации
- Проверка значения state после возврата от провайдера

### Хранение секретов:
- Использование переменных окружения
- Не хранить секреты в коде
- Использование специализированных решений (HashiCorp Vault, AWS Secrets Manager)