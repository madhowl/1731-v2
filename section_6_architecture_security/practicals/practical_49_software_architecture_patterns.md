# Практическое занятие 49: Паттерны программной архитектуры

## Паттерны проектирования, архитектурные стили, выбор архитектуры для проекта

### Цель занятия:
Изучить основные паттерны программной архитектуры, понять различия между различными архитектурными стилями и научиться выбирать подходящую архитектуру для проекта.

### Задачи:
1. Изучить основные категории паттернов проектирования
2. Понять принципы построения различных архитектурных стилей
3. Научиться анализировать требования проекта для выбора архитектуры
4. Реализовать примеры различных паттернов

### План работы:
1. Введение в паттерны проектирования
2. Порождающие паттерны
3. Структурные паттерны
4. Поведенческие паттерны
5. Архитектурные стили
6. Выбор архитектуры для проекта
7. Практические задания

---

## 1. Введение в паттерны проектирования

Паттерны проектирования - это типовые решения часто встречающихся задач проектирования программного обеспечения. Они представляют собой проверенные временем подходы к решению определенных проблем.

### Зачем нужны паттерны:
- Повторное использование проверенных решений
- Общий язык для команды разработчиков
- Упрощение поддержки и расширения кода
- Снижение сложности разработки

### Категории паттернов:
1. **Порождающие** - создание объектов
2. **Структурные** - организация структуры классов и объектов
3. **Поведенческие** - распределение обязанностей между объектами

---

## 2. Порождающие паттерны

Порождающие паттерны автоматизируют процесс создания объектов, обеспечивая гибкость и повторное использование.

### Пример 1: Фабричный метод (Factory Method)

Фабричный метод определяет интерфейс для создания объекта, но оставляет подклассам решение о том, какой класс создавать.

```python
from abc import ABC, abstractmethod

# Абстрактный продукт
class Notification(ABC):
    @abstractmethod
    def send(self, message: str) -> None:
        pass

# Конкретные продукты
class EmailNotification(Notification):
    def send(self, message: str) -> None:
        print(f"Отправка email: {message}")

class SMSNotification(Notification):
    def send(self, message: str) -> None:
        print(f"Отправка SMS: {message}")

class PushNotification(Notification):
    def send(self, message: str) -> None:
        print(f"Отправка push-уведомления: {message}")

# Создатель
class NotificationCreator(ABC):
    @abstractmethod
    def factory_method(self) -> Notification:
        pass
    
    def send_notification(self, message: str) -> None:
        notification = self.factory_method()
        notification.send(message)

# Конкретные создатели
class EmailNotificationCreator(NotificationCreator):
    def factory_method(self) -> Notification:
        return EmailNotificationCreator()

class SMSNotificationCreator(NotificationCreator):
    def factory_method(self) -> Notification:
        return SMSNotification()

class PushNotificationCreator(NotificationCreator):
    def factory_method(self) -> Notification:
        return PushNotification()

# Использование
def client_code(creator: NotificationCreator):
    creator.send_notification("Привет, мир!")

# Создание различных типов уведомлений
email_creator = EmailNotificationCreator()
sms_creator = SMSNotificationCreator()
push_creator = PushNotificationCreator()

client_code(email_creator)
client_code(sms_creator)
client_code(push_creator)
```

### Пример 2: Абстрактная фабрика (Abstract Factory)

Абстрактная фабрика предоставляет интерфейс для создания семейств взаимосвязанных объектов.

```python
from abc import ABC, abstractmethod

# Абстрактные продукты
class Button(ABC):
    @abstractmethod
    def render(self) -> str:
        pass

class Input(ABC):
    @abstractmethod
    def render(self) -> str:
        pass

# Семейство продуктов: Light Theme
class LightButton(Button):
    def render(self) -> str:
        return "<button class='light'>Кнопка</button>"

class LightInput(Input):
    def render(self) -> str:
        return "<input class='light'>"

# Семейство продуктов: Dark Theme
class DarkButton(Button):
    def render(self) -> str:
        return "<button class='dark'>Кнопка</button>"

class DarkInput(Input):
    def render(self) -> str:
        return "<input class='dark'>"

# Абстрактная фабрика
class UIFactory(ABC):
    @abstractmethod
    def create_button(self) -> Button:
        pass
    
    @abstractmethod
    def create_input(self) -> Input:
        pass

# Конкретные фабрики
class LightThemeFactory(UIFactory):
    def create_button(self) -> Button:
        return LightButton()
    
    def create_input(self) -> Input:
        return LightInput()

class DarkThemeFactory(UIFactory):
    def create_button(self) -> Button:
        return DarkButton()
    
    def create_input(self) -> Input:
        return DarkInput()

# Использование
def create_ui(factory: UIFactory):
    button = factory.create_button()
    input_field = factory.create_input()
    print(button.render())
    print(input_field.render())

# Создание интерфейса со светлой темой
print("=== Светлая тема ===")
create_ui(LightThemeFactory())

print("\n=== Тёмная тема ===")
create_ui(DarkThemeFactory())
```

### Пример 3: Одиночка (Singleton)

Гарантирует, что класс имеет только один экземпляр, и предоставляет глобальную точку доступа к нему.

```python
class DatabaseConnection:
    """Паттерн Одиночка для подключения к базе данных"""
    _instance = None
    _connection = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance
    
    def connect(self, connection_string: str) -> None:
        if self._connection is None:
            print(f"Установка соединения с: {connection_string}")
            self._connection = connection_string
        else:
            print("Соединение уже установлено")
    
    def get_connection(self):
        return self._connection
    
    def close(self):
        print("Закрытие соединения")
        self._connection = None

# Использование
db1 = DatabaseConnection()
db1.connect("postgresql://localhost/mydb")

db2 = DatabaseConnection()
db2.connect("mysql://localhost/otherdb")

print(f"db1 is db2: {db1 is db2}")
print(f"Соединение: {db1.get_connection()}")
```

---

## 3. Структурные паттерны

Структурные паттерны показывают способы построения сложных структур из объектов.

### Пример 4: Адаптер (Adapter)

Преобразует интерфейс класса в другой интерфейс, который ожидают клиенты.

```python
from abc import ABC, abstractmethod

# Адаптируемый класс (старый интерфейс)
class OldPaymentSystem:
    def process_payment(self, amount: float) -> str:
        return f"Обработка платежа на сумму {amount} через старый API"

    def refund(self, transaction_id: str) -> str:
        return f"Возврат по транзакции {transaction_id}"

# Целевой интерфейс (новый интерфейс)
class PaymentProcessor(ABC):
    @abstractmethod
    def pay(self, amount: float) -> dict:
        pass
    
    @abstractmethod
    def refund_payment(self, transaction_id: str) -> dict:
        pass

# Адаптер
class PaymentAdapter(PaymentProcessor):
    def __init__(self):
        self.old_system = OldPaymentSystem()
    
    def pay(self, amount: float) -> dict:
        result = self.old_system.process_payment(amount)
        return {
            'status': 'success',
            'message': result,
            'amount': amount
        }
    
    def refund_payment(self, transaction_id: str) -> dict:
        result = self.old_system.refund(transaction_id)
        return {
            'status': 'success',
            'message': result,
            'transaction_id': transaction_id
        }

# Использование
processor = PaymentAdapter()
result = processor.pay(100.50)
print(result)

refund_result = processor.refund_payment("TXN12345")
print(refund_result)
```

### Пример 5: Декоратор (Decorator)

Динамически добавляет объекту новые обязанности.

```python
from abc import ABC, abstractmethod

# Базовый компонент
class Coffee(ABC):
    @abstractmethod
    def get_cost(self) -> float:
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        pass

# Конкретный компонент
class SimpleCoffee(Coffee):
    def get_cost(self) -> float:
        return 100.0
    
    def get_description(self) -> str:
        return "Кофе"

# Базовый декоратор
class CoffeeDecorator(Coffee):
    def __init__(self, coffee: Coffee):
        self._coffee = coffee
    
    def get_cost(self) -> float:
        return self._coffee.get_cost()
    
    def get_description(self) -> str:
        return self._coffee.get_description()

# Конкретные декораторы
class MilkDecorator(CoffeeDecorator):
    def get_cost(self) -> float:
        return self._coffee.get_cost() + 20.0
    
    def get_description(self) -> str:
        return self._coffee.get_description() + ", молоко"

class SugarDecorator(CoffeeDecorator):
    def get_cost(self) -> float:
        return self._coffee.get_cost() + 10.0
    
    def get_description(self) -> str:
        return self._coffee.get_description() + ", сахар"

class WhipDecorator(CoffeeDecorator):
    def get_cost(self) -> float:
        return self._coffee.get_cost() + 30.0
    
    def get_description(self) -> str:
        return self._coffee.get_description() + ", сливки"

# Использование
coffee = SimpleCoffee()
print(f"{coffee.get_description()} = {coffee.get_cost()}")

coffee_with_milk = MilkDecorator(coffee)
print(f"{coffee_with_milk.get_description()} = {coffee_with_milk.get_cost()}")

coffee_deluxe = MilkDecorator(SugarDecorator(WhipDecorator(SimpleCoffee())))
print(f"{coffee_deluxe.get_description()} = {coffee_deluxe.get_cost()}")
```

### Пример 6: Фасад (Facade)

Предоставляет унифицированный интерфейс к группе интерфейсов подсистемы.

```python
# Подсистемы
class VideoFile:
    def __init__(self, filename: str):
        self.filename = filename
        self.codec = self._extract_codec()
    
    def _extract_codec(self) -> str:
        if self.filename.endswith('.mp4'):
            return 'mp4'
        elif self.filename.endswith('.avi'):
            return 'avi'
        return 'unknown'

class CodecFactory:
    @staticmethod
    def extract(file: VideoFile):
        if file.codec == 'mp4':
            return MP4Codec()
        elif file.codec == 'avi':
            return AVICodec()
        return None

class MP4Codec:
    def decode(self):
        return "Декодирование MP4"

class AVICodec:
    def decode(self):
        return "Декодирование AVI"

class AudioMixer:
    def fix(self):
        return "Исправление звука"

# Фасад
class VideoConverter:
    def convert(self, filename: str, format: str) -> str:
        file = VideoFile(filename)
        codec = CodecFactory.extract(file)
        
        # Сложные операции скрыты за фасадом
        data = codec.decode()
        audio = AudioMixer().fix()
        
        return f"Конвертирование {filename} в {format} завершено"

# Использование - клиент видит только простой интерфейс
converter = VideoConverter()
result = converter.convert("video.avi", "mp4")
print(result)
```

---

## 4. Поведенческие паттерны

Поведенческие паттерны распределяют обязанности между объектами и определяют механизмы коммуникации.

### Пример 7: Наблюдатель (Observer)

Определяет зависимость "один-ко-многим" между объектами.

```python
from abc import ABC, abstractmethod
from typing import List

# Наблюдатель
class Observer(ABC):
    @abstractmethod
    def update(self, message: str) -> None:
        pass

# Издатель
class Subject:
    def __init__(self):
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)
    
    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)
    
    def notify(self, message: str) -> None:
        for observer in self._observers:
            observer.update(message)

# Конкретный издатель
class NewsAgency(Subject):
    def __init__(self):
        super().__init__()
        self._latest_news = ""
    
    @property
    def latest_news(self) -> str:
        return self._latest_news
    
    @latest_news.setter
    def latest_news(self, news: str) -> None:
        self._latest_news = news
        self.notify(f"Новость: {news}")

# Конкретные наблюдатели
class NewsChannel(Observer):
    def __init__(self, name: str):
        self.name = name
    
    def update(self, message: str) -> None:
        print(f"{self.name} получил: {message}")

class Subscriber(Observer):
    def __init__(self, name: str):
        self.name = name
    
    def update(self, message: str) -> None:
        print(f"{self.name} (подписчик) получил уведомление: {message}")

# Использование
agency = NewsAgency()

channel1 = NewsChannel("Первый канал")
channel2 = NewsChannel("НТВ")
subscriber = Subscriber("Иван")

agency.attach(channel1)
agency.attach(channel2)
agency.attach(subscriber)

agency.latest_news = "Python 4.0 вышел!"
print()

agency.latest_news = "Новый курс по архитектуре доступен!"
print()

agency.detach(channel2)
agency.latest_news = "Изменения в языке Python"
```

### Пример 8: Стратегия (Strategy)

Определяет семейство алгоритмов, инкапсулирует каждый из них и делает их взаимозаменяемыми.

```python
from abc import ABC, abstractmethod

# Стратегия
class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> str:
        pass

# Конкретные стратегии
class CreditCardPayment(PaymentStrategy):
    def __init__(self, card_number: str):
        self.card_number = card_number
    
    def pay(self, amount: float) -> str:
        return f"Оплата {amount} картой {self.card_number[-4:]}"

class PayPalPayment(PaymentStrategy):
    def __init__(self, email: str):
        self.email = email
    
    def pay(self, amount: float) -> str:
        return f"Оплата {amount} через PayPal ({self.email})"

class CryptoPayment(PaymentStrategy):
    def __init__(self, wallet: str):
        self.wallet = wallet
    
    def pay(self, amount: float) -> str:
        return f"Оплата {amount} криптовалютой на кошелёк {self.wallet[:8]}..."

# Контекст
class ShoppingCart:
    def __init__(self):
        self.items = []
        self.payment_strategy = None
    
    def add_item(self, item: str, price: float):
        self.items.append({'item': item, 'price': price})
    
    def set_payment_strategy(self, strategy: PaymentStrategy):
        self.payment_strategy = strategy
    
    def total(self) -> float:
        return sum(item['price'] for item in self.items)
    
    def checkout(self) -> str:
        if self.payment_strategy is None:
            return "Выберите способ оплаты"
        return self.payment_strategy.pay(self.total())

# Использование
cart = ShoppingCart()
cart.add_item("Ноутбук", 50000)
cart.add_item("Мышь", 2000)

# Оплата картой
cart.set_payment_strategy(CreditCardPayment("1234567890123456"))
print(cart.checkout())

# Оплата через PayPal
cart.set_payment_strategy(PayPalPayment("user@example.com"))
print(cart.checkout())

# Оплата криптовалютой
cart.set_payment_strategy(CryptoPayment("0x742d35Cc6634C0532925a3b844Bc9e7595f"))
print(cart.checkout())
```

### Пример 9: Команда (Command)

Инкапсулирует запрос в виде объекта, позволяя параметризовать клиентов различными запросами.

```python
from abc import ABC, abstractmethod

# Команда
class Command(ABC):
    @abstractmethod
    def execute(self) -> None:
        pass
    
    @abstractmethod
    def undo(self) -> None:
        pass

# Получатель
class TextEditor:
    def __init__(self):
        self.text = ""
    
    def insert_text(self, text: str, position: int) -> None:
        self.text = self.text[:position] + text + self.text[position:]
    
    def delete_text(self, start: int, end: int) -> str:
        deleted = self.text[start:end]
        self.text = self.text[:start] + self.text[end:]
        return deleted

# Конкретные команды
class InsertCommand(Command):
    def __init__(self, editor: TextEditor, text: str, position: int):
        self.editor = editor
        self.text = text
        self.position = position
    
    def execute(self) -> None:
        self.editor.insert_text(self.text, self.position)
    
    def undo(self) -> None:
        self.editor.delete_text(self.position, self.position + len(self.text))

class DeleteCommand(Command):
    def __init__(self, editor: TextEditor, start: int, end: int):
        self.editor = editor
        self.start = start
        self.end = end
        self.deleted_text = ""
    
    def execute(self) -> None:
        self.deleted_text = self.editor.delete_text(self.start, self.end)
    
    def undo(self) -> None:
        self.editor.insert_text(self.deleted_text, self.start)

# Инвокер
class CommandManager:
    def __init__(self):
        self.history = []
    
    def execute_command(self, command: Command) -> None:
        command.execute()
        self.history.append(command)
    
    def undo_last(self) -> None:
        if self.history:
            command = self.history.pop()
            command.undo()

# Использование
editor = TextEditor()
manager = CommandManager()

# Вставка текста
insert_cmd = InsertCommand(editor, "Привет, ", 0)
manager.execute_command(insert_cmd)
print(f"После вставки: '{editor.text}'")

# Ещё одна вставка
insert_cmd2 = InsertCommand(editor, "мир!", 7)
manager.execute_command(insert_cmd2)
print(f"После второй вставки: '{editor.text}'")

# Отмена последней команды
manager.undo_last()
print(f"После отмены: '{editor.text}'")

# Отмена первой команды
manager.undo_last()
print(f"После второй отмены: '{editor.text}'")
```

---

## 5. Архитектурные стили

Архитектурные стили определяют общую организацию системы на высоком уровне.

### Пример 10: Гексагональная архитектура (Hexagonal Architecture)

```python
# Доменный слой (ядро приложения)
class Order:
    def __init__(self, order_id: str, items: list):
        self.order_id = order_id
        self.items = items
        self.status = "pending"
    
    def calculate_total(self) -> float:
        return sum(item['price'] * item['quantity'] for item in self.items)
    
    def confirm(self):
        self.status = "confirmed"
    
    def cancel(self):
        self.status = "cancelled"

# Порт (интерфейс)
class OrderRepository(ABC):
    @abstractmethod
    def save(self, order: Order):
        pass
    
    @abstractmethod
    def find_by_id(self, order_id: str) -> Order:
        pass

class PaymentGateway(ABC):
    @abstractmethod
    def process_payment(self, amount: float) -> bool:
        pass

# Адаптеры (инфраструктура)
class InMemoryOrderRepository(OrderRepository):
    def __init__(self):
        self.orders = {}
    
    def save(self, order: Order):
        self.orders[order.order_id] = order
    
    def find_by_id(self, order_id: str) -> Order:
        return self.orders.get(order_id)

class StripePaymentGateway(PaymentGateway):
    def process_payment(self, amount: float) -> bool:
        print(f"Обработка платежа {amount} через Stripe")
        return True

# Сервис (приложение)
class OrderService:
    def __init__(self, repository: OrderRepository, payment_gateway: PaymentGateway):
        self.repository = repository
        self.payment_gateway = payment_gateway
    
    def create_order(self, order_id: str, items: list) -> Order:
        order = Order(order_id, items)
        total = order.calculate_total()
        
        if self.payment_gateway.process_payment(total):
            order.confirm()
            self.repository.save(order)
            return order
        
        order.cancel()
        return order
    
    def get_order(self, order_id: str) -> Order:
        return self.repository.find_by_id(order_id)

# Использование
repository = InMemoryOrderRepository()
payment_gateway = StripePaymentGateway()
service = OrderService(repository, payment_gateway)

items = [
    {'name': 'Товар 1', 'price': 100, 'quantity': 2},
    {'name': 'Товар 2', 'price': 50, 'quantity': 3}
]

order = service.create_order("ORD001", items)
print(f"Заказ: {order.order_id}, Статус: {order.status}, Сумма: {order.calculate_total()}")
```

---

## 6. Выбор архитектуры для проекта

### Критерии выбора архитектуры:

1. **Размер проекта**
   - Небольшой проект: простая архитектура, минимум абстракций
   - Средний проект: многослойная архитектура
   - Большой проект: микросервисы, гексагональная архитектура

2. **Команда разработки**
   - Небольшая команда: простая архитектура
   - Большая команда: модульная архитектура с чётким разделением

3. **Требования к масштабируемости**
   - Вертикальное масштабирование: монолит
   - Горизонтальное масштабирование: микросервисы

4. **Сложность домена**
   - Простой домен: Active Record
   - Сложный домен: DDD, гексагональная архитектура

### Матрица выбора:

| Требования | Рекомендуемая архитектура |
|------------|---------------------------|
| Быстрая разработка, MVP | MVC, простой монолит |
| Сложная бизнес-логика | DDD, гексагональная |
| Высокая нагрузка | Микросервисы |
| Команда 1-5 человек | Монолит |
| Команда 20+ человек | Микросервисы |
| Частые изменения | Гексагональная, модульная |

---

## 7. Практические задания

### Задание 1: Реализация паттерна "Строитель" (Builder)

Создайте систему для конструирования объекта "Пользователь" с различными опциональными полями (имя, email, телефон, адрес, дата рождения).

```python
# Пример структуры для реализации
class User:
    def __init__(self):
        self.name = None
        self.email = None
        self.phone = None
        self.address = None
        self.birth_date = None

class UserBuilder:
    def __init__(self):
        self._user = User()
    
    def with_name(self, name):
        # Реализуйте
        pass
    
    def with_email(self, email):
        # Реализуйте
        pass
    
    # Добавьте остальные методы
    
    def build(self):
        return self._user

# Использование
user = (UserBuilder()
    .with_name("Иван Иванов")
    .with_email("ivan@example.com")
    .with_phone("+7-999-123-45-67")
    .build())
```

### Задание 2: Реализация паттерна "Фасад" для библиотеки

Создайте фасад для упрощённой работы с файловой системой, который скроет сложность операций чтения, записи и архивирования файлов.

### Задание 3: Выбор архитектуры

Проанализируйте следующие сценарии и предложите подходящую архитектуру:

1. **Стартап MVP**: Команда из 3 человек, нужно быстро запустить продукт
2. **Корпоративная система**: Команда из 50 человек, высокие требования к надёжности
3. **Высоконагруженный сервис**: Ожидается миллион пользователей

### Задание 4: Реализация системы событий

Создайте систему обработки событий с использованием паттерна "Наблюдатель":
- Издатель: система заказов
- Наблюдатели: email-уведомления, SMS-уведомления, логирование

### Задание 5: Рефакторинг

Преобразуйте класс "Банковский счёт" с использованием принципов SOLID:
- Добавление новых операций не должно требовать изменения существующего кода
- Класс должен иметь только одну причину для изменения

---

## Контрольные вопросы:

1. В чём разница между паттернами "Фабричный метод" и "Абстрактная фабрика"?
2. Когда следует использовать паттерн "Одиночка"? Приведите примеры.
3. Как паттерн "Адаптер" помогает интегрировать старые системы?
4. Какие преимущества даёт гексагональная архитектура?
5. Какие факторы влияют на выбор архитектуры проекта?

---

## Дополнительные материалы:

- "Design Patterns" - Gang of Four (Эрик Гамма, Ричард Хелм, Ральф Джонсон, Джон Влиссидес)
- "Architecture Patterns with Python" - Harry Percival, Bob Gregory
- "Domain-Driven Design" - Eric Evans
