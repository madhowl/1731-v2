# Упражнения для практического занятия 13: ООП - паттерн Singleton

import threading
from typing import Dict, Any

# Задание 1: Базовая реализация Singleton
class DatabaseConnection:
    """Класс для подключения к базе данных как Singleton"""
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        # Защита от повторной инициализации
        if not self._initialized:
            self.connection_string = "sqlite:///example.db"
            self.connected = False
            self._initialized = True

    def connect(self):
        """Имитация подключения к базе данных"""
        if not self.connected:
            print(f"Подключение к базе данных: {self.connection_string}")
            self.connected = True
        else:
            print("Уже подключено к базе данных")

    def disconnect(self):
        """Отключение от базы данных"""
        if self.connected:
            print("Отключение от базы данных")
            self.connected = False
        else:
            print("Нет активного подключения")

# Задание 2: Потокобезопасная реализация
class ThreadSafeSingleton:
    """Потокобезопасная реализация Singleton"""
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                # Двойная проверка для оптимизации
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    @classmethod
    def getInstance(cls):
        """Метод для получения экземпляра класса"""
        return cls()

class Logger(ThreadSafeSingleton):
    """Класс логгера как потокобезопасный Singleton"""
    def __init__(self):
        if not hasattr(self, 'logs'):
            self.logs = []

    def log(self, message: str):
        """Добавление сообщения в лог"""
        self.logs.append(message)
        print(f"[LOG] {message}")

    def get_logs(self):
        """Получение всех логов"""
        return self.logs.copy()

# Задание 3: Реализация через метакласс
class SingletonMeta(type):
    """Метакласс для реализации Singleton"""
    _instances = {}
    _lock = threading.Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                if cls not in cls._instances:
                    instance = super().__call__(*args, **kwargs)
                    cls._instances[cls] = instance
        return cls._instances[cls]

class LoggerWithMeta(metaclass=SingletonMeta):
    """Класс логгера с использованием метакласса"""
    def __init__(self):
        if not hasattr(self, 'messages'):
            self.messages = []

    def add_message(self, msg: str):
        """Добавление сообщения в лог"""
        self.messages.append(msg)

    def get_messages(self):
        """Получение всех сообщений"""
        return self.messages.copy()

# Задание 4: Декоратор Singleton
def singleton(cls):
    """Декоратор для превращения класса в Singleton"""
    instances = {}
    lock = threading.Lock()

    def get_instance(*args, **kwargs):
        if cls not in instances:
            with lock:
                if cls not in instances:
                    instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance

@singleton
class ConfigurationManager:
    """Класс управления конфигурацией как Singleton"""
    def __init__(self):
        self.config = {
            'debug': False,
            'database_url': 'sqlite:///default.db',
            'max_connections': 10
        }

    def get(self, key: str, default: Any = None):
        """Получение значения конфигурации"""
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        """Установка значения конфигурации"""
        self.config[key] = value

    def update(self, new_config: Dict[str, Any]):
        """Обновление конфигурации"""
        self.config.update(new_config)

# Задание 5: Применение Singleton в реальном сценарии
@singleton
class NotificationManager:
    """Менеджер уведомлений как Singleton"""
    def __init__(self):
        self.notifications = []
        self.subscribers = []

    def subscribe(self, subscriber: str):
        """Подписка на уведомления"""
        if subscriber not in self.subscribers:
            self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber: str):
        """Отписка от уведомлений"""
        if subscriber in self.subscribers:
            self.subscribers.remove(subscriber)

    def send_notification(self, message: str, notification_type: str = "info"):
        """Отправка уведомления"""
        notification = {
            'message': message,
            'type': notification_type,
            'timestamp': __import__('datetime').datetime.now().isoformat()
        }
        self.notifications.append(notification)
        
        # Уведомляем всех подписчиков
        for subscriber in self.subscribers:
            print(f"[{notification_type.upper()}] {subscriber}: {message}")
    
    def get_notifications(self):
        """Получение всех уведомлений"""
        return self.notifications.copy()
    
    def clear_notifications(self):
        """Очистка очереди уведомлений"""
        self.notifications.clear()

# Примеры использования:
if __name__ == "__main__":
    print("=== Задание 1: Базовая реализация Singleton ===")
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    print(f"db1 is db2: {db1 is db2}")
    db1.connect()
    db2.disconnect()

    print("\n=== Задание 2: Потокобезопасная реализация ===")
    logger1 = Logger.getInstance()
    logger2 = Logger.getInstance()
    print(f"logger1 is logger2: {logger1 is logger2}")
    logger1.log("Сообщение от первого логгера")
    logger2.log("Сообщение от второго логгера")
    print(f"Все логи: {logger1.get_logs()}")

    print("\n=== Задание 3: Реализация через метакласс ===")
    log1 = LoggerWithMeta()
    log2 = LoggerWithMeta()
    print(f"log1 is log2: {log1 is log2}")
    log1.add_message("Сообщение от первого экземпляра")
    log2.add_message("Сообщение от второго экземпляра")
    print(f"Все сообщения: {log1.get_messages()}")

    print("\n=== Задание 4: Декоратор Singleton ===")
    config1 = ConfigurationManager()
    config2 = ConfigurationManager()
    print(f"config1 is config2: {config1 is config2}")
    config1.set('debug', True)
    print(f"Значение debug в config2: {config2.get('debug')}")

    print("\n=== Задание 5: Применение Singleton в реальном сценарии ===")
    notifier1 = NotificationManager()
    notifier2 = NotificationManager()
    print(f"notifier1 is notifier2: {notifier1 is notifier2}")
    
    notifier1.subscribe("User1")
    notifier1.subscribe("User2")
    notifier2.send_notification("Новое сообщение", "info")
    print(f"Количество уведомлений: {len(notifier1.get_notifications())}")