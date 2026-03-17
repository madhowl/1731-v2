# -*- coding: utf-8 -*-
"""
Практическое занятие 38: Разработка REST API
Решение упражнений

В этом файле представлены решения для всех упражнений практического занятия
по разработке REST API.

Для запуска (Flask):
    pip install flask flask-restful flask-cors
    python practical_38_rest_api_development_solution.py

Для запуска (Django):
    pip install djangorestframework
    # Требуется Django проект
"""

import os
from flask import Flask, request, jsonify, abort
from flask_cors import CORS

# ============================================================================
# Упражнение 1: REST API на чистом Flask
# ============================================================================

app = Flask(__name__)
CORS(app)  # Разрешение CORS для фронтенда

# Имитация базы данных (в памяти)
articles = []
next_id = 1

# Имитация базы данных пользователей
users = []
next_user_id = 1

# ============================================================================
# Маршруты для статей (CRUD)
# ============================================================================

@app.route('/api/articles', methods=['GET'])
def get_articles():
    """Получить все статьи"""
    return jsonify({
        'articles': articles,
        'count': len(articles)
    })


@app.route('/api/articles/<int:article_id>', methods=['GET'])
def get_article(article_id):
    """Получить статью по ID"""
    article = next((a for a in articles if a['id'] == article_id), None)
    if article is None:
        abort(404, description="Статья не найдена")
    return jsonify(article)


@app.route('/api/articles', methods=['POST'])
def create_article():
    """Создать статью"""
    global next_id
    
    if not request.json:
        abort(400, description="Данные не в формате JSON")
    
    required_fields = ['title', 'content']
    for field in required_fields:
        if field not in request.json:
            abort(400, description=f"Поле {field} обязательно")
    
    article = {
        'id': next_id,
        'title': request.json['title'],
        'content': request.json['content'],
        'author': request.json.get('author', 'anonymous'),
        'tags': request.json.get('tags', []),
        'created_at': None
    }
    next_id += 1
    articles.append(article)
    
    return jsonify(article), 201


@app.route('/api/articles/<int:article_id>', methods=['PUT'])
def update_article(article_id):
    """Обновить статью полностью"""
    global articles
    
    article = next((a for a in articles if a['id'] == article_id), None)
    if article is None:
        abort(404, description="Статья не найдена")
    
    if not request.json:
        abort(400, description="Данные не в формате JSON")
    
    article['title'] = request.json.get('title', article['title'])
    article['content'] = request.json.get('content', article['content'])
    article['author'] = request.json.get('author', article['author'])
    article['tags'] = request.json.get('tags', article['tags'])
    
    return jsonify(article)


@app.route('/api/articles/<int:article_id>', methods=['PATCH'])
def patch_article(article_id):
    """Частичное обновление статьи"""
    article = next((a for a in articles if a['id'] == article_id), None)
    if article is None:
        abort(404, description="Статья не найдена")
    
    if not request.json:
        abort(400, description="Данные не в формате JSON")
    
    for key, value in request.json.items():
        if key in article:
            article[key] = value
    
    return jsonify(article)


@app.route('/api/articles/<int:article_id>', methods=['DELETE'])
def delete_article(article_id):
    """Удалить статью"""
    global articles
    
    article = next((a for a in articles if a['id'] == article_id), None)
    if article is None:
        abort(404, description="Статья не найдена")
    
    articles = [a for a in articles if a['id'] != article_id]
    
    return '', 204


# ============================================================================
# Маршруты для пользователей (CRUD)
# ============================================================================

@app.route('/api/users', methods=['GET'])
def get_users():
    """Получить всех пользователей"""
    return jsonify({
        'users': users,
        'count': len(users)
    })


@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Получить пользователя по ID"""
    user = next((u for u in users if u['id'] == user_id), None)
    if user is None:
        abort(404, description="Пользователь не найден")
    return jsonify(user)


@app.route('/api/users', methods=['POST'])
def create_user():
    """Создать пользователя"""
    global next_user_id
    
    if not request.json:
        abort(400, description="Данные не в формате JSON")
    
    required_fields = ['username', 'email']
    for field in required_fields:
        if field not in request.json:
            abort(400, description=f"Поле {field} обязательно")
    
    # Проверка уникальности
    for user in users:
        if user['username'] == request.json['username']:
            abort(400, description="Имя пользователя уже занято")
        if user['email'] == request.json['email']:
            abort(400, description="Email уже используется")
    
    user = {
        'id': next_user_id,
        'username': request.json['username'],
        'email': request.json['email'],
        'bio': request.json.get('bio', '')
    }
    next_user_id += 1
    users.append(user)
    
    return jsonify(user), 201


@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Обновить пользователя"""
    global users
    
    user = next((u for u in users if u['id'] == user_id), None)
    if user is None:
        abort(404, description="Пользователь не найден")
    
    if not request.json:
        abort(400, description="Данные не в формате JSON")
    
    user['username'] = request.json.get('username', user['username'])
    user['email'] = request.json.get('email', user['email'])
    user['bio'] = request.json.get('bio', user['bio'])
    
    return jsonify(user)


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Удалить пользователя"""
    global users
    
    user = next((u for u in users if u['id'] == user_id), None)
    if user is None:
        abort(404, description="Пользователь не найден")
    
    users = [u for u in users if u['id'] != user_id]
    
    return '', 204


# ============================================================================
# Вложенные ресурсы
# ============================================================================

@app.route('/api/users/<int:user_id>/articles', methods=['GET'])
def get_user_articles(user_id):
    """Получить статьи пользователя"""
    user = next((u for u in users if u['id'] == user_id), None)
    if user is None:
        abort(404, description="Пользователь не найден")
    
    user_articles = [a for a in articles if a.get('author') == user['username']]
    
    return jsonify({
        'user': user,
        'articles': user_articles,
        'count': len(user_articles)
    })


# ============================================================================
# Пагинация
# ============================================================================

@app.route('/api/articles/paginated', methods=['GET'])
def get_articles_paginated():
    """Получить статьи с пагинацией"""
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 5))
    
    start = (page - 1) * per_page
    end = start + per_page
    
    total = len(articles)
    total_pages = (total + per_page - 1) // per_page
    
    return jsonify({
        'articles': articles[start:end],
        'count': total,
        'page': page,
        'per_page': per_page,
        'total_pages': total_pages,
        'next': f'/api/articles/paginated?page={page + 1}' if page < total_pages else None,
        'previous': f'/api/articles/paginated?page={page - 1}' if page > 1 else None
    })


# ============================================================================
# Поиск и фильтрация
# ============================================================================

@app.route('/api/articles/search', methods=['GET'])
def search_articles():
    """Поиск статей"""
    query = request.args.get('q', '').lower()
    tag = request.args.get('tag', None)
    author = request.args.get('author', None)
    
    results = articles
    
    if query:
        results = [a for a in results 
                   if query in a['title'].lower() or query in a['content'].lower()]
    
    if tag:
        results = [a for a in results if tag in a.get('tags', [])]
    
    if author:
        results = [a for a in results if a.get('author', '').lower() == author.lower()]
    
    return jsonify({
        'articles': results,
        'count': len(results),
        'query': query
    })


# ============================================================================
# Обработка ошибок
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': str(error.description)}), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': str(error.description)}), 400


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Внутренняя ошибка сервера'}), 500


# ============================================================================
# Главная страница
# ============================================================================

@app.route('/')
def index():
    """Главная страница с документацией API"""
    return jsonify({
        'name': 'REST API',
        'version': '1.0',
        'description': 'API для управления статьями и пользователями',
        'endpoints': {
            'articles': {
                'GET /api/articles': 'Получить все статьи',
                'GET /api/articles/<id>': 'Получить статью по ID',
                'POST /api/articles': 'Создать статью',
                'PUT /api/articles/<id>': 'Обновить статью полностью',
                'PATCH /api/articles/<id>': 'Частично обновить статью',
                'DELETE /api/articles/<id>': 'Удалить статью',
                'GET /api/articles/paginated': 'Статьи с пагинацией',
                'GET /api/articles/search': 'Поиск статей',
            },
            'users': {
                'GET /api/users': 'Получить всех пользователей',
                'GET /api/users/<id>': 'Получить пользователя по ID',
                'POST /api/users': 'Создать пользователя',
                'PUT /api/users/<id>': 'Обновить пользователя',
                'DELETE /api/users/<id>': 'Удалить пользователя',
                'GET /api/users/<id>/articles': 'Статьи пользователя',
            }
        }
    })


# ============================================================================
# Упражнение 2: Django REST Framework (примеры кода)
# ============================================================================

DJANGO_REST_FRAMEWORK_EXAMPLES = '''
# === Настройка Django REST Framework ===

# Установка
pip install djangorestframework

# settings.py
INSTALLED_APPS = [
    ...
    'rest_framework',
]

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
}


# === Сериализаторы ===

# blog/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Article, Category, Tag, Comment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']


class CategorySerializer(serializers.ModelSerializer):
    article_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'article_count']
    
    def get_article_count(self, obj):
        return obj.articles.count()


class ArticleListSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    
    class Meta:
        model = Article
        fields = ['id', 'title', 'slug', 'excerpt', 'author', 'category', 
                  'tags', 'view_count', 'published_at', 'created_at']


class ArticleDetailSerializer(serializers.ModelSerializer):
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
        comments = obj.comments.filter(is_approved=True)
        return CommentSerializer(comments, many=True).data


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'author_name', 'author_email', 'content', 'created_at']


# === ViewSets ===

# blog/api_views.py

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.db.models import Q
from .models import Article, Category, Tag
from .serializers import (
    ArticleListSerializer, ArticleDetailSerializer, 
    CategorySerializer, TagSerializer
)


class ArticleViewSet(viewsets.ModelViewSet):
    """ViewSet для статей"""
    queryset = Article.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ArticleListSerializer
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


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для тегов (только чтение)"""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


# === URL-маршруты ===

# blog/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import ArticleViewSet, CategoryViewSet, TagViewSet

router = DefaultRouter()
router.register(r'articles', ArticleViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'tags', TagViewSet)

urlpatterns = [
    path('', include(router.urls)),
]


# === Аутентификация в DRF ===

# В views.py
from rest_framework.permissions import IsAuthenticated

class ProtectedViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    ...


# === Пагинация ===

# custom pagination
from rest_framework.pagination import PageNumberPagination

class LargeResultsSetPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = 'page_size'
    max_page_size = 10000

class ArticleViewSet(viewsets.ModelViewSet):
    pagination_class = LargeResultsSetPagination
    ...
'''

# ============================================================================
# Упражнение 3: Flask-RESTful (примеры кода)
# ============================================================================

FLASK_RESTFUL_EXAMPLES = '''
# === Flask-RESTful ===

pip install flask-restful

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
article_parser.add_argument('tags', type=str, action='split')

# Имитация базы данных
articles = {}
next_id = 1


class ArticleListResource(Resource):
    def get(self):
        return {'articles': list(articles.values()), 'count': len(articles)}
    
    def post(self):
        global next_id
        args = article_parser.parse_args()
        article = {
            'id': next_id,
            'title': args['title'],
            'content': args['content'],
            'author': args['author'],
            'tags': args['tags'] or []
        }
        articles[next_id] = article
        next_id += 1
        return article, 201


class ArticleResource(Resource):
    def get(self, article_id):
        if article_id not in articles:
            abort(404, message="Статья не найдена")
        return articles[article_id]
    
    def put(self, article_id):
        if article_id not in articles:
            abort(404, message="Статья не найдена")
        
        args = article_parser.parse_args()
        articles[article_id].update({
            'title': args['title'],
            'content': args['content'],
            'author': args['author'],
            'tags': args['tags'] or []
        })
        return articles[article_id]
    
    def delete(self, article_id):
        if article_id not in articles:
            abort(404, message="Статья не найдена")
        
        del articles[article_id]
        return '', 204


# Регистрация маршрутов
api.add_resource(ArticleListResource, '/api/articles')
api.add_resource(ArticleResource, '/api/articles/<int:article_id>')


if __name__ == '__main__':
    app.run(debug=True)
'''

# ============================================================================
# Вывод информации
# ============================================================================

def main():
    """Вывод информации о REST API"""
    print("=" * 70)
    print("Практическое занятие 38: REST API Development")
    print("=" * 70)
    print()
    print("Flask REST API запущен!")
    print("Откройте: http://127.0.0.1:5000/")
    print()
    print("Доступные endpoints:")
    print("  GET    /api/articles          - Все статьи")
    print("  GET    /api/articles/<id>    - Статья по ID")
    print("  POST   /api/articles         - Создать статью")
    print("  PUT    /api/articles/<id>    - Обновить статью")
    print("  PATCH  /api/articles/<id>   - Частичное обновление")
    print("  DELETE /api/articles/<id>   - Удалить статью")
    print()
    print("  GET    /api/users            - Все пользователи")
    print("  GET    /api/users/<id>       - Пользователь по ID")
    print("  POST   /api/users           - Создать пользователя")
    print()
    print("  GET    /api/articles/paginated?page=1&per_page=5 - Пагинация")
    print("  GET    /api/articles/search?q=python              - Поиск")
    print("=" * 70)


if __name__ == '__main__':
    main()
    app.run(debug=True, port=5000)
