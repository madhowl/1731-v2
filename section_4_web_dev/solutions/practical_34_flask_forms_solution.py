# -*- coding: utf-8 -*-
"""
Практическое занятие 34: Flask - формы
Решение упражнений

В этом файле представлены решения для всех упражнений практического занятия
по работе с формами в Flask.

Для запуска:
    python practical_34_flask_forms_solution.py

Требования:
    pip install flask flask-wtf email_validator
"""

from flask import Flask, request, render_template_string, redirect, url_for, flash, jsonify
from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, SubmitField, EmailField, TextAreaField,
    IntegerField, BooleanField, SelectField, FloatField, FileField
)
from wtforms.validators import (
    DataRequired, Email, Length, EqualTo, ValidationError, 
    NumberRange, Regexp, Optional
)
from wtforms import FormField, FieldList
import os

# ============================================================================
# Упражнение 1: Простая форма без библиотек
# ============================================================================

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'

# HTML-шаратной связи
CONTACT_FORM_TEMPLATE = '''
<!DOCTYPE html>
<html>
<headблон формы об>
    <title>Контактная форма</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
        form { background: #f4f4f4; padding: 20px; border-radius: 5px; }
        label { display: block; margin-top: 10px; font-weight: bold; }
        input, textarea { width: 100%; padding: 8px; margin-top: 5px; box-sizing: border-box; }
        button { margin-top: 15px; padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
        .error { color: red; font-size: 14px; }
        .success { color: green; font-size: 16px; }
    </style>
</head>
<body>
    <h1>Контактная форма</h1>
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <p class="{{ category }}">{{ message }}</p>
            {% endfor %}
        {% endif %}
    {% endwith %}
    {% if success %}
        <p class="success">Спасибо! Ваше сообщение отправлено.</p>
    {% endif %}
    <form method="POST">
        <label for="name">Имя:</label>
        <input type="text" name="name" id="name" value="{{ name or '' }}" required>
        
        <label for="email">Email:</label>
        <input type="email" name="email" id="email" value="{{ email or '' }}" required>
        
        <label for="subject">Тема:</label>
        <input type="text" name="subject" id="subject" value="{{ subject or '' }}">
        
        <label for="message">Сообщение:</label>
        <textarea name="message" id="message" rows="5" required>{{ message or '' }}</textarea>
        
        <button type="submit">Отправить</button>
    </form>
</body>
</html>
'''

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Обработчик формы обратной связи"""
    errors = []
    name = email = subject = message = ''
    success = False
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()
        
        # Валидация данных
        if not name:
            errors.append('Имя обязательно для заполнения')
        if not email or '@' not in email:
            errors.append('Введите корректный email')
        if not message:
            errors.append('Сообщение обязательно для заполнения')
        
        if not errors:
            success = True
            print(f"Получено сообщение от {name} ({email}): {subject} - {message}")
    
    return render_template_string(CONTACT_FORM_TEMPLATE, 
                                   errors=errors, 
                                   name=name, 
                                   email=email, 
                                   subject=subject, 
                                   message=message,
                                   success=success)


# ============================================================================
# Упражнение 2: Форма регистрации пользователя
# ============================================================================

REGISTER_FORM_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Регистрация</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 500px; margin: 50px auto; padding: 20px; }
        form { background: #f4f4f4; padding: 20px; border-radius: 5px; }
        label { display: block; margin-top: 10px; font-weight: bold; }
        input { width: 100%; padding: 8px; margin-top: 5px; box-sizing: border-box; }
        button { margin-top: 15px; padding: 10px 20px; background: #28a745; color: white; border: none; cursor: pointer; }
        .error { color: red; font-size: 14px; }
        .hint { font-size: 12px; color: #666; }
        .success { color: green; font-size: 16px; }
    </style>
</head>
<body>
    <h1>Регистрация нового пользователя</h1>
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <p class="{{ category }}">{{ message }}</p>
            {% endfor %}
        {% endif %}
    {% endwith %}
    {% if success %}
        <p class="success">Регистрация успешна! Добро пожаловать, {{ username }}!</p>
    {% endif %}
    <form method="POST">
        <label for="username">Имя пользователя (логин):</label>
        <input type="text" name="username" id="username" value="{{ username or '' }}" required>
        <span class="hint">От 3 до 20 символов, только латинские буквы и цифры</span>
        
        <label for="email">Email:</label>
        <input type="email" name="email" id="email" value="{{ email or '' }}" required>
        
        <label for="password">Пароль:</label>
        <input type="password" name="password" id="password" required>
        <span class="hint">Минимум 8 символов</span>
        
        <label for="confirm_password">Подтверждение пароля:</label>
        <input type="password" name="confirm_password" id="confirm_password" required>
        
        <label for="age">Возраст:</label>
        <input type="number" name="age" id="age" min="1" max="150" value="{{ age or '' }}">
        
        <label>
            <input type="checkbox" name="terms" required>
            Я согласен с условиями использования
        </label>
        
        <button type="submit">Зарегистрироваться</button>
    </form>
</body>
</html>
'''

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Обработчик формы регистрации"""
    errors = []
    username = email = age = ''
    success = False
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        age = request.form.get('age', '').strip()
        
        # Валидация имени пользователя
        if len(username) < 3 or len(username) > 20:
            errors.append('Имя пользователя должно быть от 3 до 20 символов')
        if not username.isalnum():
            errors.append('Имя пользователя должно содержать только латинские буквы и цифры')
        
        # Валидация email
        if '@' not in email or '.' not in email.split('@')[-1]:
            errors.append('Введите корректный email')
        
        # Валидация пароля
        if len(password) < 8:
            errors.append('Пароль должен быть минимум 8 символов')
        if password != confirm_password:
            errors.append('Пароли не совпадают')
        
        # Валидация возраста
        if age:
            try:
                age_int = int(age)
                if age_int < 1 or age_int > 150:
                    errors.append('Введите корректный возраст')
            except ValueError:
                errors.append('Возраст должен быть числом')
        
        # Проверка чекбокса условий
        if not request.form.get('terms'):
            errors.append('Вы должны согласиться с условиями использования')
        
        if not errors:
            success = True
            print(f"Зарегистрирован пользователь: {username} ({email})")
    
    return render_template_string(REGISTER_FORM_TEMPLATE, 
                                   errors=errors, 
                                   username=username, 
                                   email=email, 
                                   age=age,
                                   success=success)


# ============================================================================
# Упражнение 3: WTForms - Контактная форма
# ============================================================================

class ContactForm(FlaskForm):
    """Форма обратной связи с использованием WTForms"""
    name = StringField('Имя', validators=[
        DataRequired(message='Имя обязательно'),
        Length(min=2, max=100, message='Имя должно быть от 2 до 100 символов')
    ])
    email = EmailField('Email', validators=[
        DataRequired(message='Email обязателен'),
        Email(message='Введите корректный email')
    ])
    subject = StringField('Тема', validators=[
        Length(max=200, message='Тема слишком длинная')
    ])
    message = TextAreaField('Сообщение', validators=[
        DataRequired(message='Сообщение обязательно'),
        Length(min=10, message='Сообщение слишком короткое')
    ])
    submit = SubmitField('Отправить')


@app.route('/contact-wtforms', methods=['GET', 'POST'])
def contact_wtforms():
    """Обработчик формы с WTForms"""
    form = ContactForm()
    
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        subject = form.subject.data
        message = form.message.data
        
        flash(f'Спасибо, {name}! Ваше сообщение отправлено.', 'success')
        print(f"Получено сообщение от {name} ({email}): {subject} - {message}")
        
        return redirect(url_for('contact_wtforms'))
    
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Контактная форма (WTForms)</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 500px; margin: 50px auto; padding: 20px; }
            form { background: #f4f4f4; padding: 20px; border-radius: 5px; }
            label { display: block; margin-top: 10px; font-weight: bold; }
            input, textarea { width: 100%; padding: 8px; margin-top: 5px; box-sizing: border-box; }
            button { margin-top: 15px; padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
            .error { color: red; font-size: 14px; }
            .success { color: green; }
        </style>
    </head>
    <body>
        <h1>Контактная форма (WTForms)</h1>
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <p class="{{ category }}">{{ message }}</p>
                {% endfor %}
            {% endfor %}
        {% endwith %}
        <form method="POST">
            {{ form.hidden_tag() }}
            <label>{{ form.name.label }}</label>
            {{ form.name() }}
            {% if form.name.errors %}
                {% for error in form.name.errors %}<span class="error">{{ error }}</span>{% endfor %}
            {% endif %}
            
            <label>{{ form.email.label }}</label>
            {{ form.email() }}
            {% if form.email.errors %}
                {% for error in form.email.errors %}<span class="error">{{ error }}</span>{% endfor %}
            {% endif %}
            
            <label>{{ form.subject.label }}</label>
            {{ form.subject() }}
            {% if form.subject.errors %}
                {% for error in form.subject.errors %}<span class="error">{{ error }}</span>{% endfor %}
            {% endif %}
            
            <label>{{ form.message.label }}</label>
            {{ form.message(rows=5) }}
            {% if form.message.errors %}
                {% for error in form.message.errors %}<span class="error">{{ error }}</span>{% endfor %}
            {% endif %}
            
            {{ form.submit() }}
        </form>
    </body>
    </html>
    ''', form=form)


# ============================================================================
# Упражнение 4: WTForms - Форма регистрации
# ============================================================================

class RegistrationForm(FlaskForm):
    """Форма регистрации с использованием WTForms"""
    username = StringField('Имя пользователя', validators=[
        DataRequired(),
        Length(min=3, max=20, message='От 3 до 20 символов'),
        Regexp(r'^[a-zA-Z0-9_]+$', message='Только латинские буквы, цифры и подчёркивание')
    ])
    email = EmailField('Email', validators=[
        DataRequired(),
        Email()
    ])
    password = PasswordField('Пароль', validators=[
        DataRequired(),
        Length(min=8, message='Минимум 8 символов')
    ])
    confirm_password = PasswordField('Подтвердите пароль', validators=[
        DataRequired(),
        EqualTo('password', message='Пароли должны совпадать')
    ])
    age = IntegerField('Возраст', validators=[
        NumberRange(min=1, max=150, message='Введите корректный возраст')
    ])
    terms = BooleanField('Я согласен с условиями использования', validators=[
        DataRequired(message='Вы должны согласиться')
    ])
    submit = SubmitField('Зарегистрироваться')
    
    # Кастомный валидатор для проверки уникальности username
    def validate_username(self, field):
        # В реальном приложении здесь будет проверка в базе данных
        reserved_names = ['admin', 'root', 'administrator', 'superuser']
        if field.data.lower() in reserved_names:
            raise ValidationError('Это имя пользователя недоступно')
    
    def validate_email(self, field):
        # В реальном приложении здесь будет проверка в базе данных
        if field.data.endswith('@test.com'):
            raise ValidationError('Временные email не допускаются')


@app.route('/register-wtforms', methods=['GET', 'POST'])
def register_wtforms():
    """Обработчик формы регистрации с WTForms"""
    form = RegistrationForm()
    
    if form.validate_on_submit():
        flash(f'Регистрация успешна! Добро пожаловать, {form.username.data}!', 'success')
        print(f"Зарегистрирован пользователь: {form.username.data} ({form.email.data})")
        return redirect(url_for('register_wtforms'))
    
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Регистрация (WTForms)</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 500px; margin: 50px auto; padding: 20px; }
            form { background: #f4f4f4; padding: 20px; border-radius: 5px; }
            label { display: block; margin-top: 10px; font-weight: bold; }
            input { width: 100%; padding: 8px; margin-top: 5px; box-sizing: border-box; }
            button { margin-top: 15px; padding: 10px 20px; background: #28a745; color: white; border: none; cursor: pointer; }
            .error { color: red; font-size: 14px; }
            .hint { font-size: 12px; color: #666; }
            .success { color: green; }
        </style>
    </head>
    <body>
        <h1>Регистрация (WTForms)</h1>
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <p class="{{ category }}">{{ message }}</p>
                {% endfor %}
            {% endfor %}
        {% endwith %}
        <form method="POST">
            {{ form.hidden_tag() }}
            <label>{{ form.username.label }}</label>
            {{ form.username() }}
            <span class="hint">От 3 до 20 символов</span>
            {% if form.username.errors %}
                {% for error in form.username.errors %}<span class="error">{{ error }}</span><br>{% endfor %}
            {% endif %}
            
            <label>{{ form.email.label }}</label>
            {{ form.email() }}
            {% if form.email.errors %}
                {% for error in form.email.errors %}<span class="error">{{ error }}</span><br>{% endfor %}
            {% endif %}
            
            <label>{{ form.password.label }}</label>
            {{ form.password() }}
            <span class="hint">Минимум 8 символов</span>
            {% if form.password.errors %}
                {% for error in form.password.errors %}<span class="error">{{ error }}</span><br>{% endfor %}
            {% endif %}
            
            <label>{{ form.confirm_password.label }}</label>
            {{ form.confirm_password() }}
            {% if form.confirm_password.errors %}
                {% for error in form.confirm_password.errors %}<span class="error">{{ error }}</span><br>{% endfor %}
            {% endif %}
            
            <label>{{ form.age.label }}</label>
            {{ form.age() }}
            {% if form.age.errors %}
                {% for error in form.age.errors %}<span class="error">{{ error }}</span><br>{% endfor %}
            {% endif %}
            
            <label>{{ form.terms() }} {{ form.terms.label.text }}</label>
            {% if form.terms.errors %}
                {% for error in form.terms.errors %}<span class="error">{{ error }}</span><br>{% endfor %}
            {% endif %}
            
            {{ form.submit() }}
        </form>
    </body>
    </html>
    ''', form=form)


# ============================================================================
# Упражнение 5: Сложные формы с отношениями (FieldList, FormField)
# ============================================================================

class AddressForm(FlaskForm):
    """Вложенная форма для адреса"""
    street = StringField('Улица', validators=[DataRequired()])
    city = StringField('Город', validators=[DataRequired()])
    country = StringField('Страна', validators=[DataRequired()])
    postal_code = StringField('Почтовый индекс', validators=[DataRequired()])


class OrderItemForm(FlaskForm):
    """Вложенная форма для товара в заказе"""
    product_name = StringField('Название товара', validators=[DataRequired()])
    quantity = IntegerField('Количество', validators=[
        DataRequired(), 
        NumberRange(min=1, max=100)
    ])
    price = FloatField('Цена', validators=[
        DataRequired(), 
        NumberRange(min=0)
    ])


class OrderForm(FlaskForm):
    """Главная форма заказа"""
    customer_name = StringField('Имя клиента', validators=[
        DataRequired(), 
        Length(min=2, max=100)
    ])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Телефон', validators=[
        DataRequired(), 
        Length(min=10, max=20)
    ])
    
    # Адрес доставки (FormField)
    shipping_address = FormField(AddressForm)
    
    # Список товаров (FieldList)
    items = FieldList(FormField(OrderItemForm), min_entries=1, max_entries=10)
    
    notes = StringField('Примечания к заказу')
    submit = SubmitField('Оформить заказ')


@app.route('/order', methods=['GET', 'POST'])
def order():
    """Обработчик формы заказа"""
    form = OrderForm()
    
    # Добавление дополнительных товаров в заказ
    if request.method == 'POST':
        if 'add_item' in request.form:
            form.items.append_entry()
    
    if form.validate_on_submit():
        customer_name = form.customer_name.data
        email = form.email.data
        phone = form.phone_data
        shipping = form.shipping_address.data
        notes = form.notes.data
        
        # Расчёт общей суммы
        total = sum(item.quantity.data * item.price.data for item in form.items)
        
        flash(f'Заказ оформлен! Сумма: {total:.2f} руб.', 'success')
        print(f"Заказ от {customer_name} ({email}): {total:.2f} руб.")
        
        return redirect(url_for('order'))
    
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Оформление заказа</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            form { background: #f4f4f4; padding: 20px; border-radius: 5px; }
            fieldset { margin-top: 20px; padding: 10px; }
            label { display: inline-block; margin-top: 5px; }
            input { padding: 8px; margin-top: 5px; }
            button { margin-top: 15px; padding: 10px 20px; background: #28a745; color: white; border: none; cursor: pointer; }
            .error { color: red; font-size: 14px; }
            .success { color: green; }
            .item { background: white; padding: 10px; margin: 10px 0; border-radius: 5px; }
        </style>
    </head>
    <body>
        <h1>Оформление заказа</h1>
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <p class="{{ category }}">{{ message }}</p>
                {% endfor %}
            {% endfor %}
        {% endwith %}
        <form method="POST">
            {{ form.hidden_tag() }}
            
            <fieldset>
                <legend>Данные клиента</legend>
                <label>{{ form.customer_name.label }}</label><br>
                {{ form.customer_name(size=30) }}
                {% if form.customer_name.errors %}{% for e in form.customer_name.errors %}<span class="error">{{ e }}</span>{% endfor %}{% endif %}<br>
                
                <label>{{ form.email.label }}</label><br>
                {{ form.email(size=30) }}
                {% if form.email.errors %}{% for e in form.email.errors %}<span class="error">{{ e }}</span>{% endfor %}{% endif %}<br>
                
                <label>{{ form.phone.label }}</label><br>
                {{ form.phone(size=20) }}
                {% if form.phone.errors %}{% for e in form.phone.errors %}<span class="error">{{ e }}</span>{% endfor %}{% endif %}
            </fieldset>
            
            <fieldset>
                <legend>Адрес доставки</legend>
                {{ form.shipping_address.hidden_tag() }}
                <label>Улица:</label><br>{{ form.shipping_address.street(size=40) }}<br>
                <label>Город:</label><br>{{ form.shipping_address.city(size=30) }}<br>
                <label>Страна:</label><br>{{ form.shipping_address.country(size=30) }}<br>
                <label>Индекс:</label><br>{{ form.shipping_address.postal_code(size=10) }}
            </fieldset>
            
            <fieldset>
                <legend>Товары</legend>
                {% for item in form.items %}
                <div class="item">
                    <label>Товар:</label><br>{{ item.product_name(size=40) }}<br>
                    <label>Количество:</label><br>{{ item.quantity() }}<br>
                    <label>Цена:</label><br>{{ item.price() }}
                </div>
                {% endfor %}
                <button type="submit" name="add_item">Добавить товар</button>
            </fieldset>
            
            <fieldset>
                <legend>Примечания</legend>
                {{ form.notes(size=50) }}
            </fieldset>
            
            {{ form.submit() }}
        </form>
    </body>
    </html>
    ''', form=form)


# ============================================================================
# Упражнение 6: Кастомные валидаторы
# ============================================================================

class CustomValidators:
    """Класс с кастомными валидаторами"""
    
    @staticmethod
    def contains_uppercase(form, field):
        """Проверяет наличие заглавных букв в пароле"""
        if not any(c.isupper() for c in field.data):
            raise ValidationError('Пароль должен содержать хотя бы одну заглавную букву')
    
    @staticmethod
    def contains_digit(form, field):
        """Проверяет наличие цифр в пароле"""
        if not any(c.isdigit() for c in field.data):
            raise ValidationError('Пароль должен содержать хотя бы одну цифру')
    
    @staticmethod
    def contains_special(form, field):
        """Проверяет наличие специальных символов"""
        import re
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', field.data):
            raise ValidationError('Пароль должен содержать специальный символ (!@#$%^&*)')
    
    @staticmethod
    def russian_only(form, field):
        """Проверяет, что поле содержит только русские буквы"""
        import re
        if not re.match(r'^[а-яА-ЯёЁ\s\-]+$', field.data):
            raise ValidationError('Поле должно содержать только русские буквы')


class SecurePasswordForm(FlaskForm):
    """Форма с безопасным паролем"""
    password = PasswordField('Пароль', validators=[
        DataRequired(),
        Length(min=8, max=50),
        CustomValidators.contains_uppercase,
        CustomValidators.contains_digit,
        CustomValidators.contains_special
    ])
    submit = SubmitField('Сохранить')


class RussianNameForm(FlaskForm):
    """Форма с проверкой русских символов"""
    name = StringField('Имя', validators=[
        DataRequired(),
        CustomValidators.russian_only,
        Length(min=2, max=50)
    ])
    submit = SubmitField('Отправить')


@app.route('/secure-password', methods=['GET', 'POST'])
def secure_password():
    """Обработчик формы с безопасным паролем"""
    form = SecurePasswordForm()
    
    if form.validate_on_submit():
        flash('Пароль сохранён!', 'success')
        return redirect(url_for('secure_password'))
    
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Безопасный пароль</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 400px; margin: 50px auto; padding: 20px; }
            form { background: #f4f4f4; padding: 20px; border-radius: 5px; }
            label { display: block; margin-top: 10px; font-weight: bold; }
            input { width: 100%; padding: 8px; margin-top: 5px; box-sizing: border-box; }
            button { margin-top: 15px; padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
            .error { color: red; font-size: 14px; }
        </style>
    </head>
    <body>
        <h1>Установка пароля</h1>
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <p class="{{ category }}">{{ message }}</p>
                {% endfor %}
            {% endfor %}
        {% endwith %}
        <form method="POST">
            {{ form.hidden_tag() }}
            <label>{{ form.password.label }}</label>
            {{ form.password() }}
            <small>Требования: минимум 8 символов, заглавная буква, цифра, специальный символ</small>
            {% if form.password.errors %}
                {% for error in form.password.errors %}<br><span class="error">{{ error }}</span>{% endfor %}
            {% endif %}
            {{ form.submit() }}
        </form>
    </body>
    </html>
    ''', form=form)


@app.route('/russian-name', methods=['GET', 'POST'])
def russian_name():
    """Обработчик формы с русскими символами"""
    form = RussianNameForm()
    
    if form.validate_on_submit():
        flash(f'Привет, {form.name.data}!', 'success')
        return redirect(url_for('russian_name'))
    
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Имя (русский язык)</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 400px; margin: 50px auto; padding: 20px; }
            form { background: #f4f4f4; padding: 20px; border-radius: 5px; }
            label { display: block; margin-top: 10px; font-weight: bold; }
            input { width: 100%; padding: 8px; margin-top: 5px; box-sizing: border-box; }
            button { margin-top: 15px; padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
            .error { color: red; font-size: 14px; }
        </style>
    </head>
    <body>
        <h1>Введите ваше имя</h1>
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <p class="{{ category }}">{{ message }}</p>
                {% endfor %}
            {% endfor %}
        {% endwith %}
        <form method="POST">
            {{ form.hidden_tag() }}
            <label>{{ form.name.label }}</label>
            {{ form.name() }}
            {% if form.name.errors %}
                {% for error in form.name.errors %}<span class="error">{{ error }}</span>{% endfor %}
            {% endif %}
            {{ form.submit() }}
        </form>
    </body>
    </html>
    ''', form=form)


# ============================================================================
# Упражнение 7: Загрузка файлов
# ============================================================================

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max

def allowed_file(filename):
    """Проверка допустимого расширения файла"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class UploadForm(FlaskForm):
    """Форма для загрузки файлов"""
    file = FileField('Выберите файл', validators=[
        DataRequired(message='Выберите файл для загрузки')
    ])
    description = StringField('Описание', validators=[
        Length(max=200)
    ])
    submit = SubmitField('Загрузить')


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    """Обработчик загрузки файлов"""
    form = UploadForm()
    
    if form.validate_on_submit():
        file = form.file.data
        
        if file and allowed_file(file.filename):
            # Создаём папку для загрузки, если её нет
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            
            # Сохраняем файл
            filename = file.filename
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            flash(f'Файл {filename} успешно загружен!', 'success')
            return redirect(url_for('upload'))
        else:
            flash('Недопустимый тип файла', 'error')
    
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Загрузка файлов</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 400px; margin: 50px auto; padding: 20px; }
            form { background: #f4f4f4; padding: 20px; border-radius: 5px; }
            label { display: block; margin-top: 10px; font-weight: bold; }
            input { margin-top: 5px; }
            button { margin-top: 15px; padding: 10px 20px; background: #007bff; color: white; border: none; cursor: pointer; }
            .error { color: red; }
            .success { color: green; }
        </style>
    </head>
    <body>
        <h1>Загрузка файлов</h1>
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <p class="{{ category }}">{{ message }}</p>
                {% endfor %}
            {% endfor %}
        {% endwith %}
        <form method="POST" enctype="multipart/form-data">
            {{ form.hidden_tag() }}
            <label>{{ form.file.label }}</label>
            {{ form.file() }}
            {% if form.file.errors %}
                {% for error in form.file.errors %}<span class="error">{{ error }}</span>{% endfor %}
            {% endif %}
            
            <label>{{ form.description.label }}</label>
            {{ form.description(size=30) }}
            
            {{ form.submit() }}
        </form>
    </body>
    </html>
    ''', form=form)


# ============================================================================
# Главная страница с навигацией
# ============================================================================

@app.route('/')
def index():
    """Главная страница со списком всех упражнений"""
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Flask Forms - Практика</title>
        <style>
            body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
            h1 { color: #333; }
            ul { list-style: none; padding: 0; }
            li { margin: 10px 0; }
            a { color: #007bff; text-decoration: none; font-size: 18px; }
            a:hover { text-decoration: underline; }
            .exercise { background: #f4f4f4; padding: 15px; margin: 10px 0; border-radius: 5px; }
        </style>
    </head>
    <body>
        <h1>Практическое занятие 34: Flask - формы</h1>
        <h2>Список упражнений:</h2>
        
        <div class="exercise">
            <h3>Упражнение 1: Простая форма без библиотек</h3>
            <ul>
                <li><a href="/contact">Контактная форма</a></li>
            </ul>
        </div>
        
        <div class="exercise">
            <h3>Упражнение 2: Форма регистрации</h3>
            <ul>
                <li><a href="/register">Регистрация пользователя</a></li>
            </ul>
        </div>
        
        <div class="exercise">
            <h3>Упражнение 3: WTForms - Контактная форма</h3>
            <ul>
                <li><a href="/contact-wtforms">Контактная форма (WTForms)</a></li>
            </ul>
        </div>
        
        <div class="exercise">
            <h3>Упражнение 4: WTForms - Форма регистрации</h3>
            <ul>
                <li><a href="/register-wtforms">Регистрация (WTForms)</a></li>
            </ul>
        </div>
        
        <div class="exercise">
            <h3>Упражнение 5: Сложные формы (FieldList, FormField)</h3>
            <ul>
                <li><a href="/order">Оформление заказа</a></li>
            </ul>
        </div>
        
        <div class="exercise">
            <h3>Упражнение 6: Кастомные валидаторы</h3>
            <ul>
                <li><a href="/secure-password">Безопасный пароль</a></li>
                <li><a href="/russian-name">Русское имя</a></li>
            </ul>
        </div>
        
        <div class="exercise">
            <h3>Упражнение 7: Загрузка файлов</h3>
            <ul>
                <li><a href="/upload">Загрузка файлов</a></li>
            </ul>
        </div>
    </body>
    </html>
    ''')


# ============================================================================
# Запуск приложения
# ============================================================================

if __name__ == '__main__':
    # Создаём папку для загрузок
    os.makedirs('uploads', exist_ok=True)
    
    print("=" * 60)
    print("Запуск Flask-приложения с формами")
    print("=" * 60)
    print("Откройте в браузере: http://127.0.0.1:5000/")
    print("=" * 60)
    
    app.run(debug=True)
