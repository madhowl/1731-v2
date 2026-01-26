# Решения для практического занятия 16: ООП - паттерн Strategy

from abc import ABC, abstractmethod
from typing import List, Any, Dict, Callable
import time
import random
import threading
from enum import Enum

# Решение задания 1: Базовая реализация Strategy
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
        comparisons = 0
        swaps = 0
        start_time = time.time()
        
        for i in range(n):
            for j in range(0, n-i-1):
                comparisons += 1
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
                    swaps += 1
        end_time = time.time()
        
        print(f"BubbleSort: {comparisons} сравнений, {swaps} обменов, время: {end_time - start_time:.4f}с")
        return arr

class QuickSort(SortingStrategy):
    """Стратегия быстрой сортировки"""
    def sort(self, data: List[int]) -> List[int]:
        start_time = time.time()
        result = self._quicksort(data.copy())
        end_time = time.time()
        print(f"QuickSort: время: {end_time - start_time:.4f}с")
        return result
    
    def _quicksort(self, arr: List[int]) -> List[int]:
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return self._quicksort(left) + middle + self._quicksort(right)

class MergeSort(SortingStrategy):
    """Стратегия сортировки слиянием"""
    def sort(self, data: List[int]) -> List[int]:
        start_time = time.time()
        result = self._mergesort(data.copy())
        end_time = time.time()
        print(f"MergeSort: время: {end_time - start_time:.4f}с")
        return result
    
    def _mergesort(self, arr: List[int]) -> List[int]:
        if len(arr) <= 1:
            return arr
        
        mid = len(arr) // 2
        left = self._mergesort(arr[:mid])
        right = self._mergesort(arr[mid:])
        
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

class HeapSort(SortingStrategy):
    """Стратегия сортировки кучей"""
    def sort(self, data: List[int]) -> List[int]:
        arr = data.copy()
        n = len(arr)
        start_time = time.time()
        
        # Построение кучи
        for i in range(n // 2 - 1, -1, -1):
            self._heapify(arr, n, i)
        
        # Извлечение элементов из кучи
        for i in range(n - 1, 0, -1):
            arr[0], arr[i] = arr[i], arr[0]
            self._heapify(arr, i, 0)
        
        end_time = time.time()
        print(f"HeapSort: время: {end_time - start_time:.4f}с")
        return arr
    
    def _heapify(self, arr: List[int], n: int, i: int):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        if left < n and arr[left] > arr[largest]:
            largest = left
        
        if right < n and arr[right] > arr[largest]:
            largest = right
        
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            self._heapify(arr, n, largest)

class Sorter:
    """Контекст для сортировки"""
    def __init__(self, strategy: SortingStrategy):
        self._strategy = strategy
        self._lock = threading.Lock()
    
    def set_strategy(self, strategy: SortingStrategy):
        """Установить новую стратегию сортировки"""
        with self._lock:
            self._strategy = strategy
    
    def sort(self, data: List[int]) -> List[int]:
        """Выполнить сортировку с использованием текущей стратегии"""
        with self._lock:
            return self._strategy.sort(data)
    
    def get_strategy_name(self) -> str:
        """Получить имя текущей стратегии"""
        return self._strategy.__class__.__name__

# Решение задания 2: Финансовые стратегии
class TaxStrategy(ABC):
    """Интерфейс стратегии расчета налога"""
    @abstractmethod
    def calculate_tax(self, income: float) -> float:
        pass

class ProgressiveTax(TaxStrategy):
    """Прогрессивная система налогообложения"""
    def __init__(self, brackets: List[tuple] = None):
        # Ставки по умолчанию: (верхняя граница, ставка)
        self.brackets = brackets or [
            (10000, 0.10),
            (50000, 0.20),
            (float('inf'), 0.30)
        ]
    
    def calculate_tax(self, income: float) -> float:
        tax = 0.0
        prev_bracket = 0
        
        for bracket_limit, rate in self.brackets:
            if income <= prev_bracket:
                break
            
            taxable_income = min(income, bracket_limit) - prev_bracket
            tax += taxable_income * rate
            
            if income <= bracket_limit:
                break
            
            prev_bracket = bracket_limit
        
        return tax

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

class DeductibleTax(TaxStrategy):
    """Система с вычетами"""
    def __init__(self, rate: float = 0.13, deduction: float = 5000):
        self.rate = rate
        self.deduction = deduction
    
    def calculate_tax(self, income: float) -> float:
        taxable_income = max(0, income - self.deduction)
        return taxable_income * self.rate

class TaxCalculator:
    """Калькулятор налогов"""
    def __init__(self, strategy: TaxStrategy):
        self._strategy = strategy
        self._history = []
        self._lock = threading.Lock()
    
    def set_strategy(self, strategy: TaxStrategy):
        """Установить новую стратегию расчета налога"""
        with self._lock:
            self._strategy = strategy
    
    def calculate(self, income: float) -> float:
        """Рассчитать налог с использованием текущей стратегии"""
        with self._lock:
            tax = self._strategy.calculate_tax(income)
            self._history.append({
                'income': income,
                'tax': tax,
                'strategy': self._strategy.__class__.__name__,
                'timestamp': time.time()
            })
            return tax
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Получить историю расчетов"""
        with self._lock:
            return self._history.copy()

# Решение задания 3: Стратегии с параметрами
class CompressionStrategy(ABC):
    """Интерфейс стратегии сжатия"""
    @abstractmethod
    def compress(self, data: str, **params) -> Dict[str, Any]:
        pass

class ZipCompression(CompressionStrategy):
    """Стратегия сжатия ZIP"""
    def compress(self, data: str, **params) -> Dict[str, Any]:
        compression_level = params.get('compression_level', 6)
        algorithm = params.get('algorithm', 'deflate')
        
        # Имитация сжатия
        compressed_size = int(len(data) * (1 - compression_level / 10 * 0.5))
        
        return {
            'compressed_data': f"ZIP_COMPRESSED_{data[:min(10, len(data))]}...",
            'original_size': len(data),
            'compressed_size': compressed_size,
            'compression_ratio': compressed_size / len(data) if len(data) > 0 else 0,
            'compression_level': compression_level,
            'algorithm': algorithm,
            'format': 'ZIP'
        }

class RarCompression(CompressionStrategy):
    """Стратегия сжатия RAR"""
    def compress(self, data: str, **params) -> Dict[str, Any]:
        compression_level = params.get('compression_level', 5)
        password = params.get('password', '')
        
        # Имитация сжатия
        compressed_size = int(len(data) * (1 - compression_level / 10 * 0.4))
        
        return {
            'compressed_data': f"RAR_COMPRESSED_{data[:min(10, len(data))]}...",
            'original_size': len(data),
            'compressed_size': compressed_size,
            'compression_ratio': compressed_size / len(data) if len(data) > 0 else 0,
            'compression_level': compression_level,
            'password_protected': bool(password),
            'format': 'RAR'
        }

class GzipCompression(CompressionStrategy):
    """Стратегия сжатия GZIP"""
    def compress(self, data: str, **params) -> Dict[str, Any]:
        compression_level = params.get('compression_level', 6)
        strategy = params.get('strategy', 'default')
        
        # Имитация сжатия
        compressed_size = int(len(data) * (1 - compression_level / 10 * 0.45))
        
        return {
            'compressed_data': f"GZIP_COMPRESSED_{data[:min(10, len(data))]}...",
            'original_size': len(data),
            'compressed_size': compressed_size,
            'compression_ratio': compressed_size / len(data) if len(data) > 0 else 0,
            'compression_level': compression_level,
            'strategy': strategy,
            'format': 'GZIP'
        }

class LzwCompression(CompressionStrategy):
    """Стратегия сжатия LZW"""
    def compress(self, data: str, **params) -> Dict[str, Any]:
        # Упрощенная реализация LZW сжатия
        compression_level = params.get('compression_level', 6)
        
        # Имитация сжатия
        compressed_size = int(len(data) * (1 - compression_level / 10 * 0.35))
        
        return {
            'compressed_data': f"LZW_COMPRESSED_{data[:min(10, len(data))]}...",
            'original_size': len(data),
            'compressed_size': compressed_size,
            'compression_ratio': compressed_size / len(data) if len(data) > 0 else 0,
            'compression_level': compression_level,
            'format': 'LZW'
        }

class Compressor:
    """Компрессор данных"""
    def __init__(self, strategy: CompressionStrategy):
        self._strategy = strategy
        self._lock = threading.Lock()
    
    def set_strategy(self, strategy: CompressionStrategy):
        """Установить новую стратегию сжатия"""
        with self._lock:
            self._strategy = strategy
    
    def compress(self, data: str, **params) -> Dict[str, Any]:
        """Сжать данные с использованием текущей стратегии"""
        with self._lock:
            return self._strategy.compress(data, **params)
    
    def benchmark_compression(self, data: str, **params) -> Dict[str, Any]:
        """Сравнить все стратегии сжатия"""
        results = {}
        
        strategies = {
            'ZIP': ZipCompression(),
            'RAR': RarCompression(),
            'GZIP': GzipCompression(),
            'LZW': LzwCompression()
        }
        
        for name, strategy in strategies.items():
            start_time = time.time()
            result = strategy.compress(data, **params)
            end_time = time.time()
            
            result['compression_time'] = end_time - start_time
            results[name] = result
        
        return results

# Решение задания 4: Динамическое изменение стратегии
class RouteStrategy(ABC):
    """Интерфейс стратегии поиска маршрута"""
    @abstractmethod
    def find_route(self, start: str, end: str, **params) -> Dict[str, Any]:
        pass

class FastestRoute(RouteStrategy):
    """Стратегия поиска самого быстрого маршрута"""
    def find_route(self, start: str, end: str, **params) -> Dict[str, Any]:
        traffic_factor = params.get('traffic_factor', 1.0)
        time_estimate = random.randint(20, 60) * traffic_factor
        distance = time_estimate * 0.8  # условное расстояние
        
        return {
            'route': f"Fastest route from {start} to {end}",
            'estimated_time': f"{time_estimate:.1f} minutes",
            'distance': f"{distance:.1f} km",
            'recommended': True,
            'route_type': 'fastest',
            'details': 'Prioritizes speed over distance'
        }

class ShortestRoute(RouteStrategy):
    """Стратегия поиска кратчайшего маршрута"""
    def find_route(self, start: str, end: str, **params) -> Dict[str, Any]:
        distance = random.randint(10, 30)
        time_estimate = distance * 1.2  # условное время
        
        return {
            'route': f"Shortest route from {start} to {end}",
            'estimated_time': f"{time_estimate:.1f} minutes",
            'distance': f"{distance:.1f} km",
            'recommended': True,
            'route_type': 'shortest',
            'details': 'Prioritizes distance over speed'
        }

class EcoRoute(RouteStrategy):
    """Стратегия поиска экологичного маршрута"""
    def find_route(self, start: str, end: str, **params) -> Dict[str, Any]:
        eco_points = random.randint(80, 100)
        distance = random.randint(15, 35)
        time_estimate = random.randint(25, 65)
        
        return {
            'route': f"Eco-friendly route from {start} to {end}",
            'estimated_time': f"{time_estimate} minutes",
            'distance': f"{distance} km",
            'eco_points': eco_points,
            'recommended': True,
            'route_type': 'eco',
            'details': 'Minimizes environmental impact'
        }

class BalancedRoute(RouteStrategy):
    """Стратегия сбалансированного маршрута"""
    def find_route(self, start: str, end: str, **params) -> Dict[str, Any]:
        distance = random.randint(12, 28)
        time_estimate = distance * 1.1
        cost = distance * 0.15  # условная стоимость
        
        return {
            'route': f"Balanced route from {start} to {end}",
            'estimated_time': f"{time_estimate:.1f} minutes",
            'distance': f"{distance:.1f} km",
            'cost': f"${cost:.2f}",
            'recommended': True,
            'route_type': 'balanced',
            'details': 'Balances time, distance, and cost'
        }

class Router:
    """Система маршрутизации"""
    def __init__(self, strategy: RouteStrategy):
        self._strategy = strategy
        self._history = []
        self._lock = threading.Lock()
    
    def set_strategy(self, strategy: RouteStrategy):
        """Изменить стратегию поиска маршрута"""
        with self._lock:
            self._strategy = strategy
    
    def find_route(self, start: str, end: str, **params) -> Dict[str, Any]:
        """Найти маршрут с использованием текущей стратегии"""
        with self._lock:
            route = self._strategy.find_route(start, end, **params)
            route['timestamp'] = time.time()
            route['strategy_used'] = self._strategy.__class__.__name__
            self._history.append(route)
            return route
    
    def find_routes_all_strategies(self, start: str, end: str, **params) -> Dict[str, Dict[str, Any]]:
        """Найти маршруты с использованием всех стратегий"""
        routes = {}
        
        strategies = {
            'fastest': FastestRoute(),
            'shortest': ShortestRoute(),
            'eco': EcoRoute(),
            'balanced': BalancedRoute()
        }
        
        for name, strategy in strategies.items():
            routes[name] = strategy.find_route(start, end, **params)
        
        return routes
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Получить историю поиска маршрутов"""
        with self._lock:
            return self._history.copy()

# Решение задания 5: Комбинированные стратегии
class DataProcessingStrategy(ABC):
    """Интерфейс стратегии обработки данных"""
    @abstractmethod
    def process(self, data: List[Any]) -> List[Any]:
        pass

class SortStrategy(DataProcessingStrategy):
    """Стратегия сортировки данных"""
    def __init__(self, reverse: bool = False):
        self.reverse = reverse
    
    def process(self, data: List[Any]) -> List[Any]:
        return sorted(data, reverse=self.reverse)

class FilterStrategy(DataProcessingStrategy):
    """Стратегия фильтрации данных"""
    def __init__(self, condition: Callable[[Any], bool]):
        self.condition = condition
    
    def process(self, data: List[Any]) -> List[Any]:
        return [item for item in data if self.condition(item)]

class TransformStrategy(DataProcessingStrategy):
    """Стратегия трансформации данных"""
    def __init__(self, transform_func: Callable[[Any], Any]):
        self.transform_func = transform_func
    
    def process(self, data: List[Any]) -> List[Any]:
        return [self.transform_func(item) for item in data]

class AggregateStrategy(DataProcessingStrategy):
    """Стратегия агрегации данных"""
    def __init__(self, aggregation_func: Callable[[List[Any]], Any]):
        self.aggregation_func = aggregation_func
    
    def process(self, data: List[Any]) -> List[Any]:
        if not data:
            return []
        result = self.aggregation_func(data)
        return [result]

class CompositeStrategy(DataProcessingStrategy):
    """Комбинированная стратегия для последовательной обработки"""
    def __init__(self):
        self.strategies = []
        self._lock = threading.Lock()
    
    def add_strategy(self, strategy: DataProcessingStrategy):
        """Добавить стратегию в цепочку"""
        with self._lock:
            self.strategies.append(strategy)
    
    def remove_strategy(self, strategy: DataProcessingStrategy):
        """Удалить стратегию из цепочки"""
        with self._lock:
            if strategy in self.strategies:
                self.strategies.remove(strategy)
    
    def clear_strategies(self):
        """Очистить все стратегии"""
        with self._lock:
            self.strategies.clear()
    
    def process(self, data: List[Any]) -> List[Any]:
        """Последовательно применить все стратегии"""
        with self._lock:
            result = data
            for strategy in self.strategies:
                result = strategy.process(result)
            return result

class DataProcessor:
    """Обработчик данных"""
    def __init__(self, strategy: DataProcessingStrategy):
        self._strategy = strategy
        self._history = []
        self._lock = threading.Lock()
    
    def set_strategy(self, strategy: DataProcessingStrategy):
        """Установить новую стратегию обработки"""
        with self._lock:
            self._strategy = strategy
    
    def process(self, data: List[Any]) -> List[Any]:
        """Обработать данные с использованием текущей стратегии"""
        with self._lock:
            start_time = time.time()
            result = self._strategy.process(data)
            end_time = time.time()
            
            self._history.append({
                'input_data': data.copy(),
                'output_data': result.copy(),
                'processing_time': end_time - start_time,
                'strategy_used': self._strategy.__class__.__name__,
                'timestamp': time.time()
            })
            
            return result
    
    def get_history(self) -> List[Dict[str, Any]]:
        """Получить историю обработки данных"""
        with self._lock:
            return self._history.copy()

# Дополнительные примеры использования паттерна Strategy
class PaymentStrategy(ABC):
    """Стратегия оплаты"""
    @abstractmethod
    def pay(self, amount: float) -> Dict[str, Any]:
        pass

class CreditCardPayment(PaymentStrategy):
    """Оплата кредитной картой"""
    def __init__(self, card_number: str, cvv: str):
        self.card_number = card_number
        self.cvv = cvv
    
    def pay(self, amount: float) -> Dict[str, Any]:
        return {
            'success': True,
            'amount': amount,
            'method': 'Credit Card',
            'last_four_digits': self.card_number[-4:],
            'transaction_id': f'CC{random.randint(10000, 99999)}'
        }

class PayPalPayment(PaymentStrategy):
    """Оплата через PayPal"""
    def __init__(self, email: str):
        self.email = email
    
    def pay(self, amount: float) -> Dict[str, Any]:
        return {
            'success': True,
            'amount': amount,
            'method': 'PayPal',
            'email': self.email,
            'transaction_id': f'PP{random.randint(10000, 99999)}'
        }

class BitcoinPayment(PaymentStrategy):
    """Оплата биткоинами"""
    def __init__(self, wallet_address: str):
        self.wallet_address = wallet_address
    
    def pay(self, amount: float) -> Dict[str, Any]:
        return {
            'success': True,
            'amount': amount,
            'method': 'Bitcoin',
            'address': self.wallet_address[:10] + '...',
            'transaction_id': f'BT{random.randint(10000, 99999)}'
        }

class PaymentProcessor:
    """Процессор оплаты"""
    def __init__(self, strategy: PaymentStrategy):
        self._strategy = strategy
    
    def set_strategy(self, strategy: PaymentStrategy):
        self._strategy = strategy
    
    def process_payment(self, amount: float) -> Dict[str, Any]:
        return self._strategy.pay(amount)

def demonstrate_strategy_patterns():
    """Демонстрация различных паттернов Strategy"""
    print("=== Демонстрация паттернов Strategy ===")
    
    # Сортировка
    print("\n1. Стратегии сортировки:")
    data = [64, 34, 25, 12, 22, 11, 90, 5, 77, 30]
    print(f"Исходные данные: {data}")
    
    sorter = Sorter(BubbleSort())
    print(f"BubbleSort: {sorter.sort(data)[:5]}...")  # Показываем первые 5
    
    sorter.set_strategy(QuickSort())
    print(f"QuickSort: {sorter.sort(data)[:5]}...")
    
    sorter.set_strategy(MergeSort())
    print(f"MergeSort: {sorter.sort(data)[:5]}...")
    
    sorter.set_strategy(HeapSort())
    print(f"HeapSort: {sorter.sort(data)[:5]}...")
    
    # Налоги
    print("\n2. Финансовые стратегии (налоги):")
    calculator = TaxCalculator(ProgressiveTax())
    income = 60000
    tax = calculator.calculate(income)
    print(f"Доход: ${income}, Налог (прогрессивный): ${tax:.2f}")
    
    calculator.set_strategy(FlatTax(0.15))
    tax = calculator.calculate(income)
    print(f"Доход: ${income}, Налог (плоский): ${tax:.2f}")
    
    calculator.set_strategy(DeductibleTax(0.13, 10000))
    tax = calculator.calculate(income)
    print(f"Доход: ${income}, Налог (с вычетом): ${tax:.2f}")
    
    # Сжатие
    print("\n3. Стратегии сжатия:")
    compressor = Compressor(ZipCompression())
    text = "Это длинный текст для сжатия. " * 10
    result = compressor.compress(text, compression_level=9)
    print(f"ZIP сжатие: {result}")
    
    # Маршруты
    print("\n4. Стратегии маршрутов:")
    router = Router(FastestRoute())
    route = router.find_route("Москва", "Санкт-Петербург")
    print(f"Быстрый маршрут: {route['route_type']} - {route['estimated_time']}")
    
    # Комбинированные стратегии
    print("\n5. Комбинированные стратегии:")
    data = [5, 2, 8, 1, 9, 3, 7, 4, 6]
    print(f"Исходные данные: {data}")
    
    composite_strategy = CompositeStrategy()
    composite_strategy.add_strategy(FilterStrategy(lambda x: x > 3))
    composite_strategy.add_strategy(SortStrategy())
    composite_strategy.add_strategy(TransformStrategy(lambda x: x * 2))
    
    processor = DataProcessor(composite_strategy)
    result = processor.process(data)
    print(f"Результат: {result}")
    
    # Оплаты
    print("\n6. Стратегии оплаты:")
    processor = PaymentProcessor(CreditCardPayment("1234567890123456", "123"))
    payment_result = processor.process_payment(100.50)
    print(f"Оплата кредитной картой: {payment_result}")

def compare_strategy_implementations():
    """Сравнение различных реализаций Strategy"""
    print("\n=== Сравнение реализаций Strategy ===")
    print("""
    1. Классический Strategy:
       + Четкое разделение алгоритмов
       + Легкая замена стратегий в рантайме
       + Удовлетворяет принципу открытости/закрытости
       - Может привести к увеличению количества классов
       - Требует заранее известного набора алгоритмов
    
    2. Strategy с параметрами:
       + Повышенная гибкость за счет параметров
       + Меньше классов по сравнению с вариациями алгоритмов
       - Сложнее в реализации
       - Параметры могут усложнить интерфейс
    
    3. Комбинированные стратегии:
       + Высокая гибкость и повторное использование
       + Возможность создания сложных алгоритмов из простых
       - Более сложная логика
       - Требует тщательного тестирования
    
    4. Динамическое изменение стратегии:
       + Возможность адаптации в рантайме
       + Поддержка контекстно-зависимого выбора
       - Требует синхронизации в многопоточной среде
       - Может усложнить логику приложения
    """)

# Примеры использования:
if __name__ == "__main__":
    print("=== Решения для практического занятия 16 ===")
    
    print("\n1. Решение задания 1: Базовая реализация Strategy")
    data = [64, 34, 25, 12, 22, 11, 90]
    print(f"Исходные данные: {data}")
    
    sorter = Sorter(BubbleSort())
    print(f"Сортировка пузырьком: {sorter.sort(data)}")
    
    sorter.set_strategy(QuickSort())
    print(f"Быстрая сортировка: {sorter.sort(data)}")
    
    sorter.set_strategy(MergeSort())
    print(f"Сортировка слиянием: {sorter.sort(data)}")
    
    print(f"Текущая стратегия: {sorter.get_strategy_name()}")
    
    print("\n2. Решение задания 2: Финансовые стратегии")
    calculator = TaxCalculator(ProgressiveTax())
    income = 60000
    tax = calculator.calculate(income)
    print(f"Доход: ${income}, Налог (прогрессивный): ${tax:.2f}")
    
    calculator.set_strategy(FlatTax(0.15))
    tax = calculator.calculate(income)
    print(f"Доход: ${income}, Налог (плоский): ${tax:.2f}")
    
    print(f"История расчетов: {len(calculator.get_history())} записей")
    
    print("\n3. Решение задания 3: Стратегии с параметрами")
    compressor = Compressor(ZipCompression())
    text = "Это длинный текст для сжатия. " * 10
    result = compressor.compress(text, compression_level=9)
    print(f"ZIP сжатие: {result}")
    
    # Сравнение стратегий сжатия
    benchmark_results = compressor.benchmark_compression(text, compression_level=7)
    print("Сравнение стратегий сжатия:")
    for format_name, result in benchmark_results.items():
        print(f"  {format_name}: коэффициент {result['compression_ratio']:.2f}, время {result['compression_time']:.4f}с")
    
    print("\n4. Решение задания 4: Динамическое изменение стратегии")
    router = Router(FastestRoute())
    route = router.find_route("Москва", "Санкт-Петербург")
    print(f"Быстрый маршрут: {route['route_type']} - {route['estimated_time']}")
    
    router.set_strategy(ShortestRoute())
    route = router.find_route("Москва", "Санкт-Петербург")
    print(f"Кратчайший маршрут: {route['route_type']} - {route['distance']}")
    
    router.set_strategy(EcoRoute())
    route = router.find_route("Москва", "Санкт-Петербург")
    print(f"Экологичный маршрут: {route['route_type']} - {route['eco_points']} очков")
    
    # Сравнение всех стратегий
    all_routes = router.find_routes_all_strategies("Москва", "Санкт-Петербург")
    print("Сравнение всех стратегий маршрутов:")
    for route_type, route_info in all_routes.items():
        print(f"  {route_type}: {route_info['estimated_time']}")
    
    print("\n5. Решение задания 5: Комбинированные стратегии")
    data = [5, 2, 8, 1, 9, 3, 7, 4, 6]
    print(f"Исходные данные: {data}")
    
    # Создаем комбинированную стратегию: фильтрация -> сортировка -> трансформация
    composite_strategy = CompositeStrategy()
    composite_strategy.add_strategy(FilterStrategy(lambda x: x > 3))
    composite_strategy.add_strategy(SortStrategy())
    composite_strategy.add_strategy(TransformStrategy(lambda x: x * 2))
    
    processor = DataProcessor(composite_strategy)
    result = processor.process(data)
    print(f"Фильтрация (>3), сортировка, удвоение: {result}")
    
    print(f"История обработки: {len(processor.get_history())} записей")
    
    print("\n6. Дополнительные примеры")
    demonstrate_strategy_patterns()
    compare_strategy_implementations()