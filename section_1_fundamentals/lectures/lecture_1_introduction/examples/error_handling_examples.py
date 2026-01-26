# Примеры обработки ошибок в Python

"""
Этот файл демонстрирует различные подходы к обработке ошибок в Python
и лучшие практики в этой области.
"""

import sys
import logging
from typing import Union, List, Dict, Any
from pathlib import Path

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# 1. Создание пользовательских исключений
class ValidationError(Exception):
    """Исключение для ошибок валидации данных"""
    pass

class DataProcessingError(Exception):
    """Исключение для ошибок обработки данных"""
    pass

class ConfigurationError(Exception):
    """Исключение для ошибок конфигурации"""
    pass


# 2. Примеры базовой обработки исключений
def divide_numbers(a: float, b: float) -> float:
    """
    Деление двух чисел с обработкой исключений
    
    Args:
        a: Делимое
        b: Делитель
        
    Returns:
        Результат деления
        
    Raises:
        ZeroDivisionError: Если делитель равен нулю
        TypeError: Если аргументы не являются числами
    """
    try:
        if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
            raise TypeError(f"Ожидается число, получено {type(a).__name__} и {type(b).__name__}")
        
        if b == 0:
            raise ZeroDivisionError("Деление на ноль невозможно")
        
        result = a / b
        logger.info(f"Успешное деление: {a} / {b} = {result}")
        return result
    
    except ZeroDivisionError as e:
        logger.error(f"Ошибка деления на ноль: {a} / {b}")
        raise  # Повторно выбрасываем исключение
    except TypeError as e:
        logger.error(f"Неверный тип аргументов: {e}")
        raise  # Повторно выбрасываем исключение
    except Exception as e:
        logger.critical(f"Неожиданная ошибка при делении: {e}")
        raise  # Повторно выбрасываем исключение


def safe_convert_to_int(value: str) -> int:
    """
    Безопасное преобразование строки в целое число
    
    Args:
        value: Строка для преобразования
        
    Returns:
        Целое число
        
    Raises:
        ValueError: Если строку невозможно преобразовать в число
    """
    try:
        result = int(value)
        logger.debug(f"Успешное преобразование '{value}' в {result}")
        return result
    except ValueError as e:
        logger.warning(f"Невозможно преобразовать '{value}' в целое число: {e}")
        raise
    except TypeError as e:
        logger.error(f"Неверный тип аргумента: {e}")
        raise


# 3. Примеры работы с файлами и исключениями
def read_file_safe(file_path: str) -> str:
    """
    Безопасное чтение файла с обработкой исключений
    
    Args:
        file_path: Путь к файлу
        
    Returns:
        Содержимое файла в виде строки
    """
    try:
        path = Path(file_path)
        
        # Проверяем, что файл существует
        if not path.exists():
            raise FileNotFoundError(f"Файл не найден: {file_path}")
        
        # Проверяем, что это файл, а не директория
        if not path.is_file():
            raise IsADirectoryError(f"Путь указывает на директорию, а не на файл: {file_path}")
        
        # Читаем файл
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        logger.info(f"Файл успешно прочитан: {file_path}")
        return content
    
    except FileNotFoundError as e:
        logger.error(f"Файл не найден: {e}")
        raise
    except PermissionError as e:
        logger.error(f"Нет доступа к файлу: {e}")
        raise
    except UnicodeDecodeError as e:
        logger.error(f"Ошибка декодирования файла (возможно, неверная кодировка): {e}")
        raise
    except Exception as e:
        logger.critical(f"Неожиданная ошибка при чтении файла: {e}")
        raise


def write_file_safe(file_path: str, content: str) -> bool:
    """
    Безопасная запись в файл с обработкой исключений
    
    Args:
        file_path: Путь к файлу
        content: Содержимое для записи
        
    Returns:
        True если запись успешна, иначе False
    """
    try:
        # Создаем директории если они не существуют
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
        
        logger.info(f"Файл успешно записан: {file_path}")
        return True
    
    except PermissionError as e:
        logger.error(f"Нет прав на запись в файл: {e}")
        return False
    except OSError as e:
        logger.error(f"Ошибка операционной системы при записи файла: {e}")
        return False
    except Exception as e:
        logger.critical(f"Неожиданная ошибка при записи файла: {e}")
        return False


# 4. Примеры использования блоков finally и else
def process_data_with_cleanup(data: List[Any]) -> List[Any]:
    """
    Обработка данных с гарантией выполнения очистки
    """
    temp_resource = None
    result = []
    
    try:
        logger.info("Начало обработки данных")
        temp_resource = acquire_temp_resource()  # Условный метод получения ресурса
        
        # Обработка данных
        for item in data:
            processed_item = transform_item(item)
            result.append(processed_item)
        
        logger.info("Обработка данных завершена успешно")
        return result
    
    except DataProcessingError as e:
        logger.error(f"Ошибка обработки данных: {e}")
        raise
    except Exception as e:
        logger.critical(f"Неожиданная ошибка: {e}")
        raise
    else:
        # Выполняется только если не было исключений
        logger.debug("Блок else: обработка завершена без ошибок")
    finally:
        # Выполняется всегда
        if temp_resource:
            release_temp_resource(temp_resource)  # Условный метод освобождения ресурса
            logger.debug("Временный ресурс освобожден")


def acquire_temp_resource():
    """Условная функция получения временного ресурса"""
    logger.debug("Получение временного ресурса")
    return {"resource_id": 123, "status": "active"}


def release_temp_resource(resource):
    """Условная функция освобождения временного ресурса"""
    logger.debug(f"Освобождение ресурса: {resource['resource_id']}")


def transform_item(item):
    """Условная функция трансформации элемента"""
    if isinstance(item, str):
        return item.upper()
    elif isinstance(item, (int, float)):
        return item * 2
    else:
        raise DataProcessingError(f"Неподдерживаемый тип данных: {type(item)}")


# 5. Пример использования контекстных менеджеров
class DatabaseConnection:
    """
    Пример контекстного менеджера для подключения к базе данных
    """
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connected = False
        self.connection = None
    
    def __enter__(self):
        """Вход в контекстный менеджер"""
        logger.info(f"Подключение к базе данных: {self.connection_string}")
        try:
            # Здесь обычно происходит реальное подключение
            self.connection = {"connected": True, "cs": self.connection_string}
            self.connected = True
            return self
        except Exception as e:
            logger.error(f"Ошибка подключения к базе данных: {e}")
            raise
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Выход из контекстного менеджера"""
        if self.connected:
            logger.info(f"Отключение от базы данных: {self.connection_string}")
            # Здесь обычно происходит закрытие соединения
            self.connection = None
            self.connected = False
        
        # Обработка исключений
        if exc_type:
            logger.error(f"Исключение в контексте базы данных: {exc_type.__name__}: {exc_val}")
        
        # Возвращаем False, чтобы исключение продолжило распространение
        return False
    
    def execute_query(self, query: str) -> List[Dict[str, Any]]:
        """
        Выполнение SQL-запроса
        
        Args:
            query: SQL-запрос для выполнения
            
        Returns:
            Результат запроса в виде списка словарей
        """
        if not self.connected:
            raise ConnectionError("Соединение с базой данных не установлено")
        
        logger.info(f"Выполнение запроса: {query}")
        # Здесь обычно выполняется реальный запрос
        return [{"id": 1, "name": "Пример", "value": 100}]


def database_operation_example():
    """
    Пример использования контекстного менеджера базы данных
    """
    try:
        with DatabaseConnection("postgresql://localhost/mydb") as db:
            result = db.execute_query("SELECT * FROM users LIMIT 5")
            print(f"Результат запроса: {result}")
    except ConnectionError as e:
        logger.error(f"Ошибка подключения: {e}")
    except Exception as e:
        logger.error(f"Ошибка операции с базой данных: {e}")


# 6. Пример валидации данных с исключениями
def validate_user_data(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Валидация данных пользователя
    
    Args:
        user_data: Словарь с данными пользователя
        
    Returns:
        Валидированные данные пользователя
        
    Raises:
        ValidationError: Если данные не проходят валидацию
    """
    if not isinstance(user_data, dict):
        raise ValidationError("Данные пользователя должны быть словарем")
    
    required_fields = ["name", "email", "age"]
    for field in required_fields:
        if field not in user_data:
            raise ValidationError(f"Обязательное поле '{field}' отсутствует")
    
    # Валидация имени
    name = user_data.get("name")
    if not isinstance(name, str) or len(name.strip()) == 0:
        raise ValidationError("Поле 'name' должно быть непустой строкой")
    
    # Валидация email
    email = user_data.get("email")
    if not isinstance(email, str) or "@" not in email:
        raise ValidationError("Поле 'email' должно содержать символ @")
    
    # Валидация возраста
    age = user_data.get("age")
    if not isinstance(age, int) or age < 0 or age > 150:
        raise ValidationError("Поле 'age' должно быть целым числом от 0 до 150")
    
    # Валидация дополнительных полей
    if "phone" in user_data:
        phone = user_data["phone"]
        if not isinstance(phone, str) or not phone.isdigit():
            raise ValidationError("Поле 'phone' должно содержать только цифры")
    
    logger.info(f"Данные пользователя '{name}' прошли валидацию")
    return user_data


def validate_user_data_extended(user_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Расширенная валидация данных пользователя с различными уровнями проверки
    
    Args:
        user_data: Словарь с данными пользователя
        
    Returns:
        Валидированные данные пользователя
        
    Raises:
        ValidationError: Если данные не проходят валидацию
    """
    errors = []
    
    # Проверка структуры данных
    if not isinstance(user_data, dict):
        raise ValidationError("Данные пользователя должны быть словарем")
    
    # Обязательные поля
    required_fields = {
        "name": str,
        "email": str,
        "age": int
    }
    
    for field, expected_type in required_fields.items():
        if field not in user_data:
            errors.append(f"Отсутствует обязательное поле '{field}'")
        elif not isinstance(user_data[field], expected_type):
            errors.append(f"Поле '{field}' должно быть типа {expected_type.__name__}")
    
    if errors:
        raise ValidationError(f"Ошибки валидации: {'; '.join(errors)}")
    
    # Дополнительные проверки
    name = user_data["name"]
    if len(name.strip()) == 0:
        errors.append("Поле 'name' не может быть пустым")
    elif len(name) > 100:
        errors.append("Поле 'name' слишком длинное (максимум 100 символов)")
    
    email = user_data["email"]
    if "@" not in email or "." not in email.split("@")[-1]:
        errors.append("Поле 'email' имеет некорректный формат")
    elif len(email) > 254:
        errors.append("Поле 'email' слишком длинное (максимум 254 символа)")
    
    age = user_data["age"]
    if age < 0:
        errors.append("Поле 'age' не может быть отрицательным")
    elif age > 150:
        errors.append("Поле 'age' слишком велико (максимум 150)")
    
    if errors:
        raise ValidationError(f"Ошибки валидации: {'; '.join(errors)}")
    
    # Валидация необязательных полей
    if "phone" in user_data:
        phone = user_data["phone"]
        if not isinstance(phone, str):
            errors.append("Поле 'phone' должно быть строкой")
        else:
            # Удаляем все нецифровые символы и проверяем длину
            digits_only = ''.join(filter(str.isdigit, phone))
            if len(digits_only) < 10 or len(digits_only) > 15:
                errors.append("Поле 'phone' должно содержать от 10 до 15 цифр")
    
    if errors:
        raise ValidationError(f"Ошибки валидации: {'; '.join(errors)}")
    
    logger.info(f"Расширенная валидация данных пользователя '{name}' пройдена")
    return user_data


# 7. Пример обработки исключений в цикле
def process_multiple_files(file_paths: List[str]) -> Dict[str, Union[bool, str]]:
    """
    Обработка нескольких файлов с индивидуальной обработкой ошибок
    
    Args:
        file_paths: Список путей к файлам для обработки
        
    Returns:
        Словарь с результатами обработки для каждого файла
    """
    results = {}
    
    for file_path in file_paths:
        try:
            content = read_file_safe(file_path)
            # Условная обработка содержимого файла
            processed_content = content.upper()  # Пример простой обработки
            write_file_safe(f"processed_{file_path}", processed_content)
            
            results[file_path] = {"success": True, "message": "Файл успешно обработан"}
            logger.info(f"Файл {file_path} успешно обработан")
            
        except FileNotFoundError:
            results[file_path] = {"success": False, "message": "Файл не найден"}
            logger.warning(f"Файл не найден: {file_path}")
            
        except PermissionError:
            results[file_path] = {"success": False, "message": "Нет доступа к файлу"}
            logger.warning(f"Нет доступа к файлу: {file_path}")
            
        except Exception as e:
            results[file_path] = {"success": False, "message": f"Ошибка: {str(e)}"}
            logger.error(f"Ошибка при обработке файла {file_path}: {e}")
    
    return results


# 8. Пример логирования ошибок
def log_error_example():
    """
    Пример использования логирования для отслеживания ошибок
    """
    try:
        # Симуляция ошибки
        result = 10 / 0
    except ZeroDivisionError as e:
        # Логирование ошибки с подробной информацией
        logger.error("Произошло деление на ноль", exc_info=True)
        # Также можно добавить пользовательские данные к логу
        logger.error(f"Ошибка в модуле {__name__} в функции {sys._getframe().f_code.co_name}")
    except Exception as e:
        logger.critical(f"Неожиданная ошибка: {e}", exc_info=True)
        # При критических ошибках часто требуется завершение программы
        sys.exit(1)


# 9. Пример обработки пользовательских исключений
class BankAccount:
    """
    Пример банковского счета с обработкой ошибок
    """
    
    def __init__(self, initial_balance: float = 0.0):
        if initial_balance < 0:
            raise ValidationError("Начальный баланс не может быть отрицательным")
        
        self._balance = initial_balance
        self.transaction_history = []
    
    @property
    def balance(self) -> float:
        return self._balance
    
    def deposit(self, amount: float) -> float:
        """
        Пополнение счета
        
        Args:
            amount: Сумма для пополнения
            
        Returns:
            Новый баланс
            
        Raises:
            ValidationError: Если сумма отрицательная
        """
        if amount <= 0:
            raise ValidationError("Сумма пополнения должна быть положительной")
        
        self._balance += amount
        self.transaction_history.append({
            "type": "deposit",
            "amount": amount,
            "balance_after": self._balance,
            "timestamp": __import__('datetime').datetime.now().isoformat()
        })
        
        logger.info(f"Пополнение на {amount}, новый баланс: {self._balance}")
        return self._balance
    
    def withdraw(self, amount: float) -> float:
        """
        Снятие со счета
        
        Args:
            amount: Сумма для снятия
            
        Returns:
            Новый баланс
            
        Raises:
            ValidationError: Если сумма отрицательная
            ValueError: Если недостаточно средств
        """
        if amount <= 0:
            raise ValidationError("Сумма снятия должна быть положительной")
        
        if amount > self._balance:
            raise ValueError(f"Недостаточно средств. Баланс: {self._balance}, запрошено: {amount}")
        
        self._balance -= amount
        self.transaction_history.append({
            "type": "withdraw",
            "amount": amount,
            "balance_after": self._balance,
            "timestamp": __import__('datetime').datetime.now().isoformat()
        })
        
        logger.info(f"Снятие {amount}, новый баланс: {self._balance}")
        return self._balance


# 10. Пример использования декоратора для обработки исключений
from functools import wraps

def exception_handler(log_error=True, raise_exception=True, default_return=None):
    """
    Декоратор для обработки исключений
    
    Args:
        log_error: Логировать ли ошибки
        raise_exception: Вызывать ли исключение дальше
        default_return: Значение по умолчанию в случае ошибки
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if log_error:
                    logger.error(f"Ошибка в функции {func.__name__}: {e}")
                
                if raise_exception:
                    raise
                else:
                    return default_return
        return wrapper
    return decorator

@exception_handler(log_error=True, raise_exception=False, default_return="ERROR")
def risky_function(x, y):
    """Функция, которая может вызвать ошибку"""
    return x / y

# Пример использования
if __name__ == "__main__":
    print("=== Демонстрация обработки ошибок ===\n")
    
    # Пример 1: Деление чисел
    print("1. Деление чисел:")
    try:
        result = divide_numbers(10, 2)
        print(f"   10 / 2 = {result}")
        
        result = divide_numbers(10, 0)  # Это вызовет исключение
    except ZeroDivisionError as e:
        print(f"   Ошибка: {e}")
    
    # Пример 2: Преобразование строки в число
    print("\n2. Преобразование строки в число:")
    try:
        result = safe_convert_to_int("123")
        print(f"   Результат: {result}")
        
        result = safe_convert_to_int("abc")  # Это вызовет исключение
    except ValueError as e:
        print(f"   Ошибка: {e}")
    
    # Пример 3: Работа с файлами
    print("\n3. Работа с файлами:")
    try:
        content = read_file_safe("nonexistent.txt")  # Это вызовет исключение
    except FileNotFoundError as e:
        print(f"   Ошибка: {e}")
    
    # Пример 4: Валидация данных
    print("\n4. Валидация данных:")
    user_data = {
        "name": "Иван Иванов",
        "email": "ivan@example.com",
        "age": 30
    }
    
    try:
        validated_data = validate_user_data(user_data)
        print(f"   Данные валидны: {validated_data['name']}")
    except ValidationError as e:
        print(f"   Ошибка валидации: {e}")
    
    # Пример 5: Работа с банковским счетом
    print("\n5. Работа с банковским счетом:")
    try:
        account = BankAccount(1000.0)
        print(f"   Баланс: {account.balance}")
        
        account.deposit(500.0)
        print(f"   Баланс после пополнения: {account.balance}")
        
        account.withdraw(200.0)
        print(f"   Баланс после снятия: {account.balance}")
        
        account.withdraw(2000.0)  # Это вызовет исключение
    except (ValidationError, ValueError) as e:
        print(f"   Ошибка операции: {e}")
    
    # Пример 6: Использование декоратора
    print("\n6. Использование декоратора обработки исключений:")
    result = risky_function(10, 2)  # Работает нормально
    print(f"   10 / 2 = {result}")
    
    result = risky_function(10, 0)  # Возвращает "ERROR" вместо исключения
    print(f"   10 / 0 = {result}")
    
    print("\n=== Демонстрация завершена ===")
