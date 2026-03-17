# -*- coding: utf-8 -*-
"""
Практическое занятие 35: Flask - интеграция с базой данных
Решение упражнений

В этом файле представлены решения для всех упражнений практического занятия
по интеграции Flask с базами данных.

Для запуска:
    python practical_35_flask_database_integration_solution.py

Требования:
    pip install flask flask-sqlalchemy sqlalchemy
"""

import os
from flask import Flask, jsonify, request, render_template_string
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# ============================================================================
# Упражнение 1: Настройка базы данных в Flask
# ============================================================================

# Создаём приложение
app = Flask(__name__)

# Вариант 1: SQLite (для разработки)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация SQLAlchemy
db = SQLAlchemy(app)

# ============================================================================
# Упражнение 2: Создание моделей с SQLAlchemy
# ============================================================================

class User(db.Model):
    """Модель пользователя"""
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
            'is_active': self.is_active,
            'is_admin': self.is_admin
        }


class Author(db.Model):
    """Модель автора"""
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
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'bio': self.bio,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'articles_count': len(self.articles)
        }


class Article(db.Model):
    """Модель статьи"""
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
    
    def __repr__(self):
        return f'<Article {self.title}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'content': self.content,
            'excerpt': self.excerpt,
            'published': self.published,
            'view_count': self.view_count,
            'author': self.author.name if self.author else None,
            'category': self.category.name if self.category else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Category(db.Model):
    """Модель категории"""
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True)
    description = db.Column(db.String(200))
    
    def __repr__(self):
        return f'<Category {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
            'articles_count': len(self.articles)
        }


class Tag(db.Model):
    """Модель тега (для связи многие-ко-многим)"""
    __tablename__ = 'tags'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    slug = db.Column(db.String(50), unique=True)
    
    def __repr__(self):
        return f'<Tag {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug
        }


# Таблица связи для многие-ко-многим
article_tags = db.Table('article_tags',
    db.Column('article_id', db.Integer, db.ForeignKey('articles.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

# Добавляем связь many-to-many к Article
Article.tags = db.relationship('Tag', secondary=article_tags, backref=db.backref('articles', lazy='dynamic'))


# ============================================================================
# Упражнение 3: CRUD - Создание данных (Create)
# ============================================================================

def create_user(username, email, password_hash):
    """Создание одного пользователя"""
    new_user = User(username=username, email=email, password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()
    return new_user


def create_multiple_users():
    """Создание нескольких пользователей"""
    users_data = [
        {'username': 'admin', 'email': 'admin@example.com', 'password_hash': 'hash1', 'is_admin': True},
        {'username': 'john', 'email': 'john@example.com', 'password_hash': 'hash2'},
        {'username': 'jane', 'email': 'jane@example.com', 'password_hash': 'hash3'},
        {'username': 'bob', 'email': 'bob@example.com', 'password_hash': 'hash4'},
        {'username': 'alice', 'email': 'alice@example.com', 'password_hash': 'hash5'},
    ]
    
    users = []
    for data in users_data:
        user = User(**data)
        db.session.add(user)
        users.append(user)
    
    db.session.commit()
    return users


def create_author(name, email, bio=''):
    """Создание автора"""
    author = Author(name=name, email=email, bio=bio)
    db.session.add(author)
    db.session.commit()
    return author


def create_article(title, content, author_id, slug=None, category_id=None, published=False):
    """Создание статьи"""
    if slug is None:
        slug = title.lower().replace(' ', '-')
    
    article = Article(
        title=title,
        slug=slug,
        content=content,
        author_id=author_id,
        category_id=category_id,
        published=published
    )
    db.session.add(article)
    db.session.commit()
    return article


def create_category(name, description=''):
    """Создание категории"""
    category = Category(
        name=name,
        slug=name.lower().replace(' ', '-'),
        description=description
    )
    db.session.add(category)
    db.session.commit()
    return category


def create_tag(name):
    """Создание тега"""
    tag = Tag(
        name=name,
        slug=name.lower().replace(' ', '-')
    )
    db.session.add(tag)
    db.session.commit()
    return tag


def safe_create_user(username, email, password_hash):
    """Создание пользователя с проверкой"""
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


# ============================================================================
# Упражнение 4: CRUD - Чтение данных (Read)
# ============================================================================

def get_user_by_id(user_id):
    """Получение пользователя по ID"""
    user = db.session.get(User, user_id)
    return user


def get_user_by_username(username):
    """Получение пользователя по имени"""
    user = User.query.filter_by(username=username).first()
    return user


def get_user_by_email(email):
    """Получение пользователя по email"""
    user = User.query.filter_by(email=email).first()
    return user


def get_all_users():
    """Получение всех пользователей"""
    users = User.query.all()
    return users


def get_active_users():
    """Получение активных пользователей"""
    users = User.query.filter_by(is_active=True).all()
    return users


def get_admin_users():
    """Получение администраторов"""
    users = User.query.filter_by(is_admin=True).all()
    return users


def get_users_paginated(page=1, per_page=10):
    """Получение пользователей с пагинацией"""
    pagination = User.query.paginate(page=page, per_page=per_page)
    return {
        'items': pagination.items,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
        'has_next': pagination.has_next,
        'has_prev': pagination.has_prev,
        'per_page': per_page
    }


def search_users(search_term):
    """Поиск пользователей по имени или email"""
    from sqlalchemy import or_
    
    users = User.query.filter(
        or_(
            User.username.like(f'%{search_term}%'),
            User.email.like(f'%{search_term}%')
        )
    ).all()
    
    return users


def get_users_sorted(sort_by='username', descending=False):
    """Получение отсортированных пользователей"""
    if descending:
        users = User.query.order_by(getattr(User, sort_by).desc()).all()
    else:
        users = User.query.order_by(getattr(User, sort_by)).all()
    return users


def get_first_n_users(n=5):
    """Получение первых N пользователей"""
    users = User.query.limit(n).all()
    return users


def get_article_by_slug(slug):
    """Получение статьи по slug"""
    article = Article.query.filter_by(slug=slug).first()
    return article


def get_published_articles():
    """Получение опубликованных статей"""
    articles = Article.query.filter_by(published=True).order_by(Article.created_at.desc()).all()
    return articles


def get_articles_by_author(author_id):
    """Получение статей автора"""
    articles = Article.query.filter_by(author_id=author_id).all()
    return articles


def get_articles_by_category(category_id):
    """Получение статей категории"""
    articles = Article.query.filter_by(category_id=category_id).all()
    return articles


def get_articles_with_filters(category=None, author=None, published=None, search=None):
    """Получение статей с фильтрами"""
    query = Article.query
    
    if category:
        query = query.filter_by(category_id=category)
    if author:
        query = query.filter_by(author_id=author)
    if published is not None:
        query = query.filter_by(published=published)
    if search:
        from sqlalchemy import or_
        query = query.filter(
            or_(
                Article.title.like(f'%{search}%'),
                Article.content.like(f'%{search}%')
            )
        )
    
    return query.order_by(Article.created_at.desc()).all()


# ============================================================================
# Упражнение 5: CRUD - Обновление данных (Update)
# ============================================================================

def update_user(user_id, **kwargs):
    """Обновление пользователя"""
    user = db.session.get(User, user_id)
    
    if not user:
        return None, "Пользователь не найден"
    
    # Обновление полей
    for key, value in kwargs.items():
        if hasattr(user, key):
            setattr(user, key, value)
    
    db.session.commit()
    return user, None


def update_user_email(user_id, new_email):
    """Обновление email пользователя"""
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


def update_user_status(user_id, is_active):
    """Обновление статуса пользователя"""
    user = db.session.get(User, user_id)
    
    if not user:
        return None, "Пользователь не найден"
    
    user.is_active = is_active
    db.session.commit()
    
    return user, None


def deactivate_inactive_users():
    """Деактивация неактивных пользователей (массовое обновление)"""
    # Например, деактивировать пользователей, которые не входили более 30 дней
    # Здесь просто для примера деактивируем всех неактивных
    updated_count = User.query.filter_by(is_active=False).update({'is_active': False})
    db.session.commit()
    return updated_count


def increment_article_views(article_id):
    """Увеличение счётчика просмотров статьи"""
    article = db.session.get(Article, article_id)
    
    if not article:
        return None, "Статья не найдена"
    
    article.view_count += 1
    db.session.commit()
    
    return article, None


def publish_article(article_id):
    """Публикация статьи"""
    article = db.session.get(Article, article_id)
    
    if not article:
        return None, "Статья не найдена"
    
    article.published = True
    article.published_at = datetime.utcnow()
    db.session.commit()
    
    return article, None


# ============================================================================
# Упражнение 6: CRUD - Удаление данных (Delete)
# ============================================================================

def delete_user(user_id):
    """Удаление пользователя"""
    user = db.session.get(User, user_id)
    
    if not user:
        return False, "Пользователь не найден"
    
    db.session.delete(user)
    db.session.commit()
    
    return True, None


def delete_article(article_id):
    """Удаление статьи"""
    article = db.session.get(Article, article_id)
    
    if not article:
        return False, "Статья не найден"
    
    db.session.delete(article)
    db.session.commit()
    
    return True, None


def delete_inactive_users():
    """Удаление неактивных пользователей (массовое удаление)"""
    deleted_count = User.query.filter_by(is_active=False).delete()
    db.session.commit()
    return deleted_count


# ============================================================================
# Упражнение 7: Агрегатные функции и статистика
# ============================================================================

from sqlalchemy import func, count

def get_user_stats():
    """Получение статистики по пользователям"""
    # Количество пользователей
    total = db.session.query(func.count(User.id)).scalar()
    
    # Количество активных пользователей
    active_count = db.session.query(func.count(User.id)).filter_by(is_active=True).scalar()
    
    # Количество администраторов
    admin_count = db.session.query(func.count(User.id)).filter_by(is_admin=True).scalar()
    
    # Группировка по статусу
    stats = db.session.query(
        User.is_active,
        func.count(User.id)
    ).group_by(User.is_active).all()
    
    return {
        'total': total,
        'active': active_count,
        'admin': admin_count,
        'stats': stats
    }


def get_article_stats():
    """Получение статистики по статьям"""
    total = db.session.query(func.count(Article.id)).scalar()
    published = db.session.query(func.count(Article.id)).filter_by(published=True).scalar()
    
    # Среднее количество просмотров
    avg_views = db.session.query(func.avg(Article.view_count)).scalar()
    
    # Максимальное количество просмотров
    max_views = db.session.query(func.max(Article.view_count)).scalar()
    
    # Статистика по категориям
    category_stats = db.session.query(
        Category.name,
        func.count(Article.id)
    ).join(Article).group_by(Category.name).all()
    
    return {
        'total': total,
        'published': published,
        'avg_views': avg_views,
        'max_views': max_views,
        'category_stats': category_stats
    }


def get_author_with_most_articles():
    """Получение автора с наибольшим количеством статей"""
    result = db.session.query(
        Author.name,
        func.count(Article.id).label('article_count')
    ).join(Article).group_by(Author.id).order_by(func.count(Article.id).desc()).first()
    
    return result


# ============================================================================
# Упражнение 8: Связи между моделями
# ============================================================================

def add_tag_to_article(article_id, tag_id):
    """Добавление тега к статье"""
    article = db.session.get(Article, article_id)
    tag = db.session.get(Tag, tag_id)
    
    if article and tag:
        article.tags.append(tag)
        db.session.commit()
        return True, None
    return False, "Статья или тег не найдены"


def remove_tag_from_article(article_id, tag_id):
    """Удаление тега со статьи"""
    article = db.session.get(Article, article_id)
    tag = db.session.get(Tag, tag_id)
    
    if article and tag:
        article.tags.remove(tag)
        db.session.commit()
        return True, None
    return False, "Статья или тег не найдены"


def get_articles_by_tag(tag_id):
    """Получение статей по тегу"""
    tag = db.session.get(Tag, tag_id)
    if tag:
        return tag.articles.all()
    return []


def get_popular_articles(limit=5):
    """Получение популярных статей"""
    articles = Article.query.filter_by(published=True).order_by(
        Article.view_count.desc()
    ).limit(limit).all()
    return articles


def get_recent_articles(limit=5):
    """Получение последних статей"""
    articles = Article.query.filter_by(published=True).order_by(
        Article.created_at.desc()
    ).limit(limit).all()
    return articles


# ============================================================================
# API endpoints
# ============================================================================

@app.route('/')
def index():
    """Главная страница"""
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Flask Database - Практика</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            h1 { color: #333; }
            .endpoint { background: #f4f4f4; padding: 10px; margin: 10px 0; border-radius: 5px; }
            a { color: #007bff; }
        </style>
    </head>
    <body>
        <h1>Практическое занятие 35: Flask - интеграция с БД</h1>
        <h2>API Endpoints:</h2>
        
        <div class="endpoint">
            <h3>Пользователи:</h3>
            <ul>
                <li><a href="/api/users">GET /api/users</a> - Все пользователи</li>
                <li><a href="/api/users/1">GET /api/users/1</a> - Пользователь по ID</li>
                <li><a href="/api/users/stats">GET /api/users/stats</a> - Статистика</li>
            </ul>
        </div>
        
        <div class="endpoint">
            <h3>Статьи:</h3>
            <ul>
                <li><a href="/api/articles">GET /api/articles</a> - Все статьи</li>
                <li><a href="/api/articles/published">GET /api/articles/published</a> - Опубликованные</li>
                <li><a href="/api/articles/popular">GET /api/articles/popular</a> - Популярные</li>
            </ul>
        </div>
        
        <div class="endpoint">
            <h3>Авторы:</h3>
            <ul>
                <li><a href="/api/authors">GET /api/authors</a> - Все авторы</li>
            </ul>
        </div>
        
        <div class="endpoint">
            <h3>Категории:</h3>
            <ul>
                <li><a href="/api/categories">GET /api/categories</a> - Все категории</li>
            </ul>
        </div>
        
        <h2>Инициализация БД:</h2>
        <ul>
            <li><a href="/init-db">GET /init-db</a> - Создать таблицы и добавить тестовые данные</li>
        </ul>
    </body>
    </html>
    ''')


@app.route('/init-db')
def init_db():
    """Инициализация базы данных и добавление тестовых данных"""
    # Создание всех таблиц
    with app.app_context():
        db.create_all()
        
        # Добавление категорий
        if Category.query.count() == 0:
            categories = [
                create_category('Программирование', 'Статьи о программировании'),
                create_category('Веб-разработка', 'Статьи о веб-разработке'),
                create_category('Базы данных', 'Статьи о базах данных'),
                create_category('DevOps', 'Статьи о DevOps'),
            ]
        
        # Добавление авторов
        if Author.query.count() == 0:
            authors = [
                create_author('Иван Иванов', 'ivan@example.com', 'Опытный разработчик'),
                create_author('Пётр Петров', 'petr@example.com', 'Веб-разработчик'),
                create_author('Анна Сидорова', 'anna@example.com', 'DevOps инженер'),
            ]
        
        # Добавление тегов
        if Tag.query.count() == 0:
            tags = [
                create_tag('Python'),
                create_tag('Flask'),
                create_tag('Django'),
                create_tag('SQL'),
                create_tag('JavaScript'),
            ]
        
        # Добавление статей
        if Article.query.count() == 0:
            author1 = Author.query.filter_by(name='Иван Иванов').first()
            author2 = Author.query.filter_by(name='Пётр Петров').first()
            cat1 = Category.query.filter_by(name='Программирование').first()
            cat2 = Category.query.filter_by(name='Веб-разработка').first()
            
            articles = [
                create_article(
                    'Введение в Python',
                    'Python - это высокоуровневый язык программирования...',
                    author1.id, 'intro-python', cat1.id, True
                ),
                create_article(
                    'Flask для начинающих',
                    'Flask - это микрофреймворк для веб-разработки на Python...',
                    author1.id, 'flask-beginners', cat2.id, True
                ),
                create_article(
                    'Работа с базами данных в Flask',
                    'В этом руководстве мы рассмотрим работу с SQLAlchemy...',
                    author2.id, 'flask-database', cat2.id, True
                ),
                create_article(
                    'Основы Django',
                    'Django - это высокоуровневый фреймворк...',
                    author2.id, 'django-basics', cat1.id, True
                ),
            ]
            
            # Добавление тегов к статьям
            article1 = Article.query.filter_by(slug='intro-python').first()
            article2 = Article.query.filter_by(slug='flask-beginners').first()
            
            tag_python = Tag.query.filter_by(name='Python').first()
            tag_flask = Tag.query.filter_by(name='Flask').first()
            tag_django = Tag.query.filter_by(name='Django').first()
            
            if tag_python:
                article1.tags.append(tag_python)
            if tag_flask:
                article2.tags.append(tag_flask)
            if tag_django:
                article1.tags.append(tag_django)
            
            db.session.commit()
        
        return '''
        <h1>База данных инициализирована!</h1>
        <p>Добавлены тестовые данные:</p>
        <ul>
            <li>Категории: {}</li>
            <li>Авторы: {}</li>
            <li>Теги: {}</li>
            <li>Статьи: {}</li>
        </ul>
        <a href="/">На главную</a>
        '''.format(
            Category.query.count(),
            Author.query.count(),
            Tag.query.count(),
            Article.query.count()
        )


# API: Пользователи
@app.route('/api/users')
def api_get_users():
    """Получение всех пользователей"""
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


@app.route('/api/users/<int:user_id>')
def api_get_user(user_id):
    """Получение пользователя по ID"""
    user = db.session.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    return jsonify({'error': 'Пользователь не найден'}), 404


@app.route('/api/users/stats')
def api_get_user_stats():
    """Получение статистики по пользователям"""
    return jsonify(get_user_stats())


# API: Статьи
@app.route('/api/articles')
def api_get_articles():
    """Получение всех статей"""
    articles = Article.query.all()
    return jsonify([article.to_dict() for article in articles])


@app.route('/api/articles/published')
def api_get_published_articles():
    """Получение опубликованных статей"""
    articles = get_published_articles()
    return jsonify([article.to_dict() for article in articles])


@app.route('/api/articles/popular')
def api_get_popular_articles():
    """Получение популярных статей"""
    articles = get_popular_articles()
    return jsonify([article.to_dict() for article in articles])


@app.route('/api/articles/<int:article_id>')
def api_get_article(article_id):
    """Получение статьи по ID"""
    article = db.session.get(Article, article_id)
    if article:
        return jsonify(article.to_dict())
    return jsonify({'error': 'Статья не найдена'}), 404


# API: Авторы
@app.route('/api/authors')
def api_get_authors():
    """Получение всех авторов"""
    authors = Author.query.all()
    return jsonify([author.to_dict() for author in authors])


@app.route('/api/authors/<int:author_id>')
def api_get_author(author_id):
    """Получение автора по ID"""
    author = db.session.get(Author, author_id)
    if author:
        return jsonify(author.to_dict())
    return jsonify({'error': 'Автор не найден'}), 404


@app.route('/api/authors/<int:author_id>/articles')
def api_get_author_articles(author_id):
    """Получение статей автора"""
    articles = get_articles_by_author(author_id)
    return jsonify([article.to_dict() for article in articles])


# API: Категории
@app.route('/api/categories')
def api_get_categories():
    """Получение всех категорий"""
    categories = Category.query.all()
    return jsonify([category.to_dict() for category in categories])


@app.route('/api/categories/<int:category_id>')
def api_get_category(category_id):
    """Получение категории по ID"""
    category = db.session.get(Category, category_id)
    if category:
        return jsonify(category.to_dict())
    return jsonify({'error': 'Категория не найдена'}), 404


@app.route('/api/categories/<int:category_id>/articles')
def api_get_category_articles(category_id):
    """Получение статей категории"""
    articles = get_articles_by_category(category_id)
    return jsonify([article.to_dict() for article in articles])


# API: Теги
@app.route('/api/tags')
def api_get_tags():
    """Получение всех тегов"""
    tags = Tag.query.all()
    return jsonify([tag.to_dict() for tag in tags])


@app.route('/api/tags/<int:tag_id>')
def api_get_tag(tag_id):
    """Получение тега по ID"""
    tag = db.session.get(Tag, tag_id)
    if tag:
        return jsonify(tag.to_dict())
    return jsonify({'error': 'Тег не найден'}), 404


@app.route('/api/tags/<int:tag_id>/articles')
def api_get_tag_articles(tag_id):
    """Получение статей по тегу"""
    articles = get_articles_by_tag(tag_id)
    return jsonify([article.to_dict() for article in articles])


# ============================================================================
# Запуск приложения
# ============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("Запуск Flask-приложения с базой данных")
    print("=" * 60)
    print("Откройте в браузере: http://127.0.0.1:5000/")
    print("=" * 60)
    
    app.run(debug=True)
