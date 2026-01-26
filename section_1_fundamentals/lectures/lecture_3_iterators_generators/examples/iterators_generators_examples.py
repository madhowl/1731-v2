# Примеры итераторов и генераторов в Python

"""
Этот файл содержит примеры использования итераторов и генераторов в Python,
включая создание пользовательских итераторов и генераторов, а также их применение.
"""

# 1. Пользовательские итераторы
class CountdownIterator:
    """
    Итератор, который возвращает числа в обратном порядке от n до 0
    """
    def __init__(self, n):
        self.n = n
        self.current = n
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current >= 0:
            result = self.current
            self.current -= 1
            return result
        else:
            raise StopIteration

# Пример использования CountdownIterator
print("=== Countdown Iterator ===")
countdown = CountdownIterator(5)
for num in countdown:
    print(num, end=" ")
print("\n")

class SquareIterator:
    """
    Итератор, который возвращает квадраты чисел в заданном диапазоне
    """
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.current = start
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.current < self.end:
            result = self.current ** 2
            self.current += 1
            return result
        else:
            raise StopIteration

# Пример использования SquareIterator
print("=== Square Iterator ===")
squares = SquareIterator(1, 6)
for square in squares:
    print(square, end=" ")
print("\n")

# 2. Пользовательские генераторы
def countdown_generator(n):
    """
    Генератор, который возвращает числа в обратном порядке от n до 0
    """
    while n >= 0:
        yield n
        n -= 1

print("=== Countdown Generator ===")
for num in countdown_generator(5):
    print(num, end=" ")
print("\n")

def fibonacci_generator(max_count):
    """
    Генератор чисел Фибоначчи
    """
    count = 0
    a, b = 0, 1
    while count < max_count:
        yield a
        a, b = b, a + b
        count += 1

print("=== Fibonacci Generator ===")
fib = fibonacci_generator(10)
for num in fib:
    print(num, end=" ")
print("\n")

def file_line_generator(file_path):
    """
    Генератор, который построчно читает файл
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                yield line.rstrip('\n')
    except FileNotFoundError:
        print(f"Файл {file_path} не найден")
        yield from []  # Возвращает пустой генератор

# 3. Выражения-генераторы
def generator_expressions_demo():
    """
    Демонстрация выражений-генераторов
    """
    print("=== Generator Expressions ===")
    
    # Простое выражение-генератор
    squares_gen = (x**2 for x in range(1, 6))
    print("Квадраты чисел от 1 до 5:")
    for square in squares_gen:
        print(square, end=" ")
    print()
    
    # Фильтрация с помощью выражения-генератора
    even_squares = (x**2 for x in range(1, 11) if x % 2 == 0)
    print("Квадраты четных чисел от 1 до 10:")
    for square in even_squares:
        print(square, end=" ")
    print()
    
    # Сравнение с списковым включением
    import sys
    list_comp = [x**2 for x in range(1000)]
    gen_expr = (x**2 for x in range(1000))
    
    print(f"Размер списка: {sys.getsizeof(list_comp)} байт")
    print(f"Размер генератора: {sys.getsizeof(gen_expr)} байт")
    print()

generator_expressions_demo()

# 4. Продвинутые примеры генераторов
def prime_generator(max_num):
    """
    Генератор простых чисел до max_num
    """
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(n**0.5) + 1):
            if n % i == 0:
                return False
        return True
    
    for num in range(2, max_num + 1):
        if is_prime(num):
            yield num

print("=== Prime Generator ===")
primes = prime_generator(20)
for prime in primes:
    print(prime, end=" ")
print("\n")

def data_processing_pipeline(data_source):
    """
    Пример конвейера обработки данных с использованием генераторов
    """
    # Этап 1: фильтрация
    def filter_positive(numbers):
        for num in numbers:
            if num > 0:
                yield num
    
    # Этап 2: преобразование
    def square_numbers(numbers):
        for num in numbers:
            yield num ** 2
    
    # Этап 3: фильтрация по условию
    def filter_greater_than_threshold(numbers, threshold):
        for num in numbers:
            if num > threshold:
                yield num
    
    # Создание конвейера
    filtered_data = filter_positive(data_source)
    squared_data = square_numbers(filtered_data)
    result = list(filter_greater_than_threshold(squared_data, 10))
    
    return result

print("=== Data Processing Pipeline ===")
data = [-3, -1, 0, 1, 2, 3, 4, 5]
processed_data = data_processing_pipeline(data)
print(f"Исходные данные: {data}")
print(f"Обработанные данные (положительные, возведенные в квадрат, > 10): {processed_data}")
print()

# 5. Генераторы с отправкой значений (coroutines)
def accumulator():
    """
    Генератор-корутина, которая накапливает значения
    """
    total = 0
    while True:
        value = yield total
        if value is not None:
            total += value

print("=== Accumulator Generator ===")
acc = accumulator()
next(acc)  # Инициализация генератора
print(f"Начальное значение: {acc.send(10)}")
print(f"После добавления 5: {acc.send(5)}")
print(f"После добавления -3: {acc.send(-3)}")
print(f"После добавления 8: {acc.send(8)}")
print()

# 6. Декоратор для создания генератора с кэшированием
from functools import wraps

def cached_generator(func):
    """
    Декоратор, который кэширует значения генератора
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        cache = []
        gen = func(*args, **kwargs)
        
        def cached_iter():
            for i, value in enumerate(gen):
                cache.append(value)
                yield value
            
            # После исчерпания генератора, возвращаем значения из кэша
            while True:
                for value in cache:
                    yield value
        
        return cached_iter()
    return wrapper

@cached_generator
def simple_sequence(n):
    """Простая последовательность чисел"""
    for i in range(n):
        print(f"Генерируем {i}")  # Печатаем для демонстрации
        yield i

print("=== Cached Generator ===")
seq = simple_sequence(3)
print("Первый проход:")
for i, value in enumerate(seq):
    if i >= 5:  # Ограничиваем количество итераций для демонстрации
        break
    print(value)

print("Второй проход (из кэша):")
for i, value in enumerate(seq):
    if i >= 5:  # Ограничиваем количество итераций для демонстрации
        break
    print(value)
print()

# 7. Примеры использования itertools
import itertools
import operator

def itertools_examples():
    """
    Примеры использования модуля itertools
    """
    print("=== Itertools Examples ===")
    
    # count() - бесконечный итератор чисел
    print("Count iterator (first 5 values):")
    counter = itertools.count(start=10, step=2)
    for i, value in enumerate(counter):
        if i >= 5:
            break
        print(value, end=" ")
    print()
    
    # cycle() - циклический итератор
    print("Cycle iterator (first 8 values):")
    cycler = itertools.cycle(['A', 'B', 'C'])
    for i, value in enumerate(cycler):
        if i >= 8:
            break
        print(value, end=" ")
    print()
    
    # repeat() - повторяет значение
    print("Repeat iterator:")
    repeater = itertools.repeat('Python', 5)
    for value in repeater:
        print(value, end=" ")
    print()
    
    # chain() - объединяет несколько итераторов
    print("Chain iterator:")
    chained = itertools.chain([1, 2, 3], ['a', 'b', 'c'], (4, 5))
    for value in chained:
        print(value, end=" ")
    print()
    
    # compress() - фильтрует элементы по маске
    print("Compress iterator:")
    data = ['A', 'B', 'C', 'D']
    selectors = [True, False, True, False]
    compressed = itertools.compress(data, selectors)
    for value in compressed:
        print(value, end=" ")
    print()
    
    # dropwhile() - пропускает элементы, пока условие истинно
    print("Dropwhile iterator:")
    data = [1, 2, 3, 4, 5, 1, 2]
    dropped = itertools.dropwhile(lambda x: x < 4, data)
    for value in dropped:
        print(value, end=" ")
    print()
    
    # takewhile() - берет элементы, пока условие истинно
    print("Takewhile iterator:")
    taken = itertools.takewhile(lambda x: x < 4, data)
    for value in taken:
        print(value, end=" ")
    print()
    
    # filterfalse() - противоположность filter
    print("Filterfalse iterator:")
    filtered = itertools.filterfalse(lambda x: x % 2 == 0, range(10))
    for value in filtered:
        print(value, end=" ")
    print()
    
    # accumulate() - накапливает значения
    print("Accumulate iterator:")
    accumulated = itertools.accumulate([1, 2, 3, 4, 5], operator.mul)
    for value in accumulated:
        print(value, end=" ")
    print()
    
    # groupby() - группировка по ключу
    print("Groupby iterator:")
    data = [('a', 1), ('a', 2), ('b', 3), ('b', 4), ('c', 5)]
    for key, group in itertools.groupby(data, key=lambda x: x[0]):
        print(f"Key: {key}, Group: {list(group)}")
    
    print()

itertools_examples()

# 8. Примеры генераторов для обработки данных
def process_large_dataset():
    """
    Пример обработки большого набора данных с помощью генераторов
    """
    print("=== Processing Large Dataset ===")
    
    # Генератор данных (имитация большого набора данных)
    def data_generator(size):
        for i in range(size):
            yield {
                'id': i,
                'value': i * 2,
                'category': 'A' if i % 2 == 0 else 'B'
            }
    
    # Фильтр данных
    def filter_by_category(dataset, category):
        for item in dataset:
            if item['category'] == category:
                yield item
    
    # Преобразование данных
    def transform_data(dataset):
        for item in dataset:
            item['processed'] = True
            item['squared_value'] = item['value'] ** 2
            yield item
    
    # Использование конвейера
    raw_data = data_generator(10)  # Имитация большого набора данных
    filtered_data = filter_by_category(raw_data, 'A')
    processed_data = transform_data(filtered_data)
    
    # Вывод результата
    for item in processed_data:
        print(item)
    print()

process_large_dataset()

# 9. Генераторы для работы с файлами
def process_log_file(file_path):
    """
    Обработка лог-файла с помощью генераторов
    """
    print("=== Processing Log File ===")
    
    def log_line_generator(path):
        """Генератор строк лога"""
        with open(path, 'r') as file:
            for line in file:
                yield line.strip()
    
    def error_filter(log_lines):
        """Фильтр строк с ошибками"""
        for line in log_lines:
            if "ERROR" in line.upper():
                yield line
    
    def extract_timestamps(error_lines):
        """Извлечение временных меток из строк ошибок"""
        for line in error_lines:
            # Извлекаем временную метку (предполагаем формат: [TIMESTAMP] MESSAGE)
            if "[" in line and "]" in line:
                timestamp = line.split("[")[1].split("]")[0]
                yield (timestamp, line)
    
    # Создаем тестовый лог-файл
    test_log_content = """[2023-01-01 10:00:00] INFO: Application started
[2023-01-01 10:01:00] ERROR: Connection failed
[2023-01-01 10:02:00] WARNING: Low disk space
[2023-01-01 10:03:00] ERROR: Database connection lost
[2023-01-01 10:04:00] INFO: Retrying connection"""
    
    with open("test.log", "w") as f:
        f.write(test_log_content)
    
    # Обработка лога
    log_gen = log_line_generator("test.log")
    error_gen = error_filter(log_gen)
    timestamp_gen = extract_timestamps(error_gen)
    
    for timestamp, error_line in timestamp_gen:
        print(f"Timestamp: {timestamp}, Error: {error_line}")
    
    # Удаляем тестовый файл
    import os
    os.remove("test.log")
    print()

# 10. Примеры использования генераторов в реальных задачах
def real_world_examples():
    """
    Примеры использования генераторов в реальных задачах
    """
    print("=== Real World Examples ===")
    
    # Генератор для чтения CSV-файла
    def csv_reader(file_path, delimiter=','):
        """Генератор для чтения CSV-файла по строкам"""
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                yield line.strip().split(delimiter)
    
    # Генератор для обработки потока данных
    def data_batcher(data_stream, batch_size=3):
        """Группирует данные в батчи"""
        batch = []
        for item in data_stream:
            batch.append(item)
            if len(batch) == batch_size:
                yield batch
                batch = []
        
        # Возвращаем оставшиеся элементы
        if batch:
            yield batch
    
    # Создаем тестовый CSV
    csv_content = """name,age,city
Иван,30,Москва
Мария,25,СПб
Алексей,35,Новосибирск
Елена,28,Екатеринбург
Дмитрий,32,Казань"""
    
    with open("test.csv", "w", encoding="utf-8") as f:
        f.write(csv_content)
    
    # Чтение и обработка CSV
    print("Обработка CSV в батчах:")
    csv_gen = csv_reader("test.csv")
    next(csv_gen)  # Пропускаем заголовок
    
    for batch in data_batcher(csv_gen, 2):
        print(f"Батч: {batch}")
    
    # Удаляем тестовый файл
    os.remove("test.csv")
    print()

real_world_examples()

# 11. Примеры использования yield from
def generator_delegation_example():
    """
    Пример использования yield from для делегирования генераторов
    """
    print("=== Yield From Example ===")
    
    def sub_generator(start, end):
        for i in range(start, end):
            yield i
    
    def main_generator():
        yield from sub_generator(1, 4)
        yield from sub_generator(10, 13)
        yield from sub_generator(100, 102)
    
    for value in main_generator():
        print(value, end=" ")
    print("\n")

generator_delegation_example()

# 12. Заключение: когда использовать итераторы и генераторы
def when_to_use_iterators_generators():
    """
    Рекомендации по использованию итераторов и генераторов
    """
    print("=== Когда использовать итераторы и генераторы ===")
    
    recommendations = [
        "1. Используйте генераторы для обработки больших объемов данных",
        "2. Генераторы экономят память по сравнению с созданиями списков",
        "3. Итераторы полезны для последовательного доступа к данным",
        "4. Генераторы подходят для создания конвейеров обработки данных",
        "5. Выражения-генераторы хороши для простых преобразований",
        "6. Генераторы удобны для работы с потоками данных"
    ]
    
    for rec in recommendations:
        print(rec)

when_to_use_iterators_generators()
