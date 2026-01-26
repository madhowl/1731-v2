# Решения для практического занятия 14: ООП - паттерн Factory

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Type
import time
import threading
from enum import Enum

# Решение задания 1: Простая фабрика
class Vehicle(ABC):
    """Абстрактный класс транспортного средства"""
    @abstractmethod
    def drive(self) -> str:
        pass

class Car(Vehicle):
    def drive(self) -> str:
        return "Вождение автомобиля"

class Motorcycle(Vehicle):
    def drive(self) -> str:
        return "Вождение мотоцикла"

class Truck(Vehicle):
    def drive(self) -> str:
        return "Вождение грузовика"

class VehicleFactory:
    """Фабрика для создания транспортных средств"""
    _vehicles = {
        "car": Car,
        "motorcycle": Motorcycle,
        "truck": Truck
    }
    
    @classmethod
    def register_vehicle(cls, vehicle_type: str, vehicle_class: Type[Vehicle]):
        """Регистрация нового типа транспортного средства"""
        cls._vehicles[vehicle_type] = vehicle_class
    
    @classmethod
    def create_vehicle(cls, vehicle_type: str) -> Vehicle:
        if vehicle_type.lower() not in cls._vehicles:
            raise ValueError(f"Неизвестный тип транспортного средства: {vehicle_type}")
        
        vehicle_class = cls._vehicles[vehicle_type.lower()]
        return vehicle_class()

# Решение задания 2: Фабричный метод
class Document(ABC):
    """Абстрактный класс документа"""
    @abstractmethod
    def create(self) -> str:
        pass

class PDFDocument(Document):
    def create(self) -> str:
        return "Создание PDF документа"

class WordDocument(Document):
    def create(self) -> str:
        return "Создание Word документа"

class ExcelDocument(Document):
    def create(self) -> str:
        return "Создание Excel документа"

class DocumentCreator(ABC):
    """Абстрактный класс создателя документов"""
    @abstractmethod
    def create_document(self) -> Document:
        pass
    
    def save_document(self) -> str:
        document = self.create_document()
        return f"Сохранение: {document.create()}"
    
    def preview_document(self) -> str:
        document = self.create_document()
        return f"Предварительный просмотр: {document.create()}"

class PDFDocumentCreator(DocumentCreator):
    def create_document(self) -> Document:
        return PDFDocument()

class WordDocumentCreator(DocumentCreator):
    def create_document(self) -> Document:
        return WordDocument()

class ExcelDocumentCreator(DocumentCreator):
    def create_document(self) -> Document:
        return ExcelDocument()

# Решение задания 3: Абстрактная фабрика
class Button(ABC):
    """Абстрактный класс кнопки"""
    @abstractmethod
    def render(self) -> str:
        pass

class TextField(ABC):
    """Абстрактный класс текстового поля"""
    @abstractmethod
    def render(self) -> str:
        pass

class WindowsButton(Button):
    def render(self) -> str:
        return "Отображение Windows кнопки"

class WindowsTextField(TextField):
    def render(self) -> str:
        return "Отображение Windows текстового поля"

class MacButton(Button):
    def render(self) -> str:
        return "Отображение Mac кнопки"

class MacTextField(TextField):
    def render(self) -> str:
        return "Отображение Mac текстового поля"

class LinuxButton(Button):
    def render(self) -> str:
        return "Отображение Linux кнопки"

class LinuxTextField(TextField):
    def render(self) -> str:
        return "Отображение Linux текстового поля"

class UIFactory(ABC):
    """Абстрактная фабрика UI элементов"""
    @abstractmethod
    def create_button(self) -> Button:
        pass
    
    @abstractmethod
    def create_text_field(self) -> TextField:
        pass
    
    def create_form(self) -> Dict[str, Any]:
        """Создание формы из элементов"""
        return {
            "button": self.create_button(),
            "text_field": self.create_text_field()
        }

class WindowsUIFactory(UIFactory):
    def create_button(self) -> Button:
        return WindowsButton()
    
    def create_text_field(self) -> TextField:
        return WindowsTextField()

class MacUIFactory(UIFactory):
    def create_button(self) -> Button:
        return MacButton()
    
    def create_text_field(self) -> TextField:
        return MacTextField()

class LinuxUIFactory(UIFactory):
    def create_button(self) -> Button:
        return LinuxButton()
    
    def create_text_field(self) -> TextField:
        return LinuxTextField()

# Решение задания 4: Параметризованная фабрика
class Shape(ABC):
    """Абстрактный класс фигуры"""
    def __init__(self, color: str, size: float):
        self.color = color
        self.size = size
    
    @abstractmethod
    def draw(self) -> str:
        pass

class Circle(Shape):
    def draw(self) -> str:
        return f"Рисование {self.color} круга размером {self.size}"

class Rectangle(Shape):
    def draw(self) -> str:
        return f"Рисование {self.color} прямоугольника размером {self.size}"

class Triangle(Shape):
    def draw(self) -> str:
        return f"Рисование {self.color} треугольника размером {self.size}"

class ShapeFactory:
    """Фабрика для создания фигур с параметрами"""
    _shapes = {
        "circle": Circle,
        "rectangle": Rectangle,
        "triangle": Triangle
    }
    
    @classmethod
    def register_shape(cls, shape_type: str, shape_class: Type[Shape]):
        """Регистрация нового типа фигуры"""
        cls._shapes[shape_type] = shape_class
    
    @classmethod
    def create_shape(cls, shape_type: str, color: str = "white", size: float = 1.0) -> Shape:
        if size <= 0:
            raise ValueError("Размер должен быть положительным")
        
        if shape_type.lower() not in cls._shapes:
            raise ValueError(f"Неизвестный тип фигуры: {shape_type}")
        
        shape_class = cls._shapes[shape_type.lower()]
        return shape_class(color, size)

# Решение задания 5: Фабрика с кэшированием
class ObjectPoolFactory:
    """Фабрика с пулом объектов для повторного использования"""
    def __init__(self):
        self._available_objects = {}
        self._used_objects = {}
        self._object_creation_time = {}
        self._lock = threading.Lock()
    
    def get_object(self, obj_type: str, *args, **kwargs):
        """Получить объект из пула или создать новый"""
        with self._lock:
            if obj_type not in self._available_objects:
                self._available_objects[obj_type] = []
            
            if self._available_objects[obj_type]:
                # Возвращаем доступный объект из пула
                obj = self._available_objects[obj_type].pop()
                self._used_objects.setdefault(obj_type, []).append(obj)
                return obj
            else:
                # Создаем новый объект
                if obj_type == "car":
                    obj = Car()
                elif obj_type == "pdf_doc":
                    obj = PDFDocument()
                elif obj_type == "circle":
                    obj = Circle("red", 1.0)
                elif obj_type == "rectangle":
                    obj = Rectangle("blue", 2.0)
                elif obj_type == "triangle":
                    obj = Triangle("green", 1.5)
                else:
                    raise ValueError(f"Неизвестный тип объекта: {obj_type}")
                
                self._used_objects.setdefault(obj_type, []).append(obj)
                self._object_creation_time[id(obj)] = time.time()
                return obj
    
    def return_object(self, obj_type: str, obj) -> bool:
        """Вернуть объект в пул"""
        with self._lock:
            if obj_type in self._used_objects and obj in self._used_objects[obj_type]:
                self._used_objects[obj_type].remove(obj)
                self._available_objects[obj_type].append(obj)
                return True
            return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Получить статистику использования пула"""
        with self._lock:
            stats = {}
            for obj_type in self._available_objects:
                stats[obj_type] = {
                    'available': len(self._available_objects.get(obj_type, [])),
                    'used': len(self._used_objects.get(obj_type, []))
                }
            return stats
    
    def cleanup_old_objects(self, max_age_seconds: int = 60):
        """Очистка старых объектов из пула"""
        current_time = time.time()
        with self._lock:
            for obj_type in list(self._available_objects.keys()):
                for obj in list(self._available_objects[obj_type]):
                    creation_time = self._object_creation_time.get(id(obj), 0)
                    if current_time - creation_time > max_age_seconds:
                        self._available_objects[obj_type].remove(obj)
                        if id(obj) in self._object_creation_time:
                            del self._object_creation_time[id(obj)]

# Дополнительные примеры использования фабрик
class PaymentProcessor(ABC):
    """Абстрактный процессор платежей"""
    @abstractmethod
    def process_payment(self, amount: float) -> str:
        pass

class CreditCardProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> str:
        return f"Обработка платежа по кредитной карте на сумму {amount}$"

class PayPalProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> str:
        return f"Обработка платежа через PayPal на сумму {amount}$"

class CryptoProcessor(PaymentProcessor):
    def process_payment(self, amount: float) -> str:
        return f"Обработка криптовалютного платежа на сумму {amount}$"

class PaymentFactory:
    """Фабрика для создания процессоров платежей"""
    _processors = {
        "credit_card": CreditCardProcessor,
        "paypal": PayPalProcessor,
        "crypto": CryptoProcessor
    }
    
    @classmethod
    def create_processor(cls, processor_type: str) -> PaymentProcessor:
        if processor_type.lower() not in cls._processors:
            raise ValueError(f"Неизвестный тип процессора: {processor_type}")
        
        processor_class = cls._processors[processor_type.lower()]
        return processor_class()

def demonstrate_factory_patterns():
    """Демонстрация различных паттернов фабрики"""
    print("=== Демонстрация паттернов фабрики ===")
    
    # Простая фабрика
    print("\n1. Простая фабрика (VehicleFactory):")
    vehicle_factory = VehicleFactory()
    car = vehicle_factory.create_vehicle("car")
    motorcycle = vehicle_factory.create_vehicle("motorcycle")
    print(f"  {car.drive()}")
    print(f"  {motorcycle.drive()}")
    
    # Фабричный метод
    print("\n2. Фабричный метод (DocumentCreator):")
    creators = [PDFDocumentCreator(), WordDocumentCreator(), ExcelDocumentCreator()]
    for creator in creators:
        print(f"  {creator.save_document()}")
    
    # Абстрактная фабрика
    print("\n3. Абстрактная фабрика (UIFactory):")
    factories = {
        "windows": WindowsUIFactory(),
        "mac": MacUIFactory(),
        "linux": LinuxUIFactory()
    }
    
    for os_name, factory in factories.items():
        form = factory.create_form()
        print(f"  {os_name}: {form['button'].render()}, {form['text_field'].render()}")
    
    # Параметризованная фабрика
    print("\n4. Параметризованная фабрика (ShapeFactory):")
    shape_factory = ShapeFactory()
    circle = shape_factory.create_shape("circle", "красный", 5.0)
    rectangle = shape_factory.create_shape("rectangle", "синий", 10.0)
    triangle = shape_factory.create_shape("triangle", "зеленый", 7.5)
    print(f"  {circle.draw()}")
    print(f"  {rectangle.draw()}")
    print(f"  {triangle.draw()}")
    
    # Фабрика с кэшированием
    print("\n5. Фабрика с кэшированием (ObjectPoolFactory):")
    pool = ObjectPoolFactory()
    
    # Получаем объекты
    obj1 = pool.get_object("car")
    obj2 = pool.get_object("car")
    print(f"  Получено 2 объекта, статус пула: {pool.get_stats()}")
    
    # Возвращаем один объект
    pool.return_object("car", obj1)
    print(f"  Вернули 1 объект, статус пула: {pool.get_stats()}")
    
    # Получаем еще один объект (должен получить возвращенный)
    obj3 = pool.get_object("car")
    print(f"  Получили 3-й объект, статус пула: {pool.get_stats()}")
    
    # Фабрика платежей
    print("\n6. Дополнительный пример - PaymentFactory:")
    payment_types = ["credit_card", "paypal", "crypto"]
    for payment_type in payment_types:
        processor = PaymentFactory.create_processor(payment_type)
        print(f"  {processor.process_payment(100.0)}")

def compare_factory_implementations():
    """Сравнение различных реализаций фабрик"""
    print("\n=== Сравнение реализаций фабрик ===")
    print("""
    1. Простая фабрика:
       + Проста в реализации и использовании
       + Хороша для небольших приложений
       - Нарушает принцип открытости/закрытости (OCP)
       - Требует модификации при добавлении новых типов
    
    2. Фабричный метод:
       + Соблюдает принцип открытости/закрытости
       + Позволяет делегировать создание подклассам
       + Облегчает тестирование
       - Может привести к большому количеству подклассов
    
    3. Абстрактная фабрика:
       + Обеспечивает согласованность продуктов
       + Позволяет легко переключаться между семействами продуктов
       - Усложняет архитектуру
       - Требует создания большого количества классов
    
    4. Параметризованная фабрика:
       + Позволяет создавать объекты с разными свойствами
       + Гибкая и настраиваемая
       - Требует валидации параметров
       - Может усложнить отладку
    
    5. Фабрика с пулом:
       + Повышает производительность за счет переиспользования
       + Уменьшает потребление памяти
       - Усложняет управление жизненным циклом
       - Требует синхронизации в многопоточной среде
    """)

# Примеры использования:
if __name__ == "__main__":
    print("=== Решения для практического занятия 14 ===")
    
    print("\n1. Решение задания 1: Простая фабрика")
    factory = VehicleFactory()
    car = factory.create_vehicle("car")
    motorcycle = factory.create_vehicle("motorcycle")
    truck = factory.create_vehicle("truck")
    print(f"  {car.drive()}")
    print(f"  {motorcycle.drive()}")
    print(f"  {truck.drive()}")

    print("\n2. Решение задания 2: Фабричный метод")
    creators = [PDFDocumentCreator(), WordDocumentCreator(), ExcelDocumentCreator()]
    for creator in creators:
        print(f"  {creator.save_document()}")

    print("\n3. Решение задания 3: Абстрактная фабрика")
    factories = {
        "windows": WindowsUIFactory(),
        "mac": MacUIFactory(),
        "linux": LinuxUIFactory()
    }
    
    for os_name, factory in factories.items():
        button = factory.create_button()
        text_field = factory.create_text_field()
        print(f"  {os_name}: {button.render()}, {text_field.render()}")

    print("\n4. Решение задания 4: Параметризованная фабрика")
    shape_factory = ShapeFactory()
    circle = shape_factory.create_shape("circle", "красный", 5.0)
    rectangle = shape_factory.create_shape("rectangle", "синий", 10.0)
    print(f"  {circle.draw()}")
    print(f"  {rectangle.draw()}")

    print("\n5. Решение задания 5: Фабрика с кэшированием")
    pool = ObjectPoolFactory()
    
    # Получаем объекты
    obj1 = pool.get_object("car")
    obj2 = pool.get_object("car")
    print(f"  Получено 2 объекта, статус пула: {pool.get_stats()}")
    
    # Возвращаем один объект
    pool.return_object("car", obj1)
    print(f"  Вернули 1 объект, статус пула: {pool.get_stats()}")
    
    # Получаем еще один объект (должен получить возвращенный)
    obj3 = pool.get_object("car")
    print(f"  Получили 3-й объект, статус пула: {pool.get_stats()}")
    
    print("\n6. Дополнительные примеры")
    demonstrate_factory_patterns()
    compare_factory_implementations()