# Решения для практического занятия 12: ООП - магические методы

import functools
from typing import Union, Any, List
import os

# Решение задания 1: Арифметические магические методы
class Vector2D:
    """Класс двумерного вектора"""
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __add__(self, other: 'Vector2D') -> 'Vector2D':
        """Сложение векторов"""
        if not isinstance(other, Vector2D):
            return NotImplemented
        return Vector2D(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: 'Vector2D') -> 'Vector2D':
        """Вычитание векторов"""
        if not isinstance(other, Vector2D):
            return NotImplemented
        return Vector2D(self.x - other.x, self.y - other.y)
    
    def __mul__(self, scalar: Union[int, float]) -> 'Vector2D':
        """Скалярное умножение"""
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        return Vector2D(self.x * scalar, self.y * scalar)
    
    def __rmul__(self, scalar: Union[int, float]) -> 'Vector2D':
        """Обратное скалярное умножение"""
        return self.__mul__(scalar)
    
    def __truediv__(self, scalar: Union[int, float]) -> 'Vector2D':
        """Деление на скаляр"""
        if not isinstance(scalar, (int, float)):
            return NotImplemented
        if scalar == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        return Vector2D(self.x / scalar, self.y / scalar)
    
    def __neg__(self) -> 'Vector2D':
        """Унарный минус"""
        return Vector2D(-self.x, -self.y)
    
    def __str__(self) -> str:
        """Строковое представление вектора"""
        return f"Vector2D({self.x}, {self.y})"
    
    def __repr__(self) -> str:
        """Официальное строковое представление вектора"""
        return f"Vector2D({self.x}, {self.y})"
    
    def __eq__(self, other: 'Vector2D') -> bool:
        """Сравнение векторов на равенство"""
        if not isinstance(other, Vector2D):
            return NotImplemented
        return self.x == other.x and self.y == other.y
    
    def __abs__(self) -> float:
        """Длина вектора (модуль)"""
        return (self.x ** 2 + self.y ** 2) ** 0.5

# Решение задания 2: Методы сравнения
@functools.total_ordering
class Student:
    """Класс студента"""
    def __init__(self, name: str, average_grade: float):
        self.name = name
        self.average_grade = average_grade
    
    def __eq__(self, other: 'Student') -> bool:
        """Сравнение студентов по среднему баллу"""
        if not isinstance(other, Student):
            return NotImplemented
        return self.average_grade == other.average_grade
    
    def __lt__(self, other: 'Student') -> bool:
        """Сравнение студентов по среднему баллу (меньше)"""
        if not isinstance(other, Student):
            return NotImplemented
        return self.average_grade < other.average_grade
    
    def __hash__(self) -> int:
        """Хэш студента (имя и средний балл)"""
        return hash((self.name, self.average_grade))
    
    def __str__(self) -> str:
        """Строковое представление студента"""
        return f"Student({self.name}, avg_grade: {self.average_grade})"
    
    def __repr__(self) -> str:
        """Официальное строковое представление студента"""
        return f"Student('{self.name}', avg_grade={self.average_grade})"

# Решение задания 3: Магические методы контейнеров
class CustomList:
    """Класс кастомного списка"""
    def __init__(self, initial_list=None):
        if initial_list is None:
            self._items = []
        else:
            self._items = list(initial_list)
    
    def __getitem__(self, index: Union[int, slice]) -> Any:
        """Получение элемента по индексу или срезу"""
        return self._items[index]
    
    def __setitem__(self, index: Union[int, slice], value: Any) -> None:
        """Установка значения по индексу или срезу"""
        self._items[index] = value
    
    def __delitem__(self, index: Union[int, slice]) -> None:
        """Удаление элемента по индексу или срезу"""
        del self._items[index]
    
    def __len__(self) -> int:
        """Получение длины списка"""
        return len(self._items)
    
    def __contains__(self, item: Any) -> bool:
        """Проверка на наличие элемента в списке"""
        return item in self._items
    
    def __iter__(self):
        """Позволяет итерироваться по списку"""
        return iter(self._items)
    
    def __reversed__(self):
        """Возвращает итератор в обратном порядке"""
        return reversed(self._items)
    
    def __iadd__(self, other: List[Any]) -> 'CustomList':
        """Расширенное присваивание += (in-place addition)"""
        if isinstance(other, (list, CustomList)):
            self._items.extend(other)
        else:
            self._items.append(other)
        return self
    
    def append(self, item: Any) -> None:
        """Добавление элемента в конец списка"""
        self._items.append(item)
    
    def __str__(self) -> str:
        """Строковое представление списка"""
        return str(self._items)
    
    def __repr__(self) -> str:
        """Официальное строковое представление списка"""
        return f"CustomList({self._items})"
    
    def __add__(self, other: List[Any]) -> 'CustomList':
        """Сложение списков"""
        new_list = CustomList(self._items)
        if isinstance(other, (list, CustomList)):
            new_list._items.extend(other)
        else:
            new_list._items.append(other)
        return new_list

# Решение задания 4: Методы для вызова и представления
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
        elif operation == "**":
            result = a ** b
        elif operation == "%":
            result = a % b
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
    
    def __len__(self) -> int:
        """Количество операций в истории"""
        return len(self.history)
    
    def __bool__(self) -> bool:
        """True если есть история операций, иначе False"""
        return bool(self.history)

# Решение задания 5: Контекстный менеджер
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
        
        # Возвращаем False, чтобы позволить исключениям всплывать
        return False

# Дополнительные примеры использования магических методов
class Temperature:
    """Класс для работы с температурой"""
    def __init__(self, celsius: float):
        self.celsius = celsius
    
    def __str__(self) -> str:
        return f"{self.celsius}°C"
    
    def __repr__(self) -> str:
        return f"Temperature({self.celsius})"
    
    def __eq__(self, other) -> bool:
        if isinstance(other, Temperature):
            return self.celsius == other.celsius
        return NotImplemented
    
    def __lt__(self, other) -> bool:
        if isinstance(other, Temperature):
            return self.celsius < other.celsius
        return NotImplemented
    
    def __add__(self, other) -> 'Temperature':
        if isinstance(other, (int, float)):
            return Temperature(self.celsius + other)
        elif isinstance(other, Temperature):
            return Temperature(self.celsius + other.celsius)
        return NotImplemented
    
    def __sub__(self, other) -> 'Temperature':
        if isinstance(other, (int, float)):
            return Temperature(self.celsius - other)
        elif isinstance(other, Temperature):
            return Temperature(self.celsius - other.celsius)
        return NotImplemented
    
    def to_fahrenheit(self) -> float:
        return self.celsius * 9/5 + 32
    
    def to_kelvin(self) -> float:
        return self.celsius + 273.15

class Matrix:
    """Класс для работы с матрицами"""
    def __init__(self, data: List[List[float]]):
        self.data = [row[:] for row in data]  # Создаем копию
        self.rows = len(data)
        self.cols = len(data[0]) if data else 0
    
    def __str__(self) -> str:
        return '\n'.join([' '.join(map(str, row)) for row in self.data])
    
    def __repr__(self) -> str:
        return f"Matrix({self.data})"
    
    def __add__(self, other: 'Matrix') -> 'Matrix':
        if not isinstance(other, Matrix) or self.rows != other.rows or self.cols != other.cols:
            return NotImplemented
        
        result_data = []
        for i in range(self.rows):
            row = []
            for j in range(self.cols):
                row.append(self.data[i][j] + other.data[i][j])
            result_data.append(row)
        
        return Matrix(result_data)
    
    def __mul__(self, other: Union['Matrix', float, int]) -> 'Matrix':
        if isinstance(other, (int, float)):
            # Скалярное умножение
            result_data = []
            for i in range(self.rows):
                row = []
                for j in range(self.cols):
                    row.append(self.data[i][j] * other)
                result_data.append(row)
            return Matrix(result_data)
        elif isinstance(other, Matrix) and self.cols == other.rows:
            # Матричное умножение
            result_data = []
            for i in range(self.rows):
                row = []
                for j in range(other.cols):
                    element = sum(self.data[i][k] * other.data[k][j] for k in range(self.cols))
                    row.append(element)
                result_data.append(row)
            return Matrix(result_data)
        else:
            return NotImplemented

def demonstrate_magic_methods():
    """Демонстрация использования магических методов"""
    print("=== Демонстрация магических методов ===")
    
    # Векторы
    print("\n1. Работа с векторами:")
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
    print(f"Длина вектора v1: {abs(v1):.2f}")
    
    # Студенты
    print("\n2. Работа со студентами:")
    student1 = Student("Иван", 4.5)
    student2 = Student("Мария", 4.7)
    student3 = Student("Петр", 4.5)
    print(f"{student1} == {student2}: {student1 == student2}")
    print(f"{student1} < {student2}: {student1 < student2}")
    print(f"{student1} <= {student3}: {student1 <= student3}")
    print(f"Hashes: {hash(student1)}, {hash(student2)}, {hash(student3)}")
    
    # Кастомный список
    print("\n3. Работа с кастомным списком:")
    cl = CustomList([1, 2, 3, 4, 5])
    print(f"Initial list: {cl}")
    print(f"Length: {len(cl)}")
    print(f"Element at index 2: {cl[2]}")
    cl[2] = 10
    print(f"After setting index 2 to 10: {cl}")
    print(f"Is 10 in list? {10 in cl}")
    print(f"Reversed iteration: {list(reversed(cl))}")
    
    # Калькулятор
    print("\n4. Работа с калькулятором:")
    calc = Calculator("AdvancedCalc")
    print(calc)
    print(f"5 + 3 = {calc(5, 3, '+')}")
    print(f"10 * 5 = {calc(10, 5, '*')}")
    print(f"History length: {len(calc)}")
    print(f"Has operations: {bool(calc)}")
    
    # Контекстный менеджер
    print("\n5. Работа с контекстным менеджером:")
    with FileManager("temp_test.txt", "w") as f:
        f.write("Тестовое содержимое")
    
    with FileManager("temp_test.txt", "r") as f:
        content = f.read()
        print(f"Содержимое файла: {content}")
    
    # Удаление временного файла
    os.remove("temp_test.txt")
    
    # Дополнительные примеры
    print("\n6. Дополнительные примеры:")
    t1 = Temperature(25)
    t2 = Temperature(30)
    print(f"t1: {t1}, t2: {t2}")
    print(f"t1 < t2: {t1 < t2}")
    print(f"t1 + t2: {t1 + t2}")
    print(f"t1 в Фаренгейтах: {t1.to_fahrenheit()}°F")
    
    m1 = Matrix([[1, 2], [3, 4]])
    m2 = Matrix([[5, 6], [7, 8]])
    print(f"Матрица 1:\n{m1}")
    print(f"Матрица 2:\n{m2}")
    print(f"Сумма матриц:\n{m1 + m2}")
    print(f"Умножение матрицы 1 на 2:\n{m1 * 2}")

# Примеры использования:
if __name__ == "__main__":
    print("=== Решения для практического занятия 12 ===")
    
    print("\n1. Решение задания 1: Арифметические магические методы")
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
    
    print("\n2. Решение задания 2: Методы сравнения")
    student1 = Student("Иван", 4.5)
    student2 = Student("Мария", 4.7)
    student3 = Student("Петр", 4.5)
    print(f"{student1} == {student2}: {student1 == student2}")
    print(f"{student1} < {student2}: {student1 < student2}")
    print(f"{student1} <= {student3}: {student1 <= student3}")
    print(f"Hashes: {hash(student1)}, {hash(student2)}, {hash(student3)}")
    
    print("\n3. Решение задания 3: Магические методы контейнеров")
    cl = CustomList([1, 2, 3, 4, 5])
    print(f"Initial list: {cl}")
    print(f"Length: {len(cl)}")
    print(f"Element at index 2: {cl[2]}")
    cl[2] = 10
    print(f"After setting index 2 to 10: {cl}")
    print(f"Is 10 in list? {10 in cl}")
    del cl[1]
    print(f"After deleting index 1: {cl}")
    
    print("\n4. Решение задания 4: Методы для вызова и представления")
    calc = Calculator("MyCalc")
    print(calc)
    print(calc(5, 3, "+"))
    print(calc(10, 2, "/"))
    print(calc)
    
    print("\n5. Решение задания 5: Контекстный менеджер")
    # Создаем тестовый файл
    with FileManager("test_file.txt", "w") as f:
        f.write("Тестовое содержимое файла")
    
    # Читаем из файла
    with FileManager("test_file.txt", "r") as f:
        content = f.read()
        print(f"Содержимое файла: {content}")
    
    # Удаляем тестовый файл
    os.remove("test_file.txt")
    
    print("\n6. Дополнительные примеры")
    demonstrate_magic_methods()