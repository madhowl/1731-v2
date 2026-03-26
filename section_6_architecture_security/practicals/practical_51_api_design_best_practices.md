# Практическое занятие 51: Лучшие практики проектирования API

## RESTful API, GraphQL, версионирование API, документация

### Цель занятия:
Изучить лучшие практики проектирования API, освоить принципы RESTful API, научиться создавать качественную документацию API.

### Задачи:
1. Понять принципы RESTful API
2. Научиться проектировать удобные и масштабируемые API
3. Освоить версионирование API
4. Создать документацию для API

### План работы:
1. Принципы RESTful API
2. Проектирование URL и ресурсов
3. Обработка ошибок и коды состояния
4. Версионирование API
5. Документация API
6. Практические задания

---

## 1. Принципы RESTful API

REST (Representational State Transfer) - это архитектурный стиль для построения распределённых систем.

### Основные принципы REST:

1. **Клиент-серверная архитектура** - разделение клиента и сервера
2. **Без состояния (Stateless)** - каждый запрос содержит всю необходимую информацию
3. **Кэширование** - возможность кэширования ответов
4. **Единообразие интерфейса** - стандартные методы и форматы
5. **Слоистая система** - возможность использования промежуточных серверов

### HTTP методы и их использование:

| Метод | Описание | Идемпотентность |
|-------|----------|----------------|
| GET | Получение ресурса | Да |
| POST | Создание ресурса | Нет |
| PUT | Полная замена ресурса | Да |
| PATCH | Частичное обновление | Нет |
| DELETE | Удаление ресурса | Да |

---

## 2. Проектирование URL и ресурсов

### Пример 1: Структура URL ресурсов

```python
from flask import Flask, request, jsonify
from dataclasses import dataclass
import uuid
from typing import List, Optional

app = Flask(__name__)

# Модель данных
@dataclass
class User:
    id: str
    name: str
    email: str
    created_at: str

@dataclass
class Post:
    id: str
    user_id: str
    title: str
    content: str
    published_at: str

# Хранилище в памяти
users_db = {}
posts_db = {}

# ============ ПОЛЬЗОВАТЕЛИ ============

@app.route('/api/v1/users', methods=['GET'])
def get_users():
    """Получение списка пользователей с пагинацией"""
    # Параметры пагинации
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Параметры фильтрации
    search = request.args.get('search', '', type=str)
    
    # Фильтрация
    users = list(users_db.values())
    if search:
        users = [u for u in users if search.lower() in u.name.lower() or search.lower() in u.email.lower()]
    
    # Пагинация
    total = len(users)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_users = users[start:end]
    
    return jsonify({
        'data': [
            {'id': u.id, 'name': u.name, 'email': u.email, 'created_at': u.created_at}
            for u in paginated_users
        ],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': (total + per_page - 1) // per_page
        }
    })

@app.route('/api/v1/users', methods=['POST'])
def create_user():
    """Создание нового пользователя"""
    data = request.get_json()
    
    # Валидация
    if not data.get('name') or not data.get('email'):
        return jsonify({'error': 'Name and email are required'}), 400
    
    # Проверка уникальности email
    for user in users_db.values():
        if user.email == data['email']:
            return jsonify({'error': 'Email already exists'}), 409
    
    user = User(
        id=str(uuid.uuid4()),
        name=data['name'],
        email=data['email'],
        created_at='2024-01-01T00:00:00Z'
    )
    users_db[user.id] = user
    
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'created_at': user.created_at
    }), 201

@app.route('/api/v1/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Получение пользователя по ID"""
    user = users_db.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'created_at': user.created_at
    })

@app.route('/api/v1/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Полное обновление пользователя"""
    user = users_db.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        user.email = data['email']
    
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'created_at': user.created_at
    })

@app.route('/api/v1/users/<user_id>', methods=['PATCH'])
def patch_user(user_id):
    """Частичное обновление пользователя"""
    user = users_db.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    # Частичное обновление только переданных полей
    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        user.email = data['email']
    
    return jsonify({
        'id': user.id,
        'name': user.name,
        'email': user.email,
        'created_at': user.created_at
    })

@app.route('/api/v1/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Удаление пользователя"""
    if user_id not in users_db:
        return jsonify({'error': 'User not found'}), 404
    
    del users_db[user_id]
    return '', 204

# ============ ПОСТЫ ============

@app.route('/api/v1/posts', methods=['GET'])
def get_posts():
    """Получение списка постов"""
    posts = list(posts_db.values())
    
    # Фильтрация по автору
    author_id = request.args.get('author_id')
    if author_id:
        posts = [p for p in posts if p.user_id == author_id]
    
    return jsonify([
        {
            'id': p.id,
            'title': p.title,
            'content': p.content,
            'published_at': p.published_at
        }
        for p in posts
    ])

@app.route('/api/v1/posts', methods=['POST'])
def create_post():
    """Создание нового поста"""
    data = request.get_json()
    
    # Валидация
    if not data.get('title') or not data.get('content'):
        return jsonify({'error': 'Title and content are required'}), 400
    
    # Проверка существования автора
    if data.get('user_id') and data['user_id'] not in users_db:
        return jsonify({'error': 'User not found'}), 404
    
    post = Post(
        id=str(uuid.uuid4()),
        user_id=data.get('user_id'),
        title=data['title'],
        content=data['content'],
        published_at='2024-01-01T00:00:00Z'
    )
    posts_db[post.id] = post
    
    return jsonify({
        'id': post.id,
        'user_id': post.user_id,
        'title': post.title,
        'content': post.content,
        'published_at': post.published_at
    }), 201

@app.route('/api/v1/users/<user_id>/posts', methods=['GET'])
def get_user_posts(user_id):
    """Получение постов конкретного пользователя"""
    if user_id not in users_db:
        return jsonify({'error': 'User not found'}), 404
    
    user_posts = [p for p in posts_db.values() if p.user_id == user_id]
    
    return jsonify([
        {
            'id': p.id,
            'title': p.title,
            'content': p.content,
            'published_at': p.published_at
        }
        for p in user_posts
    ])
```

### Пример 2: Вложенные ресурсы

```python
# ============ КОММЕНТАРИИ К ПОСТАМ ============

comments_db = {}

@app.route('/api/v1/posts/<post_id>/comments'])
def get_post_comments(post_id):
', methods=['GET    """Получение комментариев к посту"""
    if post_id not in posts_db:
        return jsonify({'error': 'Post not found'}), 404
    
    post_comments = [
        c for c in comments_db.values() 
        if c['post_id'] == post_id
    ]
    
    return jsonify(post_comments)

@app.route('/api/v1/posts/<post_id>/comments', methods=['POST'])
def create_post_comment(post_id):
    """Создание комментария к посту"""
    if post_id not in posts_db:
        return jsonify({'error': 'Post not found'}), 404
    
    data = request.get_json()
    
    if not data.get('content'):
        return jsonify({'error': 'Content is required'}), 400
    
    comment = {
        'id': str(uuid.uuid4()),
        'post_id': post_id,
        'content': data['content'],
        'author': data.get('author', 'Anonymous')
    }
    comments_db[comment['id']] = comment
    
    return jsonify(comment), 201

@app.route('/api/v1/posts/<post_id>/comments/<comment_id>', methods=['DELETE'])
def delete_comment(post_id, comment_id):
    """Удаление комментария"""
    if post_id not in posts_db:
        return jsonify({'error': 'Post not found'}), 404
    
    if comment_id not in comments_db:
        return jsonify({'error': 'Comment not found'}), 404
    
    del comments_db[comment_id]
    return '', 204
```

---

## 3. Обработка ошибок и коды состояния

### Пример 3: Единообразная обработка ошибок

```python
from flask import Flask, jsonify
from functools import wraps

app = Flask(__name__)

# Стандартные коды ошибок
ERROR_CODES = {
    400: 'Bad Request - Некорректный запрос',
    401: 'Unauthorized - Требуется аутентификация',
    403: 'Forbidden - Доступ запрещён',
    404: 'Not Found - Ресурс не найден',
    409: 'Conflict - Конфликт данных',
    422: 'Unprocessable Entity - Неверные данные',
    429: 'Too Many Requests - Слишком много запросов',
    500: 'Internal Server Error - Внутренняя ошибка сервера',
    503: 'Service Unavailable - Сервис недоступен'
}

class APIException(Exception):
    """Базовый класс для API исключений"""
    def __init__(self, message: str, status_code: int = 400, error_code: str = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_code = error_code or f'ERROR_{status_code}'
    
    def to_dict(self):
        return {
            'error': {
                'message': self.message,
                'code': self.error_code,
                'status': self.status_code
            }
        }

class NotFoundException(APIException):
    def __init__(self, resource: str, resource_id: str):
        super().__init__(
            message=f'{resource} with id {resource_id} not found',
            status_code=404,
            error_code='RESOURCE_NOT_FOUND'
        )

class ValidationException(APIException):
    def __init__(self, message: str, field: str = None):
        error_message = message if not field else f'{field}: {message}'
        super().__init__(
            message=error_message,
            status_code=422,
            error_code='VALIDATION_ERROR'
        )

class AuthenticationException(APIException):
    def __init__(self, message: str = 'Authentication required'):
        super().__init__(
            message=message,
            status_code=401,
            error_code='AUTHENTICATION_REQUIRED'
        )

class AuthorizationException(APIException):
    def __init__(self, message: str = 'Access denied'):
        super().__init__(
            message=message,
            status_code=403,
            error_code='ACCESS_DENIED'
        )

# Обработчик исключений
@app.errorhandler(APIException)
def handle_api_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

@app.errorhandler(404)
def handle_not_found(error):
    return jsonify({
        'error': {
            'message': 'Resource not found',
            'code': 'NOT_FOUND',
            'status': 404
        }
    }), 404

@app.errorhandler(500)
def handle_server_error(error):
    return jsonify({
        'error': {
            'message': 'Internal server error',
            'code': 'INTERNAL_ERROR',
            'status': 500
        }
    }), 500

# Примеры использования исключений
@app.route('/api/users/<user_id>')
def get_user_safe(user_id):
    user = users_db.get(user_id)
    if not user:
        raise NotFoundException('User', user_id)
    
    return jsonify({'id': user.id, 'name': user.name})

@app.route('/api/users', methods=['POST'])
def create_user_safe():
    data = request.get_json()
    
    if not data.get('name'):
        raise ValidationException('Name is required', 'name')
    
    if not data.get('email'):
        raise ValidationException('Email is required', 'email')
    
    # Проверка email
    import re
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', data['email']):
        raise ValidationException('Invalid email format', 'email')
    
    return jsonify({'id': '123', 'name': data['name']})
```

---

## 4. Версионирование API

### Пример 4: Различные подходы к версионированию

```python
# Подход 1: URL path versioning (наиболее распространённый)
@app.route('/api/v1/users')
def get_users_v1():
    """Версия 1 API"""
    return jsonify({'version': 'v1', 'users': []})

@app.route('/api/v2/users')
def get_users_v2():
    """Версия 2 API - с дополнительными полями"""
    return jsonify({
        'version': 'v2',
        'users': [],
        'meta': {
            'deprecated': False,
            'deprecation_date': None
        }
    })

# Подход 2: Header versioning
@app.route('/api/users')
def get_users_by_header():
    version = request.headers.get('Accept-Version', 'v1')
    
    if version == 'v2':
        return jsonify({'version': 'v2', 'users': []})
    
    return jsonify({'version': 'v1', 'users': []})

# Подход 3: Query parameter versioning
@app.route('/api/users')
def get_users_by_param():
    version = request.args.get('version', 'v1')
    
    if version == 'v2':
        return jsonify({'version': 'v2', 'users': []})
    
    return jsonify({'version': 'v1', 'users': []})

# Пример: Изменения между версиями
@app.route('/api/v1/users/<user_id>')
def get_user_v1(user_id):
    """Версия 1 - базовые поля"""
    return jsonify({
        'id': user_id,
        'name': 'John Doe',
        'email': 'john@example.com'
    })

@app.route('/api/v2/users/<user_id>')
def get_user_v2(user_id):
    """Версия 2 - расширенные поля"""
    return jsonify({
        'id': user_id,
        'name': 'John Doe',
        'email': 'john@example.com',
        'profile': {
            'avatar_url': 'https://example.com/avatars/1.jpg',
            'bio': 'Software Developer',
            'location': 'Moscow, Russia'
        },
        'statistics': {
            'posts_count': 42,
            'followers_count': 100,
            'following_count': 50
        }
    })

# Поддержка устаревших версий
@app.route('/api/v1/users/<user_id>')
def get_user_v1_deprecated(user_id):
    """Версия 1 с предупреждением об устаревании"""
    response = jsonify({
        'id': user_id,
        'name': 'John Doe',
        'email': 'john@example.com'
    })
    response.headers['Deprecation'] = 'true'
    response.headers['Sunset'] = 'Sat, 01 Jan 2025 00:00:00 GMT'
    response.headers['Link'] = '<https://api.example.com/v2/users/' + user_id + '>; rel="successor-version"'
    return response
```

---

## 5. Документация API

### Пример 5: OpenAPI спецификация

```python
# Пример OpenAPI документации (YAML)
OPENAPI_SPEC = """
openapi: 3.0.3
info:
  title: User Management API
  description: API для управления пользователями и их публикациями
  version: 1.0.0
  contact:
    name: API Support
    email: support@example.com

servers:
  - url: https://api.example.com/v1
    description: Production server
  - url: https://staging-api.example.com/v1
    description: Staging server

paths:
  /users:
    get:
      summary: Получить список пользователей
      description: Возвращает список всех пользователей с поддержкой пагинации
      parameters:
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: per_page
          in: query
          schema:
            type: integer
            default: 10
            maximum: 100
        - name: search
          in: query
          schema:
            type: string
      responses:
        '200':
          description: Успешный запрос
          content:
            application/json:
              schema:
                type: object
                properties:
                  data:
                    type: array
                    items:
                      $ref: '#/components/schemas/User'
                  pagination:
                    $ref: '#/components/schemas/Pagination'
        '400':
          $ref: '#/components/responses/BadRequest'
        '401':
          $ref: '#/components/responses/Unauthorized'

    post:
      summary: Создать пользователя
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateUserRequest'
      responses:
        '201':
          description: Пользователь создан
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/User'
        '400':
          $ref: '#/components/responses/BadRequest'
        '409':
          $ref: '#/components/responses/Conflict'

components:
  schemas:
    User:
      type: object
      properties:
        id:
          type: string
          format: uuid
        name:
          type: string
        email:
          type: string
          format: email
        created_at:
          type: string
          format: date-time
    
    CreateUserRequest:
      type: object
      required:
        - name
        - email
      properties:
        name:
          type: string
          minLength: 1
          maxLength: 100
        email:
          type: string
          format: email
    
    Pagination:
      type: object
      properties:
        page:
          type: integer
        per_page:
          type: integer
        total:
          type: integer
        pages:
          type: integer

  responses:
    BadRequest:
      description: Некорректный запрос
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    
    Unauthorized:
      description: Требуется аутентификация
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    
    Conflict:
      description: Конфликт данных
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/Error'
    
    Error:
      type: object
      properties:
        error:
          type: object
          properties:
            message:
              type: string
            code:
              type: string
"""
```

---

## 6. Практические задания

### Задание 1: Проектирование API блога

Спроектируйте RESTful API для блога со следующими сущностями:
- Пользователи (Users)
- Статьи (Articles)
- Комментарии (Comments)
- Теги (Tags)

Требования:
- CRUD операции для каждой сущности
- Пагинация и фильтрация
- Вложенные ресурсы (комментарии к статьям, теги к статьям)
- Единообразная обработка ошибок

### Задание 2: Версионирование API

Добавьте версионирование к API из задания 1:
- Поддержка версий v1 и v2
- Документация изменений между версиями
- Заголовки deprecation для устаревших эндпоинтов

### Задание 3: Документация

Создайте OpenAPI спецификацию для вашего API:
- Опишите все эндпоинты
- Добавьте схемы для всех моделей данных
- Включите примеры запросов и ответов

### Задание 4: GraphQL API

Реализуйте GraphQL версию API:
- Определите схему (Schema)
- Создайте резолверы для основных операций
- Реализуйте мутации для создания и обновления данных

### Задание 5: Rate Limiting

Добавьте ограничение частоты запросов к API:
- Ограничение на количество запросов в минуту
- Различные лимиты для разных типов пользователей
- Возврат соответствующих заголовков (X-RateLimit-*)

---

## Контрольные вопросы:

1. Какие HTTP методы следует использовать для различных операций?
2. В чём разница между PUT и PATCH?
3. Какие способы версионирования API вы знаете?
4. Какие коды состояния HTTP следует использовать для различных ошибок?
5. Зачем нужна документация API и какие инструменты для этого используются?

---

## Дополнительные материалы:

- "REST API Design Rulebook" - Mark Masse
- "API Design Patterns" - JJ Geewax
- OpenAPI Specification: https://swagger.io/specification/
