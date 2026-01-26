# Практическое занятие 9: ООП - реализация классов

## Создание классов, атрибуты, методы, конструкторы

### Цель занятия:
Научиться создавать классы в Python, определять атрибуты и методы, использовать конструкторы и деструкторы.

### Задачи:
1. Создать классы с атрибутами и методами
2. Использовать конструкторы и деструкторы
3. Реализовать инкапсуляцию
4. Применить принципы ООП на практике

### План работы:
1. Создание простого класса
2. Определение атрибутов и методов
3. Использование конструктора и деструктора
4. Применение принципов инкапсуляции
5. Создание экземпляров класса
6. Практические задания

---

## 1. Создание простого класса

### Пример 1: Класс Person

```python
class Person:
    """
    Класс для представления человека
    """
    def __init__(self, name, age, email):
        """
        Конструктор класса Person
        
        Args:
            name (str): Имя человека
            age (int): Возраст человека
            email (str): Email человека
        """
        self.name = name
        self.age = age
        self.email = email
        self.created_at = __import__('datetime').datetime.now()
    
    def introduce(self):
        """
        Метод для представления человека
        """
        return f"Привет, меня зовут {self.name}, мне {self.age} лет"
    
    def is_adult(self):
        """
        Проверка, является ли человек совершеннолетним
        """
        return self.age >= 18
    
    def __str__(self):
        """
        Строковое представление объекта
        """
        return f"Person(name='{self.name}', age={self.age}, email='{self.email}')"

# Создание экземпляра класса
person1 = Person("Иван Иванов", 30, "ivan@example.com")
print(person1.introduce())  # Привет, меня зовут Иван Иванов, мне 30 лет
print(f"Совершеннолетний: {person1.is_adult()}")  # Совершеннолетний: True
print(person1)  # Person(name='Иван Иванов', age=30, email='ivan@example.com')
```

### Пример 2: Класс BankAccount

```python
class BankAccount:
    """
    Класс банковского счета
    """
    bank_name = "Тестовый банк"  # Атрибут класса
    
    def __init__(self, owner_name, initial_balance=0):
        """
        Конструктор банковского счета
        
        Args:
            owner_name (str): Имя владельца счета
            initial_balance (float): Начальный баланс
        """
        self.owner_name = owner_name  # Атрибут экземпляра
        self._balance = initial_balance  # Защищенный атрибут (инкапсуляция)
        self._transactions = []  # История транзакций
    
    def deposit(self, amount):
        """
        Внести деньги на счет
        
        Args:
            amount (float): Сумма для внесения
        """
        if amount <= 0:
            raise ValueError("Сумма внесения должна быть положительной")
        
        self._balance += amount
        self._transactions.append({
            "type": "deposit",
            "amount": amount,
            "timestamp": __import__('datetime').datetime.now()
        })
        return self._balance
    
    def withdraw(self, amount):
        """
        Снять деньги со счета
        
        Args:
            amount (float): Сумма для снятия
        """
        if amount <= 0:
            raise ValueError("Сумма снятия должна быть положительной")
        
        if amount > self._balance:
            raise ValueError("Недостаточно средств на счете")
        
        self._balance -= amount
        self._transactions.append({
            "type": "withdraw",
            "amount": -amount,
            "timestamp": __import__('datetime').datetime.now()
        })
        return self._balance
    
    def get_balance(self):
        """
        Получить баланс счета
        """
        return self._balance
    
    def get_transactions(self):
        """
        Получить историю транзакций
        """
        return self._transactions.copy()
    
    def __del__(self):
        """
        Деструктор класса
        """
        print(f"Счет для {self.owner_name} закрывается...")

# Пример использования
account = BankAccount("Иван Иванов", 1000)
print(f"Баланс: {account.get_balance()}")  # Баланс: 1000

account.deposit(500)
print(f"Баланс после внесения: {account.get_balance()}")  # Баланс после внесения: 1500

account.withdraw(200)
print(f"Баланс после снятия: {account.get_balance()}")  # Баланс после снятия: 1300
```

---

## 2. Атрибуты и методы класса

### Атрибуты экземпляра vs Атрибуты класса

```python
class Counter:
    """
    Класс для подсчета экземпляров
    """
    # Атрибут класса - общий для всех экземпляров
    total_instances = 0
    
    def __init__(self, name):
        self.name = name  # Атрибут экземпляра
        self.count = 0    # Атрибут экземпляра
        Counter.total_instances += 1  # Увеличиваем счетчик класса
    
    def increment(self):
        """
        Увеличение счетчика экземпляра
        """
        self.count += 1
        return self.count
    
    @classmethod
    def get_total_instances(cls):
        """
        Метод класса для получения общего количества экземпляров
        """
        return cls.total_instances
    
    @staticmethod
    def is_valid_name(name):
        """
        Статический метод для проверки имени
        """
        return isinstance(name, str) and len(name.strip()) > 0

# Пример использования
c1 = Counter("Первый")
c2 = Counter("Второй")
c3 = Counter("Третий")

print(f"Всего экземпляров: {Counter.get_total_instances()}")  # Всего экземпляров: 3
print(f"Счетчик c1: {c1.increment()}")  # Счетчик c1: 1
print(f"Счетчик c1: {c1.increment()}")  # Счетчик c1: 2
print(f"Счетчик c2: {c2.increment()}")  # Счетчик c2: 1

print(f"Имя c1 допустимо: {Counter.is_valid_name(c1.name)}")  # Имя c1 допустимо: True
print(f"Имя пустой строки допустимо: {Counter.is_valid_name('')}")  # Имя пустой строки допустимо: False
```

---

## 3. Инкапсуляция

### Уровни доступа в Python

```python
class Student:
    """
    Класс для представления студента
    """
    def __init__(self, name, student_id, gpa):
        self.name = name  # Публичный атрибут
        self._student_id = student_id  # Защищенный атрибут (соглашение)
        self.__gpa = gpa  # Приватный атрибут (сильное соглашение)
    
    # Методы для доступа к приватным атрибутам
    def get_gpa(self):
        return self.__gpa
    
    def set_gpa(self, gpa):
        if 0.0 <= gpa <= 5.0:
            self.__gpa = gpa
        else:
            raise ValueError("GPA должен быть между 0.0 и 5.0")
    
    # Использование property
    @property
    def gpa(self):
        """Свойство для получения GPA"""
        return self.__gpa
    
    @gpa.setter
    def gpa(self, value):
        """Свойство для установки GPA"""
        if not isinstance(value, (int, float)):
            raise TypeError("GPA должен быть числом")
        if not 0.0 <= value <= 5.0:
            raise ValueError("GPA должен быть между 0.0 и 5.0")
        self.__gpa = value
    
    @property
    def student_id(self):
        """Свойство для получения ID студента"""
        return self._student_id

# Пример использования
student = Student("Мария Петрова", "S12345", 4.5)

print(f"Имя: {student.name}")  # Публичный - доступен
print(f"ID: {student.student_id}")  # Защищенный - доступен через свойство
print(f"GPA: {student.gpa}")  # Приватный - доступен через свойство

# Изменение GPA
student.gpa = 4.8
print(f"Новый GPA: {student.gpa}")

# Попытка доступа к приватному атрибуту напрямую (не рекомендуется)
print(f"Прямой доступ к GPA: {student._Student__gpa}")  # Это работает, но не рекомендуется
```

---

## 4. Практические задания

### Задание 1: Класс Book

Создайте класс `Book` с атрибутами: название, автор, год издания, ISBN, количество страниц.
Реализуйте методы:
- `get_info()` - возвращает информацию о книге
- `is_new()` - проверяет, является ли книга новой (издана в последние 5 лет)
- `update_pages()` - обновляет количество страниц

```python
class Book:
    """
    Класс для представления книги
    """
    def __init__(self, title, author, year, isbn, pages):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def get_info(self):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def is_new(self):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def update_pages(self, new_pages):
        # ВАШ КОД ЗДЕСЬ
        pass

# Тестирование
book = Book("Python Programming", "John Doe", 2023, "978-0123456789", 450)
print(book.get_info())
print(f"Новая книга: {book.is_new()}")
```

### Задание 2: Класс Library

Создайте класс `Library`, который хранит список книг и предоставляет методы:
- `add_book(book)` - добавляет книгу в библиотеку
- `remove_book(isbn)` - удаляет книгу по ISBN
- `find_books_by_author(author)` - находит книги по автору
- `get_new_books()` - возвращает только новые книги

```python
class Library:
    """
    Класс для представления библиотеки
    """
    def __init__(self, name):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def add_book(self, book):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def remove_book(self, isbn):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def find_books_by_author(self, author):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def get_new_books(self):
        # ВАШ КОД ЗДЕСЬ
        pass
```

### Задание 3: Класс Car

Создайте класс `Car` с атрибутами: марка, модель, год выпуска, цвет, пробег.
Реализуйте методы:
- `start_engine()` - запускает двигатель
- `drive(distance)` - увеличивает пробег
- `paint(new_color)` - перекрашивает автомобиль
- `get_age()` - возвращает возраст автомобиля

```python
class Car:
    """
    Класс для представления автомобиля
    """
    def __init__(self, make, model, year, color, mileage=0):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def start_engine(self):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def drive(self, distance):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def paint(self, new_color):
        # ВАШ КОД ЗДЕСЬ
        pass
    
    def get_age(self):
        # ВАШ КОД ЗДЕСЬ
        pass

# Тестирование
car = Car("Toyota", "Camry", 2020, "Blue")
print(f"Возраст автомобиля: {car.get_age()} лет")
car.start_engine()
car.drive(150)
print(f"Новый пробег: {car.mileage}")
```

---

## 5. Дополнительные задания

### Задание 4: Класс для управления задачами

Создайте класс `TaskManager`, который позволяет:
- Добавлять задачи с описанием и приоритетом
- Отмечать задачи как выполненные
- Получать список активных задач
- Получать задачи по приоритету

### Задание 5: Класс для математических вычислений

Создайте класс `Calculator`, который реализует основные математические операции и хранит историю вычислений.

---

## Контрольные вопросы:
1. В чем разница между атрибутами класса и атрибутами экземпляра?
2. Какие уровни доступа к атрибутам существуют в Python?
3. Что такое конструктор и деструктор в Python?
4. Как использовать property в Python?
5. В чем преимущество инкапсуляции?
