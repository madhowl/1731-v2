# Практическое занятие 33: Flask - шаблоны

## Использование HTML-шаблонов в Flask

### Цель занятия:
Научиться использовать шаблоны Jinja2 в Flask-приложениях, создавать динамические HTML-страницы, применять наследование шаблонов.

### Задачи:
1. Создать структуру шаблонов Flask
2. Использовать переменные и фильтры в шаблонах
3. Применить условные конструкции и циклы
4. Реализовать наследование шаблонов

### План работы:
1. Основы шаблонов Flask
2. Переменные и фильтры
3. Условные конструкции и циклы
4. Наследование шаблонов
5. Практические задания

---

## 1. Основы шаблонов Flask

Flask использует шаблонизатор Jinja2 для генерации HTML-страниц. Шаблоны позволяют отделить логику приложения от представления.

### Пример 1: Структура проекта

```
my_flask_app/
├── app.py
├── templates/
│   ├── base.html
│   ├── index.html
│   └── user.html
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── script.js
```

### Пример 2: Базовое Flask-приложение с шаблонами

```python
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user_profile(name):
    return render_template('user.html', username=name)

if __name__ == '__main__':
    app.run(debug=True)
```

### Пример 3: Простейший шаблон (templates/index.html)

```html
<!DOCTYPE html>
<html>
<head>
    <title>Главная страница</title>
</head>
<body>
    <h1>Добро пожаловать на главную страницу!</h1>
    <p>Это пример простого шаблона Flask.</p>
</body>
</html>
```

---

## 2. Переменные и фильтры

### Пример 4: Передача переменных в шаблон

```python
@app.route('/user/<name>')
def user_profile(name):
    user_data = {
        'name': name,
        'email': f'{name.lower()}@example.com',
        'age': 25,
        'city': 'Москва'
    }
    return render_template('user.html', user=user_data)
```

### Пример 5: Использование переменных в шаблоне (templates/user.html)

```html
<!DOCTYPE html>
<html>
<head>
    <title>Профиль пользователя {{ user.name }}</title>
</head>
<body>
    <h1>Профиль пользователя: {{ user.name }}</h1>
    <p>Email: {{ user.email }}</p>
    <p>Возраст: {{ user.age }}</p>
    <p>Город: {{ user.city }}</p>
</body>
</html>
```

### Пример 6: Использование фильтров

```html
<!DOCTYPE html>
<html>
<head>
    <title>{{ title|default('Без заголовка')|title }}</title>
</head>
<body>
    <h1>{{ heading|upper }}</h1>
    <p>{{ content|striptags|truncate(100) }}</p>
    <p>Цена: {{ price|round(2)|currency('RUB') }}</p>
    <p>Дата: {{ date|strftime('%d.%m.%Y') }}</p>
</body>
</html>
```

```python
@app.route('/product')
def product():
    from datetime import datetime
    
    product_data = {
        'title': 'флажок для flask',
        'heading': 'флажок для flask',
        'content': '<p>Описание продукта с HTML тегами</p>',
        'price': 1234.567,
        'date': datetime.now()
    }
    return render_template('product.html', **product_data)
```

---

## 3. Условные конструкции и циклы

### Пример 7: Условные конструкции в шаблонах

```html
<!DOCTYPE html>
<html>
<head>
    <title>Условные конструкции</title>
</head>
<body>
    {% if user %}
        <h1>Привет, {{ user.name }}!</h1>
        {% if user.admin %}
            <p>Вы администратор</p>
        {% endif %}
    {% else %}
        <h1>Пожалуйста, войдите в систему</h1>
    {% endif %}
    
    {% if articles|length > 0 %}
        <p>Найдено {{ articles|length }} статей</p>
    {% else %}
        <p>Статей не найдено</p>
    {% endif %}
</body>
</html>
```

### Пример 8: Циклы в шаблонах

```html
<!DOCTYPE html>
<html>
<head>
    <title>Список пользователей</title>
</head>
<body>
    <h1>Список пользователей</h1>
    {% if users %}
        <ul>
        {% for user in users %}
            <li>
                <strong>{{ user.name }}</strong> - {{ user.email }}
                {% if user.active %}
                    <span style="color: green;">(активный)</span>
                {% else %}
                    <span style="color: red;">(неактивный)</span>
                {% endif %}
            </li>
        {% endfor %}
        </ul>
    {% else %}
        <p>Пользователей нет</p>
    {% endif %}
</body>
</html>
```

### Пример 9: Расширенные циклы

```html
<!DOCTYPE html>
<html>
<head>
    <title>Расширенные циклы</title>
</head>
<body>
    <h1>Список задач</h1>
    <ol>
    {% for task in tasks %}
        <li class="{% if task.completed %}completed{% else %}pending{% endif %}">
            {{ loop.index }}. {{ task.title }}
            {% if task.priority == 'high' %}
                <span style="color: red;">(важно)</span>
            {% elif task.priority == 'low' %}
                <span style="color: gray;">(низкий приоритет)</span>
            {% endif %}
        </li>
    {% else %}
        <li>Нет задач</li>
    {% endfor %}
    </ol>
    
    {% for key, value in config.items() %}
        <p>{{ key }}: {{ value }}</p>
    {% endfor %}
</body>
</html>
```

---

## 4. Наследование шаблонов

### Пример 10: Базовый шаблон (templates/base.html)

```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Мое приложение{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
    {% block head %}{% endblock %}
</head>
<body>
    <header>
        <nav>
            <ul>
                <li><a href="{{ url_for('index') }}">Главная</a></li>
                <li><a href="{{ url_for('about') }}">О нас</a></li>
                <li><a href="{{ url_for('contact') }}">Контакты</a></li>
            </ul>
        </nav>
    </header>
    
    <main>
        {% block content %}{% endblock %}
    </main>
    
    <footer>
        <p>&copy; 2023 Мое приложение. Все права защищены.</p>
    </footer>
    
    <script src="{{ url_for('static', filename='js/script.js') }}"></script>
    {% block scripts %}{% endblock %}
</body>
</html>
```

### Пример 11: Расширяющий шаблон (templates/index.html)

```html
{% extends "base.html" %}

{% block title %}Главная страница - {{ super() }}{% endblock %}

{% block content %}
    <h1>Добро пожаловать на главную страницу!</h1>
    <p>Это контент главной страницы.</p>
    
    {% if featured_articles %}
        <section>
            <h2>Популярные статьи</h2>
            <ul>
            {% for article in featured_articles %}
                <li><a href="{{ url_for('article', id=article.id) }}">{{ article.title }}</a></li>
            {% endfor %}
            </ul>
        </section>
    {% endif %}
{% endblock %}
```

### Пример 12: Шаблон профиля пользователя

```html
{% extends "base.html" %}

{% block title %}{{ user.name }} - {{ super() }}{% endblock %}

{% block content %}
    <h1>Профиль пользователя: {{ user.name }}</h1>
    <div class="profile-info">
        <p><strong>Email:</strong> {{ user.email }}</p>
        <p><strong>Дата регистрации:</strong> {{ user.registration_date.strftime('%d.%m.%Y') }}</p>
        <p><strong>Статус:</strong> 
            {% if user.is_premium %}
                <span class="premium">Премиум</span>
            {% else %}
                <span class="regular">Обычный</span>
            {% endif %}
        </p>
    </div>
    
    {% if user.posts %}
        <h2>Последние посты</h2>
        <div class="posts">
        {% for post in user.posts %}
            <article class="post">
                <h3><a href="{{ url_for('post', id=post.id) }}">{{ post.title }}</a></h3>
                <p class="post-date">{{ post.date.strftime('%d.%m.%Y') }}</p>
                <p>{{ post.preview|truncate(150) }}</p>
            </article>
        {% endfor %}
        </div>
    {% endif %}
{% endblock %}
```

---

## 5. Практические задания

### Задание 1: Создание блога
Создайте Flask-приложение с шаблонами для:
- Главной страницы со списком статей
- Страницы отдельной статьи
- Страницы автора со списком его статей
- Используйте наследование шаблонов

### Задание 2: Интернет-магазин
Разработайте шаблоны для:
- Главной страницы с товарами
- Страницы товара
- Корзины покупок
- Используйте фильтры для форматирования цен

### Задание 3: Личный кабинет
Создайте шаблоны для:
- Страницы профиля пользователя
- Страницы настроек
- Истории заказов
- Используйте условные конструкции для отображения разных элементов

### Задание 4: Админ-панель
Разработайте шаблоны для:
- Списка пользователей
- Страницы редактирования
- Статистики
- Используйте циклы для отображения списков

### Задание 5: Динамические элементы
Создайте шаблоны с:
- Формами обратной связи
- Комментариями
- Рейтингами
- Возможностью фильтрации данных

---

## 6. Дополнительные задания

### Задание 6: Макросы
Используйте макросы для создания переиспользуемых элементов интерфейса.

### Задание 7: Включения
Используйте include для включения частей шаблонов.

### Задание 8: Кастомные фильтры
Создайте свои фильтры для использования в шаблонах.

---

## Контрольные вопросы:
1. Как передать переменные из Flask-приложения в шаблон?
2. Какие фильтры доступны в Jinja2?
3. Как использовать условные конструкции в шаблонах?
4. Что такое наследование шаблонов и зачем оно нужно?
5. Как включить статические файлы в шаблон?