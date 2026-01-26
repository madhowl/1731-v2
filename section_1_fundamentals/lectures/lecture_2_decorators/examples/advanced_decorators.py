# Примеры продвинутых декораторов

from functools import wraps

def repeat_decorator(times):
    """
    Декоратор с параметрами, который повторяет выполнение функции заданное количество раз
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat_decorator(times=3)
def greet(name):
    print(f"Привет, {name}!")

def retry_decorator(max_attempts):
    """
    Декоратор с параметрами, который повторяет выполнение функции при возникновении исключения
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise e
                    print(f"Попытка {attempt + 1} не удалась: {e}. Повторная попытка...")
        return wrapper
    return decorator

@retry_decorator(max_attempts=3)
def unreliable_function():
    import random
    if random.random() < 0.7:
        raise ConnectionError("Ошибка подключения")
    return "Успешно!"

def cache_decorator(func):
    """
    Декоратор для кэширования результатов выполнения функции
    """
    cache = {}
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        # Создаем ключ из аргументов
        key = str(args) + str(sorted(kwargs.items()))
        
        if key in cache:
            print(f"Возвращаем результат из кэша для {func.__name__}")
            return cache[key]
        
        result = func(*args, **kwargs)
        cache[key] = result
        print(f"Сохраняем результат в кэш для {func.__name__}")
        return result
    
    return wrapper

@cache_decorator
def fibonacci(n):
    """Функция вычисления чисел Фибоначчи (медленная реализация для демонстрации)"""
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

def type_check(*expected_types):
    """
    Декоратор для проверки типов аргументов функции
    
    Args:
        *expected_types: Ожидаемые типы аргументов
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if len(args) > len(expected_types):
                raise TypeError(f"Функция {func.__name__} принимает {len(expected_types)} аргументов, но получила {len(args)}")
            
            for i, (arg, expected_type) in enumerate(zip(args, expected_types)):
                if not isinstance(arg, expected_type):
                    raise TypeError(f"Аргумент {i+1} функции {func.__name__} должен быть типа {expected_type.__name__}, а не {type(arg).__name__}")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

@type_check(int, int)
def divide(a, b):
    """Функция деления двух чисел"""
    if b == 0:
        raise ValueError("Деление на ноль невозможно")
    return a / b

# Декоратор для проверки прав доступа
def requires_permission(permission):
    """
    Декоратор для проверки наличия прав доступа
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # В реальной системе здесь была бы проверка прав пользователя
            user_permissions = ['read', 'write']  # пример
            
            if permission not in user_permissions:
                raise PermissionError(f"Недостаточно прав. Требуется '{permission}'")
            
            return func(*args, **kwargs)
        return wrapper
    return decorator

@requires_permission('admin')
def delete_user(user_id):
    """Функция удаления пользователя (требует права администратора)"""
    return f"Пользователь {user_id} удален"

if __name__ == "__main__":
    # Демонстрация работы декораторов
    print("=== Повторение выполнения ===")
    greet("Иван")
    
    print("\n=== Кэширование ===")
    print(fibonacci(10))
    print(fibonacci(10))  # Должно использовать кэш
    
    print("\n=== Проверка типов ===")
    print(divide(10, 2))
    try:
        print(divide(10, "2"))  # Вызовет TypeError
    except TypeError as e:
        print(f"Ошибка: {e}")
    
    print("\n=== Проверка прав доступа ===")
    try:
        delete_user(123)  # Может вызвать PermissionError в зависимости от прав
    except PermissionError as e:
        print(f"Ошибка доступа: {e}")
    
    print("\n=== Повторные попытки ===")
    try:
        result = unreliable_function()
        print(f"Результат: {result}")
    except ConnectionError as e:
        print(f"Не удалось выполнить функцию: {e}")
