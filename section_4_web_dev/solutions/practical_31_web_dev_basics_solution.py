# Решения для практического занятия 31: Основы веб-разработки

# Этот файл содержит примеры HTML и CSS для базовой веб-страницы
# Для запуска веб-приложения используйте Flask из practical_33

# =============================================================================
# Пример HTML-страницы (index.html)
# =============================================================================

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Мое первое веб-приложение</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            color: #333;
        }
        
        header {
            background: #333;
            color: #fff;
            padding: 1rem;
        }
        
        nav ul {
            list-style: none;
            display: flex;
            gap: 20px;
        }
        
        nav a {
            color: #fff;
            text-decoration: none;
        }
        
        main {
            padding: 2rem;
            max-width: 1200px;
            margin: 0 auto;
        }
        
        section {
            margin-bottom: 2rem;
            padding: 1rem;
            background: #f4f4f4;
            border-radius: 5px;
        }
        
        footer {
            background: #333;
            color: #fff;
            text-align: center;
            padding: 1rem;
            position: fixed;
            bottom: 0;
            width: 100%;
        }
        
        form {
            max-width: 500px;
            margin: 0 auto;
        }
        
        input, textarea {
            width: 100%;
            padding: 0.5rem;
            margin-bottom: 1rem;
            border: 1px solid #ddd;
            border-radius: 3px;
        }
        
        button {
            background: #007bff;
            color: #fff;
            padding: 0.5rem 1rem;
            border: none;
            border-radius: 3px;
            cursor: pointer;
        }
        
        button:hover {
            background: #0056b3;
        }
        
        .card {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
        }
        
        .card-item {
            background: #fff;
            padding: 1rem;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body>
    <header>
        <h1>Добро пожаловать на мой сайт</h1>
        <nav>
            <ul>
                <li><a href="#home">Главная</a></li>
                <li><a href="#about">О нас</a></li>
                <li><a href="#contact">Контакты</a></li>
            </ul>
        </nav>
    </header>
    
    <main>
        <section id="home">
            <h2>Главная страница</h2>
            <p>Это пример простого веб-сайта.</p>
            <div class="card">
                <div class="card-item">
                    <h3>Карточка 1</h3>
                    <p>Описание карточки 1</p>
                </div>
                <div class="card-item">
                    <h3>Карточка 2</h3>
                    <p>Описание карточки 2</p>
                </div>
                <div class="card-item">
                    <h3>Карточка 3</h3>
                    <p>Описание карточки 3</p>
                </div>
            </div>
        </section>
        
        <section id="about">
            <h2>О нас</h2>
            <p>Информация о компании или проекте.</p>
            <p>Мы создаем современные веб-приложения с использованием передовых технологий.</p>
        </section>
        
        <section id="contact">
            <h2>Контакты</h2>
            <form>
                <label for="name">Имя:</label>
                <input type="text" id="name" name="name" required>
                
                <label for="email">Email:</label>
                <input type="email" id="email" name="email" required>
                
                <label for="message">Сообщение:</label>
                <textarea id="message" name="message" rows="5" required></textarea>
                
                <button type="submit">Отправить</button>
            </form>
        </section>
    </main>
    
    <footer>
        <p>&copy; 2024 Мой сайт. Все права защищены.</p>
    </footer>
</body>
</html>
"""


# =============================================================================
# Flask приложение
# =============================================================================

from flask import Flask, render_template_string, request, jsonify

app = Flask(__name__)


# =============================================================================
# Маршруты
# =============================================================================

@app.route('/')
def index():
    """Главная страница"""
    return render_template_string(HTML_TEMPLATE)


@app.route('/about')
def about():
    """Страница о нас"""
    about_html = """
    <!DOCTYPE html>
    <html>
    <head><title>О нас</title></head>
    <body>
        <h1>О нас</h1>
        <p>Мы - команда профессиональных разработчиков.</p>
        <a href="/">На главную</a>
    </body>
    </html>
    """
    return render_template_string(about_html)


@app.route('/contact')
def contact():
    """Страница контактов"""
    contact_html = """
    <!DOCTYPE html>
    <html>
    <head><title>Контакты</title></head>
    <body>
        <h1>Контакты</h1>
        <p>Email: info@example.com</p>
        <p>Телефон: +7 (999) 123-45-67</p>
        <a href="/">На главную</a>
    </body>
    </html>
    """
    return render_template_string(contact_html)


# =============================================================================
# API маршруты
# =============================================================================

@app.route('/api/data', methods=['GET'])
def get_data():
    """Получение данных"""
    return jsonify({
        'message': 'Данные получены',
        'data': [
            {'id': 1, 'name': 'Элемент 1'},
            {'id': 2, 'name': 'Элемент 2'},
            {'id': 3, 'name': 'Элемент 3'}
        ]
    })


@app.route('/api/data', methods=['POST'])
def post_data():
    """Отправка данных"""
    data = request.get_json()
    return jsonify({
        'message': 'Данные созданы',
        'data': data
    }), 201


# =============================================================================
# Примеры работы с формами
# =============================================================================

@app.route('/form', methods=['GET', 'POST'])
def form_example():
    """Пример работы с формами"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        
        # Валидация
        if not name or not email:
            return jsonify({'error': 'Имя и email обязательны'}), 400
        
        return jsonify({
            'message': f'Спасибо, {name}! Ваше сообщение получено.',
            'email': email
        })
    
    form_html = """
    <!DOCTYPE html>
    <html>
    <head><title>Форма</title></head>
    <body>
        <h1>Контактная форма</h1>
        <form method="POST">
            <p><input type="text" name="name" placeholder="Ваше имя" required></p>
            <p><input type="email" name="email" placeholder="Ваш email" required></p>
            <p><textarea name="message" placeholder="Ваше сообщение" required></textarea></p>
            <p><button type="submit">Отправить</button></p>
        </form>
    </body>
    </html>
    """
    return render_template_string(form_html)


# =============================================================================
# Главная функция
# =============================================================================

def main():
    """Запуск веб-приложения"""
    print("=" * 70)
    print("Решения для практического занятия 31: Основы веб-разработки")
    print("=" * 70)
    print("Запуск Flask приложения на http://127.0.0.1:5000")
    print("=" * 70)
    app.run(debug=True)


if __name__ == "__main__":
    main()
