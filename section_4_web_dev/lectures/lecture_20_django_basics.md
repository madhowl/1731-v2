# Лекция 20: Django - основы

## Установка, структура проекта, административная панель

### Цель лекции:
- Познакомиться с фреймворком Django
- Изучить структуру Django-проекта
- Освоить работу с административной панелью

### План лекции:
1. Установка Django
2. Создание проекта
3. Структура Django-проекта
4. Административная панель

---

## 1. Установка Django

Django — высокопроизводительный веб-фреймворк для быстрой разработки безопасных и поддерживаемых веб-приложений.

### Установка через pip:
```bash
pip install django
```

### Проверка установки:
```python
import django
print(django.get_version())
```

### Создание нового проекта:
```bash
django-admin startproject mysite
```

### Запуск веб-сервера:
```bash
cd mysite
python manage.py runserver
```

### Основные особенности Django:
- "Все включено" (batteries included)
- ORM (объектно-реляционное отображение)
- Административный интерфейс
- Система аутентификации
- Защита от многих видов атак

---

## 2. Создание проекта

### Структура проекта после создания:
```
mysite/
    manage.py
    mysite/
        __init__.py
        settings.py
        urls.py
        wsgi.py
        asgi.py
```

### Основные файлы:
- `manage.py` - утилита командной строки для управления проектом
- `settings.py` - настройки проекта
- `urls.py` - определяет сопоставления URL
- `wsgi.py` - точка входа для WSGI-совместимых веб-серверов

### Создание приложения:
```bash
python manage.py startapp polls
```

### Структура приложения:
```
polls/
    __init__.py
    admin.py
    apps.py
    models.py
    tests.py
    views.py
    migrations/
        __init__.py
```

---

## 3. Структура Django-проекта

### Архитектура MVC в Django (MVT):
- **Model** - данные и бизнес-логика (models.py)
- **View** - отображение данных (views.py)
- **Template** - шаблоны (в папке templates/)

### Основные компоненты:
- **Models** - определяют структуру данных
- **Views** - обрабатывают запросы и возвращают ответы
- **Templates** - определяют структуру HTML
- **URLs** - маршрутизация запросов

### Пример модели:
```python
from django.db import models

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    
    def __str__(self):
        return self.question_text
```

### Пример представления:
```python
from django.http import HttpResponse
from .models import Question

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = ', '.join([q.question_text for q in latest_question_list])
    return HttpResponse(output)
```

---

## 4. Административная панель

### Создание суперпользователя:
```bash
python manage.py createsuperuser
```

### Регистрация моделей в админке:
```python
# admin.py
from django.contrib import admin
from .models import Question

admin.site.register(Question)
```

### Основные возможности админ-панели:
- CRUD операции над моделями
- Пользовательский интерфейс
- Фильтрация и поиск
- Импорт/экспорт данных

### Настройка админ-интерфейса:
```python
from django.contrib import admin
from .models import Question

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date')
    list_filter = ('pub_date',)
    search_fields = ('question_text',)
```

### Административная панель доступна по адресу:
http://127.0.0.1:8000/admin/