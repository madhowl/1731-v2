# Примеры декораторов в функциональном программировании

from functools import wraps, reduce
import time

def compose(*functions):
    """
    Композиция функций - создает новую функцию, применяющую переданные функции последовательно
    """
    return lambda x: reduce(lambda acc, f: f(acc), functions, x)

def pipe(*functions):
    """
    Пайплайн функций - аналог compose, но в более читаемом виде
    """
    return lambda x: reduce(lambda acc, f: f(acc), functions, x)

def memoize(func):
    """
    Декоратор для мемоизации (кеширования результатов функции)
    """
    cache = {}
    
    @wraps(func)
    def wrapper(*args):
        if args in cache:
            print(f"Используем кэш для {func.__name__}{args}")
            return cache[args]
        
        result = func(*args)
        cache[args] = result
        print(f"Сохраняем в кэш результат для {func.__name__}{args}")
        return result
    
    return wrapper

@memoize
def expensive_calculation(n):
    """Дорогостоящая операция"""
    print(f"Выполняем дорогостоящее вычисление для {n}")
    time.sleep(0.1)  # Имитация длительного вычисления
    return n ** 2

def curry(func):
    """
    Декоратор для каррирования функции
    """
    @wraps(func)
    def curried(*args, **kwargs):
        if len(args) + len(kwargs) >= func.__code__.co_argcount:
            return func(*args, **kwargs)
        return lambda *more_args, **more_kwargs: curried(*(args + more_args), **{**kwargs, **more_kwargs})
    return curried

@curry
def add_three_numbers(a, b, c):
    return a + b + c

def identity(x):
    """Функция тождественного отображения"""
    return x

def constant(value):
    """Функция-константа"""
    return lambda *args, **kwargs: value

def apply_twice(func):
    """Декоратор, который применяет функцию дважды"""
    @wraps(func)
    def wrapper(x):
        return func(func(x))
    return wrapper

@apply_twice
def square(x):
    return x * x

def chain_decorators(*decorators):
    """
    Функция для объединения нескольких декораторов в один
    """
    def combined_decorator(func):
        for decorator in reversed(decorators):
            func = decorator(func)
        return func
    return combined_decorator

# Примеры использования
def functional_examples():
    print("=== Композиция функций ===")
    add_one = lambda x: x + 1
    multiply_by_two = lambda x: x * 2
    square_func = lambda x: x ** 2
    
    # Композиция: сначала +1, потом *2, потом возведение в квадрат
    composed = compose(add_one, multiply_by_two, square_func)
    result = composed(3)  # ((3+1)*2)^2 = (4*2)^2 = 8^2 = 64
    print(f"Композиция функций: composed(3) = {result}")
    
    print("\n=== Мемоизация ===")
    print(f"expensive_calculation(5) = {expensive_calculation(5)}")
    print(f"expensive_calculation(5) = {expensive_calculation(5)}")  # Использует кэш
    
    print("\n=== Каррирование ===")
    add_five_and_three = add_three_numbers(5)(3)
    result = add_five_and_three(2)  # 5 + 3 + 2 = 10
    print(f"Каррирование: add_three_numbers(5)(3)(2) = {result}")
    
    print("\n=== Применение функции дважды ===")
    result = square(3)  # (3^2)^2 = 9^2 = 81
    print(f"square(3) с декоратором apply_twice = {result}")
    
    print("\n=== Цепочка декораторов ===")
    def multiply_by(x):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs) * x
            return wrapper
        return decorator
    
    def add_constant(x):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs) + x
            return wrapper
        return decorator
    
    # Создаем цепочку декораторов
    chained = chain_decorators(multiply_by(2), add_constant(5))
    
    @chained
    def base_function(x):
        return x
    
    # Результат: (x + 5) * 2
    result = base_function(3)  # (3 + 5) * 2 = 16
    print(f"Цепочка декораторов: base_function(3) = {result}")

if __name__ == "__main__":
    functional_examples()
