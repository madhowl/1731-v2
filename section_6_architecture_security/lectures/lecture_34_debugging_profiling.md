# Лекция 34: Отладка и профилирование

## Методы и инструменты для поиска ошибок и оптимизации производительности

### Цель лекции:
- Изучить техники отладки Python-приложений
- Освоить инструменты профилирования кода
- Научиться анализировать производительность
- Познакомиться с лучшими практиками оптимизации

### План лекции:
1. Методы отладки кода
2. Отладчик pdb и его расширения
3. Логирование для отладки
4. Профилирование кода
5. Анализ памяти
6. Оптимизация производительности

---

## 1. Методы отладки кода

### Print-отладка (базовый уровень):

```python
# ❌ Плохо: много print для отладки
def calculate_total(items):
    print(f"Items: {items}")
    total = 0
    for item in items:
        print(f"Processing item: {item}")
        total += item['price']
        print(f"Current total: {total}")
    print(f"Final total: {total}")
    return total

# ✅ Лучше: условная отладка
DEBUG = True

def calculate_total(items):
    if DEBUG:
        print(f"[DEBUG] Items count: {len(items)}")
    
    total = 0
    for item in items:
        total += item['price']
    
    if DEBUG:
        print(f"[DEBUG] Total: {total}")
    return total

# ✅ Хорошо: использование logging
import logging

logger = logging.getLogger(__name__)

def calculate_total(items):
    logger.debug(f"Processing {len(items)} items")
    total = sum(item['price'] for item in items)
    logger.info(f"Calculated total: {total}")
    return total
```

### Утверждения (assertions):

```python
def divide(a, b):
    assert b != 0, "Division by zero"
    return a / b

def process_user_data(data):
    assert isinstance(data, dict), "Data must be a dictionary"
    assert 'name' in data, "Name is required"
    assert 'email' in data, "Email is required"
    assert '@' in data['email'], "Invalid email format"
    
    return {
        'name': data['name'].strip(),
        'email': data['email'].lower()
    }

# Отключение assert в production
# python -O script.py (оптимизированный режим)
```

### Обработка исключений для отладки:

```python
import traceback
import logging

logger = logging.getLogger(__name__)

def risky_operation():
    try:
        # Код, который может вызвать ошибку
        result = 10 / 0
    except ZeroDivisionError as e:
        logger.error(f"Division error: {e}")
        logger.debug(traceback.format_exc())
        raise
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
        raise

# Контекстный менеджер для логирования исключений
from contextlib import contextmanager

@contextmanager
def debug_context(operation_name):
    logger.info(f"Starting: {operation_name}")
    try:
        yield
        logger.info(f"Completed: {operation_name}")
    except Exception as e:
        logger.error(f"Failed: {operation_name} - {e}")
        logger.debug(traceback.format_exc())
        raise

# Использование
with debug_context("database_query"):
    result = db.query("SELECT * FROM users")
```

---

## 2. Отладчик pdb и его расширения

### Основы pdb:

```python
import pdb

def buggy_function(x, y):
    result = x + y
    pdb.set_trace()  # Точка останова
    result = result * 2
    return result

# Запуск
# python script.py
# В точке останова:
# (Pdb) help          # Показать помощь
# (Pdb) n             # Next строка
# (Pdb) s             # Step into функцию
# (Pdb) c             # Continue выполнение
# (Pdb) l             # List код
# (Pdb) p variable    # Print переменную
# (Pdb) pp variable   # Pretty print
# (Pdb) w             # Where (stack trace)
# (Pdb) q             # Quit
```

### Команды pdb:

```
Навигация:
  n (next)          - Следующая строка в текущей функции
  s (step)          - Войти в функцию
  c (continue)      - Продолжить до следующей точки останова
  r (return)        - Продолжить до возврата из функции
  w (where)         - Показать стек вызовов

Просмотр:
  l (list)          - Показать код вокруг текущей строки
  ll (longlist)     - Показать всю функцию
  a (args)          - Показать аргументы функции
  p expr            - Выразить и напечатать выражение
  pp expr           - Pretty print выражение

Точки останова:
  b line            - Установить точку останова
  b function        - Точка останова в начале функции
  cl                - Очистить все точки останова
  disable/enable    - Отключить/включить точку останова

Прочее:
  h (help)          - Показать помощь
  q (quit)          - Выйти из отладчика
  !command          - Выполнить Python команду
```

### pdbpp (улучшенная версия):

```bash
pip install pdbpp
```

```python
# Автоматическая точка останова при ошибке
import pdb

def main():
    x = 1
    y = 0
    return x / y

if __name__ == '__main__':
    try:
        main()
    except Exception:
        pdb.post_mortem()  # Отладка после исключения

#或使用
# python -m pdb script.py
```

### breakpoint() в Python 3.7+:

```python
def calculate(x, y):
    result = x + y
    breakpoint()  # Встроенная функция (Python 3.7+)
    return result * 2

# Переменная окружения для отключения
# PYTHONBREAKPOINT=0 python script.py
```

### Отладка в IDE:

```python
# PyCharm / VS Code:
# - Установить точку останова кликом
# - F9: Toggle breakpoint
# - F5: Start debugging
# - F10: Step over
# - F11: Step into
# - Shift+F11: Step out

# Условные точки останова
for i in range(1000):
    # Точка останова с условием: i == 500
    if i == 500:
        breakpoint()
    process(i)
```

---

## 3. Логирование для отладки

### Настройка логирования:

```python
import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging(level=logging.DEBUG):
    # Создание formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # File handler с ротацией
    os.makedirs('logs', exist_ok=True)
    file_handler = RotatingFileHandler(
        'logs/app.log',
        maxBytes=10*1024*1024,  # 10 MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    
    # Root logger
    logging.basicConfig(
        level=level,
        handlers=[console_handler, file_handler]
    )

# Использование
logger = logging.getLogger(__name__)

def process_data(data):
    logger.debug(f"Processing data: {data}")
    try:
        result = transform(data)
        logger.info(f"Transformed successfully: {result}")
        return result
    except Exception as e:
        logger.error(f"Transformation failed: {e}", exc_info=True)
        raise

# Разные уровни логирования
logger.debug("Подробная информация для отладки")
logger.info("Обычная информация о работе")
logger.warning("Предупреждение о потенциальной проблеме")
logger.error("Ошибка, но приложение продолжает работу")
logger.critical("Критическая ошибка, приложение может не работать")
```

### Структурированное логирование:

```python
import json
import logging

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        if record.exc_info:
            log_entry['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_entry)

# Настройка
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

# Использование с контекстом
from pythonjsonlogger import jsonlogger

logger = logging.getLogger(__name__)
logger.info("User action", extra={
    'user_id': 123,
    'action': 'login',
    'ip': '192.168.1.1'
})
```

---

## 4. Профилирование кода

### cProfile — встроенный профилировщик:

```python
import cProfile
import pstats
from pstats import SortKey

def slow_function():
    total = 0
    for i in range(1000000):
        total += i ** 2
    return total

def fast_function():
    return sum(i ** 2 for i in range(1000000))

def main():
    slow_function()
    fast_function()

# Программный запуск
profiler = cProfile.Profile()
profiler.enable()

main()

profiler.disable()

# Вывод статистики
stats = pstats.Stats(profiler)
stats.sort_stats(SortKey.TIME)
stats.print_stats(10)  # Топ 10 функций

# Сохранение в файл
stats.dump_stats('profile.stats')

# Запуск из командной строки:
# python -m cProfile -o profile.stats script.py
# python -m pstats profile.stats
```

### Визуализация профиля:

```bash
# Установка snakeviz
pip install snakeviz

# Просмотр в браузере
snakeviz profile.stats

# Или использование py-spy
pip install py-spy
py-spy record -o profile.svg -- python script.py
```

### line_profiler — построчное профилирование:

```bash
pip install line_profiler
```

```python
from line_profiler import LineProfiler

def slow_function():
    total = 0
    for i in range(1000000):
        total += i ** 2
    return total

def fast_function():
    return sum(i ** 2 for i in range(1000000))

# Создание профилировщика
lp = LineProfiler()
lp.add_function(slow_function)
lp.add_function(fast_function)

# Обертка функции
lp_wrapper = lp(slow_function)
lp_wrapper()

# Вывод результатов
lp.print_stats()

# Запуск из командной строки:
# kernprof -l -v script.py
```

### Пример использования line_profiler:

```python
# script.py
@profile  # Декоратор добавляется автоматически kernprof
def process_data():
    data = list(range(10000))
    result = []
    for item in data:
        if item % 2 == 0:
            result.append(item ** 2)
    return result

process_data()

# Запуск:
# kernprof -l -v script.py
```

### memory_profiler — профилирование памяти:

```bash
pip install memory_profiler
```

```python
from memory_profiler import profile

@profile
def memory_intensive():
    data = []
    for i in range(10000):
        data.append([0] * 1000)
    return data

memory_intensive()

# Запуск:
# python -m memory_profiler script.py
```

---

## 5. Анализ памяти

### tracemalloc — отслеживание выделения памяти:

```python
import tracemalloc

def find_memory_leak():
    data = []
    for i in range(1000):
        data.append([0] * 1000)
    return data

# Запуск tracemalloc
tracemalloc.start()

# Снимок памяти до
snapshot1 = tracemalloc.take_snapshot()

find_memory_leak()

# Снимок памяти после
snapshot2 = tracemalloc.take_snapshot()

# Сравнение
top_stats = snapshot2.compare_to(snapshot1, 'lineno')

print("Top 10 memory allocations:")
for stat in top_stats[:10]:
    print(stat)

# Детальная информация
for stat in top_stats[:5]:
    print(f"\n{stat}")
    for frame in stat.traceback:
        print(f"  {frame}")
```

### objgraph — поиск утечек памяти:

```bash
pip install objgraph
```

```python
import objgraph
import gc

# Показать наиболее распространенные типы
objgraph.show_most_common_types()

# Показать рост объектов
objgraph.show_growth()

# Найти ссылки на объект
class MyClass:
    pass

obj = MyClass()
objgraph.show_backrefs([obj], filename='backrefs.png')

# Найти циклические ссылки
gc.collect()
print(f"Uncollectable: {gc.garbage}")
```

### pympler — анализ памяти:

```bash
pip install pympler
```

```python
from pympler import asizeof, tracker, muppy

# Размер объекта
data = [1, 2, 3, 4, 5]
print(f"Size: {asizeof.asizeof(data)} bytes")

# Отслеживание изменений
tr = tracker.SummaryTracker()

data = list(range(1000))
del data

tr.print_diff()

# Все объекты
all_objects = muppy.get_objects()
summary = muppy.get_summary(all_objects)
muppy.print_summary(summary)
```

---

## 6. Оптимизация производительности

### Измерение времени выполнения:

```python
import timeit

# Измерение времени
def slow():
    return sum(i ** 2 for i in range(10000))

def fast():
    return sum(map(lambda x: x ** 2, range(10000)))

print(f"Slow: {timeit.timeit(slow, number=100)}")
print(f"Fast: {timeit.timeit(fast, number=100)}")

# Сравнение нескольких вариантов
setup = "import math"
stmt1 = "[x**2 for x in range(1000)]"
stmt2 = "list(map(lambda x: x**2, range(1000)))"
stmt3 = "[math.pow(x, 2) for x in range(1000)]"

print(f"List comp: {timeit.timeit(stmt1, setup=setup, number=1000)}")
print(f"Map: {timeit.timeit(stmt2, setup=setup, number=1000)}")
print(f"Math.pow: {timeit.timeit(stmt3, setup=setup, number=1000)}")
```

### Оптимизация с помощью кэширования:

```python
from functools import lru_cache

# Без кэширования
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

# С кэшированием
@lru_cache(maxsize=None)
def fibonacci_cached(n):
    if n < 2:
        return n
    return fibonacci_cached(n - 1) + fibonacci_cached(n - 2)

# Измерение
print(f"Without cache: {timeit.timeit(lambda: fibonacci(30), number=1)}")
print(f"With cache: {timeit.timeit(lambda: fibonacci_cached(30), number=1)}")
```

### Оптимизация циклов:

```python
# ❌ Плохо: медленный цикл
def process_items(items):
    result = []
    for item in items:
        result.append(item * 2)
    return result

# ✅ Хорошо: list comprehension
def process_items_fast(items):
    return [item * 2 for item in items]

# ✅ Лучше: map с built-in функцией
def process_items_faster(items):
    return list(map(lambda x: x * 2, items))

# ✅ Еще лучше: generator для больших данных
def process_items_generator(items):
    return (item * 2 for item in items)
```

### Использование встроенных функций:

```python
# ❌ Плохо
def find_max(items):
    max_val = items[0]
    for item in items:
        if item > max_val:
            max_val = item
    return max_val

# ✅ Хорошо
def find_max_builtin(items):
    return max(items)

# ❌ Плохо
def concatenate(strings):
    result = ""
    for s in strings:
        result += s
    return result

# ✅ Хорошо
def concatenate_join(strings):
    return ''.join(strings)
```

### Профилирование веб-приложений:

```python
from flask import Flask, g
import time
import logging

app = Flask(__name__)
logger = logging.getLogger(__name__)

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    if hasattr(g, 'start_time'):
        elapsed = time.time() - g.start_time
        logger.info(f"{request.method} {request.path} - {elapsed:.4f}s")
    return response

# Использование middleware для профилирования
class ProfilingMiddleware:
    def __init__(self, app):
        self.app = app
    
    def __call__(self, environ, start_response):
        start_time = time.time()
        
        def logging_start_response(status, headers, exc_info=None):
            elapsed = time.time() - start_time
            logger.info(f"Request took {elapsed:.4f}s")
            return start_response(status, headers, exc_info)
        
        return self.app(environ, logging_start_response)
```

---

## Заключение

Отладка и профилирование — критически важные навыки для разработчика. Правильное использование инструментов позволяет быстро находить ошибки и оптимизировать производительность приложений.

## Контрольные вопросы:

1. Какие команды pdb вы знаете?
2. В чем разница между cProfile и line_profiler?
3. Как найти утечку памяти в Python?
4. Какие уровни логирования существуют?
5. Как оптимизировать медленный код?

## Практическое задание:

1. Отладить код с ошибками используя pdb
2. Профилировать приложение с cProfile
3. Найти и устранить утечку памяти
4. Оптимизировать медленную функцию
5. Настроить структурированное логирование
