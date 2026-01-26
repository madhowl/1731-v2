# Упражнения для практического занятия 3: Работа с итераторами и генераторами

# Задание 1: Создайте итератор для чисел Фибоначчи
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

# Задание 2: Создайте генератор для чисел Фибоначчи
def fibonacci_generator(max_count):
    """Генератор для последовательности чисел Фибоначчи"""
    count = 0
    current, next_val = 0, 1
    
    while count < max_count:
        yield current
        current, next_val = next_val, current + next_val
        count += 1

# Задание 3: Создайте генератор для четных чисел
def even_numbers_generator(start, end):
    """Генератор четных чисел в диапазоне от start до end"""
    for num in range(start, end + 1):
        if num % 2 == 0:
            yield num

# Задание 4: Создайте итератор для бесконечной последовательности
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

# Задание 5: Генератор для фильтрации последовательности
def filter_generator(iterable, predicate):
    """Генератор, применяющий фильтр к последовательности"""
    for item in iterable:
        if predicate(item):
            yield item

# Примеры использования:
if __name__ == "__main__":
    # Пример использования итератора
    print("Итератор Фибоначчи:")
    fib_iter = FibonacciIterator(10)
    for num in fib_iter:
        print(num, end=" ")
    print()
    
    # Пример использования генератора
    print("Генератор Фибоначчи:")
    for num in fibonacci_generator(10):
        print(num, end=" ")
    print()
    
    # Пример использования генератора четных чисел
    print("Четные числа от 0 до 20:")
    for num in even_numbers_generator(0, 20):
        print(num, end=" ")
    print()
    
    # Пример использования фильтрующего генератора
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    even_nums = list(filter_generator(numbers, lambda x: x % 2 == 0))
    print(f"Четные числа из списка {numbers}: {even_nums}")