#!/usr/bin/env python3
"""
Практическое занятие 51: Лучшие практики проектирования API
Решение упражнений
"""

from flask import Flask, request, jsonify
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
import uuid
import re
from datetime import datetime


# ==============================================================================
# УПРАЖНЕНИЕ 1: RESTful API для пользователей и постов
# ==============================================================================

app = Flask(__name__)


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
users_db: Dict[str, User] = {}
posts_db: Dict[str, Post] = {}
comments_db: Dict[str, Dict] = {}


# ==============================================================================
# Ресурс: Пользователи
# ==============================================================================

@app.route('/api/v1/users', methods=['GET'])
def get_users():
    """Получение списка пользователей с пагинацией"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '', type=str)
    
    users = list(users_db.values())
    
    # Фильтрация
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
    
    # Проверка формата email
    if not re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', data.get('email', '')):
        return jsonify({'error': 'Invalid email format'}), 400
    
    # Проверка уникальности email
    for user in users_db.values():
        if user.email == data['email']:
            return jsonify({'error': 'Email already exists'}), 409
    
    user = User(
        id=str(uuid.uuid4()),
        name=data['name'],
        email=data['email'],
        created_at=datetime.now().isoformat()
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


# ==============================================================================
# Ресурс: Посты
# ==============================================================================

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
    user_id = data.get('user_id')
    if user_id and user_id not in users_db:
        return jsonify({'error': 'User not found'}), 404
    
    post = Post(
        id=str(uuid.uuid4()),
        user_id=user_id or '',
        title=data['title'],
        content=data['content'],
        published_at=datetime.now().isoformat()
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


# ==============================================================================
# Ресурс: Комментарии (вложенные ресурсы)
# ==============================================================================

@app.route('/api/v1/posts/<post_id>/comments', methods=['GET'])
def get_post_comments(post_id):
    """Получение комментариев к посту"""
    if post_id not in posts_db:
        return jsonify({'error': 'Post not found'}), 404
    
    post_comments = [c for c in comments_db.values() if c['post_id'] == post_id]
    
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
        'author': data.get('author', 'Anonymous'),
        'created_at': datetime.now().isoformat()
    }
    comments_db[comment['id']] = comment
    
    return jsonify(comment), 201


# ==============================================================================
# УПРАЖНЕНИЕ 2: Обработка ошибок и коды состояния
# ==============================================================================

print("=" * 60)
print("Упражнение 2: Обработка ошибок")
print("=" * 60)


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
    
    def to_dict(self) -> Dict[str, Any]:
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


# Демонстрация использования исключений
def demonstrate_exceptions():
    """Демонстрация работы исключений"""
    
    print("1. NotFoundException:")
    try:
        raise NotFoundException('User', '123')
    except APIException as e:
        print(f"   {e.to_dict()}")
    
    print("\n2. ValidationException:")
    try:
        raise ValidationException('Email is required', 'email')
    except APIException as e:
        print(f"   {e.to_dict()}")
    
    print("\n3. AuthenticationException:")
    try:
        raise AuthenticationException()
    except APIException as e:
        print(f"   {e.to_dict()}")


demonstrate_exceptions()


# ==============================================================================
# УПРАЖНЕНИЕ 3: Версионирование API
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 3: Версионирование API")
print("=" * 60)


# Подход 1: URL path versioning
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
    """Версионирование через заголовок"""
    version = request.headers.get('Accept-Version', 'v1')
    
    if version == 'v2':
        return jsonify({'version': 'v2', 'users': []})
    
    return jsonify({'version': 'v1', 'users': []})


# Подход 3: Query parameter versioning
@app.route('/api/users')
def get_users_by_query():
    """Версионирование через query параметр"""
    version = request.args.get('version', 'v1')
    
    if version == 'v2':
        return jsonify({'version': 'v2', 'users': []})
    
    return jsonify({'version': 'v1', 'users': []})


print("Зарегистрированы endpoints:")
print("  - GET /api/v1/users")
print("  - GET /api/v2/users")
print("  - GET /api/users (с версией в заголовке или query)")


# ==============================================================================
# УПРАЖНЕНИЕ 4: Пагинация
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 4: Пагинация")
print("=" * 60)


def paginate(items: List, page: int, per_page: int) -> Dict[str, Any]:
    """Универсальная функция пагинации"""
    total = len(items)
    start = (page - 1) * per_page
    end = start + per_page
    
    return {
        'data': items[start:end],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': (total + per_page - 1) // per_page if per_page > 0 else 0,
            'has_next': end < total,
            'has_prev': page > 1
        }
    }


# Тестирование пагинации
test_items = list(range(1, 101))
result = paginate(test_items, page=2, per_page=10)
print(f"Страница 2, по 10 элементов:")
print(f"  Элементов на странице: {len(result['data'])}")
print(f"  Всего страниц: {result['pagination']['pages']}")
print(f"  Есть следующая: {result['pagination']['has_next']}")


# ==============================================================================
# УПРАЖНЕНИЕ 5: Фильтрация и сортировка
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 5: Фильтрация и сортировка")
print("=" * 60)


def filter_and_sort(
    items: List[Dict],
    filters: Dict = None,
    sort_by: str = None,
    sort_order: str = 'asc'
) -> List[Dict]:
    """Фильтрация и сортировка элементов"""
    result = items.copy()
    
    # Фильтрация
    if filters:
        for key, value in filters.items():
            result = [item for item in result if item.get(key) == value]
    
    # Сортировка
    if sort_by:
        reverse = sort_order == 'desc'
        result = sorted(result, key=lambda x: x.get(sort_by, ''), reverse=reverse)
    
    return result


# Тестирование
test_users = [
    {'name': 'Иван', 'age': 30, 'city': 'Москва'},
    {'name': 'Мария', 'age': 25, 'city': 'Санкт-Петербург'},
    {'name': 'Пётр', 'age': 35, 'city': 'Москва'},
    {'name': 'Анна', 'age': 28, 'city': 'Москва'},
]

# Фильтрация по городу
filtered = filter_and_sort(test_users, filters={'city': 'Москва'})
print(f"Пользователи из Москвы: {[u['name'] for u in filtered]}")

# Сортировка по возрасту
sorted_users = filter_and_sort(test_users, sort_by='age', sort_order='desc')
print(f"По возрасту (убывание): {[u['name'] for u in sorted_users]}")


print("\n" + "=" * 60)
print("Все упражнения выполнены!")
print("=" * 60)


if __name__ == '__main__':
    # Добавление тестовых данных
    users_db['1'] = User('1', 'Иван', 'ivan@example.com', '2024-01-01')
    users_db['2'] = User('2', 'Мария', 'maria@example.com', '2024-01-02')
    
    posts_db['1'] = Post('1', '1', 'Первый пост', 'Содержание первого поста', '2024-01-01')
    posts_db['2'] = Post('2', '1', 'Второй пост', 'Содержание второго поста', '2024-01-02')
    
    # Запуск приложения
    print("\nТестовый сервер запущен на http://localhost:5000")
    print("Доступные endpoints:")
    print("  GET    /api/v1/users")
    print("  POST   /api/v1/users")
    print("  GET    /api/v1/users/<id>")
    print("  PUT    /api/v1/users/<id>")
    print("  DELETE /api/v1/users/<id>")
    print("  GET    /api/v1/posts")
    print("  POST   /api/v1/posts")
    print("  GET    /api/v1/users/<id>/posts")
    print("  GET    /api/v1/posts/<id>/comments")
    print("  POST   /api/v1/posts/<id>/comments")
    app.run(debug=False, port=5000)
