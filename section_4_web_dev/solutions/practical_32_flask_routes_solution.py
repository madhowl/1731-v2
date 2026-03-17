# Решения для практического занятия 32: Flask - маршруты

from flask import Flask, request, jsonify, abort, render_template_string
from werkzeug.routing import BaseConverter

app = Flask(__name__)

# =============================================================================
# Задание 1: Базовые маршруты
# =============================================================================

@app.route('/')
def index():
    """Главная страница"""
    return '<h1>Главная страница</h1>'


@app.route('/about')
def about():
    """Страница о нас"""
    return '<h1>О нас</h1>'


@app.route('/contact')
def contact():
    """Страница контактов"""
    return '<h1>Контакты</h1>'


@app.route('/user/admin')
def admin_profile():
    """Профиль администратора"""
    return '<h1>Профиль администратора</h1>'


# =============================================================================
# Задание 2: Параметры в URL
# =============================================================================

@app.route('/user/<username>')
def user_profile(username):
    """Профиль пользователя по имени"""
    return f'<h1>Профиль пользователя: {username}</h1>'


@app.route('/post/<int:post_id>')
def show_post(post_id):
    """Отображение поста по ID"""
    return f'<h1>Пост #{post_id}</h1>'


@app.route('/product/<string:category>/<int:product_id>')
def show_product(category, product_id):
    """Товар по категории и ID"""
    return f'<h1>Товар: {category} - #{product_id}</h1>'


# =============================================================================
# Задание 3: HTTP-методы (API для управления задачами)
# =============================================================================

# Хранилище задач (в памяти)
tasks = []
task_id_counter = 1


@app.route('/tasks', methods=['GET'])
def get_tasks():
    """Получить список задач"""
    return jsonify({'tasks': tasks, 'count': len(tasks)})


@app.route('/tasks', methods=['POST'])
def create_task():
    """Создать задачу"""
    global task_id_counter
    
    data = request.get_json()
    if not data or 'title' not in data:
        return jsonify({'error': 'Название задачи обязательно'}), 400
    
    task = {
        'id': task_id_counter,
        'title': data['title'],
        'description': data.get('description', ''),
        'completed': False
    }
    tasks.append(task)
    task_id_counter += 1
    
    return jsonify({'message': 'Задача создана', 'task': task}), 201


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    """Получить задачу по ID"""
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'Задача не найдена'}), 404
    return jsonify(task)


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Обновить задачу"""
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'Задача не найдена'}), 404
    
    data = request.get_json()
    if 'title' in data:
        task['title'] = data['title']
    if 'description' in data:
        task['description'] = data['description']
    if 'completed' in data:
        task['completed'] = data['completed']
    
    return jsonify({'message': f'Задача {task_id} обновлена', 'task': task})


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Удалить задачу"""
    global tasks
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'Задача не найдена'}), 404
    
    tasks = [t for t in tasks if t['id'] != task_id]
    return jsonify({'message': f'Задача {task_id} удалена'}), 204


# =============================================================================
# Задание 4: Формы
# =============================================================================

CONTACT_FORM_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Контактная форма</title>
    <style>
        body { font-family: Arial; padding: 20px; }
        form { max-width: 400px; }
        input, textarea { width: 100%; padding: 8px; margin: 5px 0; }
        button { background: #007bff; color: white; padding: 10px 20px; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <h1>Контактная форма</h1>
    <form method="POST">
        <label>Имя:</label>
        <input type="text" name="name" required>
        
        <label>Email:</label>
        <input type="email" name="email" required>
        
        <label>Сообщение:</label>
        <textarea name="message" rows="5" required></textarea>
        
        <button type="submit">Отправить</button>
    </form>
    <p><a href="/contact-form">Назад к форме</a></p>
</body>
</html>
"""


@app.route('/contact-form', methods=['GET'])
def contact_form_get():
    """Отображение формы"""
    return render_template_string(CONTACT_FORM_HTML)


@app.route('/contact-form', methods=['POST'])
def contact_form_post():
    """Обработка отправленной формы"""
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    
    # Валидация данных
    if not name or not email:
        return '<h1>Имя и email обязательны!</h1>', 400
    
    # Обработка данных
    return f'''
    <h1>Спасибо, {name}! Ваше сообщение получено.</h1>
    <p>Мы свяжемся с вами по адресу: {email}</p>
    <p><a href="/contact-form">Назад к форме</a></p>
    '''


# =============================================================================
# Задание 5: Сложные маршруты
# =============================================================================

# Маршрут для просмотра статей по slug
articles = {
    'python-basics': {'title': 'Основы Python', 'content': 'Содержимое статьи о Python...'},
    'web-dev-tips': {'title': 'Советы по веб-разработке', 'content': 'Содержимое статьи о веб-разработке...'},
}


@app.route('/article/<slug>')
def article_detail(slug):
    """Просмотр статьи по slug"""
    import re
    
    # Проверка формата slug
    if not re.match(r'^[a-z0-9-]+$', slug):
        abort(400, description="Неверный формат slug")
    
    # Логика получения статьи
    article = articles.get(slug)
    if not article:
        abort(404, description="Статья не найдена")
    
    return f'''
    <h1>{article['title']}</h1>
    <p>{article['content']}</p>
    <p><a href="/">На главную</a></p>
    '''


# Маршрут с проверкой прав доступа (имитация)
def is_admin():
    """Проверка прав администратора (имитация)"""
    # В реальном приложении здесь будет проверка аутентификации
    return True


@app.route('/admin/<path:subpath>')
def admin_panel(subpath):
    """Панель администратора"""
    if not is_admin():
        abort(403, description="Доступ запрещен")
    
    return f'<h1>Панель администратора: {subpath}</h1>'


# =============================================================================
# Задание 6: Кастомные конвертеры
# =============================================================================

class RegexConverter(BaseConverter):
    """Кастомный конвертер для регулярных выражений"""
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app.url_map.converters['regex'] = RegexConverter


@app.route('/product/<regex("[A-Z]{2,5}"):code>/<int:id>')
def product_by_code(code, id):
    """Товар по коду (2-5 заглавных букв)"""
    return f'<h1>Продукт: {code}-{id}</h1>'


# =============================================================================
# Обработчики ошибок
# =============================================================================

@app.errorhandler(404)
def not_found_error(error):
    return '<h1>Страница не найдена</h1>', 404


@app.errorhandler(500)
def internal_error(error):
    return '<h1>Внутренняя ошибка сервера</h1>', 500


# =============================================================================
# Задание 7: API с версионированием
# =============================================================================

@app.route('/api/v1/users')
@app.route('/api/v2/users')
def get_users():
    """Получение списка пользователей с версионированием"""
    api_version = request.path.split('/')[2]  # Получаем версию из URL
    
    if api_version == 'v1':
        return jsonify({
            'version': 'v1',
            'users': [
                {'id': 1, 'name': 'Иван'},
                {'id': 2, 'name': 'Мария'}
            ]
        })
    else:
        return jsonify({
            'version': 'v2',
            'users': [
                {'id': 1, 'name': 'Иван', 'email': 'ivan@example.com'},
                {'id': 2, 'name': 'Мария', 'email': 'maria@example.com'}
            ],
            'pagination': {'page': 1, 'total': 2}
        })


# =============================================================================
# Главная функция
# =============================================================================

def main():
    """Запуск веб-приложения"""
    print("=" * 70)
    print("Решения для практического занятия 32: Flask - маршруты")
    print("=" * 70)
    print("Доступные маршруты:")
    print("  /                  - Главная страница")
    print("  /about            - О нас")
    print("  /contact           - Контакты")
    print("  /user/admin        - Профиль администратора")
    print("  /user/<username>   - Профиль пользователя")
    print("  /post/<int:id>     - Пост по ID")
    print("  /product/<cat>/<id> - Товар")
    print("  /tasks             - API задач (GET, POST)")
    print("  /tasks/<id>        - API задач (GET, PUT, DELETE)")
    print("  /contact-form      - Контактная форма")
    print("  /article/<slug>    - Статья по slug")
    print("  /admin/<path>     - Панель администратора")
    print("  /api/v1/users      - API v1 пользователей")
    print("  /api/v2/users      - API v2 пользователей")
    print("=" * 70)
    print("Запуск на http://127.0.0.1:5000")
    app.run(debug=True)


if __name__ == "__main__":
    main()
