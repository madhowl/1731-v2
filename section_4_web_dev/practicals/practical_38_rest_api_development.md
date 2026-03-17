# Практическое занятие 38: Разработка REST API

## Создание REST API

### Цель занятия:
Научиться создавать REST API с использованием Flask и Django, понимать принципы REST, реализовывать CRUD-операции, работать с аутентификацией и документацией API.

### Задачи:
1. Понять принципы REST
2. Создать REST API на Flask
3. Создать REST API на Django REST Framework
4. Реализовать аутентификацию в API
5. Добавить документацию

### План работы:
1. Принципы REST
2. REST API на Flask
3. Django REST Framework
4. Аутентификация в API
5. Документация API
6. Практические задания

---

## 1. Принципы REST

### Основные понятия

REST (Representational State Transfer) - это архитектурный стиль для построения веб-сервисов. RESTful API использует HTTP-методы для выполнения операций.

### HTTP-методы и их соответствие CRUD-операциям

| Метод | Операция | Описание |
|-------|----------|----------|
| GET | Read | Получение данных |
| POST | Create | Создание новых данных |
| PUT | Update | Полное обновление данных |
| PATCH | Update | Частичное обновление |
| DELETE | Delete | Удаление данных |

### Пример 1: Структура RESTful URL

```
# Ресурс: Статьи (Articles)
GET    /api/articles/          - Получить все статьи
GET    /api/articles/{id}/      - Получить статью по ID
POST   /api/articles/           - Создать статью
PUT    /api/articles/{id}/      - Обновить статью полностью
PATCH  /api/articles/{id}/      - Обновить статью частично
DELETE /api/articles/{id}/      - Удалить статью

# Вложенные ресурсы
GET    /api/users/{id}/articles/    - Статьи пользователя
GET    /api/articles/{id}/comments/ - Комментарии статьи
```

### Пример 2: Форматы ответов

```json
// Ответ при успешном получении (GET)
{
    "id": 1,
    "title": "Введение в Python",
    "content": "...",
    "author": {
        "id": 1,
        "username": "admin"
    },
    "created_at": "2024-01-15T10:30:00Z",
    "tags": ["python", "programming"]
}

// Ответ при создании (POST) - 201 Created
{
    "id": 5,
    "title": "Новая статья",
    "created_at": "2024-01-15T12:00:00Z",
    "links": {
        "self": "/api/articles/5/",
        "edit": "/api/articles/5/",
        "delete": "/api/articles/5/"
    }
}

// Пагинированный ответ
{
    "count": 100,
    "next": "/api/articles/?page=2",
    "previous": null,
    "results": [...]
}

// Ответ об ошибке
{
    "error": "Not Found",
    "message": "Статья с ID 999 не найдена",
    "status_code": 404
}
```

---

## 2. REST API на Flask

### Пример 3: Базовое REST API на Flask

```python
# app.py

from flask import Flask, request, jsonify, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Разрешение CORS для фронтенда

# Имитация базы данных
articles = [
    {'id': 1, 'title': 'Введение в Python', 'content': 'Полный курс Python...', 'author': 'admin'},
    {'id': 2, 'title': 'Flask для начинающих', 'content': 'Учимся создавать веб-приложения...', 'author': 'john'},
]
next_id = 3

# Получить все статьи
@app.route('/api/articles', methods=['GET'])
def get_articles():
    return jsonify({
        'articles': articles,
        'count': len(articles)
    })

# Получить статью по ID
@app.route('/api/articles/<int:article_id>', methods=['GET'])
def get_article(article_id):
    article = next((a for a in articles if a['id'] == article_id), None)
    if article is None:
        abort(404, description="Статья не найдена")
    return jsonify(article)

# Создать статью
@app.route('/api/articles', methods=['POST'])
def create_article():
    global next_id
    
    if not request.json:
        abort(400, description="Данные не в формате JSON")
    
    if 'title' not in request.json or 'content' not in request.json:
        abort(400, description="Заголовок и содержание обязательны")
    
    article = {
        'id': next_id,
        'title': request.json['title'],
        'content': request.json['content'],
        'author': request.json.get('author', 'anonymous')
    }
    next_id += 1
    articles.append(article)
    
    return jsonify(article), 201

# Обновить статью полностью
@app.route('/api/articles/<int:article_id>', methods=['PUT'])
def update_article(article_id):
    article = next((a for a in articles if a['id'] == article_id), None)
    if article is None:
        abort(404, description="Статья не найдена")
    
    if not request.json:
        abort(400, description="Данные не в формате JSON")
    
    article['title'] = request.json.get('title', article['title'])
    article['content'] = request.json.get('content', article['content'])
    article['author'] = request.json.get('author', article['author'])
    
    return jsonify(article)

# Частичное обновление
@app.route('/api/articles/<int:article_id>', methods=['PATCH'])
def patch_article(article_id):
    article = next((a for a in articles if a['id'] == article_id), None)
    if article is None:
        abort(404, description="Статья не найдена")
    
    if not request.json:
        abort(400, description="Данные не в формате JSON")
    
    for key, value in request.json.items():
        if key in article:
            article[key] = value
    
    return jsonify(article)

# Удалить статью
@app.route('/api/articles/<int:article_id>', methods=['DELETE'])
def delete_article(article_id):
    global articles
    article = next((a for a in articles if a['id'] == article_id), None)
    if article is None:
        abort(404, description="Статья не найдена")
    
    articles = [a for a in articles if a['id'] != article_id]
    
    return '', 204

# Обработка ошибок
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': str(error.description)}), 404

@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': str(error.description)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### Пример 4: REST API с Flask-RESTful

```bash
pip install flask-restful
```

```python
# app.py

from flask import Flask
from flask_restful import Api, Resource, reqparse, abort
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

# Инициализация парсера аргументов
article_parser = reqparse.RequestParser()
article_parser.add_argument('title', type=str, required=True, help='Заголовок обязателен')
article_parser.add_argument('content', type=str, required=True, help='Содержание обязательно')
article_parser.add_argument('author', type=str, default='anonymous')

# Класс ресурса
class ArticleListResource(Resource):
    def get(self):
        return {'articles': articles, 'count': len(articles)}
    
    def post(self):
        args = article_parser.parse_args()
        article = {
            'id': next_id,
            'title': args['title'],
            'content': args['content'],
            'author': args['author']
        }
        articles.append(article)
        return article, 201

class ArticleResource(Resource):
    def get(self, article_id):
        article = next((a for a in articles if a['id'] == article_id), None)
        if article is None:
            abort(404, message="Статья не найдена")
        return article
    
    def put(self, article_id):
        article = next((a for a in articles if a['id'] == article_id), None)
        if article is None:
            abort(404, message="Статья не найдена")
        
        args = article_parser.parse_args()
        article['title'] = args['title']
        article['content'] = args['content']
        article['author'] = args['author']
        return article
    
    def delete(self, article_id):
        global articles
        article = next((a for a in articles if a['id'] == article_id), None)
        if article is None:
            abort(404, message="Статья не найдена")
        
        articles = [a for a in articles if a['id'] != article_id]
        return '', 204

# Имитация базы данных
articles = []
next_id = 1

# Регистрация маршрутов
api.add_resource(ArticleListResource, '/api/articles')
api.add_resource(ArticleResource, '/api/articles/<int:article_id>')

if __name__ == '__main__':
    app.run(debug=True)
```

---

## 3. Django REST Framework

### Пример 5: Установка и настройка

```bash
pip install djangorestframework
```

```python
# myproject/settings.py

INSTALLED_APPS = [
    # ...
    'rest_framework',
]

# Настройки DRF
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}
```

### Пример 6: Сериализаторы

```python
# blog/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Article, Category, Tag, Comment

class UserSerializer(serializers.ModelSerializer):
    """Сериализатор пользователя"""
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        ref_name = 'BlogUser'

class TagSerializer(serializers.ModelSerializer):
    """Сериализатор тегов"""
    
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']

class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий"""
    article_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'article_count']
    
    def get_article_count(self, obj):
        return obj.articles.count()

class ArticleListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка статей"""
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'slug', 'excerpt', 'author', 'category', 
                  'tags', 'view_count', 'comment_count', 'published_at', 'created_at']
    
    def get_comment_count(self, obj):
        return obj.comments.count()

class ArticleDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детальной статьи"""
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    comments = serializers.SerializerMethodField()
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'slug', 'content', 'excerpt', 'author', 
                  'category', 'tags', 'view_count', 'comments', 
                  'published_at', 'created_at', 'updated_at']
        read_only_fields = ['view_count', 'published_at', 'created_at', 'updated_at']
    
    def get_comments(self, obj):
        comments = obj.comments.filter(is_approved=True, parent=None)
        return CommentSerializer(comments, many=True).data

class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор комментариев"""
    author_name = serializers.CharField(read_only=True)
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'author_name', 'author_email', 'content', 
                  'created_at', 'replies']
    
    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.filter(is_approved=True), many=True).data
        return []

class ArticleCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания статьи"""
    
    class Meta:
        model = Article
        fields = ['title', 'slug', 'content', 'excerpt', 'category', 'tags', 'image', 'status']
    
    def validate_title(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Заголовок слишком короткий")
        return value
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
```

### Пример 7: Представления API

```python
# blog/api_views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Q
from .models import Article, Category, Tag, Comment
from .serializers import (
    ArticleListSerializer, ArticleDetailSerializer, 
    ArticleCreateSerializer, CategorySerializer, 
    TagSerializer, CommentSerializer
)

class ArticleViewSet(viewsets.ModelViewSet):
    """ViewSet для статей"""
    queryset = Article.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer
        if self.action in ['create', 'update', 'partial_update']:
            return ArticleCreateSerializer
        return ArticleDetailSerializer
    
    def get_queryset(self):
        queryset = Article.objects.filter(status=Article.Status.PUBLISHED)
        
        # Фильтрация по категории
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category__slug=category)
        
        # Фильтрация по тегу
        tag = self.request.query_params.get('tag')
        if tag:
            queryset = queryset.filter(tags__slug=tag)
        
        # Поиск
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(content__icontains=search)
            )
        
        return queryset.select_related('author', 'category').prefetch_related('tags')
    
    @action(detail=True, methods=['post'])
    def increment_views(self, request, slug=None):
        """Увеличение счётчика просмотров"""
        article = self.get_object()
        article.view_count += 1
        article.save(update_fields=['view_count'])
        return Response({'view_count': article.view_count})
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Получить рекомендуемые статьи"""
        featured = self.queryset.filter(is_featured=True)[:5]
        serializer = self.get_serializer(featured, many=True)
        return Response(serializer.data)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для категорий (только чтение)"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для тегов (только чтение)"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    lookup_field = 'slug'

class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для комментариев"""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        article_slug = self.request.query_params.get('article')
        if article_slug:
            return Comment.objects.filter(article__slug=article_slug, is_approved=True)
        return Comment.objects.filter(is_approved=True)
    
    def perform_create(self, serializer):
        serializer.save(author_name=self.request.user.username if self.request.user.is_authenticated else 'Anonymous')
```

### Пример 8: URL-маршруты для API

```python
# blog/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'articles', api_views.ArticleViewSet, basename='article')
router.register(r'categories', api_views.CategoryViewSet, basename='category')
router.register(r'tags', api_views.TagViewSet, basename='tag')
router.register(r'comments', api_views.CommentViewSet, basename='comment')

urlpatterns = [
    path('api/', include(router.urls)),
]
```

---

## 4. Аутентификация в API

### Пример 9: Токен-аутентификация

```python
# Настройка токен-аутентификации

# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Создание токена для пользователя
from rest_framework.authtoken.models import Token

# Создать токен
token = Token.objects.create(user=user)

# Или автоматически при создании пользователя
# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
```

### Пример 10: JWT-аутентификация

```bash
pip install djangorestframework-simplejwt
```

```python
# settings.py

from datetime import timedelta

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': 'your-secret-key',
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
}

# urls.py
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
```

### Пример 11: Использование аутентификации

```python
# Пример запроса с токеном

# 1. Получение токена (POST)
# URL: /api/token/
# Body: {"username": "admin", "password": "password"}

# 2. Использование токена (заголовок)
# Headers: Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b

# Пример запроса с JWT
# Headers: Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

---

## 5. Документация API

### Пример 12: Swagger/OpenAPI с drf-spectacular

```bash
pip install drf-spectacular
```

```python
# settings.py

INSTALLED_APPS = [
    # ...
    'drf_spectacular',
]

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# urls.py

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]
```

---

## 6. Практические задания

### Задание 1: REST API для блога
Создайте REST API для системы блога:
- Статьи (CRUD)
- Категории
- Теги
- Комментарии

### Задание 2: Пагинация
Добавьте пагинацию к спискам ресурсов.

### Задание 3: Фильтрация и поиск
Реализуйте фильтрацию по категориям, тегам и поиск по названию.

### Задание 4: Аутентификация
Добавьте JWT-аутентификацию для создания и редактирования статей.

### Задание 5: Документация
Добавьте Swagger-документацию для API.

---

## Дополнительные задания

### Задание 6: Версионирование API
Реализуйте версионирование API (v1, v2).

### Задание 7: Rate Limiting
Добавьте ограничение количества запросов.

### Задание 8: Кэширование
Реализуйте кэширование часто запрашиваемых данных.

---

## Контрольные вопросы:
1. Что такое REST API?
2. Какие HTTP-методы используются в REST?
3. Чем отличаются PUT и PATCH?
4. Что такое сериализатор?
5. Что такое ViewSet?
6. Как реализовать аутентификацию в DRF?
7. Что такое JWT-токен?
8. Зачем нужна документация API?
