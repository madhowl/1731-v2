# Решения упражнений для практического занятия 10: ООП - наследование и полиморфизм

"""
Этот файл содержит решения упражнений для практического занятия 10.
"""

from abc import ABC, abstractmethod
import math

class SolutionExamples:
    """
    Класс с примерами решений упражнений
    """
    
    @staticmethod
    def create_animal_hierarchy():
        """
        Создание иерархии классов животных
        """
        class Animal(ABC):
            """
            Абстрактный базовый класс для животных
            """
            def __init__(self, name, species):
                self.name = name
                self.species = species
            
            @abstractmethod
            def make_sound(self):
                pass
            
            @abstractmethod
            def move(self):
                pass
            
            def eat(self):
                return f"{self.name} ест"
            
            def sleep(self):
                return f"{self.name} спит"

        class Mammal(Animal):
            """
            Класс млекопитающих
            """
            def __init__(self, name, species, fur_color):
                super().__init__(name, species)
                self.fur_color = fur_color
            
            def give_birth(self):
                return f"{self.name} родила детенышей"
            
            def feed_milk(self):
                return f"{self.name} кормит молоком"

        class Bird(Animal):
            """
            Класс птиц
            """
            def __init__(self, name, species, wing_span):
                super().__init__(name, species)
                self.wing_span = wing_span  # Размах крыльев в см
            
            def lay_eggs(self):
                return f"{self.name} отложила яйца"
            
            def fly(self):
                return f"{self.name} летит"

        class Dog(Mammal):
            """
            Класс собаки
            """
            def __init__(self, name, breed, fur_color):
                super().__init__(name, "Собака", fur_color)
                self.breed = breed
            
            def make_sound(self):
                return f"{self.name} говорит: Гав!"
            
            def move(self):
                return f"{self.name} бегает на четырех лапах"
            
            def fetch(self):
                return f"{self.name} принесла палку"

        class Cat(Mammal):
            """
            Класс кошки
            """
            def __init__(self, name, breed, fur_color):
                super().__init__(name, "Кошка", fur_color)
                self.breed = breed
            
            def make_sound(self):
                return f"{self.name} говорит: Мяу!"
            
            def move(self):
                return f"{self.name} осторожно передвигается"
            
            def purr(self):
                return f"{self.name} мурлычет"

        class Eagle(Bird):
            """
            Класс орла
            """
            def __init__(self, name, wing_span):
                super().__init__(name, "Орел", wing_span)
            
            def make_sound(self):
                return f"{self.name} кричит: Кра!"
            
            def move(self):
                return f"{self.name} парит в небе"
            
            def hunt(self):
                return f"{self.name} охотится на лету"

        # Создание экземпляров
        dog = Dog("Бобик", "Лабрадор", "коричневый")
        cat = Cat("Мурка", "Сиамская", "белый")
        eagle = Eagle("Гром", 200)
        
        animals = [dog, cat, eagle]
        
        print("=== Иерархия классов животных ===")
        for animal in animals:
            print(f"\n{animal.name} ({animal.species}):")
            print(f"  Звук: {animal.make_sound()}")
            print(f"  Движение: {animal.move()}")
            print(f"  Цвет шерсти/оперения: {animal.fur_color if hasattr(animal, 'fur_color') else 'N/A'}")
            
            # Методы специфичные для подклассов
            if isinstance(animal, Dog):
                print(f"  Принесла палку: {animal.fetch()}")
            elif isinstance(animal, Cat):
                print(f"  Мурлычет: {animal.purr()}")
            elif isinstance(animal, Eagle):
                print(f"  Охота: {animal.hunt()}")
        
        return animals

    @staticmethod
    def create_shape_hierarchy():
        """
        Создание иерархии классов геометрических фигур
        """
        class Shape(ABC):
            """
            Абстрактный класс для геометрических фигур
            """
            def __init__(self, name):
                self.name = name
            
            @abstractmethod
            def area(self):
                pass
            
            @abstractmethod
            def perimeter(self):
                pass
            
            def describe(self):
                return f"Это {self.name} с площадью {self.area():.2f} и периметром {self.perimeter():.2f}"

        class Rectangle(Shape):
            """
            Класс прямоугольника
            """
            def __init__(self, width, height):
                super().__init__("прямоугольник")
                self.width = width
                self.height = height
            
            def area(self):
                return self.width * self.height
            
            def perimeter(self):
                return 2 * (self.width + self.height)

        class Circle(Shape):
            """
            Класс круга
            """
            def __init__(self, radius):
                super().__init__("круг")
                self.radius = radius
            
            def area(self):
                return math.pi * self.radius ** 2
            
            def perimeter(self):
                return 2 * math.pi * self.radius

        class Triangle(Shape):
            """
            Класс треугольника
            """
            def __init__(self, side1, side2, side3):
                super().__init__("треугольник")
                self.side1 = side1
                self.side2 = side2
                self.side3 = side3
                
                # Проверка, что это действительный треугольник
                if not self.is_valid_triangle():
                    raise ValueError("Стороны не образуют действительный треугольник")
            
            def is_valid_triangle(self):
                """
                Проверка, что стороны образуют действительный треугольник
                """
                return (self.side1 + self.side2 > self.side3 and 
                        self.side1 + self.side3 > self.side2 and 
                        self.side2 + self.side3 > self.side1)
            
            def area(self):
                # Используем формулу Герона
                s = self.perimeter() / 2  # Полупериметр
                return math.sqrt(s * (s - self.side1) * (s - self.side2) * (s - self.side3))
            
            def perimeter(self):
                return self.side1 + self.side2 + self.side3

        # Создание экземпляров
        shapes = [
            Rectangle(5, 3),
            Circle(4),
            Triangle(3, 4, 5)
        ]
        
        print("\n=== Иерархия классов геометрических фигур ===")
        for shape in shapes:
            print(shape.describe())
        
        # Вычисление общей площади
        total_area = sum(shape.area() for shape in shapes)
        print(f"\nОбщая площадь всех фигур: {total_area:.2f}")
        
        return shapes

    @staticmethod
    def create_bank_account_hierarchy():
        """
        Создание иерархии классов банковских счетов
        """
        class BankAccount(ABC):
            """
            Абстрактный класс банковского счета
            """
            def __init__(self, account_holder, balance=0):
                self.account_holder = account_holder
                self.balance = balance
                self.transaction_history = []
            
            @abstractmethod
            def withdraw(self, amount):
                pass
            
            @abstractmethod
            def deposit(self, amount):
                pass
            
            def get_balance(self):
                return self.balance
            
            def add_transaction(self, transaction_type, amount):
                import datetime
                self.transaction_history.append({
                    'type': transaction_type,
                    'amount': amount,
                    'timestamp': datetime.datetime.now(),
                    'balance_after': self.balance
                })

        class SavingsAccount(BankAccount):
            """
            Сберегательный счет
            """
            def __init__(self, account_holder, balance=0, interest_rate=0.05):
                super().__init__(account_holder, balance)
                self.interest_rate = interest_rate
            
            def withdraw(self, amount):
                if amount <= 0:
                    raise ValueError("Сумма должна быть положительной")
                
                if self.balance - amount < 0:
                    raise ValueError("Недостаточно средств для снятия")
                
                self.balance -= amount
                self.add_transaction("withdraw", amount)
                return self.balance
            
            def deposit(self, amount):
                if amount <= 0:
                    raise ValueError("Сумма должна быть положительной")
                
                self.balance += amount
                self.add_transaction("deposit", amount)
                return self.balance
            
            def calculate_interest(self):
                """
                Вычисление процентов для сберегательного счета
                """
                interest = self.balance * self.interest_rate
                self.balance += interest
                self.add_transaction("interest", interest)
                return interest

        class CheckingAccount(BankAccount):
            """
            Текущий счет
            """
            def __init__(self, account_holder, balance=0, overdraft_limit=1000):
                super().__init__(account_holder, balance)
                self.overdraft_limit = overdraft_limit
            
            def withdraw(self, amount):
                if amount <= 0:
                    raise ValueError("Сумма должна быть положительной")
                
                if self.balance - amount < -self.overdraft_limit:
                    raise ValueError("Превышен лимит овердрафта")
                
                self.balance -= amount
                self.add_transaction("withdraw", amount)
                return self.balance
            
            def deposit(self, amount):
                if amount <= 0:
                    raise ValueError("Сумма должна быть положительной")
                
                self.balance += amount
                self.add_transaction("deposit", amount)
                return self.balance

        class CreditAccount(BankAccount):
            """
            Кредитный счет
            """
            def __init__(self, account_holder, credit_limit=10000):
                super().__init__(account_holder, 0)  # Начальный баланс 0
                self.credit_limit = credit_limit
                self.credit_used = 0
            
            def withdraw(self, amount):
                if amount <= 0:
                    raise ValueError("Сумма должна быть положительной")
                
                if self.credit_used + amount > self.credit_limit:
                    raise ValueError("Превышено кредитное ограничение")
                
                self.credit_used += amount
                self.balance -= amount  # Баланс становится отрицательным
                self.add_transaction("credit_used", amount)
                return self.balance
            
            def deposit(self, amount):
                if amount <= 0:
                    raise ValueError("Сумма должна быть положительной")
                
                if amount > self.credit_used:
                    amount = self.credit_used  # Не можем вернуть больше, чем использовали
                
                self.credit_used -= amount
                self.balance += amount  # Баланс увеличивается (становится менее отрицательным)
                self.add_transaction("repayment", amount)
                return self.balance

        # Создание экземпляров
        accounts = [
            SavingsAccount("Иванов И.И.", 10000, 0.08),
            CheckingAccount("Петров П.П.", 5000, 2000),
            CreditAccount("Сидоров С.С.", 20000)
        ]
        
        print("\n=== Иерархия классов банковских счетов ===")
        for account in accounts:
            print(f"\n{type(account).__name__} для {account.account_holder}:")
            print(f"  Баланс: {account.get_balance():.2f}")
            
            if isinstance(account, SavingsAccount):
                interest = account.calculate_interest()
                print(f"  Начисленные проценты: {interest:.2f}")
                print(f"  Баланс после начисления процентов: {account.get_balance():.2f}")
            elif isinstance(account, CheckingAccount):
                print(f"  Лимит овердрафта: {account.overdraft_limit}")
            elif isinstance(account, CreditAccount):
                print(f"  Кредитный лимит: {account.credit_limit}")
                print(f"  Использовано кредита: {account.credit_used}")
            
            # Демонстрация операций
            try:
                account.deposit(1000)
                print(f"  Баланс после депозита: {account.get_balance():.2f}")
                
                account.withdraw(500)
                print(f"  Баланс после снятия: {account.get_balance():.2f}")
            except ValueError as e:
                print(f"  Ошибка: {e}")
        
        return accounts

    @staticmethod
    def demonstrate_super_usage():
        """
        Демонстрация использования super()
        """
        class Vehicle:
            """
            Базовый класс транспортного средства
            """
            def __init__(self, brand, model, year):
                self.brand = brand
                self.model = model
                self.year = year
                self.running = False
            
            def start(self):
                self.running = True
                return f"{self.brand} {self.model} запущен"
            
            def stop(self):
                self.running = False
                return f"{self.brand} {self.model} остановлен"
            
            def get_info(self):
                return f"{self.year} {self.brand} {self.model}"

        class Car(Vehicle):
            """
            Класс автомобиля
            """
            def __init__(self, brand, model, year, doors):
                super().__init__(brand, model, year)  # Вызов родительского конструктора
                self.doors = doors
            
            def start(self):
                # Расширение функциональности родительского метода
                parent_result = super().start()
                return f"{parent_result} с {self.doors} дверьми"
            
            def get_info(self):
                # Переопределение родительского метода с расширением
                parent_info = super().get_info()
                return f"{parent_info} ({self.doors} дверей)"

        class ElectricCar(Car):
            """
            Класс электромобиля
            """
            def __init__(self, brand, model, year, doors, battery_capacity):
                super().__init__(brand, model, year, doors)  # Вызов конструктора Car
                self.battery_capacity = battery_capacity  # Емкость батареи в кВт·ч
                self.charge_level = 100  # Уровень заряда в %
            
            def start(self):
                # Расширение функциональности родительского метода
                if self.charge_level < 5:
                    return "Недостаточно заряда для запуска"
                
                parent_result = super().start()
                return f"{parent_result} (уровень заряда: {self.charge_level}%)"
            
            def charge(self, amount):
                """
                Зарядка автомобиля
                """
                self.charge_level = min(100, self.charge_level + amount)
                return f"Заряжен на {amount}%, текущий уровень: {self.charge_level}%"
            
            def get_info(self):
                parent_info = super().get_info()
                return f"{parent_info}, батарея: {self.battery_capacity} кВт·ч"

        # Создание экземпляра
