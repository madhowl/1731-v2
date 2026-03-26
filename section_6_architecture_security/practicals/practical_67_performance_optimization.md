# Практическое занятие 67: Оптимизация производительности

## Профилирование, оптимизация кэширования, асинхронное программирование

### Цель занятия:
Изучить методы оптимизации производительности, освоить профилирование и кэширование, научиться писать эффективный код.

### Задачи:
1. Понять основы оптимизации
2. Освоить профилирование
3. Научиться использовать кэширование

### План работы:
1. Профилирование
2. Кэширование
3. Асинхронное программирование
4. Практические задания

---

## 1. Профилирование

### Пример 1: Профилирование с cProfile

```python
import cProfile
import pstats
import io
from functools import wraps

def profile(func):
    """Декоратор для профилирования функции"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        
        result = func(*args, **kwargs)
        
        profiler.disable()
        
        # Вывод статистики
        s = io.StringIO()
        ps = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
        ps.print_stats(10)
        
        print(s.getvalue())
        
        return result
    return wrapper

@profile
def slow_function():
    """Пример медленной функции"""
    result = 0
    for i in range(100000):
        result += i ** 2
    return result

# Запуск
result = slow_function()
print(f"Result: {result}")
```

### Пример 2: Кэширование

```python
from functools import lru_cache
import time

class Cache:
    """Простой кэш"""
    
    def __init__(self, max_size: int = 100):
        self.cache = {}
        self.max_size = max_size
    
    def get(self, key: str):
        return self.cache.get(key)
    
    def set(self, key: str, value):
        if len(self.cache) >= self.max_size:
            # Удаление первого элемента
            first_key = next(iter(self.cache))
            del self.cache[first_key]
        
        self.cache[key] = value
    
    def clear(self):
        self.cache.clear()

# Использование lru_cache
@lru_cache(maxsize=128)
def expensive_operation(n: int) -> int:
    """Дорогостоящая операция с кэшированием"""
    time.sleep(0.1)  # Симуляция задержки
    return n ** 2

# Первый вызов - медленный
print(expensive_operation(100))

# Второй вызов - быстрый (из кэша)
print(expensive_operation(100))
```

### Пример 3: Асинхронное программирование

```python
import asyncio

async def fetch_data(url: str) -> dict:
    """Асинхронное получение данных"""
    await asyncio.sleep(1)  # Симуляция запроса
    return {'url': url, 'data': 'some data'}

async def main():
    """Основная асинхронная функция"""
    # Последовательное выполнение
    start = time.time()
    
    # Параллельное выполнение
    tasks = [
        fetch_data('http://example.com/1'),
        fetch_data('http://example.com/2'),
        fetch_data('http://example.com/3'),
    ]
    
    results = await asyncio.gather(*tasks)
    
    elapsed = time.time() - start
    print(f"Elapsed: {elapsed:.2f}s")  # ~1s вместо ~3s
    
    return results

# Запуск
results = asyncio.run(main())
```

---

## 2. Практические задания

### Задание 1: Профилирование

Найдите узкие места в вашем коде с помощью профилирования.

### Задание 2: Кэширование

Добавьте кэширование к часто используемым функциям.

### Задание 3: Async

Перепишите синхронный код на асинхронный.

---

## Контрольные вопросы:

1. Как профилировать код на Python?
2. Что такое lru_cache?
3. Как использовать asyncio?
