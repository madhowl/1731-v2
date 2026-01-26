# Лекция 19: Flask - основы

## Установка, маршрутизация, шаблоны, Jinja2

### Цель лекции:
- Познакомиться с фреймворком Flask
- Изучить основы маршрутизации
- Освоить работу с шаблонами и движком Jinja2

### План лекции:
1. Установка Flask
2. Основы маршрутизации
3. Работа с шаблонами
4. Движок Jinja2

---

## 1. Установка Flask

Flask — микрофреймворк для создания веб-приложений на Python. Он легковесный и гибкий.

### Установка через pip:
```bash
pip install Flask
```

### Простейшее Flask-приложение:
```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Привет, мир!'

if __name__ == '__main__':
    app.run(debug=True)
```

### Основные особенности Flask:
- Простота и минимальизм
- Большое количество расширений
- Отличная документация
- Гибкость в архитектуре

---

## 2. Основы маршрутизации

Маршрутизация — это процесс сопоставления URL-адресов с функциями приложения.

### Простой маршрут:
```python
@app.route('/')
def index():
    return 'Главная страница'
```

### Маршрут с параметрами:
```python
@app.route('/user/<username>')
def show_user_profile(username):
    return f'Пользователь: {username}'
```

### Маршрут с типизированными параметрами:
```python
@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'Пост #{post_id}'
```

### Маршруты с несколькими методами:
```python
from flask import request

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'Обработка логина'
    else:
        return 'Показ формы входа'
```

---

## 3. Работа с шаблонами

Flask использует шаблоны для генерации HTML. Шаблоны находятся в папке `templates`.

### Структура проекта:
```
myapp/
├── app.py
└── templates/
    ├── index.html
    └── user.html
```

### Использование шаблонов:
```python
from flask import render_template

@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)
```

### Пример шаблона (templates/hello.html):
```html
<!doctype html>
<title>Hello from Flask</title>
{% if name %}
  <h1>Привет, {{ name }}!</h1>
{% else %}
  <h1>Привет, незнакомец!</h1>
{% endif %}
```

---

## 4. Движок Jinja2

Jinja2 — мощный шаблонизатор для Python, используемый Flask.

### Основные элементы:
- **Переменные**: `{{ variable }}`
- **Выражения**: `{% %}`
- **Комментарии**: `{# #}`

### Переменные:
```html
<p>Здравствуй, {{ username }}!</p>
```

### Условия:
```html
{% if users %}
 <ul>
  {% for user in users %}
    <li>{{ user.username }}</li>
  {% endfor %}
  </ul>
{% endif %}
```

### Наследование шаблонов:
```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html>
<head>
  {% block head %}
  <title>Мой сайт</title>
  {% endblock %}
</head>
<body>
  <div id="content">{% block content %}{% endblock %}</div>
</body>
</html>
```

```html
<!-- templates/page.html -->
{% extends "base.html" %}
{% block title %}Страница {{ title }}{% endblock %}
{% block content %}
  <h1>{{ title }}</h1>
  <p>{{ content }}</p>
{% endblock %}
```

### Фильтры:
```html
{{ name|capitalize }}  <!-- 'john' -> 'John' -->
{{ text|truncate(20) }}  <!-- Обрезает текст до 20 символов -->
{{ number|round(2) }}  <!-- Округляет число до 2 знаков -->