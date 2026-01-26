# Практическое занятие 43: Работа с API

## Интеграция с внешними API

### Цель занятия:
Научиться работать с внешними API, использовать библиотеку requests для выполнения HTTP-запросов, обрабатывать ответы от API, реализовать аутентификацию.

### Задачи:
1. Выполнять GET, POST, PUT, DELETE запросы к API
2. Обрабатывать JSON-ответы
3. Реализовать аутентификацию с токенами
4. Обрабатывать ошибки API

### План работы:
1. Основы работы с API
2. Библиотека requests
3. Аутентификация
4. Обработка ошибок
5. Практические задания

---

## 1. Основы работы с API

API (Application Programming Interface) — интерфейс программирования приложений, позволяющий различным программам взаимодействовать друг с другом.

### Пример 1: Простой GET-запрос

```python
import requests

# Простой GET-запрос
response = requests.get('https://jsonplaceholder.typicode.com/posts/1')

# Проверка статуса ответа
if response.status_code == 200:
    data = response.json()  # Преобразование JSON в Python-объект
    print(f"Заголовок: {data['title']}")
    print(f"Содержание: {data['body']}")
else:
    print(f"Ошибка запроса: {response.status_code}")
```

### Пример 2: Основные HTTP-методы

```python
import requests

# GET запрос - получение данных
response = requests.get('https://api.example.com/users')

# POST запрос - создание данных
new_user = {
    'name': 'Иван Иванов',
    'email': 'ivan@example.com'
}
response = requests.post('https://api.example.com/users', json=new_user)

# PUT запрос - обновление данных
updated_user = {
    'name': 'Иван Петров',
    'email': 'ivan.petrov@example.com'
}
response = requests.put('https://api.example.com/users/1', json=updated_user)

# DELETE запрос - удаление данных
response = requests.delete('https://api.example.com/users/1')
```

### Пример 3: Параметры запроса

```python
import requests

# Параметры в URL
params = {
    'page': 1,
    'limit': 10,
    'sort': 'date'
}
response = requests.get('https://api.example.com/posts', params=params)

# Тело запроса (для POST/PUT)
data = {
    'title': 'Новый пост',
    'content': 'Содержание поста'
}
response = requests.post('https://api.example.com/posts', data=data)

# JSON в теле запроса
json_data = {
    'title': 'Новый пост',
    'content': 'Содержание поста'
}
response = requests.post('https://api.example.com/posts', json=json_data)
```

---

## 2. Библиотека requests

### Пример 4: Заголовки и параметры

```python
import requests

# Установка заголовков
headers = {
    'Content-Type': 'application/json',
    'User-Agent': 'MyApp/1.0',
    'Accept': 'application/json'
}

response = requests.get('https://api.example.com/data', headers=headers)

# Установка таймаута
try:
    response = requests.get('https://api.example.com/data', timeout=5)
    response.raise_for_status()  # Вызов исключения для ошибочных статусов
    data = response.json()
except requests.exceptions.Timeout:
    print("Время ожидания истекло")
except requests.exceptions.RequestException as e:
    print(f"Ошибка запроса: {e}")
```

### Пример 5: Работа с файлами

```python
import requests

# Загрузка файла
with open('document.pdf', 'rb') as f:
    files = {'file': f}
    response = requests.post('https://api.example.com/upload', files=files)

# Загрузка изображения с дополнительными параметрами
with open('image.jpg', 'rb') as image_file:
    files = {'image': image_file}
    data = {'description': 'Мое изображение', 'category': 'photo'}
    response = requests.post('https://api.example.com/images', files=files, data=data)
```

### Пример 6: Сессии

```python
import requests

# Использование сессии для сохранения cookies и настроек
session = requests.Session()

# Установка общих заголовков для всех запросов в сессии
session.headers.update({'Authorization': 'Bearer your-token'})

# Выполнение нескольких запросов с одинаковой сессией
response1 = session.get('https://api.example.com/profile')
response2 = session.get('https://api.example.com/orders')
response3 = session.post('https://api.example.com/messages', json={'text': 'Привет'})

# Закрытие сессии
session.close()
```

---

## 3. Аутентификация

### Пример 7: Токен-аутентификация

```python
import requests

# Аутентификация с помощью Bearer токена
headers = {
    'Authorization': 'Bearer your-access-token',
    'Content-Type': 'application/json'
}

response = requests.get('https://api.example.com/protected-data', headers=headers)

# Аутентификация с помощью API ключа
headers = {
    'X-API-Key': 'your-api-key',
    'Content-Type': 'application/json'
}

response = requests.get('https://api.example.com/data', headers=headers)
```

### Пример 8: OAuth аутентификация

```python
import requests

# OAuth 2.0 с использованием токена
def make_authenticated_request(endpoint, token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    response = requests.get(endpoint, headers=headers)
    return response

# Получение токена через OAuth
def get_oauth_token(client_id, client_secret, code, redirect_uri):
    token_url = 'https://api.example.com/oauth/token'
    
    data = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'code': code,
        'redirect_uri': redirect_uri
    }
    
    response = requests.post(token_url, data=data)
    
    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        raise Exception(f"Ошибка получения токена: {response.status_code}")
```

### Пример 9: Basic Authentication

```python
import requests
from requests.auth import HTTPBasicAuth

# Basic Authentication
response = requests.get(
    'https://api.example.com/data',
    auth=HTTPBasicAuth('username', 'password')
)

# Или короткая запись
response = requests.get(
    'https://api.example.com/data',
    auth=('username', 'password')
)
```

---

## 4. Обработка ошибок

### Пример 10: Обработка различных типов ошибок

```python
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError

def safe_api_call(url, **kwargs):
    try:
        response = requests.get(url, **kwargs)
        
        # Проверка статус-кода
        response.raise_for_status()
        
        # Попытка парсинга JSON
        try:
            return response.json()
        except ValueError:
            # Если ответ не в формате JSON
            return response.text
            
    except ConnectionError:
        print("Ошибка подключения к API")
        return None
    except Timeout:
        print("Время ожидания превышено")
        return None
    except requests.exceptions.HTTPError as e:
        print(f"HTTP ошибка: {e}")
        print(f"Статус код: {response.status_code}")
        return None
    except RequestException as e:
        print(f"Ошибка запроса: {e}")
        return None

# Использование функции
data = safe_api_call('https://api.example.com/data', timeout=10)
if data:
    print(data)
```

### Пример 11: Работа с различными статус-кодами

```python
import requests

def handle_api_response(response):
    if response.status_code == 200:
        # Успешный запрос
        return response.json()
    elif response.status_code == 201:
        # Ресурс успешно создан
        print("Ресурс создан")
        return response.json()
    elif response.status_code == 400:
        # Некорректный запрос
        error_data = response.json()
        print(f"Ошибка запроса: {error_data.get('message', 'Неизвестная ошибка')}")
        return None
    elif response.status_code == 401:
        # Неавторизованный доступ
        print("Требуется аутентификация")
        return None
    elif response.status_code == 403:
        # Доступ запрещен
        print("Доступ запрещен")
        return None
    elif response.status_code == 404:
        # Ресурс не найден
        print("Ресурс не найден")
        return None
    elif response.status_code == 500:
        # Внутренняя ошибка сервера
        print("Внутренняя ошибка сервера")
        return None
    else:
        print(f"Неизвестная ошибка: {response.status_code}")
        return None

# Использование
response = requests.get('https://api.example.com/data')
result = handle_api_response(response)
```

---

## 5. Практические задания

### Задание 1: Работа с JSONPlaceholder
Используйте API https://jsonplaceholder.typicode.com/ для:
- Получения списка пользователей
- Получения информации о конкретном пользователе
- Создания нового поста
- Обновления существующего поста
- Удаления поста

### Задание 2: Интеграция с погодным API
Используйте погодный API (например, OpenWeatherMap) для:
- Получения текущей погоды для заданного города
- Получения прогноза погоды
- Отображения информации в удобном формате

### Задание 3: Работа с GitHub API
Используйте GitHub API для:
- Получения информации о пользователе
- Получения списка репозиториев пользователя
- Поиска репозиториев по ключевым словам
- Получения информации о коммитах

### Задание 4: Создание обертки для API
Создайте класс-обертку для работы с любым API, который будет:
- Обрабатывать аутентификацию
- Управлять повторными попытками запросов
- Обрабатывать ошибки
- Кэшировать ответы (опционально)

### Задание 5: Интеграция с социальной сетью
Используйте API социальной сети (например, Twitter или VK) для:
- Аутентификации пользователя
- Получения ленты новостей
- Публикации поста
- Получения информации о друзьях/подписчиках

---

## 6. Дополнительные задания

### Задание 6: Асинхронные запросы
Используйте aiohttp для выполнения асинхронных запросов к API.

### Задание 7: Кэширование
Реализуйте кэширование ответов API для снижения количества запросов.

### Задание 8: Rate limiting
Реализуйте ограничение частоты запросов к API.

---

## Контрольные вопросы:
1. Какие HTTP-методы используются в REST API?
2. Как обработать ошибки при работе с API?
3. Какие способы аутентификации существуют?
4. Как установить таймаут для запроса?
5. Как передать параметры в GET-запросе?