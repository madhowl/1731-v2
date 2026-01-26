# Лекция 3: Итераторы и генераторы

## Протокол итератора, генераторы, выражения-генераторы

### План лекции:
1. Понятие итераторов
2. Протокол итератора
3. Создание итераторов
4. Генераторы
5. Выражения-генераторы
6. Применение итераторов и генераторов

---

## 1. Понятие итераторов

### Что такое итератор?

Итератор - это объект, который позволяет последовательно перебирать элементы коллекции или последовательности. В Python итераторы реализуют протокол итератора, который включает два метода: `__iter__()` и `__next__()`.

### Примеры встроенных итераторов:

```python
# Список - итерируемый объект
my_list = [1, 2, 3, 4, 5]

# Получаем итератор из списка
iterator = iter(my_list)

# Используем итератор
print(next(iterator))  # 1
print(next(iterator))  # 2
print(next(iterator))  # 3

# Или используем цикл for (внутри используется итератор)
for item in my_list:
    print(item)
```

### Итерируемые объекты в Python:

- Списки (`list`)
- Кортежи (`tuple`)
- Словари (`dict`)
- Множества (`set`)
- Строки (`str`)
- Файлы
- И многие другие

---

## 2. Протокол итератора

### Методы итератора

Каждый итератор должен реализовывать два метода:

1. `__iter__()` - возвращает сам объект итератора
2. `__next__()` - возвращает следующий элемент последовательности

Когда элементы заканчиваются, метод `__next__()` должен вызвать исключение `StopIteration`.

### Пример реализации протокола итератора:

```python
class CountDown:
    def __init__(self, start):
        self.start = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.start <= 0:
            raise StopIteration
        self.start -= 1
        return self.start + 1

# Использование
count_down = CountDown(5)
for num in count_down:
    print(num)  # Выведет: 5, 4, 3, 2, 1
```

---

## 3. Создание итераторов

### Пользовательские итераторы

```python
class Squares:
    """Итератор, возвращающий квадраты чисел"""
    def __init__(self, max_value):
        self.max_value = max_value
        self.current = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current >= self.max_value:
            raise StopIteration
        result = self.current ** 2
        self.current += 1
        return result

# Использование
squares = Squares(5)
for square in squares:
    print(square)  # 0, 1, 4, 9, 16
```

### Использование itertools для создания итераторов

```python
import itertools

# Бесконечный счетчик
counter = itertools.count(start=10, step=2)
print([next(counter) for _ in range(5)])  # [10, 12, 14, 16, 18]

# Циклический итератор
cycler = itertools.cycle(['A', 'B', 'C'])
print([next(cycler) for _ in range(7)])  # ['A', 'B', 'C', 'A', 'B', 'C', 'A']

# Повторяющийся элемент
repeater = itertools.repeat('Hello', 3)
print(list(repeater))  # ['Hello', 'Hello', 'Hello']
```

---

## 4. Генераторы

### Что такое генераторы?

Генераторы - это особый тип функций, которые возвращают итератор. Вместо `return`, генераторы используют ключевое слово `yield`. При вызове `yield` функция приостанавливается и сохраняет своё состояние.

### Простой генератор:

```python
def simple_generator():
    yield 1
    yield 2
    yield 3

# Использование
gen = simple_generator()
for value in gen:
    print(value)  # 1, 2, 3
```

### Генератор чисел Фибоначчи:

```python
def fibonacci_generator(n):
    """Генерирует n чисел Фибоначчи"""
    a, b = 0, 1
    count = 0
    while count < n:
        yield a
        a, b = b, a + b
        count += 1

# Использование
fib = fibonacci_generator(10)
print(list(fib))  # [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

### Генератор с отправкой значений:

```python
def echo_generator():
    """Генератор, который эхо-ответы"""
    while True:
        received = yield
        yield f"Вы сказали: {received}"

# Использование
gen = echo_generator()
next(gen)  # Запускаем генератор
print(gen.send("Привет"))  # Вы сказали: Привет
next(gen)  # Продолжаем
print(gen.send("Как дела?"))  # Вы сказали: Как дела?
```

---

## 5. Выражения-генераторы

### Создание генераторов с помощью выражений

Выражения-генераторы похожи на списковые включения, но используют круглые скобки и возвращают генератор, а не список.

```python
# Списковое включение (создает сразу весь список в памяти)
squares_list = [x**2 for x in range(10)]
print(squares_list)  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]

# Выражение-генератор (создает объект-генератор)
squares_gen = (x**2 for x in range(10))
print(type(squares_gen))  # <class 'generator'>

# Используем генератор
for square in squares_gen:
    print(square)  # 0, 1, 4, 9, 16, 25, 36, 49, 64, 81
```

### Преимущества выражений-генераторов:

```python
import sys

# Сравнение использования памяти
list_comp = [x for x in range(1000000)]
gen_exp = (x for x in range(1000000))

print(sys.getsizeof(list_comp))  # Большой размер
print(sys.getsizeof(gen_exp))    # Маленький размер
```

### Сложные выражения-генераторы:

```python
# Фильтрация и преобразование
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
even_squares = (x**2 for x in numbers if x % 2 == 0)
print(list(even_squares))  # [4, 16, 36, 64, 100]

# Генератор из генератора
nested_lists = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flattened = (item for sublist in nested_lists for item in sublist)
print(list(flattened))  # [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

---

## 6. Применение итераторов и генераторов

### Пример: обработка больших файлов

```python
def read_large_file(file_path):
    """Генератор для построчного чтения большого файла"""
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            yield line.strip()

# Использование
# for line in read_large_file('large_file.txt'):
#     process(line)
```

### Пример: бесконечный генератор данных

```python
import random
import time

def sensor_data_generator():
    """Симуляция генерации данных с датчика"""
    while True:
        yield {
            'timestamp': time.time(),
            'temperature': round(random.uniform(18.0, 25.0), 2),
            'humidity': round(random.uniform(40.0, 60.0), 2)
        }

# Использование первых 5 значений
sensor_gen = sensor_data_generator()
for i, data in enumerate(sensor_gen):
    if i >= 5:
        break
    print(data)
```

### Пример: конвейер обработки данных

```python
def numbers():
    """Генератор чисел"""
    for i in range(1, 11):
        yield i

def evens(source):
    """Фильтр четных чисел"""
    for num in source:
        if num % 2 == 0:
            yield num

def squared(source):
    """Возведение в квадрат"""
    for num in source:
        yield num ** 2

# Конвейер: числа -> четные -> квадраты
pipeline = squared(evens(numbers()))
print(list(pipeline))  # [4, 16, 36, 64, 100]
```

---

## Заключение

Итераторы и генераторы - важные концепции в Python, которые позволяют эффективно обрабатывать данные, особенно большие наборы. Они обеспечивают ленивые вычисления, экономию памяти и гибкость при работе с последовательностями.

## Контрольные вопросы:
1. В чем разница между итерируемым объектом и итератором?
2. Какие методы должен реализовывать итератор?
3. Что такое генератор и в чем его преимущество?
4. Как работает ключевое слово yield?
5. В чем разница между списковыми включениями и выражениями-генераторами?
