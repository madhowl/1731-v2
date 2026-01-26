# Практическое занятие 48: Архитектура приложений

## MVC, MVP, MVVM, многослойная архитектура, принципы SOLID

### Цель занятия:
Изучить основные архитектурные паттерны приложений, понять принципы построения многослойной архитектуры, освоить принципы SOLID.

### Задачи:
1. Понять различия между MVC, MVP и MVVM паттернами
2. Реализовать пример приложения с использованием одного из паттернов
3. Изучить многослойную архитектуру
4. Применить принципы SOLID в разработке

### План работы:
1. Архитектурные паттерны
2. Многослойная архитектура
3. Принципы SOLID
4. Практические задания

---

## 1. Архитектурные паттерны

Архитектурные паттерны помогают организовать код приложения, разделяя ответственность между различными компонентами.

### Пример 1: MVC (Model-View-Controller)

MVC - это архитектурный паттерн, который разделяет приложение на три основные компоненты:
- **Model** - данные и бизнес-логика
- **View** - пользовательский интерфейс
- **Controller** - управление взаимодействием между Model и View

```python
# Пример MVC на Flask
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Model
class User:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

class UserService:
    def __init__(self):
        self.users = []
        self.next_id = 1
    
    def create_user(self, name, email):
        user = User(self.next_id, name, email)
        self.users.append(user)
        self.next_id += 1
        return user
    
    def get_all_users(self):
        return self.users
    
    def get_user_by_id(self, user_id):
        return next((user for user in self.users if user.id == user_id), None)

# Controller
user_service = UserService()

@app.route('/')
def index():
    users = user_service.get_all_users()
    return render_template('users/index.html', users=users)

@app.route('/user/<int:user_id>')
def user_detail(user_id):
    user = user_service.get_user_by_id(user_id)
    if not user:
        return "User not found", 404
    return render_template('users/detail.html', user=user)

@app.route('/user/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        user_service.create_user(name, email)
        return redirect(url_for('index'))
    return render_template('users/create.html')

if __name__ == '__main__':
    app.run(debug=True)
```

### Пример 2: MVP (Model-View-Presenter)

MVP - это паттерн, похожий на MVC, но с более четким разделением:
- **Model** - данные и бизнес-логика
- **View** - интерфейс пользователя (не знает о Model)
- **Presenter** - связующее звено между View и Model

```python
# Пример MVP для консольного приложения
from abc import ABC, abstractmethod

# Model
class UserModel:
    def __init__(self):
        self.users = []
        self.next_id = 1
    
    def add_user(self, name, email):
        user = {'id': self.next_id, 'name': name, 'email': email}
        self.users.append(user)
        self.next_id += 1
        return user
    
    def get_users(self):
        return self.users

# View interface
class UserView(ABC):
    @abstractmethod
    def show_users(self, users):
        pass
    
    @abstractmethod
    def show_message(self, message):
        pass
    
    @abstractmethod
    def get_user_input(self):
        pass

# Concrete View
class ConsoleUserView(UserView):
    def show_users(self, users):
        print("Список пользователей:")
        for user in users:
            print(f"- {user['id']}: {user['name']} ({user['email']})")
    
    def show_message(self, message):
        print(message)
    
    def get_user_input(self):
        name = input("Введите имя: ")
        email = input("Введите email: ")
        return name, email

# Presenter
class UserPresenter:
    def __init__(self, model, view):
        self.model = model
        self.view = view
    
    def show_users(self):
        users = self.model.get_users()
        self.view.show_users(users)
    
    def add_user(self):
        name, email = self.view.get_user_input()
        if name and email:
            self.model.add_user(name, email)
            self.view.show_message("Пользователь добавлен успешно")
        else:
            self.view.show_message("Имя и email обязательны")

# Использование
model = UserModel()
view = ConsoleUserView()
presenter = UserPresenter(model, view)

# Добавление нескольких пользователей
presenter.add_user()
presenter.add_user()
presenter.show_users()
```

### Пример 3: MVVM (Model-View-ViewModel)

MVVM - это паттерн, часто используемый в приложениях с богатым пользовательским интерфейсом:
- **Model** - данные и бизнес-логика
- **View** - пользовательский интерфейс
- **ViewModel** - абстракция View, которая содержит состояния и команды

```python
# Пример MVVM (упрощенный)
class UserViewModel:
    def __init__(self, model):
        self.model = model
        self._users = []
        self.load_users()
    
    @property
    def users(self):
        return self._users
    
    @users.setter
    def users(self, value):
        self._users = value
    
    def load_users(self):
        """Загрузка пользователей из модели"""
        self._users = self.model.get_users()
    
    def add_user(self, name, email):
        """Добавление пользователя через модель"""
        user = self.model.add_user(name, email)
        self._users.append(user)
        return user
    
    def get_formatted_users(self):
        """Форматированный список пользователей для отображения"""
        return [f"{user['name']} ({user['email']})" for user in self._users]

# Использование
model = UserModel()
vm = UserViewModel(model)
vm.add_user("Иван Иванов", "ivan@example.com")
formatted_users = vm.get_formatted_users()
print(formatted_users)
```

---

## 2. Многослойная архитектура

Многослойная архитектура разделяет приложение на логические слои, каждый из которых имеет свою ответственность.

### Пример 4: Типичная многослойная архитектура

```
[Представление (Presentation Layer)]
    - Контроллеры
    - Вьюхи/шаблоны

[Слой бизнес-логики (Business Logic Layer)]
    - Сервисы
    - Валидация
    - Бизнес-правила

[Слой доступа к данным (Data Access Layer)]
    - Репозитории
    - DAO (Data Access Objects)
    - ORM модели

[Слой данных (Data Layer)]
    - База данных
    - Файлы
    - Внешние API
```

### Пример 5: Реализация многослойной архитектуры

```python
# Слой данных (Data Layer)
import sqlite3
from typing import List, Optional

class UserEntity:
    def __init__(self, id: int, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email

class UserDAO:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL
                )
            ''')
    
    def create(self, user: UserEntity) -> UserEntity:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (name, email) VALUES (?, ?)",
                (user.name, user.email)
            )
            user.id = cursor.lastrowid
            return user
    
    def get_all(self) -> List[UserEntity]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, email FROM users")
            rows = cursor.fetchall()
            return [UserEntity(row[0], row[1], row[2]) for row in rows]
    
    def get_by_id(self, user_id: int) -> Optional[UserEntity]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, email FROM users WHERE id = ?", (user_id,))
            row = cursor.fetchone()
            if row:
                return UserEntity(row[0], row[1], row[2])
            return None
    
    def update(self, user: UserEntity) -> UserEntity:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET name = ?, email = ? WHERE id = ?",
                (user.name, user.email, user.id)
            )
            return user
    
    def delete(self, user_id: int) -> bool:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            return cursor.rowcount > 0

# Слой бизнес-логики (Business Logic Layer)
from typing import List

class UserNotFoundException(Exception):
    pass

class InvalidUserDataException(Exception):
    pass

class UserService:
    def __init__(self, user_dao: UserDAO):
        self.user_dao = user_dao
    
    def create_user(self, name: str, email: str) -> UserEntity:
        # Валидация данных
        if not name or len(name.strip()) < 2:
            raise InvalidUserDataException("Имя должно содержать хотя бы 2 символа")
        
        if not email or '@' not in email:
            raise InvalidUserDataException("Некорректный email")
        
        # Проверка уникальности email
        existing_user = self.get_user_by_email(email)
        if existing_user:
            raise InvalidUserDataException("Пользователь с таким email уже существует")
        
        # Создание пользователя
        user = UserEntity(0, name, email)
        return self.user_dao.create(user)
    
    def get_all_users(self) -> List[UserEntity]:
        return self.user_dao.get_all()
    
    def get_user_by_id(self, user_id: int) -> UserEntity:
        user = self.user_dao.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"Пользователь с ID {user_id} не найден")
        return user
    
    def get_user_by_email(self, email: str) -> Optional[UserEntity]:
        with sqlite3.connect(self.user_dao.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, email FROM users WHERE email = ?", (email,))
            row = cursor.fetchone()
            if row:
                return UserEntity(row[0], row[1], row[2])
            return None
    
    def update_user(self, user_id: int, name: str, email: str) -> UserEntity:
        # Валидация
        if not name or len(name.strip()) < 2:
            raise InvalidUserDataException("Имя должно содержать хотя бы 2 символа")
        
        if not email or '@' not in email:
            raise InvalidUserDataException("Некорректный email")
        
        # Проверка существования
        existing_user = self.get_user_by_id(user_id)
        
        # Проверка уникальности email
        user_with_email = self.get_user_by_email(email)
        if user_with_email and user_with_email.id != user_id:
            raise InvalidUserDataException("Пользователь с таким email уже существует")
        
        # Обновление
        updated_user = UserEntity(user_id, name, email)
        return self.user_dao.update(updated_user)
    
    def delete_user(self, user_id: int) -> bool:
        return self.user_dao.delete(user_id)

# Слой представления (Presentation Layer) - Flask контроллеры
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
user_dao = UserDAO('users.db')
user_service = UserService(user_dao)

@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        users = user_service.get_all_users()
        return jsonify([{'id': u.id, 'name': u.name, 'email': u.email} for u in users])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        user = user_service.create_user(data['name'], data['email'])
        return jsonify({'id': user.id, 'name': user.name, 'email': user.email}), 201
    except (InvalidUserDataException, KeyError) as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = user_service.get_user_by_id(user_id)
        return jsonify({'id': user.id, 'name': user.name, 'email': user.email})
    except UserNotFoundException as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
```

---

## 3. Принципы SOLID

SOLID - это набор принципов объектно-ориентированного программирования и проектирования, предложенных Робертом Мартином.

### Пример 6: Принцип единственной ответственности (SRP - Single Responsibility Principle)

```python
# Плохо: класс имеет несколько причин для изменения
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def save_to_db(self):
        # Логика сохранения в базу данных
        pass
    
    def send_email(self):
        # Логика отправки email
        pass
    
    def generate_report(self):
        # Логика генерации отчета
        pass

# Хорошо: каждый класс имеет одну ответственность
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

class UserRepository:
    def save(self, user):
        # Логика сохранения в базу данных
        pass
    
    def find_by_id(self, user_id):
        # Логика поиска пользователя
        pass

class EmailService:
    def send_email(self, recipient, subject, body):
        # Логика отправки email
        pass

class ReportGenerator:
    def generate_user_report(self, user):
        # Логика генерации отчета
        pass
```

### Пример 7: Принцип открытости/закрытости (OCP - Open/Closed Principle)

```python
from abc import ABC, abstractmethod

# Плохо: для добавления нового типа уведомления нужно изменять класс NotificationService
class NotificationServiceBad:
    def send_notification(self, notification_type, message):
        if notification_type == 'email':
            # Отправка email
            pass
        elif notification_type == 'sms':
            # Отправка SMS
            pass
        elif notification_type == 'push':
            # Отправка push-уведомления
            pass

# Хорошо: класс открыт для расширения, но закрыт для модификации
class NotificationSender(ABC):
    @abstractmethod
    def send(self, message):
        pass

class EmailNotificationSender(NotificationSender):
    def send(self, message):
        print(f"Отправка email: {message}")

class SMSNotificationSender(NotificationSender):
    def send(self, message):
        print(f"Отправка SMS: {message}")

class PushNotificationSender(NotificationSender):
    def send(self, message):
        print(f"Отправка push: {message}")

class NotificationService:
    def __init__(self, sender: NotificationSender):
        self.sender = sender
    
    def notify(self, message):
        self.sender.send(message)

# Использование
email_sender = EmailNotificationSender()
notification_service = NotificationService(email_sender)
notification_service.notify("Привет, пользователь!")
```

### Пример 8: Принцип подстановки Барбары Лисков (LSP - Liskov Substitution Principle)

```python
from abc import ABC, abstractmethod

class Bird(ABC):
    @abstractmethod
    def fly(self):
        pass

class Sparrow(Bird):
    def fly(self):
        print("Воробей летит")

class Ostrich(Bird):
    def fly(self):
        # Страус не может летать, но мы обязаны реализовать метод
        raise Exception("Страус не может летать")

# Лучше: разделить на летающих и нелетающих птиц
class FlyingBird(ABC):
    @abstractmethod
    def fly(self):
        pass

class WalkingBird(ABC):
    @abstractmethod
    def walk(self):
        pass

class Sparrow(FlyingBird):
    def fly(self):
        print("Воробей летит")

class Ostrich(WalkingBird):
    def walk(self):
        print("Страус идет")
```

### Пример 9: Принцип разделения интерфейса (ISP - Interface Segregation Principle)

```python
from abc import ABC, abstractmethod

# Плохо: крупный интерфейс, который не все могут реализовать полностью
class Worker(ABC):
    @abstractmethod
    def work(self):
        pass
    
    @abstractmethod
    def eat(self):
        pass

class Human(Worker):
    def work(self):
        print("Человек работает")
    
    def eat(self):
        print("Человек ест")

class Robot(Worker):
    def work(self):
        print("Робот работает")
    
    def eat(self):
        # Робот не ест, но должен реализовать метод
        pass  # или raise NotImplementedError

# Хорошо: раздельные интерфейсы
class Workable(ABC):
    @abstractmethod
    def work(self):
        pass

class Eatable(ABC):
    @abstractmethod
    def eat(self):
        pass

class Human(Workable, Eatable):
    def work(self):
        print("Человек работает")
    
    def eat(self):
        print("Человек ест")

class Robot(Workable):
    def work(self):
        print("Робот работает")
```

### Пример 10: Принцип инверсии зависимостей (DIP - Dependency Inversion Principle)

```python
from abc import ABC, abstractmethod

# Плохо: высокий уровень зависит от низкого уровня
class MySQLDatabase:
    def connect(self):
        print("Подключение к MySQL")
    
    def query(self, sql):
        print(f"Выполнение запроса: {sql}")

class UserServiceBad:
    def __init__(self):
        self.db = MySQLDatabase()  # Зависимость от конкретной реализации
    
    def get_user(self, user_id):
        self.db.connect()
        return self.db.query(f"SELECT * FROM users WHERE id = {user_id}")

# Хорошо: зависимости инвертированы через абстракции
class Database(ABC):
    @abstractmethod
    def connect(self):
        pass
    
    @abstractmethod
    def query(self, sql):
        pass

class MySQLDatabase(Database):
    def connect(self):
        print("Подключение к MySQL")
    
    def query(self, sql):
        print(f"Выполнение MySQL запроса: {sql}")

class PostgreSQLDatabase(Database):
    def connect(self):
        print("Подключение к PostgreSQL")
    
    def query(self, sql):
        print(f"Выполнение PostgreSQL запроса: {sql}")

class UserService:
    def __init__(self, database: Database):  # Зависимость от абстракции
        self.database = database
    
    def get_user(self, user_id):
        self.database.connect()
        return self.database.query(f"SELECT * FROM users WHERE id = {user_id}")

# Использование
mysql_db = MySQLDatabase()
user_service = UserService(mysql_db)
user_service.get_user(1)

postgres_db = PostgreSQLDatabase()
user_service_pg = UserService(postgres_db)
user_service_pg.get_user(1)
```

---

## 4. Практические задания

### Задание 1: MVC реализация
Создайте простое веб-приложение с использованием паттерна MVC, реализуйте CRUD операции для сущности "Заметка".

### Задание 2: Многослойная архитектура
Реализуйте приложение с тремя слоями: Presentation, Business Logic, Data Access, для управления задачами.

### Задание 3: Применение SOLID
Перепишите предоставленный код, применив принципы SOLID.

### Задание 4: MVP или MVVM
Создайте консольное или веб-приложение с использованием паттерна MVP или MVVM.

### Задание 5: Архитектурные решения
Спроектируйте архитектуру для интернет-магазина, применяя изученные паттерны и принципы.

---

## 5. Дополнительные задания

### Задание 6: Микросервисы
Создайте простую архитектуру с двумя микросервисами, взаимодействующими друг с другом.

### Задание 7: Dependency Injection
Реализуйте внедрение зависимостей в своем приложении.

### Задание 8: Repository Pattern
Примените паттерн Repository для доступа к данным.

---

## Контрольные вопросы:
1. В чем разница между MVC, MVP и MVVM?
2. Какие преимущества дает многослойная архитектура?
3. Сформулируйте принципы SOLID.
4. Почему важно следовать принципу единственной ответственности?
5. Как применить принцип инверсии зависимостей?