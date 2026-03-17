# -*- coding: utf-8 -*-
"""
Практическое занятие 39: Аутентификация и авторизация
Решение упражнений

В этом файле представлены решения для всех упражнений практического занятия
по аутентификации и авторизации.

Для запуска:
    pip install flask flask-login flask-bcrypt pyjwt
    python practical_39_authentication_authorization_solution.py
"""

import os
import jwt
import datetime
from functools import wraps
from flask import Flask, request, jsonify, abort, render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt

# ============================================================================
# Настройка Flask приложения
# ============================================================================

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице'
login_manager.login_message_category = 'info'

# ============================================================================
# Упражнение 1: Модель пользователя
# ============================================================================

class User(db.Model, UserMixin):
    """Модель пользователя"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    def set_password(self, password):
        """Установка хэша пароля"""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """Проверка пароля"""
        return bcrypt.check_password_hash(self.password, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


@login_manager.user_loader
def load_user(user_id):
    """Загрузка пользователя по ID"""
    return User.query.get(int(user_id))


# ============================================================================
# Упражнение 2: Регистрация пользователя
# ============================================================================

@app.route('/api/register', methods=['POST'])
def register_api():
    """API регистрация пользователя"""
    data = request.get_json()
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    # Проверка данных
    if not username or not email or not password:
        return jsonify({'message': 'Все поля обязательны'}), 400
    
    if len(password) < 6:
        return jsonify({'message': 'Пароль должен быть минимум 6 символов'}), 400
    
    # Проверка уникальности
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Имя пользователя уже занято'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email уже используется'}), 400
    
    # Создание пользователя
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({
        'message': 'Пользователь создан',
        'user': user.to_dict()
    }), 201


# ============================================================================
# Упражнение 3: Вход и выход пользователя
# ============================================================================

@app.route('/api/login', methods=['POST'])
def login_api():
    """API вход пользователя"""
    data = request.get_json()
    
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'message': 'Email и пароль обязательны'}), 400
    
    user = User.query.filter_by(email=email).first()
    
    if not user or not user.check_password(password):
        return jsonify({'message': 'Неверные учётные данные'}), 401
    
    if not user.is_active:
        return jsonify({'message': 'Аккаунт деактивирован'}), 401
    
    # Создание токена
    token = create_token(user.id)
    
    return jsonify({
        'message': 'Вход выполнен',
        'token': token,
        'user': user.to_dict()
    })


@app.route('/api/logout', methods=['POST'])
@login_required
def logout_api():
    """API выход пользователя"""
    return jsonify({'message': 'Вы вышли из системы'})


# ============================================================================
# Упражнение 4: JWT токены
# ============================================================================

def create_token(user_id):
    """Создание JWT токена"""
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
    return token


def decode_token(token):
    """Расшифровка JWT токена"""
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def token_required(f):
    """Декоратор для проверки токена"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        
        if not token:
            return jsonify({'message': 'Токен отсутствует'}), 401
        
        user_id = decode_token(token)
        if not user_id:
            return jsonify({'message': 'Неверный или истёкший токен'}), 401
        
        user = User.query.get(user_id)
        if not user or not user.is_active:
            return jsonify({'message': 'Пользователь не найден или деактивирован'}), 401
        
        kwargs['current_user'] = user
        return f(*args, **kwargs)
    
    return decorated


# ============================================================================
# Упражнение 5: Защищённые маршруты
# ============================================================================

@app.route('/api/protected')
@token_required
def protected_route(current_user):
    """Защищённый маршрут"""
    return jsonify({
        'message': f'Доступ разрешён для пользователя {current_user.username}',
        'user': current_user.to_dict()
    })


@app.route('/api/profile')
@login_required
def get_profile():
    """Получение профиля текущего пользователя"""
    return jsonify(current_user.to_dict())


@app.route('/api/admin')
@token_required
def admin_route(current_user):
    """Защищённый маршрут для админов"""
    if not current_user.is_admin:
        return jsonify({'message': 'Доступ запрещён'}), 403
    
    return jsonify({
        'message': 'Добро пожаловать в админ-панель',
        'users_count': User.query.count()
    })


# ============================================================================
# Упражнение 6: Проверка авторства
# ============================================================================

# Модель статьи для примера проверки авторства
class Article(db.Model):
    """Модель статьи"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_published = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    author = db.relationship('User', backref='articles')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'author_id': self.author_id,
            'is_published': self.is_published,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


@app.route('/api/articles/<int:article_id>', methods=['PUT'])
@token_required
def update_article(article_id):
    """Обновление статьи с проверкой авторства"""
    article = Article.query.get(article_id)
    
    if not article:
        return jsonify({'message': 'Статья не найдена'}), 404
    
    # Проверка авторства или админских прав
    if article.author_id != current_user.id and not current_user.is_admin:
        return jsonify({'message': 'У вас нет прав для редактирования этой статьи'}), 403
    
    data = request.get_json()
    article.title = data.get('title', article.title)
    article.content = data.get('content', article.content)
    db.session.commit()
    
    return jsonify({
        'message': 'Статья обновлена',
        'article': article.to_dict()
    })


@app.route('/api/articles/<int:article_id>', methods=['DELETE'])
@token_required
def delete_article(article_id):
    """Удаление статьи с проверкой авторства"""
    article = Article.query.get(article_id)
    
    if not article:
        return jsonify({'message': 'Статья не найдена'}), 404
    
    # Проверка авторства или админских прав
    if article.author_id != current_user.id and not current_user.is_admin:
        return jsonify({'message': 'У вас нет прав для удаления этой статьи'}), 403
    
    db.session.delete(article)
    db.session.commit()
    
    return jsonify({'message': 'Статья удалена'})


# ============================================================================
# Главная страница
# ============================================================================

@app.route('/')
def index():
    """Главная страница"""
    return jsonify({
        'name': 'Authentication API',
        'version': '1.0',
        'endpoints': {
            'auth': {
                'POST /api/register': 'Регистрация пользователя',
                'POST /api/login': 'Вход пользователя',
                'POST /api/logout': 'Выход пользователя',
            },
            'protected': {
                'GET /api/protected': 'Защищённый маршрут',
                'GET /api/profile': 'Профиль пользователя',
                'GET /api/admin': 'Админ-панель',
            },
            'articles': {
                'PUT /api/articles/<id>': 'Обновить статью',
                'DELETE /api/articles/<id>': 'Удалить статью',
            }
        }
    })


# ============================================================================
# Django примеры кода
# ============================================================================

DJANGO_AUTH_EXAMPLES = '''
# === Django Аутентификация ===

# blog/views.py

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация успешна!')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Добро пожаловать, {username}!')
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required
def user_logout(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы')
    return redirect('home')


# === Права доступа в Django ===

from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied


# Только для авторизованных
@login_required
def profile(request):
    return render(request, 'profile.html')


# Только для администраторов
@user_passes_test(lambda u: u.is_staff)
def admin_panel(request):
    return render(request, 'admin.html')


# С правами на конкретное действие
@permission_required('blog.change_article')
def edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    return render(request, 'edit_article.html', {'article': article})


# Проверка авторства
@login_required
def edit_article(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    
    if article.author != request.user and not request.user.is_staff:
        raise PermissionDenied("У вас нет прав для редактирования этой статьи")
    
    return render(request, 'edit_article.html', {'article': article})


# === Кастомная форма регистрации ===

# blog/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        
        if commit:
            user.save()
        
        return user


# === Профиль пользователя ===

# models.py

from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    class Role(models.TextChoices):
        USER = 'user', 'Пользователь'
        MODERATOR = 'moderator', 'Модератор'
        ADMIN = 'admin', 'Администратор'
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    
    def __str__(self):
        return f'{self.user.username} Profile'
'''

# ============================================================================
# Инициализация и запуск
# ============================================================================

def init_db():
    """Инициализация базы данных"""
    with app.app_context():
        db.create_all()
        
        # Создание администратора, если его нет
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin', email='admin@example.com', is_admin=True)
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Создан администратор: admin / admin123")


def main():
    """Запуск приложения"""
    print("=" * 70)
    print("Практическое занятие 39: Аутентификация и авторизация")
    print("=" * 70)
    
    init_db()
    
    print()
    print("API доступно по адресу: http://127.0.0.1:5000/")
    print()
    print("Endpoints:")
    print("  POST /api/register  - Регистрация")
    print("  POST /api/login    - Вход")
    print("  POST /api/logout   - Выход")
    print("  GET  /api/profile  - Профиль")
    print("  GET  /api/protected - Защищённый маршрут")
    print("  GET  /api/admin    - Админ-панель")
    print()
    print("=" * 70)


if __name__ == '__main__':
    main()
    app.run(debug=True)
