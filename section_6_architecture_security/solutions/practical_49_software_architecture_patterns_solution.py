#!/usr/bin/env python3
"""
Практическое занятие 49: Паттерны программной архитектуры
Решение упражнений
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import uuid
import json
from datetime import datetime


# ==============================================================================
# УПРАЖНЕНИЕ 1: Порождающие паттерны
# ==============================================================================

# 1.1 Реализация Фабричного метода (Factory Method)
print("=" * 60)
print("Упражнение 1.1: Фабричный метод")
print("=" * 60)


class Notification(ABC):
    """Абстрактный класс уведомления"""
    @abstractmethod
    def send(self, message: str) -> Dict[str, Any]:
        pass


class EmailNotification(Notification):
    """Уведомление по email"""
    def send(self, message: str) -> Dict[str, Any]:
        return {
            'type': 'email',
            'status': 'sent',
            'message': f"Email отправлен: {message}"
        }


class SMSNotification(Notification):
    """SMS уведомление"""
    def send(self, message: str) -> Dict[str, Any]:
        return {
            'type': 'sms',
            'status': 'sent',
            'message': f"SMS отправлено: {message}"
        }


class PushNotification(Notification):
    """Push-уведомление"""
    def send(self, message: str) -> Dict[str, Any]:
        return {
            'type': 'push',
            'status': 'sent',
            'message': f"Push-уведомление отправлено: {message}"
        }


class NotificationCreator(ABC):
    """Абстрактный создатель уведомлений"""
    @abstractmethod
    def factory_method(self) -> Notification:
        pass
    
    def send_notification(self, message: str) -> Dict[str, Any]:
        notification = self.factory_method()
        return notification.send(message)


class EmailNotificationCreator(NotificationCreator):
    """Создатель email уведомлений"""
    def factory_method(self) -> Notification:
        return EmailNotification()


class SMSNotificationCreator(NotificationCreator):
    """Создатель SMS уведомлений"""
    def factory_method(self) -> Notification:
        return SMSNotification()


class PushNotificationCreator(NotificationCreator):
    """Создатель push уведомлений"""
    def factory_method(self) -> Notification:
        return PushNotification()


# Тестирование
email_creator = EmailNotificationCreator()
sms_creator = SMSNotificationCreator()
push_creator = PushNotificationCreator()

print(email_creator.send_notification("Привет!"))
print(sms_creator.send_notification("Код подтверждения: 1234"))
print(push_creator.send_notification("Новое сообщение"))


# 1.2 Реализация Абстрактной фабрики (Abstract Factory)
print("\n" + "=" * 60)
print("Упражнение 1.2: Абстрактная фабрика")
print("=" * 60)


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
        return "<button class='light-theme'>Кнопка</button>"


class LightInput(Input):
    def render(self) -> str:
        return "<input class='light-theme'>"


# Семейство продуктов: Dark Theme
class DarkButton(Button):
    def render(self) -> str:
        return "<button class='dark-theme'>Кнопка</button>"


class DarkInput(Input):
    def render(self) -> str:
        return "<input class='dark-theme'>"


class UIFactory(ABC):
    """Абстрактная фабрика UI компонентов"""
    @abstractmethod
    def create_button(self) -> Button:
        pass
    
    @abstractmethod
    def create_input(self) -> Input:
        pass


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


def create_ui(factory: UIFactory) -> Dict[str, str]:
    """Создание UI с использованием фабрики"""
    return {
        'button': factory.create_button().render(),
        'input': factory.create_input().render()
    }


# Тестирование
print("Light Theme:")
ui_light = create_ui(LightThemeFactory())
print(f"  Button: {ui_light['button']}")
print(f"  Input: {ui_light['input']}")

print("\nDark Theme:")
ui_dark = create_ui(DarkThemeFactory())
print(f"  Button: {ui_dark['button']}")
print(f"  Input: {ui_dark['input']}")


# 1.3 Реализация Одиночки (Singleton)
print("\n" + "=" * 60)
print("Упражнение 1.3: Паттерн Одиночка")
print("=" * 60)


class DatabaseConnection:
    """Паттерн Одиночка для подключения к БД"""
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._connection = None
            cls._instance._connected = False
        return cls._instance
    
    def connect(self, connection_string: str) -> bool:
        if not self._connected:
            print(f"Подключение к: {connection_string}")
            self._connection = connection_string
            self._connected = True
            return True
        print("Уже подключено")
        return False
    
    def get_connection(self) -> Optional[str]:
        return self._connection
    
    def close(self):
        print("Закрытие соединения")
        self._connection = None
        self._connected = False


# Тестирование
db1 = DatabaseConnection()
db1.connect("postgresql://localhost/mydb")

db2 = DatabaseConnection()
db2.connect("mysql://localhost/otherdb")

print(f"db1 is db2: {db1 is db2}")
print(f"Соединение: {db1.get_connection()}")


# ==============================================================================
# УПРАЖНЕНИЕ 2: Структурные паттерны
# ==============================================================================

# 2.1 Реализация Адаптера (Adapter)
print("\n" + "=" * 60)
print("Упражнение 2.1: Паттерн Адаптер")
print("=" * 60)


class OldPaymentSystem:
    """Старый платёжный API"""
    def process_payment(self, amount: float) -> str:
        return f"Обработка платежа {amount} через старый API"
    
    def refund(self, transaction_id: str) -> str:
        return f"Возврат по транзакции {transaction_id}"


class PaymentProcessor(ABC):
    """Целевой интерфейс"""
    @abstractmethod
    def pay(self, amount: float) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def refund_payment(self, transaction_id: str) -> Dict[str, Any]:
        pass


class PaymentAdapter(PaymentProcessor):
    """Адаптер для старой системы"""
    def __init__(self):
        self.old_system = OldPaymentSystem()
    
    def pay(self, amount: float) -> Dict[str, Any]:
        result = self.old_system.process_payment(amount)
        return {
            'status': 'success',
            'message': result,
            'amount': amount,
            'timestamp': datetime.now().isoformat()
        }
    
    def refund_payment(self, transaction_id: str) -> Dict[str, Any]:
        result = self.old_system.refund(transaction_id)
        return {
            'status': 'success',
            'message': result,
            'transaction_id': transaction_id
        }


# Тестирование
adapter = PaymentAdapter()
print(adapter.pay(100.50))
print(adapter.refund_payment("TXN12345"))


# 2.2 Реализация Декоратора (Decorator)
print("\n" + "=" * 60)
print("Упражнение 2.2: Паттерн Декоратор")
print("=" * 60)


class Coffee(ABC):
    """Базовый компонент"""
    @abstractmethod
    def get_cost(self) -> float:
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        pass


class SimpleCoffee(Coffee):
    """Простой кофе"""
    def get_cost(self) -> float:
        return 100.0
    
    def get_description(self) -> str:
        return "Кофе"


class CoffeeDecorator(Coffee):
    """Базовый декоратор"""
    def __init__(self, coffee: Coffee):
        self._coffee = coffee
    
    def get_cost(self) -> float:
        return self._coffee.get_cost()
    
    def get_description(self) -> str:
        return self._coffee.get_description()


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


# Тестирование
coffee = SimpleCoffee()
print(f"{coffee.get_description()} = {coffee.get_cost()}")

coffee_with_milk = MilkDecorator(coffee)
print(f"{coffee_with_milk.get_description()} = {coffee_with_milk.get_cost()}")

coffee_deluxe = MilkDecorator(SugarDecorator(WhipDecorator(SimpleCoffee())))
print(f"{coffee_deluxe.get_description()} = {coffee_deluxe.get_cost()}")


# 2.3 Реализация Фасада (Facade)
print("\n" + "=" * 60)
print("Упражнение 2.3: Паттерн Фасад")
print("=" * 60)


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
    def decode(self) -> str:
        return "Декодирование MP4"


class AVICodec:
    def decode(self) -> str:
        return "Декодирование AVI"


class AudioMixer:
    def fix(self) -> str:
        return "Исправление звука"


class VideoConverter:
    """Фасад для конвертации видео"""
    def convert(self, filename: str, format: str) -> str:
        file = VideoFile(filename)
        codec = CodecFactory.extract(file)
        
        if codec:
            data = codec.decode()
        
        audio = AudioMixer().fix()
        
        return f"Конвертирование {filename} в {format} завершено"


# Тестирование
converter = VideoConverter()
result = converter.convert("video.avi", "mp4")
print(result)


# ==============================================================================
# УПРАЖНЕНИЕ 3: Поведенческие паттерны
# ==============================================================================

# 3.1 Реализация Наблюдателя (Observer)
print("\n" + "=" * 60)
print("Упражнение 3.1: Паттерн Наблюдатель")
print("=" * 60)


class Observer(ABC):
    """Абстрактный наблюдатель"""
    @abstractmethod
    def update(self, message: str) -> None:
        pass


class Subject:
    """Издатель"""
    def __init__(self):
        self._observers: List[Observer] = []
    
    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)
    
    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)
    
    def notify(self, message: str) -> None:
        for observer in self._observers:
            observer.update(message)


class NewsAgency(Subject):
    """Новостное агентство"""
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


# Тестирование
agency = NewsAgency()

channel1 = NewsChannel("Первый канал")
channel2 = NewsChannel("НТВ")
subscriber = Subscriber("Иван")

agency.attach(channel1)
agency.attach(channel2)
agency.attach(subscriber)

agency.latest_news = "Python 4.0 вышел!"

agency.detach(channel2)
agency.latest_news = "Изменения в языке Python"


# 3.2 Реализация Стратегии (Strategy)
print("\n" + "=" * 60)
print("Упражнение 3.2: Паттерн Стратегия")
print("=" * 60)


class PaymentStrategy(ABC):
    """Абстрактная стратегия оплаты"""
    @abstractmethod
    def pay(self, amount: float) -> Dict[str, Any]:
        pass


class CreditCardPayment(PaymentStrategy):
    def __init__(self, card_number: str):
        self.card_number = card_number
    
    def pay(self, amount: float) -> Dict[str, Any]:
        return {
            'method': 'credit_card',
            'card': self.card_number[-4:],
            'amount': amount,
            'status': 'success'
        }


class PayPalPayment(PaymentStrategy):
    def __init__(self, email: str):
        self.email = email
    
    def pay(self, amount: float) -> Dict[str, Any]:
        return {
            'method': 'paypal',
            'email': self.email,
            'amount': amount,
            'status': 'success'
        }


class CryptoPayment(PaymentStrategy):
    def __init__(self, wallet: str):
        self.wallet = wallet
    
    def pay(self, amount: float) -> Dict[str, Any]:
        return {
            'method': 'crypto',
            'wallet': self.wallet[:8] + '...',
            'amount': amount,
            'status': 'success'
        }


class ShoppingCart:
    """Корзина покупок"""
    def __init__(self):
        self.items: List[Dict[str, Any]] = []
        self.payment_strategy: Optional[PaymentStrategy] = None
    
    def add_item(self, name: str, price: float, quantity: int = 1):
        self.items.append({
            'name': name,
            'price': price,
            'quantity': quantity
        })
    
    def set_payment_strategy(self, strategy: PaymentStrategy):
        self.payment_strategy = strategy
    
    def checkout(self) -> Dict[str, Any]:
        total = sum(item['price'] * item['quantity'] for item in self.items)
        
        if not self.payment_strategy:
            return {'error': 'Не выбран способ оплаты'}
        
        result = self.payment_strategy.pay(total)
        result['items'] = self.items
        return result


# Тестирование
cart = ShoppingCart()
cart.add_item("Ноутбук", 50000, 1)
cart.add_item("Мышь", 1500, 2)

print("Оплата картой:")
cart.set_payment_strategy(CreditCardPayment("4111111111111111"))
print(cart.checkout())

print("\nОплата PayPal:")
cart.set_payment_strategy(PayPalPayment("user@example.com"))
print(cart.checkout())

print("\nОплата криптовалютой:")
cart.set_payment_strategy(CryptoPayment("0x742d35Cc6634C0532925a3b844Bc9e7595f"))
print(cart.checkout())


# ==============================================================================
# УПРАЖНЕНИЕ 4: Выбор архитектуры для проекта
# ==============================================================================

print("\n" + "=" * 60)
print("Упражнение 4: Выбор архитектуры")
print("=" * 60)


class ArchitectureEvaluator:
    """Оценщик архитектуры для проекта"""
    
    @staticmethod
    def recommend_architecture(project_type: str, scale: str, team_size: int) -> Dict[str, Any]:
        """Рекомендация архитектуры на основе параметров проекта"""
        
        recommendations = []
        
        # Критерии для монолита
        if team_size <= 5 and scale in ['small', 'medium']:
            recommendations.append({
                'architecture': 'Monolithic',
                'reason': 'Небольшая команда, простой проект',
                'pros': ['Простота разработки', 'Легкое развёртывание', 'Простое тестирование'],
                'cons': ['Сложность масштабирования', 'Тесная связанность']
            })
        
        # Критерии для микросервисов
        if team_size > 10 or scale == 'large':
            recommendations.append({
                'architecture': 'Microservices',
                'reason': 'Большая команда, высокая нагрузка',
                'pros': ['Независимое масштабирование', 'Технологическая гибкость', 'Устойчивость к ошибкам'],
                'cons': ['Сложность управления', 'Сетевая задержка']
            })
        
        # Критерии для MVC
        if project_type in ['web_app', 'e-commerce']:
            recommendations.append({
                'architecture': 'MVC',
                'reason': 'Веб-приложение с UI',
                'pros': ['Разделение логики и представления', 'Поддержка', 'Расширяемость'],
                'cons': ['Сложность для больших приложений']
            })
        
        return {
            'project_type': project_type,
            'scale': scale,
            'team_size': team_size,
            'recommendations': recommendations
        }


# Тестирование
result1 = ArchitectureEvaluator.recommend_architecture('web_app', 'small', 3)
print(f"Проект: {result1['project_type']}, Масштаб: {result1['scale']}, Команда: {result1['team_size']}")
for rec in result1['recommendations']:
    print(f"  Рекомендуемая архитектура: {rec['architecture']}")
    print(f"  Причина: {rec['reason']}")

result2 = ArchitectureEvaluator.recommend_architecture('api', 'large', 20)
print(f"\nПроект: {result2['project_type']}, Масштаб: {result2['scale']}, Команда: {result2['team_size']}")
for rec in result2['recommendations']:
    print(f"  Рекомендуемая архитектура: {rec['architecture']}")
    print(f"  Причина: {rec['reason']}")

print("\n" + "=" * 60)
print("Все упражнения выполнены!")
print("=" * 60)
