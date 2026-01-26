# Лекция 9: ООП - продолжение

## Композиция, агрегация, делегирование, паттерны проектирования (Singleton, Factory)

### План лекции:
1. Композиция и агрегация
2. Делегирование
3. Паттерн Singleton
4. Паттерн Factory
5. Практические примеры

---

## 1. Композиция и агрегация

### Понятие композиции и агрегации

Композиция и агрегация - это отношения между классами, которые позволяют создавать более сложные структуры.

**Композиция** - это отношение "часть-целое", где часть не может существовать отдельно от целого.

**Агрегация** - это отношение "часть-целое", где часть может существовать отдельно от целого.

```python
class Engine:
    def __init__(self, power):
        self.power = power

    def start(self):
        return f"Двигатель мощностью {self.power} л.с. запущен"

class Wheel:
    def __init__(self, size):
        self.size = size

    def rotate(self):
        return f"Колесо размером {self.size} вращается"

class Car:
    def __init__(self, brand, engine_power):
        self.brand = brand
        # Композиция: двигатель создается внутри автомобиля
        self.engine = Engine(engine_power)
        # Агрегация: колеса создаются отдельно и передаются в автомобиль
        self.wheels = []

    def add_wheel(self, wheel):
        self.wheels.append(wheel)

    def start(self):
        return self.engine.start()

    def drive(self):
        if len(self.wheels) >= 4:
            rotations = [wheel.rotate() for wheel in self.wheels]
            return "\n".join(rotations)
        else:
            return "Недостаточно колес для движения"

# Пример использования
car = Car("Toyota", 150)

# Добавление колес (агрегация)
front_left = Wheel(16)
front_right = Wheel(16)
rear_left = Wheel(17)
rear_right = Wheel(17)

car.add_wheel(front_left)
car.add_wheel(front_right)
car.add_wheel(rear_left)
car.add_wheel(rear_right)

print(car.start())  # Двигатель мощностью 150 л.с. запущен
print(car.drive())  # Все колеса вращаются
```

### Сравнение композиции и агрегации

```python
# Композиция - отношение "владеет" и "жизненный цикл"
class House:
    def __init__(self, address):
        self.address = address
        # Комната создается вместе с домом и уничтожается вместе с ним
        self.rooms = [Room("Спальня"), Room("Гостиная"), Room("Кухня")]

class Room:
    def __init__(self, name):
        self.name = name

# Агрегация - отношение "использует"
class University:
    def __init__(self, name):
        self.name = name
        self.students = []  # Студенты существуют независимо от университета

    def add_student(self, student):
        self.students.append(student)

class Student:
    def __init__(self, name):
        self.name = name

# Пример использования
university = University("МГУ")
student1 = Student("Иван")
student2 = Student("Мария")

university.add_student(student1)
university.add_student(student2)

# Студенты могут существовать без университета
print(f"{university.name} имеет {len(university.students)} студентов")
```

---

## 2. Делегирование

### Понятие делегирования

Делегирование - это передача выполнения операций другому объекту.

```python
class Logger:
    def log(self, message):
        print(f"[LOG] {message}")

class Calculator:
    def __init__(self):
        self.logger = Logger()

    def add(self, a, b):
        result = a + b
        self.logger.log(f"Сложение {a} + {b} = {result}")
        return result

    def multiply(self, a, b):
        result = a * b
        self.logger.log(f"Умножение {a} * {b} = {result}")
        return result

calc = Calculator()
print(calc.add(5, 3))      # [LOG] Сложение 5 + 3 = 8 \n 8
print(calc.multiply(4, 7)) # [LOG] Умножение 4 * 7 = 28 \n 28
```

### Использование __getattr__ для делегирования

```python
class SmartList:
    def __init__(self):
        self._list = []
        self.logger = Logger()

    def append(self, item):
        self._list.append(item)
        self.logger.log(f"Добавлен элемент: {item}")

    def remove(self, item):
        if item in self._list:
            self._list.remove(item)
            self.logger.log(f"Удален элемент: {item}")
        else:
            self.logger.log(f"Элемент {item} не найден для удаления")

    def __getattr__(self, name):
        # Делегирование всех остальных методов внутреннему списку
        attr = getattr(self._list, name)
        self.logger.log(f"Вызван метод: {name}")
        return attr

# Пример использования
smart_list = SmartList()
smart_list.append(1)
smart_list.append(2)
smart_list.append(3)

print(len(smart_list))  # 3
print(smart_list.count(2))  # 1
```

---

## 3. Паттерн Singleton

### Реализация Singleton с помощью метаклассов

```python
class SingletonMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class DatabaseConnection(metaclass=SingletonMeta):
    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.connection_string = "sqlite:///app.db"
            self.initialized = True
            print("Подключение к базе данных установлено")

    def query(self, sql):
        return f"Выполнен запрос: {sql}"

# Пример использования
db1 = DatabaseConnection()
db2 = DatabaseConnection()

print(db1 is db2)  # True - это один и тот же объект
print(db1.query("SELECT * FROM users;"))
```

### Реализация Singleton с помощью __new__

```python
class ConfigManager:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.settings = {
                'host': 'localhost',
                'port': 8000,
                'debug': True
            }
            self._initialized = True

    def get_setting(self, key):
        return self.settings.get(key)

    def set_setting(self, key, value):
        self.settings[key] = value

# Пример использования
config1 = ConfigManager()
config2 = ConfigManager()

config1.set_setting('host', 'example.com')
print(config2.get_setting('host'))  # example.com - то же значение
print(config1 is config2)  # True
```

### Потокобезопасный Singleton

```python
import threading

class ThreadSafeSingleton:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'initialized'):
            self.data = {}
            self.initialized = True

    def add_data(self, key, value):
        with self._lock:
            self.data[key] = value

    def get_data(self, key):
        with self._lock:
            return self.data.get(key)
```

---

## 4. Паттерн Factory

### Простая фабрика

```python
class Animal:
    def speak(self):
        pass

class Dog(Animal):
    def speak(self):
        return "Гав!"

class Cat(Animal):
    def speak(self):
        return "Мяу!"

class Bird(Animal):
    def speak(self):
        return "Чирик!"

class AnimalFactory:
    @staticmethod
    def create_animal(animal_type):
        if animal_type.lower() == "dog":
            return Dog()
        elif animal_type.lower() == "cat":
            return Cat()
        elif animal_type.lower() == "bird":
            return Bird()
        else:
            raise ValueError(f"Неизвестный тип животного: {animal_type}")

# Пример использования
factory = AnimalFactory()

dog = factory.create_animal("dog")
cat = factory.create_animal("cat")
bird = factory.create_animal("bird")

animals = [dog, cat, bird]
for animal in animals:
    print(animal.speak())
```

### Фабричный метод

```python
from abc import ABC, abstractmethod

class Document(ABC):
    @abstractmethod
    def create(self):
        pass

    def save(self):
        content = self.create()
        return f"Документ сохранен: {content}"

class PDFDocument(Document):
    def create(self):
        return "PDF документ создан"

class WordDocument(Document):
    def create(self):
        return "Word документ создан"

class SpreadsheetDocument(Document):
    def create(self):
        return "Таблица создана"

class DocumentCreator(ABC):
    @abstractmethod
    def factory_method(self):
        pass

    def create_and_save(self):
        document = self.factory_method()
        return document.save()

class PDFCreator(DocumentCreator):
    def factory_method(self):
        return PDFDocument()

class WordCreator(DocumentCreator):
    def factory_method(self):
        return WordDocument()

class SpreadsheetCreator(DocumentCreator):
    def factory_method(self):
        return SpreadsheetDocument()

# Пример использования
creators = [PDFCreator(), WordCreator(), SpreadsheetCreator()]
for creator in creators:
    print(creator.create_and_save())
```

### Абстрактная фабрика

```python
from abc import ABC, abstractmethod

# Абстрактные продукты
class Button(ABC):
    @abstractmethod
    def render(self):
        pass

class Checkbox(ABC):
    @abstractmethod
    def render(self):
        pass

# Конкретные продукты
class WindowsButton(Button):
    def render(self):
        return "Отрисовка Windows кнопки"

class MacOSButton(Button):
    def render(self):
        return "Отрисовка macOS кнопки"

class WindowsCheckbox(Checkbox):
    def render(self):
        return "Отрисовка Windows чекбокса"

class MacOSCheckbox(Checkbox):
    def render(self):
        return "Отрисовка macOS чекбокса"

# Абстрактная фабрика
class GUIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        pass

    @abstractmethod
    def create_checkbox(self) -> Checkbox:
        pass

# Конкретные фабрики
class WindowsFactory(GUIFactory):
    def create_button(self) -> Button:
        return WindowsButton()

    def create_checkbox(self) -> Checkbox:
        return WindowsCheckbox()

class MacOSFactory(GUIFactory):
    def create_button(self) -> Button:
        return MacOSButton()

    def create_checkbox(self) -> Checkbox:
        return MacOSCheckbox()

# Клиентский код
def client_code(factory: GUIFactory):
    button = factory.create_button()
    checkbox = factory.create_checkbox()
    
    print(button.render())
    print(checkbox.render())

# Пример использования
print("Windows GUI:")
client_code(WindowsFactory())

print("\nmacOS GUI:")
client_code(MacOSFactory())
```

---

## 5. Практические примеры

### Пример: Система управления заказами

```python
from enum import Enum
from datetime import datetime

class OrderStatus(Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"

class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Order:
    def __init__(self, order_id):
        self.order_id = order_id
        self.products = []
        self.status = OrderStatus.PENDING
        self.created_at = datetime.now()

    def add_product(self, product):
        self.products.append(product)

    def calculate_total(self):
        return sum(product.price for product in self.products)

    def confirm(self):
        self.status = OrderStatus.CONFIRMED

    def ship(self):
        if self.status == OrderStatus.CONFIRMED:
            self.status = OrderStatus.SHIPPED

    def deliver(self):
        if self.status == OrderStatus.SHIPPED:
            self.status = OrderStatus.DELIVERED

class OrderFactory:
    _order_counter = 0
    _lock = threading.Lock()

    @classmethod
    def create_order(cls):
        with cls._lock:
            cls._order_counter += 1
            return Order(f"ORD-{cls._order_counter:04d}")

class InventorySystem:
    def __init__(self):
        self.products = {}
        self.orders = {}

    def add_product(self, product):
        self.products[product.name] = product

    def create_order(self):
        order = OrderFactory.create_order()
        self.orders[order.order_id] = order
        return order

    def process_order(self, order_id):
        order = self.orders.get(order_id)
        if order:
            total = order.calculate_total()
            order.confirm()
            order.ship()
            order.deliver()
            return f"Заказ {order_id} обработан. Сумма: {total}"
        return "Заказ не найден"

# Пример использования
inventory = InventorySystem()

# Добавление продуктов
inventory.add_product(Product("Ноутбук", 50000))
inventory.add_product(Product("Мышь", 1500))

# Создание заказа
order = inventory.create_order()
order.add_product(inventory.products["Ноутбук"])
order.add_product(inventory.products["Мышь"])

print(f"Статус заказа: {order.status.value}")
print(inventory.process_order(order.order_id))
print(f"Итоговый статус: {order.status.value}")
```

---

## Заключение

Композиция, агрегация и делегирование позволяют создавать более гибкие и поддерживаемые архитектуры. Паттерны Singleton и Factory помогают решать частые задачи проектирования, такие как управление единственным экземпляром и создание объектов. Понимание этих концепций критически важно для разработки масштабируемых приложений.

## Контрольные вопросы:
1. В чем разница между композицией и агрегацией?
2. Как реализовать паттерн Singleton?
3. Какие проблемы решает паттерн Factory?
4. В чем преимущества использования делегирования?
5. Какие существуют варианты реализации Singleton?
