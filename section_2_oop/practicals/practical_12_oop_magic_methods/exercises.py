# Упражнения для практического занятия 12: ООП - магические методы

import functools
from typing import Union, Any

# Задание 1: Арифметические магические методы
class Vector2D:
    """Класс двумерного вектора"""
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __add__(self, other: 'Vector2D') -> 'Vector2D':
        """Сложение векторов"""
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'Vector2D') -> 'Vector2D':
        """Вычитание векторов"""
        return Vector2D(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar: Union[int, float]) -> 'Vector2D':
        """Скалярное умножение"""
        return Vector2D(self.x * scalar, self.y * scalar)
    
    def __rmul__(self, scalar: Union[int, float]) -> 'Vector2D':
        """Обратное скалярное умножение"""
        return self.__mul__(scalar)
    
    def __str__(self) -> str:
        """Строковое представление вектора"""
        return f"Vector2D({self.x}, {self.y})"
    
    def __repr__(self) -> str:
        """Официальное строковое представление вектора"""
        return f"Vector2D({self.x}, {self.y})"
    
    def __eq__(self, other: 'Vector2D') -> bool:
        """Сравнение векторов на равенство"""
        return self.x == other.x and self.y == other.y

# Задание 2: Методы сравнения
@functools.total_ordering
class Student:
    """Класс студента"""
    def __init__(self, name: str, average_grade: float):
        self.name = name
        self.average_grade = average_grade
    
    def __eq__(self, other: 'Student') -> bool:
        """Сравнение студентов по среднему баллу"""
        return self.average_grade == other.average_grade
    
    def __lt__(self, other: 'Student') -> bool:
        """Сравнение студентов по среднему баллу (меньше)"""
        return self.average_grade < other.average_grade
    
    def __hash__(self) -> int:
        """Хэш студента (имя и средний балл)"""
        return hash((self.name, self.average_grade))
    
    def __str__(self) -> str:
        """Строковое представление студента"""
        return f"Student({self.name}, avg_grade: {self.average_grade})"

# Задание 3: Магические методы контейнеров
class CustomList:
    """Класс кастомного списка"""
    def __init__(self, initial_list=None):
        if initial_list is None:
            self._items = []
        else:
            self._items = list(initial_list)
    
    def __getitem__(self, index: int) -> Any:
        """Получение элемента по индексу"""
        return self._items[index]
    
    def __setitem__(self, index: int, value: Any) -> None:
        """Установка значения по индексу"""
        self._items[index] = value
    
    def __delitem__(self, index: int) -> None:
        """Удаление элемента по индексу"""
        del self._items[index]
    
    def __len__(self) -> int:
        """Получение длины списка"""
        return len(self._items)
    
    def __contains__(self, item: Any) -> bool:
        """Проверка на наличие элемента в списке"""
        return item in self._items
    
    def append(self, item: Any) -> None:
        """Добавление элемента в конец списка"""
        self._items.append(item)
    
    def __str__(self) -> str:
        """Строковое представление списка"""
        return str(self._items)
    
    def __repr__(self) -> str:
        """Официальное строковое представление списка"""
        return f"CustomList({self._items})"

# Задание 4: Методы для вызова и представления
class Calculator:
    """Класс калькулятора"""
    def __init__(self, name: str = "Calculator"):
        self.name = name
        self.history = []
    
    def __call__(self, a: Union[int, float], b: Union[int, float], operation: str = "+") -> Union[int, float]:
        """Позволяет вызывать объект как функцию"""
        if operation == "+":
            result = a + b
        elif operation == "-":
            result = a - b
        elif operation == "*":
            result = a * b
        elif operation == "/":
            if b == 0:
                raise ZeroDivisionError("Cannot divide by zero")
            result = a / b
        else:
            raise ValueError(f"Unsupported operation: {operation}")
        
        self.history.append(f"{a} {operation} {b} = {result}")
        return result
    
    def __str__(self) -> str:
        """Строковое представление калькулятора"""
        return f"{self.name} with {len(self.history)} operations in history"
    
    def __repr__(self) -> str:
        """Официальное строковое представление калькулятора"""
        return f"Calculator(name='{self.name}')"

# Задание 5: Контекстный менеджер
class FileManager:
    """Класс для работы с файлами как контекстный менеджер"""
    def __init__(self, filename: str, mode: str = 'r'):
        self.filename = filename
        self.mode = mode
        self.file = None
    
    def __enter__(self):
        """Открытие файла при входе в контекст"""
        self.file = open(self.filename, self.mode)
        return self.file
    
    def __exit__(self, exc_type, exc_value, traceback):
        """Закрытие файла при выходе из контекста"""
        if self.file:
            self.file.close()
        
        # Если произошло исключение, возвращаем False, чтобы позволить ему всплыть
        return False

# Примеры использования:
if __name__ == "__main__":
    print("=== Задание 1: Арифметические магические методы ===")
    v1 = Vector2D(2, 3)
    v2 = Vector2D(4, 5)
    v3 = v1 + v2
    v4 = v2 - v1
    v5 = v1 * 3
    print(f"v1: {v1}")
    print(f"v2: {v2}")
    print(f"v1 + v2: {v3}")
    print(f"v2 - v1: {v4}")
    print(f"v1 * 3: {v5}")
    
    print("\n=== Задание 2: Методы сравнения ===")
    student1 = Student("Иван", 4.5)
    student2 = Student("Мария", 4.7)
    student3 = Student("Петр", 4.5)
    print(f"{student1} == {student2}: {student1 == student2}")
    print(f"{student1} < {student2}: {student1 < student2}")
    print(f"{student1} == {student3}: {student1 == student3}")
    print(f"Hashes: {hash(student1)}, {hash(student2)}, {hash(student3)}")
    
    print("\n=== Задание 3: Магические методы контейнеров ===")
    cl = CustomList([1, 2, 3, 4, 5])
    print(f"Initial list: {cl}")
    print(f"Length: {len(cl)}")
    print(f"Element at index 2: {cl[2]}")
    cl[2] = 10
    print(f"After setting index 2 to 10: {cl}")
    print(f"Is 10 in list? {10 in cl}")
    del cl[1]
    print(f"After deleting index 1: {cl}")
    
    print("\n=== Задание 4: Методы для вызова и представления ===")
    calc = Calculator("MyCalc")
    print(calc)
    print(calc(5, 3, "+"))
    print(calc(10, 2, "/"))
    print(calc)
    
    print("\n=== Задание 5: Контекстный менеджер ===")
    # Создаем тестовый файл
    with FileManager("test_file.txt", "w") as f:
        f.write("Тестовое содержимое файла")
    
    # Читаем из файла
    with FileManager("test_file.txt", "r") as f:
        content = f.read()
        print(f"Содержимое файла: {content}")
    
    # Удаляем тестовый файл
    import os
    os.remove("test_file.txt")