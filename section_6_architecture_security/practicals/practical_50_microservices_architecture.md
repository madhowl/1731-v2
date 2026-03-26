# Практическое занятие 50: Архитектура микросервисов

## Принципы микросервисной архитектуры, сервис-ориентированная архитектура (SOA), коммуникация между сервисами

### Цель занятия:
Изучить основные принципы микросервисной архитектуры, понять преимущества и недостатки данного подхода, освоить методы коммуникации между сервисами.

### Задачи:
1. Понять основные принципы микросервисной архитектуры
2. Изучить способы коммуникации между сервисами
3. Научиться проектировать микросервисы
4. Освоить основы оркестрации и обнаружения сервисов

### План работы:
1. Введение в микросервисную архитектуру
2. Основные принципы
3. Коммуникация между сервисами
4. API Gateway
5. Оркестрация и обнаружение сервисов
6. Практические задания

---

## 1. Введение в микросервисную архитектуру

Микросервисная архитектура - это подход к разработке программного обеспечения, при котором приложение строится как набор небольших, независимых сервисов.

### Отличия от монолитной архитектуры:

| Монолит | Микросервисы |
|---------|--------------|
| Единое приложение | Набор независимых сервисов |
| Общая база данных | Отдельные базы данных |
| Единая точка развёртывания | Независимое развёртывание |
| Сложность масштабирования | Горизонтальное масштабирование |
| Единый язык программирования | Полиглотизм |

### Преимущества микросервисов:

1. **Независимое развёртывание** - каждый сервис можно развертывать отдельно
2. **Масштабируемость** - масштабирование только необходимых сервисов
3. **Технологическая гибкость** - использование разных технологий для разных сервисов
4. **Устойчивость к ошибкам** - сбой одного сервиса не влияет на другие
5. **Быстрая разработка** - небольшие команды могут работать независимо

### Недостатки:

1. **Сложность управления** - множество независимых компонентов
2. **Распределённые системы** - сложность отладки и мониторинга
3. **Сетевая задержка** - задержки при межсервисном взаимодействии
4. **Согласованность данных** - сложность обеспечения консистентности

---

## 2. Основные принципы

### Принцип 1: Независимость сервисов

Каждый микросервис должен быть автономным и не иметь жёстких зависимостей от других сервисов.

```python
# Пример: Сервис пользователей (User Service)
from flask import Flask, jsonify, request
from dataclasses import dataclass
import uuid

app = Flask(__name__)

@dataclass
class User:
    id: str
    name: str
    email: str

# Хранилище в памяти (в реальном проекте - база данных)
users_db = {}

class UserService:
    @staticmethod
    def create_user(name: str, email: str) -> User:
        user_id = str(uuid.uuid4())
        user = User(id=user_id, name=name, email=email)
        users_db[user_id] = user
        return user
    
    @staticmethod
    def get_user(user_id: str) -> User:
        return users_db.get(user_id)
    
    @staticmethod
    def update_user(user_id: str, name: str = None, email: str = None) -> User:
        user = users_db.get(user_id)
        if not user:
            return None
        if name:
            user.name = name
        if email:
            user.email = email
        return user
    
    @staticmethod
    def delete_user(user_id: str) -> bool:
        if user_id in users_db:
            del users_db[user_id]
            return True
        return False

user_service = UserService()

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = user_service.create_user(data['name'], data['email'])
    return jsonify({'id': user.id, 'name': user.name, 'email': user.email}), 201

@app.route('/api/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = user_service.get_user(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'id': user.id, 'name': user.name, 'email': user.email})

@app.route('/api/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    user = user_service.update_user(user_id, data.get('name'), data.get('email'))
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'id': user.id, 'name': user.name, 'email': user.email})

@app.route('/api/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_service.delete_user(user_id):
        return jsonify({'message': 'User deleted'}), 200
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(port=8001)
```

### Принцип 2: Каждый сервис имеет свою базу данных

```python
# Пример: Сервис заказов (Order Service) с собственной базой данных
from flask import Flask, jsonify, request
from dataclasses import dataclass
import sqlite3
import uuid

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('orders.db')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            product_id TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            total_price REAL NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

@dataclass
class Order:
    id: str
    user_id: str
    product_id: str
    quantity: int
    total_price: float
    status: str

class OrderRepository:
    def __init__(self, db_path='orders.db'):
        self.db_path = db_path
    
    def create_order(self, user_id: str, product_id: str, quantity: int, total_price: float) -> Order:
        order_id = str(uuid.uuid4())
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "INSERT INTO orders (id, user_id, product_id, quantity, total_price, status) VALUES (?, ?, ?, ?, ?, ?)",
                (order_id, user_id, product_id, quantity, total_price, 'pending')
            )
            conn.commit()
        return Order(order_id, user_id, product_id, quantity, total_price, 'pending')
    
    def get_order(self, order_id: str) -> Order:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
            row = cursor.fetchone()
            if row:
                return Order(*row)
        return None
    
    def get_user_orders(self, user_id: str) -> list:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("SELECT * FROM orders WHERE user_id = ?", (user_id,))
            return [Order(*row) for row in cursor.fetchall()]

# Инициализация базы данных
init_db()
order_repository = OrderRepository()

@app.route('/api/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    order = order_repository.create_order(
        data['user_id'],
        data['product_id'],
        data['quantity'],
        data['total_price']
    )
    return jsonify({
        'id': order.id,
        'user_id': order.user_id,
        'product_id': order.product_id,
        'quantity': order.quantity,
        'total_price': order.total_price,
        'status': order.status
    }), 201

@app.route('/api/orders/<order_id>', methods=['GET'])
def get_order(order_id):
    order = order_repository.get_order(order_id)
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    return jsonify({
        'id': order.id,
        'user_id': order.user_id,
        'product_id': order.product_id,
        'quantity': order.quantity,
        'total_price': order.total_price,
        'status': order.status
    })

@app.route('/api/users/<user_id>/orders', methods=['GET'])
def get_user_orders(user_id):
    orders = order_repository.get_user_orders(user_id)
    return jsonify([{
        'id': o.id,
        'product_id': o.product_id,
        'quantity': o.quantity,
        'total_price': o.total_price,
        'status': o.status
    } for o in orders])

if __name__ == '__main__':
    app.run(port=8002)
```

### Принцип 3: Сервисы общаются через API

```python
# Пример: Клиент для межсервисного взаимодействия
import requests
from typing import Optional, Dict, Any

class UserServiceClient:
    """Клиент для взаимодействия с сервисом пользователей"""
    
    def __init__(self, base_url: str = "http://localhost:8001"):
        self.base_url = base_url
    
    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        try:
            response = requests.get(f"{self.base_url}/api/users/{user_id}")
            if response.status_code == 200:
                return response.json()
        except requests.RequestException as e:
            print(f"Error fetching user: {e}")
        return None
    
    def create_user(self, name: str, email: str) -> Optional[Dict[str, Any]]:
        try:
            response = requests.post(
                f"{self.base_url}/api/users",
                json={'name': name, 'email': email}
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
    
    def create_order(self, user_id: str, product_id: str, quantity: int, total_price: float) -> Optional[Dict[str, Any]]:
        try:
            response = requests.post(
                f"{self.base_url}/api/orders",
                json={
                    'user_id': user_id,
                    'product_id': product_id,
                    'quantity': quantity,
                    'total_price': total_price
                }
            )
            if response.status_code == 201:
                return response.json()
        except requests.RequestException as e:
            print(f"Error creating order: {e}")
        return None
    
    def get_user_orders(self, user_id: str) -> list:
        try:
            response = requests.get(f"{self.base_url}/api/users/{user_id}/orders")
            if response.status_code == 200:
                return response.json()
        except requests.RequestException as e:
            print(f"Error fetching orders: {e}")
        return []


# Использование клиентов
def process_new_order(user_id: str, product_id: str, quantity: int, price: float):
    # Проверка пользователя через User Service
    user_client = UserServiceClient()
    user = user_client.get_user(user_id)
    
    if not user:
        return {"error": "Пользователь не найден"}
    
    # Создание заказа через Order Service
    order_client = OrderServiceClient()
    order = order_client.create_order(user_id, product_id, quantity, price * quantity)
    
    if order:
        return {"success": True, "order": order}
    
    return {"error": "Не удалось создать заказ"}
```

---

## 3. Коммуникация между сервисами

### Синхронная коммуникация (REST)

```python
# Пример REST API клиента с обработкой ошибок
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_session_with_retry(retries: int = 3, backoff_factor: float = 0.3):
    """Создание сессии с автоматическими повторными попытками"""
    session = requests.Session()
    retry_strategy = Retry(
        total=retries,
        backoff_factor=backoff_factor,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session

class RESTClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = create_session_with_retry()
    
    def get(self, path: str, params: dict = None):
        url = f"{self.base_url}{path}"
        response = self.session.get(url, params=params)
        response.raise_for_status()
        return response.json()
    
    def post(self, path: str, data: dict = None):
        url = f"{self.base_url}{path}"
        response = self.session.post(url, json=data)
        response.raise_for_status()
        return response.json()
    
    def put(self, path: str, data: dict = None):
        url = f"{self.base_url}{path}"
        response = self.session.put(url, json=data)
        response.raise_for_status()
        return response.json()
    
    def delete(self, path: str):
        url = f"{self.base_url}{path}"
        response = self.session.delete(url)
        response.raise_for_status()
        return response.json()
```

### Асинхронная коммуникация (Message Queue)

```python
# Пример асинхронной коммуникации через очередь сообщений
import json
import pika
from typing import Callable, Any

class MessageQueue:
    """Класс для работы с очередью сообщений (RabbitMQ)"""
    
    def __init__(self, host: str = 'localhost', queue_name: str = 'default'):
        self.host = host
        self.queue_name = queue_name
        self.connection = None
        self.channel = None
    
    def connect(self):
        """Установка соединения с очередью"""
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.host)
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)
    
    def publish(self, message: dict):
        """Публикация сообщения в очередь"""
        if not self.channel:
            self.connect()
        
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Сообщение сохраняется на диске
                content_type='application/json'
            )
        )
    
    def consume(self, callback: Callable[[dict], None]):
        """Получение сообщений из очереди"""
        if not self.channel:
            self.connect()
        
        def wrapper(ch, method, properties, body):
            message = json.loads(body)
            callback(message)
            ch.basic_ack(delivery_tag=method.delivery_tag)
        
        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=self.queue_name, on_message_callback=wrapper)
        self.channel.start_consuming()
    
    def close(self):
        """Закрытие соединения"""
        if self.connection:
            self.connection.close()


# Пример использования: сервис уведомлений
class NotificationService:
    def __init__(self):
        self.queue = MessageQueue(queue_name='notifications')
    
    def send_notification(self, user_id: str, message: str, notification_type: str = 'email'):
        """Отправка уведомления через очередь"""
        self.queue.publish({
            'user_id': user_id,
            'message': message,
            'type': notification_type,
            'timestamp': str(datetime.now())
        })
    
    def process_notifications(self):
        """Обработка входящих уведомлений"""
        def handle_notification(message: dict):
            print(f"Обработка уведомления для пользователя {message['user_id']}")
            print(f"Сообщение: {message['message']}")
            print(f"Тип: {message['type']}")
        
        self.queue.consume(handle_notification)

# Пример событийной архитектуры
class EventDrivenOrderService:
    """Сервис заказов, основанный на событиях"""
    
    def __init__(self):
        self.order_created_queue = MessageQueue(queue_name='order_created')
        self.order_updated_queue = MessageQueue(queue_name='order_updated')
    
    def create_order(self, user_id: str, items: list):
        # Создание заказа...
        order_id = "ORD123"
        
        # Публикация события
        self.order_created_queue.publish({
            'event': 'order_created',
            'order_id': order_id,
            'user_id': user_id,
            'items': items,
            'timestamp': str(datetime.now())
        })
        
        return order_id
    
    def update_order_status(self, order_id: str, new_status: str):
        # Обновление статуса...
        
        # Публикация события
        self.order_updated_queue.publish({
            'event': 'order_status_updated',
            'order_id': order_id,
            'new_status': new_status,
            'timestamp': str(datetime.now())
        })
```

---

## 4. API Gateway

API Gateway - это единая точка входа для всех клиентов, которая маршрутизирует запросы к соответствующим микросервисам.

```python
# Пример простого API Gateway на Flask
from flask import Flask, request, jsonify
import requests
from typing import Dict, Any

app = Flask(__name__)

# Конфигурация сервисов
SERVICES = {
    'users': 'http://localhost:8001',
    'orders': 'http://localhost:8002',
    'products': 'http://localhost:8003',
    'notifications': 'http://localhost:8004'
}

class APIGateway:
    """Простой API Gateway для маршрутизации запросов"""
    
    @staticmethod
    def route_request(service_name: str, path: str, method: str, data: Any = None) -> tuple:
        """Маршрутизация запроса к соответствующему сервису"""
        
        if service_name not in SERVICES:
            return jsonify({'error': 'Service not found'}), 404
        
        service_url = SERVICES[service_name]
        url = f"{service_url}{path}"
        
        try:
            if method == 'GET':
                response = requests.get(url, params=request.args)
            elif method == 'POST':
                response = requests.post(url, json=data)
            elif method == 'PUT':
                response = requests.put(url, json=data)
            elif method == 'DELETE':
                response = requests.delete(url)
            else:
                return jsonify({'error': 'Method not allowed'}), 405
            
            return jsonify(response.json()), response.status_code
            
        except requests.RequestException as e:
            return jsonify({'error': f'Service unavailable: {str(e)}'}), 503
    
    @staticmethod
    def aggregate_results(*requests_data):
        """Агрегация результатов от нескольких сервисов"""
        results = []
        for service_name, path, params in requests_data:
            try:
                service_url = SERVICES.get(service_name)
                if service_url:
                    response = requests.get(f"{service_url}{path}", params=params)
                    if response.status_code == 200:
                        results.append(response.json())
            except requests.RequestException:
                pass
        return results


gateway = APIGateway()

# Маршруты для сервиса пользователей
@app.route('/api/users', methods=['GET', 'POST'])
def users_handler():
    if request.method == 'GET':
        return gateway.route_request('users', '/api/users', 'GET')
    return gateway.route_request('users', '/api/users', 'POST', request.get_json())

@app.route('/api/users/<user_id>', methods=['GET', 'PUT', 'DELETE'])
def user_detail_handler(user_id):
    path = f'/api/users/{user_id}'
    method = request.method
    data = request.get_json() if method in ['POST', 'PUT'] else None
    return gateway.route_request('users', path, method, data)

# Маршруты для сервиса заказов
@app.route('/api/orders', methods=['GET', 'POST'])
def orders_handler():
    if request.method == 'GET':
        return gateway.route_request('orders', '/api/orders', 'GET')
    return gateway.route_request('orders', '/api/orders', 'POST', request.get_json())

@app.route('/api/orders/<order_id>', methods=['GET'])
def order_detail_handler(order_id):
    return gateway.route_request('orders', f'/api/orders/{order_id}', 'GET')

# Пример агрегированного эндпоинта
@app.route('/api/users/<user_id>/dashboard')
def user_dashboard(user_id):
    """Агрегация данных из нескольких сервисов"""
    # Получение данных пользователя
    user_request = ('users', f'/api/users/{user_id}', {})
    # Получение заказов пользователя
    orders_request = ('orders', f'/api/users/{user_id}/orders', {})
    
    results = gateway.aggregate_results(user_request, orders_request)
    
    if results:
        return jsonify({
            'user': results[0] if len(results) > 0 else None,
            'orders': results[1] if len(results) > 1 else []
        })
    return jsonify({'error': 'Data not available'}), 503

if __name__ == '__main__':
    app.run(port=8000)
```

---

## 5. Оркестрация и обнаружение сервисов

### Пример Service Discovery

```python
# Пример простой системы обнаружения сервисов
import json
from typing import Dict, List, Optional
from datetime import datetime, timedelta

class ServiceRegistry:
    """Реестр сервисов для обнаружения"""
    
    def __init__(self):
        self.services: Dict[str, List[Dict]] = {}
    
    def register(self, service_name: str, host: str, port: int, metadata: dict = None):
        """Регистрация нового сервиса"""
        if service_name not in self.services:
            self.services[service_name] = []
        
        instance = {
            'host': host,
            'port': port,
            'metadata': metadata or {},
            'registered_at': datetime.now(),
            'health_check': 'healthy'
        }
        
        self.services[service_name].append(instance)
        print(f"Сервис {service_name} зарегистрирован: {host}:{port}")
    
    def deregister(self, service_name: str, host: str, port: int):
        """Удаление сервиса из реестра"""
        if service_name in self.services:
            self.services[service_name] = [
                s for s in self.services[service_name]
                if not (s['host'] == host and s['port'] == port)
            ]
    
    def discover(self, service_name: str) -> Optional[Dict]:
        """Обнаружение доступного экземпляра сервиса"""
        instances = self.services.get(service_name, [])
        
        # Простая балансировка - выбираем первый здоровый экземпляр
        for instance in instances:
            if instance['health_check'] == 'healthy':
                return instance
        
        return None
    
    def get_all_instances(self, service_name: str) -> List[Dict]:
        """Получение всех экземпляров сервиса"""
        return self.services.get(service_name, [])
    
    def health_check(self, service_name: str, host: str, port: int, status: str):
        """Обновление статуса здоровья сервиса"""
        for instance in self.services.get(service_name, []):
            if instance['host'] == host and instance['port'] == port:
                instance['health_check'] = status


# Использование
registry = ServiceRegistry()

# Регистрация сервисов
registry.register('user-service', 'localhost', 8001, {'version': '1.0'})
registry.register('user-service', 'localhost', 8001, {'version': '1.1'})
registry.register('order-service', 'localhost', 8002, {'version': '1.0'})
registry.register('product-service', 'localhost', 8003, {'version': '1.0'})

# Обнаружение сервиса
user_service = registry.discover('user-service')
print(f"Найден сервис пользователей: {user_service}")

order_service = registry.discover('order-service')
print(f"Найден сервис заказов: {order_service}")
```

### Пример балансировщика нагрузки

```python
import random
from typing import List, Dict

class LoadBalancer:
    """Простой балансировщик нагрузки"""
    
    def __init__(self):
        self.services: Dict[str, List[Dict]] = {}
    
    def add_instance(self, service_name: str, host: str, port: int):
        if service_name not in self.services:
            self.services[service_name] = []
        self.services[service_name].append({'host': host, 'port': port})
    
    def round_robin(self, service_name: str) -> Dict:
        """Метод Round Robin"""
        instances = self.services.get(service_name, [])
        if not instances:
            return None
        
        # Простая реализация - используем счётчик
        if not hasattr(self, '_rr_counters'):
            self._rr_counters = {}
        
        if service_name not in self._rr_counters:
            self._rr_counters[service_name] = 0
        
        index = self._rr_counters[service_name] % len(instances)
        self._rr_counters[service_name] += 1
        
        return instances[index]
    
    def least_connections(self, service_name: str) -> Dict:
        """Метод наименьшего количества соединений"""
        instances = self.services.get(service_name, [])
        if not instances:
            return None
        
        # В реальном приложении нужно отслеживать количество соединений
        return random.choice(instances)
    
    def random_choice(self, service_name: str) -> Dict:
        """Случайный выбор"""
        instances = self.services.get(service_name, [])
        if not instances:
            return None
        return random.choice(instances)


# Использование
lb = LoadBalancer()

# Добавление экземпляров сервисов
lb.add_instance('user-service', 'server1.example.com', 8001)
lb.add_instance('user-service', 'server2.example.com', 8001)
lb.add_instance('user-service', 'server3.example.com', 8001)

# Тестирование балансировки
print("Round Robin:")
for i in range(5):
    instance = lb.round_robin('user-service')
    print(f"  Запрос {i+1}: {instance['host']}")

print("\nСлучайный выбор:")
for i in range(5):
    instance = lb.random_choice('user-service')
    print(f"  Запрос {i+1}: {instance['host']}")
```

---

## 6. Практические задания

### Задание 1: Проектирование микросервисов

Спроектируйте систему электронной коммерции с микросервисной архитектурой:

1. Сервис пользователей (User Service)
2. Сервис каталога товаров (Product Service)
3. Сервис заказов (Order Service)
4. Сервис платежей (Payment Service)
5. Сервис уведомлений (Notification Service)

Для каждого сервиса определите:
- Основные функции
- API эндпоинты
- Базу данных
- Способы взаимодействия с другими сервисами

### Задание 2: Реализация межсервисного взаимодействия

Реализуйте клиент для взаимодействия между сервисами заказов и пользователей:
- Проверка существования пользователя при создании заказа
- Получение информации о пользователе при просмотре заказа

### Задание 3: API Gateway

Создайте API Gateway, который:
- Маршрутизирует запросы к соответствующим сервисам
- Обрабатывает аутентификацию
- Ограничивает скорость запросов (rate limiting)

### Задание 4: Асинхронная коммуникация

Реализуйте систему уведомлений с использованием асинхронной коммуникации:
- Сервис заказов публикует событие о новом заказе
- Сервис уведомлений обрабатывает событие и отправляет email

### Задание 5: Circuit Breaker

Реализуйте паттерн Circuit Breaker для защиты от каскадных отказов:
- При превышении порога ошибок circuit breaker открывается
- Запросы не отправляются к недоступному сервису
- После таймаута circuit breaker переходит в полуоткрытое состояние

---

## Контрольные вопросы:

1. В чём основные преимущества микросервисной архитектуры перед монолитной?
2. Какие способы коммуникации между микросервисами вы знаете?
3. Зачем нужен API Gateway?
4. Что такое Service Discovery?
5. Какие проблемы могут возникнуть при использовании микросервисной архитектуры?

---

## Дополнительные материалы:

- "Building Microservices" - Sam Newman
- "Microservices Patterns" - Chris Richardson
- "Domain-Driven Design" - Eric Evans
