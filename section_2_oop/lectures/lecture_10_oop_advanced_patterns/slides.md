# Лекция 10: ООП - продвинутые паттерны

## Паттерны Observer, Strategy, Decorator, Adapter

### План лекции:
1. Паттерн Observer
2. Паттерн Strategy
3. Паттерн Decorator
4. Паттерн Adapter
5. Комбинация паттернов
6. Практические примеры

---

## 1. Паттерн Observer

### Понятие паттерна Observer

Паттерн Observer определяет зависимость "один ко многим" между объектами, так что при изменении состояния одного объекта все зависящие от него объекты уведомляются и обновляются автоматически.

```python
from abc import ABC, abstractmethod
from typing import List

class Observer(ABC):
    @abstractmethod
    def update(self, message: str):
        pass

class Subject(ABC):
    def __init__(self):
        self._observers: List[Observer] = []

    def attach(self, observer: Observer):
        self._observers.append(observer)

    def detach(self, observer: Observer):
        self._observers.remove(observer)

    def notify(self, message: str):
        for observer in self._observers:
            observer.update(message)

class NewsAgency(Subject):
    def __init__(self):
        super().__init__()
        self._news = ""

    @property
    def news(self):
        return self._news

    @news.setter
    def news(self, news: str):
        self._news = news
        self.notify(f"Новости: {news}")

class NewsChannel(Observer):
    def __init__(self, name: str):
        self.name = name

    def update(self, message: str):
        print(f"{self.name} получил новости: {message}")

class SocialMedia(Observer):
    def __init__(self, platform: str):
        self.platform = platform

    def update(self, message: str):
        print(f"{self.platform} публикует: {message}")

# Пример использования
agency = NewsAgency()

channel1 = NewsChannel("ТВ-канал 1")
channel2 = NewsChannel("ТВ-канал 2")
twitter = SocialMedia("Twitter")
facebook = SocialMedia("Facebook")

agency.attach(channel1)
agency.attach(channel2)
agency.attach(twitter)
agency.attach(facebook)

agency.news = "Новый Python релиз!"  # Все наблюдатели получат уведомление
```

### Реализация с использованием событий

```python
class EventManager:
    def __init__(self):
        self._listeners = {}

    def subscribe(self, event_type: str, listener):
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(listener)

    def unsubscribe(self, event_type: str, listener):
        if event_type in self._listeners:
            self._listeners[event_type].remove(listener)

    def notify(self, event_type: str, data=None):
        if event_type in self._listeners:
            for listener in self._listeners[event_type]:
                listener.handle_event(event_type, data)

class UserService:
    def __init__(self):
        self.event_manager = EventManager()

    def register_user(self, username: str):
        print(f"Пользователь {username} зарегистрирован")
        # Уведомляем подписчиков о регистрации
        self.event_manager.notify("user_registered", {"username": username})

class EmailService:
    def handle_event(self, event_type: str, data):
        if event_type == "user_registered":
            username = data["username"]
            print(f"Отправлено приветственное письмо пользователю {username}")

class NotificationService:
    def handle_event(self, event_type: str, data):
        if event_type == "user_registered":
            username = data["username"]
            print(f"Отправлено push-уведомление пользователю {username}")

# Пример использования
user_service = UserService()
email_service = EmailService()
notification_service = NotificationService()

user_service.event_manager.subscribe("user_registered", email_service)
user_service.event_manager.subscribe("user_registered", notification_service)

user_service.register_user("Иван")
```

---

## 2. Паттерн Strategy

### Понятие паттерна Strategy

Паттерн Strategy позволяет определять семейство алгоритмов, инкапсулировать каждый из них и делать их взаимозаменяемыми.

```python
from abc import ABC, abstractmethod

class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float):
        pass

class CreditCardPayment(PaymentStrategy):
    def __init__(self, card_number: str, cvv: str):
        self.card_number = card_number
        self.cvv = cvv

    def pay(self, amount: float):
        return f"Оплачено {amount} руб. по кредитной карте ****{self.card_number[-4:]}"

class PayPalPayment(PaymentStrategy):
    def __init__(self, email: str):
        self.email = email

    def pay(self, amount: float):
        return f"Оплачено {amount} руб. через PayPal ({self.email})"

class BitcoinPayment(PaymentStrategy):
    def __init__(self, wallet_address: str):
        self.wallet_address = wallet_address

    def pay(self, amount: float):
        return f"Оплачено {amount} руб. через Bitcoin ({self.wallet_address[:10]}...)"

class ShoppingCart:
    def __init__(self):
        self.items = []
        self.payment_strategy = None

    def add_item(self, name: str, price: float):
        self.items.append({"name": name, "price": price})

    def calculate_total(self):
        return sum(item["price"] for item in self.items)

    def set_payment_strategy(self, strategy: PaymentStrategy):
        self.payment_strategy = strategy

    def checkout(self):
        if self.payment_strategy is None:
            raise ValueError("Стратегия оплаты не установлена")
        
        total = self.calculate_total()
        return self.payment_strategy.pay(total)

# Пример использования
cart = ShoppingCart()
cart.add_item("Книга", 500)
cart.add_item("Мышь", 1000)

# Оплата кредитной картой
cart.set_payment_strategy(CreditCardPayment("1234567890123456", "123"))
print(cart.checkout())

# Оплата через PayPal
cart.set_payment_strategy(PayPalPayment("user@example.com"))
print(cart.checkout())
```

### Пример с сортировкой

```python
from typing import List, Callable

class SortStrategy(ABC):
    @abstractmethod
    def sort(self, data: List[int]) -> List[int]:
        pass

class BubbleSort(SortStrategy):
    def sort(self, data: List[int]) -> List[int]:
        # Упрощенная реализация пузырьковой сортировки
        result = data[:]
        n = len(result)
        for i in range(n):
            for j in range(0, n-i-1):
                if result[j] > result[j+1]:
                    result[j], result[j+1] = result[j+1], result[j]
        print("Сортировка пузырьком")
        return result

class QuickSort(SortStrategy):
    def sort(self, data: List[int]) -> List[int]:
        print("Быстрая сортировка")
        if len(data) <= 1:
            return data[:]
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return self.sort(left) + middle + self.sort(right)

class ContextSorter:
    def __init__(self, strategy: SortStrategy = None):
        self.strategy = strategy

    def set_strategy(self, strategy: SortStrategy):
        self.strategy = strategy

    def execute_sort(self, data: List[int]) -> List[int]:
        if self.strategy is None:
            raise ValueError("Стратегия сортировки не установлена")
        return self.strategy.sort(data)

# Пример использования
sorter = ContextSorter()

data = [64, 34, 25, 12, 22, 11, 90]

sorter.set_strategy(BubbleSort())
result1 = sorter.execute_sort(data)
print(f"Результат пузырьковой сортировки: {result1}")

sorter.set_strategy(QuickSort())
result2 = sorter.execute_sort(data)
print(f"Результат быстрой сортировки: {result2}")
```

---

## 3. Паттерн Decorator

### Понятие паттерна Decorator

Паттерн Decorator позволяет динамически добавлять объектам новую функциональность, оборачивая их в полезные "обертки".

```python
from abc import ABC, abstractmethod

class Component(ABC):
    @abstractmethod
    def operation(self) -> str:
        pass

class ConcreteComponent(Component):
    def operation(self) -> str:
        return "Конкретный компонент"

class Decorator(Component):
    def __init__(self, component: Component):
        self.component = component

    def operation(self) -> str:
        return self.component.operation()

class LoggingDecorator(Decorator):
    def operation(self) -> str:
        result = self.component.operation()
        return f"[LOG] {result}"

class TimingDecorator(Decorator):
    def operation(self) -> str:
        import time
        start = time.time()
        result = self.component.operation()
        end = time.time()
        return f"{result} [TIME: {end - start:.4f}s]"

class UppercaseDecorator(Decorator):
    def operation(self) -> str:
        result = self.component.operation()
        return result.upper()

# Пример использования
component = ConcreteComponent()
print(component.operation())  # Конкретный компонент

decorated = LoggingDecorator(component)
print(decorated.operation())  # [LOG] Конкретный компонент

double_decorated = TimingDecorator(LoggingDecorator(component))
print(double_decorated.operation())  # [LOG] Конкретный компонент [TIME: 0.0000s]

triple_decorated = UppercaseDecorator(TimingDecorator(LoggingDecorator(component)))
print(triple_decorated.operation())  # [LOG] КОНКРЕТНЫЙ КОМПОНЕНТ [TIME: 0.0000S]
```

### Функциональный декоратор

```python
import functools
from typing import Callable

def retry(max_attempts: int = 3, delay: float = 1.0):
    """Декоратор для повторных попыток выполнения функции"""
    def decorator(func: Callable):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        print(f"Функция {func.__name__} не выполнена после {max_attempts} попыток")
                        raise e
                    print(f"Попытка {attempt + 1} не удалась: {e}. Повтор через {delay} секунд...")
                    import time
                    time.sleep(delay)
        return wrapper
    return decorator

def cache(func: Callable):
    """Декоратор для кэширования результатов функции"""
    cache_dict = {}
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        key = str(args) + str(sorted(kwargs.items()))
        if key in cache_dict:
            print(f"Возвращаем результат из кэша для {func.__name__}")
            return cache_dict[key]
        
        result = func(*args, **kwargs)
        cache_dict[key] = result
        print(f"Сохраняем результат в кэш для {func.__name__}")
        return result
    
    return wrapper

@retry(max_attempts=2, delay=0.5)
@cache
def unreliable_function(x: int):
    import random
    if random.random() < 0.7:  # 70% шанс ошибки
        raise ConnectionError("Ошибка соединения")
    return x * 2

# Пример использования
try:
    print(unreliable_function(5))
    print(unreliable_function(5))  # Будет из кэша
except Exception as e:
    print(f"Функция завершилась с ошибкой: {e}")
```

---

## 4. Паттерн Adapter

### Понятие паттерна Adapter

Паттерн Adapter позволяет объектам с несовместимыми интерфейсами работать вместе, преобразуя интерфейс одного класса в другой, который ожидает клиент.

```python
class OldPaymentProcessor:
    """Старый класс обработки платежей"""
    def make_payment(self, amount: float) -> bool:
        print(f"Старый процессор: обработка платежа на сумму {amount} руб.")
        return True

class NewPaymentAPI:
    """Новый API для обработки платежей"""
    def initiate_transaction(self, transaction_data: dict) -> dict:
        amount = transaction_data["amount"]
        currency = transaction_data.get("currency", "RUB")
        print(f"Новый API: инициализация транзакции на {amount} {currency}")
        return {"status": "success", "transaction_id": "TX123456"}

class PaymentAdapter:
    """Адаптер для старого процессора к новому интерфейсу"""
    def __init__(self, adaptee: OldPaymentProcessor):
        self.adaptee = adaptee

    def process_payment(self, payment_data: dict):
        amount = payment_data["amount"]
        success = self.adaptee.make_payment(amount)
        return {"status": "success" if success else "failed", "adapter_used": True}

class NewAPIAdapter:
    """Адаптер для нового API к старому интерфейсу"""
    def __init__(self, adaptee: NewPaymentAPI):
        self.adaptee = adaptee

    def make_payment(self, amount: float) -> bool:
        transaction_data = {"amount": amount, "currency": "RUB"}
        result = self.adaptee.initiate_transaction(transaction_data)
        return result["status"] == "success"

# Пример использования
old_processor = OldPaymentProcessor()
new_api = NewPaymentAPI()

# Использование адаптера для старого процессора с новым интерфейсом
adapter = PaymentAdapter(old_processor)
result = adapter.process_payment({"amount": 1000})
print(f"Результат через адаптер: {result}")

# Использование адаптера для нового API со старым интерфейсом
api_adapter = NewAPIAdapter(new_api)
success = api_adapter.make_payment(1500)
print(f"Старый интерфейс с новым API: {'успех' if success else 'ошибка'}")
```

### Объектный адаптер

```python
class XMLData:
    def get_data(self) -> str:
        return "<data><item>value1</item><item>value2</item></data>"

class JSONData:
    def fetch_data(self) -> dict:
        return {"items": ["value1", "value2"]}

class XMLToJSONAdapter:
    def __init__(self, xml_source: XMLData):
        self.xml_source = xml_source

    def fetch_data(self) -> dict:
        xml_string = self.xml_source.get_data()
        # Упрощенная конвертация XML в JSON-подобный словарь
        # В реальном приложении использовалась бы библиотека для парсинга XML
        if "value1" in xml_string and "value2" in xml_string:
            return {"items": ["value1", "value2"]}
        return {"items": []}

def data_consumer(data_source):
    """Функция, ожидающая JSON-подобный интерфейс"""
    data = data_source.fetch_data()
    return [item.upper() for item in data.get("items", [])]

# Пример использования
xml_source = XMLData()
json_source = JSONData()

# Используем адаптер для работы с XML-источником как с JSON-источником
adapter = XMLToJSONAdapter(xml_source)

print("Данные из JSON-источника:", data_consumer(json_source))
print("Данные из XML-источника (через адаптер):", data_consumer(adapter))
```

---

## 5. Комбинация паттернов

### Пример комбинации Observer и Strategy

```python
class NotificationContext:
    def __init__(self, strategy=None):
        self.strategy = strategy
        self.observers = []

    def set_strategy(self, strategy):
        self.strategy = strategy

    def attach_observer(self, observer):
        self.observers.append(observer)

    def detach_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self, message):
        for observer in self.observers:
            observer.update(message)

    def send_notification(self, content):
        if self.strategy:
            formatted_content = self.strategy.format(content)
            self.notify_observers(formatted_content)
            return self.strategy.send(formatted_content)
        return False

class EmailNotificationStrategy:
    def format(self, content):
        return f"EMAIL: {content}"

    def send(self, content):
        print(f"Отправка email: {content}")
        return True

class SMSNotificationStrategy:
    def format(self, content):
        return f"SMS: {content[:160]}"  # Ограничение длины SMS

    def send(self, content):
        print(f"Отправка SMS: {content}")
        return True

class NotificationLogger(Observer):
    def update(self, message):
        print(f"[ЛОГ] Уведомление: {message}")

# Пример использования
context = NotificationContext()
logger = NotificationLogger()

context.attach_observer(logger)

# Отправка email
context.set_strategy(EmailNotificationStrategy())
context.send_notification("Важное уведомление")

print()

# Отправка SMS
context.set_strategy(SMSNotificationStrategy())
context.send_notification("Короткое уведомление")
```

---

## 6. Практические примеры

### Пример: Система обработки изображений

```python
from abc import ABC, abstractmethod
from typing import Any

class ImageProcessor(ABC):
    @abstractmethod
    def process(self, image_data: Any) -> Any:
        pass

class BasicImageProcessor(ImageProcessor):
    def process(self, image_data: Any) -> Any:
        print("Базовая обработка изображения")
        return image_data

class ImageFilterDecorator(ImageProcessor):
    def __init__(self, processor: ImageProcessor):
        self.processor = processor

    def process(self, image_data: Any) -> Any:
        processed = self.processor.process(image_data)
        return self.apply_filter(processed)

    @abstractmethod
    def apply_filter(self, image_data: Any) -> Any:
        pass

class BlurFilter(ImageFilterDecorator):
    def apply_filter(self, image_data: Any) -> Any:
        print("Применение размытия")
        return image_data

class ContrastFilter(ImageFilterDecorator):
    def apply_filter(self, image_data: Any) -> Any:
        print("Повышение контрастности")
        return image_data

class ResizeAdapter:
    def __init__(self, old_resize_lib):
        self.old_lib = old_resize_lib

    def process(self, image_data: Any) -> Any:
        # Адаптируем старую библиотеку к новому интерфейсу
        print("Использование старой библиотеки для изменения размера")
        return self.old_lib.resize_old_way(image_data, 800, 600)

class OldResizeLibrary:
    def resize_old_way(self, image, width, height):
        print(f"Старая библиотека изменяет размер до {width}x{height}")
        return image

# Стратегии обработки
class ProcessingStrategy(ABC):
    @abstractmethod
    def execute(self, processor: ImageProcessor, image_data: Any) -> Any:
        pass

class FastProcessing(ProcessingStrategy):
    def execute(self, processor: ImageProcessor, image_data: Any) -> Any:
        print("Быстрая обработка")
        return processor.process(image_data)

class QualityProcessing(ProcessingStrategy):
    def execute(self, processor: ImageProcessor, image_data: Any) -> Any:
        print("Обработка высокого качества")
        result = processor.process(image_data)
        # Дополнительная обработка для качества
        print("Постобработка для улучшения качества")
        return result

# Пример использования
image = "raw_image_data"

# Создаем цепочку обработки с декораторами
processor = ContrastFilter(BlurFilter(BasicImageProcessor()))

# Используем стратегию быстрой обработки
strategy = FastProcessing()
result = strategy.execute(processor, image)

print("\n" + "="*30 + "\n")

# Используем адаптер для старой библиотеки
old_lib = OldResizeLibrary()
resize_adapter = ResizeAdapter(old_lib)
resize_result = resize_adapter.process(image)
```

---

## Заключение

Паттерны Observer, Strategy, Decorator и Adapter позволяют создавать гибкие и расширяемые архитектуры. Каждый из этих паттернов решает конкретные задачи проектирования:
- Observer управляет зависимостями между объектами
- Strategy позволяет переключаться между алгоритмами
- Decorator добавляет функциональность без изменения класса
- Adapter обеспечивает совместимость между несовместимыми интерфейсами

## Контрольные вопросы:
1. В чем разница между паттернами Observer и Publisher-Subscriber?
2. Какие преимущества дает использование паттерна Strategy?
3. В чем отличие структурных паттернов от поведенческих?
4. Какие проблемы решает паттерн Adapter?
5. Можно ли комбинировать несколько паттернов в одном приложении?
