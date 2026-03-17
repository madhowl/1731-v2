# Практическое занятие 36: Django - основы

## Введение в Django

### Цель занятия:
Познакомиться с фреймворком Django, изучить его архитектуру, научиться создавать проекты и приложения, настраивать URL-маршрутизацию и использовать шаблоны.

### Задачи:
1. Установить и настроить Django
2. Создать проект и приложение
3. Настроить URL-маршрутизацию
4. Использовать шаблоны Django
5. Понять архитектуру MTV

### План работы:
1. Установка и настройка Django
2. Создание проекта
3. Структура проекта
4. URL-маршрутизация
5. Шаблоны
6. Практические задания

---

## 1. Установка и настройка Django

### Пример 1: Установка Django

```bash
# Установка Django через pip
pip install django

# Проверка установки
python -m django --version
```

### Пример 2: Создание нового проекта

```bash
# Создание проекта
django-admin startproject myproject

# Структура проекта:
# myproject/
# ├── manage.py
# ├── myproject/
# │   ├── __init__.py
# │   ├── settings.py
# │   ├── urls.py
# │   ├── asgi.py
# │   └── wsgi.py
```

### Пример 3: Запуск сервера разработки

```bash
cd myproject
python manage.py runserver

# Запуск на определённом порту
python manage.py runserver 8080

# Доступные команды
python manage.py help
```

---

## 2. Структура проекта Django

### Пример 4: Основной файл настроек (settings.py)

```python
# myproject/settings.py

import os
from pathlib import Path

# Базовая директория проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Секретный ключ (в продакшене хранить в переменных окружения)
SECRET_KEY = 'django-insecure-your-secret-key-here'

# Режим отладки
DEBUG = True

# Разрешённые хосты
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.example.com']

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
```

### Пример 5: Создание приложения

```bash
# Создание приложения blog
python manage.py startapp blog

# Структура приложения:
# blog/
# ├── __init__.py
# ├── admin.py
# ├── apps.py
# ├── models.py
# ├── tests.py
# ├── urls.py (нужно создать)
# └── views.py
```

### Пример 6: Регистрация приложения

```python
# myproject/settings.py

INSTALLED_APPS = [
    # ...
    'blog',  # Добавить в конец
]
```

---

## 3. URL-маршрутизация в Django

### Пример 7: Основной файл URL-конфигурации

```python
# myproject/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blog.urls')),  # Подключение URL-маршрутов блога
    path('shop/', include('shop.urls', namespace='shop')),
]

# Для медиа-файлов в режиме разработки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### Пример 8: URL-маршруты приложения

```python
# blog/urls.py

from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Главная страница блога
    path('', views.index, name='index'),
    
    # Просмотр статьи
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    
    # Список статей автора
    path('author/<int:author_id>/', views.author_posts, name='author_posts'),
    
    # Архив по дате
    path('archive/<int:year>/<int:month>/', views.archive, name='archive'),
    
    # Категория
    path('category/<slug:category_slug>/', views.category, name='category'),
]
```

### Пример 9: Именованные маршруты и обратные ссылки

```python
# blog/views.py

from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from .models import Post

def index(request):
    posts = Post.objects.all()
    return render(request, 'blog/index.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'blog/post_detail.html', {'post': post})

def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    # Обработка комментария
    return HttpResponseRedirect(reverse('blog:post_detail', args=[post_id]))

# В шаблоне:
# {% url 'blog:post_detail' post.id %}
# {% url 'blog:category' category.slug %}
```

---

## 4. Шаблоны Django

### Пример 10: Создание базового шаблона

```html
<!-- templates/base.html -->

<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Мой сайт{% endblock %}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; }
        header { background: #333; color: white; padding: 20px; }
        nav a { color: white; margin-right: 15px; text-decoration: none; }
        nav a:hover { text-decoration: underline; }
        main { padding: 20px; }
        footer { background: #f4f4f4; padding: 20px; text-align: center; }
        .container { max-width: 1200px; margin: 0 auto; }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>{% block header %}Мой блог{% endblock %}</h1>
            <nav>
                <a href="{% url 'blog:index' %}">Главная</a>
                <a href="{% url 'blog:category' 'technology' %}">Технологии</a>
                <a href="{% url 'blog:category' 'travel' %}">Путешествия</a>
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
</body>
</html>
```

### Пример 11: Наследование шаблонов

```html
<!-- templates/blog/index.html -->

{% extends 'base.html' %}

{% block title %}Главная страница - Мой блог{% endblock %}

{% block header %}Статьи{% endblock %}

{% block content %}
<div class="posts">
    {% for post in posts %}
        <article class="post">
            <h2>
                <a href="{% url 'blog:post_detail' post.id %}">{{ post.title }}</a>
            </h2>
            <p class="meta">
                Автор: {{ post.author.username }} | 
                Дата: {{ post.created_at|date:"d.m.Y" }}
            </p>
            <p>{{ post.excerpt }}</p>
            <a href="{% url 'blog:post_detail' post.id %}">Читать далее</a>
        </article>
    {% empty %}
        <p>Пока нет статей.</p>
    {% endfor %}
</div>

{% if is_paginated %}
<div class="pagination">
    {% if page_obj.has_previous %}
        <a href="?page=1">Первая</a>
        <a href="?page={{ page_obj.previous_page_number }}">Предыдущая</a>
    {% endif %}
    
    <span>Страница {{ page_obj.number }} из {{ page_obj.paginator.num_pages }}</span>
    
    {% if page_obj.has_next %}
        <a href="?page={{ page_obj.next_page_number }}">Следующая</a>
        <a href="?page={{ page_obj.paginator.num_pages }}">Последняя</a>
    {% endif %}
</div>
{% endif %}
{% endblock %}
```

### Пример 12: Теги шаблонов

```html
<!-- templates/blog/post_detail.html -->

{% extends 'base.html' %}
{% load static %}

{% block title %}{{ post.title }}{% endblock %}

{% block content %}
<article>
    <h1>{{ post.title }}</h1>
    
    <div class="post-meta">
        <img src="{{ post.author.avatar.url }}" alt="{{ post.author.username }}">
        <span>Автор: {{ post.author.get_full_name|default:post.author.username }}</span>
        <span>Дата: {{ post.created_at|date:"d F Y" }}</span>
        <span>Просмотров: {{ post.view_count }}</span>
    </div>
    
    <div class="post-content">
        {{ post.content|linebreaks }}
    </div>
    
    <div class="tags">
        Теги:
        {% for tag in post.tags.all %}
            <a href="{% url 'blog:tag' tag.slug %}" class="tag">{{ tag.name }}</a>
            {% if not forloop.last %}, {% endif %}
        {% empty %}
            нет
        {% endfor %}
    </div>
    
    <div class="related-posts">
        <h3>Похожие статьи</h3>
        <ul>
        {% for related in post.get_related %}
            <li><a href="{% url 'blog:post_detail' related.id %}">{{ related.title }}</a></li>
        {% endfor %}
        </ul>
    </div>
</article>
{% endblock %}
```

### Пример 13: Фильтры шаблонов

```html
<!-- Примеры использования фильтров -->

<!-- Форматирование даты -->
{{ post.created_at|date:"d.m.Y H:i" }}

<!-- Ограничение длины текста -->
{{ post.content|truncatewords:50 }}
{{ post.content|truncatechars:200 }}

<!-- Верхний/нижний регистр -->
{{ post.title|upper }}
{{ post.title|lower }}
{{ post.title|title }}

<!-- Срез -->
{{ post.title|slice:":10" }}

<!-- Условия -->
{{ post.is_published|yesno:"Да,Нет" }}

<!-- Сумма -->
{{ total|default:"0" }}

<!-- Сложные фильтры -->
{{ post.content|linebreaks|truncatewords:100 }}
```

---

## 5. Представления (Views)

### Пример 14: Функциональные представления

```python
# blog/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.template.loader import render_to_string
from .models import Post, Category, Tag
from django.core.paginator import Paginator

# Простое представление
def index(request):
    posts_list = Post.objects.filter(is_published=True).order_by('-created_at')
    paginator = Paginator(posts_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blog/index.html', {
        'posts': page_obj,
        'page_obj': page_obj,
    })

# Представление с параметрами
def post_detail(request, post_id):
    post = get_object_or_404(
        Post.objects.filter(is_published=True),
        id=post_id
    )
    
    # Увеличение счётчика просмотров
    post.view_count += 1
    post.save(update_fields=['view_count'])
    
    return render(request, 'blog/post_detail.html', {'post': post})

# Представление с фильтрацией
def category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    posts = Post.objects.filter(
        category=category,
        is_published=True
    ).order_by('-created_at')
    
    return render(request, 'blog/category.html', {
        'category': category,
        'posts': posts,
    })

# Обработка форм
def search(request):
    query = request.GET.get('q', '')
    posts = []
    
    if query:
        posts = Post.objects.filter(
            title__icontains=query,
            is_published=True
        )
    
    return render(request, 'blog/search.html', {
        'query': query,
        'posts': posts,
    })

# API-представление (JSON)
def api_posts(request):
    posts = Post.objects.filter(is_published=True)[:10]
    data = [{
        'id': p.id,
        'title': p.title,
        'slug': p.slug,
        'created_at': p.created_at.isoformat(),
    } for p in posts]
    return JsonResponse({'posts': data})
```

### Пример 15: Обработка ошибок

```python
# blog/views.py

from django.shortcuts import render
from django.http import Http404

def custom_404(request, exception):
    return render(request, 'errors/404.html', status=404)

def custom_500(request):
    return render(request, 'errors/500.html', status=500)

# myproject/urls.py
handler404 = 'myproject.views.custom_404'
handler500 = 'myproject.views.custom_500'
```

---

## 6. Практические задания

### Задание 1: Создание простого блога
Создайте простое приложение блога:
- Модель Article с заголовком, содержанием, датой
- Представления для списка и детальной статьи
- Шаблоны для отображения

### Задание 2: Категории и теги
Расширьте блог:
- Добавьте модель Category
- Добавьте модель Tag
- Реализуйте фильтрацию по категориям и тегам

### Задание 3: Пагинация
Добавьте постраничное отображение статей.

### Задание 4: Поиск
Реализуйте поиск по заголовкам и содержанию статей.

### Задание 5: RSS-лента
Создайте RSS-ленту для статей.

---

## Дополнительные задания

### Задание 6: Архив статей
Создайте страницу архива статей с группировкой по месяцам.

### Задание 7: Статистика
Добавьте страницу со статистикой блога (количество статей, авторов, просмотров).

### Задание 8: API
Создайте JSON API для получения списка статей.

---

## Контрольные вопросы:
1. Что такое Django и какие преимущества он даёт?
2. Какова структура проекта Django?
3. Что такое MTV-архитектура Django?
4. Как создать приложение в Django?
5. Как настроить URL-маршрутизацию?
6. Как работает система шаблонов Django?
7. Что такое наследование шаблонов?
8. Как передать данные из представления в шаблон?
