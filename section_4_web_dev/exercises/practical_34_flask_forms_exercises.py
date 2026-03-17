"""
Упражнения к практической работе 34: Flask - формы

Выполните следующие упражнения для закрепления навыков
работы с формами в Flask.
"""

# Упражнение 1: Базовая форма
def exercise_basic_form():
    """
    Создайте Flask-приложение с базовой HTML-формой.
    """
    from flask import Flask, render_template_string, request
    
    app = Flask(__name__)
    
    form_template = '''
    <form method="POST">
        <label>Имя:</label>
        <input type="text" name="name">
        <label>Email:</label>
        <input type="email" name="email">
        <button type="submit">Отправить</button>
    </form>
    {% if name %}
    <p>Привет, {{ name }}!</p>
    <p>Email: {{ email }}</p>
    {% endif %}
    '''
    
    @app.route('/', methods=['GET', 'POST'])
    def index():
        if request.method == 'POST':
            name = request.form.get('name')
            email = request.form.get('email')
            return render_template_string(form_template, name=name, email=email)
        return render_template_string(form_template)
    
    app.run(debug=True)


# Упражнение 2: WTForms
def exercise_wtforms():
    """
    Создайте форму с использованием WTForms.
    """
    from flask import Flask, render_template_string
    from flask_wtf import FlaskForm
    from wtforms import StringField, PasswordField, SubmitField
    from wtforms.validators import DataRequired, Email, Length
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'
    
    class LoginForm(FlaskForm):
        username = StringField('Имя пользователя', validators=[DataRequired()])
        password = PasswordField('Пароль', validators=[DataRequired(), Length(min=6)])
        submit = SubmitField('Войти')
    
    template = '''
    <form method="POST">
        {{ form.hidden_tag() }}
        <p>
            {{ form.username.label }}<br>
            {{ form.username(size=30) }}
        </p>
        <p>
            {{ form.password.label }}<br>
            {{ form.password(size=30) }}
        </p>
        <p>{{ form.submit() }}</p>
    </form>
    {% if form.username.errors %}
    <ul>
    {% for error in form.username.errors %}
        <li>{{ error }}</li>
    {% endfor %}
    </ul>
    {% endif %}
    '''
    
    @app.route('/', methods=['GET', 'POST'])
    def index():
        form = LoginForm()
        if form.validate_on_submit():
            return f'Вход выполнен: {form.username.data}'
        return render_template_string(template, form=form)
    
    app.run(debug=True)


# Упражнение 3: Валидация формы
def exercise_form_validation():
    """
    Создайте форму с комплексной валидацией.
    """
    from flask import Flask, render_template_string
    from flask_wtf import FlaskForm
    from wtforms import StringField, IntegerField, SelectField, SubmitField
    from wtforms.validators import DataRequired, NumberRange, ValidationError
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'
    
    def custom_validator(form, field):
        if field.data and 'admin' in field.data.lower():
            raise ValidationError('Недопустимое имя пользователя')
    
    class RegistrationForm(FlaskForm):
        username = StringField('Имя', validators=[DataRequired(), custom_validator])
        age = IntegerField('Возраст', validators=[NumberRange(min=18, max=100)])
        city = SelectField('Город', choices=[('msk', 'Москва'), ('spb', 'Санкт-Петербург'), ('other', 'Другой')])
        submit = SubmitField('Регистрация')
    
    template = '''
    <form method="POST">
        {{ form.hidden_tag() }}
        <p>{{ form.username.label }}: {{ form.username() }}</p>
        {% for error in form.username.errors %}{{ error }}{% endfor %}
        <p>{{ form.age.label }}: {{ form.age() }}</p>
        <p>{{ form.city.label }}: {{ form.city() }}</p>
        <p>{{ form.submit() }}</p>
    </form>
    {% if success %}<p>Регистрация успешна!</p>{% endif %}
    '''
    
    @app.route('/', methods=['GET', 'POST'])
    def index():
        form = RegistrationForm()
        success = False
        if form.validate_on_submit():
            success = True
        return render_template_string(template, form=form, success=success)
    
    app.run(debug=True)


if __name__ == "__main__":
    print("Доступные упражнения:")
    print("1. exercise_basic_form() - Базовая форма")
    print("2. exercise_wtforms() - WTForms")
    print("3. exercise_form_validation() - Валидация")
    print("\nДля запуска раскомментируйте нужную функцию:")
    # exercise_basic_form()
    # exercise_wtforms()
    # exercise_form_validation()
