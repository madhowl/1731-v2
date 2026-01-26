# Лекция 2: Декораторы в Python

## Создание и применение декораторов, встроенные декораторы, функциональное программирование

### План лекции:
1. Понятие декоратора
2. Простые декораторы
3. Декораторы с аргументами
4. Встроенные декораторы Python
5. Примеры использования
6. Функциональное программирование и декораторы

---

## 1. Понятие декоратора

### Что такое декоратор?

Декоратор в Python - это функция, которая принимает другую функцию в качестве аргумента и возвращает новую функцию, расширяющую или изменяющую поведение оригинальной функции, не изменяя её кода напрямую.

Декораторы позволяют модифицировать поведение функций или классов, используя синтаксис `@decorator_name`.

```python
def my_decorator(func):
    def wrapper():
        print("Что-то делается перед вызовом функции")
        func()
        print("Что-то делается после вызова функции")
    return wrapper

@my_decorator
def say_hello():
    print("Привет!")

say_hello()
```

Вывод:
```
Что-то делается перед вызовом функции
Привет!
Что-то делается после вызова функции
```

### Декораторы как синтаксический сахар

Синтаксис `@decorator` является синтаксическим сахаром для следующего:

```python
# Это
@my_decorator
def say_hello():
    print("Привет!")

# Эквивалентно этому
def say_hello():
    print("Привет!")
say_hello = my_decorator(say_hello)
```

---

## 2. Простые декораторы

### Примеры простых декораторов

#### Декоратор для измерения времени выполнения

```python
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

print(slow_function())
```

#### Декоратор для логирования

```python
def log_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Вызывается функция {func.__name__} с аргументами {args} и {kwargs}")
        result = func(*args, **kwargs)
        print(f"Функция {func.__name__} вернула {result}")
        return result
    return wrapper

@log_decorator
def add(a, b):
    return a + b

print(add(3, 5))
```

#### Декоратор для кэширования

```python
def cache_decorator(func):
    cache = {}
    
    def wrapper(*args):
        if args in cache:
            print(f"Возвращаем результат из кэша для {args}")
            return cache[args]
        
        result = func(*args)
        cache[args] = result
        print(f"Сохраняем результат в кэш для {args}")
        return result
    
    return wrapper

@cache_decorator
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

print(fibonacci(5))
```

---

## 3. Декораторы с аргументами

### Декораторы, которые принимают параметры

Для создания декоратора, который сам принимает аргументы, нужна дополнительная обертка:

```python
def repeat_decorator(times):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat_decorator(times=3)
def greet(name):
    print(f"Привет, {name}!")

greet("Иван")
```

### Декоратор с параметрами для ограничения попыток

```python
def retry(max_attempts):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if attempt == max_attempts - 1:
                        raise e
                    print(f"Попытка {attempt + 1} не удалась: {e}. Повтор...")
        return wrapper
    return decorator

@retry(max_attempts=3)
def unstable_function():
    import random
    if random.random() < 0.7:
        raise Exception("Ошибка соединения")
    return "Успешно!"
```

---

## 4. Встроенные декораторы Python

### @staticmethod

Метод, который не принимает ни экземпляр класса (self), ни сам класс (cls) в качестве первого аргумента.

```python
class MyClass:
    @staticmethod
    def static_method(x, y):
        return x + y

print(MyClass.static_method(5, 3))  # Работает без создания экземпляра
```

### @classmethod

Метод, который получает класс в качестве первого аргумента вместо экземпляра класса.

```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    
    @classmethod
    def from_birth_year(cls, name, birth_year):
        current_year = 2023
        age = current_year - birth_year
        return cls(name, age)

person = Person.from_birth_year("Иван", 1990)
print(f"{person.name}, возраст: {person.age}")
```

### @property

Позволяет определить метод как атрибут.

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius
    
    @property
    def radius(self):
        return self._radius
    
    @radius.setter
    def radius(self, value):
        if value <= 0:
            raise ValueError("Радиус должен быть положительным")
        self._radius = value
    
    @property
    def area(self):
        return 3.14159 * self._radius ** 2

circle = Circle(5)
print(circle.area)  # Вызывает метод area как атрибут
circle.radius = 10  # Использует setter
```

---

## 5. Примеры использования

### Декоратор для проверки аутентификации

```python
def requires_auth(func):
    def wrapper(*args, **kwargs):
        # Здесь могла бы быть проверка аутентификации
        user_authenticated = True  # Упрощение для примера
        if not user_authenticated:
            raise PermissionError("Требуется аутентификация")
        return func(*args, **kwargs)
    return wrapper

@requires_auth
def sensitive_operation():
    return "Операция выполнена"

print(sensitive_operation())
```

### Декоратор для проверки типов аргументов

```python
def type_check(*expected_types):
    def decorator(func):
        def wrapper(*args, **kwargs):
            for arg, expected_type in zip(args, expected_types):
                if not isinstance(arg, expected_type):
                    raise TypeError(f"Аргумент {arg} должен быть типа {expected_type.__name__}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@type_check(int, int)
def multiply(a, b):
    return a * b

print(multiply(5, 3))  # Работает
# print(multiply("5", 3))  # Вызовет TypeError
```

---

## 6. Функциональное программирование и декораторы

### Декораторы как функции высшего порядка

Декораторы являются примером функций высшего порядка - функций, которые принимают другие функции в качестве аргументов или возвращают их.

```python
def compose(f, g):
    """Композиция двух функций"""
    def composed(*args, **kwargs):
        return f(g(*args, **kwargs))
    return composed

def add_ten(x):
    return x + 10

def multiply_by_two(x):
    return x * 2

# Создаем композицию: сначала умножаем на 2, потом прибавляем 10
combined = compose(add_ten, multiply_by_two)
print(combined(5))  # (5 * 2) + 10 = 20
```

### Декоратор для мемоизации

```python
from functools import wraps

def memoize(func):
    cache = {}
    
    @wraps(func)
    def wrapper(*args):
        if args in cache:
            return cache[args]
        result = func(*args)
        cache[args] = result
        return result
    
    return wrapper

@memoize
def expensive_calculation(n):
    """Дорогостоящая операция"""
    print(f"Выполняем дорогостоящее вычисление для {n}")
    return sum(i**2 for i in range(n))

print(expensive_calculation(1000))  # Выполняется
print(expensive_calculation(1000))  # Возвращается из кэша
```

---

## Заключение

Декораторы - мощный инструмент Python, который позволяет изменять поведение функций и классов без изменения их кода. Они широко используются в фреймворках, для логирования, кэширования, проверки аутентификации и многих других задач.

## Контрольные вопросы:
1. Что такое декоратор в Python?
2. Как создать декоратор с параметрами?
3. Какие встроенные декораторы есть в Python?
4. В чем заключается преимущество использования декораторов?
5. Как работает функция wraps из модуля functools?
