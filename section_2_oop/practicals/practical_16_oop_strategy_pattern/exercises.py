# Упражнения для практического занятия 16: ООП - паттерн Strategy

from abc import ABC, abstractmethod
from typing import List, Any, Dict
import time
import random

# Задание 1: Базовая реализация Strategy
class SortingStrategy(ABC):
    """Интерфейс стратегии сортировки"""
    @abstractmethod
    def sort(self, data: List[int]) -> List[int]:
        pass

class BubbleSort(SortingStrategy):
    """Стратегия сортировки пузырьком"""
    def sort(self, data: List[int]) -> List[int]:
        arr = data.copy()
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr

class QuickSort(SortingStrategy):
    """Стратегия быстрой сортировки"""
    def sort(self, data: List[int]) -> List[int]:
        if len(data) <= 1:
            return data
        pivot = data[len(data) // 2]
        left = [x for x in data if x < pivot]
        middle = [x for x in data if x == pivot]
        right = [x for x in data if x > pivot]
        return self.sort(left) + middle + self.sort(right)

class MergeSort(SortingStrategy):
    """Стратегия сортировки слиянием"""
    def sort(self, data: List[int]) -> List[int]:
        if len(data) <= 1:
            return data
        
        mid = len(data) // 2
        left = self.sort(data[:mid])
        right = self.sort(data[mid:])
        
        return self._merge(left, right)
    
    def _merge(self, left: List[int], right: List[int]) -> List[int]:
        result = []
        i = j = 0
        
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        
        result.extend(left[i:])
        result.extend(right[j:])
        return result

class Sorter:
    """Контекст для сортировки"""
    def __init__(self, strategy: SortingStrategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: SortingStrategy):
        """Установить новую стратегию сортировки"""
        self._strategy = strategy
    
    def sort(self, data: List[int]) -> List[int]:
        """Выполнить сортировку с использованием текущей стратегии"""
        return self._strategy.sort(data)

# Задание 2: Финансовые стратегии
class TaxStrategy(ABC):
    """Интерфейс стратегии расчета налога"""
    @abstractmethod
    def calculate_tax(self, income: float) -> float:
        pass

class ProgressiveTax(TaxStrategy):
    """Прогрессивная система налогообложения"""
    def calculate_tax(self, income: float) -> float:
        if income <= 10000:
            return income * 0.1
        elif income <= 50000:
            return 1000 + (income - 10000) * 0.2
        else:
            return 9000 + (income - 50000) * 0.3

class FlatTax(TaxStrategy):
    """Пропорциональная (плоская) система налогообложения"""
    def __init__(self, rate: float = 0.15):
        self.rate = rate
    
    def calculate_tax(self, income: float) -> float:
        return income * self.rate

class ProportionalTax(TaxStrategy):
    """Пропорциональная система (другая реализация)"""
    def __init__(self, rate: float = 0.13):
        self.rate = rate
    
    def calculate_tax(self, income: float) -> float:
        return income * self.rate

class TaxCalculator:
    """Калькулятор налогов"""
    def __init__(self, strategy: TaxStrategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: TaxStrategy):
        """Установить новую стратегию расчета налога"""
        self._strategy = strategy
    
    def calculate(self, income: float) -> float:
        """Рассчитать налог с использованием текущей стратегии"""
        return self._strategy.calculate_tax(income)

# Задание 3: Стратегии с параметрами
class CompressionStrategy(ABC):
    """Интерфейс стратегии сжатия"""
    @abstractmethod
    def compress(self, data: str, **params) -> Dict[str, Any]:
        pass

class ZipCompression(CompressionStrategy):
    """Стратегия сжатия ZIP"""
    def compress(self, data: str, **params) -> Dict[str, Any]:
        compression_level = params.get('compression_level', 6)
        return {
            'compressed_data': f"ZIP_COMPRESSED_{data[:10]}...",
            'original_size': len(data),
            'compressed_size': len(data) // 2,  # Условное сжатие
            'compression_ratio': 0.5,
            'compression_level': compression_level
        }

class RarCompression(CompressionStrategy):
    """Стратегия сжатия RAR"""
    def compress(self, data: str, **params) -> Dict[str, Any]:
        password = params.get('password', '')
        return {
            'compressed_data': f"RAR_COMPRESSED_{data[:10]}...",
            'original_size': len(data),
            'compressed_size': len(data) // 3,  # Условное сжатие
            'compression_ratio': 0.33,
            'password_protected': bool(password)
        }

class GzipCompression(CompressionStrategy):
    """Стратегия сжатия GZIP"""
    def compress(self, data: str, **params) -> Dict[str, Any]:
        compression_level = params.get('compression_level', 6)
        return {
            'compressed_data': f"GZIP_COMPRESSED_{data[:10]}...",
            'original_size': len(data),
            'compressed_size': len(data) // 2.5,  # Условное сжатие
            'compression_ratio': 0.4,
            'compression_level': compression_level
        }

class Compressor:
    """Компрессор данных"""
    def __init__(self, strategy: CompressionStrategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: CompressionStrategy):
        """Установить новую стратегию сжатия"""
        self._strategy = strategy
    
    def compress(self, data: str, **params) -> Dict[str, Any]:
        """Сжать данные с использованием текущей стратегии"""
        return self._strategy.compress(data, **params)

# Задание 4: Динамическое изменение стратегии
class RouteStrategy(ABC):
    """Интерфейс стратегии поиска маршрута"""
    @abstractmethod
    def find_route(self, start: str, end: str, **params) -> Dict[str, Any]:
        pass

class FastestRoute(RouteStrategy):
    """Стратегия поиска самого быстрого маршрута"""
    def find_route(self, start: str, end: str, **params) -> Dict[str, Any]:
        time_estimate = random.randint(20, 60)  # Условное время в минутах
        return {
            'route': f"Fastest route from {start} to {end}",
            'estimated_time': f"{time_estimate} minutes",
            'distance': round(time_estimate * 0.8, 1),  # Условное расстояние
            'recommended': True
        }

class ShortestRoute(RouteStrategy):
    """Стратегия поиска кратчайшего маршрута"""
    def find_route(self, start: str, end: str, **params) -> Dict[str, Any]:
        distance = random.randint(10, 30)  # Условное расстояние в км
        return {
            'route': f"Shortest route from {start} to {end}",
            'estimated_time': f"{int(distance * 1.2)} minutes",  # Условное время
            'distance': f"{distance} km",
            'recommended': True
        }

class EcoRoute(RouteStrategy):
    """Стратегия поиска экологичного маршрута"""
    def find_route(self, start: str, end: str, **params) -> Dict[str, Any]:
        eco_points = random.randint(80, 100)  # Условные экологические баллы
        return {
            'route': f"Eco-friendly route from {start} to {end}",
            'estimated_time': f"{random.randint(25, 65)} minutes",
            'distance': f"{random.randint(15, 35)} km",
            'eco_points': eco_points,
            'recommended': True
        }

class Router:
    """Система маршрутизации"""
    def __init__(self, strategy: RouteStrategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: RouteStrategy):
        """Изменить стратегию поиска маршрута"""
        self._strategy = strategy
    
    def find_route(self, start: str, end: str, **params) -> Dict[str, Any]:
        """Найти маршрут с использованием текущей стратегии"""
        return self._strategy.find_route(start, end, **params)

# Задание 5: Комбинированные стратегии
class DataProcessingStrategy(ABC):
    """Интерфейс стратегии обработки данных"""
    @abstractmethod
    def process(self, data: List[Any]) -> List[Any]:
        pass

class SortStrategy(DataProcessingStrategy):
    """Стратегия сортировки данных"""
    def process(self, data: List[Any]) -> List[Any]:
        return sorted(data)

class FilterStrategy(DataProcessingStrategy):
    """Стратегия фильтрации данных"""
    def __init__(self, condition):
        self.condition = condition
    
    def process(self, data: List[Any]) -> List[Any]:
        return [item for item in data if self.condition(item)]

class TransformStrategy(DataProcessingStrategy):
    """Стратегия трансформации данных"""
    def __init__(self, transform_func):
        self.transform_func = transform_func
    
    def process(self, data: List[Any]) -> List[Any]:
        return [self.transform_func(item) for item in data]

class CompositeStrategy(DataProcessingStrategy):
    """Комбинированная стратегия для последовательной обработки"""
    def __init__(self):
        self.strategies = []
    
    def add_strategy(self, strategy: DataProcessingStrategy):
        """Добавить стратегию в цепочку"""
        self.strategies.append(strategy)
    
    def process(self, data: List[Any]) -> List[Any]:
        """Последовательно применить все стратегии"""
        result = data
        for strategy in self.strategies:
            result = strategy.process(result)
        return result

class DataProcessor:
    """Обработчик данных"""
    def __init__(self, strategy: DataProcessingStrategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: DataProcessingStrategy):
        """Установить новую стратегию обработки"""
        self._strategy = strategy
    
    def process(self, data: List[Any]) -> List[Any]:
        """Обработать данные с использованием текущей стратегии"""
        return self._strategy.process(data)

# Примеры использования:
if __name__ == "__main__":
    print("=== Задание 1: Базовая реализация Strategy ===")
    data = [64, 34, 25, 12, 22, 11, 90]
    print(f"Исходные данные: {data}")
    
    sorter = Sorter(BubbleSort())
    print(f"Сортировка пузырьком: {sorter.sort(data)}")
    
    sorter.set_strategy(QuickSort())
    print(f"Быстрая сортировка: {sorter.sort(data)}")
    
    sorter.set_strategy(MergeSort())
    print(f"Сортировка слиянием: {sorter.sort(data)}")
    print()
    
    print("=== Задание 2: Финансовые стратегии ===")
    calculator = TaxCalculator(ProgressiveTax())
    income = 60000
    tax = calculator.calculate(income)
    print(f"Доход: ${income}, Налог (прогрессивный): ${tax:.2f}")
    
    calculator.set_strategy(FlatTax(0.15))
    tax = calculator.calculate(income)
    print(f"Доход: ${income}, Налог (плоский): ${tax:.2f}")
    
    calculator.set_strategy(ProportionalTax(0.13))
    tax = calculator.calculate(income)
    print(f"Доход: ${income}, Налог (пропорциональный): ${tax:.2f}")
    print()
    
    print("=== Задание 3: Стратегии с параметрами ===")
    compressor = Compressor(ZipCompression())
    text = "Это длинный текст для сжатия"
    result = compressor.compress(text, compression_level=9)
    print(f"ZIP сжатие: {result}")
    
    compressor.set_strategy(RarCompression())
    result = compressor.compress(text, password="secret")
    print(f"RAR сжатие: {result}")
    
    compressor.set_strategy(GzipCompression())
    result = compressor.compress(text, compression_level=7)
    print(f"GZIP сжатие: {result}")
    print()
    
    print("=== Задание 4: Динамическое изменение стратегии ===")
    router = Router(FastestRoute())
    route = router.find_route("Москва", "Санкт-Петербург")
    print(f"Быстрый маршрут: {route}")
    
    router.set_strategy(ShortestRoute())
    route = router.find_route("Москва", "Санкт-Петербург")
    print(f"Кратчайший маршрут: {route}")
    
    router.set_strategy(EcoRoute())
    route = router.find_route("Москва", "Санкт-Петербург")
    print(f"Экологичный маршрут: {route}")
    print()
    
    print("=== Задание 5: Комбинированные стратегии ===")
    data = [5, 2, 8, 1, 9, 3, 7, 4, 6]
    print(f"Исходные данные: {data}")
    
    # Создаем комбинированную стратегию: сначала фильтрация, потом сортировка
    composite_strategy = CompositeStrategy()
    composite_strategy.add_strategy(FilterStrategy(lambda x: x > 3))  # Фильтруем числа > 3
    composite_strategy.add_strategy(SortStrategy())  # Сортируем результат
    
    processor = DataProcessor(composite_strategy)
    result = processor.process(data)
    print(f"Фильтрация (>3) и сортировка: {result}")
    
    # Добавим трансформацию
    composite_strategy.add_strategy(TransformStrategy(lambda x: x * 2))  # Удваиваем числа
    result = processor.process(data)
    print(f"Фильтрация (>3), сортировка и удвоение: {result}")