# Решения для практического занятия 15: ООП - паттерн Observer

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Callable, Set
import asyncio
import threading
import time
from datetime import datetime

# Решение задания 1: Базовая реализация Observer
class Observer(ABC):
    """Интерфейс наблюдателя"""
    @abstractmethod
    def update(self, subject, *args, **kwargs):
        pass

class Subject(ABC):
    """Интерфейс наблюдаемого объекта"""
    def __init__(self):
        self._observers: List[Observer] = []
        self._lock = threading.Lock()
    
    def attach(self, observer: Observer):
        """Добавить наблюдателя"""
        with self._lock:
            if observer not in self._observers:
                self._observers.append(observer)
    
    def detach(self, observer: Observer):
        """Удалить наблюдателя"""
        with self._lock:
            if observer in self._observers:
                self._observers.remove(observer)
    
    def notify(self, *args, **kwargs):
        """Уведомить всех наблюдателей"""
        with self._lock:
            observers_copy = self._observers[:]  # Создаем копию для избежания проблем с изменением списка во время итерации
        
        for observer in observers_copy:
            try:
                observer.update(self, *args, **kwargs)
            except Exception as e:
                print(f"Ошибка при уведомлении наблюдателя: {e}")

class CurrencyRate(Subject):
    """Класс курса валюты как наблюдаемый объект"""
    def __init__(self, currency: str, rate: float):
        super().__init__()
        self.currency = currency
        self._rate = rate
        self.timestamp = datetime.now()
    
    @property
    def rate(self):
        return self._rate
    
    @rate.setter
    def rate(self, new_rate: float):
        if new_rate != self._rate:
            old_rate = self._rate
            self._rate = new_rate
            self.timestamp = datetime.now()
            print(f"Курс {self.currency} изменился с {old_rate} на {new_rate} в {self.timestamp.strftime('%H:%M:%S')}")
            self.notify(old_rate=old_rate, new_rate=new_rate, timestamp=self.timestamp)

class EmailNotifier(Observer):
    """Наблюдатель для отправки email-уведомлений"""
    def __init__(self, email: str):
        self.email = email
    
    def update(self, subject, *args, **kwargs):
        if isinstance(subject, CurrencyRate):
            old_rate = kwargs.get('old_rate')
            new_rate = kwargs.get('new_rate')
            timestamp = kwargs.get('timestamp')
            print(f"EMAIL NOTIFICATION для {self.email}: Курс {subject.currency} изменился с {old_rate} на {new_rate} в {timestamp.strftime('%H:%M:%S')}")

class SMSNotifier(Observer):
    """Наблюдатель для отправки SMS-уведомлений"""
    def __init__(self, phone: str):
        self.phone = phone
    
    def update(self, subject, *args, **kwargs):
        if isinstance(subject, CurrencyRate):
            old_rate = kwargs.get('old_rate')
            new_rate = kwargs.get('new_rate')
            timestamp = kwargs.get('timestamp')
            print(f"SMS NOTIFICATION для {self.phone}: Курс {subject.currency} изменился с {old_rate} на {new_rate} в {timestamp.strftime('%H:%M:%S')}")

# Решение задания 2: Использование встроенных средств
class EventManager:
    """Менеджер событий с использованием callback-функций"""
    def __init__(self):
        self._callbacks: Dict[str, List[Callable]] = {}
        self._lock = threading.Lock()
    
    def subscribe(self, event_type: str, callback: Callable):
        """Подписаться на событие"""
        with self._lock:
            if event_type not in self._callbacks:
                self._callbacks[event_type] = []
            if callback not in self._callbacks[event_type]:
                self._callbacks[event_type].append(callback)
    
    def unsubscribe(self, event_type: str, callback: Callable):
        """Отписаться от события"""
        with self._lock:
            if event_type in self._callbacks and callback in self._callbacks[event_type]:
                self._callbacks[event_type].remove(callback)
    
    def emit(self, event_type: str, data: Any = None):
        """Вызвать все callback-функции для типа события"""
        with self._lock:
            callbacks_copy = self._callbacks.get(event_type, [])[:]
        
        for callback in callbacks_copy:
            try:
                callback(event_type, data)
            except Exception as e:
                print(f"Ошибка при вызове callback-функции: {e}")

# Решение задания 3: Параметризованные уведомления
class EventPublisher:
    """Издатель событий с фильтрацией по типам"""
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
        self._lock = threading.Lock()
    
    def subscribe(self, event_type: str, handler: Callable):
        """Подписаться на определенный тип события"""
        with self._lock:
            if event_type not in self._subscribers:
                self._subscribers[event_type] = []
            if handler not in self._subscribers[event_type]:
                self._subscribers[event_type].append(handler)
    
    def unsubscribe(self, event_type: str, handler: Callable):
        """Отписаться от определенного типа события"""
        with self._lock:
            if event_type in self._subscribers and handler in self._subscribers[event_type]:
                self._subscribers[event_type].remove(handler)
    
    def publish(self, event_type: str, event_data: Dict[str, Any] = None):
        """Опубликовать событие с данными"""
        with self._lock:
            handlers_copy = self._subscribers.get(event_type, [])[:]
        
        for handler in handlers_copy:
            try:
                handler(event_type, event_data or {})
            except Exception as e:
                print(f"Ошибка при обработке события: {e}")

class EventSubscriber:
    """Подписчик на события"""
    def __init__(self, name: str):
        self.name = name
    
    def handle_event(self, event_type: str, event_data: Dict[str, Any]):
        """Обработать событие"""
        print(f"{self.name} получил событие '{event_type}': {event_data}")

# Решение задания 4: Асинхронный Observer
class AsyncObserver(ABC):
    """Асинхронный интерфейс наблюдателя"""
    @abstractmethod
    async def update_async(self, subject, *args, **kwargs):
        pass

class AsyncSubject(ABC):
    """Асинхронный наблюдаемый объект"""
    def __init__(self):
        self._async_observers: List[AsyncObserver] = []
        self._lock = asyncio.Lock()
    
    async def attach_async(self, observer: AsyncObserver):
        """Добавить асинхронного наблюдателя"""
        async with self._lock:
            if observer not in self._async_observers:
                self._async_observers.append(observer)
    
    async def detach_async(self, observer: AsyncObserver):
        """Удалить асинхронного наблюдателя"""
        async with self._lock:
            if observer in self._async_observers:
                self._async_observers.remove(observer)
    
    async def notify_async(self, *args, **kwargs):
        """Асинхронно уведомить всех наблюдателей"""
        async with self._lock:
            observers_copy = self._async_observers[:]
        
        tasks = []
        for observer in observers_copy:
            task = asyncio.create_task(observer.update_async(self, *args, **kwargs))
            tasks.append(task)
        
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    print(f"Ошибка при уведомлении асинхронного наблюдателя {i}: {result}")

class AsyncCurrencyRate(AsyncSubject):
    """Асинхронный класс курса валюты"""
    def __init__(self, currency: str, rate: float):
        super().__init__()
        self.currency = currency
        self._rate = rate
        self.timestamp = datetime.now()
    
    @property
    def rate(self):
        return self._rate
    
    @rate.setter
    async def rate(self, new_rate: float):
        if new_rate != self._rate:
            old_rate = self._rate
            self._rate = new_rate
            self.timestamp = datetime.now()
            print(f"Асинхронное изменение курса {self.currency} с {old_rate} на {new_rate} в {self.timestamp.strftime('%H:%M:%S')}")
            await self.notify_async(old_rate=old_rate, new_rate=new_rate, timestamp=self.timestamp)

class AsyncEmailNotifier(AsyncObserver):
    """Асинхронный наблюдатель для email-уведомлений"""
    def __init__(self, email: str):
        self.email = email
    
    async def update_async(self, subject, *args, **kwargs):
        # Имитация асинхронной операции отправки email
        await asyncio.sleep(0.1)
        if isinstance(subject, AsyncCurrencyRate):
            old_rate = kwargs.get('old_rate')
            new_rate = kwargs.get('new_rate')
            timestamp = kwargs.get('timestamp')
            print(f"ASYNC EMAIL NOTIFICATION для {self.email}: Курс {subject.currency} изменился с {old_rate} на {new_rate} в {timestamp.strftime('%H:%M:%S')}")

class AsyncSMSNotifier(AsyncObserver):
    """Асинхронный наблюдатель для SMS-уведомлений"""
    def __init__(self, phone: str):
        self.phone = phone
    
    async def update_async(self, subject, *args, **kwargs):
        # Имитация асинхронной операции отправки SMS
        await asyncio.sleep(0.05)
        if isinstance(subject, AsyncCurrencyRate):
            old_rate = kwargs.get('old_rate')
            new_rate = kwargs.get('new_rate')
            timestamp = kwargs.get('timestamp')
            print(f"ASYNC SMS NOTIFICATION для {self.phone}: Курс {subject.currency} изменился с {old_rate} на {new_rate} в {timestamp.strftime('%H:%M:%S')}")

# Решение задания 5: Практическое применение
class UserProfile(Subject):
    """Профиль пользователя как наблюдаемый объект"""
    def __init__(self, username: str):
        super().__init__()
        self.username = username
        self.status = ""
        self.friends_count = 0
        self.posts_count = 0
        self.last_action_time = datetime.now()
    
    def update_status(self, new_status: str):
        """Обновить статус пользователя"""
        old_status = self.status
        self.status = new_status
        self.last_action_time = datetime.now()
        print(f"{self.username} обновил статус: {new_status} в {self.last_action_time.strftime('%H:%M:%S')}")
        self.notify(
            event_type="status_update", 
            old_status=old_status, 
            new_status=new_status,
            timestamp=self.last_action_time
        )
    
    def add_friend(self):
        """Добавить друга"""
        old_count = self.friends_count
        self.friends_count += 1
        self.last_action_time = datetime.now()
        print(f"{self.username} теперь имеет {self.friends_count} друзей (было {old_count})")
        self.notify(
            event_type="friend_added", 
            old_count=old_count, 
            new_count=self.friends_count,
            timestamp=self.last_action_time
        )
    
    def create_post(self):
        """Создать пост"""
        old_posts_count = self.posts_count
        self.posts_count += 1
        self.last_action_time = datetime.now()
        print(f"{self.username} создал новый пост #{self.posts_count} (всего постов: {self.posts_count})")
        self.notify(
            event_type="post_created",
            post_number=self.posts_count,
            old_posts_count=old_posts_count,
            timestamp=self.last_action_time
        )

class FriendNotifier(Observer):
    """Наблюдатель для уведомления друзей"""
    def __init__(self, friend_name: str):
        self.friend_name = friend_name
    
    def update(self, subject, *args, **kwargs):
        if isinstance(subject, UserProfile):
            event_type = kwargs.get('event_type')
            timestamp = kwargs.get('timestamp')
            if event_type == "status_update":
                new_status = kwargs.get('new_status')
                print(f"[{timestamp.strftime('%H:%M:%S')}] {self.friend_name}: Ваш друг {subject.username} обновил статус: {new_status}")
            elif event_type == "friend_added":
                print(f"[{timestamp.strftime('%H:%M:%S')}] {self.friend_name}: {subject.username} добавил нового друга!")
            elif event_type == "post_created":
                post_number = kwargs.get('post_number')
                print(f"[{timestamp.strftime('%H:%M:%S')}] {self.friend_name}: {subject.username} создал новый пост #{post_number}")

class FeedUpdater(Observer):
    """Наблюдатель для обновления ленты"""
    def update(self, subject, *args, **kwargs):
        if isinstance(subject, UserProfile):
            event_type = kwargs.get('event_type')
            timestamp = kwargs.get('timestamp')
            if event_type == "status_update":
                new_status = kwargs.get('new_status')
                print(f"[{timestamp.strftime('%H:%M:%S')}] FEED: Новый статус от {subject.username}: {new_status}")
            elif event_type == "friend_added":
                print(f"[{timestamp.strftime('%H:%M:%S')}] FEED: {subject.username} добавил нового друга!")
            elif event_type == "post_created":
                post_number = kwargs.get('post_number')
                print(f"[{timestamp.strftime('%H:%M:%S')}] FEED: {subject.username} опубликовал пост #{post_number}")

class NotificationService(Observer):
    """Сервис уведомлений"""
    def __init__(self):
        self.notifications = []
    
    def update(self, subject, *args, **kwargs):
        if isinstance(subject, UserProfile):
            event_type = kwargs.get('event_type')
            timestamp = kwargs.get('timestamp')
            notification = {
                'user': subject.username,
                'event_type': event_type,
                'timestamp': timestamp,
                'details': kwargs
            }
            self.notifications.append(notification)
            print(f"[{timestamp.strftime('%H:%M:%S')}] NOTIFICATION SERVICE: Зарегистрировано событие {event_type} для пользователя {subject.username}")

# Дополнительные примеры использования Observer
class StockMarket(Subject):
    """Биржа как наблюдаемый объект"""
    def __init__(self):
        super().__init__()
        self.prices = {}
    
    def update_price(self, symbol: str, price: float):
        """Обновить цену акции"""
        old_price = self.prices.get(symbol)
        self.prices[symbol] = price
        print(f"Цена акции {symbol} обновлена: {old_price} -> {price}")
        self.notify(
            event_type="price_update",
            symbol=symbol,
            old_price=old_price,
            new_price=price
        )

class PriceAlert(Observer):
    """Система оповещения о ценах"""
    def __init__(self, symbol: str, threshold: float, alert_type: str = "above"):
        self.symbol = symbol
        self.threshold = threshold
        self.alert_type = alert_type  # "above" или "below"
    
    def update(self, subject, *args, **kwargs):
        if isinstance(subject, StockMarket):
            event_type = kwargs.get('event_type')
            if event_type == "price_update":
                symbol = kwargs.get('symbol')
                new_price = kwargs.get('new_price')
                if symbol == self.symbol:
                    if (self.alert_type == "above" and new_price > self.threshold) or \
                       (self.alert_type == "below" and new_price < self.threshold):
                        print(f"ALERT: Цена акции {symbol} пересекла порог {self.threshold}: {new_price}")

def demonstrate_observer_patterns():
    """Демонстрация различных паттернов Observer"""
    print("=== Демонстрация паттернов Observer ===")
    
    # Базовый Observer
    print("\n1. Базовая реализация Observer (CurrencyRate):")
    currency = CurrencyRate("USD", 75.5)
    
    email_notifier1 = EmailNotifier("user1@example.com")
    email_notifier2 = EmailNotifier("user2@example.com")
    sms_notifier = SMSNotifier("+79991234567")
    
    currency.attach(email_notifier1)
    currency.attach(email_notifier2)
    currency.attach(sms_notifier)
    
    currency.rate = 76.0
    time.sleep(0.1)  # Задержка для сортировки вывода
    
    # Отписываем одного наблюдателя
    currency.detach(email_notifier2)
    currency.rate = 75.8
    time.sleep(0.1)
    
    # EventManager
    print("\n2. EventManager с callback-функциями:")
    event_manager = EventManager()
    
    def log_event(event_type, data):
        print(f"ЛОГ: Событие '{event_type}' с данными: {data}")
    
    def send_alert(event_type, data):
        print(f"ТРЕВОГА: Произошло событие '{event_type}'!")
    
    event_manager.subscribe("warning", log_event)
    event_manager.subscribe("error", log_event)
    event_manager.subscribe("error", send_alert)
    
    event_manager.emit("warning", {"message": "Предупреждение"})
    event_manager.emit("error", {"message": "Ошибка", "code": 500})
    time.sleep(0.1)
    
    # Параметризованные уведомления
    print("\n3. Параметризованные уведомления (EventPublisher):")
    publisher = EventPublisher()
    
    subscriber1 = EventSubscriber("Subscriber1")
    subscriber2 = EventSubscriber("Subscriber2")
    
    publisher.subscribe("news", subscriber1.handle_event)
    publisher.subscribe("news", subscriber2.handle_event)
    publisher.subscribe("alerts", subscriber2.handle_event)
    
    publisher.publish("news", {"title": "Новость дня", "content": "Содержимое новости"})
    publisher.publish("alerts", {"priority": "high", "message": "Важное уведомление"})
    time.sleep(0.1)
    
    # Асинхронный Observer
    print("\n4. Асинхронный Observer:")
    async def async_demo():
        async_currency = AsyncCurrencyRate("EUR", 85.0)
        
        async_email1 = AsyncEmailNotifier("async_user1@example.com")
        async_email2 = AsyncEmailNotifier("async_user2@example.com")
        async_sms = AsyncSMSNotifier("+79997654321")
        
        await async_currency.attach_async(async_email1)
        await async_currency.attach_async(async_email2)
        await async_currency.attach_async(async_sms)
        
        await async_currency.rate.__set__(async_currency, 86.5)
    
    # Запускаем асинхронный пример
    asyncio.run(async_demo())
    time.sleep(0.1)
    
    # Практическое применение
    print("\n5. Практическое применение (Social Network):")
    user = UserProfile("Alex")
    
    friend1 = FriendNotifier("Bob")
    friend2 = FriendNotifier("Charlie")
    feed_updater = FeedUpdater()
    notification_service = NotificationService()
    
    user.attach(friend1)
    user.attach(friend2)
    user.attach(feed_updater)
    user.attach(notification_service)
    
    user.update_status("Впервые на этой платформе!")
    time.sleep(0.1)
    user.add_friend()
    time.sleep(0.1)
    user.update_status("Изучаю паттерн Observer")
    time.sleep(0.1)
    user.create_post()
    time.sleep(0.1)
    
    # Система оповещений о ценах
    print("\n6. Дополнительный пример - Система оповещений о ценах:")
    market = StockMarket()
    
    alert1 = PriceAlert("AAPL", 150, "above")
    alert2 = PriceAlert("GOOGL", 2500, "below")
    
    market.attach(alert1)
    market.attach(alert2)
    
    market.update_price("AAPL", 155)  # Выше порога
    market.update_price("AAPL", 145)  # Ниже порога
    market.update_price("GOOGL", 2400)  # Ниже порога
    market.update_price("MSFT", 300)   # Без алертов

def compare_observer_implementations():
    """Сравнение различных реализаций Observer"""
    print("\n=== Сравнение реализаций Observer ===")
    print("""
    1. Классический Observer:
       + Простая реализация и понимание
       + Хорошо подходит для синхронных систем
       + Четкое разделение ответственности
       - Может вызвать проблемы с производительностью при большом числе наблюдателей
       - Сложно управлять порядком уведомлений
       - Риск утечек памяти при неправильном управлении подписками
    
    2. EventManager с callback-функциями:
       + Гибкость в выборе обработчиков событий
       + Возможность подписки на разные типы событий
       + Простота добавления новых обработчиков
       - Менее строгая типизация
       - Сложнее отлаживать
       - Риск коллизий имен типов событий
    
    3. Параметризованные уведомления:
       + Возможность передачи данных о событии
       + Фильтрация по типам событий
       + Повышенная гибкость
       - Сложнее в реализации
       - Требует четкого контракта на передаваемые данные
    
    4. Асинхронный Observer:
       + Не блокирует выполнение основного потока
       + Подходит для систем с высокой нагрузкой
       + Возможность параллельной обработки уведомлений
       - Сложнее в отладке
       - Требует понимания асинхронного программирования
       - Возможны проблемы с синхронизацией
    
    5. Практическое применение:
       + Реальная ценность для бизнес-логики
       + Интеграция с реальными сценариями использования
       + Возможность комплексного тестирования
       - Требует больше времени на реализацию
       - Сложнее тестировать из-за зависимости от внешних факторов
    """)

# Примеры использования:
if __name__ == "__main__":
    print("=== Решения для практического занятия 15 ===")
    
    print("\n1. Решение задания 1: Базовая реализация Observer")
    currency = CurrencyRate("USD", 75.5)
    
    email_notifier1 = EmailNotifier("user1@example.com")
    email_notifier2 = EmailNotifier("user2@example.com")
    sms_notifier = SMSNotifier("+79991234567")
    
    currency.attach(email_notifier1)
    currency.attach(email_notifier2)
    currency.attach(sms_notifier)
    
    currency.rate = 76.0
    time.sleep(0.1)
    
    # Отписываем одного наблюдателя
    currency.detach(email_notifier2)
    currency.rate = 75.8
    time.sleep(0.1)
    
    print("\n2. Решение задания 2: Использование встроенных средств")
    event_manager = EventManager()
    
    def log_event(event_type, data):
        print(f"ЛОГ: Событие '{event_type}' с данными: {data}")
    
    def send_alert(event_type, data):
        print(f"ТРЕВОГА: Произошло событие '{event_type}'!")
    
    event_manager.subscribe("warning", log_event)
    event_manager.subscribe("error", log_event)
    event_manager.subscribe("error", send_alert)
    
    event_manager.emit("warning", {"message": "Предупреждение"})
    event_manager.emit("error", {"message": "Ошибка", "code": 500})
    time.sleep(0.1)
    
    print("\n3. Решение задания 3: Параметризованные уведомления")
    publisher = EventPublisher()
    
    subscriber1 = EventSubscriber("Subscriber1")
    subscriber2 = EventSubscriber("Subscriber2")
    
    publisher.subscribe("news", subscriber1.handle_event)
    publisher.subscribe("news", subscriber2.handle_event)
    publisher.subscribe("alerts", subscriber2.handle_event)
    
    publisher.publish("news", {"title": "Новость дня", "content": "Содержимое новости"})
    publisher.publish("alerts", {"priority": "high", "message": "Важное уведомление"})
    time.sleep(0.1)
    
    print("\n4. Решение задания 4: Асинхронный Observer")
    async def async_demo():
        async_currency = AsyncCurrencyRate("EUR", 85.0)
        
        async_email1 = AsyncEmailNotifier("async_user1@example.com")
        async_email2 = AsyncEmailNotifier("async_user2@example.com")
        async_sms = AsyncSMSNotifier("+79997654321")
        
        await async_currency.attach_async(async_email1)
        await async_currency.attach_async(async_email2)
        await async_currency.attach_async(async_sms)
        
        await async_currency.rate.__set__(async_currency, 86.5)
    
    # Запускаем асинхронный пример
    asyncio.run(async_demo())
    time.sleep(0.1)
    
    print("\n5. Решение задания 5: Практическое применение")
    user = UserProfile("Alex")
    
    friend1 = FriendNotifier("Bob")
    friend2 = FriendNotifier("Charlie")
    feed_updater = FeedUpdater()
    notification_service = NotificationService()
    
    user.attach(friend1)
    user.attach(friend2)
    user.attach(feed_updater)
    user.attach(notification_service)
    
    user.update_status("Впервые на этой платформе!")
    time.sleep(0.1)
    user.add_friend()
    time.sleep(0.1)
    user.update_status("Изучаю паттерн Observer")
    time.sleep(0.1)
    user.create_post()
    time.sleep(0.1)
    
    print("\n6. Дополнительные примеры")
    demonstrate_observer_patterns()
    compare_observer_implementations()