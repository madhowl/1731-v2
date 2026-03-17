# Практическое занятие 39: Аутентификация и авторизация

## Аутентификация и авторизация в веб-приложениях

### Цель занятия:
Научиться реализовывать системы аутентификации и авторизации в веб-приложениях, работать с сессиями, токенами, управлять правами доступа.

### Задачи:
1. Понять разницу между аутентификацией и авторизацией
2. Реализовать регистрацию и вход пользователей
3. Использовать Flask-Login и Django Auth
4. Реализовать JWT-аутентификацию
5. Управлять правами доступа

### План работы:
1. Основы аутентификации и авторизации
2. Аутентификация в Flask
3. Аутентификация в Django
4. JWT-токены
5. Управление правами
6. Практические задания

---

## 1. Основы аутентификации и авторизации

### Основные понятия

**Аутентификация (Authentication)** - процесс проверки личности пользователя. Отвечает на вопрос "Кто вы?"

**Авторизация (Authorization)** - процесс определения прав доступа. Отвечает на вопрос "Что вам разрешено делать?"

### Пример 1: Разница между аутентификацией и авторизацией

```
Аутентификация:
- Пользователь вводит логин и пароль
- Система проверяет, что такие данные есть в базе
- Пользователь получает доступ к системе

Авторизация:
- Аутентифицированный пользователь пытается редактировать статью
- Система проверяет, является ли пользователь автором статьи
- Если да - разрешает редактирование, если нет - запрещает
```

---

## 2. Аутентификация в Flask

### Пример 2: Установка и настройка Flask-Login

```bash
pip install flask-login flask-bcrypt
```

```python
# app.py

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице'
login_manager.login_message_category = 'info'

# Модель пользователя
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Создание базы данных
with app.app_context():
    db.create_all()
```

### Пример 3: Регистрация пользователя

```python
# routes.py

from flask import Flask, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user
from app import db, app
from app.models import User

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Проверка данных
        errors = []
        
        if User.query.filter_by(username=username).first():
            errors.append('Имя пользователя уже занято')
        
        if User.query.filter_by(email=email).first():
            errors.append('Email уже используется')
        
        if password != confirm_password:
            errors.append('Пароли не совпадают')
        
        if len(password) < 6:
            errors.append('Пароль должен быть минимум 6 символов')
        
        if errors:
            for error in errors:
                flash(error, 'danger')
            return redirect(url_for('register'))
        
        # Создание пользователя
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Регистрация успешна! Теперь вы можете войти.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')
```

### Пример 4: Вход и выход пользователя

```python
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user, remember=request.form.get('remember'))
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Неверный email или пароль', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
```

### Пример 5: Защищённые маршруты

```python
from flask_login import login_required, current_user
from functools import wraps

# Декоратор для проверки прав администратора
def admin_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            flash('Доступ запрещён', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

# Примеры защищённых маршрутов
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@app.route('/admin')
@admin_required
def admin_panel():
    return render_template('admin.html')

# Проверка авторства
@app.route('/article/<int:article_id>/edit')
@login_required
def edit_article(article_id):
    article = Article.query.get_or_404(article_id)
    
    if article.author_id != current_user.id and not current_user.is_admin:
        flash('У вас нет прав для редактирования этой статьи', 'danger')
        return redirect(url_for('article_detail', article_id=article_id))
    
    return render_template('edit_article.html', article=article)
```

---

## 3. Аутентификация в Django

### Пример 6: Использование встроенной аутентификации Django

```python
# Django views для аутентификации

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
                messages.error(request, 'Неверное имя пользователя или пароль')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def user_logout(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы')
    return redirect('home')
```

### Пример 7: Кастомная форма регистрации

```python
# forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        
        if commit:
            user.save()
            Profile.objects.create(user=user)
        
        return user
```

### Пример 8: Права доступа в Django

```python
# views.py

from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from .models import Article

# Только для авторизованных пользователей
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
    
    # Проверка, что пользователь - автор статьи или админ
    if article.author != request.user and not request.user.is_staff:
        raise PermissionDenied("У вас нет прав для редактирования этой статьи")
    
    return render(request, 'edit_article.html', {'article': article})
```

---

## 4. JWT-токены

### Пример 9: JWT-аутентификация во Flask

```bash
pip install pyjwt
```

```python
# auth.py

import jwt
import datetime
from functools import wraps
from flask import request, jsonify, current_app

def create_token(user_id):
    """Создание JWT-токена"""
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return token

def decode_token(token):
    """Расшифровка JWT-токена"""
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
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
        
        # Добавляем user_id в kwargs
        kwargs['user_id'] = user_id
        return f(*args, **kwargs)
    
    return decorated

# Использование
@app.route('/api/protected')
@token_required
def protected_route(user_id):
    return jsonify({'message': f'Доступ разрешён для пользователя {user_id}'})
```

### Пример 10: Регистрация и вход с JWT

```python
# auth_routes.py

@app.route('/api/register', methods=['POST'])
def register_api():
    data = request.get_json()
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    # Проверка данных
    if User.query.filter_by(username=username).first():
        return jsonify({'message': 'Имя пользователя занято'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'message': 'Email уже используется'}), 400
    
    # Создание пользователя
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    
    # Создание токена
    token = create_token(user.id)
    
    return jsonify({
        'message': 'Пользователь создан',
        'token': token,
        'user': {'id': user.id, 'username': user.username}
    }), 201

@app.route('/api/login', methods=['POST'])
def login_api():
    data = request.get_json()
    
    email = data.get('email')
    password = data.get('password')
    
    user = User.query.filter_by(email=email).first()
    
    if not user or not user.check_password(password):
        return jsonify({'message': 'Неверные учётные данные'}), 401
    
    token = create_token(user.id)
    
    return jsonify({
        'message': 'Вход выполнен',
        'token': token,
        'user': {'id': user.id, 'username': user.username}
    })
```

---

## 5. Управление правами

### Пример 11: Система прав в Django

```python
# Модель профиля с дополнительными правами

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
    
    @property
    def is_moderator(self):
        return self.role in [self.Role.MODERATOR, self.Role.ADMIN]
    
    @property
    def is_admin(self):
        return self.role == self.Role.ADMIN
```

### Пример 12: Проверка прав в Django

```python
# В представлениях

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    
    # Проверка прав: автор комментария, автор статьи или модератор
    profile = request.user.profile
    if (comment.author != request.user and 
        comment.article.author != request.user and
        not profile.is_moderator):
        raise PermissionDenied("У вас нет прав для удаления этого комментария")
    
    comment.delete()
    return redirect('article_detail', slug=comment.article.slug)

# Использование Mixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class ArticleEditMixin(UserPassesTestMixin):
    def test_func(self):
        article = self.get_object()
        return article.author == self.request.user or self.request.user.profile.is_moderator
```

---

## 6. Практические задания

### Задание 1: Регистрация и вход
Создайте систему регистрации и входа пользователей с использованием Flask-Login.

### Задание 2: Профиль пользователя
Создайте страницу профиля пользователя с возможностью редактирования данных.

### Задание 3: Права доступа
Реализуйте систему прав доступа: автор может редактировать/удалять свои статьи, модератор - все статьи.

### Задание 4: JWT-аутентификация
Добавьте JWT-аутентификацию для REST API.

### Задание 5: Сброс пароля
Реализуйте функционал сброса пароля по email.

---

## Дополнительные задания

### Задание 6: Социальная аутентификация
Добавьте вход через Google или GitHub.

### Задание 7: Двухфакторная аутентификация
Реализуйте 2FA с отправкой кода по email.

### Задание 8: Блокировка пользователей
Добавьте функционал блокировки пользователей за нарушения.

---

## Контрольные вопросы:
1. В чём разница между аутентификацией и авторизацией?
2. Что такое сессия пользователя?
3. Как работает Flask-Login?
4. Что такое JWT-токен и как он используется?
5. Какие способы аутентификации вы знаете?
6. Как реализовать проверку прав доступа?
7. Что такое хэширование паролей?
8. Как защитить пароли в базе данных?
