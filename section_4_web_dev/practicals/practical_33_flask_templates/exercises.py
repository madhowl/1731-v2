# Упражнения для практического занятия 33: Flask - шаблоны

from flask import Flask, render_template

app = Flask(__name__)

# Пример данных для передачи в шаблоны
users = [
    {'name': 'Иван', 'age': 25, 'email': 'ivan@example.com'},
    {'name': 'Мария', 'age': 30, 'email': 'maria@example.com'},
    {'name': 'Петр', 'age': 35, 'email': 'petr@example.com'}
]

@app.route('/')
def index():
    return render_template('index.html', title='Главная страница', users=users)

@app.route('/about')
def about():
    return render_template('about.html', title='О нас')

@app.route('/users')
def user_list():
    return render_template('users.html', title='Список пользователей', users=users)

if __name__ == '__main__':
    app.run(debug=True)