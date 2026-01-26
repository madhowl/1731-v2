# Упражнения по созданию декораторов

# Упражнение 1: Простой декоратор логирования
def log_calls(func):
    """
    Декоратор, который логирует вызовы функции
    """
    def wrapper(*args, **kwargs):
        print(f"Вызывается функция {func.__name__} с аргументами {args}, {kwargs}")
        result = func(*args, **kwargs)
        print(f"Функция {func.__name__} вернула {result}")
        return result
    return wrapper

# Упражнение 2: Декоратор для измерения времени выполнения
import time

def timing_decorator(func):
    """
    Декоратор, который измеряет время выполнения функции
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Функция {func.__name__} выполнилась за {end_time - start_time:.4f} секунд")
        return result
    return wrapper

# Упражнение 3: Декоратор с параметрами для повторения выполнения
def repeat(times):
    """
    Декоратор, который повторяет выполнение функции заданное количество раз
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

# Упражнение 4: Декоратор для ограничения количества попыток
def retry(max_attempts, exception_type=Exception):
    """
    Декоратор, который повторяет выполнение функции при возникновении исключения
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except exception_type as e:
                    if attempt == max_attempts - 1:
                        raise e
                    print(f"Попытка {attempt + 1} не удалась: {e}. Повторная попытка...")
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Упражнение 5: Декоратор для кэширования
def cache_decorator(func):
    """
    Декоратор, который кэширует результаты выполнения функции
    """
    cache = {}
    
    def wrapper(*args, **kwargs):
        # Создаем ключ из аргументов
        key = str(args) + str(sorted(kwargs.items()))
        
        if key in cache:
            print(f"Используем кэш для {func.__name__}")
            return cache[key]
        
        result = func(*args, **kwargs)
        cache[key] = result
        print(f"Сохраняем результат в кэш для {func.__name__}")
        return result
    
    return wrapper

# Упражнение 6: Декоратор для проверки типов аргументов
def type_check(*expected_types):
    """
    Декоратор для проверки типов аргументов функции
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            if len(args) != len(expected_types):
                raise TypeError(f"Функция {func.__name__} должна принимать {len(expected_types)} аргументов, а не {len(args)}")
            
            for i, (arg, expected_type) in enumerate(zip(args, expected_types)):
                if not isinstance(arg, expected_type):
                    raise TypeError(f"Аргумент {i+1} функции {func.__name__} должен быть типа {expected_type.__name__}, а не {type(arg).__name__}")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Упражнение 7: Декоратор singleton
def singleton(cls):
    """
    Декоратор-синглтон, гарантирующий, что класс имеет только один экземпляр
    """
    instances = {}
    
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instance

# Упражнение 8: Декоратор rate limiter
import time
from functools import wraps

def rate_limit(calls_per_second=1):
    """
    Декоратор, который ограничивает частоту вызовов функции
    """
    min_interval = 1.0 / calls_per_second
    last_called = [0.0]

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = min_interval - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            ret = func(*args, **kwargs)
            last_called[0] = time.time()
            return ret
        return wrapper
    return decorator

# Упражнение 9: Декоратор validate
def validate(**validators):
    """
    Декоратор, который проверяет значения аргументов с помощью заданных валидаторов
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Получаем имена аргументов функции
            import inspect
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            # Проверяем каждый аргумент, для которого есть валидатор
            for param_name, validator in validators.items():
                if param_name in bound_args.arguments:
                    value = bound_args.arguments[param_name]
                    if not validator(value):
                        raise ValueError(f"Аргумент {param_name} функции {func.__name__} не прошел валидацию")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Тестирование декораторов
if __name__ == "__main__":
    # Тестирование декоратора логирования
    @log_calls
    def add_numbers(a, b):
        """Функция сложения двух чисел"""
        return a + b

    print("=== Тестирование log_calls ===")
    result = add_numbers(5, 3)
    print(f"Результат: {result}\n")

    # Тестирование декоратора измерения времени
    @timing_decorator
    def slow_function():
        """Функция, которая имитирует долгое выполнение"""
        time.sleep(0.5)
        return "Готово!"

    print("=== Тестирование timing_decorator ===")
    result = slow_function()
    print(f"Результат: {result}\n")

    # Тестирование декоратора повторения
    @repeat(times=3)
    def say_hello():
        print("Привет!")

    print("=== Тестирование repeat ===")
    say_hello()
    print()

    # Тестирование декоратора retry
    @retry(max_attempts=3)
    def unreliable_function():
        import random
        if random.random() < 0.7:
            raise ConnectionError("Ошибка подключения")
        return "Успешно!"

    print("=== Тестирование retry ===")
    try:
        result = unreliable_function()
        print(f"Результат: {result}")
    except Exception as e:
        print(f"Не удалось выполнить функцию: {e}")
    print()

    # Тестирование декоратора кэширования
    @cache_decorator
    def fibonacci(n):
        """Функция вычисления чисел Фибоначчи (медленная реализация для демонстрации)"""
        if n < 2:
            return n
        return fibonacci(n-1) + fibonacci(n-2)

    print("=== Тестирование cache_decorator ===")
    print(f"fibonacci(10) = {fibonacci(10)}")
    print(f"fibonacci(10) = {fibonacci(10)}")  # Должно использовать кэш
    print()

    # Тестирование декоратора проверки типов
    @type_check(int, int)
    def divide(a, b):
        """Функция деления двух чисел"""
        if b == 0:
            raise ValueError("Деление на ноль невозможно")
        return a / b

    print("=== Тестирование type_check ===")
    try:
        result = divide(10, 2)
        print(f"divide(10, 2) = {result}")
        
        result = divide(10, "2")  # Должно вызвать TypeError
    except TypeError as e:
        print(f"Ошибка: {e}")
    print()

    # Тестирование декоратора singleton
    @singleton
    class DatabaseConnection:
        def __init__(self):
            self.connection_string = "connection_string"
            print("Создание подключения к базе данных")

    print("=== Тестирование singleton ===")
    db1 = DatabaseConnection()
    db2 = DatabaseConnection()
    print(f"db1 is db2: {db1 is db2}")
    print()

    # Тестирование декоратора rate_limit
    @rate_limit(calls_per_second=2)
    def limited_function():
        print("Вызов функции")

    print("=== Тестирование rate_limit ===")
    print("Вызываем функцию 3 раза с ограничением 2 вызова в секунду:")
    start_time = time.time()
    for i in range(3):
        limited_function()
    end_time = time.time()
    print(f"Время выполнения: {end_time - start_time:.2f} секунд")
    print()

    # Тестирование декоратора validate
    @validate(x=lambda x: x > 0, y=lambda y: y != 0)
    def validated_divide(x, y):
        return x / y

    print("=== Тестирование validate ===")
    try:
        result = validated_divide(10, 2)
        print(f"validated_divide(10, 2) = {result}")
        
        result = validated_divide(-5, 2)  # Должно вызвать ValueError
    except ValueError as e:
        print(f"Ошибка: {e}")
