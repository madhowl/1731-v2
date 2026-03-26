"""
Упражнения к практической работе 49: Паттерны архитектуры ПО

Выполните упражнения по паттернам архитектуры программного обеспечения.
"""

# Упражнение 1: MVC
def exercise_mvc_pattern():
    """
    Реализуйте MVC паттерн.
    """
    class Model:
        def __init__(self):
            self.data = []
        
        def add_item(self, item):
            self.data.append(item)
        
        def get_data(self):
            return self.data
    
    class View:
        def display_data(self, data):
            print("Данные:", data)
    
    class Controller:
        def __init__(self, model, view):
            self.model = model
            self.view = view
        
        def add_item(self, item):
            self.model.add_item(item)
        
        def display_data(self):
            data = self.model.get_data()
            self.view.display_data(data)


# Упражнение 2: Layered Architecture
def exercise_layered_architecture():
    """
    Создайте многоуровневую архитектуру.
    """
    # Presentation Layer
    class UserController:
        def __init__(self, service):
            self.service = service
        
        def create_user(self, name, email):
            return self.service.create_user(name, email)
    
    # Business Logic Layer
    class UserService:
        def __init__(self, repository):
            self.repository = repository
        
        def create_user(self, name, email):
            if '@' not in email:
                raise ValueError("Некорректный email")
            user = User(name, email)
            return self.repository.save(user)
    
    # Data Access Layer
    class UserRepository:
        def save(self, user):
            # Сохранение в БД
            print(f"Сохранён пользователь: {user.name}")
            return user
    
    class User:
        def __init__(self, name, email):
            self.name = name
            self.email = email


# Упражнение 3: Microservices
def exercise_microservices():
    """
    Моделируйте микросервисную архитектуру.
    """
    # Service Registry
    class ServiceRegistry:
        def __init__(self):
            self.services = {}
        
        def register(self, name, url):
            self.services[name] = url
        
        def get_url(self, name):
            return self.services.get(name)
    
    # User Service
    class UserService:
        def __init__(self, registry):
            self.registry = registry
        
        def get_user(self, user_id):
            # Получение пользователя
            return {"id": user_id, "name": "Иван"}
    
    # Order Service
    class OrderService:
        def __init__(self, registry):
            self.registry = registry
            self.user_service_url = registry.get_url("user_service")
        
        def get_order_with_user(self, order_id):
            # Получение заказа и связанного пользователя
            user = self.get_user_from_service(1)
            return {"order_id": order_id, "user": user}
        
        def get_user_from_service(self, user_id):
            # Здесь будет вызов HTTP API
            return {"id": user_id, "name": "Иван"}


# Упражнение 4: Event-Driven Architecture
def exercise_event_driven():
    """
    Реализуйте событийно-ориентированную архитектуру.
    """
    class EventBus:
        def __init__(self):
            self.handlers = {}
        
        def subscribe(self, event_type, handler):
            if event_type not in self.handlers:
                self.handlers[event_type] = []
            self.handlers[event_type].append(handler)
        
        def publish(self, event):
            event_type = type(event).__name__
            if event_type in self.handlers:
                for handler in self.handlers[event_type]:
                    handler(event)
    
    class UserCreatedEvent:
        def __init__(self, user_id, name):
            self.user_id = user_id
            self.name = name
    
    class NotificationService:
        def handle_user_created(self, event):
            print(f"Отправка уведомления для пользователя {event.name}")
    
    # Использование
    bus = EventBus()
    notification_service = NotificationService()
    bus.subscribe("UserCreatedEvent", notification_service.handle_user_created)
    
    # Публикация события
    bus.publish(UserCreatedEvent(1, "Иван"))


if __name__ == "__main__":
    print("Упражнения по архитектурным паттернам")
