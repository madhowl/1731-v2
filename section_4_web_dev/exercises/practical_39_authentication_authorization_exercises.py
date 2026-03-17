"""
Упражнения к практической работе 39: Аутентификация и авторизация

Выполните упражнения по аутентификации и авторизации.
"""

# Упражнение 1: Flask-Login
def exercise_flask_login():
    """
    Настройте аутентификацию в Flask.
    """
    from flask import Flask, render_template_string
    from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
    
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret'
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    
    users = {'user': {'password': 'password'}}
    
    class User(UserMixin):
        def __init__(self, id):
            self.id = id
    
    @login_manager.user_loader
    def load_user(user_id):
        if user_id in users:
            return User(user_id)
        return None
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            if username in users and users[username]['password'] == password:
                user = User(username)
                login_user(user)
                return 'Logged in!'
        return '<form method="POST"><input name="username"><input name="password"><button>Login</button></form>'
    
    @app.route('/logout')
    @login_required
    def logout():
        logout_user()
        return 'Logged out!'
    
    @app.route('/protected')
    @login_required
    def protected():
        return f'Hello, {current_user.id}!'
    
    app.run(debug=True)


# Упражнение 2: JWT аутентификация
def exercise_jwt():
    """
    Настройте JWT аутентификацию.
    """
    import jwt
    from datetime import datetime, timedelta
    
    SECRET_KEY = 'secret'
    
    def create_token(user_id):
        payload = {
            'user_id': user_id,
            'exp': datetime.utcnow() + timedelta(hours=1)
        }
        return jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    
    def verify_token(token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            return None


# Упражнение 3: Ролевая авторизация
def exercise_rbac():
    """
    Реализуйте ролевую авторизацию.
    """
    from functools import wraps
    
    def role_required(roles):
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                if current_user.role not in roles:
                    return 'Access denied'
                return f(*args, **kwargs)
            return decorated_function
        return decorator
    
    # @role_required(['admin', 'moderator'])
    # def admin_panel():
    #     return 'Admin panel'


if __name__ == "__main__":
    from flask import request
    print("Упражнения по аутентификации")
