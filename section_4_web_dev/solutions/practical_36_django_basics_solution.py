# -*- coding: utf-8 -*-
"""
Практическое занятие 36: Django - основы
Решение упражнений

В этом файле представлены решения для всех упражнений практического занятия
по основам Django.

Примечание: Для запуска этого кода требуется Django проект.
Данный файл демонстрирует структуру и компоненты Django.

Для изучения:
    - Структура Django проекта
    - URL-маршрутизация
    - Шаблоны Django
    - MTV архитектура
"""

# ============================================================================
# Упражнение 1: Конфигурация Django проекта
# ============================================================================

# Пример файла settings.py для Django проекта

DJANGO_SETTINGS_EXAMPLE = '''
# myproject/settings.py

import os
from pathlib import Path

# Базовая директория проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Секретный ключ
SECRET_KEY = 'django-insecure-your-secret-key-here-change-in-production'

# Режим отладки
DEBUG = True

# Разрешённые хосты
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Установленные приложения
INSTALLED_APPS = [
    'django.contrib.admin',          # Админ-панель
    'django.contrib.auth',           # Система аутентификации
    'django.contrib.contenttypes',   # Типы контента
    'django.contrib.sessions',       # Сессии
    'django.contrib.messages',       # Сообщения
    'django.contrib.staticfiles',   # Статические файлы
    # Свои приложения
    'blog',
    'shop',
]

# Промежуточное ПО (middleware)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Корневой URL-конфигурация
ROOT_URLCONF = 'myproject.urls'

# Шаблоны
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI-приложение
WSGI_APPLICATION = 'myproject.wsgi.application'

# База данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Пароли и авторизация
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Интернационализация
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# Статические файлы
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

# Медиа-файлы
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Автоматическое поле для первичного ключа
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
'''


# ============================================================================
# Упражнение 2: URL-маршрутизация в Django
# ============================================================================

# Пример главного файла URL конфигурации

MAIN_URLS_EXAMPLE = '''
# myproject/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls', namespace='blog')),
    path('shop/', include('shop.urls', namespace='shop')),
    path('api/', include('api.urls')),
]

# Для медиа-файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
'''

# Пример URL-маршрутов приложения

BLOG_URLS_EXAMPLE = '''
# blog/urls.py

from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Главная страница блога
    path('', views.index, name='index'),
    
    # Просмотр статьи
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    
    # Просмотр статьи по slug
    path('article/<slug:slug>/', views.article_detail, name='article_detail'),
    
    # Список статей автора
    path('author/<int:author_id>/', views.author_posts, name='author_posts'),
    
    # Архив по дате
    path('archive/<int:year>/<int:month>/', views.archive, name='archive'),
    
    # Категория
    path('category/<slug:category_slug>/', views.category, name='category'),
    
    # Тег
    path('tag/<slug:tag_slug>/', views.tag_articles, name='tag'),
    
    # Поиск
    path('search/', views.search, name='search'),
    
    # RSS лента
    path('feed/', views.rss_feed, name='feed'),
]
'''


# ============================================================================
# Упражнение 3: Представления (Views)
# ============================================================================

# Пример функциональных представлений

FUNCTIONAL_VIEWS_EXAMPLE = '''
# blog/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse, Http404
from django.template.loader import render_to_string
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from .models import Post, Category, Tag, Author


def index(request):
    """Главная страница блога"""
    # Получаем все опубликованные посты
    posts_list = Post.objects.filter(is_published=True).order_by('-created_at')
    
    # Пагинация
    paginator = Paginator(posts_list, 10)
    page = request.GET.get('page')
    
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    
    return render(request, 'blog/index.html', {
        'posts': posts,
        'page': page,
    })


def post_detail(request, post_id):
    """Детальная страница поста"""
    post = get_object_or_404(Post, id=post_id)
    
    # Увеличиваем счётчик просмотров
    post.views += 1
    post.save(update_fields=['views'])
    
    # Похожие посты
    similar_posts = Post.objects.filter(
        category=post.category,
        is_published=True
    ).exclude(id=post.id)[:3]
    
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'similar_posts': similar_posts,
    })


def article_detail(request, slug):
    """Детальная страница поста по slug"""
    post = get_object_or_404(Post, slug=slug, is_published=True)
    return render(request, 'blog/post_detail.html', {'post': post})


def category_posts(request, slug):
    """Посты категории"""
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(
        category=category,
        is_published=True
    ).order_by('-created_at')
    
    return render(request, 'blog/category.html', {
        'category': category,
        'posts': posts,
    })


def author_posts(request, author_id):
    """Посты автора"""
    author = get_object_or_404(Author, id=author_id)
    posts = Post.objects.filter(
        author=author,
        is_published=True
    ).order_by('-created_at')
    
    return render(request, 'blog/author.html', {
        'author': author,
        'posts': posts,
    })


def archive(request, year, month):
    """Архив по дате"""
    from datetime import datetime
    from django.utils import timezone
    
    # Получаем посты за указанный месяц
    posts = Post.objects.filter(
        created_at__year=year,
        created_at__month=month,
        is_published=True
    ).order_by('-created_at')
    
    return render(request, 'blog/archive.html', {
        'year': year,
        'month': month,
        'posts': posts,
    })


def search(request):
    """Поиск постов"""
    query = request.GET.get('q', '')
    
    if query:
        posts = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query),
            is_published=True
        ).order_by('-created_at')
    else:
        posts = []
    
    return render(request, 'blog/search.html', {
        'query': query,
        'posts': posts,
    })


def tag_articles(request, slug):
    """Статьи по тегу"""
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(
        tags=tag,
        is_published=True
    ).order_by('-created_at')
    
    return render(request, 'blog/tag.html', {
        'tag': tag,
        'posts': posts,
    })
'''


# ============================================================================
# Упражнение 4: Шаблоны Django
# ============================================================================

# Пример базового шаблона

BASE_TEMPLATE_EXAMPLE = '''
<!-- templates/base.html -->

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Мой сайт{% endblock %}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; line-height: 1.6; }
        header { background: #333; color: white; padding: 1rem; }
        nav a { color: white; margin-right: 15px; text-decoration: none; }
        nav a:hover { text-decoration: underline; }
        main { padding: 20px; max-width: 1200px; margin: 0 auto; }
        footer { background: #f4f4f4; padding: 20px; text-align: center; }
        .container { max-width: 1200px; margin: 0 auto; }
    </style>
    {% block extra_css %}{% endblock %}
</head>
<body>
    <header>
        <div class="container">
            <h1>{% block header %}Мой блог{% endblock %}</h1>
            <nav>
                <a href="{% url 'blog:index' %}">Главная</a>
                <a href="{% url 'blog:category' 'technology' %}">Технологии</a>
                <a href="{% url 'blog:category' 'travel' %}">Путешествия</a>
                <a href="{% url 'blog:search' %}">Поиск</a>
            </nav>
        </div>
    </header>
    
    <main>
        <div class="container">
            {% block content %}
            <p>Добро пожаловать на сайт!</p>
            {% endblock %}
        </div>
    </main>
    
    <footer>
        <div class="container">
            <p>&copy; 2024 Мой блог. Все права защищены.</p>
        </div>
    </footer>
    
    {% block extra_js %}{% endblock %}
</body>
</html>
'''

# Пример шаблона списка постов

POST_LIST_TEMPLATE_EXAMPLE = '''
<!-- templates/blog/index.html -->

{% extends 'base.html' %}

{% block title %}Главная страница - Мой блог{% endblock %}

{% block header %}Статьи{% endblock %}

{% block content %}
<div class="posts">
    {% for post in posts %}
        <article class="post" style="margin-bottom: 30px; padding: 20px; border: 1px solid #ddd;">
            <h2>
                <a href="{% url 'blog:post_detail' post.id %}" style="text-decoration: none; color: #333;">
                    {{ post.title }}
                </a>
            </h2>
            
            <div class="post-meta" style="color: #666; font-size: 14px;">
                <span>Автор: {{ post.author.username }}</span> |
                <span>Дата: {{ post.created_at|date:"d.m.Y" }}</span> |
                <span>Категория: <a href="{% url 'blog:category' post.category.slug %}">{{ post.category.name }}</a></span> |
                <span>Просмотров: {{ post.views }}</span>
            </div>
            
            <p class="excerpt" style="margin-top: 10px;">
                {{ post.excerpt|truncatewords:50 }}
            </p>
            
            <a href="{% url 'blog:post_detail' post.id %}" style="color: #007bff;">
                Читать далее →
            </a>
            
            {% if post.tags.all %}
            <div class="tags" style="margin-top: 10px;">
                Теги:
                {% for tag in post.tags.all %}
                    <a href="{% url 'blog:tag' tag.slug %}" style="margin-right: 5px;">{{ tag.name }}</a>
                {% endfor %}
            </div>
            {% endif %}
        </article>
    {% empty %}
        <p>Пока нет статей.</p>
    {% endfor %}
</div>

<!-- Пагинация -->
{% if posts.has_other_pages %}
<div class="pagination" style="margin-top: 20px;">
    {% if posts.has_previous %}
        <a href="?page=1">Первая</a>
        <a href="?page={{ posts.previous_page_number }}">Предыдущая</a>
    {% endif %}
    
    <span>Страница {{ posts.number }} из {{ posts.paginator.num_pages }}</span>
    
    {% if posts.has_next %}
        <a href="?page={{ posts.next_page_number }}">Следующая</a>
        <a href="?page={{ posts.paginator.num_pages }}">Последняя</a>
    {% endif %}
</div>
{% endif %}
{% endblock %}
'''

# Пример шаблона детальной страницы

POST_DETAIL_TEMPLATE_EXAMPLE = '''
<!-- templates/blog/post_detail.html -->

{% extends 'base.html' %}

{% block title %}{{ post.title }}{% endblock %}

{% block content %}
<article>
    <h1>{{ post.title }}</h1>
    
    <div class="post-meta" style="color: #666; margin: 20px 0;">
        <img src="{{ post.author.avatar.url|default:'/static/default-avatar.png' }}" 
             alt="{{ post.author.username }}" 
             style="width: 50px; height: 50px; border-radius: 50%;">
        <span>Автор: {{ post.author.get_full_name|default:post.author.username }}</span>
        <span>Дата: {{ post.created_at|date:"d F Y" }}</span>
        <span>Просмотров: {{ post.views }}</span>
    </div>
    
    {% if post.image %}
    <img src="{{ post.image.url }}" alt="{{ post.title }}" style="max-width: 100%;">
    {% endif %}
    
    <div class="post-content" style="margin: 30px 0; line-height: 1.8;">
        {{ post.content|linebreaks }}
    </div>
    
    {% if post.tags.all %}
    <div class="tags" style="margin: 20px 0;">
        <strong>Теги:</strong>
        {% for tag in post.tags.all %}
            <a href="{% url 'blog:tag' tag.slug %}" 
               style="background: #eee; padding: 5px 10px; margin-right: 5px; text-decoration: none;">
                {{ tag.name }}
            </a>
        {% endfor %}
    </div>
    {% endif %}
    
    <!-- Похожие статьи -->
    {% if similar_posts %}
    <div class="related-posts" style="margin-top: 40px;">
        <h3>Похожие статьи</h3>
        <ul>
        {% for similar in similar_posts %}
            <li><a href="{% url 'blog:post_detail' similar.id %}">{{ similar.title }}</a></li>
        {% endfor %}
        </ul>
    </div>
    {% endif %}
    
    <!-- Комментарии -->
    <div class="comments" style="margin-top: 40px;">
        <h3>Комментарии ({{ post.comments.count }})</h3>
        
        {% for comment in post.comments.all %}
        <div class="comment" style="margin: 20px 0; padding: 15px; background: #f9f9f9;">
            <strong>{{ comment.author_name }}</strong>
            <span style="color: #666; font-size: 12px;">{{ comment.created_at|date:"d.m.Y H:i" }}</span>
            <p>{{ comment.content }}</p>
        </div>
        {% endfor %}
        
        <!-- Форма комментария -->
        <h4>Оставить комментарий</h4>
        <form method="post" action="{% url 'blog:add_comment' post.id %}">
            {% csrf_token %}
            <input type="text" name="author_name" placeholder="Ваше имя" required>
            <input type="email" name="author_email" placeholder="Email" required>
            <textarea name="content" placeholder="Комментарий" rows="4" required></textarea>
            <button type="submit">Отправить</button>
        </form>
    </div>
</article>
{% endblock %}
'''

# ============================================================================
# Упражнение 5: Теги и фильтры шаблонов
# ============================================================================

TEMPLATE_TAGS_EXAMPLE = '''
<!-- Примеры использования тегов шаблонов -->

<!-- Цикл for -->
{% for item in items %}
    {{ forloop.counter }}. {{ item.name }}
{% empty %}
    Нет элементов
{% endfor %}

<!-- Условие if -->
{% if user.is_authenticated %}
    Привет, {{ user.username }}!
{% else %}
    <a href="/login/">Войти</a>
{% endif %}

<!-- Тег with -->
{% with total=items.count %}
    Всего элементов: {{ total }}
{% endwith %}

<!-- Тег include -->
{% include 'partials/menu.html' %}

<!-- Тег block и extends -->
{% extends 'base.html' %}
{% block content %}
    Контент
{% endblock %}

<!-- Фильтры -->
{{ post.title|upper }}
{{ post.title|lower }}
{{ post.title|title }}
{{ post.content|truncatewords:50 }}
{{ post.content|truncatechars:200 }}
{{ post.created_at|date:"d.m.Y H:i" }}
{{ price|currency:"руб" }}
{{ items|join:", " }}
{{ value|default:"Нет данных" }}
{{ text|escape|linebreaks }}
'''

# ============================================================================
# Упражнение 6: Модели Django (краткий обзор)
# ============================================================================

MODELS_EXAMPLE = '''
# blog/models.py

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User


class Category(models.Model):
    """Модель категории"""
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Post(models.Model):
    """Модель поста"""
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    content = models.TextField()
    excerpt = models.CharField(max_length=300, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    tags = models.ManyToManyField('Tag', blank=True)
    image = models.ImageField(upload_to='posts/%Y/%m/%d/', blank=True)
    is_published = models.BooleanField(default=False)
    views = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_published']),
        ]
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'id': self.id})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Tag(models.Model):
    """Модель тега"""
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('blog:tag', kwargs={'slug': self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Comment(models.Model):
    """Модель комментария"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author_name = models.CharField(max_length=100)
    author_email = models.EmailField()
    content = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Комментарий от {self.author_name}"
'''


# ============================================================================
# Упражнение 7: Admin-интерфейс
# ============================================================================

ADMIN_EXAMPLE = '''
# blog/admin.py

from django.contrib import admin
from .models import Category, Post, Tag, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'description']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'is_published', 'views', 'created_at']
    list_filter = ['is_published', 'category', 'created_at', 'tags']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Основное', {
            'fields': ('title', 'slug', 'content', 'excerpt', 'image')
        }),
        ('Метаданные', {
            'fields': ('author', 'category', 'tags', 'is_published')
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'post', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['author_name', 'content']
    actions = ['approve_comments', 'disapprove_comments']
    
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
    approve_comments.short_description = 'Одобрить выбранные комментарии'
    
    def disapprove_comments(self, request, queryset):
        queryset.update(is_approved=False)
    disapprove_comments.short_description = 'Отклонить выбранные комментарии'
'''


# ============================================================================
# Упражнение 8: Управление Django через manage.py
# ============================================================================

MANAGE_PY_COMMANDS = '''
# Основные команды Django

# Создание нового проекта
django-admin startproject myproject

# Создание нового приложения
python manage.py startapp blog

# Запуск сервера разработки
python manage.py runserver
python manage.py runserver 8080

# Создание миграций
python manage.py makemigrations
python manage.py makemigrations blog

# Применение миграций
python manage.py migrate

# Создание суперпользователя
python manage.py createsuperuser

# Сбор статических файлов
python manage.py collectstatic

# Проверка проекта
python manage.py check

# Открытие оболочки Django
python manage.py shell

# Создание дампа базы данных
python manage.py dumpdata blog > blog.json

# Загрузка данных
python manage.py loaddata blog.json
'''


# ============================================================================
# Итоговый пример: Простой Django проект
# ============================================================================

# Структура файлов простого Django проекта:

DJANGO_PROJECT_STRUCTURE = '''
myproject/
├── manage.py
├── myproject/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── blog/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
│   └── migrations/
│       └── __init__.py
└── templates/
    ├── base.html
    └── blog/
        ├── index.html
        ├── post_detail.html
        └── ...
'''

# ============================================================================
# Вывод информации о Django
# ============================================================================

def main():
    """Вывод информации о Django"""
    print("=" * 70)
    print("Практическое занятие 36: Django - основы")
    print("=" * 70)
    print()
    print("Структура Django проекта:")
    print(DJANGO_PROJECT_STRUCTURE)
    print()
    print("Основные команды:")
    print(MANAGE_PY_COMMANDS)
    print()
    print("=" * 70)
    print("Для запуска Django проекта:")
    print("1. pip install django")
    print("2. django-admin startproject myproject")
    print("3. cd myproject && python manage.py startapp blog")
    print("4. Настройте settings.py и создайте модели")
    print("5. python manage.py migrate")
    print("6. python manage.py runserver")
    print("=" * 70)


if __name__ == '__main__':
    main()
