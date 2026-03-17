"""
Упражнения к практической работе 35: Flask - интеграция с базой данных

Выполните следующие упражнения для закрепления навыков
интеграции Flask с базами данных.
"""

# Упражнение 1: SQLAlchemy базовая настройка
def exercise_sqlalchemy_setup():
    """
    Настройте Flask с SQLAlchemy.
    """
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db = SQLAlchemy(app)
    
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
    
    with app.app_context():
        db.create_all()
        print("База данных создана!")


# Упражнение 2: CRUD операции
def exercise_crud_operations():
    """
    Выполните CRUD операции с SQLAlchemy.
    """
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    db = SQLAlchemy(app)
    
    class User(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), nullable=False)
    
    with app.app_context():
        # Create
        user = User(username='ivan')
        db.session.add(user)
        db.session.commit()
        
        # Read
        users = User.query.all()
        print(f"Пользователи: {users}")
        
        # Update
        user = User.query.first()
        user.username = 'ivan_updated'
        db.session.commit()
        
        # Delete
        db.session.delete(user)
        db.session.commit()


# Упражнение 3: Связи между моделями
def exercise_relationships():
    """
    Создайте связи между моделями.
    """
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    db = SQLAlchemy(app)
    
    class Author(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        books = db.relationship('Book', backref='author', lazy=True)
    
    class Book(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(200), nullable=False)
        author_id = db.Column(db.Integer, db.ForeignKey('author.id'))
    
    with app.app_context():
        db.create_all()
        
        author = Author(name='Толстой')
        book = Book(title='Война и мир', author=author)
        db.session.add(author)
        db.session.add(book)
        db.session.commit()
        
        print(f"Книги автора: {author.books}")


if __name__ == "__main__":
    print("Доступные упражнения:")
    print("1. exercise_sqlalchemy_setup() - Настройка SQLAlchemy")
    print("2. exercise_crud_operations() - CRUD операции")
    print("3. exercise_relationships() - Связи между моделями")
    print("\nДля запуска раскомментируйте нужную функцию:")
    # exercise_sqlalchemy_setup()
    # exercise_crud_operations()
    # exercise_relationships()
