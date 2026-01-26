# Решения для практического занятия 13: ООП - паттерн Singleton

import threading
import time
from typing import Dict, Any
from concurrent.futures import ThreadPoolExecutor

# Решение задания 1: Базовая реализация Singleton
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

# Решение задания 2: Потокобезопасная реализация
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
            self._lock = threading.Lock()

    def log(self, message: str):
        """Добавление сообщения в лог"""
        with self._lock:
            self.logs.append(message)
        print(f"[LOG] {message}")

    def get_logs(self):
        """Получение всех логов"""
        with self._lock:
            return self.logs.copy()

    def clear_logs(self):
        """Очистка логов"""
        with self._lock:
            self.logs.clear()

# Решение задания 3: Реализация через метакласс
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
            self._lock = threading.Lock()

    def add_message(self, msg: str):
        """Добавление сообщения в лог"""
        with self._lock:
            self.messages.append(msg)

    def get_messages(self):
        """Получение всех сообщений"""
        with self._lock:
            return self.messages.copy()

    def clear_messages(self):
        """Очистка сообщений"""
        with self._lock:
            self.messages.clear()

# Решение задания 4: Декоратор Singleton
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
        self._lock = threading.Lock()

    def get(self, key: str, default: Any = None):
        """Получение значения конфигурации"""
        with self._lock:
            return self.config.get(key, default)

    def set(self, key: str, value: Any):
        """Установка значения конфигурации"""
        with self._lock:
            self.config[key] = value

    def update(self, new_config: Dict[str, Any]):
        """Обновление конфигурации"""
        with self._lock:
            self.config.update(new_config)

    def get_all_config(self):
        """Получение всей конфигурации"""
        with self._lock:
            return self.config.copy()

# Решение задания 5: Применение Singleton в реальном сценарии
@singleton
class NotificationManager:
    """Менеджер уведомлений как Singleton"""
    def __init__(self):
        self.notifications = []
        self.subscribers = []
        self._lock = threading.Lock()

    def subscribe(self, subscriber: str):
        """Подписка на уведомления"""
        with self._lock:
            if subscriber not in self.subscribers:
                self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber: str):
        """Отписка от уведомлений"""
        with self._lock:
            if subscriber in self.subscribers:
                self.subscribers.remove(subscriber)

    def send_notification(self, message: str, notification_type: str = "info"):
        """Отправка уведомления"""
        notification = {
            'message': message,
            'type': notification_type,
            'timestamp': __import__('datetime').datetime.now().isoformat()
        }
        
        with self._lock:
            self.notifications.append(notification)
            # Сохраняем копию подписчиков на момент отправки
            subscribers_copy = self.subscribers.copy()
        
        # Уведомляем всех подписчиков (вне блокировки для избежания блокировки)
        for subscriber in subscribers_copy:
            print(f"[{notification_type.upper()}] {subscriber}: {message}")
    
    def get_notifications(self):
        """Получение всех уведомлений"""
        with self._lock:
            return self.notifications.copy()
    
    def clear_notifications(self):
        """Очистка очереди уведомлений"""
        with self._lock:
            self.notifications.clear()

# Дополнительные примеры и тесты для демонстрации работы Singleton
def test_thread_safety():
    """Тестирование потокобезопасности Singleton"""
    print("\n=== Тестирование потокобезопасности ===")
    
    instances = []
    def create_instance():
        time.sleep(0.01)  # Задержка для увеличения вероятности гонки
        instance = Logger.getInstance()
        instances.append(id(instance))
    
    # Создаем 10 потоков, каждый из которых создает экземпляр Logger
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(create_instance) for _ in range(10)]
        for future in futures:
            future.result()
    
    # Проверяем, что все потоки получили один и тот же экземпляр
    unique_instances = set(instances)
    print(f"Количество уникальных экземпляров: {len(unique_instances)}")
    print(f"Все потоки получили один экземпляр: {len(unique_instances) == 1}")

def demonstrate_singleton_approaches():
    """Демонстрация различных подходов к реализации Singleton"""
    print("\n=== Демонстрация различных подходов к Singleton ===")
    
    # 1. Подход через __new__
    print("\n1. Подход через __new__ (DatabaseConnection):")
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    print(f"db1 is db2: {db1 is db2}")
    
    # 2. Подход через метакласс
    print("\n2. Подход через метакласс (LoggerWithMeta):")
    log_meta1 = LoggerWithMeta()
    log_meta2 = LoggerWithMeta()
    print(f"log_meta1 is log_meta2: {log_meta1 is log_meta2}")
    
    # 3. Подход через декоратор
    print("\n3. Подход через декоратор (ConfigurationManager):")
    config1 = ConfigurationManager()
    config2 = ConfigurationManager()
    print(f"config1 is config2: {config1 is config2}")
    
    # 4. Потокобезопасный подход
    print("\n4. Потокобезопасный подход (Logger):")
    logger1 = Logger.getInstance()
    logger2 = Logger.getInstance()
    print(f"logger1 is logger2: {logger1 is logger2}")

def demonstrate_real_world_usage():
    """Демонстрация реального использования Singleton"""
    print("\n=== Демонстрация реального использования ===")
    
    # Использование менеджера конфигурации
    print("\n1. Менеджер конфигурации:")
    config = ConfigurationManager()
    config.set('debug', True)
    config.set('max_users', 100)
    print(f"Значение debug: {config.get('debug')}")
    print(f"Значение max_users: {config.get('max_users')}")
    
    # Использование менеджера уведомлений
    print("\n2. Менеджер уведомлений:")
    notifier = NotificationManager()
    notifier.subscribe("User1")
    notifier.subscribe("User2")
    notifier.subscribe("ServiceMonitor")
    
    notifier.send_notification("Система запущена", "info")
    notifier.send_notification("Ошибка подключения к БД", "error")
    
    print(f"Всего уведомлений: {len(notifier.get_notifications())}")

def compare_singleton_implementations():
    """Сравнение различных реализаций Singleton"""
    print("\n=== Сравнение реализаций Singleton ===")
    print("""
    1. Через __new__:
       + Простая реализация
       - Не потокобезопасен (в базовой версии)
       - Может быть переопределен в подклассах
    
    2. Через метакласс:
       + Очень гибкий подход
       + Потокобезопасен
       + Работает со всеми подклассами
       - Более сложен в понимании
    
    3. Через декоратор:
       + Прост в использовании
       + Потокобезопасен
       - Менее очевиден при чтении кода
    
    4. Потокобезопасный через getInstance:
       + Явно показывает намерение использовать Singleton
       + Потокобезопасен
       - Требует вызова специального метода
    """)

# Примеры использования:
if __name__ == "__main__":
    print("=== Решения для практического занятия 13 ===")
    
    print("\n1. Решение задания 1: Базовая реализация Singleton")
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    print(f"db1 is db2: {db1 is db2}")
    db1.connect()
    db2.disconnect()

    print("\n2. Решение задания 2: Потокобезопасная реализация")
    logger1 = Logger.getInstance()
    logger2 = Logger.getInstance()
    print(f"logger1 is logger2: {logger1 is logger2}")
    logger1.log("Сообщение от первого логгера")
    logger2.log("Сообщение от второго логгера")
    print(f"Все логи: {logger1.get_logs()}")

    print("\n3. Решение задания 3: Реализация через метакласс")
    log1 = LoggerWithMeta()
    log2 = LoggerWithMeta()
    print(f"log1 is log2: {log1 is log2}")
    log1.add_message("Сообщение от первого экземпляра")
    log2.add_message("Сообщение от второго экземпляра")
    print(f"Все сообщения: {log1.get_messages()}")

    print("\n4. Решение задания 4: Декоратор Singleton")
    config1 = ConfigurationManager()
    config2 = ConfigurationManager()
    print(f"config1 is config2: {config1 is config2}")
    config1.set('debug', True)
    print(f"Значение debug в config2: {config2.get('debug')}")

    print("\n5. Решение задания 5: Применение Singleton в реальном сценарии")
    notifier1 = NotificationManager()
    notifier2 = NotificationManager()
    print(f"notifier1 is notifier2: {notifier1 is notifier2}")
    
    notifier1.subscribe("User1")
    notifier1.subscribe("User2")
    notifier2.send_notification("Новое сообщение", "info")
    print(f"Количество уведомлений: {len(notifier1.get_notifications())}")
    
    print("\n6. Дополнительные примеры")
    demonstrate_singleton_approaches()
    test_thread_safety()
    demonstrate_real_world_usage()
    compare_singleton_implementations()