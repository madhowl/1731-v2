# Упражнения для практического занятия 10: ООП - наследование и полиморфизм

"""
Этот файл содержит упражнения для закрепления понимания наследования и полиморфизма в Python.
"""

from abc import ABC, abstractmethod
import math

# Упражнение 1: Создание иерархии классов животных
class Animal(ABC):
    """
    Абстрактный базовый класс для животных
    """
    def __init__(self, name, species):
        self.name = name
        self.species = species
    
    @abstractmethod
    def make_sound(self):
        """
        Абстрактный метод для издавания звука
        """
        pass
    
    @abstractmethod
    def move(self):
        """
        Абстрактный метод для перемещения
        """
        pass
    
    def eat(self):
        """
        Общий метод для всех животных
        """
        return f"{self.name} ест"
    
    def sleep(self):
        """
        Общий метод для всех животных
        """
        return f"{self.name} спит"

class Mammal(Animal):
    """
    Класс млекопитающих
    """
    def __init__(self, name, species, fur_color):
        super().__init__(name, species)
        self.fur_color = fur_color
    
    def give_birth(self):
        """
        Метод, характерный для млекопитающих
        """
        return f"{self.name} родила детенышей"
    
    def feed_milk(self):
        """
        Метод, характерный для млекопитающих
        """
        return f"{self.name} кормит молоком"

class Bird(Animal):
    """
    Класс птиц
    """
    def __init__(self, name, species, wing_span):
        super().__init__(name, species)
        self.wing_span = wing_span  # Размах крыльев в см
    
    def lay_eggs(self):
        """
        Метод, характерный для птиц
        """
        return f"{self.name} отложила яйца"
    
    def fly(self):
        """
        Метод, характерный для птиц
        """
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

def exercise_1_solution():
    """
    Решение упражнения 1: Демонстрация наследования и полиморфизма
    """
    print("=== Упражнение 1: Иерархия классов животных ===")
    
    # Создание экземпляров
    dog = Dog("Бобик", "Лабрадор", "коричневый")
    cat = Cat("Мурка", "Сиамская", "белый")
    eagle = Eagle("Гром", 200)
    
    animals = [dog, cat, eagle]
    
    for animal in animals:
        print(f"\n{animal.name} ({animal.species}):")
        print(f"  Звук: {animal.make_sound()}")
        print(f"  Движение: {animal.move()}")
        print(f"  Еда: {animal.eat()}")
        print(f"  Сон: {animal.sleep()}")
        
        # Дополнительные методы в зависимости от типа
        if isinstance(animal, Mammal):
            print(f"  Цвет шерсти: {animal.fur_color}")
            print(f"  Рождение: {animal.give_birth()}")
            print(f"  Кормление молоком: {animal.feed_milk()}")
        elif isinstance(animal, Bird):
            print(f"  Размах крыльев: {animal.wing_span} см")
            print(f"  Полет: {animal.fly()}")
            print(f"  Откладывание яиц: {animal.lay_eggs()}")
        
        # Методы специфичные для подклассов
        if isinstance(animal, Dog):
            print(f"  Принесла палку: {animal.fetch()}")
        elif isinstance(animal, Cat):
            print(f"  Мурлычет: {animal.purr()}")
        elif isinstance(animal, Eagle):
            print(f"  Охота: {animal.hunt()}")

# Упражнение 2: Создание классов для геометрических фигур
class Shape(ABC):
    """
    Абстрактный класс для геометрических фигур
    """
    def __init__(self, name):
        self.name = name
    
    @abstractmethod
    def area(self):
        """
        Абстрактный метод для вычисления площади
        """
        pass
    
    @abstractmethod
    def perimeter(self):
        """
        Абстрактный метод для вычисления периметра
        """
        pass
    
    def describe(self):
        """
        Общий метод описания фигуры
        """
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

def exercise_2_solution():
    """
    Решение упражнения 2: Демонстрация полиморфизма с геометрическими фигурами
    """
    print("\n=== Упражнение 2: Геометрические фигуры ===")
    
    shapes = [
        Rectangle(5, 3),
        Circle(4),
        Triangle(3, 4, 5)
    ]
    
    for shape in shapes:
        print(shape.describe())
    
    # Вычисление общей площади
    total_area = sum(shape.area() for shape in shapes)
    print(f"\nОбщая площадь всех фигур: {total_area:.2f}")

# Упражнение 3: Классы для банковских счетов
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
        """
        Абстрактный метод снятия денег
        """
        pass
    
    @abstractmethod
    def deposit(self, amount):
        """
        Абстрактный метод внесения денег
        """
        pass
    
    def get_balance(self):
        """
        Общий метод получения баланса
        """
        return self.balance
    
    def add_transaction(self, transaction_type, amount):
        """
        Добавление транзакции в историю
        """
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

def exercise_3_solution():
    """
    Решение упражнения 3: Демонстрация наследования с банковскими счетами
    """
    print("\n=== Упражнение 3: Банковские счета ===")
    
    accounts = [
        SavingsAccount("Иванов И.И.", 10000, 0.08),
        CheckingAccount("Петров П.П.", 5000, 2000),
        CreditAccount("Сидоров С.С.", 20000)
    ]
    
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

# Упражнение 4: Практика с super()
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

def exercise_4_solution():
    """
    Решение упражнения 4: Практика с super()
    """
    print("\n=== Упражнение 4: Практика с super() ===")
    
    electric_car = ElectricCar("Tesla", "Model S", 2023, 4, 100)
    
    print(electric_car.get_info())
    print(electric_car.start())
    
    # Разрядка и повторный запуск
    electric_car.charge_level = 2
    print(electric_car.start())  # Недостаточно заряда
    
    print(electric_car.charge(50))
    print(electric_car.start())  # Теперь запустится

# Упражнение 5: Множественное наследование
class Flyable:
    """
    Класс для объектов, которые могут летать
    """
    def __init__(self):
        self.altitude = 0  # Высота
    
    def take_off(self):
        self.altitude = 1000
        return "Взлет выполнен"
    
    def land(self):
        self.altitude = 0
        return "Посадка выполнена"
    
    def fly(self, altitude):
        if 0 <= altitude <= 10000:
            self.altitude = altitude
            return f"Летит на высоте {altitude} м"
        else:
            return "Невозможная высота для полета"

class Swimmable:
    """
    Класс для объектов, которые могут плавать
    """
    def __init__(self):
        self.depth = 0  # Глубина
    
    def dive(self, depth):
        if 0 <= depth <= 100:
            self.depth = depth
            return f"Погрузился на глубину {depth} м"
        else:
            return "Невозможная глубина для погружения"
    
    def surface(self):
        self.depth = 0
        return "Вышел на поверхность"
    
    def swim(self):
        return "Плавает в воде"

class AmphibiousVehicle(Car, Flyable, Swimmable):
    """
    Амфибийное транспортное средство - наследуется от Car, Flyable и Swimmable
    """
    def __init__(self, brand, model, year, doors, battery_capacity):
        Car.__init__(self, brand, model, year, doors)
        Flyable.__init__(self)
        Swimmable.__init__(self)
        self.battery_capacity = battery_capacity
        self.mode = "ground"  # ground, air, water
    
    def change_mode(self, new_mode):
        """
        Смена режима работы транспортного средства
        """
        if new_mode in ["ground", "air", "water"]:
            self.mode = new_mode
            return f"Режим изменен на {new_mode}"
        else:
            return "Неверный режим"
    
    def move(self):
        """
        Перемещение в зависимости от режима
        """
        if self.mode == "ground":
            return self.start()  # Используем метод из Car
        elif self.mode == "air":
            return self.take_off()  # Используем метод из Flyable
        elif self.mode == "water":
            return self.swim()  # Используем метод из Swimmable
        else:
            return "Неизвестный режим"

def exercise_5_solution():
    """
    Решение упражнения 5: Множественное наследование
    """
    print("\n=== Упражнение 5: Множественное наследование ===")
    
    amphibious = AmphibiousVehicle("FutureTech", "AquaFlyer", 2024, 2, 150)
    
    print(amphibious.get_info())
    print(amphibious.change_mode("air"))
    print(amphibious.fly(5000))
    print(f"Высота: {amphibious.altitude} м")
    
    print(amphibious.change_mode("water"))
    print(amphibious.dive(10))
    print(f"Глубина: {amphibious.depth} м")
    
    print(amphibious.change_mode("ground"))
    print(amphibious.start())

def run_all_exercises():
    """
    Запуск всех упражнений
    """
    print("Решения упражнений по ООП: наследование и полиморфизм")
    print("="*60)
    
    exercise_1_solution()
    exercise_2_solution()
    exercise_3_solution()
    exercise_4_solution()
    exercise_5_solution()
    
    print("\n" + "="*60)
    print("Все упражнения выполнены!")

if __name__ == "__main__":
    run_all_exercises()
