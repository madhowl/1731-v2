# Практическое занятие 34: Flask - формы

## Работа с формами в Flask

### Цель занятия:
Научиться создавать и обрабатывать формы в Flask-приложениях, использовать валидацию данных, работать с различными типами полей форм, реализовывать загрузку файлов.

### Задачи:
1. Создавать HTML-формы в Flask
2. Использовать WTForms для создания форм
3. Реализовывать валидацию данных
4. Обрабатывать загрузку файлов
5. Создавать сложные формы с отношениями

### План работы:
1. Основы работы с формами в Flask
2. Библиотека WTForms
3. Валидация данных
4. Загрузка файлов
5. Практические задания

---

## 1. Основы работы с формами в Flask

Формы являются основным способом взаимодействия пользователя с веб-приложением. Flask предоставляет несколько способов работы с формами.

### Пример 1: Простая форма без библиотек

```python
from flask import Flask, request, render_template_string

app = Flask(__name__)

# HTML-шаблон формы
FORM_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Контактная форма</title>
    <style>
        body { font-family: Arial; max-width: 600px; margin: 50px auto; }
        form { background: #f4f4f4; padding: 20px; border-radius: 5px; }
        label { display: block; margin-top: 10px; font-weight: bold; }
        input, textarea { width: 100%; padding: 8px; margin-top: 5px; }
        button { margin-top: 15px; padding: 10px 20px; background: #007bff; color: white; border: none; }
        .error { color: red; font-size: 14px; }
    </style>
</head>
<body>
    <h1>Контактная форма</h1>
    {% if success %}
        <p style="color: green;">Спасибо! Ваше сообщение отправлено.</p>
    {% endif %}
    {% if errors %}
        <div class="error">
            {% for error in errors %}
                <p>{{ error }}</p>
            {% endfor %}
        </div>
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
            # Здесь можно отправить email или сохранить данные
            print(f"Получено сообщение от {name} ({email}): {subject} - {message}")
    
    return render_template_string(FORM_TEMPLATE, 
                                   errors=errors, 
                                   name=name, 
                                   email=email, 
                                   subject=subject, 
                                   message=message,
                                   success=success)

if __name__ == '__main__':
    app.run(debug=True)
```

### Пример 2: Форма регистрации пользователя

```python
from flask import Flask, request, render_template_string

app = Flask(__name__)

REGISTER_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Регистрация</title>
    <style>
        body { font-family: Arial; max-width: 500px; margin: 50px auto; }
        form { background: #f4f4f4; padding: 20px; border-radius: 5px; }
        label { display: block; margin-top: 10px; font-weight: bold; }
        input { width: 100%; padding: 8px; margin-top: 5px; box-sizing: border-box; }
        button { margin-top: 15px; padding: 10px 20px; background: #28a745; color: white; border: none; }
        .error { color: red; font-size: 14px; }
        .hint { font-size: 12px; color: #666; }
    </style>
</head>
<body>
    <h1>Регистрация нового пользователя</h1>
    {% if success %}
        <p style="color: green;">Регистрация успешна! Добро пожаловать, {{ name }}!</p>
    {% endif %}
    {% if errors %}
        <div class="error">
            {% for error in errors %}
                <p>{{ error }}</p>
            {% endfor %}
        </div>
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
            # Здесь можно сохранить пользователя в базу данных
            print(f"Зарегистрирован пользователь: {username} ({email})")
    
    return render_template_string(REGISTER_TEMPLATE, 
                                   errors=errors, 
                                   username=username, 
                                   email=email, 
                                   age=age,
                                   success=success)

if __name__ == '__main__':
    app.run(debug=True)
```

---

## 2. Библиотека WTForms

WTForms предоставляет удобный способ создания и валидации форм в Flask.

### Пример 3: Установка и базовое использование WTForms

```bash
pip install flask-wtf email_validator
```

```python
from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'

# Определение формы с использованием WTForms
class ContactForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired(message='Имя обязательно')])
    email = EmailField('Email', validators=[DataRequired(), Email(message='Некорректный email')])
    subject = StringField('Тема')
    message = TextAreaField('Сообщение', validators=[DataRequired(), Length(min=10, message='Сообщение слишком короткое')])
    submit = SubmitField('Отправить')

@app.route('/contact-wtforms', methods=['GET', 'POST'])
def contact_wtforms():
    form = ContactForm()
    
    if form.validate_on_submit():
        # Обработка данных формы
        name = form.name.data
        email = form.email.data
        subject = form.subject.data
        message = form.message.data
        
        flash(f'Спасибо, {name}! Ваше сообщение отправлено.', 'success')
        print(f"Получено сообщение от {name} ({email}): {subject} - {message}")
        
        return redirect(url_for('contact_wtforms'))
    
    return render_template('contact_wtforms.html', form=form)
```

### Пример 4: Форма регистрации с WTForms

```python
from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField, IntegerField, BooleanField
from wtforms.validators import DataRequired, Email, Length, EqualTo, Regexp, NumberRange

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', 
                           validators=[
                               DataRequired(),
                               Length(min=3, max=20, message='От 3 до 20 символов'),
                               Regexp(r'^[a-zA-Z0-9_]+$', message='Только латинские буквы, цифры и подчёркивание')
                           ])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired(), Length(min=8, message='Минимум 8 символов')])
    confirm_password = PasswordField('Подтвердите пароль', 
                                     validators=[DataRequired(), EqualTo('password', message='Пароли должны совпадать')])
    age = IntegerField('Возраст', validators=[NumberRange(min=1, max=150, message='Введите корректный возраст')])
    terms = BooleanField('Я согласен с условиями использования', validators=[DataRequired(message='Вы должны согласиться')])
    submit = SubmitField('Зарегистрироваться')
    
    # Кастомный валидатор для проверки уникальности username
    def validate_username(self, field):
        # В реальном приложении здесь будет проверка в базе данных
        if field.data.lower() in ['admin', 'root', 'administrator']:
            raise ValidationError('Это имя пользователя недоступно')
    
    def validate_email(self, field):
        # В реальном приложении здесь будет проверка в базе данных
        if field.data.endswith('@test.com'):
            raise ValidationError('Временные email не допускаются')

@app.route('/register-wtforms', methods=['GET', 'POST'])
def register_wtforms():
    form = RegistrationForm()
    
    if form.validate_on_submit():
        flash(f'Регистрация успешна! Добро пожаловать, {form.username.data}!', 'success')
        # Здесь можно сохранить пользователя в базу данных
        return redirect(url_for('register_wtforms'))
    
    # Вывод ошибок валидации
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'{getattr(form, field).label.text}: {error}', 'error')
    
    return render_template('register_wtforms.html', form=form)
```

### Пример 5: Сложная форма с отношениями

```python
from flask import Flask, render_template, flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, IntegerField, FloatField
from wtforms import FormField, FieldList
from wtforms.validators import DataRequired, Email, Length, NumberRange

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'

# Вложенная форма для адреса
class AddressForm(FlaskForm):
    street = StringField('Улица', validators=[DataRequired()])
    city = StringField('Город', validators=[DataRequired()])
    country = StringField('Страна', validators=[DataRequired()])
    postal_code = StringField('Почтовый индекс', validators=[DataRequired()])

# Вложенная форма для товара в заказе
class OrderItemForm(FlaskForm):
    product_name = StringField('Название товара', validators=[DataRequired()])
    quantity = IntegerField('Количество', validators=[DataRequired(), NumberRange(min=1, max=100)])
    price = FloatField('Цена', validators=[DataRequired(), NumberRange(min=0)])

# Главная форма заказа
class OrderForm(FlaskForm):
    customer_name = StringField('Имя клиента', validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Телефон', validators=[DataRequired(), Length(min=10, max=20)])
    
    # Адрес доставки
    shipping_address = FormField(AddressForm)
    
    # Список товаров
    items = FieldList(FormField(OrderItemForm), min_entries=1, max_entries=10)
    
    notes = StringField('Примечания к заказу')
    submit = SubmitField('Оформить заказ')

@app.route('/order', methods=['GET', 'POST'])
def order():
    form = OrderForm()
    
    # Добавление дополнительных товаров в заказ
    if request.method == 'POST':
        if 'add_item' in request.form:
            form.items.append_entry()
    
    if form.validate_on_submit():
        total = sum(item.quantity.data * item.price.data for item in form.items)
        flash(f'Заказ оформлен! Сумма: {total:.2f} руб.', 'success')
        return redirect(url_for('order'))
    
    return render_template('order.html', form=form)

# Добавление маршрута для добавления товара
from flask import request, url_for, redirect

@app.route('/order/add-item', methods=['POST'])
def add_order_item():
    # Логика добавления нового товара
    return redirect(url_for('order'))
```

---

## 3. Валидация данных

### Пример 6: Кастомные валидаторы

```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import ValidationError
import re

class CustomValidators:
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
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', field.data):
            raise ValidationError('Пароль должен содержать специальный символ (!@#$%^&*)')
    
    @staticmethod
    def russian_only(form, field):
        """Проверяет, что поле содержит только русские буквы"""
        if not re.match(r'^[а-яА-ЯёЁ\s\-]+$', field.data):
            raise ValidationError('Поле должно содержать только русские буквы')

class SecurePasswordForm(FlaskForm):
    password = PasswordField('Пароль', validators=[
        DataRequired(),
        Length(min=8, max=50),
        CustomValidators.contains_uppercase,
        CustomValidators.contains_digit,
        CustomValidators.contains_special
    ])
    submit = SubmitField('Сохранить')

class RussianNameForm(FlaskForm):
    name = StringField('Имя', validators=[
        DataRequired(),
        CustomValidators.russian_only,
        Length(min=2, max=50)
    ])
    submit = SubmitField('Отправить')
```

### Пример 7: Валидация на стороне клиента и сервера

```html
<!-- Шаблон с валидацией на стороне клиента -->
<!DOCTYPE html>
<html>
<head>
    <title>Форма с валидацией</title>
    <style>
        .error { border-color: red; }
        .error-message { color: red; font-size: 12px; }
        input:valid { border-color: green; }
    </style>
</head>
<body>
    <form id="registrationForm">
        <div>
            <label>Email:</label>
            <input type="email" name="email" required 
                   pattern="[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$">
            <span class="error-message" id="emailError"></span>
        </div>
        
        <div>
            <label>Пароль:</label>
            <input type="password" name="password" required minlength="8"
                   pattern="(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]">
            <span class="error-message" id="passwordError"></span>
        </div>
        
        <div>
            <label>Подтверждение пароля:</label>
            <input type="password" name="confirmPassword" required>
            <span class="error-message" id="confirmError"></span>
        </div>
        
        <button type="submit">Зарегистрироваться</button>
    </form>
    
    <script>
        const form = document.getElementById('registrationForm');
        
        form.addEventListener('submit', function(e) {
            let isValid = true;
            
            // Проверка совпадения паролей
            const password = form.password.value;
            const confirm = form.confirmPassword.value;
            
            if (password !== confirm) {
                document.getElementById('confirmError').textContent = 'Пароли не совпадают';
                isValid = false;
            } else {
                document.getElementById('confirmError').textContent = '';
            }
            
            if (!isValid) {
                e.preventDefault();
            }
        });
        
        // Валидация при вводе
        form.password.addEventListener('input', function() {
            const errorSpan = document.getElementById('passwordError');
            if (this.validity.valid) {
                errorSpan.textContent = '';
            } else if (this.validity.tooShort) {
                errorSpan.textContent = 'Пароль слишком короткий';
            } else if (this.validity.patternMismatch) {
                errorSpan.textContent = 'Пароль должен содержать заглавную, строчную букву, цифру и специальный символ';
            }
        });
    </script>
</body>
</html>
```

---

## 4. Загрузка файлов

### Пример 8: Загрузка файлов в Flask

```python
from flask import Flask, request, render_template_string, send_from_directory
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Настройки загрузки файлов
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc', 'docx'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Создаем папку для загрузок
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    """Проверка допустимого расширения файла"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_size(file):
    """Получение размера файла"""
    file.seek(0, 2)  # Переходим в конец файла
    size = file.tell()  # Получаем позицию (размер)
    file.seek(0)  # Возвращаемся в начало
    return size

UPLOAD_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Загрузка файлов</title>
    <style>
        body { font-family: Arial; max-width: 600px; margin: 50px auto; }
        form { background: #f4f4f4; padding: 20px; border-radius: 5px; }
        input { margin: 10px 0; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; }
        .message { padding: 10px; margin: 10px 0; border-radius: 5px; }
        .success { background: #d4edda; color: #155724; }
        .error { background: #f8d7da; color: #721c24; }
        ul { list-style: none; padding: 0; }
        li { padding: 5px 0; }
    </style>
</head>
<body>
    <h1>Загрузка файлов</h1>
    
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="message {{ category }}">{{ message }}</div>
            {% endfor %}
        {% endif %}
    {% endwith %}
    
    <form method="POST" enctype="multipart/form-data">
        <label>Выберите файл:</label>
        <input type="file" name="file" required>
        <br>
        <label>Описание файла:</label>
        <input type="text" name="description" placeholder="Описание">
        <br>
        <button type="submit">Загрузить</button>
    </form>
    
    <h2>Загруженные файлы:</h2>
    <ul>
    {% for file in files %}
        <li>
            <a href="{{ url_for('download_file', filename=file) }}">{{ file }}</a>
            - <a href="{{ url_for('delete_file', filename=file) }}" style="color: red;">Удалить</a>
        </li>
    {% else %}
        <li>Нет загруженных файлов</li>
    {% endfor %}
    </ul>
</body>
</html>
'''

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Проверка наличия файла
        if 'file' not in request.files:
            return 'No file part'
        
        file = request.files['file']
        description = request.form.get('description', '')
        
        if file.filename == '':
            return 'No selected file'
        
        if file and allowed_file(file.filename):
            # Безопасное имя файла
            filename = secure_filename(file.filename)
            
            # Проверка размера файла
            file_size = get_file_size(file)
            if file_size > MAX_FILE_SIZE:
                return f'Файл слишком большой. Максимальный размер: {MAX_FILE_SIZE // (1024*1024)}MB'
            
            # Сохранение файла
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            return f'Файл {filename} успешно загружен!'
    
    # Получение списка загруженных файлов
    files = []
    if os.path.exists(UPLOAD_FOLDER):
        files = os.listdir(app.config['UPLOAD_FOLDER'])
    
    return render_template_string(UPLOAD_TEMPLATE, files=files)

@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/delete/<filename>')
def delete_file(filename):
    try:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return 'Файл удален'
    except:
        return 'Ошибка при удалении файла'

if __name__ == '__main__':
    app.run(debug=True)
```

### Пример 9: Загрузка нескольких файлов

```python
from flask import Flask, request, render_template_string
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

MULTI_UPLOAD_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Загрузка нескольких файлов</title>
</head>
<body>
    <h1>Загрузка нескольких файлов</h1>
    <form method="POST" enctype="multipart/form-data">
        <label>Выберите файлы (можно несколько):</label>
        <input type="file" name="files" multiple required>
        <br><br>
        <button type="submit">Загрузить все</button>
    </form>
    
    {% if results %}
    <h2>Результаты:</h2>
    <ul>
    {% for result in results %}
        <li style="color: {{ 'green' if result.success else 'red' }}">
            {{ result.filename }} - {{ result.message }}
        </li>
    {% endfor %}
    </ul>
    {% endif %}
</body>
</html>
'''

@app.route('/multi-upload', methods=['GET', 'POST'])
def multi_upload():
    results = []
    
    if request.method == 'POST':
        files = request.files.getlist('files')
        
        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                results.append({
                    'filename': filename,
                    'success': True,
                    'message': 'Загружен успешно'
                })
            else:
                results.append({
                    'filename': file.filename,
                    'success': False,
                    'message': 'Недопустимый файл'
                })
    
    return render_template_string(MULTI_UPLOAD_TEMPLATE, results=results)

if __name__ == '__main__':
    app.run(debug=True)
```

---

## 5. Практические задания

### Задание 1: Форма обратной связи
Создайте форму обратной связи со следующими полями:
- Имя (обязательно)
- Email (обязательно, валидация email)
- Телефон (опционально)
- Тема сообщения (выпадающий список: Техническая поддержка, Продажи, Общие вопросы)
- Сообщение (обязательно, минимум 20 символов)

### Задание 2: Форма опроса
Создайте форму опроса с использованием WTForms:
- Возраст (числовое поле, от 1 до 100)
- Пол (радиокнопки: Мужской, Женский, Другое)
- Интересы (чекбоксы: Программирование, Дизайн, Маркетинг, Другое)
- Уровень знаний (селектор: Начинающий, Средний, Продвинутый)
- Комментарий (текстовое поле)

### Задание 3: Форма входа
Создайте форму входа с:
- Email/логин
- Пароль
- Запомнить меня (checkbox)
- Забыли пароль? (ссылка)

### Задание 4: Загрузка аватара
Реализуйте загрузку изображения для профиля пользователя:
- Проверка типа файла (только изображения)
- Проверка размера (максимум 2MB)
- Изменение размера изображения
- Сохранение с уникальным именем

### Задание 5: Многошаговая форма
Создайте форму регистрации, разбитую на несколько шагов:
- Шаг 1: Личные данные (имя, email, телефон)
- Шаг 2: Адрес (город, улица, дом, квартира)
- Шаг 3: Настройки (уведомления, язык интерфейса)
- Сохранение данных между шагами в сессии

---

## Дополнительные задания

### Задание 6: Ajax-форма
Создайте форму с отправкой данных без перезагрузки страницы (AJAX).

### Задание 7: Динамическая форма
Реализуйте форму с возможностью добавления/удаления полей на лету.

### Задание 8: Форма с загрузкой нескольких файлов
Создайте форму для загрузки галереи изображений.

---

## Контрольные вопросы:
1. Как создать форму в Flask без использования библиотек?
2. Что такое WTForms и какие преимущества она дает?
3. Какие встроенные валидаторы WTForms вы знаете?
4. Как создать кастомный валидатор?
5. Как обработать загрузку файла в Flask?
6. Как проверить тип и размер загружаемого файла?
7. Что такое CSRF-защита и как её включить в Flask-WTF?
8. Как работать с вложенными формами в WTForms?
