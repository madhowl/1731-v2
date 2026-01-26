# Упражнения для практического занятия 11: ООП - абстрактные классы и интерфейсы

from abc import ABC, abstractmethod
import math

# Задание 1: Создание абстрактного класса Shape
class Shape(ABC):
    """Абстрактный класс для геометрических фигур"""
    
    @abstractmethod
    def area(self):
        """Абстрактный метод для вычисления площади"""
        pass
    
    @abstractmethod
    def perimeter(self):
        """Абстрактный метод для вычисления периметра"""
        pass
    
    def description(self):
        """Конкретный метод для описания фигуры"""
        return f"Это {self.__class__.__name__} с площадью {self.area():.2f} и периметром {self.perimeter():.2f}"

# Задание 2: Интерфейс Drawable
class Drawable(ABC):
    """Интерфейс для отрисовки объектов"""
    
    @abstractmethod
    def draw(self):
        """Абстрактный метод для отрисовки"""
        pass

# Реализация конкретных фигур
class Circle(Shape):
    """Класс круга"""
    def __init__(self, radius):
        self.radius = radius
    
    def area(self):
        return math.pi * self.radius ** 2
    
    def perimeter(self):
        return 2 * math.pi * self.radius

class Rectangle(Shape):
    """Класс прямоугольника"""
    def __init__(self, width, height):
        self.width = width
        self.height = height
    
    def area(self):
        return self.width * self.height
    
    def perimeter(self):
        return 2 * (self.width + self.height)

class Triangle(Shape):
    """Класс треугольника (прямоугольного)"""
    def __init__(self, base, height):
        self.base = base
        self.height = height
        # Для упрощения считаем, что это прямоугольный треугольник
        self.hypotenuse = math.sqrt(base**2 + height**2)
    
    def area(self):
        return 0.5 * self.base * self.height
    
    def perimeter(self):
        return self.base + self.height + self.hypotenuse

# Задание 3: Абстрактный класс Animal
class Animal(ABC):
    """Абстрактный класс животного"""
    
    def __init__(self, name):
        self.name = name
    
    @abstractmethod
    def make_sound(self):
        """Абстрактный метод для издавания звука"""
        pass
    
    @abstractmethod
    def move(self):
        """Абстрактный метод для передвижения"""
        pass
    
    def sleep(self):
        """Конкретный метод для сна"""
        return f"{self.name} спит"

# Реализация конкретных животных
class Dog(Animal):
    def make_sound(self):
        return f"{self.name} говорит: Гав-гав!"
    
    def move(self):
        return f"{self.name} бегает на четырех лапах"

class Cat(Animal):
    def make_sound(self):
        return f"{self.name} говорит: Мяу!"
    
    def move(self):
        return f"{self.name} движется с грацией"

class Bird(Animal):
    def make_sound(self):
        return f"{self.name} поет: Чирик-чирик!"
    
    def move(self):
        return f"{self.name} летает в небе"

# Задание 4: Система платежей
class PaymentMethod(ABC):
    """Абстрактный класс для метода оплаты"""
    
    @abstractmethod
    def pay(self, amount):
        """Абстрактный метод для оплаты"""
        pass

class CreditCard(PaymentMethod):
    def __init__(self, card_number, cvv):
        self.card_number = card_number
        self.cvv = cvv
    
    def pay(self, amount):
        if amount <= 0:
            raise ValueError("Сумма оплаты должна быть положительной")
        return f"Оплата {amount:.2f} руб. по кредитной карте ****{self.card_number[-4:]} выполнена успешно"

class PayPal(PaymentMethod):
    def __init__(self, email):
        self.email = email
    
    def pay(self, amount):
        if amount <= 0:
            raise ValueError("Сумма оплаты должна быть положительной")
        return f"Оплата {amount:.2f} руб. через PayPal ({self.email}) выполнена успешно"

class BankTransfer(PaymentMethod):
    def __init__(self, account_number):
        self.account_number = account_number
    
    def pay(self, amount):
        if amount <= 0:
            raise ValueError("Сумма оплаты должна быть положительной")
        return f"Оплата {amount:.2f} руб. по банковскому переводу на счёт {self.account_number} выполнена успешно"

# Примеры использования:
if __name__ == "__main__":
    print("=== Задание 1: Абстрактный класс Shape ===")
    shapes = [
        Circle(5),
        Rectangle(4, 6),
        Triangle(3, 4)
    ]
    
    for shape in shapes:
        print(shape.description())
    
    print("\n=== Задание 3: Абстрактный класс Animal ===")
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
    
    print("\n=== Задание 4: Система платежей ===")
    payment_methods = [
        CreditCard("1234567890123456", "123"),
        PayPal("user@example.com"),
        BankTransfer("RU12345678901234567890")
    ]
    
    for method in payment_methods:
        try:
            result = method.pay(100.50)
            print(result)
        except ValueError as e:
            print(f"Ошибка: {e}")