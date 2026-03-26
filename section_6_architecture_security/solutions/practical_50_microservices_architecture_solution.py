#!/usr/bin/env python3
"""
Практическое занятие 50: Архитектура микросервисов
Решение упражнений
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
import uuid
import json
from datetime import datetime
import sqlite3
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


# ==============================================================================
# УПРАЖНЕНИЕ 1: Сервис пользователей (User Service)
# ==============================================================================

print("=" * 60)
print("Упражнение 1: Сервис пользователей")
print("=" * 60)


@dataclass
class User:
    """Модель пользователя"""
    id: str
    name: str
    email: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


class UserService:
    """Сервис пользователей"""
    
    def __init__(self):
        self.users_db: Dict[str, User] = {}
    
    def create_user(self, name: str, email: str) -> User:
        """Создание пользователя"""
        user_id = str(uuid.uuid4())
        user = User(id=user_id, name=name, email=email)
        self.users_db[user_id] = user
        return user
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Получение пользователя по ID"""
        return self.users_db.get(user_id)
    
    def get_all_users(self) -> List[User]:
        """Получение всех пользователей"""
        return list(self.users_db.values())
    
    def update_user(self, user_id: str, name: str = None, email: str = None) -> Optional[User]:
        """Обновление пользователя"""
        user = self.users_db.get(user_id)
        if not user:
            return None
        if name:
            user.name = name
        if email:
            user.email = email
        return user
    
    def delete_user(self, user_id: str) -> bool:
        """Удаление пользователя"""
        if user_id in self.users_db:
            del self.users_db[user_id]
            return True
        return False


# Тестирование
user_service = UserService()

# Создание пользователей
user1 = user_service.create_user("Иван", "ivan@example.com")
user2 = user_service.create_user("Мария", "maria@example.com")

print(f"Создан пользователь: {user1.name} ({user1.email})")
print(f"ID пользователя: {user1.id}")

# Получение пользователя
found_user = user_service.get_user(user1.id)
print(f"Найден пользователь: {found_user.name}")

# Обновление пользователя
user_service.update_user(user1.id, name="Иван Иванов")
updated_user = user_service.get_user(user1.id)
print(f"Обновлённое имя: {updated_user.name}")

# Удаление пользователя
user_service.delete_user(user2.id)
print(f"Всего пользователей: {len(user_service.get_all_users())}")


# ==============================================================================
# УПРАЖНЕНИЕ 2: Сервис заказов (Order Service)
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 2: Сервис заказов")
print("=" * 60)


@dataclass
class Order:
    """Модель заказа"""
    id: str
    user_id: str
    product_id: str
    quantity: int
    total_price: float
    status: str
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


class OrderRepository:
    """Репозиторий заказов"""
    
    def __init__(self, db_path: str = ':memory:'):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Инициализация БД"""
        conn = sqlite3.connect(self.db_path)
        conn.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id TEXT PRIMARY KEY,
                user_id TEXT NOT NULL,
                product_id TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                total_price REAL NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()
    
    def create_order(self, user_id: str, product_id: str, quantity: int, total_price: float) -> Order:
        """Создание заказа"""
        order_id = str(uuid.uuid4())
        order = Order(
            id=order_id,
            user_id=user_id,
            product_id=product_id,
            quantity=quantity,
            total_price=total_price,
            status='pending'
        )
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO orders (id, user_id, product_id, quantity, total_price, status, created_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (order.id, order.user_id, order.product_id, order.quantity, order.total_price, order.status, order.created_at)
            )
            conn.commit()
        
        return order
    
    def get_order(self, order_id: str) -> Optional[Order]:
        """Получение заказа по ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
            row = cursor.fetchone()
            if row:
                return Order(*row)
        return None
    
    def get_user_orders(self, user_id: str) -> List[Order]:
        """Получение заказов пользователя"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT * FROM orders WHERE user_id = ?", (user_id,))
            return [Order(*row) for row in cursor.fetchall()]
    
    def update_order_status(self, order_id: str, status: str) -> bool:
        """Обновление статуса заказа"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("UPDATE orders SET status = ? WHERE id = ?", (status, order_id))
            conn.commit()
            return cursor.rowcount > 0


# Тестирование
order_repository = OrderRepository()

# Создание заказов
order1 = order_repository.create_order(user1.id, "PROD-001", 2, 500.0)
order2 = order_repository.create_order(user1.id, "PROD-002", 1, 250.0)

print(f"Создан заказ: {order1.id}")
print(f"Статус: {order1.status}")

# Получение заказов пользователя
user_orders = order_repository.get_user_orders(user1.id)
print(f"Заказов у пользователя: {len(user_orders)}")

# Обновление статуса
order_repository.update_order_status(order1.id, "shipped")
updated_order = order_repository.get_order(order1.id)
print(f"Обновлённый статус: {updated_order.status}")


# ==============================================================================
# УПРАЖНЕНИЕ 3: Клиенты для межсервисного взаимодействия
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 3: Клиенты для межсервисного взаимодействия")
print("=" * 60)


class UserServiceClient:
    """Клиент для взаимодействия с сервисом пользователей"""
    
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        """Создание сессии с retry"""
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Получение пользователя"""
        try:
            response = self.session.get(f"{self.base_url}/api/users/{user_id}", timeout=5)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException as e:
            print(f"Error fetching user: {e}")
        return None
    
    def create_user(self, name: str, email: str) -> Optional[Dict[str, Any]]:
        """Создание пользователя"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/users",
                json={'name': name, 'email': email},
                timeout=5
            )
            if response.status_code == 201:
                return response.json()
        except requests.RequestException as e:
            print(f"Error creating user: {e}")
        return None


class OrderServiceClient:
    """Клиент для взаимодействия с сервисом заказов"""
    
    def __init__(self, base_url: str = "http://localhost:8002"):
        self.base_url = base_url
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=0.5,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session
    
    def create_order(self, user_id: str, product_id: str, quantity: int, total_price: float) -> Optional[Dict[str, Any]]:
        """Создание заказа"""
        try:
            response = self.session.post(
                f"{self.base_url}/api/orders",
                json={
                    'user_id': user_id,
                    'product_id': product_id,
                    'quantity': quantity,
                    'total_price': total_price
                },
                timeout=5
            )
            if response.status_code == 201:
                return response.json()
        except requests.RequestException as e:
            print(f"Error creating order: {e}")
        return None
    
    def get_user_orders(self, user_id: str) -> List[Dict[str, Any]]:
        """Получение заказов пользователя"""
        try:
            response = self.session.get(f"{self.base_url}/api/users/{user_id}/orders", timeout=5)
            if response.status_code == 200:
                return response.json()
        except requests.RequestException as e:
            print(f"Error fetching orders: {e}")
        return []


# Симуляция межсервисного взаимодействия (без реальных HTTP запросов)
def process_new_order(user_id: str, product_id: str, quantity: int, price: float, user_service: UserService, order_repo: OrderRepository) -> Dict[str, Any]:
    """Обработка нового заказа с проверкой пользователя"""
    
    # Проверка пользователя
    user = user_service.get_user(user_id)
    if not user:
        return {"error": "Пользователь не найден"}
    
    # Создание заказа
    order = order_repo.create_order(user_id, product_id, quantity, price * quantity)
    
    return {
        "success": True,
        "order": {
            "id": order.id,
            "user_id": order.user_id,
            "product_id": order.product_id,
            "quantity": order.quantity,
            "total_price": order.total_price,
            "status": order.status
        }
    }


# Тестирование
result = process_new_order(user1.id, "PROD-003", 3, 100.0, user_service, order_repository)
print(f"Результат: {result}")


# ==============================================================================
# УПРАЖНЕНИЕ 4: Синхронная и асинхронная коммуникация
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 4: Синхронная и асинхронная коммуникация")
print("=" * 60)


class RESTClient:
    """REST клиент с retry логикой"""
    
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = self._create_session()
    
    def _create_session(self) -> requests.Session:
        session = requests.Session()
        retry_strategy = Retry(
            total=3,
            backoff_factor=0.3,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session
    
    def get(self, path: str, params: dict = None) -> Dict[str, Any]:
        """GET запрос"""
        url = f"{self.base_url}{path}"
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {'error': str(e)}
    
    def post(self, path: str, data: dict = None) -> Dict[str, Any]:
        """POST запрос"""
        url = f"{self.base_url}{path}"
        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {'error': str(e)}
    
    def put(self, path: str, data: dict = None) -> Dict[str, Any]:
        """PUT запрос"""
        url = f"{self.base_url}{path}"
        try:
            response = self.session.put(url, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {'error': str(e)}
    
    def delete(self, path: str) -> Dict[str, Any]:
        """DELETE запрос"""
        url = f"{self.base_url}{path}"
        try:
            response = self.session.delete(url)
            response.raise_for_status()
            return response.json() if response.content else {}
        except requests.RequestException as e:
            return {'error': str(e)}


# Симуляция асинхронной коммуникации через очередь сообщений
class MessageQueue:
    """Симуляция очереди сообщений"""
    
    def __init__(self, queue_name: str = 'default'):
        self.queue_name = queue_name
        self.messages: List[Dict[str, Any]] = []
    
    def publish(self, message: Dict[str, Any]) -> bool:
        """Публикация сообщения"""
        self.messages.append(message)
        print(f"Сообщение опубликовано в очередь {self.queue_name}: {message.get('event', 'unknown')}")
        return True
    
    def consume(self) -> List[Dict[str, Any]]:
        """Получение всех сообщений"""
        messages = self.messages.copy()
        self.messages.clear()
        return messages


class NotificationService:
    """Сервис уведомлений"""
    
    def __init__(self):
        self.queue = MessageQueue(queue_name='notifications')
    
    def send_notification(self, user_id: str, message: str, notification_type: str = 'email') -> bool:
        """Отправка уведомления через очередь"""
        return self.queue.publish({
            'user_id': user_id,
            'message': message,
            'type': notification_type,
            'timestamp': datetime.now().isoformat()
        })


class EventDrivenOrderService:
    """Сервис заказов, основанный на событиях"""
    
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository
        self.order_created_queue = MessageQueue(queue_name='order_created')
        self.order_updated_queue = MessageQueue(queue_name='order_updated')
        self.notification_service = NotificationService()
    
    def create_order(self, user_id: str, product_id: str, quantity: int, total_price: float) -> Order:
        """Создание заказа с публикацией события"""
        order = self.order_repository.create_order(user_id, product_id, quantity, total_price)
        
        # Публикация события
        self.order_created_queue.publish({
            'event': 'order_created',
            'order_id': order.id,
            'user_id': user_id,
            'product_id': product_id,
            'quantity': quantity,
            'total_price': total_price,
            'timestamp': datetime.now().isoformat()
        })
        
        # Отправка уведомления
        self.notification_service.send_notification(
            user_id,
            f"Заказ {order.id} создан",
            'email'
        )
        
        return order


# Тестирование
event_service = EventDrivenOrderService(order_repository)
order = event_service.create_order(user1.id, "PROD-004", 1, 150.0)
print(f"Создан заказ: {order.id}")


# ==============================================================================
# УПРАЖНЕНИЕ 5: API Gateway
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 5: API Gateway")
print("=" * 60)


class APIGateway:
    """Простой API Gateway"""
    
    def __init__(self):
        self.routes: Dict[str, Dict[str, Any]] = {}
    
    def register_route(self, path: str, service: str, methods: List[str] = None):
        """Регистрация маршрута"""
        self.routes[path] = {
            'service': service,
            'methods': methods or ['GET']
        }
    
    def route_request(self, path: str, method: str) -> Optional[Dict[str, Any]]:
        """Маршрутизация запроса"""
        # Упрощённая маршрутизация
        for route_path, config in self.routes.items():
            if path.startswith(route_path):
                return {
                    'service': config['service'],
                    'method': method,
                    'path': path
                }
        return None


# Тестирование
gateway = APIGateway()
gateway.register_route('/api/users', 'user-service', ['GET', 'POST', 'PUT', 'DELETE'])
gateway.register_route('/api/orders', 'order-service', ['GET', 'POST'])
gateway.register_route('/api/products', 'product-service', ['GET'])

route = gateway.route_request('/api/users/123', 'GET')
print(f"Маршрут: {route}")

route = gateway.route_request('/api/orders', 'POST')
print(f"Маршрут: {route}")


# ==============================================================================
# УПРАЖНЕНИЕ 6: Circuit Breaker для микросервисов
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 6: Circuit Breaker")
print("=" * 60)


from enum import Enum
import time
import random


class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"


class CircuitBreaker:
    """Circuit Breaker для защиты от каскадных отказов"""
    
    def __init__(self, name: str, failure_threshold: int = 3, timeout: float = 5.0):
        self.name = name
        self.failure_threshold = failure_threshold
        self.timeout = timeout
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None
    
    def call(self, func, *args, **kwargs):
        """Вызов функции с защитой"""
        if self.state == CircuitState.OPEN:
            if time.time() - self.last_failure_time >= self.timeout:
                self.state = CircuitState.HALF_OPEN
                print(f"Circuit breaker {self.name} перешёл в состояние HALF_OPEN")
            else:
                raise Exception(f"Circuit breaker {self.name} OPEN - запрос заблокирован")
        
        try:
            result = func(*args, **kwargs)
            self.on_success()
            return result
        except Exception as e:
            self.on_failure()
            raise
    
    def on_success(self):
        """Обработка успешного вызова"""
        if self.state == CircuitState.HALF_OPEN:
            self.state = CircuitState.CLOSED
            self.failure_count = 0
            print(f"Circuit breaker {self.name} CLOSED")
        elif self.state == CircuitState.CLOSED:
            self.failure_count = 0
    
    def on_failure(self):
        """Обработка неудачного вызова"""
        self.failure_count += 1
        self.last_failure_time = time.time()
        
        if self.failure_count >= self.failure_threshold:
            self.state = CircuitState.OPEN
            print(f"Circuit breaker {self.name} OPENED после {self.failure_count} отказов")


def unstable_service(data: str) -> str:
    """Нестабильный сервис"""
    if random.random() < 0.5:
        raise ConnectionError("Service unavailable")
    return f"Success: {data}"


# Тестирование
breaker = CircuitBreaker("user-service", failure_threshold=3, timeout=2.0)

for i in range(10):
    try:
        result = breaker.call(unstable_service, f"request_{i}")
        print(f"Request {i}: {result}")
    except Exception as e:
        print(f"Request {i}: {e}")
        time.sleep(0.5)

print("\n" + "=" * 60)
print("Все упражнения выполнены!")
print("=" * 60)
