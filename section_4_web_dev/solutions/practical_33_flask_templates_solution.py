# Решения для практического занятия 33: Flask - шаблоны

from flask import Flask, render_template, render_template_string, request, jsonify

app = Flask(__name__)


# =============================================================================
# Примеры данных для передачи в шаблоны
# =============================================================================

# Пример пользователей
users = [
    {'name': 'Иван', 'age': 25, 'email': 'ivan@example.com', 'city': 'Москва'},
    {'name': 'Мария', 'age': 30, 'email': 'maria@example.com', 'city': 'Санкт-Петербург'},
    {'name': 'Петр', 'age': 35, 'email': 'petr@example.com', 'city': 'Новосибирск'},
    {'name': 'Анна', 'age': 28, 'email': 'anna@example.com', 'city': 'Екатеринбург'},
    {'name': 'Сергей', 'age': 32, 'email': 'sergey@example.com', 'city': 'Казань'}
]

# Пример статей
articles = [
    {'id': 1, 'title': 'Основы Python', 'author': 'Иван', 'date': '2024-01-15', 'category': 'Программирование'},
    {'id': 2, 'title': 'Веб-разработка с Flask', 'author': 'Мария', 'date': '2024-01-20', 'category': 'Веб'},
    {'id': 3, 'title': 'Работа с базами данных', 'author': 'Петр', 'date': '2024-02-01', 'category': 'Базы данных'},
    {'id': 4, 'title': 'Тестирование приложений', 'author': 'Анна', 'date': '2024-02-10', 'category': 'Тестирование'},
]

# Пример товаров
products = [
    {'id': 1, 'name': 'Ноутбук', 'price': 50000, 'category': 'Электроника'},
    {'id': 2, 'name': 'Смартфон', 'price': 30000, 'category': 'Электроника'},
    {'id': 3, 'name': 'Книга', 'price': 500, 'category': 'Книги'},
    {'id': 4, 'name': 'Наушники', 'price': 5000, 'category': 'Аксессуары'},
    {'id': 5, 'name': 'Клавиатура', 'price': 3000, 'category': 'Аксессуары'},
]


# =============================================================================
# Базовый шаблон
# =============================================================================

BASE_TEMPLATE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }} - {{ site_name }}</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; line-height: 1.6; }
        header { background: #333; color: #fff; padding: 1rem; }
        nav ul { list-style: none; display: flex; gap: 20px; }
        nav a { color: #fff; text-decoration: none; }
        nav a:hover { text-decoration: underline; }
        main { padding: 2rem; min-height: 60vh; }
        footer { background: #333; color: #fff; text-align: center; padding: 1rem; }
        .container { max-width: 1200px; margin: 0 auto; }
        {% block extra_styles %}{% endblock %}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1>{{ site_name }}</h1>
            <nav>
                <ul>
                    <li><a href="/">Главная</a></li>
                    <li><a href="/about">О нас</a></li>
                    <li><a href="/users">Пользователи</a></li>
                    <li><a href="/articles">Статьи</a></li>
                    <li><a href="/products">Товары</a></li>
                </ul>
            </nav>
        </div>
    </header>
    
    <main>
        <div class="container">
            {% block content %}{% endblock %}
        </div>
    </main>
    
    <footer>
        <p>&copy; 2024 {{ site_name }}. Все права защищены.</p>
    </footer>
</body>
</html>
"""


# =============================================================================
# Главная страница
# =============================================================================

@app.route('/')
def index():
    """Главная страница"""
    return render_template_string(BASE_TEMPLATE,
        title='Главная',
        site_name='Мой сайт',
        content="""
        <h2>Добро пожаловать!</h2>
        <p>Это пример веб-приложения на Flask с использованием шаблонов Jinja2.</p>
        
        <h3>Доступные страницы:</h3>
        <ul>
            <li><a href="/users">Список пользователей</a></li>
            <li><a href="/articles">Статьи</a></li>
            <li><a href="/products">Товары</a></li>
        </ul>
        
        <h3>Примеры Jinja2:</h3>
        <ul>
            <li>Переменные: {{ variable }}</li>
            <li>Циклы: {% for item in items %}</li>
            <li>Условия: {% if condition %}</li>
            <li>Фильтры: {{ name|upper }}</li>
        </ul>
        """,
        extra_styles="""
            .container { max-width: 1200px; margin: 0 auto; }
            ul { margin: 20px 0; }
            li { margin: 10px 0; }
        """
    )


# =============================================================================
# Примеры работы с переменными
# =============================================================================

@app.route('/variables')
def variables_example():
    """Пример работы с переменными"""
    user = {'name': 'Иван', 'age': 25}
    
    return render_template_string(BASE_TEMPLATE,
        title='Переменные',
        site_name='Примеры Jinja2',
        content=f"""
        <h2>Работа с переменными</h2>
        
        <h3>Простые переменные:</h3>
        <p>Имя: {{{{ user.name }}}}</p>
        <p>Возраст: {{{{ user.age }}}}</p>
        
        <h3>Вычисления:</h3>
        <p>Возраст через 5 лет: {{{{ user.age + 5 }}}}</p>
        
        <h3>Фильтры:</h3>
        <p>Имя (upper): {{{{ user.name|upper }}}}</p>
        <p>Имя (lower): {{{{ user.name|lower }}}}</p>
        <p>Имя (title): {{{{ user.name|title }}}}</p>
        
        <h3>Длина:</h3>
        <p>Длина имени: {{{{ user.name|length }}}}</p>
        """,
        extra_styles="""
            p { margin: 10px 0; }
        """
    )


# =============================================================================
# Примеры работы с циклами
# =============================================================================

@app.route('/loops')
def loops_example():
    """Пример работы с циклами"""
    return render_template_string(BASE_TEMPLATE,
        title='Циклы',
        site_name='Примеры Jinja2',
        content=f"""
        <h2>Работа с циклами</h2>
        
        <h3>Список пользователей (for):</h3>
        <ul>
        {{{{ ''.join([f'<li>{u["name"]} - {u["age"]} лет</li>' for u in users]) }}}}
        </ul>
        
        <h3>Нумерованный список (loop.index):</h3>
        <ol>
        {{{{ ''.join([f'<li>{u["name"]} (индекс: {i})</li>' for i, u in enumerate(users)]) }}}}
        </ol>
        
        <h3>Цикл с условием (for + if):</h3>
        <ul>
        {{{{ ''.join([f'<li>{u["name"]}</li>' for u in users if u["age"] > 28]) }}}}
        </ul>
        
        <h3>Цикл по словарю:</h3>
        <ul>
        {{{{ ''.join([f'<li>{{{{ key }}}}: {{ value }}</li>' for key, value in users[0].items()]) }}}}
        </ul>
        """,
        extra_styles="""
            li { margin: 5px 0; }
        """,
        users=users
    )


# =============================================================================
# Примеры работы с условиями
# =============================================================================

@app.route('/conditions')
def conditions_example():
    """Пример работы с условиями"""
    return render_template_string(BASE_TEMPLATE,
        title='Условия',
        site_name='Примеры Jinja2',
        content=f"""
        <h2>Работа с условиями</h2>
        
        <h3>Простое условие (if):</h3>
        {{{{ 'Привет, Иван!' if users[0].name == 'Иван' else 'Привет, незнакомец!' }}}}
        
        <h3>Условие с else:</h3>
        {{{{ 'Пользователь совершеннолетний' if users[0].age >= 18 else 'Пользователь несовершеннолетний' }}}}
        
        <h3>Множественные условия (elif):</h3>
        {{{{ 
            'Возраст меньше 25' if users[0].age < 25 
            else 'Возраст от 25 до 30' if users[0].age < 30 
            else 'Возраст 30 и более' 
        }}}}
        
        <h3>Проверка наличия данных:</h3>
        {{{{ 'Список не пуст' if users else 'Список пуст' }}}}
        
        <h3>Логические операторы:</h3>
        {{{{ True and True }}}} - True
        {{{{ True or False }}}} - True
        {{{{ not False }}}} - True
        """,
        extra_styles="""
            p, h3 { margin: 10px 0; }
        """,
        users=users
    )


# =============================================================================
# Примеры фильтров
# =============================================================================

@app.route('/filters')
def filters_example():
    """Пример работы с фильтрами"""
    text = "  Hello, World!  "
    
    return render_template_string(BASE_TEMPLATE,
        title='Фильтры',
        site_name='Примеры Jinja2',
        content=f"""
        <h2>Работа с фильтрами</h2>
        
        <h3>Строковые фильтры:</h3>
        <p>Оригинал: '{text}'</p>
        <p>upper: {{{{ '{text}'|upper }}}}</p>
        <p>lower: {{{{ '{text}'|lower }}}}</p>
        <p>title: {{{{ '{text}'|title }}}}</p>
        <p>strip: {{{{ '{text}'|strip }}}}</p>
        <p>trim: {{{{ '{text}'|trim }}}}</p>
        
        <h3>Числовые фильтры:</h3>
        <p>abs: {{{{ -42|abs }}}}</p>
        
        <h3>Фильтры списка:</h3>
        <p>first: {{{{ users|first|attr('name') }}}}</p>
        <p>last: {{{{ users|last|attr('name') }}}}</p>
        <p>length: {{{{ users|length }}}}</p>
        
        <h3>Объединение фильтров:</h3>
        <p>upper|trim: {{{{ '{text}'|upper|trim }}}}</p>
        """,
        extra_styles="""
            p { margin: 5px 0; }
        """,
        text=text,
        users=users
    )


# =============================================================================
# Страница пользователей
# =============================================================================

@app.route('/users')
def user_list():
    """Список пользователей"""
    return render_template_string(BASE_TEMPLATE,
        title='Пользователи',
        site_name='Мой сайт',
        content=f"""
        <h2>Список пользователей</h2>
        
        <table border="1" cellpadding="10" style="border-collapse: collapse; width: 100%;">
            <tr style="background: #f0f0f0;">
                <th>№</th>
                <th>Имя</th>
                <th>Возраст</th>
                <th>Email</th>
                <th>Город</th>
            </tr>
            {{{{ ''.join([f'''
            <tr>
                <td>{{{{ loop.index }}}}</td>
                <td>{{{{ u.name|title }}}}</td>
                <td>{{{{ u.age }}}}</td>
                <td><a href="mailto:{{{{ u.email }}}}>{{{{ u.email }}}}</a></td>
                <td>{{{{ u.city }}}}</td>
            </tr>
            ''' for u in users]) }}}}
        </table>
        
        <p>Всего пользователей: {{{{ users|length }}}}</p>
        
        <h3>Фильтрация (возраст > 28):</h3>
        <ul>
        {{{{ ''.join([f'<li>{{{{ u.name }}}}</li>' for u in users if u.age > 28]) }}}}
        </ul>
        """,
        extra_styles="""
            table { margin: 20px 0; }
            th, td { padding: 10px; }
            li { margin: 5px 0; }
        """,
        users=users
    )


# =============================================================================
# Страница статей
# =============================================================================

@app.route('/articles')
def article_list():
    """Список статей"""
    return render_template_string(BASE_TEMPLATE,
        title='Статьи',
        site_name='Мой сайт',
        content=f"""
        <h2>Статьи</h2>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); gap: 20px;">
        {{{{ ''.join([f'''
        <div style="border: 1px solid #ddd; padding: 15px; border-radius: 5px;">
            <h3>{{{{ a.title }}}}</h3>
            <p><strong>Автор:</strong> {{{{ a.author }}}}</p>
            <p><strong>Дата:</strong> {{{{ a.date }}}}</p>
            <p><strong>Категория:</strong> <span style="background: #e0e0e0; padding: 2px 8px; border-radius: 3px;">
                {{{{ a.category }}}}
            </span></p>
        </div>
        ''' for a in articles]) }}}}
        </div>
        
        <p style="margin-top: 20px;">Всего статей: {{{{ articles|length }}}}</p>
        """,
        extra_styles="""
            .container { padding: 20px; }
            div { background: #f9f9f9; }
        """,
        articles=articles
    )


# =============================================================================
# Страница товаров
# =============================================================================

@app.route('/products')
def product_list():
    """Список товаров"""
    # Вычисляемые значения
    total_price = sum(p['price'] for p in products)
    avg_price = total_price / len(products) if products else 0
    
    return render_template_string(BASE_TEMPLATE,
        title='Товары',
        site_name='Мой сайт',
        content=f"""
        <h2>Каталог товаров</h2>
        
        <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 20px;">
        {{{{ ''.join([f'''
        <div style="border: 1px solid #ddd; padding: 15px; border-radius: 5px; text-align: center;">
            <h3>{{{{ p.name }}}}</h3>
            <p style="font-size: 24px; color: green; font-weight: bold;">
                {{{{ p.price|int }}}} руб.
            </p>
            <p style="color: #666;">Категория: {{{{ p.category }}}}</p>
        </div>
        ''' for p in products]) }}}}
        </div>
        
        <div style="margin-top: 30px; padding: 20px; background: #f0f0f0; border-radius: 5px;">
            <h3>Итого:</h3>
            <p>Количество товаров: {{{{ products|length }}}}</p>
            <p>Общая стоимость: {{{{ total_price }}}} руб.</p>
            <p>Средняя цена: {{{{ avg_price|round(2) }}}} руб.</p>
        </div>
        
        <h3 style="margin-top: 20px;">Товары дороже 10000 руб.:</h3>
        <ul>
        {{{{ ''.join([f'<li>{{{{ p.name }}}} - {{{{ p.price }}}} руб.</li>' for p in products if p.price > 10000]) }}}}
        </ul>
        """,
        extra_styles="""
            .container { padding: 20px; }
            li { margin: 5px 0; }
        """,
        products=products,
        total_price=total_price,
        avg_price=avg_price
    )


# =============================================================================
# О нас
# =============================================================================

@app.route('/about')
def about():
    """Страница о нас"""
    return render_template_string(BASE_TEMPLATE,
        title='О нас',
        site_name='Мой сайт',
        content="""
        <h2>О нас</h2>
        <p>Мы - команда профессиональных разработчиков, создающих современные веб-приложения.</p>
        <p>Наш сайт построен с использованием Flask и шаблонов Jinja2.</p>
        
        <h3>Наши преимущества:</h3>
        <ul>
            <li>Современные технологии</li>
            <li>Качественный код</li>
            <li>Индивидуальный подход</li>
        </ul>
        """,
        extra_styles="""
            li { margin: 10px 0; }
        """
    )


# =============================================================================
# Главная функция
# =============================================================================

def main():
    """Запуск веб-приложения"""
    print("=" * 70)
    print("Решения для практического занятия 33: Flask - шаблоны")
    print("=" * 70)
    print("Доступные страницы:")
    print("  /           - Главная страница")
    print("  /variables  - Примеры работы с переменными")
    print("  /loops      - Примеры работы с циклами")
    print("  /conditions - Примеры работы с условиями")
    print("  /filters    - Примеры работы с фильтрами")
    print("  /users      - Список пользователей")
    print("  /articles   - Список статей")
    print("  /products   - Каталог товаров")
    print("  /about      - О нас")
    print("=" * 70)
    print("Запуск на http://127.0.0.1:5000")
    app.run(debug=True)


if __name__ == "__main__":
    main()
