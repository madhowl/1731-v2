# Практическое занятие 32: Flask - маршруты

## Создание и обработка маршрутов в Flask

### Цель занятия:
Научиться создавать маршруты в Flask-приложениях, использовать параметры URL, обрабатывать различные HTTP-методы, создавать сложные маршруты с условиями.

### Задачи:
1. Создать базовые маршруты Flask
2. Использовать параметры в URL
3. Обработать различные HTTP-методы
4. Реализовать сложные маршруты

### План работы:
1. Основы маршрутов Flask
2. Параметры в URL
3. HTTP-методы
4. Сложные маршруты
5. Практические задания

---

## 1. Основы маршрутов Flask

Маршруты (routes) в Flask определяют, какие URL будут обслуживаться приложением и как будет обрабатываться каждый запрос.

### Пример 1: Простейший маршрут

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Привет, мир!'

if __name__ == '__main__':
    app.run(debug=True)
```

### Пример 2: Несколько маршрутов

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Главная страница</h1>'

@app.route('/about')
def about():
    return '<h1>О нас</h1>'

@app.route('/contact')
def contact():
    return '<h1>Контакты</h1>'

# Маршруты с одинаковой обработкой
@app.route('/user')
@app.route('/profile')
def user_profile():
    return '<h1>Профиль пользователя</h1>'
```

### Пример 3: Использование параметров в маршрутах

```python
@app.route('/user/<username>')
def show_user_profile(username):
    return f'<h1>Профиль пользователя: {username}</h1>'

@app.route('/post/<int:post_id>')
def show_post(post_id):
    return f'<h1>Пост #{post_id}</h1>'

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    return f'<h1>Подпуть: {subpath}</h1>'
```

---

## 2. Параметры в URL

Flask поддерживает различные типы параметров, которые можно использовать в маршрутах.

### Пример 4: Различные типы параметров

```python
@app.route('/string/<string:name>')  # Строка (по умолчанию)
def string_param(name):
    return f'<h1>Строка: {name}</h1>'

@app.route('/int/<int:count>')  # Целое число
def int_param(count):
    return f'<h1>Число: {count}, квадрат: {count**2}</h1>'

@app.route('/float/<float:value>')  # Число с плавающей точкой
def float_param(value):
    return f'<h1>Float: {value}, удвоенное значение: {value*2}</h1>'

@app.route('/uuid/<uuid:id>')  # UUID
def uuid_param(id):
    return f'<h1>UUID: {id}</h1>'
```

### Пример 5: Параметры с регулярными выражениями

```python
from werkzeug.routing import Rule
from flask import Flask

app = Flask(__name__)

# Регистрация правила с регулярным выражением
app.url_map.add(Rule('/product/<regex("[a-z]+"):category>/<int:id>', endpoint='product_detail'))

# Альтернативный подход с кастомным конвертером
from werkzeug.routing import BaseConverter

class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter

@app.route('/product/<regex("[A-Z]{2,5}"):code>/<int:id>')
def product_by_code(code, id):
    return f'<h1>Продукт: {code}-{id}</h1>'
```

### Пример 6: Необязательные параметры

```python
@app.route('/user/<username>')  # Обязательный параметр
@app.route('/user/')  # Маршрут без параметра
def show_user_optional(username=None):
    if username:
        return f'<h1>Профиль пользователя: {username}</h1>'
    else:
        return '<h1>Пожалуйста, укажите имя пользователя</h1>'

# Альтернативный способ с использованием defaults
from flask import Flask

app = Flask(__name__)

@app.route('/page/')
@app.route('/page/<int:num>')
def show_page(num=1):
    return f'<h1>Страница номер: {num}</h1>'
```

---

## 3. HTTP-методы

Flask позволяет обрабатывать различные HTTP-методы: GET, POST, PUT, DELETE, PATCH и другие.

### Пример 7: Обработка разных методов в одном маршруте

```python
from flask import request

@app.route('/api/data', methods=['GET'])
def get_data():
    return {'message': 'Данные получены', 'method': 'GET'}

@app.route('/api/data', methods=['POST'])
def create_data():
    data = request.get_json()
    return {'message': 'Данные созданы', 'data': data}, 201

@app.route('/api/data/<int:item_id>', methods=['PUT'])
def update_data(item_id):
    data = request.get_json()
    return {'message': f'Данные с ID {item_id} обновлены', 'data': data}

@app.route('/api/data/<int:item_id>', methods=['DELETE'])
def delete_data(item_id):
    return {'message': f'Данные с ID {item_id} удалены'}, 204
```

### Пример 8: Множественные методы в одном маршруте

```python
@app.route('/api/items', methods=['GET', 'POST'])
def handle_items():
    if request.method == 'GET':
        return {'items': [], 'count': 0}
    elif request.method == 'POST':
        data = request.get_json()
        # Логика создания элемента
        return {'message': 'Элемент создан', 'data': data}, 201

@app.route('/api/items/<int:item_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_item(item_id):
    if request.method == 'GET':
        return {'id': item_id, 'name': 'Sample Item'}
    elif request.method == 'PUT':
        data = request.get_json()
        return {'message': f'Элемент {item_id} обновлен', 'data': data}
    elif request.method == 'DELETE':
        return {'message': f'Элемент {item_id} удален'}, 204
```

### Пример 9: Работа с формами

```python
@app.route('/form', methods=['GET', 'POST'])
def handle_form():
    if request.method == 'POST':
        # Получение данных формы
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Валидация данных
        if not name or not email:
            return '<h1>Имя и email обязательны!</h1>', 400
        
        # Обработка данных
        return f'<h1>Спасибо, {name}! Ваше сообщение получено.</h1>'
    
    # GET-запрос - отображение формы
    return '''
    <form method="POST">
        <p><input type=text name=name placeholder="Имя" required></p>
        <p><input type=email name=email placeholder="Email" required></p>
        <p><textarea name=message placeholder="Сообщение"></textarea></p>
        <p><input type=submit value="Отправить"></p>
    </form>
    '''
```

---

## 4. Сложные маршруты

### Пример 10: Маршруты с условиями

```python
from flask import abort

@app.route('/user/<username>')
def show_user(username):
    # Проверка существования пользователя
    if not user_exists(username):
        abort(404)  # Возвращает 404 ошибку
    
    return f'<h1>Профиль пользователя: {username}</h1>'

def user_exists(username):
    # Имитация проверки существования пользователя
    valid_users = ['admin', 'user1', 'user2']
    return username in valid_users

# Маршруты с условиями по методу
@app.route('/api/resource', defaults={'resource_id': None}, methods=['POST'])
@app.route('/api/resource/<int:resource_id>', methods=['GET', 'PUT', 'DELETE'])
def handle_resource(resource_id):
    if request.method == 'POST':
        # Создание нового ресурса
        return {'message': 'Ресурс создан'}, 201
    elif resource_id is None:
        # Неверный маршрут
        abort(400)
    else:
        # Обработка существующего ресурса
        if request.method == 'GET':
            return {'id': resource_id, 'name': 'Resource'}
        elif request.method == 'PUT':
            return {'message': f'Ресурс {resource_id} обновлен'}
        elif request.method == 'DELETE':
            return {'message': f'Ресурс {resource_id} удален'}, 204
```

### Пример 11: Специальные маршруты

```python
# Маршрут для статических файлов (обычно не нужно определять вручную)
@app.route('/static/<path:filename>')
def static_files(filename):
    from flask import send_from_directory
    return send_from_directory('static', filename)

# Маршрут для favicon
@app.route('/favicon.ico')
def favicon():
    return '', 204

# Маршрут для обработки ошибок
@app.errorhandler(404)
def not_found_error(error):
    return '<h1>Страница не найдена</h1>', 404

@app.errorhandler(500)
def internal_error(error):
    return '<h1>Внутренняя ошибка сервера</h1>', 500

# Маршрут для API с версионированием
@app.route('/api/v1/users')
@app.route('/api/v2/users')
def get_users():
    api_version = request.path.split('/')[2]  # Получаем версию из URL
    return {'version': api_version, 'users': []}
```

### Пример 12: Продвинутые маршруты

```python
# Маршруты с кастомными условиями
@app.route('/article/<slug>')
def article_detail(slug):
    # Проверка формата slug
    import re
    if not re.match(r'^[a-z0-9-]+$', slug):
        abort(400, description="Неверный формат slug")
    
    # Логика получения статьи
    article = get_article_by_slug(slug)
    if not article:
        abort(404, description="Статья не найдена")
    
    return render_template('article.html', article=article)

def get_article_by_slug(slug):
    # Имитация получения статьи из базы данных
    articles = {
        'python-flask-basics': {'title': 'Основы Flask', 'content': 'Содержимое статьи...'},
        'web-development-tips': {'title': 'Советы по веб-разработке', 'content': 'Содержимое статьи...'}
    }
    return articles.get(slug)

# Маршруты с ограничениями
@app.route('/admin/<path:subpath>')  # path параметр позволяет использовать /
def admin_panel(subpath):
    # Проверка прав доступа
    if not is_admin():
        abort(403)
    
    return f'<h1>Панель администратора: {subpath}</h1>'

def is_admin():
    # Имитация проверки прав администратора
    return True  # В реальном приложении здесь будет проверка аутентификации
```

---

## 5. Практические задания

### Задание 1: Базовые маршруты
Создайте Flask-приложение с маршрутами:
- '/' - главная страница
- '/about' - страница о нас
- '/contact' - страница контактов
- '/user/admin' - профиль администратора

### Задание 2: Параметры в URL
Реализуйте маршруты с параметрами:
- '/user/<username>' - профиль пользователя
- '/post/<int:post_id>' - отображение поста по ID
- '/product/<string:category>/<int:product_id>' - товар по категории и ID

### Задание 3: HTTP-методы
Создайте API для управления задачами:
- GET /tasks - получить список задач
- POST /tasks - создать задачу
- PUT /tasks/<int:task_id> - обновить задачу
- DELETE /tasks/<int:task_id> - удалить задачу

### Задание 4: Формы
Реализуйте маршрут для обработки контактной формы:
- GET - отображение формы
- POST - обработка отправленной формы

### Задание 5: Сложные маршруты
Создайте маршруты с условиями:
- Маршрут для просмотра статей по slug
- Маршрут с проверкой прав доступа
- Маршрут с кастомной валидацией параметров

---

## 6. Дополнительные задания

### Задание 6: API с версионированием
Реализуйте API с поддержкой нескольких версий.

### Задание 7: Кастомные URL-конвертеры
Создайте свои URL-конвертеры для специфических типов данных.

### Задание 8: Обработка ошибок
Добавьте обработчики для различных HTTP-ошибок.

---

## Контрольные вопросы:
1. Как создать маршрут в Flask?
2. Какие типы параметров поддерживаются в Flask?
3. Как обработать несколько HTTP-методов в одном маршруте?
4. Как получить данные из формы в Flask?
5. Как обработать ошибки в Flask-приложении?