# Практическое занятие 10: ООП - наследование и полиморфизм

## Наследование, переопределение методов, полиморфизм, абстрактные классы

### Цель занятия:
Научиться использовать наследование и полиморфизм в Python для создания иерархий классов и расширения функциональности.

### Задачи:
1. Создать классы с наследованием
2. Переопределять методы родительского класса
3. Применять полиморфизм
4. Использовать абстрактные классы
5. Реализовать иерархии классов

### План работы:
1. Основы наследования
2. Переопределение методов
3. Полиморфизм
4. Абстрактные классы
5. Практические задания

---

## 1. Основы наследования

### Пример 1: Базовый класс и наследование

```python
class Vehicle:
    """
    Базовый класс для транспортного средства
    """
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year
        self.is_running = False
    
    def start(self):
        """
        Запуск транспортного средства
        """
        self.is_running = True
        print(f"{self.brand} {self.model} запущен")
    
    def stop(self):
        """
        Остановка транспортного средства
        """
        self.is_running = False
        print(f"{self.brand} {self.model} остановлен")
    
    def get_info(self):
        """
        Получение информации о транспортном средстве
        """
        return f"{self.year} {self.brand} {self.model}"

class Car(Vehicle):
    """
    Класс для автомобиля - наследуется от Vehicle
    """
    def __init__(self, brand, model, year, doors=4):
        super().__init__(brand, model, year)  # Вызов конструктора родительского класса
        self.doors = doors
        self.type = "Автомобиль"
    
    def honk(self):
        """
        Сигнал автомобиля
        """
        print("Бип-бип!")

class Motorcycle(Vehicle):
    """
    Класс для мотоцикла - наследуется от Vehicle
    """
    def __init__(self, brand, model, year, engine_capacity):
        super().__init__(brand, model, year)
        self.engine_capacity = engine_capacity
        self.type = "Мотоцикл"
    
    def wheelie(self):
        """
        Мотоцикл делает вилли
        """
        if self.is_running:
            print("Мотоцикл делает вилли!")
        else:
            print("Сначала запустите двигатель")

# Пример использования
car = Car("Toyota", "Camry", 2022, 4)
motorcycle = Motorcycle("Honda", "CBR", 2023, 600)

print(car.get_info())  # 2022 Toyota Camry
print(motorcycle.get_info())  # 2023 Honda CBR

car.start()
car.honk()

motorcycle.start()
motorcycle.wheelie()
```

### Пример 2: Множественное наследование

```python
class Flyable:
    """
    Класс, представляющий возможность полета
    """
    def __init__(self, max_altitude=10000):
        self.max_altitude = max_altitude
        self.current_altitude = 0
    
    def take_off(self):
        print("Поднимаюсь в воздух...")
        self.current_altitude = 1000
    
    def land(self):
        print("Приземляюсь...")
        self.current_altitude = 0
    
    def fly(self, altitude):
        if 0 <= altitude <= self.max_altitude:
            self.current_altitude = altitude
            print(f"Лечу на высоте {altitude} метров")
        else:
            print(f"Невозможно лететь на высоте {altitude} метров")

class Swimmable:
    """
    Класс, представляющий возможность плавания
    """
    def __init__(self, max_depth=10):
        self.max_depth = max_depth
        self.current_depth = 0
    
    def dive(self, depth):
        if 0 <= depth <= self.max_depth:
            self.current_depth = depth
            print(f"Погружаюсь на глубину {depth} метров")
        else:
            print(f"Невозможно погрузиться на глубину {depth} метров")
    
    def surface(self):
        print("Выхожу на поверхность...")
        self.current_depth = 0

class AmphibiousVehicle(Vehicle, Flyable, Swimmable):
    """
    Амфибийное транспортное средство - наследуется от Vehicle, Flyable и Swimmable
    """
    def __init__(self, brand, model, year, doors=4, max_altitude=1000, max_depth=5):
        Vehicle.__init__(self, brand, model, year)
        Flyable.__init__(self, max_altitude)
        Swimmable.__init__(self, max_depth)
        self.type = "Амфибийное ТС"
    
    def get_info(self):
        """
        Переопределение метода родительского класса
        """
        base_info = super().get_info()  # Вызов метода из Vehicle
        return f"{base_info} (Амфибийное ТС с {self.doors} дверьми)"

# Пример использования
amphibious = AmphibiousVehicle("AmphiCorp", "AquaticFlyer", 2023, 2, 500, 3)

print(amphibious.get_info())
amphibious.start()
amphibious.take_off()
amphibious.fly(500)
amphibious.land()
amphibious.dive(2)
amphibious.surface()
```

---

## 2. Переопределение методов

### Пример 3: Переопределение методов и использование super()

```python
class Animal:
    """
    Базовый класс для животных
    """
    def __init__(self, name, species):
        self.name = name
        self.species = species
    
    def make_sound(self):
        """
        Создание звука (будет переопределен в дочерних классах)
        """
        return f"{self.name} издает звук"
    
    def move(self):
        """
        Перемещение животного
        """
        return f"{self.name} двигается"
    
    def info(self):
        """
        Информация о животном
        """
        return f"{self.name} - {self.species}"

class Dog(Animal):
    """
    Класс для собаки
    """
    def __init__(self, name, breed):
        super().__init__(name, "Собака")
        self.breed = breed
    
    def make_sound(self):
        # Переопределение метода
        return f"{self.name} говорит: Гав!"
    
    def move(self):
        # Переопределение метода с дополнительной функциональностью
        base_movement = super().move()  # Вызов родительского метода
        return f"{base_movement} и бегает на четырех лапах"
    
    def fetch(self):
        """
        Метод, специфичный для собаки
        """
        return f"{self.name} приносит палку"
    
    def info(self):
        # Переопределение метода с расширением
        base_info = super().info()
        return f"{base_info}, порода: {self.breed}"

class Cat(Animal):
    """
    Класс для кошки
    """
    def __init__(self, name, fur_color):
        super().__init__(name, "Кошка")
        self.fur_color = fur_color
    
    def make_sound(self):
        return f"{self.name} говорит: Мяу!"
    
    def move(self):
        return f"{self.name} двигается осторожно на мягких лапках"
    
    def purr(self):
        """
        Мурлыканье кошки
        """
        return f"{self.name} мурлычет"
    
    def info(self):
        base_info = super().info()
        return f"{base_info}, цвет шерсти: {self.fur_color}"

class Bird(Animal):
    """
    Класс для птицы
    """
    def __init__(self, name, wingspan):
        super().__init__(name, "Птица")
        self.wingspan = wingspan  # Размах крыльев
    
    def make_sound(self):
        return f"{self.name} поет: Чирик!"
    
    def move(self):
        return f"{self.name} летает с размахом крыльев {self.wingspan} см"
    
    def fly(self):
        """
        Метод полета для птицы
        """
        return f"{self.name} взлетает в небо"
    
    def info(self):
        base_info = super().info()
        return f"{base_info}, размах крыльев: {self.wingspan} см"

# Пример использования
animals = [
    Dog("Бобик", "Лабрадор"),
    Cat("Мурка", "Рыжая"),
    Bird("Кеша", 30)
]

for animal in animals:
    print(animal.info())
    print(animal.make_sound())
    print(animal.move())
    print()
```

---

## 3. Полиморфизм

### Пример 4: Полиморфизм в действии

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    """
    Абстрактный класс для геометрических фигур
    """
    @abstractmethod
    def area(self):
        """
        Вычисление площади фигуры
        """
        pass
    
    @abstractmethod
    def perimeter(self):
        """
        Вычисление периметра фигуры
        """
        pass
    
    def describe(self):
        """
        Общее описание фигуры
        """
        return f"Это {self.__class__.__name__} с площадью {self.area():.2f} и периметром {self.perimeter():.2f}"

class Rectangle(Shape):
    """
    Класс прямоугольника
    """
    def __init__(self, width, height):
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
        self.radius = radius
    
    def area(self):
        return 3.14159 * self.radius ** 2
    
    def perimeter(self):
        return 2 * 3.14159 * self.radius

class Triangle(Shape):
    """
    Класс треугольника
    """
    def __init__(self, side1, side2, side3):
        self.side1 = side1
        self.side2 = side2
        self.side3 = side3
        
        # Проверка, что это действительный треугольник
        if not self.is_valid_triangle():
            raise ValueError("Неверные стороны для треугольника")
    
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
        return (s * (s - self.side1) * (s - self.side2) * (s - self.side3)) ** 0.5
    
    def perimeter(self):
        return self.side1 + self.side2 + self.side3

def print_shapes_info(shapes):
    """
    Функция, демонстрирующая полиморфизм
    Принимает список фигур и выводит информацию о каждой
    """
    for shape in shapes:
        print(shape.describe())
        print()

# Пример использования
shapes = [
    Rectangle(5, 3),
    Circle(4),
    Triangle(3, 4, 5)
]

print_shapes_info(shapes)

# Функция для вычисления общей площади
def calculate_total_area(shapes):
    """
    Вычисление общей площади всех фигур
    """
    total = 0
    for shape in shapes:
        total += shape.area()
    return total

total_area = calculate_total_area(shapes)
print(f"Общая площадь: {total_area:.2f}")
```

---

## 4. Абстрактные классы

### Пример 5: Использование абстрактных классов

```python
from abc import ABC, abstractmethod

class Employee(ABC):
    """
    Абстрактный класс для сотрудника
    """
    def __init__(self, name, employee_id):
        self.name = name
        self.employee_id = employee_id
    
    @abstractmethod
    def calculate_salary(self):
        """
        Вычисление зарплаты (должен быть реализован в дочернем классе)
        """
        pass
    
    @abstractmethod
    def get_role(self):
        """
        Получение роли сотрудника (должен быть реализован в дочернем классе)
        """
        pass
    
    def get_info(self):
        """
        Общая информация о сотруднике
        """
        return f"ID: {self.employee_id}, Имя: {self.name}, Роль: {self.get_role()}"

class Developer(Employee):
    """
    Класс разработчика
    """
    def __init__(self, name, employee_id, hourly_rate, hours_worked):
        super().__init__(name, employee_id)
        self.hourly_rate = hourly_rate
        self.hours_worked = hours_worked
    
    def calculate_salary(self):
        return self.hourly_rate * self.hours_worked
    
    def get_role(self):
        return "Разработчик"
    
    def write_code(self):
        return f"{self.name} пишет код"

class Manager(Employee):
    """
    Класс менеджера
    """
    def __init__(self, name, employee_id, monthly_salary, bonus_percentage=0):
        super().__init__(name, employee_id)
        self.monthly_salary = monthly_salary
        self.bonus_percentage = bonus_percentage
    
    def calculate_salary(self):
        bonus = self.monthly_salary * (self.bonus_percentage / 100)
        return self.monthly_salary + bonus
    
    def get_role(self):
        return "Менеджер"
    
    def manage_team(self):
        return f"{self.name} управляет командой"

class SalesPerson(Employee):
    """
    Класс продавца
    """
    def __init__(self, name, employee_id, base_salary, commission_rate, sales_amount):
        super().__init__(name, employee_id)
        self.base_salary = base_salary
        self.commission_rate = commission_rate
        self.sales_amount = sales_amount
    
    def calculate_salary(self):
        commission = self.sales_amount * (self.commission_rate / 100)
        return self.base_salary + commission
    
    def get_role(self):
        return "Продавец"
    
    def make_sale(self):
        return f"{self.name} совершает продажу на {self.sales_amount} руб."

def process_employees(employees):
    """
    Функция для обработки списка сотрудников (демонстрация полиморфизма)
    """
    total_salaries = 0
    for employee in employees:
        print(employee.get_info())
        salary = employee.calculate_salary()
        print(f"Зарплата: {salary:.2f} руб.")
        total_salaries += salary
        print()
    
    print(f"Общая зарплата: {total_salaries:.2f} руб.")

# Пример использования
employees = [
    Developer("Иван Иванов", "DEV001", 1000, 160),  # 1000 руб/час * 160 часов
    Manager("Мария Петрова", "MGR001", 80000, 10),  # 80000 + 10% бонуса
    SalesPerson("Алексей Сидоров", "SALES001", 30000, 5, 500000)  # 30000 + 5% от 500000
]

process_employees(employees)
```

---

## 5. Практические задания

### Задание 1: Классы для банковских счетов

Создайте иерархию классов для банковских счетов:
- `BaseAccount` (абстрактный класс)
- `SavingsAccount` (сберегательный счет)
- `CheckingAccount` (текущий счет)
- `CreditAccount` (кредитный счет)

Каждый класс должен реализовать методы:
- `deposit(amount)` - внести деньги
- `withdraw(amount)` - снять деньги
- `get_balance()` - получить баланс
- `calculate_interest()` - вычислить проценты (для сберегательного счета)

```python
from abc import ABC, abstractmethod

class BaseAccount(ABC):
    """
    Абстрактный базовый класс для банковского счета
    """
    def __init__(self, account_holder, initial_balance=0):
        self.account_holder = account_holder
        self.balance = initial_balance
    
    @abstractmethod
    def deposit(self, amount):
        """
        Внести деньги на счет
        """
        pass
    
    @abstractmethod
    def withdraw(self, amount):
        """
        Снять деньги со счета
        """
        pass
    
    @abstractmethod
    def calculate_interest(self):
        """
        Вычислить проценты (для сберегательного счета)
        """
        pass

class SavingsAccount(BaseAccount):
    """
    Сберегательный счет
    """
    def __init__(self, account_holder, initial_balance=0, interest_rate=0.05):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def deposit(self, amount):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def withdraw(self, amount):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def calculate_interest(self):
        # ВАШ КОД ЗДЕСЬ
        pass

class CheckingAccount(BaseAccount):
    """
    Текущий счет
    """
    def __init__(self, account_holder, initial_balance=0, overdraft_limit=1000):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def deposit(self, amount):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def withdraw(self, amount):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def calculate_interest(self):
        # Сберегательные счета не начисляют проценты
        return 0

class CreditAccount(BaseAccount):
    """
    Кредитный счет
    """
    def __init__(self, account_holder, credit_limit=10000):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def deposit(self, amount):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def withdraw(self, amount):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def calculate_interest(self):
        # ВАШ КОД ЗДЕСЬ
        pass

# Тестирование
savings = SavingsAccount("Иванов И.И.", 10000, 0.08)
checking = CheckingAccount("Петров П.П.", 5000, 2000)
credit = CreditAccount("Сидоров С.С.", 20000)

accounts = [savings, checking, credit]
for account in accounts:
    print(f"{account.account_holder}: {account.get_balance():.2f} руб.")
    account.deposit(1000)
    print(f"После депозита: {account.get_balance():.2f} руб.")
    print()
```

### Задание 2: Иерархия пользователей

Создайте иерархию классов для пользователей системы:
- `User` (базовый класс)
- `AdminUser` (администратор)
- `RegularUser` (обычный пользователь)
- `PremiumUser` (премиум пользователь)

Каждый класс должен реализовать свои методы и атрибуты.

```python
class User:
    """
    Базовый класс пользователя
    """
    def __init__(self, username, email):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def login(self):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def logout(self):
        # ВАШ КОД ЗДЕСЬ
        pass

class AdminUser(User):
    """
    Администратор системы
    """
    def __init__(self, username, email):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def create_user(self, username, email):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def delete_user(self, user):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def access_admin_panel(self):
        # ВАШ КОД ЗДЕСЬ
        pass

class RegularUser(User):
    """
    Обычный пользователь
    """
    def __init__(self, username, email):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def upload_file(self, file_path):
        # ВАШ КОД ЗДЕСЬ
        pass

class PremiumUser(RegularUser):
    """
    Премиум пользователь
    """
    def __init__(self, username, email):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def get_additional_features(self):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def increase_storage(self, additional_gb):
        # ВАШ КОД ЗДЕСЬ
        pass

# Тестирование
admin = AdminUser("admin", "admin@example.com")
regular = RegularUser("user1", "user1@example.com")
premium = PremiumUser("premium_user", "premium@example.com")

users = [admin, regular, premium]
for user in users:
    user.login()
    print(f"Пользователь: {user.username}, роль: {type(user).__name__}")
    user.logout()
    print()
```

### Задание 3: Система управления документами

Создайте иерархию классов для документов:
- `Document` (абстрактный класс)
- `TextDocument`
- `SpreadsheetDocument`
- `PresentationDocument`

Каждый класс должен реализовать методы:
- `open()`
- `save()`
- `close()`
- `get_type()`

```python
from abc import ABC, abstractmethod

class Document(ABC):
    """
    Абстрактный класс для документа
    """
    def __init__(self, title, author):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    @abstractmethod
    def open(self):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    @abstractmethod
    def save(self):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    @abstractmethod
    def close(self):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    @abstractmethod
    def get_type(self):
        # ВАШ КОД ЗДЕСЬ
        pass

class TextDocument(Document):
    """
    Текстовый документ
    """
    def __init__(self, title, author, content=""):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def open(self):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def save(self):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def close(self):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def get_type(self):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def add_text(self, text):
        # ВАШ КОД ЗДЕСЬ
        pass

class SpreadsheetDocument(Document):
    """
    Табличный документ
    """
    def __init__(self, title, author):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def open(self):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def save(self):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def close(self):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def get_type(self):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def add_row(self, row_data):
        # ВАШ КОД ЗДЕСЬ
        pass

class PresentationDocument(Document):
    """
    Презентационный документ
    """
    def __init__(self, title, author):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def open(self):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def save(self):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def close(self):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def get_type(self):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def add_slide(self, slide_content):
        # ВАШ КОД ЗДЕСЬ
        pass

# Тестирование
documents = [
    TextDocument("Отчет", "Иванов И.И.", "Содержимое отчета"),
    SpreadsheetDocument("Бюджет", "Петров П.П."),
    PresentationDocument("Презентация", "Сидоров С.С.")
]

for doc in documents:
    print(f"Открываем {doc.get_type()}: {doc.title}")
    doc.open()
    print(f"Закрываем {doc.get_type()}")
    doc.close()
    print()
```

---

## 6. Дополнительные задания

### Задание 4: Игровая система

Создайте иерархию классов для игровых персонажей:
- `Character` (абстрактный класс)
- `Warrior`
- `Mage`
- `Archer`

### Задание 5: Система геометрических фигур

Расширьте пример с геометрическими фигурами, добавив:
- `Square` (квадрат)
- `Ellipse` (эллипс)
- `Polygon` (многоугольник)

---

## Контрольные вопросы:
1. В чем разница между наследованием и композицией?
2. Что такое полиморфизм и как он реализуется в Python?
3. Как использовать ключевое слово super()?
4. Что такое абстрактный класс и зачем он нужен?
5. Как реализовать множественное наследование?
