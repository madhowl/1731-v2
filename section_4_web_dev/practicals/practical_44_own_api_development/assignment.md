# Практическое занятие 44: Создание своего API

## Разработка REST API с использованием Flask и Django

### Цель занятия:
Научиться создавать собственные REST API с использованием Flask и Django, реализовывать CRUD-операции, работать с маршрутами и обрабатывать различные типы запросов.

### Задачи:
1. Создать простое API с использованием Flask
2. Реализовать CRUD-операции для сущности
3. Настроить маршруты для API
4. Обработать различные типы HTTP-запросов

### План работы:
1. Основы REST API
2. Создание API с Flask
3. Создание API с Django
4. Работа с базой данных
5. Практические задания

---

## 1. Основы REST API

REST (Representational State Transfer) - это архитектурный стиль для создания веб-сервисов. REST API использует стандартные HTTP-методы для выполнения операций над ресурсами.

### Пример 1: Основные принципы REST

```
GET /users - получить список пользователей
GET /users/1 - получить пользователя с ID 1
POST /users - создать нового пользователя
PUT /users/1 - обновить пользователя с ID 1
DELETE /users/1 - удалить пользователя с ID 1
```

### Пример 2: Структура REST API ответа

```json
{
  "status": "success",
  "data": {
    "id": 1,
    "name": "Иван Иванов",
    "email": "ivan@example.com"
  },
  "message": "Пользователь успешно получен"
}
```

### Пример 3: Ошибки в REST API

```json
{
  "status": "error",
  "message": "Пользователь не найден",
  "code": 404
}
```

---

## 2. Создание API с Flask

### Пример 4: Простой Flask API

```python
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# Имитация базы данных
users = [
    {'id': 1, 'name': 'Иван Иванов', 'email': 'ivan@example.com', 'created_at': datetime.now()},
    {'id': 2, 'name': 'Мария Петрова', 'email': 'maria@example.com', 'created_at': datetime.now()}
]

# Получить всех пользователей
@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify({
        'status': 'success',
        'data': users,
        'count': len(users)
    })

# Получить пользователя по ID
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if user:
        return jsonify({
            'status': 'success',
            'data': user
        })
    else:
        return jsonify({
            'status': 'error',
            'message': 'Пользователь не найден',
            'code': 404
        }), 404

# Создать нового пользователя
@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    # Валидация данных
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({
            'status': 'error',
            'message': 'Имя и email обязательны',
            'code': 400
        }), 400
    
    # Создание нового пользователя
    new_user = {
        'id': len(users) + 1,
        'name': data['name'],
        'email': data['email'],
        'created_at': datetime.now()
    }
    users.append(new_user)
    
    return jsonify({
        'status': 'success',
        'data': new_user,
        'message': 'Пользователь успешно создан'
    }), 201

# Обновить пользователя
@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = next((u for u in users if u['id'] == user_id), None)
    if not user:
        return jsonify({
            'status': 'error',
            'message': 'Пользователь не найден',
            'code': 404
        }), 404
    
    data = request.get_json()
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'Нет данных для обновления',
            'code': 400
        }), 400
    
    # Обновление данных
    if 'name' in data:
        user['name'] = data['name']
    if 'email' in data:
        user['email'] = data['email']
    
    return jsonify({
        'status': 'success',
        'data': user,
        'message': 'Пользователь успешно обновлен'
    })

# Удалить пользователя
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    global users
    user_index = next((i for i, u in enumerate(users) if u['id'] == user_id), None)
    if user_index is not None:
        deleted_user = users.pop(user_index)
        return jsonify({
            'status': 'success',
            'data': deleted_user,
            'message': 'Пользователь успешно удален'
        })
    else:
        return jsonify({
            'status': 'error',
            'message': 'Пользователь не найден',
            'code': 404
        }), 404

if __name__ == '__main__':
    app.run(debug=True)
```

### Пример 5: Flask API с базой данных

```python
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Модель пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }

# Создание таблиц
with app.app_context():
    db.create_all()

# CRUD операции
@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify({
        'status': 'success',
        'data': [user.to_dict() for user in users],
        'count': len(users)
    })

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({
            'status': 'error',
            'message': 'Имя и email обязательны',
            'code': 400
        }), 400
    
    # Проверка уникальности email
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({
            'status': 'error',
            'message': 'Пользователь с таким email уже существует',
            'code': 400
        }), 400
    
    new_user = User(name=data['name'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'data': new_user.to_dict(),
        'message': 'Пользователь успешно создан'
    }), 201

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({
            'status': 'success',
            'data': user.to_dict()
        })
    else:
        return jsonify({
            'status': 'error',
            'message': 'Пользователь не найден',
            'code': 404
        }), 404

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({
            'status': 'error',
            'message': 'Пользователь не найден',
            'code': 404
        }), 404
    
    data = request.get_json()
    if not data:
        return jsonify({
            'status': 'error',
            'message': 'Нет данных для обновления',
            'code': 400
        }), 400
    
    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        # Проверка уникальности email
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user and existing_user.id != user.id:
            return jsonify({
                'status': 'error',
                'message': 'Пользователь с таким email уже существует',
                'code': 400
            }), 400
        user.email = data['email']
    
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'data': user.to_dict(),
        'message': 'Пользователь успешно обновлен'
    })

@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({
            'status': 'error',
            'message': 'Пользователь не найден',
            'code': 404
        }), 404
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'data': user.to_dict(),
        'message': 'Пользователь успешно удален'
    })

if __name__ == '__main__':
    app.run(debug=True)
```

---

## 3. Создание API с Django

### Пример 6: Django API с Django REST Framework

```python
# models.py
from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title

# serializers.py
from rest_framework import serializers
from .models import Article
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class ArticleSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # Добавляем текущего пользователя как автора
        request = self.context.get('request')
        if request:
            validated_data['author'] = request.user
        return super().create(validated_data)
```

### Пример 7: Django API ViewSets

```python
# views.py
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Article
from .serializers import ArticleSerializer

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        # Фильтрация статей по пользователю
        if self.action == 'my_articles':
            return Article.objects.filter(author=self.request.user)
        return Article.objects.all()
    
    def perform_create(self, serializer):
        # Установка автора при создании статьи
        serializer.save(author=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_articles(self, request):
        """Получить статьи текущего пользователя"""
        articles = self.get_queryset()
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """Получить последние 5 статей"""
        articles = Article.objects.order_by('-created_at')[:5]
        serializer = self.get_serializer(articles, many=True)
        return Response(serializer.data)
```

### Пример 8: URLs для Django API

```python
# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'articles', views.ArticleViewSet, basename='article')

urlpatterns = [
    path('api/', include(router.urls)),
    # Дополнительные маршруты
    path('api/auth/', include('rest_framework.urls')),
]
```

### Пример 9: Django API с кастомными представлениями

```python
# views.py (альтернативный подход)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Article
from .serializers import ArticleSerializer

class ArticleList(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        articles = Article.objects.filter(author=request.user)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = ArticleSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ArticleDetail(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_object(self, pk, user):
        try:
            return Article.objects.get(pk=pk, author=user)
        except Article.DoesNotExist:
            return None
    
    def get(self, request, pk):
        article = self.get_object(pk, request.user)
        if article:
            serializer = ArticleSerializer(article)
            return Response(serializer.data)
        return Response({'error': 'Article not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def put(self, request, pk):
        article = self.get_object(pk, request.user)
        if not article:
            return Response({'error': 'Article not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ArticleSerializer(article, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        article = self.get_object(pk, request.user)
        if not article:
            return Response({'error': 'Article not found'}, status=status.HTTP_404_NOT_FOUND)
        
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
```

---

## 4. Работа с базой данных

### Пример 10: Пагинация в API

```python
# Flask с пагинацией
@app.route('/api/users', methods=['GET'])
def get_users_paginated():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    
    # Ограничение максимального количества элементов на странице
    per_page = min(per_page, 100)
    
    offset = (page - 1) * per_page
    paginated_users = users[offset:offset + per_page]
    
    return jsonify({
        'status': 'success',
        'data': paginated_users,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': len(users),
            'pages': (len(users) + per_page - 1) // per_page
        }
    })

# Django REST Framework с пагинацией
from rest_framework.pagination import PageNumberPagination

class CustomPageNumberPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'per_page'
    max_page_size = 100

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    pagination_class = CustomPageNumberPagination
```

### Пример 11: Фильтрация и поиск

```python
# Flask с фильтрацией
@app.route('/api/users', methods=['GET'])
def get_filtered_users():
    name_filter = request.args.get('name')
    email_filter = request.args.get('email')
    sort_by = request.args.get('sort_by', 'id')
    order = request.args.get('order', 'asc')
    
    filtered_users = users
    
    if name_filter:
        filtered_users = [u for u in filtered_users if name_filter.lower() in u['name'].lower()]
    
    if email_filter:
        filtered_users = [u for u in filtered_users if email_filter.lower() in u['email'].lower()]
    
    # Сортировка
    reverse_order = order.lower() == 'desc'
    filtered_users.sort(key=lambda x: x[sort_by], reverse=reverse_order)
    
    return jsonify({
        'status': 'success',
        'data': filtered_users
    })

# Django REST Framework с фильтрацией
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['author__username', 'created_at']
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']
```

---

## 5. Практические задания

### Задание 1: Простой Flask API
Создайте Flask API для управления книгами:
- Маршруты для получения списка книг, получения книги по ID
- Создание, обновление и удаление книг
- Валидация данных при создании/обновлении

### Задание 2: Django API
Создайте Django API для управления задачами:
- Модель задачи с полями: название, описание, статус, приоритет, дата создания
- API для CRUD операций
- Использование Django REST Framework

### Задание 3: Аутентификация в API
Реализуйте аутентификацию в созданном API:
- Регистрация пользователя
- Аутентификация по токену
- Защита маршрутов

### Задание 4: Пагинация и фильтрация
Добавьте в API:
- Пагинацию для списковых представлений
- Возможность фильтрации по различным полям
- Поиск по ключевым словам

### Задание 5: Отношения между моделями
Создайте API с несколькими связанными моделями:
- Пользователи, проекты, задачи
- Реализуйте API для работы с этими сущностями
- Обеспечьте корректную сериализацию связанных данных

---

## 6. Дополнительные задания

### Задание 6: Кэширование
Реализуйте кэширование для часто запрашиваемых данных.

### Задание 7: Rate limiting
Добавьте ограничение частоты запросов к API.

### Задание 8: Документация API
Создайте документацию для вашего API (с помощью Swagger/OpenAPI).

---

## Контрольные вопросы:
1. Какие HTTP-методы используются в REST API?
2. Как создать API с использованием Flask?
3. Какие преимущества предоставляет Django REST Framework?
4. Как реализовать аутентификацию в API?
5. Как добавить пагинацию и фильтрацию в API?