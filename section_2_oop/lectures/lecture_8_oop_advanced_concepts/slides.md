# Лекция 8: ООП - продвинутые концепции

## Наследование, полиморфизм, инкапсуляция, абстрактные классы, магические методы

### План лекции:
1. Продвинутые аспекты наследования
2. Полиморфизм в Python
3. Инкапсуляция и уровни доступа
4. Абстрактные классы
5. Магические методы (dunder-методы)
6. Практические примеры

---

## 1. Продвинутые аспекты наследования

### Множественное наследование

В Python класс может наследоваться от нескольких родительских классов:

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        pass

class Mammal:
    def __init__(self, warm_blooded=True):
        self.warm_blooded = warm_blooded

    def give_birth(self):
        return "рождает живых детенышей"

class Dog(Animal, Mammal):
    def __init__(self, name, breed):
        Animal.__init__(self, name)
        Mammal.__init__(self)
        self.breed = breed

    def speak(self):
        return f"{self.name} говорит: Гав!"

# Пример использования
dog = Dog("Бобик", "Лабрадор")
print(dog.speak())  # Бобик говорит: Гав!
print(dog.give_birth())  # рождает живых детенышей
```

### MRO (Method Resolution Order)

Python использует алгоритм C3 linearization для определения порядка разрешения методов:

```python
class A:
    def method(self):
        print("A.method")

class B(A):
    def method(self):
        print("B.method")

class C(A):
    def method(self):
        print("C.method")

class D(B, C):
    pass

# Проверка порядка разрешения методов
print(D.__mro__)
# (<class '__main__.D'>, <class '__main__.B'>, <class '__main__.C'>, <class '__main__.A'>, <class 'object'>)

d = D()
d.method()  # Выведет: B.method
```

### super() и его использование

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)

    def area(self):
        print("Вычисление площади квадрата")
        return super().area()

square = Square(5)
print(square.area())  # Вычисление площади квадрата \n 25
```

---

## 2. Полиморфизм в Python

### Понятие полиморфизма

Полиморфизм позволяет использовать объекты разных классов через общий интерфейс:

```python
class Shape:
    def area(self):
        pass

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def area(self):
        return 0.5 * self.base * self.height

# Полиморфное использование
shapes = [Circle(5), Rectangle(4, 6), Triangle(3, 8)]

for shape in shapes:
    print(f"Площадь: {shape.area():.2f}")
```

### Duck Typing

В Python используется концепция "утиной типизации":

```python
class Duck:
    def quack(self):
        print("Кря!")

    def fly(self):
        print("Утка летит")

class Airplane:
    def quack(self):
        print("Вжжж!")

    def fly(self):
        print("Самолет летит")

class Whale:
    def quack(self):
        print("Уииии!")

def make_it_fly(thing):
    thing.quack()
    thing.fly()

# Все эти объекты могут "летать" с точки зрения нашей функции
duck = Duck()
airplane = Airplane()
whale = Whale()

make_it_fly(duck)      # Кря! \n Утка летит
make_it_fly(airplane)  # Вжжж! \n Самолет летит
make_it_fly(whale)     # Уииии! \n Уииии!
```

---

## 3. Инкапсуляция и уровни доступа

### Уровни доступа в Python

```python
class BankAccount:
    def __init__(self, initial_balance=0):
        self.public_balance = initial_balance      # Публичный атрибут
        self._protected_pin = "1234"              # Защищенный атрибут (соглашение)
        self.__private_account_number = "1234567890"  # Приватный атрибут (сильное соглашение)

    def get_account_info(self):
        return f"Баланс: {self.public_balance}, PIN: {self._protected_pin}, Номер: {self.__private_account_number}"

    def _internal_operation(self):
        # Защищенный метод
        return "Внутренняя операция"

    def __critical_operation(self):
        # Приватный метод
        return "Критическая операция"

account = BankAccount(1000)
print(account.public_balance)  # 1000
print(account._protected_pin)  # 1234 (работает, но не рекомендуется)
# print(account.__private_account_number)  # Ошибка AttributeError
print(account._BankAccount__private_account_number)  # 1234567890 (через name mangling)
```

### Свойства (properties)

```python
class Temperature:
    def __init__(self, celsius=0):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Температура не может быть ниже абсолютного нуля")
        self._celsius = value

    @property
    def fahrenheit(self):
        return self._celsius * 9/5 + 32

    @fahrenheit.setter
    def fahrenheit(self, value):
        self.celsius = (value - 32) * 5/9

temp = Temperature()
temp.celsius = 25
print(temp.celsius)     # 25
print(temp.fahrenheit)  # 77.0

temp.fahrenheit = 100
print(temp.celsius)     # 37.7777777778
```

---

## 4. Абстрактные классы

### Создание абстрактных классов

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def make_sound(self):
        pass

    @abstractmethod
    def move(self):
        pass

    def sleep(self):
        # Конкретный метод
        print(f"{self.name} спит")

class Dog(Animal):
    def make_sound(self):
        return f"{self.name} говорит: Гав!"

    def move(self):
        return f"{self.name} бегает"

class Bird(Animal):
    def make_sound(self):
        return f"{self.name} поёт: Чирик!"

    def move(self):
        return f"{self.name} летает"

# animal = Animal("Generic")  # Ошибка: нельзя создать экземпляр абстрактного класса

dog = Dog("Шарик")
bird = Bird("Чижик")

print(dog.make_sound())  # Шарик говорит: Гав!
print(bird.make_sound()) # Чижик поёт: Чирик!

dog.sleep()  # Шарик спит
bird.sleep() # Чижик спит
```

---

## 5. Магические методы (dunder-методы)

### Основные магические методы

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __abs__(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

    def __bool__(self):
        return bool(abs(self))

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise IndexError("Индекс вне диапазона")

    def __len__(self):
        return 2  # Вектор всегда 2D

# Пример использования
v1 = Vector(2, 4)
v2 = Vector(3, 6)

print(v1)           # (2, 4)
print(repr(v1))     # Vector(2, 4)
print(v1 + v2)      # (5, 10)
print(v1 * 3)       # (6, 12)
print(abs(v1))      # 4.47213595499958
print(v1[0], v1[1]) # 2 4
print(len(v1))      # 2
```

### Контекстный менеджер

```python
class ManagedFile:
    def __init__(self, filename):
        self.filename = filename

    def __enter__(self):
        print(f"Открытие файла {self.filename}")
        self.file = open(self.filename, 'w')
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"Закрытие файла {self.filename}")
        if self.file:
            self.file.close()

# Использование контекстного менеджера
with ManagedFile('hello.txt') as f:
    f.write('Привет, мир!')
    print("Запись выполнена")
# Файл автоматически закрывается
```

---

## 6. Практические примеры

### Пример: Иерархия пользователей системы

```python
from abc import ABC, abstractmethod
from datetime import datetime

class User(ABC):
    def __init__(self, username, email):
        self.username = username
        self.email = email
        self.created_at = datetime.now()

    @abstractmethod
    def get_access_level(self):
        pass

    def __str__(self):
        return f"Пользователь: {self.username} ({self.email})"

class RegularUser(User):
    def get_access_level(self):
        return "Обычный"

    def view_content(self):
        return "Просмотр контента разрешен"

class PremiumUser(RegularUser):
    def get_access_level(self):
        return "Премиум"

    def view_content(self):
        return "Просмотр всего контента разрешен"

    def download_content(self):
        return "Загрузка контента разрешена"

class AdminUser(User):
    def get_access_level(self):
        return "Администратор"

    def manage_users(self):
        return "Управление пользователями разрешено"

    def access_system_logs(self):
        return "Доступ к системным логам разрешен"

# Создание пользователей
users = [
    RegularUser("ivan", "ivan@example.com"),
    PremiumUser("maria", "maria@example.com"),
    AdminUser("admin", "admin@example.com")
]

for user in users:
    print(f"{user} - Уровень доступа: {user.get_access_level()}")
```

---

## Заключение

Продвинутые концепции ООП в Python позволяют создавать гибкие и масштабируемые архитектуры приложений. Понимание наследования, полиморфизма, инкапсуляции, абстрактных классов и магических методов критически важно для разработки качественного кода.

## Контрольные вопросы:
1. Как работает множественное наследование в Python?
2. Что такое MRO и как его можно проверить?
3. Какие уровни доступа к атрибутам существуют в Python?
4. Что такое абстрактные классы и для чего они используются?
5. Какие магические методы вы знаете и для чего они применяются?
