# Решения для практического занятия 11: ООП - абстрактные классы и интерфейсы

from abc import ABC, abstractmethod
import math
from typing import List

# Решение задания 1: Создание абстрактного класса Shape
class Shape(ABC):
    """Абстрактный класс для геометрических фигур"""
    
    @abstractmethod
    def area(self) -> float:
        """Абстрактный метод для вычисления площади"""
        pass
    
    @abstractmethod
    def perimeter(self) -> float:
        """Абстрактный метод для вычисления периметра"""
        pass
    
    def description(self) -> str:
        """Конкретный метод для описания фигуры"""
        return f"Это {self.__class__.__name__} с площадью {self.area():.2f} и периметром {self.perimeter():.2f}"

# Решение задания 2: Интерфейс Drawable
class Drawable(ABC):
    """Интерфейс для отрисовки объектов"""
    
    @abstractmethod
    def draw(self) -> str:
        """Абстрактный метод для отрисовки"""
        pass

# Расширим классы фигур, чтобы реализовать интерфейс Drawable
class Circle(Shape, Drawable):
    """Класс круга"""
    def __init__(self, radius: float):
        if radius <= 0:
            raise ValueError("Радиус должен быть положительным")
        self.radius = radius
    
    def area(self) -> float:
        return math.pi * self.radius ** 2
    
    def perimeter(self) -> float:
        return 2 * math.pi * self.radius
    
    def draw(self) -> str:
        return f"Рисуем круг с радиусом {self.radius}"

class Rectangle(Shape, Drawable):
    """Класс прямоугольника"""
    def __init__(self, width: float, height: float):
        if width <= 0 or height <= 0:
            raise ValueError("Ширина и высота должны быть положительными")
        self.width = width
        self.height = height
    
    def area(self) -> float:
        return self.width * self.height
    
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)
    
    def draw(self) -> str:
        return f"Рисуем прямоугольник {self.width}x{self.height}"

class Triangle(Shape, Drawable):
    """Класс треугольника (произвольного)"""
    def __init__(self, a: float, b: float, c: float):
        # Проверяем неравенство треугольника
        if a + b <= c or a + c <= b or b + c <= a:
            raise ValueError("Нарушено неравенство треугольника")
        if a <= 0 or b <= 0 or c <= 0:
            raise ValueError("Стороны должны быть положительными")
        self.a = a
        self.b = b
        self.c = c
    
    def area(self) -> float:
        # Используем формулу Герона
        s = self.perimeter() / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))
    
    def perimeter(self) -> float:
        return self.a + self.b + self.c
    
    def draw(self) -> str:
        return f"Рисуем треугольник со сторонами {self.a}, {self.b}, {self.c}"

# Решение задания 3: Абстрактный класс Animal
class Animal(ABC):
    """Абстрактный класс животного"""
    
    def __init__(self, name: str):
        self.name = name
    
    @abstractmethod
    def make_sound(self) -> str:
        """Абстрактный метод для издавания звука"""
        pass
    
    @abstractmethod
    def move(self) -> str:
        """Абстрактный метод для передвижения"""
        pass
    
    def sleep(self) -> str:
        """Конкретный метод для сна"""
        return f"{self.name} спит"

# Реализация конкретных животных
class Dog(Animal):
    def make_sound(self) -> str:
        return f"{self.name} говорит: Гав-гав!"
    
    def move(self) -> str:
        return f"{self.name} бегает на четырех лапах"

class Cat(Animal):
    def make_sound(self) -> str:
        return f"{self.name} говорит: Мяу!"
    
    def move(self) -> str:
        return f"{self.name} движется с грацией"

class Bird(Animal):
    def make_sound(self) -> str:
        return f"{self.name} поет: Чирик-чирик!"
    
    def move(self) -> str:
        return f"{self.name} летает в небе"

# Решение задания 4: Система платежей
class PaymentMethod(ABC):
    """Абстрактный класс для метода оплаты"""
    
    @abstractmethod
    def pay(self, amount: float) -> str:
        """Абстрактный метод для оплаты"""
        pass

class CreditCard(PaymentMethod):
    def __init__(self, card_number: str, cvv: str):
        if len(card_number) != 16 or not card_number.isdigit():
            raise ValueError("Номер карты должен содержать 16 цифр")
        if len(cvv) != 3 or not cvv.isdigit():
            raise ValueError("CVV должен содержать 3 цифры")
        self.card_number = card_number
        self.cvv = cvv
    
    def pay(self, amount: float) -> str:
        if amount <= 0:
            raise ValueError("Сумма оплаты должна быть положительной")
        return f"Оплата {amount:.2f} руб. по кредитной карте ****{self.card_number[-4:]} выполнена успешно"

class PayPal(PaymentMethod):
    def __init__(self, email: str):
        if "@" not in email or "." not in email:
            raise ValueError("Некорректный email")
        self.email = email
    
    def pay(self, amount: float) -> str:
        if amount <= 0:
            raise ValueError("Сумма оплаты должна быть положительной")
        return f"Оплата {amount:.2f} руб. через PayPal ({self.email}) выполнена успешно"

class BankTransfer(PaymentMethod):
    def __init__(self, account_number: str):
        self.account_number = account_number
    
    def pay(self, amount: float) -> str:
        if amount <= 0:
            raise ValueError("Сумма оплаты должна быть положительной")
        return f"Оплата {amount:.2f} руб. по банковскому переводу на счёт {self.account_number} выполнена успешно"

# Дополнительные примеры использования абстрактных классов
class Vehicle(ABC):
    """Абстрактный класс транспортного средства"""
    def __init__(self, brand: str, model: str):
        self.brand = brand
        self.model = model
    
    @abstractmethod
    def start_engine(self) -> str:
        pass
    
    @abstractmethod
    def stop_engine(self) -> str:
        pass
    
    def get_info(self) -> str:
        return f"{self.brand} {self.model}"

class Car(Vehicle):
    def start_engine(self) -> str:
        return f"Двигатель автомобиля {self.get_info()} запущен"
    
    def stop_engine(self) -> str:
        return f"Двигатель автомобиля {self.get_info()} остановлен"

class Motorcycle(Vehicle):
    def start_engine(self) -> str:
        return f"Мотоцикл {self.get_info()} готов к поездке"
    
    def stop_engine(self) -> str:
        return f"Мотоцикл {self.get_info()} остановлен"

def process_shapes(shapes: List[Shape]) -> None:
    """Функция для обработки списка фигур"""
    total_area = sum(shape.area() for shape in shapes)
    total_perimeter = sum(shape.perimeter() for shape in shapes)
    print(f"Общая площадь всех фигур: {total_area:.2f}")
    print(f"Общий периметр всех фигур: {total_perimeter:.2f}")

def draw_all_drawables(drawables: List[Drawable]) -> None:
    """Функция для отрисовки всех объектов, реализующих интерфейс Drawable"""
    for drawable in drawables:
        print(drawable.draw())

def process_payments(methods: List[PaymentMethod], amounts: List[float]) -> None:
    """Функция для обработки платежей разными методами"""
    for method, amount in zip(methods, amounts):
        try:
            result = method.pay(amount)
            print(result)
        except ValueError as e:
            print(f"Ошибка при оплате {amount:.2f} руб.: {e}")

# Примеры использования:
if __name__ == "__main__":
    print("=== Решения для практического занятия 11 ===")
    
    print("\n1. Решение задания 1: Абстрактный класс Shape")
    shapes = [
        Circle(5),
        Rectangle(4, 6),
        Triangle(3, 4, 5)
    ]
    
    for shape in shapes:
        print(shape.description())
    
    print("\n2. Решение задания 2: Интерфейс Drawable")
    drawables = [Circle(3), Rectangle(2, 4), Triangle(3, 4, 5)]
    draw_all_drawables(drawables)
    
    print("\n3. Решение задания 3: Абстрактный класс Animal")
    animals = [
        Dog("Бобик"),
        Cat("Мурка"),
        Bird("Чижик")
    ]
    
    for animal in animals:
        print(animal.make_sound())
        print(animal.move())
        print(animal.sleep())
        print()
    
    print("\n4. Решение задания 4: Система платежей")
    payment_methods = [
        CreditCard("1234567890123456", "123"),
        PayPal("user@example.com"),
        BankTransfer("RU12345678901234567890")
    ]
    
    amounts = [100.50, 250.00, 50.25]
    process_payments(payment_methods, amounts)
    
    print("\n5. Дополнительные примеры")
    print("Обработка списка фигур:")
    process_shapes([Circle(2), Rectangle(3, 4)])
    
    print("\nПримеры транспортных средств:")
    vehicles = [Car("Toyota", "Camry"), Motorcycle("Honda", "CBR")]
    for vehicle in vehicles:
        print(vehicle.start_engine())
        print(vehicle.stop_engine())
        print()