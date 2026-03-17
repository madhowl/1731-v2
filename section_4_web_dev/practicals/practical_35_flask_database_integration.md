# Практическое занятие 35: Flask - интеграция с базой данных

## Работа с базами данных в Flask

### Цель занятия:
Научиться интегрировать Flask-приложения с базами данных, использовать ORM SQLAlchemy, создавать модели данных, выполнять CRUD-операции и миграции баз данных.

### Задачи:
1. Настроить подключение к базе данных
2. Создать модели данных с SQLAlchemy
3. Выполнять CRUD-операции
4. Использовать миграции Alembic
5. Реализовать связи между моделями

### План работы:
1. Настройка базы данных в Flask
2. Создание моделей с SQLAlchemy
3. CRUD-операции
4. Связи между моделями
5. Миграции базы данных
6. Практические задания

---

## 1. Настройка базы данных в Flask

### Пример 1: Установка необходимых библиотек

```bash
pip install flask-sqlalchemy flask-migrate sqlalchemy
```

### Пример 2: Базовая настройка SQLite

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Настройка базы данных SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация расширения
db = SQLAlchemy(app)

# Тестовое представление
@app.route('/')
def index():
    return 'База данных подключена!'

if __name__ == '__main__':
    app.run(debug=True)
```

### Пример 3: Настройка PostgreSQL

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Подключение к PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username:password@localhost/dbname'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
```

### Пример 4: Конфигурация с отдельным файлом

```python
# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    # SQLite для разработки
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db')
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    # PostgreSQL для продакшена
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class DevelopmentConfig(Config):
    DEBUG = True

# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

def create_app(config_name='development'):
    app = Flask(__name__)
    
    if config_name == 'production':
        app.config.from_object('config.ProductionConfig')
    else:
        app.config.from_object('config.DevelopmentConfig')
    
    db = SQLAlchemy(app)
    
    return app, db
```

---

## 2. Создание моделей с SQLAlchemy

### Пример 5: Простая модель пользователя

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Определение модели User
class User(db.Model):
    # Имя таблицы (опционально)
    __tablename__ = 'users'
    
    # Первичный ключ
    id = db.Column(db.Integer, primary_key=True)
    
    # Поля таблицы
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # Временные метки
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Дополнительные поля
    is_active = db.Column(db.Boolean, default=True)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Представление объекта
    def __repr__(self):
        return f'<User {self.username}>'
    
    # Строковое представление
    def __str__(self):
        return self.username
    
    # Преобразование в словарь
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active
        }

# Создание таблиц
with app.app_context():
    db.create_all()
    print("Таблицы созданы!")
```

### Пример 6: Модель статьи с отношениями

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Модель автора
class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True)
    bio = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Связь один-ко-многим с Article
    articles = db.relationship('Article', backref='author', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Author {self.name}>'

# Модель статьи
class Article(db.Model):
    __tablename__ = 'articles'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, index=True)
    content = db.Column(db.Text, nullable=False)
    excerpt = db.Column(db.String(500))
    published = db.Column(db.Boolean, default=False)
    view_count = db.Column(db.Integer, default=0)
    
    # Внешний ключ
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    
    # Временные метки
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = db.Column(db.DateTime)
    
    # Связь с категорией
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    category = db.relationship('Category', backref='articles')
    
    # Связь многие-ко-многим с Tag
    tags = db.relationship('Tag', secondary='article_tags', backref=db.backref('articles', lazy='dynamic'))
    
    def __repr__(self):
        return f'<Article {self.title}>'

# Модель категории
class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(200))
    
    def __repr__(self):
        return f'<Category {self.name}>'

# Модель тега (для связи многие-ко-многим)
class Tag(db.Model):
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True)
    
    def __repr__(self):
        return f'<Tag {self.name}>'

# Таблица связи для многие-ко-многим
article_tags = db.Table('article_tags',
    db.Column('article_id', db.Integer, db.ForeignKey('articles.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

# Создание таблиц
with app.app_context():
    db.create_all()
    print("Все таблицы созданы!")
```

---

## 3. CRUD-операции

### Пример 7: Создание данных (Create)

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Определение моделей (из предыдущего примера)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

# Создание одной записи
def create_user(username, email, password_hash):
    new_user = User(username=username, email=email, password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()
    return new_user

# Создание нескольких записей
def create_multiple_users():
    users_data = [
        {'username': 'admin', 'email': 'admin@example.com', 'password_hash': 'hash1'},
        {'username': 'john', 'email': 'john@example.com', 'password_hash': 'hash2'},
        {'username': 'jane', 'email': 'jane@example.com', 'password_hash': 'hash3'},
    ]
    
    users = []
    for data in users_data:
        user = User(**data)
        db.session.add(user)
        users.append(user)
    
    db.session.commit()
    return users

# Создание с обработкой ошибок
def safe_create_user(username, email, password_hash):
    try:
        # Проверка существования пользователя
        existing = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()
        
        if existing:
            return None, "Пользователь с таким именем или email уже существует"
        
        new_user = User(username=username, email=email, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        
        return new_user, None
    
    except Exception as e:
        db.session.rollback()
        return None, str(e)

# Демонстрация использования
with app.app_context():
    db.create_all()
    
    # Создание пользователя
    user, error = safe_create_user('testuser', 'test@example.com', 'password123')
    
    if error:
        print(f"Ошибка: {error}")
    else:
        print(f"Создан пользователь: {user}")
```

### Пример 8: Чтение данных (Read)

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

# Получение одной записи по ID
def get_user_by_id(user_id):
    user = User.query.get(user_id)  # Устаревший метод
    # Или
    user = db.session.get(User, user_id)  # Новый метод
    return user

# Получение одной записи по условию
def get_user_by_username(username):
    user = User.query.filter_by(username=username).first()
    return user

# Получение всех записей
def get_all_users():
    users = User.query.all()
    return users

# Получение с пагинацией
def get_users_paginated(page=1, per_page=10):
    pagination = User.query.paginate(page=page, per_page=per_page)
    return {
        'items': pagination.items,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev
    }

# Фильтрация с условиями
def get_active_users():
    users = User.query.filter_by(is_active=True).all()
    return users

# Сложные запросы с фильтрацией
def search_users(search_term):
    # LIKE запрос
    users = User.query.filter(User.username.like(f'%{search_term}%')).all()
    
    # Или с or_
    from sqlalchemy import or_
    users = User.query.filter(
        or_(
            User.username.like(f'%{search_term}%'),
            User.email.like(f'%{search_term}%')
        )
    ).all()
    
    return users

# Сортировка
def get_users_sorted():
    # По возрастанию
    users = User.query.order_by(User.username).all()
    
    # По убыванию
    users = User.query.order_by(User.username.desc()).all()
    
    # Несколько полей сортировки
    users = User.query.order_by(User.is_active.desc(), User.username).all()
    
    return users

# Ограничение результатов
def get_first_n_users(n=5):
    users = User.query.limit(n).all()
    return users

# Агрегатные функции
from sqlalchemy import func, count

def get_user_stats():
    # Количество пользователей
    total = db.session.query(func.count(User.id)).scalar()
    
    # Количество активных пользователей
    active_count = db.session.query(func.count(User.id)).filter_by(is_active=True).scalar()
    
    # Группировка
    stats = db.session.query(
        User.is_active,
        func.count(User.id)
    ).group_by(User.is_active).all()
    
    return {
        'total': total,
        'active': active_count,
        'stats': stats
    }

with app.app_context():
    db.create_all()
```

### Пример 9: Обновление данных (Update)

```python
# Обновление одной записи
def update_user(user_id, **kwargs):
    user = db.session.get(User, user_id)
    
    if not user:
        return None, "Пользователь не найден"
    
    # Обновление полей
    for key, value in kwargs.items():
        if hasattr(user, key):
            setattr(user, key, value)
    
    db.session.commit()
    return user, None

# Обновление с проверкой
def update_user_email(user_id, new_email):
    user = db.session.get(User, user_id)
    
    if not user:
        return None, "Пользователь не найден"
    
    # Проверка уникальности email
    existing = User.query.filter(
        User.email == new_email,
        User.id != user_id
    ).first()
    
    if existing:
        return None, "Email уже используется"
    
    user.email = new_email
    db.session.commit()
    
    return user, None

# Массовое обновление
def deactivate_inactive_users():
    # Обновление всех неактивных пользователей
    updated_count = User.query.filter_by(is_active=False).update({'is_active': False})
    db.session.commit()
    
    return updated_count

# Обновление с условием
def increment_view_count(article_id):
    from sqlalchemy import text
    
    # Прямой SQL запрос
    result = db.session.execute(
        text("UPDATE articles SET view_count = view_count + 1 WHERE id = :id"),
        {'id': article_id}
    )
    db.session.commit()
    
    return result.rowcount
```

### Пример 10: Удаление данных (Delete)

```python
# Удаление одной записи
def delete_user(user_id):
    user = db.session.get(User, user_id)
    
    if not user:
        return False, "Пользователь не найден"
    
    db.session.delete(user)
    db.session.commit()
    
    return True, None

# Удаление с проверкой
def safe_delete_user(user_id):
    user = db.session.get(User, user_id)
    
    if not user:
        return False, "Пользователь не найден"
    
    # Проверка связанных записей
    if hasattr(user, 'articles') and user.articles:
        return False, "Невозможно удалить: у пользователя есть статьи"
    
    db.session.delete(user)
    db.session.commit()
    
    return True, None

# Мягкое удаление (soft delete)
def soft_delete_user(user_id):
    user = db.session.get(User, user_id)
    
    if not user:
        return None, "Пользователь не найден"
    
    user.is_active = False
    db.session.commit()
    
    return user

# Массовое удаление
def delete_inactive_users():
    deleted_count = User.query.filter_by(is_active=False).delete()
    db.session.commit()
    
    return deleted_count
```

---

## 4. Связи между моделями

### Пример 11: Связь один-ко-многим

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Категория товаров (один)
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(50), unique=True)
    
    # Связь с товарами
    products = db.relationship('Product', backref='category', lazy='dynamic')

# Товар (много)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    
    def __repr__(self):
        return f'<Product {self.name}>'

# Примеры запросов
with app.app_context():
    db.create_all()
    
    # Создание категории и товаров
    electronics = Category(name='Электроника', slug='electronics')
    db.session.add(electronics)
    db.session.commit()
    
    # Добавление товара к категории
    laptop = Product(name='Ноутбук', price=50000, category=electronics)
    phone = Product(name='Смартфон', price=30000, category=electronics)
    db.session.add_all([laptop, phone])
    db.session.commit()
    
    # Получение товаров категории
    for product in electronics.products:
        print(f"{product.name}: {product.price} руб.")
    
    # Получение категории товара
    print(laptop.category.name)
```

### Пример 12: Связь многие-ко-многим

```python
# Таблица связи
students_courses = db.Table('students_courses',
    db.Column('student_id', db.Integer, db.ForeignKey('student.id'), primary_key=True),
    db.Column('course_id', db.Integer, db.ForeignKey('course.id'), primary_key=True),
    db.Column('enrolled_at', db.DateTime, default=datetime.utcnow)
)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True)
    
    # Связь many-to-many
    courses = db.relationship('Course', secondary=students_courses, backref='students')

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

# Примеры запросов
with app.app_context():
    db.create_all()
    
    # Запись студента на курс
    student = Student(name='Иван', email='ivan@example.com')
    course = Course(name='Python Basic', description='Базовый курс Python')
    
    student.courses.append(course)
    db.session.add_all([student, course])
    db.session.commit()
    
    # Получение курсов студента
    for c in student.courses:
        print(c.name)
    
    # Получение студентов курса
    for s in course.students:
        print(s.name)
```

---

## 5. Миграции базы данных

### Пример 13: Настройка Alembic

```bash
# Инициализация Alembic
flask db init

# Создание миграции
flask db migrate -m "Initial migration"

# Применение миграции
flask db upgrade

# Откат миграции
flask db downgrade
```

### Пример 14: Работа с миграциями в коде

```python
# Создание миграции
def create_migration():
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_migrate import Migrate
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db = SQLAlchemy(app)
    migrate = Migrate(app, db)
    
    return app, db, migrate

# Создание новой модели после миграции
class NewModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Команды для терминала:
# flask db init
# flask db migrate -m "Add new model"
# flask db upgrade
# flask db downgrade
```

---

## 6. Практические задания

### Задание 1: Система управления задачами
Создайте приложение для управления задачами (Todo List) со следующими моделями:
- Task: название, описание, статус (выполнена/не выполнена), дата создания, срок выполнения
- Выполните CRUD-операции для задач

### Задание 2: Блог с комментариями
Создайте модели для блога:
- Post: заголовок, содержание, автор, дата публикации
- Comment: текст, автор, дата, связанный пост
- Реализуйте вывод постов с комментариями

### Задание 3: Интернет-магазин
Создайте модели для простого интернет-магазина:
- Category: название, описание
- Product: название, цена, описание, категория
- Order: дата заказа, статус, клиент
- OrderItem: товар, количество, цена

### Задание 4: Система комментариев
Реализуйте систему комментариев с вложенными ответами:
- Comment: текст, автор, дата, родительский комментарий
- Вывод дерева комментариев

### Задание 5: Пагинация и поиск
Добавьте к блогу:
- Пагинацию постов
- Поиск по названию и содержанию
- Фильтрацию по дате

---

## Дополнительные задания

### Задание 6: Транзакции
Реализуйте перевод денег между счетами с использованием транзакций.

### Задание 7: Сложные запросы
Создайте отчеты с использованием агрегатных функций и группировки.

### Задание 8: Миграции
Настройте полный цикл миграций для существующего приложения.

---

## Контрольные вопросы:
1. Как настроить подключение к базе данных в Flask?
2. Что такое SQLAlchemy и какие преимущества она дает?
3. Как создать модель данных?
4. Какие типы связей между моделями вы знаете?
5. Как выполнить CRUD-операции?
6. Что такое миграции и зачем они нужны?
7. Как реализовать мягкое удаление?
8. Как использовать пагинацию в SQLAlchemy?
