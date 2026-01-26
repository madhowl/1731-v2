# Упражнения для практического занятия 14: ООП - паттерн Factory

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import time

# Задание 1: Простая фабрика
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
    @staticmethod
    def create_vehicle(vehicle_type: str) -> Vehicle:
        if vehicle_type.lower() == "car":
            return Car()
        elif vehicle_type.lower() == "motorcycle":
            return Motorcycle()
        elif vehicle_type.lower() == "truck":
            return Truck()
        else:
            raise ValueError(f"Неизвестный тип транспортного средства: {vehicle_type}")

# Задание 2: Фабричный метод
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

class PDFDocumentCreator(DocumentCreator):
    def create_document(self) -> Document:
        return PDFDocument()

class WordDocumentCreator(DocumentCreator):
    def create_document(self) -> Document:
        return WordDocument()

class ExcelDocumentCreator(DocumentCreator):
    def create_document(self) -> Document:
        return ExcelDocument()

# Задание 3: Абстрактная фабрика
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

# Задание 4: Параметризованная фабрика
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
    @staticmethod
    def create_shape(shape_type: str, color: str, size: float) -> Shape:
        if size <= 0:
            raise ValueError("Размер должен быть положительным")
        
        if shape_type.lower() == "circle":
            return Circle(color, size)
        elif shape_type.lower() == "rectangle":
            return Rectangle(color, size)
        elif shape_type.lower() == "triangle":
            return Triangle(color, size)
        else:
            raise ValueError(f"Неизвестный тип фигуры: {shape_type}")

# Задание 5: Фабрика с кэшированием
class ObjectPoolFactory:
    """Фабрика с пулом объектов для повторного использования"""
    def __init__(self):
        self._available_objects = {}
        self._used_objects = {}
        self._object_creation_time = {}
    
    def get_object(self, obj_type: str, *args, **kwargs):
        """Получить объект из пула или создать новый"""
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
            else:
                raise ValueError(f"Неизвестный тип объекта: {obj_type}")
            
            self._used_objects.setdefault(obj_type, []).append(obj)
            self._object_creation_time[id(obj)] = time.time()
            return obj
    
    def return_object(self, obj_type: str, obj) -> bool:
        """Вернуть объект в пул"""
        if obj_type in self._used_objects and obj in self._used_objects[obj_type]:
            self._used_objects[obj_type].remove(obj)
            self._available_objects[obj_type].append(obj)
            return True
        return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Получить статистику использования пула"""
        stats = {}
        for obj_type in self._available_objects:
            stats[obj_type] = {
                'available': len(self._available_objects.get(obj_type, [])),
                'used': len(self._used_objects.get(obj_type, []))
            }
        return stats

# Примеры использования:
if __name__ == "__main__":
    print("=== Задание 1: Простая фабрика ===")
    factory = VehicleFactory()
    car = factory.create_vehicle("car")
    motorcycle = factory.create_vehicle("motorcycle")
    print(car.drive())
    print(motorcycle.drive())

    print("\n=== Задание 2: Фабричный метод ===")
    creators = [PDFDocumentCreator(), WordDocumentCreator(), ExcelDocumentCreator()]
    for creator in creators:
        print(creator.save_document())

    print("\n=== Задание 3: Абстрактная фабрика ===")
    factories = {
        "windows": WindowsUIFactory(),
        "mac": MacUIFactory(),
        "linux": LinuxUIFactory()
    }
    
    for os_name, factory in factories.items():
        button = factory.create_button()
        text_field = factory.create_text_field()
        print(f"{os_name}: {button.render()}, {text_field.render()}")

    print("\n=== Задание 4: Параметризованная фабрика ===")
    shape_factory = ShapeFactory()
    circle = shape_factory.create_shape("circle", "красный", 5.0)
    rectangle = shape_factory.create_shape("rectangle", "синий", 10.0)
    print(circle.draw())
    print(rectangle.draw())

    print("\n=== Задание 5: Фабрика с кэшированием ===")
    pool = ObjectPoolFactory()
    
    # Получаем объекты
    obj1 = pool.get_object("car")
    obj2 = pool.get_object("car")
    print(f"Получено 2 объекта, статус пула: {pool.get_stats()}")
    
    # Возвращаем один объект
    pool.return_object("car", obj1)
    print(f"Вернули 1 объект, статус пула: {pool.get_stats()}")
    
    # Получаем еще один объект (должен получить возвращенный)
    obj3 = pool.get_object("car")
    print(f"Получили 3-й объект, статус пула: {pool.get_stats()}")