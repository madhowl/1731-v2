# Решения для практического занятия 48: Архитектура приложений

"""
Этот файл содержит примеры реализации различных архитектурных паттернов:
- MVC (Model-View-Controller)
- MVP (Model-View-Presenter)
- MVVM (Model-View-ViewModel)
- Многослойная архитектура
- Принципы SOLID
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import sqlite3


# =============================================================================
# Задание 1: MVC реализация
# =============================================================================

# Model - Модель данных
class User:
    """Модель пользователя"""
    def __init__(self, id: int, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email
    
    def to_dict(self):
        return {"id": self.id, "name": self.name, "email": self.email}


class UserService:
    """Сервис для работы с пользователями"""
    def __init__(self):
        self.users = []
        self.next_id = 1
    
    def create_user(self, name: str, email: str) -> User:
        user = User(self.next_id, name, email)
        self.users.append(user)
        self.next_id += 1
        return user
    
    def get_all_users(self) -> List[User]:
        return self.users
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return next((user for user in self.users if user.id == user_id), None)
    
    def update_user(self, user_id: int, name: str, email: str) -> Optional[User]:
        user = self.get_user_by_id(user_id)
        if user:
            user.name = name
            user.email = email
        return user
    
    def delete_user(self, user_id: int) -> bool:
        user = self.get_user_by_id(user_id)
        if user:
            self.users.remove(user)
            return True
        return False


# Controller - Контроллер
user_service = UserService()


def mvc_get_users():
    """Получение списка пользователей (Controller)"""
    users = user_service.get_all_users()
    return [user.to_dict() for user in users]


def mvc_get_user(user_id: int):
    """Получение пользователя по ID (Controller)"""
    user = user_service.get_user_by_id(user_id)
    return user.to_dict() if user else None


def mvc_create_user(name: str, email: str):
    """Создание пользователя (Controller)"""
    user = user_service.create_user(name, email)
    return user.to_dict()


# =============================================================================
# Задание 2: Многослойная архитектура
# =============================================================================

# Data Layer - Слой доступа к данным
class UserEntity:
    """Сущность пользователя для БД"""
    def __init__(self, id: int, name: str, email: str):
        self.id = id
        self.name = name
        self.email = email


class UserDAO:
    """Data Access Object для пользователей"""
    def __init__(self, db_path: str = ":memory:"):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Инициализация БД"""
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


# Business Logic Layer - Слой бизнес-логики
class UserNotFoundException(Exception):
    pass


class InvalidUserDataException(Exception):
    pass


class UserServiceBLL:
    """Сервис пользователей (бизнес-логика)"""
    def __init__(self, user_dao: UserDAO):
        self.user_dao = user_dao
    
    def create_user(self, name: str, email: str) -> UserEntity:
        # Валидация
        if not name or len(name.strip()) < 2:
            raise InvalidUserDataException("Имя должно содержать хотя бы 2 символа")
        
        if not email or '@' not in email:
            raise InvalidUserDataException("Некорректный email")
        
        # Проверка уникальности
        for user in self.user_dao.get_all():
            if user.email == email:
                raise InvalidUserDataException("Пользователь с таким email уже существует")
        
        user = UserEntity(0, name, email)
        return self.user_dao.create(user)
    
    def get_all_users(self) -> List[UserEntity]:
        return self.user_dao.get_all()
    
    def get_user_by_id(self, user_id: int) -> UserEntity:
        user = self.user_dao.get_by_id(user_id)
        if not user:
            raise UserNotFoundException(f"Пользователь с ID {user_id} не найден")
        return user
    
    def update_user(self, user_id: int, name: str, email: str) -> UserEntity:
        # Валидация
        if not name or len(name.strip()) < 2:
            raise InvalidUserDataException("Имя должно содержать хотя бы 2 символа")
        
        if not email or '@' not in email:
            raise InvalidUserDataException("Некорректный email")
        
        # Проверка существования
        self.get_user_by_id(user_id)
        
        user = UserEntity(user_id, name, email)
        return self.user_dao.update(user)
    
    def delete_user(self, user_id: int) -> bool:
        self.get_user_by_id(user_id)
        return self.user_dao.delete(user_id)


# Presentation Layer - Слой представления
user_dao = UserDAO('users.db')
user_service_bll = UserServiceBLL(user_dao)


def get_users():
    """Получение списка пользователей"""
    users = user_service_bll.get_all_users()
    return [{"id": u.id, "name": u.name, "email": u.email} for u in users]


def get_user(user_id: int):
    """Получение пользователя"""
    try:
        user = user_service_bll.get_user_by_id(user_id)
        return {"id": user.id, "name": user.name, "email": user.email}
    except UserNotFoundException as e:
        return {"error": str(e)}


# =============================================================================
# Задание 3: Принципы SOLID
# =============================================================================

# Принцип единственной ответственности (SRP)
class User:
    """Модель пользователя - только данные"""
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email


class UserRepository:
    """Отвечает только за сохранение в БД"""
    def save(self, user: User):
        print(f"Сохранение пользователя {user.name} в БД")
        print(f"Сохранение пользователя {user.name} в БД")
    
    def find_by_id(self, user_id: int):
        print(f"Поиск пользователя по ID {user_id}")
        return None


class EmailService:
    """Отвечает только за отправку email"""
    def send_email(self, recipient: str, subject: str, body: str):
        print(f"Отправка email на {recipient}")


class UserController:
    """Отвечает только за обработку запросов"""
    def create_user(self, name: str, email: str):
        user = User(name, email)
        repo = UserRepository()
        repo.save(user)
        return user


# Принцип открытости/закрытости (OCP)
class NotificationService:
    """Расширяемая система уведомлений"""
    def __init__(self):
        self.notifiers = []
    
    def add_notifier(self, notifier):
        self.notifiers.append(notifier)
    
    def send_notification(self, message: str):
        for notifier in self.notifiers:
            notifier.send(message)


class Notifier(ABC):
    @abstractmethod
    def send(self, message: str):
        pass


class EmailNotifier(Notifier):
    def send(self, message: str):
        print(f"Email: {message}")


class SMSNotifier(Notifier):
    def send(self, message: str):
        print(f"SMS: {message}")


class PushNotifier(Notifier):
    def send(self, message: str):
        print(f"Push: {message}")


# Принцип подстановки Барбары Лисков (LSP)
class Animal:
    def speak(self):
        return "Some sound"


class Dog(Animal):
    def speak(self):
        return "Woof!"


class Cat(Animal):
    def speak(self):
        return "Meow!"


def animal_speaks(animals: List[Animal]):
    for animal in animals:
        print(animal.speak())


# Принцип разделения интерфейса (ISP)
class Printer:
    @abstractmethod
    def print(self, document):
        pass


class Scanner:
    @abstractmethod
    def scan(self, document):
        pass


class SimplePrinter(Printer):
    def print(self, document):
        print(f"Печать: {document}")


class MultiFunctionDevice(Printer, Scanner):
    def print(self, document):
        print(f"Печать: {document}")
    
    def scan(self, document):
        print(f"Сканирование: {document}")


# Принцип инверсии зависимостей (DIP)
class MySQLDatabase:
    def connect(self):
        print("Подключение к MySQL")


class PostgreSQLDatabase:
    def connect(self):
        print("Подключение к PostgreSQL")


class DatabaseApplication:
    def __init__(self, database):
        self.database = database
    
    def connect(self):
        self.database.connect()


# =============================================================================
# Задание 4: MVP паттерн
# =============================================================================

# Model
class TaskModel:
    """Модель задачи"""
    def __init__(self):
        self.tasks = []
        self.next_id = 1
    
    def add_task(self, title: str) -> Dict:
        task = {"id": self.next_id, "title": title, "completed": False}
        self.tasks.append(task)
        self.next_id += 1
        return task
    
    def get_tasks(self) -> List[Dict]:
        return self.tasks
    
    def complete_task(self, task_id: int) -> bool:
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                return True
        return False
    
    def delete_task(self, task_id: int) -> bool:
        for i, task in enumerate(self.tasks):
            if task["id"] == task_id:
                self.tasks.pop(i)
                return True
        return False


# View
class TaskView(ABC):
    @abstractmethod
    def show_tasks(self, tasks: List[Dict]):
        pass
    
    @abstractmethod
    def show_message(self, message: str):
        pass


class ConsoleTaskView(TaskView):
    def show_tasks(self, tasks: List[Dict]):
        print("\n=== Список задач ===")
        for task in tasks:
            status = "✓" if task["completed"] else "✗"
            print(f"{task['id']}. [{status}] {task['title']}")
    
    def show_message(self, message: str):
        print(f"\n>>> {message}\n")


# Presenter
class TaskPresenter:
    def __init__(self, model: TaskModel, view: TaskView):
        self.model = model
        self.view = view
    
    def load_tasks(self):
        tasks = self.model.get_tasks()
        self.view.show_tasks(tasks)
    
    def add_task(self, title: str):
        if title.strip():
            self.model.add_task(title)
            self.view.show_message(f"Задача '{title}' добавлена!")
        else:
            self.view.show_message("Ошибка: название задачи не может быть пустым")
    
    def complete_task(self, task_id: int):
        if self.model.complete_task(task_id):
            self.view.show_message(f"Задача {task_id} выполнена!")
        else:
            self.view.show_message(f"Задача {task_id} не найдена")
    
    def delete_task(self, task_id: int):
        if self.model.delete_task(task_id):
            self.view.show_message(f"Задача {task_id} удалена!")
        else:
            self.view.show_message(f"Задача {task_id} не найдена")


# =============================================================================
# Задание 5: MVVM паттерн
# =============================================================================

class UserViewModel:
    """ViewModel для пользователя"""
    def __init__(self, model):
        self.model = model
        self._users = []
    
    @property
    def users(self):
        return self._users
    
    @users.setter
    def users(self, value):
        self._users = value
    
    def load_users(self):
        self._users = self.model.get_users()
    
    def add_user(self, name: str, email: str):
        user = self.model.add_user(name, email)
        self._users.append(user)
        return user
    
    def get_formatted_users(self):
        return [f"{user['name']} ({user['email']})" for user in self._users]


# =============================================================================
# Пример использования
# =============================================================================

def demonstrate_mvc():
    """Демонстрация MVC"""
    print("\n=== MVC Demo ===")
    
    # Создание пользователей
    mvc_create_user("Иван Иванов", "ivan@example.com")
    mvc_create_user("Мария Петрова", "maria@example.com")
    
    # Получение списка
    users = mvc_get_users()
    print(f"Пользователи: {users}")


def demonstrate_multilayer():
    """Демонстрация многослойной архитектуры"""
    print("\n=== Многослойная архитектура Demo ===")
    
    try:
        # Создание пользователя
        user = user_service_bll.create_user("Иван Иванов", "ivan@example.com")
        print(f"Создан пользователь: {user.id}, {user.name}, {user.email}")
        
        # Получение списка
        users = user_service_bll.get_all_users()
        print(f"Всего пользователей: {len(users)}")
        
    except InvalidUserDataException as e:
        print(f"Ошибка валидации: {e}")


def demonstrate_solid():
    """Демонстрация SOLID"""
    print("\n=== SOLID Demo ===")
    
    # OCP - Расширяемая система уведомлений
    notification_service = NotificationService()
    notification_service.add_notifier(EmailNotifier())
    notification_service.add_notifier(SMSNotifier())
    notification_service.add_notifier(PushNotifier())
    notification_service.send_notification("Привет!")
    
    # LSP - Полиморфизм
    animals = [Dog(), Cat(), Animal()]
    animal_speaks(animals)


def demonstrate_mvp():
    """Демонстрация MVP"""
    print("\n=== MVP Demo ===")
    
    model = TaskModel()
    view = ConsoleTaskView()
    presenter = TaskPresenter(model, view)
    
    # Добавление задач
    presenter.add_task("Изучить Python")
    presenter.add_task("Изучить Flask")
    presenter.add_task("Создать проект")
    
    # Показать задачи
    presenter.load_tasks()
    
    # Выполнить задачу
    presenter.complete_task(2)
    presenter.load_tasks()


def demonstrate_mvvm():
    """Демонстрация MVVM"""
    print("\n=== MVVM Demo ===")
    
    # Простая модель для примера
    simple_model = {
        "users": [
            {"name": "Иван", "email": "ivan@example.com"},
            {"name": "Мария", "email": "maria@example.com"}
        ],
        "get_users": lambda self: self["users"],
        "add_user": lambda self, name, email: self["users"].append({"name": name, "email": email})
    }
    simple_model["get_users"] = lambda: simple_model["users"]
    simple_model["add_user"] = lambda name, email: simple_model["users"].append({"name": name, "email": email})
    
    # Использование ViewModel
    vm = UserViewModel(simple_model)
    vm.load_users()
    print("Пользователи:", vm.get_formatted_users())


# =============================================================================
# Главная функция
# =============================================================================

def main():
    """Демонстрация решений"""
    print("=" * 70)
    print("Решения для практического занятия 48: Архитектура приложений")
    print("=" * 70)
    
    # Задание 1: MVC
    demonstrate_mvc()
    
    # Задание 2: Многослойная архитектура
    demonstrate_multilayer()
    
    # Задание 3: SOLID
    demonstrate_solid()
    
    # Задание 4: MVP
    demonstrate_mvp()
    
    # Задание 5: MVVM
    demonstrate_mvvm()
    
    print("\n" + "=" * 70)
    print("Все примеры выполнены успешно!")


if __name__ == "__main__":
    main()
