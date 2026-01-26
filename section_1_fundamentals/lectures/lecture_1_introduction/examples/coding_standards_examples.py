# Примеры стандартов кодирования Python

"""
Этот файл демонстрирует стандарты кодирования Python (PEP 8)
и лучшие практики оформления кода.
"""

# 1. Импорты
# Правильный порядок импортов:
# 1. Стандартная библиотека
# 2. Сторонние библиотеки
# 3. Локальные импорты

import os
import sys
import json
from datetime import datetime
from typing import List, Dict, Optional, Union

import requests
import numpy as np
import pandas as pd

# from my_local_module import my_function


# 2. Именование переменных и функций (snake_case)
def calculate_user_age(birth_date: str) -> int:
    """
    Вычисляет возраст пользователя по дате рождения.
    
    Args:
        birth_date: Дата рождения в формате 'YYYY-MM-DD'
        
    Returns:
        Возраст пользователя в годах
    """
    birth = datetime.strptime(birth_date, "%Y-%m-%d")
    today = datetime.now()
    
    age = today.year - birth.year
    
    # Проверяем, был ли день рождения в текущем году
    if today.month < birth.month or (today.month == birth.month and today.day < birth.day):
        age -= 1
    
    return age


# 3. Именование классов (CamelCase)
class UserManager:
    """
    Класс для управления пользователями
    """
    
    def __init__(self, storage_path: str = "users.json"):
        """
        Инициализация менеджера пользователей
        
        Args:
            storage_path: Путь к файлу хранения данных пользователей
        """
        self.storage_path = storage_path
        self.users: List[Dict[str, Union[str, int]]] = []
        self._load_users()
    
    def _load_users(self) -> None:
        """
        Загрузка пользователей из файла
        """
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    self.users = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                self.users = []
    
    def save_users(self) -> None:
        """
        Сохранение пользователей в файл
        """
        with open(self.storage_path, 'w', encoding='utf-8') as f:
            json.dump(self.users, f, ensure_ascii=False, indent=2)
    
    def add_user(self, 
                 name: str, 
                 birth_date: str, 
                 email: Optional[str] = None) -> Dict[str, Union[str, int]]:
        """
        Добавление нового пользователя
        
        Args:
            name: Имя пользователя
            birth_date: Дата рождения в формате 'YYYY-MM-DD'
            email: Email пользователя (опционально)
            
        Returns:
            Словарь с информацией о пользователе
        """
        # Валидация данных
        if not name or not name.strip():
            raise ValueError("Имя пользователя не может быть пустым")
        
        # Проверка формата даты
        try:
            datetime.strptime(birth_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Неверный формат даты рождения. Ожидается YYYY-MM-DD")
        
        # Создание пользователя
        user = {
            "id": len(self.users) + 1,
            "name": name.strip(),
            "birth_date": birth_date,
            "email": email,
            "age": calculate_user_age(birth_date),
            "created_at": datetime.now().isoformat()
        }
        
        self.users.append(user)
        self.save_users()
        
        return user
    
    def find_users_by_age_range(self, 
                                min_age: int, 
                                max_age: int) -> List[Dict[str, Union[str, int]]]:
        """
        Поиск пользователей в заданном диапазоне возраста
        
        Args:
            min_age: Минимальный возраст
            max_age: Максимальный возраст
            
        Returns:
            Список пользователей в заданном диапазоне возраста
        """
        return [
            user for user in self.users
            if min_age <= user.get("age", 0) <= max_age
        ]


# 4. Использование констант
DATABASE_HOST = "localhost"
DATABASE_PORT = 5432
DEFAULT_TIMEOUT = 30
MAX_CONNECTIONS = 100

# 5. Пример документации функции с более сложной аннотацией
def process_user_data(users: List[Dict[str, str]], 
                     operation: str = "uppercase") -> List[Dict[str, str]]:
    """
    Обработка данных пользователей в зависимости от операции
    
    Args:
        users: Список словарей с данными пользователей
        operation: Операция для выполнения над данными
        
    Returns:
        Обработанный список пользователей
        
    Raises:
        ValueError: Если операция не поддерживается
    """
    if operation == "uppercase":
        return [
            {key: value.upper() if isinstance(value, str) else value 
             for key, value in user.items()}
            for user in users
        ]
    elif operation == "lowercase":
        return [
            {key: value.lower() if isinstance(value, str) else value 
             for key, value in user.items()}
            for user in users
        ]
    else:
        raise ValueError(f"Неподдерживаемая операция: {operation}")


# 6. Пример использования аннотаций типов для сложных структур
UserData = Dict[str, Union[str, int, float, bool, List, Dict]]

def validate_user_data(user: UserData) -> bool:
    """
    Валидация данных пользователя
    
    Args:
        user: Словарь с данными пользователя
        
    Returns:
        True если данные валидны, иначе False
    """
    required_fields = ["name", "email", "age"]
    
    for field in required_fields:
        if field not in user:
            print(f"Отсутствует обязательное поле: {field}")
            return False
    
    # Проверка типа данных для возраста
    if not isinstance(user["age"], int) or user["age"] < 0:
        print("Поле 'age' должно быть положительным целым числом")
        return False
    
    # Проверка формата email (упрощенная)
    if not isinstance(user["email"], str) or "@" not in user["email"]:
        print("Поле 'email' должно содержать символ @")
        return False
    
    return True


# 7. Пример класса с property и setter
class Temperature:
    """
    Класс для работы с температурой
    """
    
    def __init__(self, celsius: float = 0):
        self._celsius = celsius
    
    @property
    def celsius(self) -> float:
        """Температура в градусах Цельсия"""
        return self._celsius
    
    @celsius.setter
    def celsius(self, value: float) -> None:
        """Установка температуры в градусах Цельсия"""
        if value < -273.15:
            raise ValueError("Температура не может быть ниже абсолютного нуля (-273.15°C)")
        self._celsius = value
    
    @property
    def fahrenheit(self) -> float:
        """Температура в градусах Фаренгейта"""
        return self._celsius * 9/5 + 32
    
    @property
    def kelvin(self) -> float:
        """Температура в Кельвинах"""
        return self._celsius + 273.15


# 8. Пример использования логирования
import logging

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def complex_calculation(data: List[float]) -> float:
    """
    Выполняет сложные вычисления с логированием
    
    Args:
        data: Список чисел для вычислений
        
    Returns:
        Результат вычислений
    """
    logger.info(f"Начало вычислений с {len(data)} элементами")
    
    try:
        # Проверка данных
        if not data:
            raise ValueError("Данные не могут быть пустыми")
        
        # Выполнение вычислений
        result = sum(x ** 2 for x in data if isinstance(x, (int, float)))
        logger.info(f"Вычисления завершены успешно, результат: {result}")
        
        return result
    except Exception as e:
        logger.error(f"Ошибка при вычислениях: {e}")
        raise


# 9. Пример использования контекстных менеджеров
class DatabaseConnection:
    """
    Класс-контекстный менеджер для подключения к базе данных
    """
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connection = None
    
    def __enter__(self):
        logger.info(f"Подключение к базе данных: {self.connection_string}")
        # Здесь обычно происходит реальное подключение
        self.connection = {"connected": True, "cs": self.connection_string}
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.info(f"Закрытие соединения с базой данных: {self.connection_string}")
        # Здесь обычно происходит закрытие соединения
        if self.connection:
            self.connection["connected"] = False
        
        if exc_type:
            logger.error(f"Ошибка при работе с БД: {exc_type.__name__}: {exc_val}")
        
        return False  # Не подавлять исключения


# 10. Пример модульного тестирования
def test_user_manager():
    """
    Простые тесты для UserManager
    """
    import tempfile
    
    # Создание временного файла для тестов
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as temp_file:
        temp_file_path = temp_file.name
    
    try:
        # Создание менеджера пользователей
        manager = UserManager(temp_file_path)
        
        # Тест добавления пользователя
        user = manager.add_user("Иван Иванов", "1990-01-01", "ivan@example.com")
        assert user["name"] == "Иван Иванов"
        assert user["age"] > 20  # Проверяем, что возраст вычислен правильно
        
        # Тест поиска пользователей по возрасту
        users = manager.find_users_by_age_range(25, 40)
        assert len(users) >= 1
        
        print("Все тесты пройдены успешно!")
        
    except AssertionError as e:
        print(f"Тест не пройден: {e}")
    except Exception as e:
        print(f"Ошибка при тестировании: {e}")
    finally:
        # Удаление временного файла
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


# 11. Пример документации класса с методами
class DataProcessor:
    """
    Класс для обработки данных различных типов
    
    Этот класс предоставляет методы для:
    - Валидации данных
    - Преобразования данных
    - Фильтрации данных
    - Агрегации данных
    
    Пример использования:
    >>> processor = DataProcessor()
    >>> data = [{"name": "Иван", "age": 30}, {"name": "Мария", "age": 25}]
    >>> result = processor.filter_by_age(data, min_age=20, max_age=35)
    >>> len(result)
    2
    """
    
    def __init__(self, default_encoding: str = "utf-8"):
        """
        Инициализация процессора данных
        
        Args:
            default_encoding: Кодировка по умолчанию для работы с файлами
        """
        self.default_encoding = default_encoding
    
    def filter_by_age(self, 
                     data: List[Dict[str, Union[str, int]]], 
                     min_age: int, 
                     max_age: int) -> List[Dict[str, Union[str, int]]]:
        """
        Фильтрация данных по возрасту
        
        Args:
            data: Список словарей с ключом 'age'
            min_age: Минимальный возраст
            max_age: Максимальный возраст
            
        Returns:
            Отфильтрованный список данных
        """
        return [
            item for item in data
            if isinstance(item.get('age'), int) and min_age <= item['age'] <= max_age
        ]


# 12. Пример использования if __name__ == "__main__":
def main():
    """
    Основная функция приложения
    """
    print("Демонстрация стандартов кодирования Python")
    
    # Создание экземпляра класса
    temp = Temperature(25)
    print(f"Температура: {temp.celsius}°C = {temp.fahrenheit}°F = {temp.kelvin}K")
    
    # Работа с пользовательскими данными
    user_manager = UserManager()
    user_manager.add_user("Алексей Петров", "1985-06-15", "alexey@example.com")
    
    # Демонстрация логирования
    data = [1.0, 2.0, 3.0, 4.0, 5.0]
    result = complex_calculation(data)
    print(f"Результат вычислений: {result}")
    
    # Использование контекстного менеджера
    with DatabaseConnection("postgresql://localhost/mydb") as conn:
        print(f"Соединение установлено: {conn['connected']}")
    
    # Запуск тестов
    test_user_manager()


if __name__ == "__main__":
    main()
