# Лекция 23: Работа с API

## REST API, работа с библиотекой requests

### Цель лекции:
- Познакомиться с понятием API
- Изучить принципы REST API
- Освоить работу с библиотекой requests

### План лекции:
1. Что такое API
2. Принципы REST API
3. Библиотека requests
4. Практические примеры

---

## 1. Что такое API

API (Application Programming Interface) — интерфейс программирования приложений, позволяющий различным программам взаимодействовать друг с другом.

### Основные понятия:
- **API** - набор определений, протоколов и инструментов для создания программного обеспечения
- **Web API** - API, доступ к которому осуществляется по протоколам интернета
- **REST API** - стиль архитектуры для создания веб-сервисов

### Виды API:
- **SOAP** - протокол с жесткой структурой (XML)
- **REST** - более гибкий подход (обычно JSON)
- **GraphQL** - язык запросов для API

### Примеры использования API:
- Получение погоды с Weather API
- Работа с Twitter API
- Интеграция с Google Maps
- Платежные системы

---

## 2. Принципы REST API

REST (Representational State Transfer) — архитектурный стиль для распределенных гипермедиа-систем.

### Основные принципы:
- **Клиент-серверная архитектура**
- **Отсутствие состояния (Stateless)**
- **Кэширование**
- **Единообразие интерфейса**

### HTTP методы в REST:
- **GET** - получить данные
- **POST** - создать ресурс
- **PUT** - обновить ресурс
- **DELETE** - удалить ресурс
- **PATCH** - частичное обновление

### Примеры RESTful URL:
```
GET /users - получить всех пользователей
GET /users/123 - получить пользователя с ID 123
POST /users - создать нового пользователя
PUT /users/123 - обновить пользователя с ID 123
DELETE /users/123 - удалить пользователя с ID 123
```

### Структура JSON-ответа:
```json
{
  "id": 123,
  "name": "Иван Иванов",
  "email": "ivan@example.com",
  "created_at": "2023-01-01T10:00:00Z"
}
```

---

## 3. Библиотека requests

Requests — популярная библиотека для отправки HTTP-запросов в Python.

### Установка:
```bash
pip install requests
```

### Основные методы:
```python
import requests

# GET-запрос
response = requests.get('https://api.example.com/users')

# POST-запрос
data = {'key': 'value'}
response = requests.post('https://api.example.com/users', json=data)

# PUT-запрос
response = requests.put('https://api.example.com/users/123', json=data)

# DELETE-запрос
response = requests.delete('https://api.example.com/users/123')
```

### Обработка ответа:
```python
response = requests.get('https://api.example.com/users')

# Статус код
print(response.status_code)  # 200

# Текст ответа
print(response.text)

# JSON-ответ
data = response.json()

# Заголовки
print(response.headers['Content-Type'])
```

### Параметры запроса:
```python
# Параметры в URL
params = {'page': 1, 'limit': 10}
response = requests.get('https://api.example.com/users', params=params)

# Заголовки
headers = {'Authorization': 'Bearer token123'}
response = requests.get('https://api.example.com/users', headers=headers)

# Таймаут
response = requests.get('https://api.example.com/users', timeout=5)
```

---

## 4. Практические примеры

### Пример 1: Получение данных из JSONPlaceholder
```python
import requests

# Получение списка пользователей
response = requests.get('https://jsonplaceholder.typicode.com/users')
users = response.json()

for user in users:
    print(f"{user['id']}: {user['name']} - {user['email']}")
```

### Пример 2: Создание нового поста
```python
import requests

post_data = {
    'title': 'Новый пост',
    'body': 'Содержимое поста',
    'userId': 1
}

response = requests.post('https://jsonplaceholder.typicode.com/posts', json=post_data)

if response.status_code == 201:
    new_post = response.json()
    print(f"Создан пост с ID: {new_post['id']}")
else:
    print(f"Ошибка: {response.status_code}")
```

### Пример 3: Аутентификация с токеном
```python
import requests

headers = {
    'Authorization': 'Bearer your_token_here',
    'Content-Type': 'application/json'
}

response = requests.get('https://api.example.com/protected-endpoint', headers=headers)

if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print("Ошибка аутентификации")
```

### Обработка ошибок:
```python
import requests
from requests.exceptions import RequestException

try:
    response = requests.get('https://api.example.com/data', timeout=10)
    response.raise_for_status()  # Вызовет исключение для кодов ошибок
    data = response.json()
except requests.exceptions.HTTPError as errh:
    print(f"HTTP Error: {errh}")
except requests.exceptions.ConnectionError as errc:
    print(f"Error Connecting: {errc}")
except requests.exceptions.Timeout as errt:
    print(f"Timeout Error: {errt}")
except requests.exceptions.RequestException as err:
    print(f"Something went wrong: {err}")