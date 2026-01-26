# Примеры структуры приложения Python

"""
Этот файл демонстрирует основные концепции структурирования Python-приложений.
"""

# 1. Пример простой структуры приложения
def main():
    """
    Основная функция приложения
    """
    print("Добро пожаловать в приложение!")
    name = input("Введите ваше имя: ")
    greet_user(name)

def greet_user(name):
    """
    Функция приветствия пользователя
    
    Args:
        name (str): Имя пользователя
    """
    if name.strip():
        print(f"Привет, {name}!")
    else:
        print("Привет, незнакомец!")

# 2. Пример использования классов
class Calculator:
    """
    Простой калькулятор для демонстрации объектно-ориентированного подхода
    """
    
    def __init__(self):
        """
        Инициализация калькулятора
        """
        self.history = []
    
    def add(self, a, b):
        """
        Сложение двух чисел
        
        Args:
            a (float): Первое число
            b (float): Второе число
            
        Returns:
            float: Результат сложения
        """
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result
    
    def subtract(self, a, b):
        """
        Вычитание двух чисел
        
        Args:
            a (float): Первое число
            b (float): Второе число
            
        Returns:
            float: Результат вычитания
        """
        result = a - b
        self.history.append(f"{a} - {b} = {result}")
        return result
    
    def get_history(self):
        """
        Получение истории операций
        
        Returns:
            list: Список выполненных операций
        """
        return self.history

# 3. Пример обработки исключений
def safe_divide(a, b):
    """
    Безопасное деление с обработкой исключений
    
    Args:
        a (float): Делимое
        b (float): Делитель
        
    Returns:
        float or None: Результат деления или None в случае ошибки
    """
    try:
        result = a / b
        return result
    except ZeroDivisionError:
        print("Ошибка: деление на ноль невозможно")
        return None
    except TypeError:
        print("Ошибка: неподдерживаемый тип данных")
        return None

# 4. Пример работы с файлами
def write_to_file(filename, content):
    """
    Запись содержимого в файл с обработкой исключений
    
    Args:
        filename (str): Имя файла
        content (str): Содержимое для записи
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"Содержимое успешно записано в {filename}")
    except Exception as e:
        print(f"Ошибка при записи в файл: {e}")

def read_from_file(filename):
    """
    Чтение содержимого из файла с обработкой исключений
    
    Args:
        filename (str): Имя файла
        
    Returns:
        str or None: Содержимое файла или None в случае ошибки
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"Файл {filename} не найден")
        return None
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
        return None

# 5. Пример использования модулей
import os
import sys
from datetime import datetime

def get_system_info():
    """
    Получение информации о системе
    
    Returns:
        dict: Словарь с информацией о системе
    """
    info = {
        'current_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'current_directory': os.getcwd(),
        'python_version': sys.version,
        'platform': sys.platform
    }
    return info

# 6. Пример работы с коллекциями
def process_data(data_list):
    """
    Обработка списка данных
    
    Args:
        data_list (list): Список данных для обработки
        
    Returns:
        dict: Словарь с результатами обработки
    """
    from collections import Counter, defaultdict
    
    # Подсчет элементов
    counts = Counter(data_list)
    
    # Группировка по типу
    grouped = defaultdict(list)
    for item in data_list:
        grouped[type(item).__name__].append(item)
    
    return {
        'counts': dict(counts),
        'grouped': dict(grouped),
        'unique_items': list(set(data_list)),
        'total_items': len(data_list)
    }

# 7. Пример использования документации и аннотаций типов
from typing import List, Dict, Optional

def typed_function(numbers: List[int], multiplier: int = 2) -> List[int]:
    """
    Умножает все числа в списке на заданный множитель
    
    Args:
        numbers: Список целых чисел
        multiplier: Множитель (по умолчанию 2)
        
    Returns:
        Список чисел, умноженных на множитель
    """
    return [num * multiplier for num in numbers]

def demonstrate_app_structure():
    """
    Демонстрация структуры приложения
    """
    print("=== Демонстрация структуры приложения ===\n")
    
    # Пример 1: Простая функция
    print("1. Простая функция:")
    greet_user("Иван")
    
    # Пример 2: Использование класса
    print("\n2. Использование класса:")
    calc = Calculator()
    print(f"5 + 3 = {calc.add(5, 3)}")
    print(f"10 - 4 = {calc.subtract(10, 4)}")
    print(f"История операций: {calc.get_history()}")
    
    # Пример 3: Обработка исключений
    print("\n3. Обработка исключений:")
    print(f"10 / 2 = {safe_divide(10, 2)}")
    print(f"10 / 0 = {safe_divide(10, 0)}")
    
    # Пример 4: Работа с файлами
    print("\n4. Работа с файлами:")
    write_to_file("example.txt", "Это пример содержимого файла")
    content = read_from_file("example.txt")
    print(f"Прочитанное содержимое: {content}")
    
    # Пример 5: Системная информация
    print("\n5. Системная информация:")
    sys_info = get_system_info()
    for key, value in sys_info.items():
        print(f"  {key}: {value}")
    
    # Пример 6: Обработка данных
    print("\n6. Обработка данных:")
    sample_data = [1, 2, "hello", 3, 2, "world", "hello", 4.5, 1]
    processed = process_data(sample_data)
    print(f"  Подсчет элементов: {processed['counts']}")
    print(f"  Группировка по типу: {processed['grouped']}")
    
    # Пример 7: Аннотации типов
    print("\n7. Аннотации типов:")
    result = typed_function([1, 2, 3, 4, 5])
    print(f"typed_function([1, 2, 3, 4, 5]) = {result}")

if __name__ == "__main__":
    demonstrate_app_structure()
