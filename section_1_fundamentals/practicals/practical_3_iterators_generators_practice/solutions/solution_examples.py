# Решения для практического занятия 3: Работа с итераторами и генераторами

# Решение задания 1: Создайте итератор для чисел Фибоначчи
class FibonacciIterator:
    """Итератор для последовательности чисел Фибоначчи"""
    def __init__(self, max_count):
        self.max_count = max_count
        self.count = 0
        self.current = 0
        self.next_val = 1
    
    def __iter__(self):
        return self
    
    def __next__(self):
        if self.count >= self.max_count:
            raise StopIteration
        
        result = self.current
        self.current, self.next_val = self.next_val, self.current + self.next_val
        self.count += 1
        return result

# Решение задания 2: Создайте генератор для чисел Фибоначчи
def fibonacci_generator(max_count):
    """Генератор для последовательности чисел Фибоначчи"""
    count = 0
    current, next_val = 0, 1
    
    while count < max_count:
        yield current
        current, next_val = next_val, current + next_val
        count += 1

# Решение задания 3: Создайте генератор для четных чисел
def even_numbers_generator(start, end):
    """Генератор четных чисел в диапазоне от start до end"""
    for num in range(start, end + 1):
        if num % 2 == 0:
            yield num

# Решение задания 4: Создайте итератор для бесконечной последовательности
class InfiniteCounter:
    """Итератор, который считает до бесконечности, начиная с заданного числа"""
    def __init__(self, start=0, step=1):
        self.current = start
        self.step = step
    
    def __iter__(self):
        return self
    
    def __next__(self):
        result = self.current
        self.current += self.step
        return result

# Решение задания 5: Генератор для фильтрации последовательности
def filter_generator(iterable, predicate):
    """Генератор, применяющий фильтр к последовательности"""
    for item in iterable:
        if predicate(item):
            yield item

# Дополнительные примеры решений

# Пример использования itertools
import itertools

def get_combinations(items, r):
    """Получить все комбинации элементов длиной r"""
    return list(itertools.combinations(items, r))

def get_permutations(items, r):
    """Получить все перестановки элементов длиной r"""
    return list(itertools.permutations(items, r))

def take_first_n(iterator, n):
    """Взять первые n элементов из итератора"""
    return list(itertools.islice(iterator, n))

# Примеры использования:
if __name__ == "__main__":
    print("=== Решения для практического занятия 3 ===")
    
    # Пример использования итератора
    print("\n1. Итератор Фибоначчи:")
    fib_iter = FibonacciIterator(10)
    fib_sequence = [num for num in fib_iter]
    print(fib_sequence)
    
    # Пример использования генератора
    print("\n2. Генератор Фибоначчи:")
    fib_gen = list(fibonacci_generator(10))
    print(fib_gen)
    
    # Пример использования генератора четных чисел
    print("\n3. Четные числа от 0 до 20:")
    even_nums = list(even_numbers_generator(0, 20))
    print(even_nums)
    
    # Пример использования фильтрующего генератора
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    even_nums_filtered = list(filter_generator(numbers, lambda x: x % 2 == 0))
    print(f"\n4. Четные числа из списка {numbers}: {even_nums_filtered}")
    
    # Примеры с itertools
    items = ['a', 'b', 'c']
    print(f"\n5. Комбинации из {items}: {get_combinations(items, 2)}")
    print(f"6. Перестановки из {items}: {get_permutations(items, 2)}")
    
    # Пример бесконечного итератора
    print("\n7. Первые 5 значений бесконечного счетчика:")
    infinite_counter = InfiniteCounter(start=10, step=3)
    first_five = take_first_n(infinite_counter, 5)
    print(first_five)