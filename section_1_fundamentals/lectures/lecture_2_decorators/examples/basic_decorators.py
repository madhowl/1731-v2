# Примеры базовых декораторов

def my_decorator(func):
    """
    Простой декоратор, который добавляет сообщения до и после выполнения функции
    """
    def wrapper():
        print("До выполнения функции")
        func()
        print("После выполнения функции")
    return wrapper

@my_decorator
def say_hello():
    print("Привет!")

# Декоратор с аргументами
def decorator_with_args(func):
    def wrapper(*args, **kwargs):
        print(f"Вызов функции {func.__name__} с аргументами {args}, {kwargs}")
        result = func(*args, **kwargs)
        print(f"Функция {func.__name__} вернула {result}")
        return result
    return wrapper

@decorator_with_args
def add(a, b):
    return a + b

# Декоратор для измерения времени выполнения
import time

def timer_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Функция {func.__name__} выполнилась за {end_time - start_time:.4f} секунд")
        return result
    return wrapper

@timer_decorator
def slow_function():
    time.sleep(1)
    return "Готово!"

# Декоратор для логирования
def log_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Вызывается функция {func.__name__}")
        result = func(*args, **kwargs)
        print(f"Функция {func.__name__} завершена")
        return result
    return wrapper

@log_decorator
def multiply(x, y):
    return x * y

if __name__ == "__main__":
    say_hello()
    print(add(5, 3))
    print(slow_function())
    print(multiply(4, 7))
