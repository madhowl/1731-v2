# Упражнения для практического занятия 15: ООП - паттерн Observer

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Callable
import asyncio
import time

# Задание 1: Базовая реализация Observer
class Observer(ABC):
    """Интерфейс наблюдателя"""
    @abstractmethod
    def update(self, subject, *args, **kwargs):
        pass

class Subject(ABC):
    """Интерфейс наблюдаемого объекта"""
    def __init__(self):
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer):
        """Добавить наблюдателя"""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: Observer):
        """Удалить наблюдателя"""
        if observer in self._observers:
            self._observers.remove(observer)
    
    def notify(self, *args, **kwargs):
        """Уведомить всех наблюдателей"""
        for observer in self._observers:
            observer.update(self, *args, **kwargs)

class CurrencyRate(Subject):
    """Класс курса валюты как наблюдаемый объект"""
    def __init__(self, currency: str, rate: float):
        super().__init__()
        self.currency = currency
        self.rate = rate
    
    def set_rate(self, new_rate: float):
        """Установить новый курс"""
        old_rate = self.rate
        self.rate = new_rate
        print(f"Курс {self.currency} изменился с {old_rate} на {new_rate}")
        self.notify(old_rate=old_rate, new_rate=new_rate)

class EmailNotifier(Observer):
    """Наблюдатель для отправки email-уведомлений"""
    def __init__(self, email: str):
        self.email = email
    
    def update(self, subject, *args, **kwargs):
        if isinstance(subject, CurrencyRate):
            old_rate = kwargs.get('old_rate')
            new_rate = kwargs.get('new_rate')
            print(f"EMAIL NOTIFICATION для {self.email}: Курс {subject.currency} изменился с {old_rate} на {new_rate}")

class SMSNotifier(Observer):
    """Наблюдатель для отправки SMS-уведомлений"""
    def __init__(self, phone: str):
        self.phone = phone
    
    def update(self, subject, *args, **kwargs):
        if isinstance(subject, CurrencyRate):
            old_rate = kwargs.get('old_rate')
            new_rate = kwargs.get('new_rate')
            print(f"SMS NOTIFICATION для {self.phone}: Курс {subject.currency} изменился с {old_rate} на {new_rate}")

# Задание 2: Использование встроенных средств
class EventManager:
    """Менеджер событий с использованием callback-функций"""
    def __init__(self):
        self._callbacks: Dict[str, List[Callable]] = {}
    
    def subscribe(self, event_type: str, callback: Callable):
        """Подписаться на событие"""
        if event_type not in self._callbacks:
            self._callbacks[event_type] = []
        if callback not in self._callbacks[event_type]:
            self._callbacks[event_type].append(callback)
    
    def unsubscribe(self, event_type: str, callback: Callable):
        """Отписаться от события"""
        if event_type in self._callbacks and callback in self._callbacks[event_type]:
            self._callbacks[event_type].remove(callback)
    
    def emit(self, event_type: str, data: Any = None):
        """Вызвать все callback-функции для типа события"""
        if event_type in self._callbacks:
            for callback in self._callbacks[event_type]:
                callback(event_type, data)

# Задание 3: Параметризованные уведомления
class EventPublisher:
    """Издатель событий с фильтрацией по типам"""
    def __init__(self):
        self._subscribers: Dict[str, List[Callable]] = {}
    
    def subscribe(self, event_type: str, handler: Callable):
        """Подписаться на определенный тип события"""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        if handler not in self._subscribers[event_type]:
            self._subscribers[event_type].append(handler)
    
    def unsubscribe(self, event_type: str, handler: Callable):
        """Отписаться от определенного типа события"""
        if event_type in self._subscribers and handler in self._subscribers[event_type]:
            self._subscribers[event_type].remove(handler)
    
    def publish(self, event_type: str, event_data: Dict[str, Any]):
        """Опубликовать событие с данными"""
        if event_type in self._subscribers:
            for handler in self._subscribers[event_type]:
                handler(event_type, event_data)

class EventSubscriber:
    """Подписчик на события"""
    def __init__(self, name: str):
        self.name = name
    
    def handle_event(self, event_type: str, event_data: Dict[str, Any]):
        """Обработать событие"""
        print(f"{self.name} получил событие '{event_type}': {event_data}")

# Задание 4: Асинхронный Observer
class AsyncObserver(ABC):
    """Асинхронный интерфейс наблюдателя"""
    @abstractmethod
    async def update_async(self, subject, *args, **kwargs):
        pass

class AsyncSubject(ABC):
    """Асинхронный наблюдаемый объект"""
    def __init__(self):
        self._async_observers: List[AsyncObserver] = []
    
    def attach_async(self, observer: AsyncObserver):
        """Добавить асинхронного наблюдателя"""
        if observer not in self._async_observers:
            self._async_observers.append(observer)
    
    def detach_async(self, observer: AsyncObserver):
        """Удалить асинхронного наблюдателя"""
        if observer in self._async_observers:
            self._async_observers.remove(observer)
    
    async def notify_async(self, *args, **kwargs):
        """Асинхронно уведомить всех наблюдателей"""
        tasks = []
        for observer in self._async_observers:
            task = asyncio.create_task(observer.update_async(self, *args, **kwargs))
            tasks.append(task)
        
        if tasks:
            await asyncio.gather(*tasks)

class AsyncCurrencyRate(AsyncSubject):
    """Асинхронный класс курса валюты"""
    def __init__(self, currency: str, rate: float):
        super().__init__()
        self.currency = currency
        self.rate = rate
    
    async def set_rate(self, new_rate: float):
        """Асинхронно установить новый курс"""
        old_rate = self.rate
        self.rate = new_rate
        print(f"Асинхронное изменение курса {self.currency} с {old_rate} на {new_rate}")
        await self.notify_async(old_rate=old_rate, new_rate=new_rate)

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
            print(f"ASYNC EMAIL NOTIFICATION для {self.email}: Курс {subject.currency} изменился с {old_rate} на {new_rate}")

# Задание 5: Практическое применение
class UserProfile(Subject):
    """Профиль пользователя как наблюдаемый объект"""
    def __init__(self, username: str):
        super().__init__()
        self.username = username
        self.status = ""
        self.friends_count = 0
    
    def update_status(self, new_status: str):
        """Обновить статус пользователя"""
        old_status = self.status
        self.status = new_status
        print(f"{self.username} обновил статус: {new_status}")
        self.notify(event_type="status_update", old_status=old_status, new_status=new_status)
    
    def add_friend(self):
        """Добавить друга"""
        old_count = self.friends_count
        self.friends_count += 1
        print(f"{self.username} теперь имеет {self.friends_count} друзей")
        self.notify(event_type="friend_added", old_count=old_count, new_count=self.friends_count)

class FriendNotifier(Observer):
    """Наблюдатель для уведомления друзей"""
    def __init__(self, friend_name: str):
        self.friend_name = friend_name
    
    def update(self, subject, *args, **kwargs):
        if isinstance(subject, UserProfile):
            event_type = kwargs.get('event_type')
            if event_type == "status_update":
                new_status = kwargs.get('new_status')
                print(f"{self.friend_name}: Ваш друг {subject.username} обновил статус: {new_status}")
            elif event_type == "friend_added":
                print(f"{self.friend_name}: {subject.username} добавил нового друга!")

class FeedUpdater(Observer):
    """Наблюдатель для обновления ленты"""
    def update(self, subject, *args, **kwargs):
        if isinstance(subject, UserProfile):
            event_type = kwargs.get('event_type')
            if event_type == "status_update":
                new_status = kwargs.get('new_status')
                print(f"FEED: Новый статус от {subject.username}: {new_status}")
            elif event_type == "friend_added":
                print(f"FEED: {subject.username} добавил нового друга!")

# Примеры использования:
if __name__ == "__main__":
    print("=== Задание 1: Базовая реализация Observer ===")
    currency = CurrencyRate("USD", 75.5)
    
    email_notifier1 = EmailNotifier("user1@example.com")
    email_notifier2 = EmailNotifier("user2@example.com")
    sms_notifier = SMSNotifier("+79991234567")
    
    currency.attach(email_notifier1)
    currency.attach(email_notifier2)
    currency.attach(sms_notifier)
    
    currency.set_rate(76.0)
    print()
    
    # Отписываем одного наблюдателя
    currency.detach(email_notifier2)
    currency.set_rate(75.8)
    print()
    
    print("=== Задание 2: Использование встроенных средств ===")
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
    print()
    
    print("=== Задание 3: Параметризованные уведомления ===")
    publisher = EventPublisher()
    
    subscriber1 = EventSubscriber("Subscriber1")
    subscriber2 = EventSubscriber("Subscriber2")
    
    publisher.subscribe("news", subscriber1.handle_event)
    publisher.subscribe("news", subscriber2.handle_event)
    publisher.subscribe("alerts", subscriber2.handle_event)
    
    publisher.publish("news", {"title": "Новость дня", "content": "Содержимое новости"})
    publisher.publish("alerts", {"priority": "high", "message": "Важное уведомление"})
    print()
    
    print("=== Задание 4: Асинхронный Observer ===")
    async def async_demo():
        async_currency = AsyncCurrencyRate("EUR", 85.0)
        
        async_email1 = AsyncEmailNotifier("async_user1@example.com")
        async_email2 = AsyncEmailNotifier("async_user2@example.com")
        
        async_currency.attach_async(async_email1)
        async_currency.attach_async(async_email2)
        
        await async_currency.set_rate(86.5)
    
    # Запускаем асинхронный пример
    asyncio.run(async_demo())
    print()
    
    print("=== Задание 5: Практическое применение ===")
    user = UserProfile("Alex")
    
    friend1 = FriendNotifier("Bob")
    friend2 = FriendNotifier("Charlie")
    feed_updater = FeedUpdater()
    
    user.attach(friend1)
    user.attach(friend2)
    user.attach(feed_updater)
    
    user.update_status("Впервые на этой платформе!")
    user.add_friend()
    user.update_status("Изучаю паттерн Observer")